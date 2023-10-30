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
	* `b2<<8+b3`: lateral G force
+ **0x07D (HS1, 20ms):**
	* `b0<<8+b1`: braking pressure
+ **0x082 (HS1):**
	* `b0`: steering with some noise
	* `b2<<8+b3`: current consumption
	* `b4`: voltage (`b4/20+6`V)
+ **0x083 (HS1, 100ms):**
	* `b0`: turn signals (16 - left, 32 - right)
+ **0x084 (HS1, 1000ms):**
	* `b4`: time, seconds (0-60)
	* `b5`: time, minutes
+ **0x085 (HS1):**
	* `b0<<8+b1`: steering
+ **0x092 (HS1, 100ms):**
	* *`b2<<8+b3`: noise during driving, some kind of body position sensor?*
	* *`b4<<8+b5`: body position sensor on rear axle*
+ **0x109 (HS3):**
	* `b0<<8+b1`: RPM: `(b0<<8 + b1) / 4`
	* `b2`: gearbox mode (1 - P, 14 - during engine start, 17 - R, 33 - N, 49 - D, 65 - S)
	* `b4<<8+b5`: speed: `(b4<<8 + b5) / 100`
	* `b6`: 1 for rear gear
+ **0x156 (HS1 & HS3, 10ms):**
	* `b1`: engine coolant temperature (`(b1-60)`°C)
+ **0x167 (HS1 & HS3, 10ms):**
	* `b0`: 0 if engine off, 32 on engine start, 114 if engine running
	* *`b1<<8+b2`: looks like engine load / torque (use this formula for reasonable values: `((b1-128)<<8 + b2) / 4`)*
	* `b5<<8+b6`: MAP (manifold abs. pressure): `(b5-25)<<8 + b6 - 128) / 5`
+ **0x171 (HS1 & HS3, 30ms):**
	* `b0`: current gear (20 - P/N, 36, 52, 68, 84, 100 - for gears), `bit1` for manual mode. *Sometimes value differs, ex: P->R: 14->10->14*
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
	* *`b4`: 0 when driving, 128 if speed=0*
	* `b5<<8+b6`: longitudinal G force: `if (b5 & 0x2) then b6 else if (b5 & 0x1) then (b6 - 256) else 0`
+ **0x216 (HS1 & HS3, 20ms):**
	* *not understandable saw-like graphs, frequency correlates with speed*
+ **0x217 (HS1, 10ms):**
	* speed on 4 wheels per every 2 bytes (LF, RF, LR, RR): `(b0<<8 + b1) / 100`
+ **0x230 (HS1, 20ms):**
	* `b0`: current gear (224 - R, 16 - 1, 32 - 2, ..., bit0 for clutch disengaged)
	* `b1`: gearbox mode (2 - R, 4 - N, 6 - D, 8 - S)
 	* `b4`: transmission fluid temperature (`(b4-60)`°C)
+ **0x242 (HS1, 40ms):**
	* *`b2<<8+b3`: correlates with headlights on/off, saw-like graph when engine idles. Current?*
+ **0x313 (HS3):**
	* *`b5`: constantly grows, depending on speed. Odometer?*
+ **0x315 (HS3):**
	* *`b6<<8+b7`: smooth inertial graph, corelates with acceleration pedal with some delay (use this formula for reasonable values: `(b6&3)<<8 + b7) / 4`)*
+ **0x318 (HS3):**
	* *`b5<<8+b6`: slowly decreases during run. Gas in tank?*
+ **0x326 (HS1):** 
	* * correlates with climate functionality*
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
	* `b0`: 40 - headlamp off, 44 - headlamp on
	* `b1`: 48 - ambient daylight, 88 - ambient twilight, 4A - hazard light
	* `b2`: x0/x2/x4/x6 - counter for pressed instruments cluster backlight +/- buttons, 1x - headlamp on non-auto, Cx - headlamp on auto (during daylight)
	* `b3`: 0C - dashboard dark mode(?), 0D-12 - instruments cluster backlight dimming
	* `b4`: 10 - turn signals off, 18 - any of turn signals on (left, right, hazard)
	* `b5`: 0 - instruments cluster backlight in day mode, 5 - instruments cluster backlight in night mode
	* `b6`: 0/40 - left turn signal
	* `b7`: bit0 - fog light, 8x - hazard light, Cx - right turn signal
+ **0x3B5 (HS1 & HS3):**
	* tire pressure: `b1` - front left, `b3` - front right, `b5` - rear right, `b7` - rear left (in kPa, x0.1450377377 to convert to PSI) 
+ **0x3D0 (HS3):**
	* *`b2<<8+b3`: slowly grows during engine off, idle stay and run*
+ **0x415 (HS1 & HS3):**
	* `b0<<8+b1`: speed: `(b0<<8 + b1) / 100`
	* *`b2`, `b3`: saw-like graph* 
	* *`b6<<8+b7`: not understandable graph during engine off, idle stay and run*
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
