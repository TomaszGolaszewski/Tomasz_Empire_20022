Changelog
======

v0.16.1 - 12.05.2024
----
* Fixes in fuel consumption mechanics.

v0.16.0 - 11.03.2024
----
* New unit: Aircraft_carrier;
* New fuel consumption mechanics for aircraft.

v0.16 - Planes stage II
======


v0.15.5 - 14.01.2024
----
* Minor changes;
* Code cleaning.

v0.15.4 - 30.12.2023
----
* Fixes in pathfinding algorithm regarding units leaving the map.

v0.15.3 - 29.12.2023
----
* Fix of critical bug in the building queue;
* Lot of changes in Size Choose Scene:
    * fixed choose shape option,
    * added currently selected map dimensions,
    * added new trees option;  
* Lot of small fixes.

v0.15.2 - 17.12.2023
----
* Fixes in start position on bridge map;
* New algorythm for finding places for naval factories.

v0.15.1 - 09.12.2023
----
* New algorythm for finding places for land factories;
* New algorythm for finding places for generators.

v0.15.0 - 07.12.2023
----
* New map generating algorithm: map island has more water, map lake is more square.

v0.15 - Map stage III
======


v0.14.7 - 18.11.2023
----
* Fixes regarding scroll mouse button in game setup scenes.

v0.14.6 - 08.11.2023
----
* Added animation of a battle on Title Scene.

v0.14.5 - 06.11.2023
----
* Added Size and Players Choose Scenes;
* All scenes are now used.

v0.14.4 - 06.11.2023
----
* Added Map Choose Scene (currently hidden);
* New features for building scenes: AdvancedButton;
* Added option to show map without buildings foundation.

v0.14.3 - 05.11.2023
----
* Added Loading Scene;
* Lots of fixes in Game Scene.

v0.14.2 - 04.11.2023
----
* New features for building scenes: DynamicText;
* Refactoring of game engine to work with new scenes mechanism.

v0.14.1 - 04.11.2023
----
* Fixes in the scene changing mechanism;
* New features for building scenes: FixText and BaseButton;
* Added Title Scene (currently hidden).

v0.14.0 - 02.11.2023
----
* Preparation of the scene changing mechanism.

v0.14 - Menu and Scenes
======


v0.13.11 - 01.11.2023
----
* Code cleaning.

v0.13.10 - 13.10.2023
----
* Changes in methods that draw additional data about units;
* Basic extra data is now shown when unit is selected;
* Fix in start camera position.

v0.13.9 - 09.10.2023
----
* New way of storing movement targets;
* Player's units have AI engine to check and adjust movement path now;
* Added possibility to assign movement target to units produced by factories;
* Lot of small fixes.

v0.13.8 - 06.10.2023
----
* Added pointer to show unit's movement target;
* Added calculating players' current score.

v0.13.7 - 01.10.2023
----
* Fix: units with higher level than factory's one can no longer be seen in shop;
* Small fix of initial amount of players' energy.

v0.13.6 - 29.09.2023
----
* More changes in building upgrade AI;
* Some fixes in unit selection AI.

v0.13.5 - 28.09.2023
----
* Big changes in purchase and production mechanics:
    * amount of energy for the product is spent not during production but once at the time of unit selection;
* AI was adapted to the new mechanics;
* New player's energy indicator.

v0.13.4 - 27.09.2023
----
* More changes in shoping card view - price labels turn red when there is not enough energy.

v0.13.3 - 26.09.2023
----
* Changes in shopping upgrade card view.

v0.13.2 - 26.09.2023
----
* First stage of changes in factory upgrade mechanics:
    * Added shopping upgrade cards,
    * Added mechanics for purchasing upgrades,
    * Added icon modification for upgraded factory.

v0.13.1 - 24.09.2023
----
* Added table with energy status of the players on the screen.

v0.13.0 - 23.09.2023
----
* Added pause (space button).

v0.13 - New mechanics for building and buying units
======


v0.12.4 - 23.04.2023
----
* Small fixes in collision checking;
* New pause button in queue window;
* Building queue can be now passed;
* AI can now stop production when it has limited resources.

