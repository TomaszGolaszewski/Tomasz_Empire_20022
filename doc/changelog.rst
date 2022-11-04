v0.7.1 - 04.11.2022
====
* New sprites to animate all units
* Fixes in degrade method in Map class 

v0.7.0 - 04.11.2022
====
* New class: Base_object - base for old unanimated objects
* New class of units: Air unit
* New unit: Fighter


v0.6.3 - 04.11.2022
====
* New unit: Spider tank

v0.6.2 - 04.11.2022
====
* New animated draw method in Base_animated_object class

v0.6.1 - 04.11.2022
====
* New class: Base_animated_object
* New initialization method to prepare list of sprites for further animation process

v0.6.0 - 03.11.2022
====
* New sprites for future animated units: spider tanks and fighters


v0.5.3 - 03.11.2022
====
* New algorithm used to calculate angle to target
* New run method in Vehicle class

v0.5.2 - 02.11.2022
====
* Added collision checking between units
* Small changes in selection function

v0.5.1 - 02.11.2022
====
* Added mouse control of selected units

v0.5.0 - 02.11.2022
====
* The target of vehicle movement is now a list


v0.4.4 - 02.11.2022
====
* Small changes in draw_HP method
* Unit symbols are now bigger

v0.4.3 - 01.11.2022
====
* Small fixes in aiming algorithm
* Bullets are checking now if they hit units
* Units are getting now damage
* Added draw_HP method to Unit class

v0.4.2 - 31.10.2022
====
* Added deletion of old bullets

v0.4.1 - 31.10.2022
====
* New units: Light tank and Main battle tank
* Lots of small fixes

v0.4.0 - 31.10.2022
====
* Added Bullet class with draw and run methods
* Turrets are shooting bullets now
* Small changes in ground degradation


v0.3.3 - 31.10.2022
====
* Added rotating the tower to run method in Turret class

v0.3.2 - 31.10.2022
====
* Added method find_target to Turret class

v0.3.1 - 29.10.2022
====
* Added team and unit class indicator

v0.3.0 - 28.10.2022
====
* Added Turret class with draw method
* Added Unit class which is made of Vehicle and Turret objects


v0.2.2 - 24.10.2022
====
* Added ground degradation

v0.2.1 - 24.10.2022
====
* Performance optimisation in HexTile class
* Bugfixes in Vehicle class

v0.2.0 - 23.10.2022
====
* Created Vehicle class with draw, move, accelerate methods


v0.1.2 - 23.10.2022
====
* Performance optimisation in HexTile class

v0.1.1 - 22.10.2022
====
* New HexTile class structure;
* New Map class structure, new methods: id2world;
* New math functions, e.g. world2screen, screen2world;
* Added manipulation of the map view using mouse and keyboard.

v0.1.0 - 21.10.2022
====
* Project initialization;
* Created HexTile class with draw method;
* Created Map class with draw method.
