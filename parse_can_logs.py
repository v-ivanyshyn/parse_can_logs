import matplotlib.pyplot as plt
import matplotlib.collections as plt_collections
import csv

csvFilaPath = 'log.csv'
frameId = '0x540'  # CAN ID to analyze


class FrameStream:
    def __init__(self):
        self.timeStream = []
        self.bytesStream = []  # array of [8]
        self.constTimestamps = []  # array of [8](start, end) tuples


frames = dict()

with open(csvFilaPath, 'r') as file:
    rows = csv.reader(file, delimiter=',')
    for row in rows:
        if len(row) < 3:
            print 'incorrect row:', row
            continue
        id = row[0]
        time = int(row[1])
        bytes = map(lambda x: int(x), row[2:])
        if not id in frames:
            frames[id] = FrameStream()
        frame = frames[id]
        if len(frame.bytesStream) == 0:
            frame.bytesStream = [[x] for x in bytes]
        else:
            if len(bytes) != len(frame.bytesStream):
                continue # frame damaged
            for b, byte in enumerate(bytes):
                frame.bytesStream[b].append(byte)
        frame.timeStream.append(time)
        assert len(frame.timeStream) == len(frame.bytesStream[0])

print 'CSV parsed'

errorsCount = 0
for (_, frame) in frames.items():
    for byteStream in frame.bytesStream:
        for i, b5 in enumerate(zip(byteStream[:-4], byteStream[1:-3], byteStream[2:-2], byteStream[3:-1], byteStream[4:])):
            if b5[2] != b5[0] and b5[0] == b5[1] and b5[0] == b5[3] and b5[0] == b5[4]:
                byteStream[i+2] = b5[0]
                errorsCount += 1

print 'errors fixed (bytes):', errorsCount

# calculate constancy intervals (means how much time the byte keeps constant bitmask):
for (_, frame) in frames.items():
    for byteStream in frame.bytesStream:
        frame.constTimestamps.append(list())
        if len(set(byteStream)) > 10:
            continue  # skip bytes with real numeric data
        timeStart = 0
        for i, b2 in enumerate(zip(byteStream[:-1], byteStream[1:])):
            if (b2[0] != b2[1]) or (i == len(byteStream) - 2):
                if timeStart < (i - 10):
                    frame.constTimestamps[-1].append([timeStart, i])
                timeStart = i+1

for key, frame in frames.iteritems():
    print key, "constant intervals: [", ', '.join([str(len(x)) for x in frame.constTimestamps]), "]"

# make 4 subplots with shared X axis:
fig, axs = plt.subplots(4, 1, sharex='all')

# display graphs of parsed and calculated RPM, Torque, etc. :
axs[0].set_title('0x280 parsed')
x = map(lambda time: time * 0.001, frames['0x280'].timeStream)
y = map(lambda (b1, b2): (b1*256 + b2) / 4 / 10, zip(frames['0x280'].bytesStream[3], frames['0x280'].bytesStream[2]))
axs[0].plot(x, y, label='RPM /10')
y = map(lambda b: b * 2, frames['0x280'].bytesStream[1])
axs[0].plot(x, y, label='Torque')
y = map(lambda b: b, frames['0x280'].bytesStream[5])
axs[0].plot(x, y, label='Acceleration pedal')
axs[0].fill_between(x, 0, y, label='Acceleration pedal', facecolor='red', alpha=0.25)
# byte #0 contains bitmask of clutch and acceleration pedals, display area when the clutch is pressed:
y = map(lambda b: b, frames['0x280'].bytesStream[0])
collection = plt_collections.BrokenBarHCollection.span_where(x, ymin=0, ymax=20, where=[dy <= 1 for dy in y], facecolor='green', alpha=0.25)
axs[0].add_collection(collection)

# dispaly speed steering angle and L/R forces:
axs[1].set_title('0x1A0, 0xC2, 0x540, 0x5C0 parsed')
x = map(lambda time: time * 0.001, frames['0x1A0'].timeStream)
y = map(lambda (b1, b2): (b1*256 + b2) * 0.005, zip(frames['0x1A0'].bytesStream[3], frames['0x1A0'].bytesStream[2]))
axs[1].plot(x, y, label='Speed')
y = map(lambda b: b, frames['0x1A0'].bytesStream[1])
# byte #1 contains bitmask for brake pedal, display area when brake is pressed:
collection = plt_collections.BrokenBarHCollection.span_where(x, ymin=-10, ymax=10, where=[dy == 72 for dy in y], facecolor='red', alpha=0.25)
axs[1].add_collection(collection)
x = map(lambda time: time * 0.001, frames['0xC2'].timeStream)
y = map(lambda (b1, b2): ((128 - b1 if b1 & 128 else b1) * 256 + b2) / 256, zip(frames['0xC2'].bytesStream[1], frames['0xC2'].bytesStream[0]))
axs[1].plot(x, y, label='Steering')
axs[1].fill_between(x, 0, y, label='Steering', facecolor='green', alpha=0.25)
x = map(lambda time: time * 0.001, frames['0x540'].timeStream)
y = map(lambda b: b, frames['0x540'].bytesStream[7])
axs[1].plot(x, y, label='Gear')
x = map(lambda time: time * 0.001, frames['0x5C0'].timeStream)
y = map(lambda b: b, frames['0x5C0'].bytesStream[2])
axs[1].plot(x, y, label='L. force')
axs[1].fill_between(x, [128 for a in y], y, label='L. force', facecolor='blue', alpha=0.25)

# display raw values of 8 bytes of specified CAN ID, skip constant and noise bytes:
bytesCount = len(frames[frameId].bytesStream)
axs[2].set_title(frameId + ': ' + str(bytesCount) + ' bytes')
x = map(lambda time: time * 0.001, frames[frameId].timeStream)
for i in range(0, bytesCount):
    y = frames[frameId].bytesStream[i]
    dy = map(lambda (v1, v2): v2-v1, zip(y, y[1:]))
    avr = sum(map(lambda x: abs(x), dy))
    if avr == 0:
        print frameId, 'skip constant byte', i
        continue  # skip constant byte
    avr /= len(dy)
    if avr > 5:
        print frameId, 'skip noise byte', i
        continue  # skip noise
    axs[2].plot(x, y, label='Byte ' + str(i))

axs[3].set_title(frameId + ' constant values intervals')
axs[3].yaxis.set_visible(False)
frame = frames[frameId]
for b, byteTimestamps in enumerate(frame.constTimestamps):
    if len(byteTimestamps) == 0:
        continue
    axs[3].text(1, b + 0.5, 'b' + str(b), va='center', color='black', fontsize='x-small')
    prevTimeStart = frame.timeStream[byteTimestamps[0][0]] * 0.001
    for i, timestamp in enumerate(byteTimestamps):
        timeStart = frame.timeStream[timestamp[0]] * 0.001
        timeEnd = frame.timeStream[timestamp[1]] * 0.001
        axs[3].barh(y=b, bottom=b+1, width=timeEnd - timeStart, left=prevTimeStart, color=('yellow' if i % 2 == 0 else 'lime'))
        prevTimeStart = timeEnd
        byteValue = frame.bytesStream[b][timestamp[0]]
        axs[3].text((timeStart + timeEnd) / 2, b + 0.5, str(byteValue), ha='center', va='center', color='black', fontsize='x-small')

axs[0].legend(fontsize='x-small')
axs[1].legend(fontsize='x-small')
axs[2].legend(fontsize='x-small')
plt.show()
