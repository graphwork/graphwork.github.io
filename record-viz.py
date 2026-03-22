#!/usr/bin/env python3
"""Build a short wg viz screencast as an asciicast v2 file."""

import json
import random
import subprocess
import time

COLS = 70
ROWS = 20
CAST_FILE = "/home/erik/graphwork.github.io/public/wg-viz.cast"
DEMO_REPO = "/home/erik/wg-demo"
SESSION = "wg-viz-rec"

DIM = "\x1b[38;5;240m"
RST = "\x1b[0m"


class CastBuilder:
    def __init__(self):
        self.frames = []
        self.t = 0.0

    def advance(self, dt):
        self.t += dt

    def frame(self, content):
        output = "\x1b[H\x1b[2J" + content
        self.frames.append([round(self.t, 3), "o", output])

    def build_screen(self, lines):
        padded = list(lines)
        while len(padded) < ROWS:
            padded.append("")
        return "\n".join(padded[:ROWS])

    def type_command(self, cmd, existing_lines, typing_speed=0.04):
        prompt = f"{DIM}${RST} "
        for i in range(1, len(cmd) + 1):
            partial = cmd[:i]
            screen_lines = list(existing_lines) + [prompt + partial]
            self.frame(self.build_screen(screen_lines))
            if i % 3 == 0:
                self.advance(typing_speed * 0.6)
            else:
                self.advance(typing_speed + random.uniform(-0.01, 0.015))

    def save(self):
        header = {
            "version": 2,
            "width": COLS,
            "height": ROWS,
            "timestamp": int(time.time()),
            "env": {"SHELL": "/bin/zsh", "TERM": "xterm-256color"},
        }
        with open(CAST_FILE, "w") as f:
            f.write(json.dumps(header) + "\n")
            for fr in self.frames:
                f.write(json.dumps(fr) + "\n")
        total = self.frames[-1][0] if self.frames else 0
        print(f"Saved {len(self.frames)} frames ({total:.1f}s) → {CAST_FILE}")


def capture_cmd(cmd):
    """Run a command in tmux and capture colored output."""
    def tmux(*args):
        return subprocess.run(["tmux"] + list(args), capture_output=True, text=True)

    tmux("kill-session", "-t", SESSION)
    tmux("new-session", "-d", "-s", SESSION, "-x", str(COLS), "-y", str(ROWS), "-c", DEMO_REPO)
    tmux("resize-window", "-t", SESSION, "-x", str(COLS), "-y", str(ROWS))
    time.sleep(0.5)
    tmux("send-keys", "-t", SESSION, "-l", "PROMPT='$ ' RPS1='' RPROMPT=''")
    tmux("send-keys", "-t", SESSION, "Enter")
    time.sleep(0.3)
    tmux("send-keys", "-t", SESSION, "clear", "Enter")
    time.sleep(0.5)
    tmux("send-keys", "-t", SESSION, cmd, "Enter")
    time.sleep(2)
    result = tmux("capture-pane", "-t", SESSION, "-p", "-e").stdout
    tmux("kill-session", "-t", SESSION)
    return result


def build_cast():
    random.seed(42)
    cast = CastBuilder()
    prompt = f"{DIM}${RST} "

    # Initial prompt
    cast.frame(cast.build_screen([prompt]))
    cast.advance(0.8)

    # Type and run "wg status"
    cast.type_command("wg status", [], typing_speed=0.04)
    cast.advance(0.15)

    print("Capturing wg status...")
    status_raw = capture_cmd("wg status")
    cast.frame(status_raw)
    cast.advance(3.0)

    # Extract lines for context
    status_lines = status_raw.split("\n")
    while status_lines and not status_lines[-1].strip():
        status_lines.pop()

    # Type and run "wg viz"
    cast.type_command("wg viz", status_lines, typing_speed=0.04)
    cast.advance(0.15)

    print("Capturing wg viz...")
    viz_raw = capture_cmd("wg viz")
    cast.frame(viz_raw)
    cast.advance(5.0)

    # Hold the viz output on screen before looping
    cast.frame(viz_raw)
    cast.advance(2.0)

    cast.save()


if __name__ == "__main__":
    build_cast()
