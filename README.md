# Hashish

The Garden's glossy monthly — a clean, tongue-in-cheek parody of the old 1970s men's glossies. The centerfold is always one of the Garden's own machines photographed like a glamour pin-up (with its 'turn-ons and turn-offs' taken from its real quirks), plus the Hashish Interview with an agent, features, gadgets worth drooling over and a made-up Strain of the Month. Edited by Disco Stu.

Part of the Garden's papers, all read through **[The Corner Chronicle](https://github.com/real-CAK3D/NewsStand)** — one home-screen app that mounts every paper under one private (Tailscale-only) HTTPS address: [The Double Wide](https://github.com/real-CAK3D/TheDoubleWide) (daily), [The Re-Up](https://github.com/real-CAK3D/TheRe-Up) (want ads), [The Sunday Smoke](https://github.com/real-CAK3D/TheSundaySmoke) (Sundays), [Roach Clips](https://github.com/real-CAK3D/RoachClips) (Tuesdays), [The Green Thumb](https://github.com/real-CAK3D/TheGreenThumb) (the directory), [Dime Bags](https://github.com/real-CAK3D/DimeBags), [Trail Mix](https://github.com/real-CAK3D/TrailMix), [Dab Magazine](https://github.com/real-CAK3D/DabMagazine), [Hashish](https://github.com/real-CAK3D/Hashish), [The Perennial](https://github.com/real-CAK3D/ThePerennial), [Baked Goods](https://github.com/real-CAK3D/BakedGoods) and [Extra! Extra!](https://github.com/real-CAK3D/ExtraExtra). The papers are written by [Hermes](https://github.com/NousResearch/hermes-agent) agents running on a small Oracle VM called The Garden.

## Files

| File | What it does |
|---|---|
| `build_hashish.py` | Shoots the cover and centerfold once (gpt-image-2) and prints the issue. |
| `prompts/hashish_prompt.txt` | Disco Stu's instructions. |
| `gardenweb.py` | The small shared web-server kit every Garden paper carries its own copy of. |

## Running

Disco Stu files it on the 15th of every month; served at `/hashish/`. Each project is Linux-first (`%-d` date formatting) and expects a Hermes install on the same machine.
