This is a python roguelike that I'll be maintaining as a hobby project.
Parts of this will follow the libtcod tutorial.

Short instructions.
Arrow keys to move
g: pick up items
i: bring up inventory
q: equip items
w: wear items
d: drop items
e: eat items

UPDATE log
- 0.02: The big one! Limb update, right now your character is just a set of hands though.
Ideally all creatures will have x amount of limbs with certain properties; they'll be able to
fall off, be chopped off, rot off or some other nasty stuff. S'gonna be fun.
You can equip and wear gauntlets or swords! Very suitable for a set of floating hands.
Field of view has been implemented, level generation has been expanded upon. Currently,
I'm using a miner cave generation algorithm. Pretty cool! Next up: adding more levels to
our cave, making combat more involved than rubbing your face against creatures.

---

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
