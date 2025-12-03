NPC_DATA = {
    '0001': {
        'dialogue': {
            'default': [
                "Hello, my name is Professor Griffiths.",
                "I never thought i'd be an NPC in a Pokemon knockoff!"
            ]
        },
        'directions': ['down', 'left', 'up', 'right'],
        'look_around': True,
        'defeated': False,
    }
}

MONSTER_DATA = {
    'Kermit': {
        'stats': {
            'element': 'plant',
            'max_health': 15,
            'max_energy': 17,
            'attack': 4,
            'defense': 8,
            'recovery': 5,
            'speed': 1
        },
        'abilities': {0: 'scratch', 1: 'bite'}
    },
}

MONSTER_ATTACK_DATA = {
    'scratch': {'target': 'opponent', 'amount': 1, 'cost': 20, 'element': 'normal'},
    'bite':    {'target': 'opponent', 'amount': 1.2, 'cost': 20, 'element': 'normal'}
    }

PLAYER_DATA = {
    'Player': {
        'stats': {
            'max_health': 20,
            'max_energy': 20,
            'attack': 5,
            'defense': 5,
            'recovery': 5,
            'speed': 1
        }
    }
}

EQUIPMENT_DATA = {
    'fists': {
        'name': 'Fists',
        'slot': 'weapon',
        'stats': {
            'attack': 0,
            'defense': 0,
            'speed': 0,
            'max_health': 0,
            'max_energy': 0,
            'recovery': 0
        },
        'damage_range': (2, 4)
    },
    'empty_slot': {
        'name': 'Empty Slot',
        'slot': 'none',
        'stats': {
            'attack': 0,
            'defense': 0,
            'speed': 0,
            'max_health': 0,
            'max_energy': 0,
            'recovery': 0
        },
    },

    'rusty_sword': {
        'name': 'Rusty Sword',
        'slot': 'weapon',
        'stats': {
            'attack': 3,
            'speed': -1,
            'recovery': 0
        },
        'damage_range': (5, 10)
    },
    'cloth_tunic': {
        'name': 'Cloth Tunic',
        'slot': 'armor',
        'stats': {
            'defense': 2,
            'max_health': 5,
            'recovery': 0
        },
    },
    'adventurer_ring': {
        'name': 'Adventurer Ring',
        'slot': 'accessory',
        'stats': {
            'recovery': 5,
            'max_energy': 5,
            'attack': 0},
    }
}

PLAYER_STARTER_EQUIPMENT = {
            'weapon': 'rusty_sword',
            'armor': 'cloth_tunic',
            'accessory': 'adventurer_ring',
        }