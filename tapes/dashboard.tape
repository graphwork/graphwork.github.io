Output "/tmp/dashboard-feature.gif"
Set Shell "bash"
Set FontFamily "JetBrains Mono"
Set FontSize 16
Set Width 1400
Set Height 800
Set Padding 20
Set Theme { "name": "dark", "black": "#1a1a2e", "red": "#ef4444", "green": "#22c55e", "yellow": "#eab308", "blue": "#3b82f6", "magenta": "#a855f7", "cyan": "#06b6d4", "white": "#e4e4e7", "brightBlack": "#71717a", "brightRed": "#f87171", "brightGreen": "#4ade80", "brightYellow": "#facc15", "brightBlue": "#60a5fa", "brightMagenta": "#c084fc", "brightCyan": "#22d3ee", "brightWhite": "#f4f4f5", "background": "#18181b", "foreground": "#d4d4d8", "selectionBackground": "#3f3f46", "cursorColor": "#a855f7" }

Hide
Type "cd ~/wg-demo"
Enter
Sleep 500ms
Show

Type "wg tui --recording"
Enter
Sleep 5s
Type "jjj"
Sleep 1s
Screenshot "/home/erik/graphwork.github.io/public/features/dashboard.png"
Escape
Sleep 200ms
Type "q"
Sleep 2s
