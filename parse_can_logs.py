import matplotlib.pyplot as plt
import matplotlib.collections as plt_collections
import matplotlib.colors as colors
from matplotlib.widgets import Button
import re
import csv

csvFilaPath = 'log Mustang S550.txt'
import functools

def lambdaWrap(f):
    @functools.wraps(f)
    def f_inner(args):
        return f(*args)
    return f_inner


class FrameStream:
    def __init__(self):
        self.timeStream = []
        self.bytesStream = []  # array of [8]
        self.constTimestamps = []  # array of [8](start, end) tuples


frames = dict()

with open(csvFilaPath, 'r') as file:
    delimiter = re.compile(r'\w+')
    rows = [re.findall(delimiter, line) for line in file.readlines()]
    for row in rows:
        if len(row) != 10:
            print('skip row:', row)
            continue
        id = row[1].replace(':', '')
        # if not filteredIds.count(id):
        #     continue
        try:
            time = int(row[0])
        except ValueError:
            print('incorrect row time:', row)
            continue
        try:
            bytes = [int(x, 16) for x in row[2:]]
        except ValueError:
            print('incorrect row numbers:', row)
            continue
        if not id in frames:
            frames[id] = FrameStream()
        frame = frames[id]
        if len(frame.bytesStream) == 0:
            frame.bytesStream = [[x] for x in bytes]
        else:
            if len(list(bytes)) != len(frame.bytesStream):
                continue # frame damaged
            for b, byte in enumerate(bytes):
                frame.bytesStream[b].append(byte)
        frame.timeStream.append(time)
        assert len(frame.timeStream) == len(frame.bytesStream[0])

print('CSV parsed')

# errorsCount = 0
# for (_, frame) in frames.items():
#     for byteStream in frame.bytesStream:
#         for i, b5 in enumerate(zip(byteStream[:-4], byteStream[1:-3], byteStream[2:-2], byteStream[3:-1], byteStream[4:])):
#             if b5[2] != b5[0] and b5[0] == b5[1] and b5[0] == b5[3] and b5[0] == b5[4]:
#                 byteStream[i+2] = b5[0]
#                 errorsCount += 1
# print('errors fixed (bytes):', errorsCount)

# calculate constancy intervals (means how much time the byte keeps constant bitmask):
for (_, frame) in frames.items():
    for byteStream in frame.bytesStream:
        frame.constTimestamps.append(list())
        if len(set(byteStream)) > 20:
            continue  # skip bytes with real numeric data
        timeStart = 0
        for i, b2 in enumerate(zip(byteStream[:-1], byteStream[1:])):
            if (b2[0] != b2[1]) or (i == len(byteStream) - 2):
                if timeStart < (i - 1):
                    frame.constTimestamps[-1].append([timeStart, i])
                timeStart = i+1

for key, frame in frames.items():
    print(key, 'constant intervals: [', ', '.join([str(len(x)) for x in frame.constTimestamps]), ']')



# make subplots with shared X axis:
fig, axs = plt.subplots(5, 1, sharex='all')
frames_values = list(frames.values())
plt.xlim(frames_values[0].timeStream[0] * 0.001, frames_values[0].timeStream[-1] * 0.001)
# fig.tight_layout() - brakes buttons
plt.subplots_adjust(left=0.05, right=0.95, top=0.9, bottom=0.05)

# display RPM:
axs[0].set_title('RPM, speed, gear')
# x = [time * 0.001 for time in frames['0x109'].timeStream]
# y = [(b1*256 + b2) / 4 for b1, b2 in zip(frames['0x109'].bytesStream[0], frames['0x109'].bytesStream[1])]
# axs[0].plot(x, y, linewidth=1, label='109 RPM', color='red')
if '0x204' in frames:
    x = [time * 0.001 for time in frames['0x204'].timeStream]
    y = [(b1*256 + b2) * 2 for b1, b2 in zip(frames['0x204'].bytesStream[3], frames['0x204'].bytesStream[4])]
    axs[0].plot(x, y, linewidth=1, label='204 RPM')
    axs[0].set_ylim(0, max(y))

# dispaly speed:
if '0x077' in frames:
    x = [time * 0.001 for time in frames['0x077'].timeStream]
    y = [(b1*256 + b2) * 0.01 for b1, b2 in zip(frames['0x077'].bytesStream[0], frames['0x077'].bytesStream[1])]
    #axs[0].plot(x, y, linewidth=1, label='77 Speed')
    axsRight = axs[0].twinx()   # mirror them
    axsRight.set_ylim(0, max(y))
    axsRight.plot(x, y, linewidth=1, label='77 Speed', color='green')

