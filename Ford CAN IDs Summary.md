# Ford HS1 & HS3 CAN bus IDs (Mustang S550, GT, 6R80 auto)
---
## Shortkeys:

`b0, b1, b...` - means byte index

`b0<<8` - left shift for 8 bits, the same as `b0 * 256`

---

+ **0x076 (HS1 & HS3, 20ms):**
	* `b0<<8+b1`: steering
	* `b5<<8+b6`: speed: `(b5<<8 + b6) / 100`
+ **0x077 (HS1 & HS3, 20ms):**
	* `b0<<8+b1`: speed
	* `b2<<8+b3`: lateral G force relative to the car base (is 0 when the car stays still, in contrast to `0x092`). Use the formula `((b2&31)<<8 + b3 - 2048) / 200` (m/s^2)
+ **0x07D (HS1, 20ms):**
	* `b0<<8+b1`: braking pressure *applied from brake pedal?*
	* `b3<<8+b4`: braking pressure *applied also in case of traction control (along with `0x416 b1 bit7`)*
+ **0x081 (HS3):**
	* `b0`: wheel buttons on left side: `bit0` - down, `bit1` - left, `bit2` - right, `bit3` - up, `bit4` - ok
+ **0x082 (HS1):**
	* `b0`: steering with some noise
	* `b2<<8+b3`: current consumption
	* `b4`: voltage (`b4/20+6`V)
	* `b6`: steering mode (`0x40` - normal, `0x44` - sport, `0x48` - comfort)
+ **0x083 (HS1, 100ms):**
  	* steering wheel buttons (headlight, cruise control, windshield wiper)
	* `b0`: turn signals (`bit4` - left, `bit5` - right)
+ **0x084 (HS1, 1000ms):**
	* `b0`: current year, last 2 digits
	* `b2<<8+b3`: current day number of the year (ex. `0x00` `0x20` -> `0*256+32=32` -> Feb. 1)
	* `b4`: current time, seconds (0-60)
	* `b5`: current time, minutes
	* `b6`: current time, hour
+ **0x085 (HS1):**
	* `b0<<8+b1`: steering
+ **0x092 (HS1, 100ms):**
	* G-force relative to ground plane, noisy. If the car stays on inclined surface it will affect the value. Use the formula: `((b1&31)<<8 + b2) / 100 - 40` (m/s^2)
  	* `b0<<8+b1`: lateral (positive if directed towards right side) 
	* `b2<<8+b3`: longitudinal (positive if directed towards back)
	* `b4<<8+b5`: vertical (is 9.8 when stay still on horigontal surface)
+ **0x109 (HS3):**
	* `b0<<8+b1`: RPM: `(b0<<8 + b1) / 4`
	* `b2`: gearbox mode (1 - P, 14 - during engine start, 17 - R, 33 - N, 49 - D, 65 - S)
	* `b4<<8+b5`: speed: `(b4<<8 + b5) / 100`
	* `b6`: 1 for rear gear
+ **0x156 (HS1 & HS3, 10ms):**
	* `b0`: coolant temperature (`(b0-60)`°C)
	* `b1`: engine oil temperature (`(b1-60)`°C)
+ **0x167 (HS1 & HS3, 10ms):**
	* `b0`: 0 if engine off, 32 on engine start, 114 if engine running
	* *`b1<<8+b2`: looks like engine load / torque (use this formula for reasonable values: `((b1-128)<<8 + b2) / 4`)*
	* `b5<<8+b6`: MAP (manifold abs. pressure): `(b5-25)<<8 + b6 - 128) / 5`
+ **0x171 (HS1 & HS3, 30ms):**
	* `b0`: current gear (20 - P/N, 36, 52, 68, 84, 100 - for gears), `bit0` for manual mode, `bit1` if attempt to change gear fails
	* `b1`: gearbox mode (0 - P, 32 - R, 64 - N, 96 - D, 128 - S)
