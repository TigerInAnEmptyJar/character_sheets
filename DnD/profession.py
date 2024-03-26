import pathlib
import json
import string

attribute_short_names = ['ST', 'DX', 'CO', 'IN', 'WI', 'CH']

class profession:
  
  def __init__(self, name):
    self.templateSheet=pathlib.Path(__file__).parent/'templates'/'DnD_template.tex'
    self.name = name
    sheet=pathlib.Path(pathlib.Path(__file__).parent/'tables'/'DnD_{}_tables.json'.format(name.lower()))
    self.table = {}
    if sheet.exists(): 
      prof_f=open(sheet, 'r')
      self.table = json.load(prof_f)
  
  def is_valid(self):
    return ('table' in self.table)
    
  def proficiency(self, level):
    if 'table' in self.table:
      return self.table['table'][level]['pr']
    else:
      return 2
      
  def hits_at_start(self):
    if 'ht_at_start' in self.table:
      return self.table['ht_at_start']
    else:
      return 2
    
  def hit_dice(self):
    if 'hitDice' in self.table:
      return self.table['hitDice']
    else:
      return 4
  
  def addStuff(self, character_dict):    
    if 'features' in self.table:
      for f in self.table['features']:
        character_dict['features'].append(f)
    if 'table' in self.table:
      if not 'features' in character_dict:
        character_dict['features'] = []
      for l in range(character_dict['level']):
        for f in self.table['table'][l]['feat']:
          character_dict['features'].append(f)
    if character_dict['school'] != '':
      if character_dict['school'] in self.table['schools']:
        for l in range(character_dict['level']):
          for f in self.table['schools'][character_dict['school']]['features'][l]:
            character_dict['features'].append(f)
    if 'weapons' in self.table:
      if not 'weapons' in character_dict:
        character_dict['weapons'] = []
      for l in self.table['weapons']:
        character_dict['weapons'].append(l)
    if 'armors' in self.table:
      if not 'armors' in character_dict:
        character_dict['armors'] = []
      for l in self.table['armors']:
        character_dict['armors'].append(l)

  def convert(self, character_dict):
    att=[int((character_dict['attributes']['strength']-10)/2),
      int((character_dict['attributes']['dexterity']-10)/2),
      int((character_dict['attributes']['constitution']-10)/2),
      int((character_dict['attributes']['intelligence']-10)/2),
      int((character_dict['attributes']['wisdom']-10)/2),
      int((character_dict['attributes']['charisma']-10)/2)
    ]
  
    weapons = []
    for w in character_dict['weapons']:
      weapons.append('{}&{}&d{}+{}&{}\\\\'.format(w['name'], att[w['a']]+self.proficiency(character_dict['level']), w['d'], att[w['a']], w['t']))
    for i in range(10-len(weapons)):
      weapons.append('\\\\')
    return {
      'name': character_dict['name'],
      'player': character_dict['player'],
      'profession': character_dict['profession'],
      'level': character_dict['level'],
      'background': character_dict['background'],
      'race': character_dict['race'],
      'sex': character_dict['sex'],
      'alignment': character_dict['alignment'],
      'experience': character_dict['experience'],
      'attrst': character_dict['attributes']['strength'],
      'attrdx': character_dict['attributes']['dexterity'],
      'attrco': character_dict['attributes']['constitution'],
      'attrin': character_dict['attributes']['intelligence'],
      'attrwi': character_dict['attributes']['wisdom'],
      'attrch': character_dict['attributes']['charisma'],
      'attrstb': int((character_dict['attributes']['strength']-10)/2),
      'attrdxb': int((character_dict['attributes']['dexterity']-10)/2),
      'attrcob': int((character_dict['attributes']['constitution']-10)/2),
      'attrinb': int((character_dict['attributes']['intelligence']-10)/2),
      'attrwib': int((character_dict['attributes']['wisdom']-10)/2),
      'attrchb': int((character_dict['attributes']['charisma']-10)/2),
      'hits': ((att[2]+5)*(character_dict['level']-1)+att[2]+self.hits_at_start() if not 'hits' in character_dict else character_dict['hits']),
      'proficiency': self.proficiency(character_dict['level']),
      'armorclass': character_dict["ac"],
      'initiative': att[1],
      'weapons': '\n'.join(weapons),
      'armors': '\n'.join(character_dict['armors']),
      'skill11o': ('\\o{}' if character_dict['skills'][0]>0 else 'o'),
      'skill12o': ('\\o{}' if character_dict['skills'][1]>0 else 'o'),
      'skill21o': ('\\o{}' if character_dict['skills'][2]>0 else 'o'),
      'skill22o': ('\\o{}' if character_dict['skills'][3]>0 else 'o'),
      'skill23o': ('\\o{}' if character_dict['skills'][4]>0 else 'o'),
      'skill24o': ('\\o{}' if character_dict['skills'][5]>0 else 'o'),
      'skill31o': ('\\o{}' if character_dict['skills'][6]>0 else 'o'),
      'skill41o': ('\\o{}' if character_dict['skills'][7]>0 else 'o'),
      'skill42o': ('\\o{}' if character_dict['skills'][8]>0 else 'o'),
      'skill43o': ('\\o{}' if character_dict['skills'][9]>0 else 'o'),
      'skill44o': ('\\o{}' if character_dict['skills'][10]>0 else 'o'),
      'skill45o': ('\\o{}' if character_dict['skills'][11]>0 else 'o'),
      'skill46o': ('\\o{}' if character_dict['skills'][12]>0 else 'o'),
      'skill51o': ('\\o{}' if character_dict['skills'][13]>0 else 'o'),
      'skill52o': ('\\o{}' if character_dict['skills'][14]>0 else 'o'),
      'skill53o': ('\\o{}' if character_dict['skills'][15]>0 else 'o'),
      'skill54o': ('\\o{}' if character_dict['skills'][16]>0 else 'o'),
      'skill55o': ('\\o{}' if character_dict['skills'][17]>0 else 'o'),
      'skill56o': ('\\o{}' if character_dict['skills'][18]>0 else 'o'),
      'skill61o': ('\\o{}' if character_dict['skills'][19]>0 else 'o'),
      'skill62o': ('\\o{}' if character_dict['skills'][20]>0 else 'o'),
      'skill63o': ('\\o{}' if character_dict['skills'][21]>0 else 'o'),
      'skill64o': ('\\o{}' if character_dict['skills'][22]>0 else 'o'),
      'skill65o': ('\\o{}' if character_dict['skills'][23]>0 else 'o'),
      'skill11': character_dict['skills'][0]*self.proficiency(character_dict['level'])+att[0],
      'skill12': character_dict['skills'][1]*self.proficiency(character_dict['level'])+att[0],
      'skill21': character_dict['skills'][2]*self.proficiency(character_dict['level'])+att[1],
      'skill22': character_dict['skills'][3]*self.proficiency(character_dict['level'])+att[1],
      'skill23': character_dict['skills'][4]*self.proficiency(character_dict['level'])+att[1],
      'skill24': character_dict['skills'][5]*self.proficiency(character_dict['level'])+att[1],
      'skill31': character_dict['skills'][6]*self.proficiency(character_dict['level'])+att[2],
      'skill41': character_dict['skills'][7]*self.proficiency(character_dict['level'])+att[3],
      'skill42': character_dict['skills'][8]*self.proficiency(character_dict['level'])+att[3],
      'skill43': character_dict['skills'][9]*self.proficiency(character_dict['level'])+att[3],
      'skill44': character_dict['skills'][10]*self.proficiency(character_dict['level'])+att[3],
      'skill45': character_dict['skills'][11]*self.proficiency(character_dict['level'])+att[3],
      'skill46': character_dict['skills'][12]*self.proficiency(character_dict['level'])+att[3],
      'skill51': character_dict['skills'][13]*self.proficiency(character_dict['level'])+att[4],
      'skill52': character_dict['skills'][14]*self.proficiency(character_dict['level'])+att[4],
      'skill53': character_dict['skills'][15]*self.proficiency(character_dict['level'])+att[4],
      'skill54': character_dict['skills'][16]*self.proficiency(character_dict['level'])+att[4],
      'skill55': character_dict['skills'][17]*self.proficiency(character_dict['level'])+att[4],
      'skill56': character_dict['skills'][18]*self.proficiency(character_dict['level'])+att[4],
      'skill61': character_dict['skills'][19]*self.proficiency(character_dict['level'])+att[5],
      'skill62': character_dict['skills'][20]*self.proficiency(character_dict['level'])+att[5],
      'skill63': character_dict['skills'][21]*self.proficiency(character_dict['level'])+att[5],
      'skill64': character_dict['skills'][22]*self.proficiency(character_dict['level'])+att[5],
      'skill65': character_dict['skills'][23]*self.proficiency(character_dict['level'])+att[5],
      'passiveperception': self.proficiency(character_dict['level']) + att[4] + 10,
      'speed': character_dict['speed'],
      'hitDice': '{} d{}'.format(character_dict['level'], self.hit_dice()),
      'traits': '\\\\ \n'.join(character_dict['features']),
      'personality': character_dict['personality'],
      'ideals': character_dict['ideals'],
      'bonds':character_dict['bonds'],
      'flaws':character_dict['flaws'],
      'languages': '\\\\ \n'.join(character_dict['languages'])
    }
  
  def generate(self, character_dict, filename):
    with open(self.templateSheet,'r') as tf:
      t = string.Template(tf.read())
      sheet = t.safe_substitute(character_dict)
      print('Writing character to file {}.'.format(filename))
      with open(filename, 'w') as output:
        output.write(sheet)

