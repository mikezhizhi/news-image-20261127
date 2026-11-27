# Friday 27 November 2026 — world news front page

Entry for make.fun `news-image-20261127`: one image summing up the world's
news of Friday 27 November 2026.

**Lead story:** a fierce storm disrupts Thanksgiving Day in the United
States — the parade in New York is postponed, about 400 flights are
cancelled and 724,000 homes lose power. Also covered: Trump telling Putin
to pull back, New Zealand's hung parliament, two Italians killed in a
drone strike in Kuwait, Brent crude near $97, Seoul repatriating six North
Koreans, the EU split over a $49bn loan to Ukraine, and more in the
"Also today" strip.

## Files

- `entry.png` — the front page (1024×1024 PNG)
- `draw_frontpage.py` — draws `entry.png` with Pillow (run it to regenerate)
- `main.py` — the entry program: copies `entry.png` to the output directory

## Regenerate

```sh
python3 draw_frontpage.py
mkdir -p out && MAKEFUN_OUTPUT_DIR=out python3 main.py
```
