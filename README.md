# EXOS AGENT

**Exos Agent** — an AI coding agent for the terminal: interactive chat, full tool access (read/write/search/bash/web), custom themes, and web/TUI interfaces. 100% open source under the MIT license.

```
                                   ▄
█▀▀ █ █ █▀█ █▀▀ █▀█ █▀▀ █▀▀ █▀█ ▀█▀
█▀   █  █ █ ▀▀█ █▀█ █▀█ █▀  █ █  █
▀▀▀  ▀  ▀▀▀ ▀▀▀ ▀ ▀ ▀▀▀ ▀▀▀ ▀ ▀  ▀
```

## ✨ Features

- **Interactive chat in the terminal** (`exos-agent chat`) — real back-and-forth conversation with session memory; ask, get answers, let it act on your codebase, keep going.
- **Rich TUI** (`exos-agent`) — full-screen terminal UI with custom Exos theme, markdown rendering, diffs, and session management.
- **One-shot runs** (`exos-agent run "..."`) — for scripts and CI.
- **Full toolset**: file read/write/edit, glob/grep search, bash execution, todos, web fetch & web search, sub-agents.
- **OpenAI-compatible providers** — point it at any compatible endpoint via `exos-agent.json`.
- **Sessions** — resume, fork, and search past conversations (`--continue`, `--session`).

## 🚀 Quick start

```bash
# interactive chat session (tui-free, in-terminal)
exos-agent chat

# continue your last chat session
exos-agent chat --continue

# full-screen TUI
exos-agent

# one-shot
exos-agent run "explain this repo"
```

## ⚙️ Configuration

`~/.config/exos-agent/exos-agent.json`:

```json
{
  "provider": {
    "my-provider": {
      "npm": "@ai-sdk/openai-compatible",
      "options": { "baseURL": "http://127.0.0.1:8787/v1", "apiKey": "public" },
      "models": { "my-model": { "name": "My Model", "tools": true } }
    }
  },
  "model": "my-provider/my-model",
  "theme": "exos"
}
```

Custom themes live in `~/.config/exos-agent/themes/<name>.json`.

## 🏗️ Build from source

Requires [Bun](https://bun.sh):

```bash
git clone <this repo>
cd exos-repo
bun install
cd packages/exos-agent
EXOS_AGENT_VERSION=1.18.4 EXOS_AGENT_CHANNEL=latest \
  bun run script/build.ts --single --skip-embed-web-ui
# binary: packages/exos-agent/dist/exos-agent-linux-x64/bin/exos-agent
```

## 📦 Repository layout

| Path | ما بيحتوي |
|---|---|
| `packages/exos-agent` | CLI, agent loop, tools, server |
| `packages/tui` | Terminal UI (OpenTUI), themes, logo |
| `packages/core` | sessions, catalog, providers |
| `packages/protocol` | wire protocol & event schemas |
| `packages/vendor/*` | vendored & rebranded auth/provider plugins (GitLab, Poe, gitlab-ai-provider) |
| `packages/sdk` `packages/ui` `packages/server` … | SDK, shared UI, server pieces |

## 📄 License

MIT — see [LICENSE](LICENSE).