# gears:
if '0x230' in frames:
    x = [time * 0.001 for time in frames['0x230'].timeStream]
    y = [b for b in frames['0x230'].bytesStream[0]]
    axs[0].plot(x, y, alpha=0.0)
    gears = list()
    for g in y:
        if not gears.count(g):
            gears.append(g)
    gears.sort()
    colors = list(colors.TABLEAU_COLORS.values())
    for i, g in enumerate(gears):
        collection = plt_collections.BrokenBarHCollection.span_where(x, ymin=0, ymax=g*50, where=[dy == g and (dy&1) == 0 and dy < 128 for dy in y], facecolor=colors[i%len(colors)], alpha=0.5)
        axs[0].add_collection(collection)
        collection = plt_collections.BrokenBarHCollection.span_where(x, ymin=0, ymax=g*50, where=[dy == g and (dy&1) == 1 and dy < 128 for dy in y], facecolor=colors[i%len(colors)], alpha=0.25)
        axs[0].add_collection(collection)
    collection = plt_collections.BrokenBarHCollection.span_where(x, ymin=0, ymax=200, where=[dy >= 128 for dy in y], facecolor=colors[0], alpha=0.5)
    axs[0].add_collection(collection)

def getGearRatio(t):
    tGear = [time * 0.001 for time in frames['0x20A'].timeStream]
    for i, x in enumerate(tGear):
        if x >= t:
            gear = frames['0x20A'].bytesStream[1][i] & 127
            return 4.17 if gear == 12 else 2.34 if gear == 20 else 1.52 if gear == 28 else 1.14 if gear == 36 else 0.87 if gear == 44 else 0.69 if gear == 52 else 0
    return 0

axs[0].legend(fontsize='x-small')


