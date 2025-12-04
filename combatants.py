from game_data import MONSTER_DATA, MONSTER_ATTACK_DATA, PLAYER_DATA, EQUIPMENT_DATA
from random import randint


class BattleEntity:
    def __init__(self, name, level, base_stats, max_health, max_energy):
        self.name = name
        self.level = level
        self.paused = False

        # Core Stats (Shared)
        self._base_stats = base_stats
        self.health = max_health * self.level
        self.energy = max_energy * self.level
        self.initiative = 0
        self.defending = False

    def get_base_stat(self, stat):
        return self._base_stats.get(stat, 0) * self.level

    # gets overridden in child class so it can include stat increases
    def get_stat(self, stat):
        return self.get_base_stat(stat)

    # returns all stats incl modifications if get_stat was overridden
    def get_stats(self):
        return {
            'health': self.get_stat('max_health'),
            'energy': self.get_stat('max_energy'),
            'attack': self.get_stat('attack'),
            'defense': self.get_stat('defense'),
            'speed': self.get_stat('speed'),
            'recovery': self.get_stat('recovery'),
        }

    # returns current character health, energy, and initiative out of max value
    def get_info(self):
        return (
            (self.health, self.get_stat('max_health')),
            (self.energy, self.get_stat('max_energy')),
            (self.initiative, 100)  # 100 is the full bar for initiative
        )

    # prevents health and energy from overflowing max values
    def stat_limiter(self):
        self.health = max(0, min(self.health, self.get_stat('max_health')))
        self.energy = max(0, min(self.energy, self.get_stat('max_energy')))


    def update(self, dt):
        self.stat_limiter()
        if not self.paused:
            self.initiative += self.get_stat('speed') * dt


class Monster(BattleEntity):
    def __init__(self, name, level):
        # Fetch data specific to the monster name
        monster_data = MONSTER_DATA[name]
        stats = monster_data['stats']
        super().__init__(name, level, stats, stats['max_health'], stats['max_energy'])
        self.base_stats = stats
        self.abilities = monster_data['abilities']

        # element uses not yet implemented
        self.element = stats['element']

    def __repr__(self):
        return f'monster: {self.name}, lvl: {self.level}'

    # currently only uses level scaling, may eventually inc buff/debuff
    def get_stat(self, stat):
        return self.get_base_stat(stat)

    def get_abilities(self, all = True):
        learned_abilities = [ability for lvl, ability in self.abilities.items() if self.level >= lvl]
        if all:
            return learned_abilities
        else:
            return [ability for ability in learned_abilities if
                    MONSTER_ATTACK_DATA.get(ability, {}).get('cost', float('inf')) <= self.energy]

    def reduce_energy(self, attack):
        self.energy -= MONSTER_ATTACK_DATA[attack]['cost']

    def get_base_damage(self, attack):
        return self.get_stat('attack') * MONSTER_ATTACK_DATA[attack]['amount']


class PlayerCharacter(BattleEntity):
    def __init__(self, name, level, equipment_data = EQUIPMENT_DATA):
        player_base_data = PLAYER_DATA[name]['stats']
        super().__init__(name, level, player_base_data, player_base_data['max_health'], player_base_data['max_energy'])
        self.equipment = PLAYER_DATA[name]['equipment']
        self._equipment_data = equipment_data

        # experience
        self.xp = 0
        self.level_up = self.level * 150  # Base XP needed to level up

    def __repr__(self):
        return f'Player: {self.name}, Lvl: {self.level}'

    def get_equipment_bonus(self, stat):
        total_bonus = 0
        for item_key in self.equipment.values():
            item = self._equipment_data.get(item_key, {})
            if 'stats' in item:
                total_bonus += item['stats'].get(stat, 0)
        return total_bonus

    def get_stat(self, stat):
        base_value = self.get_base_stat(stat)
        equipment_bonus = self.get_equipment_bonus(stat)
        return base_value + equipment_bonus


    def reduce_energy(self, attack):
        self.energy -= PLAYER_DATA[attack]['cost']

    def get_abilities(self, all=True):
        learned_abilities = [ability for lvl, ability in self.abilities.items() if self.level >= lvl]
        if all:
            return learned_abilities
        else:
            return [ability for ability in learned_abilities if
                    PLAYER_DATA.get(ability, {}).get('cost', float('inf')) <= self.energy]

    # parses player data for current weapon and stats, returns wep for use in damage step
    # basically bridges equipment and equipped data sets so we don't duplicate data
    def get_basic_attack(self):
        weapon_key = self.equipment.get('weapon')
        weapon = self._equipment_data.get(weapon_key, {})
        if weapon.get('damage_range'):
            return [weapon_key]
        return []

    def get_base_damage(self, wep_name):
        item = self._equipment_data.get(wep_name)
        if item and item.get('damage_range'):
            min_dmg, max_dmg = item['damage_range']
            # damage is a random roll within the item range plus the player's attack stat, includes equip bonuses
            return randint(min_dmg, max_dmg) + self.get_stat('attack')
        # if player doesn't have a wep, use attack stat for damage
        # FIX THIS LATER: this should use fists instead of wep if the player has no wep equipped
        return self.get_stat('attack')

    def update_xp(self, amount):
        remaining_xp_to_level = self.level_up - self.xp
        if remaining_xp_to_level > amount:
            self.xp += amount
        else:
            self.level += 1
            self.xp = amount - remaining_xp_to_level
            self.level_up = self.level * 150