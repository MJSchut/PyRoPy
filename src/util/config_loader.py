from lupa import LuaRuntime
import os
from typing import Dict, Any

class ConfigLoader:
    def __init__(self):
        self.lua = LuaRuntime(unpack_returned_tuples=True)
        self.creatures = {}
        self.items = {}
        self.spawns = {}
        self.colors = {}
        self.load_configs()

    def load_configs(self):
        """Load all configuration files from the config directory."""
        config_dir = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(__file__))), 'config')
        
        # Load color definitions
        colors_file = os.path.join(config_dir, 'colors.lua')
        if os.path.exists(colors_file):
            with open(colors_file, 'r') as f:
                lua_code = f.read()
                self.colors = self.lua.execute(lua_code)
        
        # Load creature definitions
        creatures_file = os.path.join(config_dir, 'creatures.lua')
        if os.path.exists(creatures_file):
            with open(creatures_file, 'r') as f:
                lua_code = f.read()
                self.creatures = self.lua.execute(lua_code)
        
        # Load item definitions
        items_file = os.path.join(config_dir, 'items.lua')
        if os.path.exists(items_file):
            with open(items_file, 'r') as f:
                lua_code = f.read()
                self.items = self.lua.execute(lua_code)
        
        # Load spawn configurations
        spawns_file = os.path.join(config_dir, 'spawns.lua')
        if os.path.exists(spawns_file):
            with open(spawns_file, 'r') as f:
                lua_code = f.read()
                self.spawns = self.lua.execute(lua_code)

    def _convert_lua_color(self, lua_color):
        """Convert a Lua color table to a Python tuple."""
        if hasattr(lua_color, 'values'):
            # Convert Lua table to Python tuple
            values = list(lua_color.values())
            if len(values) == 3:
                return (int(values[0]), int(values[1]), int(values[2]))
            elif len(values) == 4:
                return (int(values[0]), int(values[1]), int(values[2]), int(values[3]))
        return lua_color

    def get_color(self, color_name: str) -> tuple:
        """Get a color tuple by name."""
        if color_name in self.colors:
            return self._convert_lua_color(self.colors[color_name])
        return (255, 255, 255)  # Default to white if color not found

    def get_creature_definition(self, creature_type: str) -> Dict[str, Any]:
        """Get the base definition for a creature type."""
        if creature_type in self.creatures:
            definition = dict(self.creatures[creature_type])
            # Convert color to Python tuple
            if 'color' in definition:
                definition['color'] = self._convert_lua_color(definition['color'])
            return definition
        return {}

    def get_item_definition(self, item_type: str) -> Dict[str, Any]:
        """Get the base definition for an item type."""
        if item_type in self.items:
            definition = dict(self.items[item_type])
            # Convert color to Python tuple
            if 'color' in definition:
                definition['color'] = self._convert_lua_color(definition['color'])
            return definition
        return {}

    def get_spawn_config(self, creature_type: str) -> Dict[str, Any]:
        """Get the spawn configuration for a creature type."""
        return dict(self.spawns['creatures'][creature_type])

    def get_item_spawn_config(self, item_type: str) -> Dict[str, Any]:
        """Get the spawn configuration for an item type."""
        return dict(self.spawns['items'][item_type])

    def get_all_creature_spawns(self) -> Dict[str, Dict[str, Any]]:
        """Get all creature spawn configurations."""
        return {k: dict(v) for k, v in self.spawns['creatures'].items()}

    def get_all_item_spawns(self) -> Dict[str, Dict[str, Any]]:
        """Get all item spawn configurations."""
        return {k: dict(v) for k, v in self.spawns['items'].items()} 