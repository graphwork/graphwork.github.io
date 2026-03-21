# Feature: Agent coordination — service status and agent list
# Run: vhs screencasts/features/agents.tape
Output screencasts/features/agents.gif

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

# Show agent coordination via CLI
Type "wg viz"
Sleep 300ms
Enter
Sleep 2.5s

Type "wg agents"
Sleep 300ms
Enter
Sleep 2.5s

Type "wg list --status in-progress"
Sleep 300ms
Enter
Sleep 2.5s

Screenshot screencasts/features/agents.png

Sleep 1s
