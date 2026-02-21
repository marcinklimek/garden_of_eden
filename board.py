#!/usr/bin/env python3
"""Cross-platform build and upload tool for Garden of Eden ESPHome boards.

Usage:
    uv run python board.py list
    uv run python board.py compile <board>
    uv run python board.py upload <board> [--device <port_or_ip>]
    uv run python board.py run <board> [--device <port_or_ip>]
    uv run python board.py compile-all
"""

import argparse
import glob
import os
import platform
import subprocess
import sys

CONFIGURATIONS_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), "configurations")


def find_boards():
    """Discover all board directories and their YAML config files."""
    boards = {}
    for entry in sorted(os.listdir(CONFIGURATIONS_DIR)):
        if not entry.startswith("board_"):
            continue
        board_dir = os.path.join(CONFIGURATIONS_DIR, entry)
        if not os.path.isdir(board_dir):
            continue
        yamls = sorted(
            f
            for f in os.listdir(board_dir)
            if f.endswith(".yaml") and f != "secrets.yaml" and f != "secrets.yaml.example"
        )
        for yaml_file in yamls:
            board_name = yaml_file.removesuffix(".yaml")
            boards[board_name] = os.path.join(board_dir, yaml_file)
    return boards


def detect_serial_ports():
    """List available serial ports on the current platform."""
    system = platform.system()
    ports = []
    if system == "Darwin":
        ports = sorted(glob.glob("/dev/cu.usbserial-*") + glob.glob("/dev/cu.usbmodem*"))
    elif system == "Linux":
        ports = sorted(glob.glob("/dev/ttyUSB*") + glob.glob("/dev/ttyACM*"))
    elif system == "Windows":
        # Scan COM1-COM20
        for i in range(1, 21):
            port = f"COM{i}"
            try:
                import serial

                s = serial.Serial(port)
                s.close()
                ports.append(port)
            except Exception:
                pass
        if not ports:
            # Fallback: suggest common ports without pyserial
            ports = ["COM3"]
    return ports


def run_esphome(command, config_path, device=None):
    """Run an esphome command via uv."""
    cmd = ["uv", "run", "esphome", command, config_path]
    if device and command in ("upload", "run"):
        cmd.extend(["--device", device])
    print(f">>> {' '.join(cmd)}")
    return subprocess.call(cmd)


def cmd_list(args):
    boards = find_boards()
    if not boards:
        print("No boards found.")
        return 1
    print("Available boards:\n")
    for name, path in boards.items():
        rel = os.path.relpath(path)
        print(f"  {name:<20s} {rel}")

    ports = detect_serial_ports()
    if ports:
        print(f"\nDetected serial ports: {', '.join(ports)}")
    else:
        print("\nNo serial ports detected.")
    return 0


def cmd_compile(args):
    boards = find_boards()
    name = args.board
    if name not in boards:
        print(f"Unknown board: {name}")
        print(f"Available: {', '.join(boards)}")
        return 1
    return run_esphome("compile", boards[name])


def cmd_upload(args):
    boards = find_boards()
    name = args.board
    if name not in boards:
        print(f"Unknown board: {name}")
        print(f"Available: {', '.join(boards)}")
        return 1

    device = args.device
    if not device:
        ports = detect_serial_ports()
        if len(ports) == 1:
            device = ports[0]
            print(f"Auto-detected serial port: {device}")
        elif len(ports) > 1:
            print(f"Multiple serial ports found: {', '.join(ports)}")
            print("Please specify one with --device")
            return 1
        else:
            print("No serial port detected. Please specify with --device <port_or_ip>")
            return 1

    return run_esphome("upload", boards[name], device)


def cmd_run(args):
    boards = find_boards()
    name = args.board
    if name not in boards:
        print(f"Unknown board: {name}")
        print(f"Available: {', '.join(boards)}")
        return 1

    device = args.device
    if not device:
        ports = detect_serial_ports()
        if len(ports) == 1:
            device = ports[0]
            print(f"Auto-detected serial port: {device}")
        elif len(ports) > 1:
            print(f"Multiple serial ports found: {', '.join(ports)}")
            print("Please specify one with --device")
            return 1
        else:
            print("No serial port detected. Please specify with --device <port_or_ip>")
            return 1

    return run_esphome("run", boards[name], device)


def cmd_compile_all(args):
    boards = find_boards()
    if not boards:
        print("No boards found.")
        return 1

    failed = []
    for name, path in boards.items():
        print(f"\n{'='*60}")
        print(f"Compiling: {name}")
        print(f"{'='*60}")
        rc = run_esphome("compile", path)
        if rc != 0:
            failed.append(name)

    print(f"\n{'='*60}")
    if failed:
        print(f"FAILED: {', '.join(failed)}")
        return 1
    else:
        print(f"All {len(boards)} boards compiled successfully.")
        return 0


def main():
    parser = argparse.ArgumentParser(
        description="Garden of Eden - ESPHome board management tool"
    )
    sub = parser.add_subparsers(dest="command")

    sub.add_parser("list", help="List available boards and serial ports")

    p_compile = sub.add_parser("compile", help="Compile a board configuration")
    p_compile.add_argument("board", help="Board name (e.g. beczka, siren)")

    p_upload = sub.add_parser("upload", help="Upload firmware to a board")
    p_upload.add_argument("board", help="Board name")
    p_upload.add_argument("--device", help="Serial port or IP address (auto-detected if omitted)")

    p_run = sub.add_parser("run", help="Compile, upload and show logs")
    p_run.add_argument("board", help="Board name")
    p_run.add_argument("--device", help="Serial port or IP address (auto-detected if omitted)")

    sub.add_parser("compile-all", help="Compile all board configurations")

    args = parser.parse_args()

    if not args.command:
        parser.print_help()
        return 1

    handlers = {
        "list": cmd_list,
        "compile": cmd_compile,
        "upload": cmd_upload,
        "run": cmd_run,
        "compile-all": cmd_compile_all,
    }

    return handlers[args.command](args)


if __name__ == "__main__":
    sys.exit(main())
