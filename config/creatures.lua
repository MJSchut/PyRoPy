-- Creature definitions for PyRoPy
-- Each creature has a base definition that can be overridden by spawn configurations

return {
    fungus = {
        name = "Fungus",
        char = "f",
        color = {0, 255, 0},  -- Green
        hp = 10,
        max_hp = 10,
        attack = 2,
        defense = 0,
        speed = 1,
        ai_type = "fungus",
        description = "A slow-growing fungus that spreads through the dungeon.",
        vision_radius = 3,
        inventory_size = 0
    },
    
    bat = {
        name = "Bat",
        char = "b",
        color = {128, 128, 128},  -- Gray
        hp = 5,
        max_hp = 5,
        attack = 3,
        defense = 1,
        speed = 2,
        ai_type = "bat",
        description = "A small flying creature that hunts in the darkness.",
        vision_radius = 5,
        inventory_size = 0
    },
    
    snake = {
        name = "Snake",
        char = "s",
        color = {0, 255, 0},  -- Green
        hp = 8,
        max_hp = 8,
        attack = 4,
        defense = 1,
        speed = 2,
        ai_type = "snake",
        description = "A venomous snake that slithers through the dungeon.",
        vision_radius = 4,
        inventory_size = 0
    },
    
    gargoyle = {
        name = "Gargoyle",
        char = "G",
        color = {128, 128, 128},  -- Gray
        hp = 15,
        max_hp = 15,
        attack = 5,
        defense = 3,
        speed = 1,
        ai_type = "gargoyle",
        description = "A stone guardian that comes to life to protect the dungeon.",
        vision_radius = 6,
        inventory_size = 0
    },
    
    player = {
        name = "Player",
        char = "@",
        color = {255, 255, 255},  -- White
        hp = 30,
        max_hp = 30,
        attack = 5,
        defense = 2,
        speed = 1,
        ai_type = "player",
        description = "You are the player character.",
        vision_radius = 9,
        inventory_size = 20,
        max_hunger = 100,
        hunger = 100
    }
} 