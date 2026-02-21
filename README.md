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

- check the COM port number

## After cloning the repo

1. Set up the Python environment:
   ```
   uv sync
   ```

2. Each board directory under `configurations/` needs a `secrets.yaml` file (gitignored).
   Copy the example and fill in your credentials:
   ```
   cp configurations/board_bartek/secrets.yaml.example configurations/board_bartek/secrets.yaml
   cp configurations/board_marcin/secrets.yaml.example configurations/board_marcin/secrets.yaml
   cp configurations/board_siren/secrets.yaml.example configurations/board_siren/secrets.yaml
   cp configurations/board_squirt/secrets.yaml.example configurations/board_squirt/secrets.yaml
   ```

3. Edit each `secrets.yaml` with real WiFi and OTA credentials.

4. Compile and upload:
   ```
   uv run esphome compile configurations/<board_dir>/<config>.yaml
   uv run esphome upload configurations/<board_dir>/<config>.yaml --device /dev/cu.usbserial-0001
   ```

## how to set the WiFi ssid and pass


Main yaml file.

```shell
wifi:
  ssid: !secret wifi_ssid
  password: !secret wifi_password
```

secrets.yaml

```shell
# WiFi credentials
wifi_ssid: "SSID"
wifi_password: "password"
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

Each board has its own directory under `configurations/`. Every directory contains a `secrets.yaml` (gitignored) for WiFi and OTA credentials, and one or more device YAML files.

To set up a new board, copy `secrets.yaml.example` to `secrets.yaml` in the board directory and fill in real credentials.

### board_bartek

#### beczka.yaml

Water barrel level monitor.

| Setting | Value |
|---|---|
| Board | esp32dev (Arduino) |
| Hostname | `beczka` |
| Web server | port 80 |
| Secrets | `wifi_ssid`, `wifi_password` |

**Sensors (binary, GPIO input with pullup):**

| Name | GPIO |
|---|---|
| level_high | GPIO21 |
| level_mid | GPIO19 |
| level_low | GPIO18 |

#### szklarnia.yaml

Greenhouse soil moisture + temperature monitor with pump control.

| Setting | Value |
|---|---|
| Board | esp32dev (Arduino) |
| Hostname | `szklarnia` |
| Web server | port 80 |
| Secrets | `wifi_ssid`, `wifi_password` |

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

### board_marcin

#### jezus.yaml

Sprinkler controller with 3 valve zones, pump, and temperature sensor.

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

### board_siren

#### siren.yaml

4-channel GPIO switch controller (named "mermaid").

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

### board_squirt

#### squirt.yaml

4-channel GPIO switch controller with temperature sensor.

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