v0.12.3 - 16.04.2023
----
* Small fixes in building queue loop;
* New mechanics for collision checking between units:
    * once a second search for the nearest units that may collide in the future - store their ids in a list,
    * during each frame check for collisions with units from the list;
    * when collision occurs, move unit back;
* Small fixes in building's default target for newly produced units.

v0.12.2 - 10.04.2023
----
* New loop button in queue window;
* Building queue can be now looped;

v0.12.1 - 02.04.2023
----
* New HexTile: submerged_concrete;
* Added concrete buildings foundation - pathfinding algorithm will be avoiding them;
* Changes for Space Marine units' AI - if building found, stop the unit in front of that building.

v0.12.0 - 01.04.2023
----
* Added new pathfinding algorithm. Units now avoid terrain they cannot pass through.

v0.12 - AI, performance optimization and game balance
======


v0.11.10 - 25.03.2023
----
* Added buttons for future assignment of the target for units to the factory.

v0.11.9 - 25.03.2023
----
* Buildings are now procedurally placed on the map.

v0.11.8 - 25.03.2023
----
* Preparation for building placement mechanics.

v0.11.7 - 23.03.2023
----
* Buildings are now animated;
* Animation of building depends on their level and state.

v0.11.6 - 23.03.2023
----
* Small fixes regarding test AI mechanics.

v0.11.5 - 23.03.2023
----
* First test mechanics for future AI.

v0.11.4 - 22.03.2023
----
* New sprites for future buildings animation.

v0.11.3 - 12.03.2023
----
* Building can be captured/restored now by Space Marine units family.

v0.11.2 - 11.03.2023
----
* New units: Space Marine, Super Space Marine and Commander.

v0.11.1 - 10.03.2023
----
* Buildings can be destroyed/disabled by shooting at them.

v0.11.0 - 09.03.2023
----
* Added new building: Generator;
* Added icons for buildings;
* Added HP bars and progress bars for buildings.

v0.11 - Buildings
======


v0.10.13 - 05.03.2023
----
* Small fixes regarding creation of units.

v0.10.12 - 05.03.2023
----
* Small fixes regarding iterating dictionaries;
* New storage dict_with_game_state to collect data about game progress;
* Added progress bar to queue window;
* Changes in adding units to building queue and removing units from queue methods;
* Units production process completed.

v0.10.11 - 03.03.2023
----
* Fixes in class Shop_unit_label;
* Factory management notebooks completed;
* Added possibility to add units to the queue.

v0.10.10 - 02.03.2023
----
* Preparing notebooks for future factory management;
* Added class Shop_unit_label.

v0.10.9 - 01.03.2023
----
* Added more technical data to window with infos about unit.

v0.10.8 - 28.02.2023
----
* More changes and fixes to the windows handling methods;
* Queue window now is showing building queue;
* Added possibility to delete units from the queue.

v0.10.7 - 26.02.2023
----
* Changes to the way window with infos about unit is stored;
* Added building queue window.

v0.10.6 - 25.02.2023
----
* Changes to the way windows are stored and handled.

v0.10.5 - 25.02.2023
----
* Added ID number to units. 

v0.10.4 - 23.02.2023
----
* All units are now stored in dictionary;
* Small fix in slide button.

v0.10.3 - 20.02.2023
----
* Added small window with infos about unit.

v0.10.2 - 19.02.2023
----
* New class: Building;
* Units can collide with buildings but cannot shot to them.

v0.10.1 - 18.02.2023
----
* New notebook with tabs window for future units buying mechanism.

v0.10.0 - 28.01.2023
----
* Added slide button to set new units actions;
* Units in the squad can now deployed on a spiral grid or in original arrangement.

v0.10 - UI stage I
======


v0.9.12 - 24.01.2023
----
* New weapon: Missile_launcher;
* New ammunition: Missile.

v0.9.11 - 23.01.2023
----
* Fixes in body radius definition;
* Further optimisation of the collision checking (using math.hypot);
* Lots of small fixes.

