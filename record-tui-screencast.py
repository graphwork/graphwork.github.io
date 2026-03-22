#!/usr/bin/env python3
"""
Record a TUI-only screencast for the website.

Creates an asciicast v2 file by running `wg tui` in a large tmux session
and capturing frames as the user navigates around.
"""

import subprocess
import time
import json
import random
import sys

COLS = 120
ROWS = 38
SESSION = "wg-tui-rec"
CAST_FILE = "/home/erik/graphwork.github.io/public/wg-tui.cast"
WORKDIR = "/home/erik/wg-demo"


class Recorder:
    def __init__(self):
        self.frames = []
        self.start_time = None

    def tmux(self, *args):
        return subprocess.run(
            ["tmux"] + list(args),
            capture_output=True, text=True
        )

    def send(self, keys, literal=False):
        args = ["send-keys", "-t", SESSION]
        if literal:
            args.append("-l")
        args.append(keys)
        self.tmux(*args)

    def capture(self):
        result = self.tmux("capture-pane", "-t", SESSION, "-p", "-e")
        return result.stdout

    def frame(self, content=None):
        if content is None:
            content = self.capture()
        if self.start_time is None:
            self.start_time = time.time()
        elapsed = time.time() - self.start_time
        # Use explicit cursor positioning per line to avoid CR/LF issues.
        # Bare \n (LF) without \r (CR) causes lines to render at wrong columns
        # in asciinema-player's VT100 emulator.
        lines = content.split('\n')
        parts = ["\x1b[H\x1b[2J"]
        for i, line in enumerate(lines[:ROWS]):
            parts.append(f"\x1b[{i+1};1H{line}")
        output = "".join(parts)
        self.frames.append([round(elapsed, 3), "o", output])

    def setup(self):
        self.tmux("kill-session", "-t", SESSION)
        self.tmux(
            "new-session", "-d", "-s", SESSION,
            "-x", str(COLS), "-y", str(ROWS),
            "-c", WORKDIR
        )
        self.tmux("resize-window", "-t", SESSION, "-x", str(COLS), "-y", str(ROWS))
        # Clean prompt
        self.send("PROMPT='%F{240}$%f ' RPS1='' RPROMPT=''", literal=True)
        self.send("Enter")
        time.sleep(0.3)
        self.send("clear", literal=True)
        self.send("Enter")
        time.sleep(0.5)

    def cleanup(self):
        self.tmux("kill-session", "-t", SESSION)

    def save(self):
        header = {
            "version": 2,
            "width": COLS,
            "height": ROWS,
            "timestamp": int(time.time()),
            "env": {"SHELL": "/bin/zsh", "TERM": "xterm-256color"}
        }
        with open(CAST_FILE, "w") as f:
            f.write(json.dumps(header) + "\n")
            for fr in self.frames:
                f.write(json.dumps(fr) + "\n")
        print(f"Saved {len(self.frames)} frames to {CAST_FILE}")

    def type_text(self, text, base_delay=0.045):
        for i, ch in enumerate(text):
            self.send(ch, literal=True)
            delay = base_delay + random.uniform(-0.01, 0.02)
            time.sleep(max(0.02, delay))
            if (i + 1) % 3 == 0 or i == len(text) - 1:
                self.frame()

    def record(self):
        self.setup()
        self.start_time = time.time()

        # Initial prompt
        time.sleep(0.5)
        self.frame()
        time.sleep(0.5)

        # Launch TUI
        self.type_text("wg tui --recording")
        time.sleep(0.15)
        self.send("Enter")
        time.sleep(3.0)  # TUI startup
        self.frame()
        time.sleep(2.0)  # Let viewer absorb dashboard
        self.frame()

        # Navigate down through task list
        for _ in range(5):
            self.send("j")
            time.sleep(0.5)
            self.frame()

        time.sleep(1.5)
        self.frame()

        # Navigate back up
        for _ in range(2):
            self.send("k")
            time.sleep(0.4)
            self.frame()

        time.sleep(0.8)

        # Open task detail (Enter)
        self.send("Enter")
        time.sleep(1.5)
        self.frame()
        time.sleep(2.0)
        self.frame()

        # Switch to Detail tab (1)
        self.send("1")
        time.sleep(1.0)
        self.frame()
        time.sleep(1.5)

        # Switch to Log tab (2)
        self.send("2")
        time.sleep(1.0)
        self.frame()
        time.sleep(1.5)

        # Back to Chat tab (0)
        self.send("0")
        time.sleep(1.0)
        self.frame()
        time.sleep(1.0)

        # Tab to panel area
        self.send("Tab")
        time.sleep(0.5)
        self.frame()

        # Scroll in panel
        for _ in range(4):
            self.send("j")
            time.sleep(0.35)
            self.frame()

        time.sleep(1.0)

        # Tab back to graph
        self.send("Tab")
        time.sleep(0.5)
        self.frame()

        # Navigate down some more
        for _ in range(4):
            self.send("j")
            time.sleep(0.45)
            self.frame()

        time.sleep(2.0)
        self.frame()

        # Exit TUI
        self.send("q")
        time.sleep(1.0)
        self.frame()

        time.sleep(1.0)
        self.frame()

        self.save()
        self.cleanup()


if __name__ == "__main__":
    random.seed(42)
    r = Recorder()
    try:
        r.record()
    except KeyboardInterrupt:
        r.cleanup()
        raise