+ **0x178 (HS1 & HS3, 100ms):**
	* *`b2<<8+b3`: some +/- constant graph during run*
	* *`b5`: some +/- constant graph during run*
	* *`b6`: some +/- constant graph during run*
	* *`b7`: some +/- constant graph during run*
+ **0x179 (HS1 & HS3, 100ms):**
	* *`b5<<8+b6`: some growing graph
	* *`b7`: saw-like graph during engine off, idle stay and run*
+ **0x200 (HS1, 20ms):**
	* `b2<<8+b3`: ?
	* *`b4<<8+b5`: throttle position?*
+ **0x202 (HS1 & HS3, 20ms):**
	* `b0`: rear gear (4 - P/N/D/S, 12 - R)
	* `b6<<8+b7`: speed: `(b6<<8 + b7) / 100`
+ **0x204 (HS1 & HS3, 10ms):**
	* `b0<<8+b1`: accelerator pedal (0-100): `((b0&3)<<8 + b1) / 10`
	* *`b3<<8+b4`: matches RPM, but with smoother up/down edges sometimes: `(b3<<8 + b4) * 2`*
+ **0x20A (HS3):**
	* `b0`: drive modes (1 - normal, 17 - sport/track, 33 - snow)
	* *`b1`: represents current gear, `bit7` - drops sometimes when gears change, `bit2` drops sometimes*
