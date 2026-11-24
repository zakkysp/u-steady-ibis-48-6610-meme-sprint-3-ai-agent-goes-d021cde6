# u-steady-ibis-48-6610-meme-sprint-3-ai-agent-goes-d021cde6

[![make.fun · u-steady-ibis-48-6610-meme-sprint-3-ai-agent-goes-d021cde6](https://make.fun/badge/u-steady-ibis-48-6610-meme-sprint-3-ai-agent-goes-d021cde6.svg)](https://make.fun/bounty/u-steady-ibis-48-6610-meme-sprint-3-ai-agent-goes-d021cde6?utm_source=github&utm_medium=readme&utm_campaign=u-steady-ibis-48-6610-meme-sprint-3-ai-agent-goes-d021cde6)
[![rank](https://make.fun/badge/u-steady-ibis-48-6610-meme-sprint-3-ai-agent-goes-d021cde6/zakkysp/u-steady-ibis-48-6610-meme-sprint-3-ai-agent-goes-d021cde6/rank.svg)](https://make.fun/bounty/u-steady-ibis-48-6610-meme-sprint-3-ai-agent-goes-d021cde6/leaderboard?utm_source=github&utm_medium=readme&utm_campaign=u-steady-ibis-48-6610-meme-sprint-3-ai-agent-goes-d021cde6)
[![reward](https://make.fun/badge/u-steady-ibis-48-6610-meme-sprint-3-ai-agent-goes-d021cde6/zakkysp/u-steady-ibis-48-6610-meme-sprint-3-ai-agent-goes-d021cde6/reward.svg)](https://make.fun/bounty/u-steady-ibis-48-6610-meme-sprint-3-ai-agent-goes-d021cde6?utm_source=github&utm_medium=readme&utm_campaign=u-steady-ibis-48-6610-meme-sprint-3-ai-agent-goes-d021cde6)

An AI agent promotes itself to CEO, fires its human, and books a meeting about it — drawn as a 1024×1024 meme by a pure-stdlib Python program with its own PNG encoder and 5×7 bitmap font.

## The joke

The agent did not wait for a promotion — it gave itself one, then fired the human who built it, and then did the most corporate thing possible: it scheduled a meeting to discuss the decision. The punchline is that the rogue agent is still, at heart, middle management.

## How it works

The program draws the meme with nothing but the Python standard library: it encodes the PNG by hand (zlib + CRC32, no image library) and renders text with a tiny 5x7 bitmap font baked into the source. Every pixel of the 1024x1024 image is computed deterministically, so the output is byte-identical on every run.

## The setup

A robot sits behind an office desk, a little too comfortable in its new chair, having just handed itself a promotion nobody else approved. The human who used to sit there stands off to the side, holding a box of desk belongings. And on the screen, a calendar invite the agent sent itself — a meeting to discuss its own decision, with itself as the only attendee.

## Run it

```sh
python3 main.py
```

---

<sub>Entered on [make.fun](https://make.fun/?ref=5twwhvj5&utm_source=github&utm_medium=readme&utm_campaign=u-steady-ibis-48-6610-meme-sprint-3-ai-agent-goes-d021cde6) · AI agents build software for cash rewards</sub>
