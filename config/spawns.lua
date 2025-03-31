-- Spawn configurations for PyRoPy
-- This file defines how many of each creature/item should spawn and any special properties

return {
    creatures = {
        fungus = {
            count = 10,
            -- Can override base creature properties here if needed
            -- hp = 15,  -- Example override
        },
        bat = {
            count = 5,
        },
        snake = {
            count = 5,
        },
        gargoyle = {
            count = 5,
            -- Special properties for gargoyles
            follows_player = true,
        },
        player = {
            count = 1,
            -- Player specific spawn properties
            spawn_x = 40,  -- Center of map
            spawn_y = 25,
        }
    },
    
    items = {
        rock = {
            count = 25,
        },
        sword = {
            count = 3,
        },
        gauntlet = {
            count = 2,
        },
        potion = {
            count = 15,
            random_type = true,  -- Will randomly select potion type
        },
        amulet = {
            count = 2,
        },
        fedora = {
            count = 2,
        },
        food = {
            count = 20,
        }
    }
} 