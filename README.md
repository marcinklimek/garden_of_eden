# Garden of eden


## First use

- connect esp to PC via USB
- go to https://web.esphome.io/
- run first use
	- web interface 

- esphome tool
	- uv init
	- uv add esphome
	- prepare configuration yaml like: board.yaml
	- uv run compile board.yaml
	- uv run upload board.yaml --device COM3  // --use-address <192.168.x.x>
		- pay attantion to capital COM3 !!!


## sensors


| #  | DRY   | WET   |
|----|-------|-------|
| 1  | 2900  | 1231  |
| 2  | 3088  | 1266  |
| 3  | 3047  | 1286  |
| 4  | 2958  | 1245  |
| 5  | 3110  | 1254  |
| 6  | 3091  | 1275  |
| 7  | 3057  | 1271  |
| 8  | 2930  | 1198  |
| 9  | 3083  | 1266  |
| 10 | 3090  | 1280  |
| 11 | 3041  | 1231  |
| 12 | 3034  | 1283  |
| 13 | 3035  | 1268  |
| 14 | 3058  | 1250  |
| 15 | 3066  | 1295  |
| 16*| 3415  | 1630  |
| 17 | 2971  | 1250  |
| 18 | 2891  | 1258  |
| 19 | 2943  | 1255  |
| 20 | 2950  | 1238  |


- **DRY:** The lowest value is **2891** (from row 18).
- **WET:** The lowest value is **1198** (from row 8).

These minimum values can serve as your calibration endpoints:
- **Dry (0% moisture):** 2891
- **Wet (100% moisture):** 1198

To convert any ADC reading (let’s call it _X_) into a moisture percentage, you can use the following formula:

\[
\text{Moisture \%} = \frac{(2891 - X)}{(2891 - 1198)} \times 100
\]

Here, the denominator is the range (2891 – 1198 = 1693). With this formula:
- An ADC reading equal to **2891** yields 0% moisture.
- An ADC reading equal to **1198** yields 100% moisture.

