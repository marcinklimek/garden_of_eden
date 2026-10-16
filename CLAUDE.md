# garden_of_eden

garden_of_eden is an ESP32 garden automation set: ESPHome firmware for five boards (watering, soil and water-level sensing, switching) that connect to Home Assistant. The owner flashes and runs the boards on real hardware; a change is done when `board.py compile-all` passes and the owner has checked the affected board on the device.

## Profile

Values the kit rules refer to. Keep each line short and true. Delete a line that does not apply.

| Key | Value |
|---|---|
| owner language | Polish (full diacritics) |
| start folder | the repository root (Claude Code loads `.claude/` and `.mcp.json` only from the start folder) |
| stack | Python 3.12 (uv, `pyproject.toml`) with esphome >=2025.3.0; ESP32 boards configured in YAML under `configurations/`; legacy Arduino sketch in `src/sketch_jun23a/` |
| checks | `uv run python board.py compile-all` (compiles every `board_*` config under `configurations/`; needs each board's `secrets.yaml`) |
| check pass means | exit code 0 and the line "All N boards compiled successfully." (`board.py`, `cmd_compile_all`) |
| risky paths | `configurations/common/` (shared by all boards), `configurations/board_*/*.yaml` (pins and actuators) |
| owner approval | GPIO pin assignments, watering and siren behaviour, OTA and WiFi settings; changes that need a physical flash |
| push targets | see `.claude/kit.json` `guard.pushAllow` |
| board | GitHub project created by `kit.py board setup`, config `.claude/board/board.json` |
| glossary | default `docs/CONTEXT.md` (skill `domain-modeling`) |
| decisions | ADR folder, default `docs/decisions/` (skill `domain-modeling`) |
| tools dir | `board.py` (compile, upload and run helper) |
| libraries to re-check | esphome (YAML component options change between releases) |
| forbidden | `configurations/board_*/secrets.yaml` (WiFi and OTA credentials, git-ignored) and `.esphome/` (generated build output) |

## Invariants

Testable statements that every change keeps. Review checks each one the change can touch.

- INVARIANT: every board configuration under `configurations/` compiles with ESPHome. Check: `uv run python board.py compile-all`.

## Overrides

Deviations from kit rules. Everything not listed follows the kit. One entry per deviation:

- Overrides kit `<rule>.md` (<what the kit says>): <what this project does>. Reason: <why>.

## Project rules

Project-specific rules that are short go here. Longer ones go to `.claude/rules/<name>.md`
(project-owned files next to the kit links in `.claude/rules/kit/`).

<!-- kit:begin (managed by kit.py sync; do not edit) -->
## Kit

This project uses claude-workflow-kit as Claude Code plugins (marketplace `claude-workflow-kit`): `kit-core`, `kit-board`.
Kit rules arrive as SessionStart context from the plugins. Setup and update steps: the kit `SETUP.md`.
Kit rules apply; project files narrow them. A deviation from a kit rule is valid only as an entry in `## Overrides` of this file.
<!-- kit:end -->
