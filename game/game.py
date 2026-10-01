"""THE VAULT: a small command-line adventure."""


def say(text):
    print(text)
    print()


def ask():
    return input("> ").strip().lower()


def show_help():
    say(
        "Commands: LOOK, GO NORTH/SOUTH/EAST/WEST, TAKE <item>, INVENTORY, SEARCH, "
        "USE PANEL, OPEN VAULT, MAP, STATUS, HELP, RESTART, or QUIT."
    )


def show_map():
    say(
        "Map: HALL connects to the VAULT (north), LIBRARY (east), and CELLAR (west). "
        "The LIBRARY leads to the OBSERVATORY (east). The CELLAR leads to the CRYPT (south)."
    )


def show_status(room, moves, limit, has_key, has_lamp, has_gem, gate_open):
    pressure = min(100, int((moves / limit) * 100))
    say(
        f"Status: you are in the {room.upper()} | moves {moves}/{limit} | storm pressure {pressure}% | "
        f"key {str(has_key).lower()} | lamp {str(has_lamp).lower()} | gem {str(has_gem).lower()} | gate {str(gate_open).lower()}"
    )


def describe_room(room, has_lamp, has_key, has_gem, gate_open):
    """Show the useful details of the room the player is exploring."""
    if room == "hall":
        print("THE DUSTY HALL")
        print("The air tastes of dust and old rain. A cracked portrait watches over a rug and three doorways.")
        print("Exits: NORTH to the vault, EAST to the library, WEST to the cellar.")
        if not has_key:
            print("Something glints beneath the rug.")
    elif room == "library":
        print("THE SILENT LIBRARY")
        print("Shelves lean together like tired old trees. A reading desk sits beneath a dying window.")
        print("Exits: WEST to the hall, EAST to the observatory.")
        if not has_lamp:
            print("A brass LAMP rests on a reading desk.")
    elif room == "cellar":
        print("THE FLOODED CELLAR")
        print("Cold water covers the floor. A narrow tunnel disappears SOUTH beneath a crack in the wall.")
        print("Exits: EAST to the hall, SOUTH to the crypt.")
        if not has_key:
            print("The water ripples around something metallic.")
    elif room == "crypt":
        print("THE CRYPT")
        print("Stone doors line the walls. The air smells of rain and old iron. An open coffin waits in the center.")
        print("Exits: NORTH to the cellar.")
        if not has_gem:
            print("A pale GEM glows inside an open stone coffin.")
    elif room == "observatory":
        print("THE OBSERVATORY")
        if not has_lamp:
            print("It is too dark to see. You need a lamp to explore safely.")
        else:
            print("Moonlight pours through the broken dome as the storm rattles the windows.")
            print("Exits: WEST to the library, NORTH to the vault.")
            if not gate_open:
                print("A brass control panel is set into the floor.")
    elif room == "vault":
        print("THE VAULT")
        print("A steel door waits beneath a ceiling painted with stars. The room hums with hidden machinery.")
        print("Exits: SOUTH to the hall.")
        if not gate_open:
            print("The vault gate is sealed behind a locked mechanism.")


def show_inventory(has_key, has_lamp, has_gem):
    items = []
    if has_key:
        items.append("brass key")
    if has_lamp:
        items.append("lamp")
    if has_gem:
        items.append("pale gem")
    if items:
        say("You are carrying: " + ", ".join(items) + ".")
    else:
        say("Your pockets are empty.")


def inspect_room(room, has_key, has_lamp, has_gem, gate_open):
    if room == "hall":
        if not has_key:
            say("You search the rug and find a star-shaped brass key hidden beneath it.")
        else:
            say("The rug is folded back and the floor is bare. The hall feels strangely calm.")
    elif room == "library":
        if not has_lamp:
            say("The reading desk holds a brass lamp with a blue flame burned into its metal.")
        else:
            say("A stack of old maps crinkles in your hands. Nothing else of value remains.")
    elif room == "cellar":
        if not has_key:
            say("The water swirls around a metallic object at the bottom of the tank.")
        else:
            say("The cellar is quiet apart from dripping water and an uneasy echo.")
    elif room == "crypt":
        if not has_gem:
            say("Inside the coffin rests a pale gem that pulses with a cold, moonlit glow.")
        else:
            say("The coffin is empty except for dust and a bitter smell of rain.")
    elif room == "observatory":
        if not has_lamp:
            say("You can barely make out the shapes around you. The darkness swallows everything.")
        elif not gate_open:
            say("A brass control panel sits in the floor, waiting for the right object to be used.")
        else:
            say("The panel is humming softly. The vault gate is open and the old house is listening.")
    elif room == "vault":
        if gate_open:
            say("The vault door has been unlocked. A keyhole gleams beside the open seal.")
        else:
            say("The vault is sealed behind a mechanism that only responds to the observatory panel.")


def reset_game():
    return {
        "room": "hall",
        "has_key": False,
        "has_lamp": False,
        "has_gem": False,
        "gate_open": False,
        "moves": 0,
        "limit": 24,
    }


print("=" * 52)
print("                    THE VAULT")
print("=" * 52)
print("A storm is closing in. Find the vault before the old house wakes.")
print()

player_name = input("What is your name, explorer? ").strip() or "Nobody"
state = reset_game()

