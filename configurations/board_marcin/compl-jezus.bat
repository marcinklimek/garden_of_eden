@echo off
uv run esphome compile jezus.yaml
rem uv run esphome upload jezus.yaml  --device COM3
uv run esphome run jezus.yaml  --device 192.168.1.107