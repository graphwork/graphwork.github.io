# Feature: Graph Explorer — tree view with dependency arrows
# Run: vhs screencasts/features/graph-explorer.tape
Output screencasts/features/graph-explorer.gif

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

# Press = twice to cycle to Off mode (full graph, no inspector)
# Default: TwoThirdsInspector → FullInspector → Off
Type "="
Sleep 500ms
Type "="
Sleep 2s

# Navigate through the graph
Down
Sleep 500ms
Down
Sleep 500ms
Down
Sleep 500ms
Up
Sleep 500ms

Screenshot screencasts/features/graph-explorer.png

Sleep 1s
