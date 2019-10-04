# Volkswagen drivetrain CAN bus IDs
---
## Shortkeys:

`b0, b1, b...` - means byte index

`b0<<8` - left shift for 8 bits, the same as `b0 * 256`

`d(some param)` - means derivative, represents changing of the param

---

ID | Decoded bytes data | Assumptions/observations
--- | --- | ---
0xC2  | `b1<<8+b0` - steering (b1 bit7 for L/R direction) | `b3<<8+b2` - noise, correlates d(steering), wheel amplifier?
0xD0  | | `b2` - radial force (correlates speed*steering)? `b5` - correlates steer
0x1A0 | `b1` - `64/72` - brake bitmask, `b3<<8+b2` - speed | `b7` - noise
0x1AC | | `b1` - brake pressure?, `b4` - noisy, correlates d(speed)
0x280 | `b0` - `0/1/8/9` - clutch and acceleration pedals, engine on bitmasks, `b1`=`b4`=`b7` - torque or engine load, `b3<<8+b2` - RPM, `b5` - acceleration pedal | `b6` - some smooth graph
0x320 | `b4<<8+b3` - speed, `b6<<8+b5` - speed adjusted (+5%) | `b0` - bit change when engine on, `b1` - bit change when start/stop driving, `b2` - fuel level?
0x480 | | `b3` - slowly grows up when engine on, grow corelates with speed
0x488 | `b1`, `b2` - same values, torque or engine load |
0x48A | | `b2<<8+b1` - correlates RPM
0x4A0 | `b1<<8+b0` - ABS speed, each pair of bytes for each wheel |
0x4A8 | | `b2` - brake pressure?
0x588 | | `b1` - correlates torque?, `b4` - turbine boost?
0x5A0 | | `b2<<8+b1` - acceleration force?, `b0` - interesting smooth graph, `b6<<8+b5` - some other smooth graph
0x5C0 | | `b0`, `b1` - parking brake?, `b2` - some other smooth graph

---

Other IDs in CAN bus traffic with totally unclear params:

`0x50, 0xAE, 0xD2, 0x284, 0x2A0, 0x368, 0x38A, 0x3A0, 0x3D0, 0x540`
