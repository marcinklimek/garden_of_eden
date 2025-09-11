@echo off
uv run esphome compile siren.yaml
uv run esphome upload siren.yaml  --device COM3
rem uv run esphome run siren.yaml  --device 192.168.1.107