say("Welcome, " + player_name + ". Type HELP for commands, or QUIT to leave.")
describe_room(state["room"], state["has_lamp"], state["has_key"], state["has_gem"], state["gate_open"])
print()

while True:
    command = ask()

    if command == "":
        say("The house waits. Type HELP if you need a direction.")
        continue

    state["moves"] += 1

    if state["moves"] >= state["limit"]:
        say("The storm breaks through the roof. The house seals itself around you. Game over.")
        break

    if command in ("quit", "exit"):
        say("You escape into the storm after " + str(state["moves"]) + " moves. The vault remains sealed.")
        break

    if command in ("help", "?", "commands"):
        show_help()
        continue

    if command in ("look", "l"):
        describe_room(state["room"], state["has_lamp"], state["has_key"], state["has_gem"], state["gate_open"])
        print()
        continue

    if command in ("inventory", "i", "items"):
        show_inventory(state["has_key"], state["has_lamp"], state["has_gem"])
        continue

    if command in ("map", "maze"):
        show_map()
        continue

    if command in ("status", "stats"):
        show_status(
            state["room"],
            state["moves"],
            state["limit"],
            state["has_key"],
            state["has_lamp"],
            state["has_gem"],
            state["gate_open"],
        )
        continue

    if command in ("search", "examine", "inspect"):
        inspect_room(state["room"], state["has_key"], state["has_lamp"], state["has_gem"], state["gate_open"])
        continue

    if command in ("restart", "reset"):
        state = reset_game()
        say("The house resets itself. A new storm begins.")
        describe_room(state["room"], state["has_lamp"], state["has_key"], state["has_gem"], state["gate_open"])
        continue

    direction = command.replace("go ", "", 1)
    if direction in ("n", "s", "e", "w"):
        direction = {"n": "north", "s": "south", "e": "east", "w": "west"}[direction]

    if direction in ("north", "south", "east", "west"):
        destination = {
            ("hall", "north"): "vault",
            ("hall", "east"): "library",
            ("hall", "west"): "cellar",
            ("library", "west"): "hall",
            ("library", "east"): "observatory",
            ("cellar", "east"): "hall",
            ("cellar", "south"): "crypt",
            ("crypt", "north"): "cellar",
            ("observatory", "west"): "library",
            ("observatory", "north"): "vault",
            ("vault", "south"): "hall",
        }.get((state["room"], direction))

        if destination is None:
            say("There is no open path that way.")
        elif destination == "observatory" and not state["has_lamp"]:
            say("The darkness beyond the library is absolute. Find a lamp first.")
        elif destination == "vault" and not state["gate_open"]:
            say("A hidden mechanism holds the vault entrance shut. Search the observatory.")
        else:
            state["room"] = destination
            describe_room(state["room"], state["has_lamp"], state["has_key"], state["has_gem"], state["gate_open"])
            print()
        continue

    if command in ("take all", "grab all"):
        if state["room"] == "hall" and not state["has_key"]:
            state["has_key"] = True
            say("You scoop up the brass key from beneath the rug.")
        elif state["room"] == "library" and not state["has_lamp"]:
            state["has_lamp"] = True
            say("You lift the brass lamp and the blue flame answers your touch.")
        elif state["room"] == "crypt" and not state["has_gem"]:
            state["has_gem"] = True
            say("You take the pale gem and feel the house shiver around you.")
        else:
            say("There is nothing here worth picking up.")
        continue

    if command in ("take key", "get key", "take brass key") and state["room"] in ("hall", "cellar"):
        if state["has_key"]:
            say("You already have the brass key.")
        else:
            state["has_key"] = True
            say("You find a brass key. Its teeth are shaped like tiny stars.")
        continue

    if command in ("take lamp", "get lamp") and state["room"] == "library":
        if state["has_lamp"]:
            say("You already have the lamp.")
        else:
            state["has_lamp"] = True
            say("You light the lamp. The flame burns blue and steady.")
        continue

    if command in ("take gem", "get gem", "take pale gem") and state["room"] == "crypt":
        if state["has_gem"]:
            say("You already have the gem.")
        else:
            state["has_gem"] = True
            say("You lift the gem. Somewhere above you, a lock clicks open.")
        continue

    if command in ("use panel", "activate panel", "open panel") and state["room"] == "observatory":
        if not state["has_lamp"]:
            say("You cannot see the control panel in the dark.")
        elif state["has_gem"]:
            state["gate_open"] = True
            say("The gem fits the panel. Brass gears turn, and the vault gate unlocks.")
        else:
            say("The panel has a gem-shaped socket. Something in the crypt may fit it.")
        continue

    if command in ("open vault", "enter vault") and state["room"] == "vault":
        if not state["gate_open"]:
            say("The vault is sealed. The observatory panel must be used first.")
        elif state["has_key"]:
            if state["has_gem"]:
                print("The star-key turns. The vault opens onto a room full of sunrise.")
                say("You leave with the treasure and the house's secrets. You win in " + str(state["moves"]) + " moves!")
            else:
                print("The star-key turns. Inside is a single locked glass case.")
                say("You found the vault, but the true treasure is still hidden. You escape with a mystery.")
            break
        else:
            say("The vault accepts a key, but you do not have one.")
        continue

    say("That command does not work here. Try LOOK, HELP, or MAP for clues.")

