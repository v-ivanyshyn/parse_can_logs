# Volkswagen drivetrain CAN bus IDs
---
## Shortkeys:

`b0, b1, b...` - means byte index

`b0<<8` - left shift for 8 bits, the same as `b0 * 256`

`d(some param)` - means derivative, represents changing of the param

---

+ **0x50**
  * (?) `b2`, `b3` - some time-based ticks
+ **0xC2**
  * `b1<<8+b0` - steering (`b1` `bit7` for L/R direction)
  * (?) `b3<<8+b2` - noise, correlates d(steering)
+ **0xD0**
  * (?) `b2` - steering wheel amplifier
+ **0x1A0**
  * `b1` - brake pedal (`bit3`)
  * `b3<<8+b2` - speed
  * (?) `b7` - noise
+ **0x1AC**
  * (?) `b0` inverse of `b1` - brake pressure?
  * (?) `b4` - noisy, correlates d(speed)
+ **0x280**
  * `b0` - clutch (`bit3`) and acceleration (`bit0`) pedals
  * `b1`=`b4`=`b7` - torque or engine load
  * `b3<<8+b2` - RPM
  * `b5` - acceleration pedal or cruise
  * (?)`b6` - some smooth graph
+ **0x284**
  * (?) `b1` - saw on different levels, levels corelate braking
  * (?) `b3<<8+b2` - smooth graph corelates braking
+ **0x288**
  * `b1` - coolant temp. (X*0.75-48)
  * `b2` - ACC working (`bit6`)
  * (?) `b6` - power? (correlates torque+rpm)
+ **0x320**
  * (?) `b0` - bit change when engine on
  * (?) `b1` - bit change when start/stop driving
  * `b2` - fuel level
  * `b4<<8+b3` - speed
  * `b6<<8+b5` - speed adjusted (+5%)
+ **0x380**
  * `b2` - acceleration pedal (excluding cruise control)
+ **0x38A**
  * `b1` - ACC buttons (128 - off, `bit0` - on/off, `bit2` - spd down, `bit3` - spd up)
+ **0x390**
  * `b2` - driver door open (`bit0`)
  * `b3` - reverse gear light (`bit4`), rear left and right doors open (`bit2` and `bit3`)
  * `b4` - left/right turn signals (`bit2`/`bit3`)
  * `b5` - front right door open (`bit1`), trunk open (`bit3`)
  * `b6` - low/high beam light (`bit0`/`bit1`), hazard lights (`bit7`)
  * `b7` - windscreen wipers (`bit2`), brake signal (`bit3`)
+ **0x392**
  * `b4` - headlights auto mode (`bit5`), rear fog light (`bit7`)
  * (?) `b3` - ambient light level (very low values)
+ **0x3A0**
  * (?) `b6` - some ticks, correlates speed
+ **0x3D0**
  * (?) `b0` - noisy when steering, wheel amplifier?
+ **0x480**
  * (?) `b3` - slowly grows up when engine on, grow correlates speed, fuel concumption?
  * `b5` - clutch fully disengaged (`bit7`)
+ **0x488**
  * `b1`, `b2` - same values, torque or engine load
+ **0x48A**
  * (?) `b2<<8+b1` - low values, correlates RPM
  * `b6` - selected/recommended gear (calculated from speed/rpm ratio)
+ **0x4A0**
  * `b1<<8+b0` - ABS speed, each pair of bytes for each wheel
+ **0x4A8**
  * (?) `b2` - brake pressure?
+ **0x497**
  * `b1`, `b7` - parktronic
+ **0x520**
  * `b7<<8<<8 + b6<<8 + b5` - mileage (odometer)
+ **0x540**
  * `b7` - selected/recommended gear (calculated from speed/rpm ratio)
+ **0x588**
  * (?) `b1` - correlates torque/speed?
  * `b4` - turbine boost
+ **0x598**
  * `b0` - DCC mode - last two bits for comfort (`01`), normal (`10`), sport (`11`), `bit1` always `1`, `bit3` - button pressed
+ **0x5A0**
  * (?) `b0` - radial force (128 - baseline, noisy),
  * (?) `b2<<8+b1` - correlates speed
  * (?) `b6<<8+b5` - some other smooth graph
+ **0x5C0**
  * (?) `b0`, `b1` - parking brake?
  * `b2` - long. force (128 - baseline)
  * `b5` - clutch (`bit5`)
  * `b7` - saw, level means acceleration/braking (binary)
+ **0x5E0**
  * `b4`, `b6` - climate on/off



