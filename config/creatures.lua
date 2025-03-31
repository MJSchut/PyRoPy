-- Creature definitions for PyRoPy
-- Each creature has a base definition that can be overridden by spawn configurations

return {
    fungus = {
        name = "Fungus",
        char = "f",
        color = {0, 255, 0},  -- Green
        hp = 10,
        maxhp = 10,
        attack = 2,
        defense = 0,
        speed = 1,
        ai_type = "fungus",
        description = "A slow-growing fungus that spreads through the dungeon."
    },
    
    bat = {
        name = "Bat",
        char = "b",
        color = {128, 128, 128},  -- Gray
        hp = 5,
        maxhp = 5,
        attack = 3,
        defense = 1,
        speed = 2,
        ai_type = "bat",
        description = "A small flying creature that hunts in the darkness."
    },
    
    snake = {
        name = "Snake",
        char = "s",
        color = {0, 255, 0},  -- Green
        hp = 8,
        maxhp = 8,
        attack = 4,
        defense = 1,
        speed = 2,
        ai_type = "snake",
        description = "A venomous snake that slithers through the dungeon."
    },
    
    gargoyle = {
        name = "Gargoyle",
        char = "G",
        color = {128, 128, 128},  -- Gray
        hp = 15,
        maxhp = 15,
        attack = 5,
        defense = 3,
        speed = 1,
        ai_type = "gargoyle",
        description = "A stone guardian that comes to life to protect the dungeon."
    },
    
    player = {
        name = "Player",
        char = "@",
        color = {255, 255, 255},  -- White
        hp = 30,
        maxhp = 30,
        attack = 5,
        defense = 2,
        speed = 1,
        ai_type = "player",
        description = "You are the player character.",
        vision_radius = 9,
        inventory_size = 20,
        maxhunger = 100,
        hunger = 100,
        messages = None  -- This will be set by the factory
    }
} 