+ **0x213 (HS1 & HS3, 20ms):**
  	* `b1`: is 255, goes down when traction control applies braking
  	* `b2`: `bit7` - traction control applied when the wheels slide (works with TC ON & OFF, doesn't work with ATC OFF)
  	* `b3`: `0x00`->`0x80` - traction control applies braking (same as `b1`)
	* *`b4`: 0 when driving, 128 if speed=0*
	* `b5<<8+b6`: longitudinal G force relative to the car base (is 0 when the car stays still, in contrast to `0x092`). Use the formula `((b5&3)<<8 + b6 - 512) / 28` (m/s^2)
+ **0x216 (HS1 & HS3, 20ms):**
	* *not understandable saw-like graphs, frequency correlates with speed*
+ **0x217 (HS1, 10ms):**
	* speed on 4 wheels per every 2 bytes (LF, RF, LR, RR): `(b0<<8 + b1) / 100`
+ **0x230 (HS1, 20ms):**
	* `b0`: current gear (224 - R, 16 - 1, 32 - 2, ..., bit0 for clutch disengaged)
	* `b1`: gearbox mode (2 - R, 4 - N, 6 - D, 8 - S)
 	* `b4`: transmission fluid temperature (`(b4-60)`°C)
+ **0x242 (HS1, 40ms):**
	* `b2<<8+b3`: correlates with headlights on/off, saw-like graph when engine idles. Current?
 	* `b4`: voltage (`b4/16`V), smoother than `0x082 b4`
+ **0x2A1 (HS3):**
	* `b0`: wheel buttons on right side: `0xFF` if no buttons pressed, `0xFD` - vol+, `0xFE` - vol-, `0x32` - previous, `0x33` - next, `0x4F` - M, `0x45` - phone up, `0x46` - phone down, `0x30` - voice command, `0x44` - mute
+ **0x313 (HS3):**
	* *`b5`: constantly grows, depending on speed. Odometer?*
+ **0x315 (HS3):**
	* *`b6<<8+b7`: smooth inertial graph, corelates with acceleration pedal with some delay (use this formula for reasonable values: `(b6&3)<<8 + b7) / 4`)*
+ **0x318 (HS3):**
	* *`b5<<8+b6`: slowly decreases during run. Gas in tank?*
+ **0x326 (HS1):** 
	* *correlates with climate functionality*
+ **0x331 (HS1 & HS3):**
	* *`b2<<8+b3`: slowly grows during run*
	* *`b7`: changes 4/2 when ambiant light or headlights on/off*
+ **0x38D (HS1 & HS3):**
	* *`b4`: spike on engine start. Alternator?*
+ **0x3A8 (HS1):**
	* `b2<<8+b3`: steering
+ **0x3AA (HS1 & HS3):**
	* *`b1`: 32->33->32 on engine start*
+ **0x3B2 (HS3):**
	* same as `0x3B3`
+ **0x3B3 (HS1 & HS3):**
	* `b0`: `0x40` - headlamp off, `0x44` - headlamp on
	* `b1`: `0x48` - ambient daylight, `0x88` - ambient twilight, `0x4A` - hazard light
	* `b2`: `0x#0/#2/#4/#6` - counter for pressed instruments cluster backlight +/- buttons, `0x1#` - headlamp on non-auto, `0xC#` - headlamp on auto (during daylight)
	* `b3`: `0x0C` - dashboard dark mode(?), `0x0D`-`0x12` - instruments cluster backlight dimming
	* `b4`: `0x10` - turn signals off, `0x18` - any of turn signals on (left, right, hazard)
	* `b5`: `0x0` - instruments cluster backlight in day mode, `0x5` - instruments cluster backlight in night mode
	* `b6`: `0x40` - left turn signal
	* `b7`: `bit0` - fog light, `0x8#` - hazard light, `0xC#` - right turn signal
+ **0x3B5 (HS1 & HS3):**
	* tire pressure: `b1` - front left, `b3` - front right, `b5` - rear right, `b7` - rear left (in kPa, x0.1450377377 to convert to PSI) 
+ **0x3C8 (HS1, 1000ms):**
	* `b0`, `b4`, `b5` - RGB colors of My Color
	* `b2` - drive mode (0 - normal, 1 - sport, 2 - snow, 3 - track)
+ **0x3D0 (HS3):**
	* *`b2<<8+b3`: slowly grows during engine off, idle stay and run*
+ **0x40A (HS1 & HS3):**
	* VIN code: when `b0` is `0xC1` the `b1` may be `0x00`, `0x01` or `0x02` and the following bytes `b2`-`b7` contain ASCII encoded VIN, for example:
	`0x40A: C1 00 31 46 41 36 50 38`
	`0x40A: C1 01 43 46 38 47 35 32`
	`0x40A: C1 02 33 34 31 39 37 FF`
	results in `1FA6P8CF8G5234197`
+ **0x415 (HS1 & HS3):**
	* `b0<<8+b1`: speed: `(b0<<8 + b1) / 100`
	* *`b2`, `b3`: saw-like graph* 
	* *`b6<<8+b7`: not understandable graph during engine off, idle stay and run*
+ **0x416 (HS1 & HS3, 100ms):**
	* `b0`: brake pedal, some bits work as a counter
	* `b1`: `bit7` set when braking automatically because of traction control
	* `b5`: traction control mode (`0x0` - TC ON, `0x8` - TC OFF, `0x18` - ATC OFF when pressing the button for 7 seconds)
+ **0x421 (HS1 & HS3):**
	* *`b2`: smooth saw-like graph during run, changes when engine starts, voltage/current?*
	* *`b6`: smooth saw-like graph during run, changes when engine starts, voltage/current?*
+ **0x42D (HS1 & HS3):**
	* *`b2`: graph opposite to speed, low on idle stay, grows when engine starts, decreases on speeding, current?*
+ **0x42F (HS1 & HS3):**
	* *`b4<<8+b5`: looks like torque, the same as `0x167 b1<<8+b2` (use this formula for reasonable values: `(b4&3)<<8 + b5 - 256`)*
+ **0x43D (HS1):**
	* *`b2` & `b3` opposite to each other, correlates with RPM/acceleration*
+ **0x43E (HS1 & HS3):**
	* *`b3`: opposite to `b5<<8+b6`*
	* `b5<<8+b6`: engine load in %: `(b5<<8 + b6) / 72 - 140`
+ **0x4B0 (HS1):**
	* `b5<<8+b6` - braking pressure