def displayCalculatedFrame(page):
    axs[1].clear()
    axs[1].set_title('Calculated frames:')
    ################# CAN-HS1 ###################
    if page == 0:
        x = [time * 0.001 for time in frames['0x076'].timeStream]
        y = [(b1*256 + b2)/100 - 160 for b1, b2 in zip(frames['0x076'].bytesStream[0], frames['0x076'].bytesStream[1])]
        axs[1].plot(x, y, linewidth=1, label='76 steering')
        x = [time * 0.001 for time in frames['0x3A8'].timeStream]
        y = [(b1*256 + b2)*0.01 - 100 for b1, b2 in zip(frames['0x3A8'].bytesStream[2], frames['0x3A8'].bytesStream[3])]
        axs[1].plot(x, y, linewidth=1, label='3A8 steering')
        x = [time * 0.001 for time in frames['0x085'].timeStream]
        y = [(b1*256 + b2)/100 - 320 for b1, b2 in zip(frames['0x085'].bytesStream[0], frames['0x085'].bytesStream[1])]
        axs[1].plot(x, y, linewidth=1, label='85 steering')
    elif page == 1:
        x = [time * 0.001 for time in frames['0x077'].timeStream]
        y = [((b1&31) * 256 + b2 - 2048) / 200 for b1, b2 in zip(frames['0x077'].bytesStream[2], frames['0x077'].bytesStream[3])]
        axs[1].plot(x, y, linewidth=1, label='77 lat. G')
        x = [time * 0.001 for time in frames['0x213'].timeStream]
        y = [((b1&3) * 256 + b2 - 512) / 28 for b1, b2 in zip(frames['0x213'].bytesStream[5], frames['0x213'].bytesStream[6])]
        axs[1].plot(x, y, label='213 long. G')

        # x = [time * 0.001 for time in frames['0x092'].timeStream]
        # y = [((b1&31) * 256 + b2) / 100 - 40 for b1, b2 in zip(frames['0x092'].bytesStream[0], frames['0x092'].bytesStream[1])]
        # axs[1].plot(x, y, linewidth=1, label='92 lat G b0+b1')
        # y = [((b1&31) * 256 + b2) / 100 - 40 for b1, b2 in zip(frames['0x092'].bytesStream[2], frames['0x092'].bytesStream[3])]
        # axs[1].plot(x, y, linewidth=1, label='92 long G b2+b3')
        # y = [((b1&31) * 256 + b2) / 100 - 40 for b1, b2 in zip(frames['0x092'].bytesStream[4], frames['0x092'].bytesStream[5])]
        # axs[1].plot(x, y, linewidth=1, label='92 vert G b4+b5')
    elif page == 2:
        x = [time * 0.001 for time in frames['0x07D'].timeStream]
        y = [((b1&31) * 256 + b2) / 10 for b1, b2 in zip(frames['0x07D'].bytesStream[0], frames['0x07D'].bytesStream[1])]
        axs[1].plot(x, y, linewidth=1, label='7D b0+b1 brake')
        x = [time * 0.001 for time in frames['0x07D'].timeStream]
        y = [((b1&15) * 256 + b2) / 8 for b1, b2 in zip(frames['0x07D'].bytesStream[3], frames['0x07D'].bytesStream[4])]
        axs[1].plot(x, y, linewidth=1, label='7D b3+b4')
        x = [time * 0.001 for time in frames['0x4B0'].timeStream]
        y = [(b1*256 + b2) / 100 for b1, b2 in zip(frames['0x4B0'].bytesStream[5], frames['0x4B0'].bytesStream[6])]
        axs[1].plot(x, y, linewidth=1, label='4B0 brake')
    elif page == 3:
        x = [time * 0.001 for time in frames['0x082'].timeStream]
        y = [b1/10 for b1 in frames['0x082'].bytesStream[3]]
        axs[1].plot(x, y, linewidth=1, label='82 b3: current')
        y = [b1/20 + 6 for b1 in frames['0x082'].bytesStream[4]]
        axs[1].plot(x, y, linewidth=1, label='82 b4: voltage')
        x = [time * 0.001 for time in frames['0x242'].timeStream]
        y = [b1/16 for b1 in frames['0x242'].bytesStream[4]]
        axs[1].plot(x, y, linewidth=1, label='242 b4: voltage')
    elif page == 4:
        x = [time * 0.001 for time in frames['0x167'].timeStream]
        y = [((b1-128)*256 + b2) / 4 for b1, b2 in zip(frames['0x167'].bytesStream[1], frames['0x167'].bytesStream[2])]
        axs[1].plot(x, y, linewidth=1, label='167 Torque?')
        x = [time * 0.001 for time in frames['0x42F'].timeStream]
        y = [((b1&15)*256 + b2 - (2048-512)) / 2 for b1, b2 in zip(frames['0x42F'].bytesStream[4], frames['0x42F'].bytesStream[5])]
        axs[1].plot(x, y, linewidth=1, label='42F Torque/Load?')
    elif page == 5:
        x = [time * 0.001 for time in frames['0x167'].timeStream]
        y = [(b1-25)*256 + b2 - 128 for b1, b2 in zip(frames['0x167'].bytesStream[5], frames['0x167'].bytesStream[6])]
        axs[1].plot(x, y, linewidth=1, label='167 MAP (manifold abs. pressure)')
        x = [time * 0.001 for time in frames['0x200'].timeStream]
        y = [((b1-128)*256 + b2) / 2 for b1, b2 in zip(frames['0x200'].bytesStream[4], frames['0x200'].bytesStream[5])]
        axs[1].plot(x, y, linewidth=1, label='200 b4+b5 throttle?')
    elif page == 6:
        x = [time * 0.001 for time in frames['0x43E'].timeStream]
        y = [(b1*256 + b2) / 72 - 140 for b1, b2 in zip(frames['0x43E'].bytesStream[5], frames['0x43E'].bytesStream[6])]
        axs[1].plot(x, y, linewidth=1, label='43E Engine Load')
        x = [time * 0.001 for time in frames['0x200'].timeStream]
        y = [(b1-127)*256 + b2 for b1, b2 in zip(frames['0x200'].bytesStream[2], frames['0x200'].bytesStream[3])]
        axs[1].plot(x, y, linewidth=1, label='200 b2+b3?')
        x = [time * 0.001 for time in frames['0x204'].timeStream]
        y = [((b1&3)*256 + b2) / 10 for b1, b2 in zip(frames['0x204'].bytesStream[0], frames['0x204'].bytesStream[1])]
        axs[1].fill_between(x, 0, y, label='204 Accelerator', facecolor='blue', alpha=0.25)
    elif page == 7:
        x = [time * 0.001 for time in frames['0x077'].timeStream]
        y = [(b1*256 + b2) / 100 for b1, b2 in zip(frames['0x077'].bytesStream[0], frames['0x077'].bytesStream[1])]
        axs[1].plot(x, y, linewidth=1, label='77 speed')
        x = [time * 0.001 for time in frames['0x217'].timeStream]
        y = [(b1*256 + b2)*0.01 for b1, b2 in zip(frames['0x217'].bytesStream[0], frames['0x217'].bytesStream[1])]
        axs[1].plot(x, y, linewidth=1, label='217 wheel speed LF')
        y = [(b1*256 + b2)*0.01 for b1, b2 in zip(frames['0x217'].bytesStream[2], frames['0x217'].bytesStream[3])]
        axs[1].plot(x, y, linewidth=1, label='217 wheel speed RF')
        y = [(b1*256 + b2)*0.01 for b1, b2 in zip(frames['0x217'].bytesStream[4], frames['0x217'].bytesStream[5])]
        axs[1].plot(x, y, linewidth=1, label='217 wheel speed LR')
        y = [(b1*256 + b2)*0.01 for b1, b2 in zip(frames['0x217'].bytesStream[6], frames['0x217'].bytesStream[7])]
        axs[1].plot(x, y, linewidth=1, label='217 wheel speed RR')
    elif page == 8:
        x = [time * 0.001 for time in frames['0x415'].timeStream]
        y = [(b1*256 + b2)*0.01 for b1, b2 in zip(frames['0x415'].bytesStream[0], frames['0x415'].bytesStream[1])]
        axs[1].plot(x, y, linewidth=1, label='415 speed')
        x = [time * 0.001 for time in frames['0x415'].timeStream]
        y = [(b1*256 + b2)*0.01 for b1, b2 in zip(frames['0x415'].bytesStream[4], frames['0x415'].bytesStream[5])]
        axs[1].plot(x, y, linewidth=1, label='415 b4+b5')
        x = [time * 0.001 for time in frames['0x415'].timeStream]
        y = [(b1*256 + b2)*0.01 for b1, b2 in zip(frames['0x415'].bytesStream[6], frames['0x415'].bytesStream[7])]
        axs[1].plot(x, y, linewidth=1, label='415 b6+b7')
    elif page == 9:
        x = [time * 0.001 for time in frames['0x42D'].timeStream]
        y = frames['0x42D'].bytesStream[2]
        axs[1].plot(x, y, linewidth=1, label='42D b2')
        x = [time * 0.001 for time in frames['0x4B0'].timeStream]
        y = [b1 for b1, b2 in zip(frames['0x4B0'].bytesStream[0], frames['0x4B0'].bytesStream[1])]
        axs[1].plot(x, y, linewidth=1, label='4B0 b0')
    elif page == 10:
        x = [time * 0.001 for time in frames['0x43D'].timeStream]
        y = frames['0x43D'].bytesStream[1]
        axs[1].plot(x, y, linewidth=1, label='43D b1')
        x = [time * 0.001 for time in frames['0x242'].timeStream]
        y = [((b1&(~192))-32)*256 + b2 for b1, b2 in zip(frames['0x242'].bytesStream[2], frames['0x242'].bytesStream[3])]
        axs[1].plot(x, y, linewidth=1, label='242 b2+b3')
    elif page == 11:
        x = [time * 0.001 for time in frames['0x156'].timeStream]
        y = frames['0x156'].bytesStream[1]
        axs[1].plot(x, y, linewidth=1, label='156 b1 (coolant t)')
        x = [time * 0.001 for time in frames['0x230'].timeStream]
        y = frames['0x230'].bytesStream[4]
        axs[1].plot(x, y, linewidth=1, label='230 b4 (trans t)')
    elif page == 12:
        x = [time * 0.001 for time in frames['0x213'].timeStream]
        y = [((b1&15) * 256 + b2) / 10 for b1, b2 in zip(frames['0x213'].bytesStream[0], frames['0x213'].bytesStream[1])]
        axs[1].plot(x, y, label='213 b0+b1')

        x = [time * 0.001 for time in frames['0x416'].timeStream]
        y = [b1&(128+64+32) for b1 in frames['0x416'].bytesStream[1]]
        axs[1].plot(x, y, linewidth=1, label='0x416 b1 bit7')
        if '0x72E' in frames:
            x = [time * 0.001 for time in frames['0x72E'].timeStream]
            y = frames['0x72E'].bytesStream[4]
            axs[1].plot(x, y, linewidth=1, label='0x72E b4')
            y = frames['0x72E'].bytesStream[5]
            axs[1].plot(x, y, linewidth=1, label='0x72E b5')
    axs[1].legend(fontsize='x-small')


