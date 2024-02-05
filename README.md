# Parse CAN logs and visualize data streams on plot

## How to use it:
Assuming you have raw logs of massive CAN traffic in the following format:

`timestamp CAN_ID byte0 byte1...byte7` (any non-alphanumeric character may be a delimiter)

For example:
```
820298   0x085: 7C 33 80 00 47 E0 7C 7F
820301   0x047: 20 00 00 00 00 00 00 00
820302   0x165: 10 C0 00 00 00 00 00 00
820302   0x167: 72 80 6E 00 00 1A 0A 00
820303   0x200: 00 00 80 53 80 53 10 00
820303   0x202: 04 F9 18 00 60 00 00 00
```

In the python script you set the file path (instead of `log Mustang S550.txt`).

![Sample plot](https://github.com/v-ivanyshyn/parse_can_logs/blob/master/screenshot.png "Sample plot")

Running the script you get graphs of per-byte streams for individual frame. On the top chart there is predefined compiled data of RPM, speed, gear, etc... The second chart contains precompiled custom data based on formulas defined in code and supposed to be edited while investigating it. You can iterate the pages of these charts. Below on the last charts you can see the raw data, time lags and each byte values over time if these values aren't changing too frequently.

It becomes very useful for searching for correlations in CAN bus traffic with actual car parameters while driving (ex. speed, RPM, steering, ...).

Personally I reverse-engeneered Volkswagen CC drivetrain CAN bus. Decoded some pretty interesting parameters and put them in the [summary file](https://github.com/v-ivanyshyn/parse_can_logs/blob/master/VW%20CAN%20IDs%20Summary.md).

Currently investigating [Mustang S550 CAN bus](https://github.com/v-ivanyshyn/parse_can_logs/blob/master/Ford%20CAN%20IDs%20Summary.md).

---
By the way, looking forward for collaboration - if you have any information about CAN bus traffic, would be thankful for sharing it.
