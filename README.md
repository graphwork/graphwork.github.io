# graphwork.github.io

Workgraph project website, built with [Astro](https://astro.build/).

## Development

```bash
npm install
npm run dev     # Start dev server
npm run build   # Production build
```

## Screencasts

TUI screencasts are generated automatically using [VHS](https://github.com/charmbracelet/vhs).

### Prerequisites

- **vhs** — Download from [releases](https://github.com/charmbracelet/vhs/releases) or `go install github.com/charmbracelet/vhs@latest`
- **ttyd** — Download from [releases](https://github.com/tsl0922/ttyd/releases) or `brew install ttyd`
- **ffmpeg** — `apt install ffmpeg` or `brew install ffmpeg`
- **wg** — `cargo install --path /path/to/workgraph`

### Re-recording after TUI changes

```bash
make screencast
# or directly:
./screencasts/record.sh
```

This runs the VHS tape file (`screencasts/demo.tape`) which:
1. Sets up a temporary workgraph project with sample tasks
2. Shows the ASCII dependency graph (`wg viz`)
3. Launches the TUI and navigates through task list, graph view, inspector, search, and help
4. Outputs `screencasts/demo.gif` and `screencasts/demo.webm`
5. Copies outputs to `public/` so Astro can serve them on the landing page

### Editing the demo

Edit `screencasts/demo.tape` to change what the screencast shows. The tape uses VHS declarative syntax — see [VHS documentation](https://github.com/charmbracelet/vhs#vhs) for the full command reference.

To change the sample project (tasks, dependencies, status), edit `screencasts/setup-demo.sh`.
