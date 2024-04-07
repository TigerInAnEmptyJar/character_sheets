import pathlib
import json

class race:

  def __init__(self, name):
    sheet=pathlib.Path(pathlib.Path(__file__).parent/'tables'/'DnD_{}_tables.json'.format(name.lower()))
    self.table = {}
    if sheet.exists(): 
      race_f=open(sheet, 'r')
      self.table = json.load(race_f)

  def addStuff(self, character_dict):    
    if 'speed' in self.table:
      character_dict['speed'] = self.table['speed']
    if 'features' in self.table:
      if not 'features' in character_dict:
        character_dict['features'] = []
      for f in self.table['features']:
        character_dict['features'].append(f)
    if 'languages' in self.table:
      if not 'languages' in character_dict:
        character_dict['languages'] = []
      for l in self.table['languages']:
        character_dict['languages'].append(l)
    if not 'weapons' in character_dict:
      character_dict['weapons'] = []
    if 'weapons' in self.table:
      for l in self.table['weapons']:
        character_dict['weapons'].append(l)
    if 'attributes' in self.table:
      for a in character_dict['attributes']:
        character_dict['attributes'][a] = character_dict['attributes'][a] + self.table['attributes'][a]
    if 'proficiencies' in self.table:
      for a in range(len(character_dict['skills'])):
        character_dict['skills'][a] = (1 if character_dict['skills'][a] + self.table['proficiencies'][a] > 0 else 0)
    if not 'armors' in character_dict:
      character_dict['armors'] = []
    if 'armors' in self.table:
      for l in self.table['armors']:
        character_dict['armors'].append(l)
    
class woodelf(race):  
  def __init__(self):
    super().__init__('WoodElf')

class highelf(race):  
  def __init__(self):
    super().__init__('HighElf')

class darkelf(race):  
  def __init__(self):
    super().__init__('DarkElf')

  def addStuff(self, character_dict):
    super().addStuff(character_dict)
    if not 'spells' in character_dict:
      character_dict['spells'] = []
    for s in self.table['spells']:
      character_dict['spells'].append(s)

class hilldwarf(race):
  def __init__(self):
    super().__init__('HillDwarf')

class mountaindwarf(race):
  def __init__(self):
    super().__init__('MountainDwarf')

class halforc(race):
  def __init__(self):
    super().__init__('Halforc')

class dragonborn(race):  
  def __init__(self):
    super().__init__('Dragonborn')
  def addStuff(self, character_dict):
    super().addStuff(character_dict)
    # if not 'spells' in character_dict:
    #   character_dict['spells'] = []
    # for s in self.table['spells']:
    #   character_dict['spells'].append(s)
    if character_dict['level'] >= 16:
      d = '5d6'
    elif character_dict['level']>= 11:
      d = '4d6'
    elif character_dict['level']>= 6:
      d = '3d6'
    else:
      d = '2d6' 
    character_dict['weapons'].append({'name': 'Breath Weapon', 'd': d, 'a': 2,'t': 'element'})

class forestgnome(race):  
  def __init__(self):
    super().__init__('ForestGnome')
  def addStuff(self, character_dict):
    super().addStuff(character_dict)
    if not 'spells' in character_dict:
      character_dict['spells'] = []
    for s in self.table['spells']:
      character_dict['spells'].append(s)

class halfelf(race):  
  def __init__(self):
    super().__init__('HalfElf')

class human(race):  
  def __init__(self):
    super().__init__('Human')

class lightfoothalfling(race):  
  def __init__(self):
    super().__init__('LightfootHalfling')

class stouthalfling(race):  
  def __init__(self):
    super().__init__('StoutHalfling')

class rockgnome(race):  
  def __init__(self):
    super().__init__('RockGnome')

class tiefling(race):  
  def __init__(self):
    super().__init__('Tiefling')

  def addStuff(self, character_dict):
    super().addStuff(character_dict)
    if not 'spells' in character_dict:
      character_dict['spells'] = []
    for s in self.table['spells']:
      character_dict['spells'].append(s)

