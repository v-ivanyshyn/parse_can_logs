# Ford HS3-CAN bus IDs (Mustang S550)
---
## Shortkeys:

`b0, b1, b...` - means byte index

`b0<<8` - left shift for 8 bits, the same as `b0 * 256`

---

+ **0x076:**
	* *`b1`: some sort of graph during run*
	* `(b5<<8+b6)/100`: speed
+ **0x077:**
	* *`b0+b1`: some sort of graph during run*
+ **0x109:**
	* `(b0<<8+b1)/4`: RPM
	* `b2`: gear mode (1 - P, 14 - during engine start, 17 - R, 33 - N, 49 - D, 65 - S)
	* `(b4<<8+b5)/100`: Speed
	* `b6`: 1 for rear gear
+ **0x167:**
	* *`b1<<8+b2`: looks like torque demand (use this formula for reasonable values: `((b1-127)<<8 + b2 - 128) / 5`)*
	* *`b5<<8+b6`: looks like torque torque/load (use this formula for reasonable values: `((b5-25)<<8 + b6 - 128) / 5`)*
+ **0x171:**
	* `b0`: current gear (20 - P/N, 36, 52, 68, 84, 100), `bit1` for manual mode. *Sometimes value differs, ex: P->R: 14->10->14*
	* `b1`: gear mode (0 - P, 32 - R, 64 - N, 96 - D, 128 - S)
+ **0x178:**
	* *`b2<<8+b3`: some +/- constant graph during run*
	* *`b5`: some +/- constant graph during run*
	* *`b6`: some +/- constant graph during run*
	* *`b7`: some +/- constant graph during run*
+ **0x179:**
	* *`b6`, `b7`: saw-like graph during engine off, idle stay and run*
+ **0x202:**
	* `b0`: rear gear (P/N/D/S - 4, R - 12)
	* `(b6<<8+b7)/100`: speed
+ **0x204:**
	* `((b0&3)<<8+b1) / 10`: accelerator pedal (0-100)
	* *`(b3<<8+b4) * 2`: matches RPM, but with smoother up/down edges sometimes*
+ **0x20A:**
	* `b0`: drive modes (0 - engine off, 1 - normal, 17 - sport/track, 33 - snow)
	* *`b1`: current gear (P/N - 132, R - 244, D/S - 140, `bit3` - engine on, `bit7` - drops on gears change, is it clutch?*
+ **0x213:**
	* *`b5<<8+b6`: looks like G force (`b5` is 2 for forward force, 1 for backward)*
+ **0x226:**
	* *`b0, b1, b2, b3, b4, b5` - very noisy graphs during engine off, idle stay and run*
+ **0x313:**
	* *`b5`: constantly grows, depend on speed. Odometer?*
+ **0x315:**
	* *`b6<<8+b7`: smooth inertial graph, corelates with acceleration pedal with some delay (use this formula for reasonable values: `(b6&3)<<8 + b7) / 4`)*
+ **0x318:**
	* *`b5<<8+b6`: slowly decreases during run. Gas in tank?*
+ **0x331:**
	* *`b2<<8+b3`: slowly grows during run*
+ **0x3D0:**
	* *`b2<<8+b3`: slowly grows during engine off, idle stay and run*
+ **0x415:**
	* `(b0<<8+b1)/100`: speed
	* *`b2`, `b3`: saw-like graph* 
	* *`b6<<8+b7`: not understandable graph during engine off, idle stay and run*
+ **0x421:**
	* *`b2`: smooth saw-like graph during run, changes when engine starts, voltage/current?*
	* *`b6`: smooth saw-like graph during run, changes when engine starts, voltage/current?*
+ **0x42D:**
	* *`b2`: graph opposite to spped, low on idle stay, grows when engine starts, current?*
+ **0x42F:**
	* *`b4<<8+b5`: smooth inertial graph, looks like load (use this formula for reasonable values: `(b4&3)<<8 + b5 - 256`)*
+ **0x43E:**
	* *`b3`: opposite to `b5<<8+b6`*
	* *`b5<<8+b6`: smooth inertial graph, looks like load (use this formula for reasonable values: `(b5<<8+b6)/40`)*
