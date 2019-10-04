import matplotlib.pyplot as plt
import matplotlib.collections as plt_collections
import csv
from collections import defaultdict

csvFilaPath = 'log.csv'
frameId = '0x588'  # CAN ID to analyze

class Frame:
    id = ''
    time = 0
    data = []

frames = defaultdict(list)

with open(csvFilaPath, 'r') as file:
    rows = csv.reader(file, delimiter=',')
    for row in rows:
        frame = Frame()
        if len(row) < 3:
            print 'incorrect row:', row
            continue
        frame.id = row[0]
        frame.time = int(row[1])
        frame.data = map(lambda x: int(x), row[2:] + ['0']*(10-len(row)))  # for frames with less than 8 bytes data fill missing ones with 0
        frames[frame.id].append(frame)

# smooth single frame spikes (it happens that time to time we get broken data in CAN frames):
errorsCount = 0
for (_, frame) in frames.items():
    for i, f in enumerate(frame):
        if 0 < i < len(frame)-1:
            prevF = frame[i-1]
            nextF = frame[i+1]
            for n in range(0, len(f.data)):
                if prevF.data[n] == nextF.data[n] and prevF.data[n] != f.data[n]:
                    f.data[n] = prevF.data[n]
                    errorsCount += 1
print 'errors fixed (bytes):', errorsCount

# make 4 subplots with shared X axis:
fig, axs = plt.subplots(4, 1, sharex='all')

# display graphs of parsed and calculated RPM, Torque, etc. :
axs[0].set_title('0x280 parsed')
x = map(lambda f: f.time * 0.001, frames['0x280'])
y = map(lambda f: (f.data[3]*256 + f.data[2]) / 4 / 10, frames['0x280'])
axs[0].plot(x, y, label='RPM /10')
y = map(lambda f: f.data[1] * 2, frames['0x280'])
axs[0].plot(x, y, label='Torque')
y = map(lambda f: f.data[5], frames['0x280'])
axs[0].plot(x, y, label='Acceleration pedal')
# byte #0 contains bitmask of clutch and acceleration pedals, display area when the pedals are pressed:
y = map(lambda f: f.data[0], frames['0x280'])
collection = plt_collections.BrokenBarHCollection.span_where(x, ymin=0, ymax=20, where=[dy <= 1 for dy in y], facecolor='green', alpha=0.25)
axs[0].add_collection(collection)
collection = plt_collections.BrokenBarHCollection.span_where(x, ymin=0, ymax=20, where=[not (dy & 1) for dy in y], facecolor='red', alpha=0.25)
axs[0].add_collection(collection)

# dispaly speed and steering angle:
axs[1].set_title('0x1A0 & 0xC2 parsed')
x = map(lambda f: f.time * 0.001, frames['0x1A0'])
y = map(lambda f: (f.data[3]*256 + f.data[2]) * 0.005, frames['0x1A0'])
axs[1].plot(x, y, label='Speed')
y = map(lambda f: f.data[1], frames['0x1A0'])
# byte #1 contains butmask for brake pedal, display area when brake is pressed:
collection = plt_collections.BrokenBarHCollection.span_where(x, ymin=-10, ymax=10, where=[dy == 72 for dy in y], facecolor='red', alpha=0.25)
axs[1].add_collection(collection)
x = map(lambda f: f.time * 0.001, frames['0xC2'])
y = map(lambda f: ((128 - f.data[1] if f.data[1] & 128 else f.data[1]) * 256 + f.data[0]) / 256, frames['0xC2'])
axs[1].plot(x, y, label='Steering')
axs[1].fill_between(x, 0, y, label='Steering', facecolor='green', alpha=0.25)

# x = map(lambda f: f.time * 0.001, frames['4A8'])
# y = map(lambda f: f.data[2], frames['4A8'])
# axs[1].plot(x, y, label='Brake press')

# x = map(lambda f: f.time * 0.001, frames['4A0'])
# y = map(lambda f: (f.data[1]*256 + f.data[0]) / 200, frames['4A0'])
# axs[2].plot(x, y, label='ABS 1')
# y = map(lambda f: (f.data[3]*256 + f.data[2]) / 200, frames['4A0'])
# axs[2].plot(x, y, label='ABS 2')
# y = map(lambda f: (f.data[5]*256 + f.data[4]) / 200, frames['4A0'])
# axs[2].plot(x, y, label='ABS 3')
# y = map(lambda f: (f.data[7]*256 + f.data[6]) / 200, frames['4A0'])
# axs[2].plot(x, y, label='ABS 4')

# display raw values of 8 bytes of specified CAN ID, skip constant and noise bytes:
axs[2].set_title(frameId + ' bytes 0-3')
axs[3].set_title(frameId + ' bytes 4-7')
x = map(lambda f: f.time * 0.001, frames[frameId])
for i in range(0, len(frames[frameId][0].data)):
    y = map(lambda f: f.data[i], frames[frameId])
    dy = map(lambda (v1, v2): v2-v1, zip(y, y[1:]))
    avr = sum(map(lambda x: abs(x), dy))
    if avr == 0:
        continue  # skip constant byte
    avr /= len(dy)
    if avr > 5:
        continue  # skip noise
    axs[2 if i < 4 else 3].plot(x, y, label='Byte ' + str(i))
    # dy.append(0)
    # axs[2 if i < 4 else 3].plot(x, dy, label='d' + str(i))

    # recognize bitmask bytes by counting variants:
    variants = set(y)
    if len(variants) <= 5:
        for n, v in enumerate(variants):
            # display area for each variant:
            collection = plt_collections.BrokenBarHCollection.span_where(x, ymin=n*10, ymax=(n+1)*10, where=[dy == v for dy in y], alpha=0.25)
            axs[2 if i < 4 else 3].add_collection(collection)

axs[0].legend(fontsize='x-small')
axs[1].legend(fontsize='x-small')
axs[2].legend(fontsize='x-small')
axs[3].legend(fontsize='x-small')
plt.show()
