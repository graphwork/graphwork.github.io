# Feature: Cycles — dependency cycles with iteration support
# Run: vhs screencasts/features/cycles.tape
Output screencasts/features/cycles.gif

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

# Show cycles via CLI
Type "wg cycles"
Sleep 300ms
Enter
Sleep 2.5s

Type "wg viz ci-checks"
Sleep 300ms
Enter
Sleep 2.5s

Screenshot screencasts/features/cycles.png

Sleep 1s
