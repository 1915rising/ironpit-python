#!/usr/bin/env python3
"""Ironpit - a turn-based arena battler.

Fight through three challengers in the pit. Each turn pick a move:
strike, heavy swing, guard, or drink a tonic. Read the foe's rhythm:
every third turn they wind up a heavy blow, and a guard will blunt it.

Stdlib only. Use --seed N for a deterministic match.
"""

import argparse
import random
import sys

PLAYER_MAX_HP = 34
TONICS = 2
TONIC_HEAL = 12

# name, max hp, light damage range, heavy damage range
FOES = [
    ("Rookie Brawler", 16, (2, 4), (5, 7)),
    ("Iron Guard", 22, (3, 5), (7, 9)),
    ("Pit Champion", 30, (4, 6), (8, 11)),
]


class Fighter:
    def __init__(self, name, hp):
        self.name = name
        self.hp = hp
        self.max_hp = hp
        self.guarding = False


def bar(current, maximum, width=20):
    filled = int(width * max(current, 0) / maximum)
    return "[" + "#" * filled + "-" * (width - filled) + "]"


def show(player, foe, round_no):
    print(f"--- Round {round_no}: {foe.name} ---")
    print(f"You  {bar(player.hp, player.max_hp)} {player.hp}/{player.max_hp}")
    print(f"Foe  {bar(foe.hp, foe.max_hp)} {foe.hp}/{foe.max_hp}")


def player_turn(player, foe, rng, tonics):
    """Returns (tonics, quit_flag)."""
    while True:
        print("Choose: [1] Strike  [2] Heavy swing  [3] Guard  "
              f"[4] Tonic ({tonics} left)  [q] Quit")
        try:
            choice = input("> ").strip().lower()
        except EOFError:
            choice = "q"
        if choice == "q":
            return tonics, True
        if choice == "1":
            dmg = rng.randint(5, 8)
            foe.hp -= dmg
            print(f"You strike {foe.name} for {dmg} damage.")
            return tonics, False
        if choice == "2":
            if rng.random() < 0.25:
                print("Your heavy swing misses!")
            else:
                dmg = rng.randint(8, 14)
                foe.hp -= dmg
                print(f"Your heavy swing lands on {foe.name} for {dmg} damage.")
            return tonics, False
        if choice == "3":
            player.guarding = True
            print("You raise your guard.")
            return tonics, False
        if choice == "4":
            if tonics <= 0:
                print("No tonics left!")
                continue
            tonics -= 1
            healed = min(TONIC_HEAL, player.max_hp - player.hp)
            player.hp += healed
            print(f"You drink a tonic and recover {healed} HP.")
            return tonics, False
        print("Invalid choice, try again.")


def foe_turn(player, foe, rng, turn_no, light, heavy):
    if foe.hp <= 0:
        return
    winding = (turn_no % 3 == 0)
    if winding:
        lo, hi = heavy
        kind = "heavy blow"
    else:
        lo, hi = light
        kind = "strike"
    dmg = rng.randint(lo, hi)
    if player.guarding:
        dmg = dmg // 2
        print(f"{foe.name} throws a {kind}; your guard blunts it to {dmg} damage.")
        player.guarding = False
    else:
        print(f"{foe.name} throws a {kind} and hits you for {dmg} damage.")
    player.hp -= dmg


def play(seed):
    rng = random.Random(seed)
    player = Fighter("You", PLAYER_MAX_HP)
    tonics = TONICS
    print("Welcome to the Ironpit!")
    print("Defeat all three challengers to take the pit crown.")
    for round_no, (name, hp, light, heavy) in enumerate(FOES, start=1):
        foe = Fighter(name, hp)
        print(f"\n{name} steps into the pit!")
        turn_no = 0
        while foe.hp > 0 and player.hp > 0:
            turn_no += 1
            show(player, foe, round_no)
            if turn_no % 3 == 0:
                print(f"{foe.name} is winding up a heavy blow...")
            tonics, quit_game = player_turn(player, foe, rng, tonics)
            if quit_game:
                print("You leave the pit. The crowd boos softly.")
                print("RESULT: QUIT")
                return 0
            foe_turn(player, foe, rng, turn_no, light, heavy)
        if player.hp <= 0:
            print(f"\n{foe.name} knocks you down. The pit goes quiet.")
            print("RESULT: DEFEAT")
            return 0
        print(f"{name} falls! The crowd roars.")
        if round_no < len(FOES):
            rest = min(8, player.max_hp - player.hp)
            player.hp += rest
            print(f"You catch your breath and recover {rest} HP.")
    print("\nAll challengers fall. You take the pit crown!")
    print("RESULT: VICTORY")
    return 0


def main(argv=None):
    parser = argparse.ArgumentParser(description="Ironpit - turn-based arena battler")
    parser.add_argument("--seed", type=int, default=42,
                        help="random seed for a deterministic match (default: 42)")
    args = parser.parse_args(argv)
    return play(args.seed)


if __name__ == "__main__":
    sys.exit(main())
