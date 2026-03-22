#!/usr/bin/env python3
"""
Record a real wg tui screencast using tmux capture-pane.

Creates an asciicast v2 file by:
1. Running real wg commands in a fixed-size tmux session
2. Capturing pane content (with ANSI escape codes) at key moments
3. Building the .cast file from captured frames

The resulting screencast shows the REAL wg tui, not scripted output.
"""

import subprocess
import time
import json
import random
import sys

COLS = 55
ROWS = 35
SESSION = "wg-rec"
CAST_FILE = "/home/erik/graphwork.github.io/public/wg-demo.cast"
WORKDIR = "/home/erik/workgraph"


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
        """Send keys to the tmux session."""
        args = ["send-keys", "-t", SESSION]
        if literal:
            args.append("-l")
        args.append(keys)
        self.tmux(*args)

    def capture(self):
        """Capture the current pane content with escape codes."""
        result = self.tmux("capture-pane", "-t", SESSION, "-p", "-e")
        return result.stdout

    def frame(self, content=None):
        """Add a frame to the recording."""
        if content is None:
            content = self.capture()
        if self.start_time is None:
            self.start_time = time.time()
        elapsed = time.time() - self.start_time
        # Clear screen and redraw from top-left
        output = "\x1b[H\x1b[2J" + content
        self.frames.append([round(elapsed, 3), "o", output])

    def type_text(self, text, base_delay=0.045):
        """Type text character by character with realistic timing."""
        for i, ch in enumerate(text):
            self.send(ch, literal=True)
            delay = base_delay + random.uniform(-0.01, 0.02)
            time.sleep(max(0.02, delay))
            # Capture every 3rd character and the last one
            if (i + 1) % 3 == 0 or i == len(text) - 1:
                self.frame()

    def setup(self):
        """Create tmux session with clean prompt at exact size."""
        self.tmux("kill-session", "-t", SESSION)
        self.tmux(
            "new-session", "-d", "-s", SESSION,
            "-x", str(COLS), "-y", str(ROWS),
            "-c", WORKDIR
        )
        # Force exact window/pane size (tmux -x/-y isn't always honored)
        self.tmux("resize-window", "-t", SESSION, "-x", str(COLS), "-y", str(ROWS))
        # Use zsh-compatible prompt (PROMPT, not PS1 with bash escapes)
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

    def record(self):
        self.setup()
        self.start_time = time.time()

        # ── Act 1: CLI intro (~15s) ───────────────────────────
        # Initial clean prompt
        time.sleep(0.5)
        self.frame()
        time.sleep(1.0)

        # wg status — show the live system
        self.type_text("wg status")
        time.sleep(0.1)
        self.send("Enter")
        time.sleep(2.5)
        self.frame()
        time.sleep(4.0)  # Let viewer read the output
        self.frame()

        # ── Act 2: TUI showcase (~35s, the main event) ───────
        self.type_text("wg tui --recording")
        time.sleep(0.15)
        self.send("Enter")
        time.sleep(3.0)  # TUI startup
        self.frame()
        time.sleep(2.5)  # Let viewer absorb the dashboard
        self.frame()

        # Navigate down through task tree
        for _ in range(7):
            self.send("j")
            time.sleep(0.5)
            self.frame()

        time.sleep(1.5)
        self.frame()

        # Navigate back up
        for _ in range(3):
            self.send("k")
            time.sleep(0.4)
            self.frame()

        time.sleep(0.8)

        # Inspect a task (Enter)
        self.send("Enter")
        time.sleep(1.5)
        self.frame()
        time.sleep(2.5)  # Let viewer read task detail
        self.frame()

        # Switch to Detail tab (1)
        self.send("1")
        time.sleep(1.0)
        self.frame()
        time.sleep(2.0)

        # Switch to Log tab (2)
        self.send("2")
        time.sleep(1.0)
        self.frame()
        time.sleep(2.0)

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
        for _ in range(6):
            self.send("j")
            time.sleep(0.45)
            self.frame()

        time.sleep(2.5)  # Final pause on TUI
        self.frame()

        # Exit TUI
        self.send("q")
        time.sleep(1.0)
        self.frame()

        # ── Act 3: CLI outro (~5s) ───────────────────────────
        time.sleep(2.0)
        self.frame()

        # Save the recording
        self.save()
        self.cleanup()


if __name__ == "__main__":
    random.seed(42)  # Reproducible typing timing
    r = Recorder()
    try:
        r.record()
    except KeyboardInterrupt:
        r.cleanup()
        raise
