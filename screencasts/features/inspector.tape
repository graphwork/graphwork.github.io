# Feature: Inspector panel — multi-tab detail view
# Run: vhs screencasts/features/inspector.tape
Output screencasts/features/inspector.gif

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

# Navigate to an in-progress task for more detail
Down
Sleep 300ms
Down
Sleep 300ms
Down
Sleep 300ms
Down
Sleep 300ms

# Switch to Detail tab
Type "1"
Sleep 1.5s

# Cycle through a few tabs to show the multi-tab nature
# Switch to Log tab
Type "2"
Sleep 1s

# Switch to Agency tab
Type "4"
Sleep 1s

# Back to Detail tab
Type "1"
Sleep 1s

Screenshot screencasts/features/inspector.png

Sleep 1s
