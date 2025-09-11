@echo off
uv run esphome compile szklarnia.yaml
uv run esphome upload szklarnia.yaml  --device COM3