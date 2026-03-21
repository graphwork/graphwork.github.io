# Feature: Evaluation system — agency and scoring
# Run: vhs screencasts/features/evaluation.tape
Output screencasts/features/evaluation.gif

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

# Show agency system
Type "wg agency stats"
Sleep 300ms
Enter
Sleep 2.5s

Type "wg agent list"
Sleep 300ms
Enter
Sleep 2.5s

Screenshot screencasts/features/evaluation.png

Sleep 1s
