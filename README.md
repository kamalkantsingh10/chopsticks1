# 🐕 Chopsticks

**An LLM-powered pet robot dog. A weekend project that grew up.**

[![Chopsticks — LLM-powered pet robot, weeks 3 & 4](https://img.youtube.com/vi/sdet6u1EK-M/hqdefault.jpg)](https://www.youtube.com/shorts/sdet6u1EK-M)

A four-legged companion robot built from scratch — custom CAD, 3D-printed body, servo-driven legs with inverse kinematics, pan-tilt head with LCD eyes, an articulated neck and tail, and an LLM-driven voice loop. Sister project to [OLAF](https://github.com/kamalkantsingh10/OLAF) — same philosophy (build the body and the brain together), different form factor.

---

## What it is

Chopsticks is a quadruped pet robot. The goal is **personality before utility**: a robot you'd want around because it has presence, not because it folds laundry.

- **Body:** 3D-printed quadruped with strut-frame body, articulated head pan/tilt, and a moving tail.
- **Legs:** Servo-driven with inverse-kinematics control.
- **Face:** LCD eyes with rendered animations; expressive states (curious, sleepy, alert).
- **Voice:** LLM-powered conversation paired with the [chopsticks-server](https://github.com/kamalkantsingh10/chopsticks-server) LiveKit voice agent — STT, LLM, real-time TTS over the wire.
- **Audio:** Onboard speaker for chirps, beeps, and synthesized speech.

This is build-in-public hobbyist hardware, not a polished product. Things break. The archive folder has the scars.

---

## Repo layout

```
cad_models/
  body/                    Strut-frame body STLs
  head-pan&tilt/           Head mechanism STLs
  gcode/                   Pre-sliced gcode for the printer
controllers/
  audio.py                 Audio playback
calibrate.py               Servo calibration helper
archive/                   Earlier iterations — eyes, legs, neck, tail, speaker, face
                           — useful for reference; not the current code path.
```

---

## Hardware

- 3D printer (the body assumes ~220×220×250 mm bed minimum)
- Servos (MG90s for the head pan-tilt; larger for the legs — see `cad_models/head-pan&tilt/Pan_Servo_Base-mg90s.stl`)
- Camera module (Foxeer HS-1172v2 mount included)
- LCD module (1.69" round)
- A Raspberry Pi-class SBC for the brain
- Power supply sufficient for multi-servo simultaneous load

---

## Status

Active build-in-public. The current code under repo root (`calibrate.py`, `controllers/`) is the live path. Everything in `archive/` is earlier prototyping and is kept for reference, not as the canonical implementation.

---

## Related

- [OLAF](https://github.com/kamalkantsingh10/OLAF) — the bipedal sibling project
- [chopsticks-server](https://github.com/kamalkantsingh10/chopsticks-server) — the LiveKit voice agent

---

## Build log

Posted on [LinkedIn](https://www.linkedin.com/posts/kamal-singh_opensource-ai-weekendproject-activity-7299897449245024256-GNfG/).
