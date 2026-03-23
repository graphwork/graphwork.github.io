#!/usr/bin/env python3
"""
Capture TUI screenshots via tmux, then render with VHS using JetBrains Mono.

Strategy:
1. Run wg tui in a fixed-size tmux session
2. Navigate with tmux send-keys (reliable key delivery)
3. Capture each frame with tmux capture-pane -e (preserves ANSI escapes)
4. Save captured content to files
5. Use VHS to render each captured frame as a PNG with JetBrains Mono
"""

import subprocess
import time
import sys
import os

COLS = 140
ROWS = 40
SESSION = "wg-features"
WORKDIR = "/home/erik/wg-demo"
OUTPUT_DIR = "/home/erik/graphwork.github.io/public/features"
TAPE_DIR = "/home/erik/graphwork.github.io/tapes"


def tmux(*args):
    return subprocess.run(["tmux"] + list(args), capture_output=True, text=True)


def send(keys, literal=False):
    args = ["send-keys", "-t", SESSION]
    if literal:
        args.append("-l")
    args.append(keys)
    tmux(*args)


def capture():
    result = tmux("capture-pane", "-t", SESSION, "-p", "-e")
    return result.stdout


def setup():
    tmux("kill-session", "-t", SESSION)
    tmux("new-session", "-d", "-s", SESSION,
         "-x", str(COLS), "-y", str(ROWS), "-c", WORKDIR)
    tmux("resize-window", "-t", SESSION, "-x", str(COLS), "-y", str(ROWS))
    time.sleep(0.5)


def cleanup():
    tmux("kill-session", "-t", SESSION)


def save_frame(content, name):
    """Save captured frame to a text file for VHS rendering."""
    path = f"/tmp/tui-frame-{name}.txt"
    with open(path, "w") as f:
        f.write(content)
    print(f"  Saved frame: {name} ({len(content)} chars)")
    return path


def render_with_vhs(frame_path, output_png, name):
    """Use VHS to render a captured frame as a PNG with JetBrains Mono."""
    tape = f'''Output "/tmp/{name}-render.gif"
Set Shell "bash"
Set FontFamily "JetBrains Mono"
Set FontSize 16
Set Width 1400
Set Height 800
Set Padding 20
Set Theme {{ "name": "dark", "black": "#1a1a2e", "red": "#ef4444", "green": "#22c55e", "yellow": "#eab308", "blue": "#3b82f6", "magenta": "#a855f7", "cyan": "#06b6d4", "white": "#e4e4e7", "brightBlack": "#71717a", "brightRed": "#f87171", "brightGreen": "#4ade80", "brightYellow": "#facc15", "brightBlue": "#60a5fa", "brightMagenta": "#c084fc", "brightCyan": "#22d3ee", "brightWhite": "#f4f4f5", "background": "#18181b", "foreground": "#d4d4d8", "selectionBackground": "#3f3f46", "cursorColor": "#a855f7" }}

Hide
Type "cat '{frame_path}'"
Enter
Sleep 1s
Show
Sleep 500ms
Screenshot "{output_png}"
Sleep 500ms
'''
    tape_path = f"/tmp/{name}-render.tape"
    with open(tape_path, "w") as f:
        f.write(tape)

    result = subprocess.run(["vhs", tape_path], capture_output=True, text=True)
    if result.returncode != 0:
        print(f"  VHS error for {name}: {result.stderr}")
        return False
    print(f"  Rendered: {output_png}")
    return True


def capture_tui_screenshots():
    """Navigate TUI and capture screenshots at key states."""
    setup()

    # Launch TUI
    print("Launching TUI...")
    send("wg tui --recording 2>/dev/null", literal=True)
    send("Enter")
    time.sleep(4)

    frames = {}

    # 1. Dashboard: default view with task selected
    print("Capturing dashboard...")
    send("j")
    time.sleep(0.4)
    send("j")
    time.sleep(0.4)
    send("j")
    time.sleep(0.5)
    frames["dashboard"] = capture()

    # 2. Graph explorer: navigate through more of the graph
    print("Capturing graph explorer...")
    send("j")
    time.sleep(0.3)
    send("j")
    time.sleep(0.3)
    send("j")
    time.sleep(0.3)
    send("k")
    time.sleep(0.3)
    send("k")
    time.sleep(0.5)
    frames["graph-explorer"] = capture()

    # 3. Inspector: Tab to inspector, show Detail tab
    print("Capturing inspector...")
    # First navigate back to recipe-crud
    send("k")
    time.sleep(0.3)
    send("k")
    time.sleep(0.3)
    # Tab to inspector pane
    send("Tab")
    time.sleep(0.5)
    # Try pressing 1 for Detail tab (when inspector is focused)
    send("1")
    time.sleep(0.5)
    frames["inspector"] = capture()

    # 4. Chat: show Messages tab
    print("Capturing chat/messages...")
    send("3")
    time.sleep(0.5)
    frames["chat"] = capture()

    # Exit TUI
    send("Tab")
    time.sleep(0.3)
    send("q")
    time.sleep(1)

    cleanup()
    return frames


def main():
    print("=== Capturing TUI frames via tmux ===")
    frames = capture_tui_screenshots()

    # Save frames to files
    frame_files = {}
    for name, content in frames.items():
        frame_files[name] = save_frame(content, name)

    print(f"\n=== Rendering {len(frame_files)} frames with VHS + JetBrains Mono ===")
    for name, frame_path in frame_files.items():
        output_png = f"{OUTPUT_DIR}/{name}.png"
        render_with_vhs(frame_path, output_png, name)

    print("\nDone!")


if __name__ == "__main__":
    main()
