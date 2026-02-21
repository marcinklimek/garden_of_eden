# Garden of eden

ESP32-based garden automation system using [ESPHome](https://esphome.io/). Manages watering, soil monitoring, water level sensing, and general-purpose switching across multiple boards connected to Home Assistant.


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

- check the COM port number

## After cloning the repo

1. Set up the Python environment:
   ```
   uv sync
   ```

2. Each board directory under `configurations/` needs a `secrets.yaml` file (gitignored).
   Copy the example and fill in your credentials:
   ```
   cp configurations/board_beczka/secrets.yaml.example configurations/board_beczka/secrets.yaml
   cp configurations/board_szklarnia/secrets.yaml.example configurations/board_szklarnia/secrets.yaml
   cp configurations/board_marcin/secrets.yaml.example configurations/board_marcin/secrets.yaml
   cp configurations/board_siren/secrets.yaml.example configurations/board_siren/secrets.yaml
   cp configurations/board_squirt/secrets.yaml.example configurations/board_squirt/secrets.yaml
   ```

3. Edit each `secrets.yaml` with real WiFi and OTA credentials.

4. Use the board management tool:
   ```bash
   # List available boards and detected serial ports
   uv run python board.py list

   # Compile a single board
   uv run python board.py compile beczka

   # Upload via auto-detected serial port
   uv run python board.py upload beczka

   # Upload to a specific port or IP
   uv run python board.py upload beczka --device COM3                       # Windows
   uv run python board.py upload beczka --device /dev/cu.usbserial-0001    # macOS
   uv run python board.py upload jezus --device 192.168.1.107              # OTA via IP

   # Compile, upload and show logs
   uv run python board.py run szklarnia --device COM3

   # Compile all boards at once
   uv run python board.py compile-all
   ```

   Or use esphome directly:
   ```
   uv run esphome compile configurations/<board_dir>/<config>.yaml
   uv run esphome upload configurations/<board_dir>/<config>.yaml --device /dev/cu.usbserial-0001
   ```

## how to set the WiFi ssid and pass


Main yaml file.

```yaml
wifi:
  ssid: !secret wifi_ssid
  password: !secret wifi_password
```

secrets.yaml

```yaml
# WiFi credentials
wifi_ssid: "SSID"
wifi_password: "password"

# OTA update password
ota_password: "password"
```


## Project structure

```
configurations/
  common/
    base.yaml           # Shared ESP32 base: wifi, OTA, web server, logging, API
    monitoring.yaml     # Shared diagnostics: wifi signal, uptime, network info
  board_beczka/         # Water barrel level monitor
  board_szklarnia/      # Greenhouse soil & temperature monitor
  board_marcin/         # Sprinkler controller (3 zones)
  board_siren/          # 4-channel switch (mermaid)
  board_squirt/         # 4-channel switch + temperature
board.py                # Cross-platform build/upload tool (Windows + macOS)
```


## Board DNESP32

Check `GND`. The esp modue should be placed right to the left side, close to the middle 8 pin.

```
----------------------
    xxxxxxxxxxxxxxxx|
	  xxxxxxxxxxxxxxxx|
    xxxxxxxxxxxxxxxx|
----------------------

```

|Board hole | Board green | esp | gpio   |
|-----------|-------------|-----|--------|
|8 				  | 16 					| D2  | GPIO02 |
|9 				  | 17 					| D4  | GPIO04 |
|10				  | 5  					| Rx2 | GPIO16 |
|11         | 18 					| Tx2 | GPIO17 |
|12         | 19 					| D5  | GPIO5  |
|5          | 2 					| 3v3 | -      |
|6          | 0 					| gnd | -      |


-------------------


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

To convert any ADC reading (let's call it _X_) into a moisture percentage, you can use the following formula:

\[
\text{Moisture \%} = \frac{(2891 - X)}{(2891 - 1198)} \times 100
\]

Here, the denominator is the range (2891 – 1198 = 1693). With this formula:
- An ADC reading equal to **2891** yields 0% moisture.
- An ADC reading equal to **1198** yields 100% moisture.


## Configurations

Each board has its own directory under `configurations/`. Every directory contains a `secrets.yaml` (gitignored) for WiFi and OTA credentials, and one or more device YAML files. Shared configuration (base settings, monitoring sensors) lives in `configurations/common/`.

To set up a new board, copy `secrets.yaml.example` to `secrets.yaml` in the board directory and fill in real credentials.

### board_beczka - Water barrel level monitor

Monitors water level in a rain barrel using three float switches at different heights. Reports high/mid/low water levels as binary sensors to Home Assistant, enabling automations like pump control or low-water alerts.

#### beczka.yaml

| Setting | Value |
|---|---|
| Board | esp32dev (Arduino) |
| Hostname | `beczka-esp` |
| Web server | port 80 (v3) |
| Secrets | `wifi_ssid`, `wifi_password`, `ota_password` |

**Sensors (binary, GPIO input with pullup):**

| Name | GPIO | Wire color |
|---|---|---|
| level_high | GPIO21 | blue |
| level_mid | GPIO19 | yellow |
| level_low | GPIO18 | red |

Power wire: black.

### board_szklarnia - Greenhouse soil & temperature monitor

Monitors soil moisture and air temperature inside a greenhouse. An ADC capacitive sensor reads raw soil moisture which is converted to a 0-100% scale using calibrated dry/wet values. A Dallas 1-Wire sensor reads temperature. A pump output allows automatic or manual irrigation. A binary alert fires when soil moisture drops below 30%.

#### szklarnia.yaml

| Setting | Value |
|---|---|
| Board | esp32dev (Arduino) |
| Hostname | `szklarnia-esp` |
| Web server | port 80 (v3) |
| Secrets | `wifi_ssid`, `wifi_password`, `ota_password` |

**Sensors:**

| Name | Type | Pin |
|---|---|---|
| Soil Moisture Raw | ADC (raw, 12dB) | GPIO36 |
| Soil Moisture | Template (% from raw) | - |
| temperatura | Dallas 1-Wire | GPIO4 |

**Outputs:**

| Name | GPIO |
|---|---|
| pompa | GPIO16 |

**Alerts:** Low Soil Moisture Alert triggers below 30%.

### board_marcin - Sprinkler controller

Automated 3-zone lawn/garden sprinkler system with a shared pump. The ESPHome sprinkler component handles sequencing through sections A, B, C with configurable run durations (default 900s each), auto-advance, and pump start/stop delays. A Dallas temperature sensor provides ambient readings.

#### jezus.yaml

| Setting | Value |
|---|---|
| Board | esp32dev (Arduino) |
| Hostname | `jezus-esp` |
| Web server | port 80 (v3) |
| BLE Improv | enabled |
| Secrets | `wifi_ssid`, `wifi_password`, `ota_password` |

**Sensors:**

| Name | Type | Pin |
|---|---|---|
| temperature | Dallas 1-Wire | GPIO4 |
| WiFi Signal | wifi_signal | - |
| Uptime | uptime (seconds) | - |

**Sprinkler valves (900s run duration each):**

| Valve | Switch GPIO | Pump GPIO |
|---|---|---|
| Section A | GPIO21 | GPIO5 |
| Section B | GPIO19 | GPIO5 |
| Section C | GPIO18 | GPIO5 |

### board_siren - 4-channel switch (mermaid)

General-purpose 4-channel relay/switch board. Each output can be independently toggled from Home Assistant or the built-in web interface. Used for controlling lights, pumps, or other on/off loads around the garden.

#### siren.yaml

| Setting | Value |
|---|---|
| Board | esp32dev (Arduino) |
| Hostname | `mermaid-esp` |
| Web server | port 80 (v3) |
| BLE Improv | enabled |
| Secrets | `wifi_ssid`, `wifi_password`, `ota_password` |

**Switches:**

| Name | GPIO |
|---|---|
| mermaid_01 | GPIO02 |
| mermaid_02 | GPIO04 |
| mermaid_03 | GPIO16 |
| mermaid_04 | GPIO17 |

### board_squirt - 4-channel switch + temperature

Same as board_siren but adds a Dallas 1-Wire temperature sensor for environmental monitoring alongside the 4 switching channels.

#### squirt.yaml

| Setting | Value |
|---|---|
| Board | esp32dev (Arduino) |
| Hostname | `squirt-esp` |
| Web server | port 80 (v3) |
| BLE Improv | enabled |
| Secrets | `wifi_ssid`, `wifi_password`, `ota_password` |

**Sensors:**

| Name | Type | Pin |
|---|---|---|
| temperature | Dallas 1-Wire | GPIO5 |
| WiFi Signal | wifi_signal | - |
| Uptime | uptime (seconds) | - |

**Switches:**

| Name | GPIO |
|---|---|
| squirt_01 | GPIO02 |
| squirt_02 | GPIO04 |
| squirt_03 | GPIO16 |
| squirt_04 | GPIO17 |
