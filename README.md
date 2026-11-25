# Ironpit

A turn-based arena battler in a single Python 3 file (standard library only).
You step into the pit and fight three challengers in a row — the Rookie
Brawler, the Iron Guard, and the Pit Champion. Drop all three to take the
pit crown; get knocked down and the run ends.

By 1915rising.

## Run it

```sh
python3 ironpit.py            # default seed 42
python3 ironpit.py --seed 7   # deterministic match for that seed
```

Requires Python 3. No dependencies.

## Controls and rules

Each turn, type a number and press Enter:

- `1` — Strike: reliable hit for 5–8 damage.
- `2` — Heavy swing: 8–14 damage, but a 25% chance to miss.
- `3` — Guard: halves the foe's next hit (rounded down).
- `4` — Tonic: restore 12 HP. You carry only 2 per run.
- `q` — Quit the run.

You start with 34 HP. Between rounds you catch your breath and recover
8 HP. Every third turn a foe winds up a heavy blow — the game warns you
the turn before it lands, so that is the turn to guard. Foes hit harder
and take more punishment as you climb the ladder:

| Foe           | HP | Light hit | Heavy blow |
|---------------|----|-----------|------------|
| Rookie Brawler| 16 | 2–4       | 5–7        |
| Iron Guard    | 22 | 3–5       | 7–9        |
| Pit Champion  | 30 | 4–6       | 8–11       |

End states: defeating the Pit Champion prints `RESULT: VICTORY`, being
knocked down prints `RESULT: DEFEAT`, and quitting prints `RESULT: QUIT`.

## Determinism

All randomness comes from one `random.Random(seed)` instance, so the same
seed plus the same sequence of inputs always produces identical output.

## Tested envelope

Verified on Python 3.12.3 with scripted (piped stdin) playthroughs:

- Win path: seed 42, strike every turn → `RESULT: VICTORY`.
- Lose path: seed 42, guard every turn → `RESULT: DEFEAT`.
- Quit path: `q` as the first input → `RESULT: QUIT`, exit code 0.
- EOF on stdin is treated as a clean quit; invalid menu entries are
  rejected and re-prompted without consuming the turn.
- Determinism: two runs with the same seed and inputs (both a strike-only
  script and a mixed strike/heavy/guard/tonic script) produced
  byte-identical output.
- Balance spot check: across seeds 1–40, mindless strike-only play won
  25 of 40 runs — reading the heavy-blow warning and using guard, heavy
  swings, and tonics does noticeably better.
