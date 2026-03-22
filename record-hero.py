#!/usr/bin/env python3
"""
Build the website hero screencast as an asciicast v2 file.

CLI parts are synthesized for clean output (no draft-mode warnings, no agency noise).
TUI parts are captured from real `wg tui` via tmux at 110x38.
"""

import json
import os
import random
import subprocess
import time

COLS = 110
ROWS = 38
CAST_FILE = "/home/erik/graphwork.github.io/public/wg-demo.cast"
DEMO_REPO = "/home/erik/wg-demo"
SESSION = "wg-hero-tui"

# Dim gray for prompt
DIM = "\x1b[38;5;240m"
RST = "\x1b[0m"
GREEN = "\x1b[32m"
YELLOW = "\x1b[33m"
WHITE = "\x1b[37m"
GRAY = "\x1b[90m"
BOLD = "\x1b[1m"
DIM2 = "\x1b[2m"
CYAN = "\x1b[36m"


class CastBuilder:
    def __init__(self):
        self.frames = []
        self.t = 0.0  # current time

    def advance(self, dt):
        self.t += dt

    def frame(self, content):
        """Add a frame: clear screen + content.
        Uses cursor positioning per line to avoid bare-LF rendering issues."""
        lines = content.split('\n')
        parts = ["\x1b[H\x1b[2J"]
        for i, line in enumerate(lines[:ROWS]):
            parts.append(f"\x1b[{i+1};1H{line}")
        output = "".join(parts)
        self.frames.append([round(self.t, 3), "o", output])

    def build_screen(self, lines):
        """Build a full screen from lines (pad to ROWS height). Does not mutate input.
        Uses explicit cursor positioning to avoid CR/LF issues in asciinema-player."""
        padded = list(lines)  # copy to avoid mutation
        while len(padded) < ROWS:
            padded.append("")
        parts = []
        for i, line in enumerate(padded[:ROWS]):
            parts.append(f"\x1b[{i+1};1H{line}")
        return "".join(parts)

    def type_command(self, cmd, existing_lines, typing_speed=0.04):
        """Animate typing a command after existing output lines."""
        prompt = f"{DIM}${RST} "
        for i in range(1, len(cmd) + 1):
            partial = cmd[:i]
            screen_lines = list(existing_lines) + [prompt + partial]
            self.frame(self.build_screen(screen_lines))
            # Vary speed: every 3rd char is faster
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


def capture_tui_frames():
    """Launch real wg tui in tmux and capture navigation frames."""
    frames = {}

    def tmux(*args):
        return subprocess.run(["tmux"] + list(args), capture_output=True, text=True)

    def cap():
        return tmux("capture-pane", "-t", SESSION, "-p", "-e").stdout

    tmux("kill-session", "-t", SESSION)
    tmux("new-session", "-d", "-s", SESSION, "-x", str(COLS), "-y", str(ROWS), "-c", DEMO_REPO)
    tmux("resize-window", "-t", SESSION, "-x", str(COLS), "-y", str(ROWS))
    time.sleep(0.5)
    tmux("send-keys", "-t", SESSION, "wg tui --recording 2>/dev/null", "Enter")
    time.sleep(3)

    # Initial
    frames["init"] = cap()

    # Navigate down 1-7
    for i in range(1, 8):
        tmux("send-keys", "-t", SESSION, "j")
        time.sleep(0.4)
        frames[f"down-{i}"] = cap()

    # Navigate up 1-3
    for i in range(1, 4):
        tmux("send-keys", "-t", SESSION, "k")
        time.sleep(0.4)
        frames[f"up-{i}"] = cap()

    # Enter to inspect
    tmux("send-keys", "-t", SESSION, "Enter")
    time.sleep(1.5)
    frames["inspect"] = cap()

    # Detail tab
    tmux("send-keys", "-t", SESSION, "1")
    time.sleep(1)
    frames["detail"] = cap()

    # Log tab
    tmux("send-keys", "-t", SESSION, "2")
    time.sleep(1)
    frames["log"] = cap()

    # Back to Chat
    tmux("send-keys", "-t", SESSION, "0")
    time.sleep(0.5)
    frames["chat"] = cap()

    # Tab to panel
    tmux("send-keys", "-t", SESSION, "Tab")
    time.sleep(0.5)
    frames["panel"] = cap()

    # Scroll panel
    for i in range(1, 4):
        tmux("send-keys", "-t", SESSION, "j")
        time.sleep(0.3)
    frames["panel-scrolled"] = cap()

    # Tab back
    tmux("send-keys", "-t", SESSION, "Tab")
    time.sleep(0.5)
    frames["back"] = cap()

    # Navigate to different tasks
    for i in range(1, 5):
        tmux("send-keys", "-t", SESSION, "j")
        time.sleep(0.4)
        frames[f"final-{i}"] = cap()

    # Exit
    tmux("send-keys", "-t", SESSION, "q")
    time.sleep(1)
    frames["exit"] = cap()

    tmux("kill-session", "-t", SESSION)
    print(f"Captured {len(frames)} TUI frames")
    return frames


def get_viz_output():
    """Get the viz output from the demo repo (with ANSI colors)."""
    # Capture via tmux to preserve colors
    def tmux(*args):
        return subprocess.run(["tmux"] + list(args), capture_output=True, text=True)

    tmux("kill-session", "-t", "wg-viz")
    tmux("new-session", "-d", "-s", "wg-viz", "-x", str(COLS), "-y", str(ROWS), "-c", DEMO_REPO)
    tmux("resize-window", "-t", "wg-viz", "-x", str(COLS), "-y", str(ROWS))
    time.sleep(0.5)
    tmux("send-keys", "-t", "wg-viz", "-l", "PROMPT='$ ' RPS1='' RPROMPT=''")
    tmux("send-keys", "-t", "wg-viz", "Enter")
    time.sleep(0.3)
    tmux("send-keys", "-t", "wg-viz", "clear", "Enter")
    time.sleep(0.5)
    tmux("send-keys", "-t", "wg-viz", "wg viz", "Enter")
    time.sleep(2)
    result = tmux("capture-pane", "-t", "wg-viz", "-p", "-e").stdout
    tmux("kill-session", "-t", "wg-viz")
    return result