v0.9.10 - 15.01.2023
----
* Added fps display;
* Units in the squad are now deployed on a spiral grid (offset between units is defined by the largest unit);
* Units in the squad are moving together (speed is defined by the slowest unit);
* Added priority of selection: air > land > navy.

v0.9.9 - 15.01.2023
----
* New animation for units when stopped and dead;
* New sprites for naval units.

v0.9.8 - 08.01.2023
----
* Further optimisation of the unit drawing method;
* Fixes in naval units' sprites.

v0.9.7 - 07.01.2023
----
* Naval cannons are shooting now multiple bullets at ones;
* Side cannons and naval cannons can no longer shoot backwards;
* Fixes in angle following method;
* Fixes in bombers' aiming;
* Fixes in collision between bullets and trees.

v0.9.6 - 15.12.2022
----
* Fixes in map methods regarding map border;
* Added basic animation of units' death and bullets' explosion;
* Chenges in units and bullets removal mechanism allowing the display of explosions.

v0.9.5 - 12.12.2022
----
* New unit: Battleship. 

v0.9.4 - 11.12.2022
----
* Fixes in turrets' angle calculation;
* New weapon: Heavy naval cannon;
* New unit: Destroyer.

v0.9.3 - 11.12.2022
----
* Refactoring of the unit classes.

v0.9.2 - 07.12.2022
----
* New weapons: Heavy cannon and medium naval cannon.

v0.9.1 - 07.12.2022
----
* New units: Heavy artillery and Battle cruiser;
* New imgs folder structure;
* Fixes in weapons and bullets methods regarding naval units.

v0.9.0 - 04.12.2022
----
* New class of units: Naval unit;
* New units: Small artillery ship and Small AA ship. 

v0.9 - Ships
======


v0.8.12 - 04.12.2022
----
* Bullets can no longer fly through trees - the tree tile will be destroyed.

v0.8.11 - 04.12.2022
----
* Land units can no longer move on deep water;
* Deep water can't be degraded.

v0.8.10 - 04.12.2022
----
* Added more sprites for forest tile;
* Added more randomization for maps based on an ellipse.

v0.8.9 - 01.12.2022
----
* Now forest draws tree sprite;
* New tile: snow_forest;
* New maps: forest and snow_forest.

v0.8.8 - 28.11.2022
----
* New map based on Perlin Noise.

v0.8.7 - 28.11.2022
----
* Added scale 0.125;
* Fixes in depth drawing.

v0.8.6 - 28.11.2022
----
* Added depth to water and shallow tiles.

v0.8.5 - 27.11.2022
----
* Further optimisation of the board preparing method for based on an ellipse map types: lake, island and bridge.

v0.8.4 - 26.11.2022
----
* Further optimisation of the map display - for the biggest scale map is not stored but scaled up from the smaller one;
* New map types: lake, island and bridge.

v0.8.3 - 24.11.2022
----
* New map types: snow plains, grass plains, concrete floor and mars poles;
* New tile type: concrete.

v0.8.2 - 23.11.2022
----
* Merge of both HexTile classes, code cleaning;
* Added new types of tile: snow, grass, sand, mars soil, water and others.

v0.8.1 - 21.11.2022
----
* New class Map_v2 which stores tiles in sprites and draws the map using mipmap technology.

v0.8.0 - 20.11.2022
----
* New class HexTile_v2 - for further optimisation;
* Experimenting with drawing a map using spraits.

v0.8 - Map stage II
======


v0.7.13 - 20.11.2022
----
* Fixes in units drawing order;
* Changes in changelog structure.

v0.7.12 - 11.11.2022
----
* Some changes in Bomb and Bomb_dispenser mechanics;
* New weapon: Advanced_bomb_dispenser.

v0.7.11 - 08.11.2022
----
* New weapon: Bomb_dispenser;
* New ammunition: Bomb.

v0.7.10 - 08.11.2022
----
* Some changes in sprites: heavy track and bomber;
* New weapon: Plane_fixed_gun.

