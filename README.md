# Parse CAN logs and visualize data streams on plot

## How to use it:
Assuming you have raw logs of massive CAN traffic in the following CSV format:

`CAN ID, timestamp, byte0, byte1...byte7`

For example:
```
0xC2,4871,183,0,0,0,128,80,172,248
0x540,4873,160,0,255,0,255,0,32,0
0xD2,4873,48,56,0,0,8,0,0,0
0x284,4874,15,15,0,0,0,0,0,0
0x38A,4874,244,128,116,0,0,0,0,0
0xD0,4877,210,42,0,56,0,192,0,0
0x320,4877,32,34,29,1,0,9,0,128
0x4A8,4878,37,128,2,144,0,0,80,103
```

In the python script you set the CSV file path and interesting CAN frame ID.
Running the script you get graphs of per-byte streams for individual frame.

![Sample plot](https://github.com/v-ivanyshyn/parse_can_logs/blob/master/screenshot.png "Sample plot")

It becomes very useful for searching for correlations in CAN bus traffic with actual car parameters while driving (ex. speed, RPM, steering, ...).

Personally I'm reverse-engeneering Volkswagen CC drivetrain CAN bus. Decoded some pretty interesting parameters and put them in the [summary file](https://github.com/v-ivanyshyn/parse_can_logs/blob/master/VW%20CAN%20IDs%20Summary.md).

---
By the way, looking forward for collaboration - if you have any information about CAN bus traffic, would be thankful for sharing it.
