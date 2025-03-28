# PyRoPy

A roguelike game written in Python using the tcod library.

> **Note**: This project is currently undergoing restoration and modernization. The codebase is being updated from Python 2.7/libtcodpy to Python 3.12/tcod, while preserving the original game mechanics and expanding upon them.

## Requirements

- Python 3.12 or higher
- tcod library
- numpy

## Installation

1. Create a virtual environment (recommended):
```bash
python -m venv .venv
source .venv/bin/activate  # On Windows use: .venv\Scripts\activate
```

2. Install the required packages:
```bash
pip install -r requirements.txt
```

## Running the Game

1. Make sure your virtual environment is activated
2. Run the game:
```bash
python main.py
```

## Controls

- Arrow keys or numpad: Move
- g: Pick up items
- i: Open inventory
- d: Drop items
- e: Eat items
- w: Wear items
- q: Equip items
- r: Drink items
- ;: Examine items
- ESC: Exit game

## Game Features

- Roguelike dungeon exploration
- Item management (pickup, drop, use)
- Combat system
- Status effects
- Hunger and thirst mechanics
- Various creatures and items to discover

## Development

This game was originally written in Python 2.7 using libtcodpy. It is currently being restored and modernized to work with Python 3.12 using the tcod library. The restoration process includes:

- Updating the codebase to modern Python standards
- Replacing deprecated libtcodpy calls with modern tcod equivalents
- Preserving and enhancing the original game mechanics
- Improving code documentation and structure
- Adding new features while maintaining the original roguelike feel

## License

This program is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with this program. If not, see <http://www.gnu.org/licenses/>.

## Historical Development Notes

This section contains historical information about the project's earlier versions.

### Original Description
This is a python roguelike that was maintained as a hobby project.
Parts of this followed the libtcod tutorial.

### Update Log
- **0.02a/b**: Added Limb system with humanoid creature presets. Relocated message log. Added potion color persistence. Added creature bleeding.
- **0.02**: Major update! Added Limb system (currently player is a set of hands). Added equipment system. Implemented field of view. Expanded level generation with miner cave algorithm.
- **0.01e**: Expanded combat, improved message system, basic level generation.
- **0.01d**: Added run.bat and Python 2.7 release. Added message and basic combat systems.
- **0.01c**: Added camera system. Made walls bumpable and fungus killable.
- **0.01b**: Added Entity system with OOP principles.
- **0.01a**: Initial version with basic @ movement.

---

Features:
Randomly generated cave system to explore!

(Work in progress) Involved creature system. Creatures consist of limbs, ai, can equip items and much more.

Effects system, items or creatures can poison other creatures.

---

UPDATE log
- 0.02a/b: Adding onto the Limb system. There's a preset structure for humanoid creatures now
Some ideas are thrown into the todo file. Don't pay too much mind to it. Relocated the 
message log. Potion colors are picked at the start of level generation are remain constant per
effect. Creatures bleed when hit. Started working on a thirst system.
Next up: adding 't'hrow command :)
- 0.02: The big one! Limb update, right now your character is just a set of hands though.
Ideally all creatures will have x amount of limbs with certain properties; they'll be able to
fall off, be chopped off, rot off or some other nasty stuff. S'gonna be fun.
You can equip and wear gauntlets or swords! Very suitable for a set of floating hands.
Field of view has been implemented, level generation has been expanded upon. Currently,
I'm using a miner cave generation algorithm. Pretty cool! Next up: adding more levels to
our cave, making combat more involved than rubbing your face against creatures.


- 0.01e: Combat has been expanded, message system is more coherent. Level generation
is quite basic, but functioning. One more version and then we push to 0.02.
- 0.01d: Added run.bat and a python 2.7 release. Just click and run the (not yet) game.
Message system has been added, so has a basic combat system.
- 0.01c: Camera system has been added. Walls are bumpable, pieces of fungus are killable.
- 0.01b: Added an Entity system. Now we are getting OOP. Documentation..
is still a bit lacking. I'll work on it once we get some semblance of a 
game going.
- 0.01a: Bare bones, an @ moves around the screen. Nothing much to see
yet.

---

DISCLAIMER:
This program is free software: you can redistribute it and/or modify it
under the terms of the GNU General Public License as published by the
Free Software Foundation, either version 3 of the License, or (at your
option) any later version.

This program is distributed in the hope that it will be useful as
educational tool, but WITHOUT ANY WARRANTY; without even the implied
warranty of MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See
the GNU General Public License for more details.

You should have received a copy of the GNU General Public License along
with this program.  If not, see <http://www.gnu.org/licenses/>
