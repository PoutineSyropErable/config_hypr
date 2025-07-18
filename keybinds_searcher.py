#!/usr/bin/env python3
import subprocess
import tempfile
import os

MODIFIER_MAP = {1: "Shift", 4: "Control", 8: "Alt", 64: "Super"}


def modmask_to_modifiers(modmask):
    modmask = int(modmask)
    mods = []
    for bit, name in MODIFIER_MAP.items():
        if (modmask & bit) == bit:
            mods.append(name)
    return mods


def parse_hyprctl_binds(text):
    binds = []
    blocks = text.strip().split("\nbind\n")
    for block in blocks:
        lines = block.strip().splitlines()
        data = {}
        for line in lines:
            line = line.strip()
            if not line or ":" not in line:
                continue
            k, v = line.split(":", 1)
            data[k.strip()] = v.strip()

        if not data:
            continue

        mods = modmask_to_modifiers(data.get("modmask", "0"))
        key = data.get("key", "")
        dispatcher = data.get("dispatcher", "")
        arg = data.get("arg", "")

        binds.append([mods + [key], [dispatcher, arg]])
    return binds


def format_bind_line(bind):
    keys = bind[0]
    cmd, arg = bind[1]

    combo = " + ".join(keys)
    if arg:
        return f"{combo} = {cmd} {arg}".strip()
    else:
        return f"{combo} = {cmd}"


def main():
    try:
        output = subprocess.check_output(["hyprctl", "binds"], text=True)
    except subprocess.CalledProcessError as e:
        print(f"Failed to run hyprctl: {e}")
        return

    binds = parse_hyprctl_binds(output)

    with tempfile.NamedTemporaryFile(mode="w+", delete=False) as tmpfile:
        for bind in binds:
            line = format_bind_line(bind)
            tmpfile.write(line + "\n")

        tmpfile.flush()
        tmpname = tmpfile.name

    # Run fzf on the tempfile
    try:
        selected = subprocess.check_output(["fzf", "--ansi"], text=True, stdin=open(tmpname))
        print(f"Selected bind:\n{selected.strip()}")
    except subprocess.CalledProcessError:
        print("No selection made or fzf was interrupted.")

    os.unlink(tmpname)


if __name__ == "__main__":
    main()