def build_cast():
    random.seed(42)
    cast = CastBuilder()

    prompt = f"{DIM}${RST} "

    # ════════════════════════════════════════════════
    # Act 1: Init (~8s)
    # ════════════════════════════════════════════════
    print("Building Act 1: Init...")

    # Clean prompt, brief pause
    cast.frame(cast.build_screen([prompt]))
    cast.advance(1.0)

    # Type "wg init"
    cast.type_command("wg init", [])

    # Press Enter, show output
    cast.advance(0.15)
    init_output = [
        f"{DIM}${RST} wg init",
        f"Initialized workgraph at {BOLD}.workgraph{RST}",
        f"{GREEN}Agency is ready.{RST} The service will now auto-assign agents to tasks.",
        f"  Next: {CYAN}wg service start{RST}",
        "",
        prompt,
    ]
    cast.frame(cast.build_screen(init_output))
    cast.advance(2.0)

    # ════════════════════════════════════════════════
    # Act 2: Build the graph (~18s)
    # ════════════════════════════════════════════════
    print("Building Act 2: Build the graph...")

    # Each add command: type, show clean output
    adds = [
        ('wg add "Design API schema"', "design-api-schema", None),
        ('wg add "Set up database" --after design-api-schema', "set-up-database", "design-api-schema"),
        ('wg add "Build auth module" --after design-api-schema', "build-auth-module", "design-api-schema"),
        ('wg add "Recipe CRUD" --after set-up-database --verify "cargo test passes"', "recipe-crud", "set-up-database"),
        ('wg add "Integration tests" --after recipe-crud,build-auth-module', "integration-tests", "recipe-crud,build-auth-module"),
    ]

    running_lines = list(init_output[:-1])  # Remove trailing prompt

    for cmd, task_id, after in adds:
        cast.type_command(cmd, running_lines, typing_speed=0.03)
        cast.advance(0.15)

        # Show result
        running_lines.append(f"{DIM}${RST} {cmd}")
        running_lines.append(f"Added task: {BOLD}{task_id}{RST}")
        running_lines.append("")

        # If screen is getting full, trim top
        if len(running_lines) > ROWS - 3:
            running_lines = running_lines[3:]

        cast.frame(cast.build_screen(running_lines + [prompt]))
        cast.advance(0.6)

    # Show wg viz
    cast.advance(0.3)
    cast.type_command("wg viz", running_lines, typing_speed=0.04)
    cast.advance(0.15)

    # For viz output, use the real viz from the demo repo (has nice state with mixed statuses)
    print("Capturing real viz output...")
    viz_raw = get_viz_output()
    cast.frame(viz_raw)
    cast.advance(5.0)  # Let viewer absorb the graph

    # Show wg service start
    viz_lines = viz_raw.split("\n")
    # Remove trailing empty lines from viz
    while viz_lines and not viz_lines[-1].strip():
        viz_lines.pop()
    cast.type_command("wg service start", viz_lines, typing_speed=0.04)
    cast.advance(0.15)

    # Show service start output
    service_lines = list(viz_lines)
    service_lines.append(f"{DIM}${RST} wg service start")
    service_lines.append(f"{GREEN}Service started.{RST} Coordinator polling every 60s.")
    service_lines.append(f"  Dispatching agents to ready tasks...")
    service_lines.append("")
    service_lines.append(prompt)
    cast.frame(cast.build_screen(service_lines))
    cast.advance(2.0)

    # ════════════════════════════════════════════════
    # Act 3: TUI showcase (~30s)
    # ════════════════════════════════════════════════
    print("Capturing TUI frames...")
    tui = capture_tui_frames()

    # Type "wg tui"
    cast.type_command("wg tui", service_lines[:-1], typing_speed=0.04)
    cast.advance(0.15)

    # TUI launch
    cast.frame(tui["init"])
    cast.advance(3.0)  # Let viewer absorb the full TUI layout

    # Navigate down through tasks
    for i in range(1, 6):
        cast.frame(tui[f"down-{i}"])
        cast.advance(0.55)

    cast.advance(1.5)  # Pause to read

    # Navigate back up
    for i in range(1, 3):
        cast.frame(tui[f"up-{i}"])
        cast.advance(0.45)

    cast.advance(0.6)

    # Inspect a task (Enter)
    cast.frame(tui["inspect"])
    cast.advance(2.5)

    # Detail tab
    cast.frame(tui["detail"])
    cast.advance(2.5)

    # Log tab
    cast.frame(tui["log"])
    cast.advance(2.0)

    # Back to chat
    cast.frame(tui["chat"])
    cast.advance(1.0)

    # Tab to panel
    cast.frame(tui["panel"])
    cast.advance(0.6)

    cast.frame(tui["panel-scrolled"])
    cast.advance(1.2)

    # Back to graph
    cast.frame(tui["back"])
    cast.advance(0.6)

    # Navigate to different tasks
    for i in range(1, 5):
        cast.frame(tui[f"final-{i}"])
        cast.advance(0.55)

    cast.advance(2.5)  # Final pause on TUI

    # Exit TUI
    cast.frame(tui["exit"])
    cast.advance(1.5)

    cast.save()


if __name__ == "__main__":
    build_cast()
