# Tomasz Empire 20022: Supreme Leader

<p align="center">
  <img src="screens/screenshot1_20230115.png" alt="Tomasz Empire 20022">
</p>

## About
**'Tomasz Empire 20022: Supreme Leader'** is another part of the story about my Empire! The Future &amp; RTS - this is where the fun begins!!!

**Project still under development**

### Current stage:
v0.12 - AI, performance optimization and game balance

### Last changes:
v0.12.3 - 16.04.2023

* Small fixes in building queue loop;
* New mechanics for collision checking between units:
  * once a second search for the nearest units that may collide in the future - store their ids in a list,
  * during each frame check for collisions with units from the list;
  * when collision occurs, move unit back;
* Small fixes in building's default target for newly produced units.

v0.12.2 - 10.04.2023

* New loop button in queue window;
* Building queue can be now looped;

v0.12.1 - 02.04.2023

* New HexTile: submerged_concrete;
* Added concrete buildings foundation - pathfinding algorithm will be avoiding them;
* Changes for Space Marine units' AI - if building found, stop the unit in front of that building.

<p align="center">
  <img src="screens/screenshot2_20230115.png" alt="Tomasz Empire 20022 - Fleet">
  <br />
  <img src="screens/screenshot3_20230115.png" alt="Tomasz Empire 20022 - Mars poles Map">
</p>
