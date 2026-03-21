# Feature: Dashboard view — split-pane tasks + agents
# Run: vhs screencasts/features/dashboard.tape
Output screencasts/features/dashboard.gif

Require wg
Require bash

Set Shell "bash"
Set FontSize 15
Set FontFamily "JetBrains Mono"
Set Width 1400
Set Height 800
Set Padding 8
Set Theme "Catppuccin Mocha"
Set WindowBar Colorful
Set WindowBarSize 40

# Setup
Hide
Type "export PATH=$HOME/.local/bin:$HOME/.cargo/bin:$PATH"
Enter
Sleep 500ms
Type "bash screencasts/features/setup-features-demo.sh /tmp/wg-features-demo 2>/dev/null"
Enter
Sleep 3s
Type "cd /tmp/wg-features-demo"
Enter
Sleep 500ms
Type "clear"
Enter
Sleep 500ms
Show

# Launch TUI
Type "wg tui --no-mouse"
Sleep 300ms
Enter
Sleep 2s

# Switch to Detail tab (key 1) for a richer view
Type "1"
Sleep 1s

# Navigate through tasks
Down
Sleep 400ms
Down
Sleep 400ms
Down
Sleep 400ms
Down
Sleep 400ms
Up
Sleep 400ms
Up
Sleep 600ms

Screenshot screencasts/features/dashboard.png

Sleep 1s
