# The Vault — a text adventure

**This game already works.** Your job is not to build one from nothing — it is to take one that
runs and make it yours. That is how real software actually gets written.

---

## Run it

Open `game.py`, then either:

- Click the **▶ Run** button, top right of the editor, **or**
- In the terminal: `python game/game.py`

Output shows up in the terminal panel at the bottom. Play all the way through — **win it, and lose
it.** You cannot improve something you have not seen work.

> Commands include: `look`, `go east`, `take lamp`, `take gem`, `use panel`, `inventory`,
> `open vault`, `help`, and `quit`. Short directions such as `n` and `w` also work.

---

## What is in the game

The house has five rooms, three items, a hidden progression puzzle, and a 24-move storm timer.
There are multiple endings: find the key and gem for the best ending, or open the vault with only
the key to escape with an unfinished mystery.

The code is intentionally readable so you can customize the rooms, items, commands, and endings.
Run it after each change so you know exactly which change needs attention.

---

## When it breaks

| Python says                          | It means                                                                               |
| ------------------------------------ | -------------------------------------------------------------------------------------- |
| `IndentationError`                   | Your spaces are wrong. Everything inside an `if` or `while` is indented **4 spaces**.  |
| `SyntaxError: invalid syntax`        | Usually a missing `:` at the end of an `if`/`elif`/`else`/`while`, or a missing quote. |
| `NameError: name 'x' is not defined` | A variable you never made, or spelled differently than when you made it.               |
| Nothing happens when I type          | Your `elif` never matched. Check spelling, and that it is lower case.                  |
| It never stops                       | Your `while` has no reachable `break`.                                                 |

**Read the last line of the error first** — it gives you the line number. Python is being helpful.
