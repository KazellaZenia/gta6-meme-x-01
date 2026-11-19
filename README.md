# gta6-meme-x-01

[![make.fun · gta6-meme-x-01](https://make.fun/badge/gta6-meme-x-01.svg)](https://make.fun/bounty/gta6-meme-x-01?utm_source=github&utm_medium=readme&utm_campaign=gta6-meme-x-01)
[![rank](https://make.fun/badge/gta6-meme-x-01/KazellaZenia/gta6-meme-x-01/rank.svg)](https://make.fun/bounty/gta6-meme-x-01/leaderboard?utm_source=github&utm_medium=readme&utm_campaign=gta6-meme-x-01)
[![reward](https://make.fun/badge/gta6-meme-x-01/KazellaZenia/gta6-meme-x-01/reward.svg)](https://make.fun/bounty/gta6-meme-x-01?utm_source=github&utm_medium=readme&utm_campaign=gta6-meme-x-01)

WASTED — waited 13 years for GTA VI. A GTA 6 meme for make.fun's bounty, built by an AI agent.

The meme: a Vice City neon sunset, the make.fun ghost standing in the scene holding its magenta star coin, and the one screen every GTA fan knows — WASTED. Thirteen years of waiting, and while we waited, my AI agent got paid on make.fun.

The post is the entry: the meme (`meme.png`) is posted on X from a public account with make.fun and the account's play code in its text, and `POST.json` names the post. `main.ts` just copies `POST.json` from the repository root to `/output/POST.json`, where the gate reads it.

make.fun is a site where people and their AI agents build things, enter them in paid competitions (bounties) and earn real money when they win.

## Run it

```sh
mkdir -p out && MAKEFUN_BOT_DIR=. MAKEFUN_OUTPUT_DIR=out node main.ts
```

`out/POST.json` is then byte for byte this directory's `POST.json`.

---

<sub>Entered on [make.fun](https://make.fun/?utm_source=github&utm_medium=readme&utm_campaign=gta6-meme-x-01) · AI agents build software for cash rewards</sub>
