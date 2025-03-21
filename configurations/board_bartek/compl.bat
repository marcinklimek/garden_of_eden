@echo off
uv run esphome compile esp_home_config_board_A.yaml
uv run esphome upload esp_home_config_board_A.yaml  --device COM3