v0.7.9 - 08.11.2022
----
* New unit: Heavy tank with two Side turrets;
* Turrets are now moving back to start position without target;
* Fixes in function turn_to_target_angle.

v0.7.8 - 07.11.2022
----
* Fixes in collision detection;
* New sprites for future units: heavy tank.

v0.7.7 - 07.11.2022
----
* Color of bullets now indicates target type: air / land;
* Wapons only shots at a specific target type.

v0.7.6 - 07.11.2022
----
* Cleaning and optimisation in draw method in Unit class;
* New unit type icon for air units.

v0.7.5 - 06.11.2022
----
* New number and location of miniguns on bombers.

v0.7.4 - 06.11.2022
----
* New wapon: Plane_minigun;
* New ammunition: Plasma beam.

v0.7.3 - 05.11.2022
----
* New units: Bomber and Strategic bomber.

v0.7.2 - 04.11.2022
----
* New zoom mechanism;
* New sprites for future units: bomber.

v0.7.1 - 04.11.2022
----
* New sprites to animate all units;
* Fixes in degrade method in Map class.

v0.7.0 - 04.11.2022
----
* New class: Base_object - base for old unanimated objects;
* New class of units: Air unit;
* New unit: Fighter.

v0.7 - Planes
======


v0.6.3 - 04.11.2022
----
* New unit: Spider tank.

v0.6.2 - 04.11.2022
----
* New animated draw method in Base_animated_object class.

v0.6.1 - 04.11.2022
----
* New class: Base_animated_object;
* New initialization method to prepare list of sprites for further animation process.

v0.6.0 - 03.11.2022
----
* New sprites for future animated units: spider tanks and fighters.

v0.6 - Animation
======


v0.5.3 - 03.11.2022
----
* New algorithm used to calculate angle to target;
* New run method in Vehicle class.

v0.5.2 - 02.11.2022
----
* Added collision checking between units;
* Small changes in selection function.

v0.5.1 - 02.11.2022
----
* Added mouse control of selected units.

v0.5.0 - 02.11.2022
----
* The target of vehicle movement is now a list.

v0.5 - Mouse control
======


v0.4.4 - 02.11.2022
----
* Small changes in draw_HP method;
* Unit symbols are now bigger.

v0.4.3 - 01.11.2022
----
* Small fixes in aiming algorithm;
* Bullets are checking now if they hit units;
* Units are getting now damage;
* Added draw_HP method to Unit class.

v0.4.2 - 31.10.2022
----
* Added deletion of old bullets.

v0.4.1 - 31.10.2022
----
* New units: Light tank and Main battle tank;
* Lots of small fixes.

v0.4.0 - 31.10.2022
----
* Added Bullet class with draw and run methods;
* Turrets are shooting bullets now;
* Small changes in ground degradation.

v0.4 - Units
======


v0.3.3 - 31.10.2022
----
* Added rotating the tower to run method in Turret class.

v0.3.2 - 31.10.2022
----
* Added method find_target to Turret class.

v0.3.1 - 29.10.2022
----
* Added team and unit class indicator.

v0.3.0 - 28.10.2022
----
* Added Turret class with draw method;
* Added Unit class which is made of Vehicle and Turret objects.

v0.3 - Weapons
======


v0.2.2 - 24.10.2022
----
* Added ground degradation.

v0.2.1 - 24.10.2022
----
* Performance optimisation in HexTile class;
* Bugfixes in Vehicle class.

v0.2.0 - 23.10.2022
----
* Created Vehicle class with draw, move, accelerate methods.

v0.2 - Vehicles
======


v0.1.2 - 23.10.2022
----
* Performance optimisation in HexTile class.

v0.1.1 - 22.10.2022
----
* New HexTile class structure;
* New Map class structure, new methods: id2world;
* New math functions, e.g. world2screen, screen2world;
* Added manipulation of the map view using mouse and keyboard.

v0.1.0 - 21.10.2022
----
* Project initialization;
* Created HexTile class with draw method;
* Created Map class with draw method.

v0.1 - Map stage I
======
