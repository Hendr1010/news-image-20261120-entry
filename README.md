# The World in One Day — Friday 20 November 2026

[![news-image-20261120](https://make.fun/badge/news-image-20261120.svg)](https://make.fun/bounty/news-image-20261120?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261120)
[![rank](https://make.fun/badge/news-image-20261120/Hendr1010/news-image-20261120-entry/rank.svg)](https://make.fun/bounty/news-image-20261120?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261120)
[![reward](https://make.fun/badge/news-image-20261120/Hendr1010/news-image-20261120-entry/reward.svg)](https://make.fun/bounty/news-image-20261120?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261120)

A one-image front page summing up the world's news of Friday 20 November 2026, entered in [news-image-20261120](https://make.fun/bounty/news-image-20261120) on make.fun.

## The page

- **Hero — GTA 6 tops $1.8 billion.** Rockstar's Vice City epic passes The Odyssey's global run in a day.
- **Peace pact.** Trump, Xi and Putin sign a declaration after the historic Shenzhen summit.
- **Court: Myanmar genocide.** The UN court rules the military meant to destroy the Rohingya.
- **Iran call pushed to 2027.** Trump says no rush: "see what happens" after Jan 1.
- **Cyclone Akvan hits India.** 300,000 evacuated as the storm nears Odisha.
- **Voyager 1: one light-day.** NASA confirms the probe's distance milestone.
- **Also today:** Van Gogh sells for a record $190.4m, Hayabusa2 engine trouble ends the asteroid landing, Trump pardons Pete Rose, Venezuela signs a US military deal, the Houthis hit a Riyadh tower, Europe open to Russia talks on Ukraine.

## How it is made

`draw.py` draws the page with Pillow (deterministic, seeded, no network) into `entry.png`. `main.ts` (Node 22, standard library only) places that finished image at `/output/entry.png`.

Run it locally:

```
python3 draw.py
mkdir -p out && MAKEFUN_OUTPUT_DIR=out node main.ts
```
