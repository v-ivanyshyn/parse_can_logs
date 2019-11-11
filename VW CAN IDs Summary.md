# Volkswagen drivetrain CAN bus IDs
---
## Shortkeys:

`b0, b1, b...` - means byte index

`b0<<8` - left shift for 8 bits, the same as `b0 * 256`

`d(some param)` - means derivative, represents changing of the param

---

ID | Decoded bytes data | Assumptions/observations
--- | --- | ---
0x50  | | `b2`, `b3` - some time-based ticks
0xC2  | `b1<<8+b0` - steering (`b1` `bit7` for L/R direction) | `b3<<8+b2` - noise, correlates d(steering), wheel amplifier?
0xD0  | | `b2`, `b4` - radial force (correlates speed*steering)?
0x1A0 | `b1` - brake (`bit3`), `b3<<8+b2` - speed | `b7` - noise
0x1AC | | `b0` inverse of `b1` - brake pressure?, `b4` - noisy, correlates d(speed)
0x280 | `b0` - clutch (`bit3`) and acceleration (`bit0`) pedals, `b1`=`b4`=`b7` - torque or engine load, `b3<<8+b2` - RPM, `b5` - acceleration pedal | `b6` - some smooth graph
0x288 | `b1` - coolant temp. (X*0.75-48) | `b2` - low correlation to braking, `b6` - correlates to torque
0x320 | `b4<<8+b3` - speed, `b6<<8+b5` - speed adjusted (+5%) | `b0` - bit change when engine on, `b1` - bit change when start/stop driving, `b2` - fuel level?
0x390 | `b3` - reverse gear light (`bit4`), `b4` - left/right turn signals (`bit2`/`bit3`), `b6` - low/high beam light (`bit0`/`bit1`), hazard lights (`bit7`), `b7` - brake signal (`bit3`) |
0x3A0 | | `b6` - some ticks, correlates with speed
0x3D0 | | `b0` - noisy when steering, wheel amplifier?
0x480 | `b5` - clutch (8/136) | `b3` - slowly grows up when engine on, grow correlates with speed, fuel concumption?
0x488 | `b1`, `b2` - same values, torque or engine load |
0x48A | `b6` - selected/recommended gear (calculated from speed/rpm ratio) | `b2<<8+b1` - correlates RPM
0x4A0 | `b1<<8+b0` - ABS speed, each pair of bytes for each wheel |
0x4A8 | | `b2` - brake pressure?
0x497 | `b1`, `b7` - parktronic |
0x540 | `b7` - selected/recommended gear (calculated from speed/rpm ratio) |
0x588 | | `b1` - correlates torque/speed?, `b4` - turbine boost?
0x5A0 | | `b2<<8+b1` - correlates speed, `b0` - noisy, correlates steering, some force?, `b6<<8+b5` - some other smooth graph
0x5C0 | `b5` - clutch (changes when pedal pressed full) | `b0`, `b1` - parking brake?, `b2` - smooth graph, correlates d(speed)
0x5E0 | `b4`, `b6` - climate on/off |
---


