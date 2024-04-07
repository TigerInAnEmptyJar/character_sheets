import pathlib
import json
import random

def roll_attribute():
    return random.choice([8,9,10,11,12,13,14,15,16,17,18])
    
def roll_skill_table(number):
    skills = []
    for i in range(24):
        skills.append(random.choice([0,1]))
    return skills

def roll_some_weapons():
    return [{'name': 'Light Crossbow', 'a': 1, 'd': 8, 't': 'pi'}]

def roll_some_spells(level):
    return [ [],
             [],
             [],
             [],
             [],
             [],
             [],
             [],
             [],
             []
           ]

def roll_some_languages(level):
    return []

def roll_some_feats(level):
    f = []
    if level >= 4:
        f.append('feat1')
    if level >= 8:
        f.append('feat2')
    if level >= 12:
        f.append('feat3')
    if level >= 16:
        f.append('feat4')
    if level >= 20:
        f.append('feat5')
    return f

def create_character(profession, race, level, skills):
    return {
            'name': 'Beard Stronginthearm',
            'player': 'Bob',
            'profession': profession,
            'level': level,
            'background': 'Acolyte',
            'race': race,
            'sex': 'male',
            'alignment': 'Neutral Good',
            'experience': 'Lathander',
            'attributes': {
                'strength': roll_attribute(),
                'dexterity': roll_attribute(),
                'constitution': roll_attribute(),
                'intelligence': roll_attribute(),
                'wisdom': roll_attribute(),
                'charisma': roll_attribute()
            },
            'ac': 18,
            'skills': skills,
            'features': [],
            'personality': 'Confused',
            'ideals': 'Greater Good',
            'bonds': 'Common People',
            'flaws': 'Gluttony',
            'languages': []
            }

def generate(datapath):
    professions = {'Barbarian': {'schools': [
                    {'n': 'Path of the Berserker', 'c': False},
                    {'n': 'Path of the Totem Warrior', 'c': False}
                   ]}, 
                   'Bard': {'schools': [
                    {'n': 'College of Lore', 'c': True},
                    {'n': 'College of Valor', 'c': True},
                    {'n': 'College of Creation', 'c': True},
                    {'n': 'College of Eloquence', 'c': True},
                    {'n': 'College of Glamour', 'c': True},
                    {'n': 'College of Spirits', 'c': True},
                    {'n': 'College of Swords', 'c': True},
                    {'n': 'College of Whispers', 'c': True}
                   ]}, 
                   'Cleric': {'schools': [
                    {'n': 'Life', 'c': True},
                    {'n': 'Knowledge', 'c': True},
                    {'n': 'Light', 'c': True},
                    {'n': 'Nature', 'c': True},
                    {'n': 'Tempest', 'c': True},
                    {'n': 'Trickery', 'c': True},
                    {'n': 'War', 'c': True}
                   ]}, 
                   'Druid': {'schools': [
                    {'n': 'Circle of the Land', 'c': True},
                    {'n': 'Circle of the Moon', 'c': True}
                   ]}, 
                   'Fighter': {'schools': [
                    {'n': 'Champion', 'c': False},
                    {'n': 'Battle Master', 'c': False},
                    {'n': 'Eldrich Knight', 'c': True}
                   ]}, 
                   'Monk': {'schools': [
                    {'n': 'Way of Mercy', 'c': False},
                    {'n': 'Way of the Ascendant Dragon', 'c': False},
                    {'n': 'Way of the Astral Self', 'c': False},
                    {'n': 'Way of the Drunken Master', 'c': False},
                    {'n': 'Way of the Four Elements', 'c': False},
                    {'n': 'Way of the Kensei', 'c': False},
                    {'n': 'Way of the Long Death', 'c': False},
                    {'n': 'Way of the Open Hand', 'c': False},
                    {'n': 'Way of Shadow', 'c': False},
                    {'n': 'Way of the Sun Soul', 'c': False}
                   ]}, 
                   'Paladin': {'schools': [
                    {'n': 'Oath of Devotion', 'c': True},
                    {'n': 'Oath of Ancients', 'c': True},
                    {'n': 'Oath of Vengenance', 'c': True}
                   ]}, 
                   'Ranger': {'schools': [
                    {'n': 'Hunter', 'c': True},
                    {'n': 'Beast Master', 'c': True}
                   ]}, 
                   'Rogue': {'schools': [
                    {'n': 'Thief', 'c': False},
                    {'n': 'Assassin', 'c': False},
                    {'n': 'Arcane Trickster', 'c': True}
                   ]}}
    races = [
            'Wood Elf',
            'High Elf',
            'Dark Elf',
            'Hill Dwarf',
            'Mountain Dwarf',
            'Halforc',
            'Dragonborn',
            'Halfelf',
            'Human',
            'Lightfoot Halfling',
            'Stout Halfling',
            'Forest Gnome',
            'Rock Gnome',
            'Tiefling',
            ]
    for p in professions.keys():
        for r in races:
            for l in range(20):
                character = create_character(p, r, l+1, roll_skill_table(5))
                for s in professions[p]['schools']:
                    c = character
                    c['school'] = s['n']
                    c['weapons'] = roll_some_weapons()
                    if s['c']:
                        c['spells'] = roll_some_spells(l + 1)
                    c['languages'] = roll_some_languages(l + 1)
                    c['feats'] = roll_some_feats(l + 1)
                    file = datapath/(p + '_' + r + '_' + s['n'] + '_' + str(l) + '.json')
                    with open(file, 'w') as f:
                        json.dump(c, f)

outPath = pathlib.Path.cwd() / 'generated_data'
if not outPath.exists():
    outPath.mkdir()
generate(outPath)