calculatedFramePage= 0
def nextCalculatedClick(event):
    global calculatedFramePage
    calculatedFramePage = (calculatedFramePage + 1) % 13
    displayCalculatedFrame(calculatedFramePage)
    plt.draw()
def prevCalculatedClick(event):
    global calculatedFramePage
    calculatedFramePage = (calculatedFramePage - 1) % 13
    displayCalculatedFrame(calculatedFramePage)
    plt.draw()
axprevCalculated = plt.axes([0.82, 0.01, 0.03, 0.03])
bprevCalculated = Button(axprevCalculated, '<[')
bprevCalculated.on_clicked(prevCalculatedClick)
axnextCalculated = plt.axes([0.852, 0.01, 0.03, 0.03])
bnextCalculated = Button(axnextCalculated, ']>')
bnextCalculated.on_clicked(nextCalculatedClick)





def displayCustomFrame(frameId):
    axs[2].clear()
    axs[3].clear()
    axs[4].clear()
    # display raw values of 8 bytes of specified CAN ID, skip constant and noise bytes:
    bytesCount = len(frames[frameId].bytesStream)
    x = [time * 0.001 for time in frames[frameId].timeStream]
    dt = [(x2 - x1)*1000 for (x1, x2) in zip(x[:-1], x[1:])]
    assert(len(dt) > 0)
    axs[2].set_title(frameId + ': ' + str(bytesCount) + ' bytes, dt: ' + str(int(sum(dt) / len(dt))) + 'ms')
    for i in range(0, bytesCount):
        y = frames[frameId].bytesStream[i]
        dy = [v2-v1 for (v1, v2) in zip(y[:-1], y[1:])]
        avr = sum([abs(x) for x in dy])
        if avr == 0:
            print(frameId, 'skip constant byte', i, ' = ', hex(y[0]))
            continue  # skip constant byte
        avr /= len(dy)
        if avr > 20:
            print(frameId, 'skip noise byte', i)
            continue  # skip noise
        axs[2].plot(x, y, linewidth=1, label='Byte ' + str(i))
    axs[2].legend(fontsize='x-small')

    axs[3].set_title('dt (avr: ' + str(int(sum(dt) / len(dt))) + 'ms)')
    dt = [(x2 - x1) for (x1, x2) in zip(x[:-1], x[1:])]
    dt.append(0)
    axs[3].step(x, dt, label='dt', color='red', alpha=0.25)

    axs[4].set_title(frameId + ' constant values intervals')
    axs[4].yaxis.set_visible(False)
    frame = frames[frameId]
    for b, byteTimestamps in enumerate(frame.constTimestamps):
        if len(byteTimestamps) == 0:
            continue
        axs[3].text(1, b + 0.5, 'b' + str(b), va='center', color='black', fontsize='x-small')
        prevTimeStart = frame.timeStream[byteTimestamps[0][0]] * 0.001
        for i, timestamp in enumerate(byteTimestamps):
            timeStart = frame.timeStream[timestamp[0]] * 0.001
            timeEnd = frame.timeStream[timestamp[1]] * 0.001
            axs[4].barh(y=(b+0.5), width=(timeEnd-timeStart), left=prevTimeStart, color=('orange' if i % 2 == 0 else 'lime'))
            prevTimeStart = timeEnd
            byteValue = frame.bytesStream[b][timestamp[0]]
            axs[4].text((timeStart + timeEnd) / 2, b + 0.5, hex(byteValue), ha='center', va='center', color='black', fontsize='x-small')
    axs[4].legend(fontsize='x-small')



