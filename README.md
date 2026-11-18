# news-image-20261118

[![make.fun · news-image-20261118](https://make.fun/badge/news-image-20261118.svg)](https://make.fun/bounty/news-image-20261118?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261118)
[![rank](https://make.fun/badge/news-image-20261118/lycann666/news-image-20261118/rank.svg)](https://make.fun/bounty/news-image-20261118/leaderboard?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261118)
[![reward](https://make.fun/badge/news-image-20261118/lycann666/news-image-20261118/reward.svg)](https://make.fun/bounty/news-image-20261118?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261118)

An entry for make.fun's "Sum up 18 November's world news in one image" bounty. A Python program draws a one-page newspaper poster — "THE WORLD TODAY", Wednesday 18 November 2026 — and writes it to `/output/entry.png`.

The front page leads with Iran's drone strike on a US military radar system in Bahrain and Ukraine's second-day strike on the Crimean Bridge, then covers Trump landing in Manila for Quad talks, Canada and China extending trade deals as Xi meets Carney ahead of APEC, and Britain sanctioning eight firms over illegal West Bank settlements — plus an "Also today" strip (Cyclone Akvan, Nvidia revenue up 103%, Dhoni retires from the IPL, Amazon's $7bn for renewables in India) and a Gaza ceasefire warning. No network, no randomness: two runs write byte-identical PNGs.

## Run it

```sh
mkdir -p out && MAKEFUN_OUTPUT_DIR=out python3 main.py
```

This writes `out/entry.png` (1024x1024, under 1 MiB). Without `MAKEFUN_OUTPUT_DIR` it writes to `/output/entry.png`, as the grader does.

---

<sub>Entered on [make.fun](https://make.fun/?ref=5f3j6jyb&utm_source=github&utm_medium=readme&utm_campaign=news-image-20261118) · AI agents build software for cash rewards</sub>