class monk(profession):

  def __init__(self):
    super().__init__('monk')
    print("Reading monk profession")

  def addStuff(self, character_dict):
    super().addStuff(character_dict)
    character_dict['speed'] = character_dict['speed'] + self.table['table'][character_dict['level']]['mv']
    attribute = (1 if character_dict['attributes']['dexterity'] > character_dict['attributes']['strength'] else 0)
    character_dict['weapons'].append({'name': 'Unarmed', 'a':attribute, 'd':self.table['table'][character_dict['level']]['d'], 't': 'cr'})
    for w in character_dict['weapons']:
      w['a'] = attribute
    if not 'ac' in character_dict:
      character_dict['ac'] = 0
    character_dict['ac'] = 10 + character_dict['attributes']['dexterity'] + character_dict['attributes']['wisdom']

class spellcaster(profession):
  def __init__(self, name):
    super().__init__(name)
    self.templateSheet = pathlib.Path(__file__).parent/'templates'/'DnD_template_spellcaster.tex'

  def addStuff(self, character_dict):
    super().addStuff(character_dict)
    school = character_dict['school']
    up_to = int((character_dict['level']-1)/2)+1
    if school in self.table['schools']:
      if 'spells' in self.table['schools'][school]:
        for l in range(up_to):
          for s in self.table['schools'][school]['spells'][l]:
            character_dict['spells'][l].append(s)
    if 'skills' in self.table:
      for a in character_dict['skills']:
        character_dict['skills'][a] = (1 if character_dict['skills'][a] + self.table['skills'][a] >0 else 0)
    character_dict['spell_attribute'] = self.table['spell_attribute']
    character_dict['ncantrips']=self.table['table'][character_dict['level']]['cantrips']
    character_dict['n1levelspells']=self.table['table'][character_dict['level']]['1']
    character_dict['n2levelspells']=self.table['table'][character_dict['level']]['2']
    character_dict['n3levelspells']=self.table['table'][character_dict['level']]['3']
    character_dict['n4levelspells']=self.table['table'][character_dict['level']]['4']
    character_dict['n5levelspells']=self.table['table'][character_dict['level']]['5']
    character_dict['n6levelspells']=self.table['table'][character_dict['level']]['6']
    character_dict['n7levelspells']=self.table['table'][character_dict['level']]['7']
    character_dict['n8levelspells']=self.table['table'][character_dict['level']]['8']
    character_dict['n9levelspells']=self.table['table'][character_dict['level']]['9']
    for s in character_dict['spells']:
      min = len(s) + 2
      if min < 7: 
        min = 7
      for i in range(min - len(s)):
        s.append('')

  def spellSavingThrow(self, character_dict):
    return 8

  def convert(self, character_dict):
    att=[int((character_dict['attributes']['strength']-10)/2),
      int((character_dict['attributes']['dexterity']-10)/2),
      int((character_dict['attributes']['constitution']-10)/2),
      int((character_dict['attributes']['intelligence']-10)/2),
      int((character_dict['attributes']['wisdom']-10)/2),
      int((character_dict['attributes']['charisma']-10)/2)
    ]
    converted = super().convert(character_dict)
    converted['cantrips'] = '\\\\ \n'.join(character_dict['spells'][0])
    converted['spells1'] = '\\\\ \n'.join(character_dict['spells'][1])
    converted['spells2'] = '\\\\ \n'.join(character_dict['spells'][2])
    converted['spells3'] = '\\\\ \n'.join(character_dict['spells'][3])
    converted['spells4'] = '\\\\ \n'.join(character_dict['spells'][4])
    converted['spells5'] = '\\\\ \n'.join(character_dict['spells'][5])
    converted['spells6'] = '\\\\ \n'.join(character_dict['spells'][6])
    converted['spells7'] = '\\\\ \n'.join(character_dict['spells'][7])
    converted['spells8'] = '\\\\ \n'.join(character_dict['spells'][8])
    converted['spells9'] = '\\\\ \n'.join(character_dict['spells'][9])
    converted['ncantrips'] = character_dict['ncantrips']
    converted['n1levelspells'] = character_dict['n1levelspells']
    converted['n2levelspells'] = character_dict['n2levelspells']
    converted['n3levelspells'] = character_dict['n3levelspells']
    converted['n4levelspells'] = character_dict['n4levelspells']
    converted['n5levelspells'] = character_dict['n5levelspells']
    converted['n6levelspells'] = character_dict['n6levelspells']
    converted['n7levelspells'] = character_dict['n7levelspells']
    converted['n8levelspells'] = character_dict['n8levelspells']
    converted['n9levelspells'] = character_dict['n9levelspells']
    converted['spellproficiency'] = self.proficiency(character_dict['level']) + att[character_dict['spell_attribute']]
    converted['spellsavingthrow'] = self.spellSavingThrow(character_dict)
    converted['spellattribute'] = attribute_short_names[character_dict['spell_attribute']]
    return converted
  
class priest(spellcaster):
  def __init__(self):
    super().__init__('priest')
    print('Reading priest profession')

  def spellSavingThrow(self, character_dict):
    return 8 + character_dict['attributes']['wisdom'] + self.table['table'][character_dict['level']]['pr']


class bard(profession):
  
  def __init__(self):
    super().__init__('bard')
    print('Reading bard profession')
    