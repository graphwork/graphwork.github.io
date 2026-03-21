# Workgraph TUI Demo — Automated screencast
# Run: vhs screencasts/demo.tape
# Produces: screencasts/demo.gif and screencasts/demo.webm

Output screencasts/demo.gif
Output screencasts/demo.webm

Require wg
Require bash

Set Shell "bash"
Set FontSize 16
Set FontFamily "JetBrains Mono"
Set Width 1400
Set Height 800
Set Padding 12
Set Framerate 24
Set TypingSpeed 40ms
Set Theme "Catppuccin Mocha"
Set WindowBar Colorful
Set WindowBarSize 40

# --- Setup: create demo project (hidden) ---
Hide
Type "export PATH=$HOME/.local/bin:$HOME/.cargo/bin:$PATH"
Enter
Sleep 500ms
Type "bash screencasts/setup-demo.sh /tmp/wg-demo 2>/dev/null"
Enter
Sleep 2s
Type "cd /tmp/wg-demo"
Enter
Sleep 500ms
Type "clear"
Enter
Sleep 500ms
Show

# --- Scene 1: Show the task graph in the terminal ---
Type "wg viz"
Sleep 500ms
Enter
Sleep 3s

# --- Scene 2: Launch the TUI ---
Type "wg tui --no-mouse"
Sleep 500ms
Enter
Sleep 2s

# --- Scene 3: Navigate the task list ---
# Move down through tasks
Down
Sleep 600ms
Down
Sleep 600ms
Down
Sleep 600ms
Down
Sleep 600ms
Down
Sleep 600ms

# --- Scene 4: Toggle right panel (inspector) ---
Type "\"
Sleep 1.5s

# Scroll through tasks to show inspector updates
Up
Sleep 800ms
Up
Sleep 800ms
Up
Sleep 800ms
Down
Sleep 800ms
Down
Sleep 800ms

# --- Scene 5: Switch to graph view ---
# Press Tab to switch to graph pane
Tab
Sleep 2s

# Navigate in graph view
Down
Sleep 600ms
Down
Sleep 600ms
Up
Sleep 600ms

# --- Scene 6: Cycle layout mode ---
Type "="
Sleep 2s

# --- Scene 7: Toggle back to split view ---
Type "="
Sleep 2s

# --- Scene 8: Show help overlay ---
Type "?"
Sleep 3s

# Dismiss help
Escape
Sleep 1s

# --- Scene 9: Search for a task ---
Type "/"
Sleep 500ms
Type "pipeline"
Sleep 1s
Enter
Sleep 1.5s

# Clear search
Escape
Sleep 1s

# --- Final: hold on the view ---
Sleep 2s

# Quit
Type "q"
Sleep 500ms
