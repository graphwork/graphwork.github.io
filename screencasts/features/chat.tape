# Feature: Chat — inline messaging to coordinator
# Run: vhs screencasts/features/chat.tape
Output screencasts/features/chat.gif

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

# Launch TUI — default starts on Chat tab
Type "wg tui --no-mouse"
Sleep 300ms
Enter
Sleep 2s

# Navigate to impl-users which has a message
Down
Sleep 300ms
Down
Sleep 300ms
Down
Sleep 300ms
Down
Sleep 300ms

# Stay on Chat tab (tab 0 — already default)
# Switch to Messages tab to see task messages
Type "3"
Sleep 1.5s

Screenshot screencasts/features/chat.png

Sleep 1s
