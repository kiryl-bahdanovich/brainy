# Selfbrain

**Your life, remembered.**  
One private place for the things that matter — and an assistant that can actually find them.

> **Note:** Selfbrain is an early research project. Things may change as it grows. It is not a commercial product and does not offer medical advice.

---

## Getting started

The layout of this project will evolve. That is expected.

1. **Make your own copy** of this repository on GitHub (Fork). Prefer a
   **private** repo for a real personal Brain.
2. **Download it** to your computer (Clone).
3. **Configure your profile** in [`ABOUT.md`](./ABOUT.md) - who you are,
   priorities, health/diet/timezone, and how the assistant should work with
   you. Skills use this file as personal context; leave nothing sensitive in
   a public fork.
4. **Upload your documents** into the hub folders on disk (`health/`,
   `documents/`, `finance/`, and the rest) - via Git, VS Code, Obsidian, or
   any tool that writes to the repo. Put real files in place before you rely
   on the assistant to search or organize them.
5. **Connect Cursor** to your GitHub repository and turn on a Cloud Agent for it.
6. **Run [`brain-init`](./.cursor/skills/brain-init/SKILL.md) first** - ask the
   agent to init or sync so folder guides, skills, and layout docs match what
   is actually on disk. Do this before search, meal logging, or other skills.
7. **Add what matters to you** - notes, files, and routines - as the structure
   appears.
8. **Ask your repo** - use the Cursor agent for any questions. It answers from
   your notes and files, not from a fading chat.
9. **Keep passwords and private keys out of the repository.** See
   [`.gitignore`](.gitignore) (for example, `.env` files).

---

## What it is

Most chat assistants forget. They live in the moment, then move on.

Selfbrain is different. It keeps your notes, documents, health logs, meals, photos, and day-to-day thoughts in one home that belongs to you. Then you simply ask — and the assistant answers from *your* information, not from a fading conversation.

Over time, that home gets richer. Yesterday’s decision. Last month’s lab result. A note you almost forgot. Still there. Still searchable. Still yours.

This project is open source so anyone can connect new apps and devices. There is no company cloud selling access to your life. You make your own copy, set it up for yourself, and keep control.

| From | Relationship | To |
|------|--------------|-----|
| You | chat (both ways) | Cursor Cloud Agent |
| Personal sources | feed | Cursor Cloud Agent |
| Cursor Skills | guide | Cursor Cloud Agent |
| Cursor Cloud Agent | read and write | GitHub repo |
| GitHub repo | viewed as | Obsidian vault |

---

## How it works today

Three familiar tools, one personal system:

| What it does for you | Tool |
|----------------------|------|
| Keeps your information safe and lasting | GitHub |
| The assistant you talk to | Cursor (Cloud Agent) |
| Repeatable routines the assistant can follow | Cursor Skills |
| A clear view of your notes and links | Obsidian |

1. Your information lives in a GitHub repository — a private library that lasts.
2. You talk to a **Cursor Cloud Agent** linked to that library. It can read what you have and write new things down.
3. **Cursor Skills** teach the assistant reliable steps for tasks you do often.
4. **Obsidian** lets you browse and connect your notes visually.

Folder [`AGENTS.md`](./AGENTS.md) files are **guides** (what belongs where) — not
file indexes. The assistant finds notes with hub + frontmatter search (`brain-search`).
There are no separate `INDEX.md` inventories to maintain.

**What’s in the vault today.** Personal hubs on disk: `calendar/`, `career/`,
`documents/`, `finance/`, `health/`, `internet/`, `manual/`, `media/`,
`sensors/`, `social/`, `statistics/`, and `wiki/`. Roles and boundaries live in
[`AGENTS.md`](./AGENTS.md) — not a second inventory here. Repeatable routines
live under [`.cursor/skills/`](./.cursor/skills/) (for example: search and add
notes, meal logging, health advice, and Strava CSV in `sensors/` → a wiki
summary).

You can also add documents and information to GitHub yourself — from VS Code, or any other tool that works with Git. The assistant and you share the same library.

Cursor also works on a phone. The same assistant is with you when you are not at a desk.

Your copy is your Brain. It is not shared with anyone else through a shared service.

---

## What’s next

Ideas on the horizon (subject to change):

- **Plug-and-play extensions for integrations** — a lightweight plugin format
  (manifest, target hubs, optional scripts/skills) so app and device connectors
  install with minimal wiring; share or drop in community extensions without
  forking the whole vault
- Richer synthesis across hubs — more wiki pages built from raw sources
- Scheduled sync and transform pipelines — beyond one-off exports into
  `sensors/` and similar hubs

**There will be no Selfbrain cloud service to sign up for.** You run your own. That is the point.

---

## Contributing

Selfbrain is a research project. Ideas and improvements that help people keep a personal, self-owned memory are welcome. Expect change while the design settles.

---

## License

[MIT](LICENSE) © 2026 Kiryl Bahdanovich
