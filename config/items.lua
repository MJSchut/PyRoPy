-- Item definitions for PyRoPy
-- Each item has a base definition that can be overridden by spawn configurations

return {
    rock = {
        name = "Rock",
        char = ".",
        color = {128, 128, 128},  -- Gray
        type = "weapon",
        damage = 2,
        description = "A simple rock that can be used as a weapon.",
        weight = 1,
        equipment = true,
        holdable = true,
        equippable = true
    },
    
    sword = {
        name = "Sword",
        char = "|",
        color = {192, 192, 192},  -- Silver
        type = "weapon",
        damage = 5,
        description = "A sharp sword that can be used to attack enemies.",
        weight = 3,
        equipment = true,
        holdable = true,
        equippable = true
    },
    
    gauntlet = {
        name = "Gauntlet",
        char = "}",
        color = {192, 192, 192},  -- Silver
        type = "armor",
        defense = 2,
        description = "A metal glove that provides protection.",
        weight = 2,
        equipment = true,
        holdable = true,
        wearable = true,
        equippable = true
    },
    
    potion = {
        name = "Potion",
        char = "!",
        color = {255, 0, 255},  -- Magenta
        type = "consumable",
        effect = "heal",
        value = 20,
        description = "A magical potion that restores health.",
        weight = 1,
        drinkable = true,
        holdable = true
    },
    
    amulet = {
        name = "Amulet",
        char = "'",
        color = {255, 215, 0},  -- Gold
        type = "accessory",
        defense = 1,
        description = "A magical amulet that provides protection.",
        weight = 1,
        equipment = true,
        holdable = true,
        wearable = true,
        equippable = true
    },
    
    fedora = {
        name = "Fedora",
        char = "^",
        color = {139, 69, 19},  -- Brown
        type = "armor",
        defense = 1,
        description = "A stylish hat that provides minimal protection.",
        weight = 1,
        equipment = true,
        holdable = true,
        wearable = true,
        equippable = true
    },
    
    food = {
        name = "Food",
        char = "%",
        color = {139, 69, 19},  -- Brown
        type = "consumable",
        effect = "hunger",
        value = 20,
        description = "A piece of food that reduces hunger.",
        weight = 1,
        edible = true,
        holdable = true
    }
} 