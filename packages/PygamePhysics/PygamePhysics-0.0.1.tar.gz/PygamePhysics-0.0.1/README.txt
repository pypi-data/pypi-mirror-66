This project is to help with creating physics with Pygame
Knowledge of Pygame is still required

This package contains 2 modules: Collisions and Physics, you only need to worry about the physics module

__init__ function:
    • This function is for creating the object. You can not use this package if you create your own Pygame rect object
    • Args- x of object, y of object, width, height, color, the window object that you would like the object to be placed on, velocity of object (Cannot be changed later on)

setDimensions function:
    • Args- windowWidth, windowHeight

move function:
    • Moves the object in the direction specified (up, down, left, right)
    • Args- velocity, direction

setGravity function:
    • Sets the gravity for the different axis
    • Args- x gravity, y gravity

keepInBounds function:
    • Keeps the object in the bounds of the screen (Called in the update function)

update function:
    • Updates all of the objects' gravity and does collision resolution
    • Args- A list of all of the objects

processCollisions functions:
    • Handles collision resolution
    • Args- A list of all of the objects

draw function:
    • Draws the object on the window specified in the init function

jump function:
    • Makes the object jump
    • Args- jump power, object_list (This can be left with a None value, it is not used
