"""THE VAULT: a small command-line adventure."""


def say(text):
    print(text)
    print()


def ask():
    return input("> ").strip().lower()


def describe_room(room, has_lamp, has_key, has_gem, gate_open):
    """Show the useful details of the room the player is exploring."""
    if room == "hall":
        print("THE DUSTY HALL")
        print("A cracked portrait watches over a rug and three doorways.")
        print("Exits: NORTH to the vault, EAST to the library, WEST to the cellar.")
        if not has_key:
            print("Something glints beneath the rug.")
    elif room == "library":
        print("THE SILENT LIBRARY")
        print("Shelves lean together like tired old trees.")
        print("Exits: WEST to the hall, EAST to the observatory.")
        if not has_lamp:
            print("A brass LAMP rests on a reading desk.")
    elif room == "cellar":
        print("THE FLOODED CELLAR")
        print("Cold water covers the floor. A narrow tunnel disappears SOUTH.")
        print("Exits: EAST to the hall, SOUTH to the crypt.")
        if not has_key:
            print("The water ripples around something metallic.")
    elif room == "crypt":
        print("THE CRYPT")
        print("Stone doors line the walls. The air smells of rain and iron.")
        print("Exits: NORTH to the cellar.")
        if not has_gem:
            print("A pale GEM glows inside an open stone coffin.")
    elif room == "observatory":
        print("THE OBSERVATORY")
        if not has_lamp:
            print("It is too dark to see. You need a lamp to explore safely.")
        else:
            print("Moonlight pours through the broken dome.")
            print("Exits: WEST to the library, NORTH to the vault.")
            if not gate_open:
                print("A brass control panel is set into the floor.")
    elif room == "vault":
        print("THE VAULT")
        print("A steel door waits beneath a ceiling painted with stars.")
        print("Exits: SOUTH to the hall.")


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


print("=" * 52)
print("                    THE VAULT")
print("=" * 52)
print("A storm is closing in. Find the vault before the old house wakes.")
print()

player_name = input("What is your name, explorer? ").strip() or "Nobody"
room = "hall"
has_key = False
has_lamp = False
has_gem = False
gate_open = False
moves = 0
limit = 24

say("Welcome, " + player_name + ". Type HELP for commands, or QUIT to leave.")
describe_room(room, has_lamp, has_key, has_gem, gate_open)
print()

while True:
    command = ask()

    if command == "":
        say("The house waits. Type HELP if you need a direction.")
        continue

    moves += 1

    if moves >= limit:
        say("The storm breaks through the roof. The house seals itself around you. Game over.")
        break

    if command in ("quit", "exit"):
        say("You escape into the storm after " + str(moves) + " moves. The vault remains sealed.")
        break

    if command in ("help", "?"):
        say("Commands: LOOK, GO NORTH/SOUTH/EAST/WEST, TAKE, INVENTORY, OPEN VAULT, QUIT")
        continue

    if command in ("look", "l"):
        describe_room(room, has_lamp, has_key, has_gem, gate_open)
        print()
        continue

    if command in ("inventory", "i", "items"):
        show_inventory(has_key, has_lamp, has_gem)
        continue

    # Accept both "north" and the more natural "go north".
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
        }.get((room, direction))

        if destination is None:
            say("There is no open path that way.")
        elif destination == "observatory" and not has_lamp:
            say("The darkness beyond the library is absolute. Find a lamp first.")
        elif destination == "vault" and not gate_open:
            say("A hidden mechanism holds the vault entrance shut. Search the observatory.")
        else:
            room = destination
            describe_room(room, has_lamp, has_key, has_gem, gate_open)
            print()
        continue

    if command in ("take", "take key", "get key") and room in ("hall", "cellar"):
        if has_key:
            say("You already have the brass key.")
        else:
            has_key = True
            say("You find a brass key. Its teeth are shaped like tiny stars.")
        continue

    if command in ("take lamp", "get lamp") and room == "library":
        if has_lamp:
            say("You already have the lamp.")
        else:
            has_lamp = True
            say("You light the lamp. The flame burns blue and steady.")
        continue

    if command in ("take gem", "get gem") and room == "crypt":
        if has_gem:
            say("You already have the gem.")
        else:
            has_gem = True
            say("You lift the gem. Somewhere above you, a lock clicks open.")
        continue

    if command in ("use panel", "activate panel", "open panel") and room == "observatory":
        if not has_lamp:
            say("You cannot see the control panel in the dark.")
        elif has_gem:
            gate_open = True
            say("The gem fits the panel. Brass gears turn, and the vault gate unlocks.")
        else:
            say("The panel has a gem-shaped socket. Something in the crypt may fit it.")
        continue

    if command in ("open vault", "enter vault") and room == "vault":
        if has_key:
            if has_gem:
                print("The star-key turns. The vault opens onto a room full of sunrise.")
                say("You leave with the treasure and the house's secrets. You win in " + str(moves) + " moves!")
            else:
                print("The star-key turns. Inside is a single locked glass case.")
                say("You found the vault, but the true treasure is still hidden. You escape with a mystery.")
            break
        say("The vault accepts a key, but you do not have one.")
        continue

    say("That command does not work here. Try LOOK or HELP.")