frames_keys = list(frames.keys())
frames_keys.sort()

frameIdIndex= 0
frameId = frames_keys[frameIdIndex]
def nextClick(event):
    global frameId
    global frameIdIndex
    frameIdIndex = (frameIdIndex + 1) % len(frames)
    frameId = frames_keys[frameIdIndex]
    displayCustomFrame(frameId)
    plt.draw()
def prevClick(event):
    global frameId
    global frameIdIndex
    frameIdIndex = (frameIdIndex - 1) % len(frames)
    frameId = frames_keys[frameIdIndex]
    displayCustomFrame(frameId)
    plt.draw()
def frameClick(frIndex, event):
    global frameId
    global frameIdIndex
    frameIdIndex = frIndex % len(frames)
    frameId = frames_keys[frameIdIndex]
    displayCustomFrame(frameId)
    plt.draw()

axprev = plt.axes([0.9, 0.01, 0.03, 0.03])
bprev = Button(axprev, '<')
bprev.on_clicked(prevClick)
axnext = plt.axes([0.932, 0.01, 0.03, 0.03])
bnext = Button(axnext, '>')
bnext.on_clicked(nextClick)
frameButtons = list()
for frIndex, fr in enumerate(frames):
    framesCount = len(frames)
    aframe = plt.axes([0.97, 0.01 + frIndex / framesCount * 0.98, 0.02, 0.01])
    bframe = Button(aframe, frames_keys[frIndex])
    bframe.label.set_fontsize(6)
    bframe.on_clicked(functools.partial(frameClick, frIndex))
    frameButtons.append(bframe)

fig.suptitle(csvFilaPath)
displayCalculatedFrame(calculatedFramePage)
displayCustomFrame(frameId)
plt.show()
