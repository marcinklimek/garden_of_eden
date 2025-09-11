@echo off
uv run esphome compile beczka.yaml
uv run esphome upload beczka.yaml  --device COM3