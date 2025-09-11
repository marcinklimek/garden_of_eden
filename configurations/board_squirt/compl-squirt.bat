@echo off
uv run esphome compile squirt.yaml
uv run esphome upload squirt.yaml  --device COM3
rem uv run esphome run squirt.yaml  --device 192.168.1.107