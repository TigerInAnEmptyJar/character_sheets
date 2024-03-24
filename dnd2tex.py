import pathlib
import argparse
import json
import string

class race:

  def __init__(self, name):
    sheet=pathlib.Path('DnD_{}_tables.json'.format(name.lower()))
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
    if 'weapons' in self.table:
      if not 'weapons' in character_dict:
        character_dict['weapons'] = []
      for l in self.table['weapons']:
        character_dict['weapons'].append(l)
    if 'attributes' in self.table:
      for a in character_dict['attributes']:
        character_dict['attributes'][a] = character_dict['attributes'][a] + self.table['attributes'][a]
    
class woodelf(race):
  
  def __init__(self):
    super().__init__('WoodElf')

class profession:
  
  def __init__(self, name):
    self.templateSheet=pathlib.Path('DnD_template.tex')
    self.name = name
    sheet=pathlib.Path('DnD_{}_tables.json'.format(name.lower()))
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




template_sheet=pathlib.Path('DnD_template.tex')

parser = argparse.ArgumentParser(prog='dnd2tex', description='Converts a DnD json sheet to tex', add_help=True)
parser.add_argument('filename')
parser.add_argument('--outfile', action='store', required=True)

args = parser.parse_args()

print('Convert character in {} to tex in file {}.'.format(args.filename, args.outfile))

with open(args.filename) as f:
  char = json.load(f)
  prof = char['profession']
  c_race = char['race']
  
  match(c_race.lower()):
    case 'wood elf':
      race_gen = woodelf()
    case _:
      print('Race {} not found'.format(c_race))
      exit(1)

  match(prof.lower()):
    case 'monk':
      prof_gen = monk()
    case _:
      print('Profession {} not found'.format(prof))
      exit(1)

  race_gen.addStuff(char)
  prof_gen.addStuff(char)

#  proficiency = prof_gen.proficiency(char['level'])
  att=[int((char['attributes']['strength']-10)/2),
    int((char['attributes']['dexterity']-10)/2),
    int((char['attributes']['constitution']-10)/2),
    int((char['attributes']['intelligence']-10)/2),
    int((char['attributes']['wisdom']-10)/2),
    int((char['attributes']['charisma']-10)/2)
  ]

  weapons = []
  for w in char['weapons']:
    weapons.append('{}&{}&d{}+{}&{}\\\\'.format(w['name'], att[w['a']]+prof_gen.proficiency(char['level']), w['d'], att[w['a']], w['t']))
  for i in range(10-len(weapons)):
    weapons.append('\\\\')
  char_dict={
    'name': char['name'],
    'player': char['player'],
    'profession': char['profession'],
    'level': char['level'],
    'background': char['background'],
    'race': char['race'],
    'sex': char['sex'],
    'alignment': char['alignment'],
    'experience': char['experience'],
    'attrst': char['attributes']['strength'],
    'attrdx': char['attributes']['dexterity'],
    'attrco': char['attributes']['constitution'],
    'attrin': char['attributes']['intelligence'],
    'attrwi': char['attributes']['wisdom'],
    'attrch': char['attributes']['charisma'],
    'attrstb': int((char['attributes']['strength']-10)/2),
    'attrdxb': int((char['attributes']['dexterity']-10)/2),
    'attrcob': int((char['attributes']['constitution']-10)/2),
    'attrinb': int((char['attributes']['intelligence']-10)/2),
    'attrwib': int((char['attributes']['wisdom']-10)/2),
    'attrchb': int((char['attributes']['charisma']-10)/2),
    'hits': ((att[2]+5)*(char['level']-1)+att[2]+prof_gen.hits_at_start() if not 'hits' in char else char['hits']),
    'proficiency': prof_gen.proficiency(char['level']),
    'armorclass': 10 + att[1] + att[4],
    'initiative': att[1],
    'weapons': '\n'.join(weapons),
    'skill11o': ('\\o{}' if char['skills'][0]>0 else 'o'),
    'skill12o': ('\\o{}' if char['skills'][1]>0 else 'o'),
    'skill21o': ('\\o{}' if char['skills'][2]>0 else 'o'),
    'skill22o': ('\\o{}' if char['skills'][3]>0 else 'o'),
    'skill23o': ('\\o{}' if char['skills'][4]>0 else 'o'),
    'skill24o': ('\\o{}' if char['skills'][5]>0 else 'o'),
    'skill31o': ('\\o{}' if char['skills'][6]>0 else 'o'),
    'skill41o': ('\\o{}' if char['skills'][7]>0 else 'o'),
    'skill42o': ('\\o{}' if char['skills'][8]>0 else 'o'),
    'skill43o': ('\\o{}' if char['skills'][9]>0 else 'o'),
    'skill44o': ('\\o{}' if char['skills'][10]>0 else 'o'),
    'skill45o': ('\\o{}' if char['skills'][11]>0 else 'o'),
    'skill46o': ('\\o{}' if char['skills'][12]>0 else 'o'),
    'skill51o': ('\\o{}' if char['skills'][13]>0 else 'o'),
    'skill52o': ('\\o{}' if char['skills'][14]>0 else 'o'),
    'skill53o': ('\\o{}' if char['skills'][15]>0 else 'o'),
    'skill54o': ('\\o{}' if char['skills'][16]>0 else 'o'),
    'skill55o': ('\\o{}' if char['skills'][17]>0 else 'o'),
    'skill56o': ('\\o{}' if char['skills'][18]>0 else 'o'),
    'skill61o': ('\\o{}' if char['skills'][19]>0 else 'o'),
    'skill62o': ('\\o{}' if char['skills'][20]>0 else 'o'),
    'skill63o': ('\\o{}' if char['skills'][21]>0 else 'o'),
    'skill64o': ('\\o{}' if char['skills'][22]>0 else 'o'),
    'skill65o': ('\\o{}' if char['skills'][23]>0 else 'o'),
    'skill11': char['skills'][0]*prof_gen.proficiency(char['level'])+att[0],
    'skill12': char['skills'][1]*prof_gen.proficiency(char['level'])+att[0],
    'skill21': char['skills'][2]*prof_gen.proficiency(char['level'])+att[1],
    'skill22': char['skills'][3]*prof_gen.proficiency(char['level'])+att[1],
    'skill23': char['skills'][4]*prof_gen.proficiency(char['level'])+att[1],
    'skill24': char['skills'][5]*prof_gen.proficiency(char['level'])+att[1],
    'skill31': char['skills'][6]*prof_gen.proficiency(char['level'])+att[2],
    'skill41': char['skills'][7]*prof_gen.proficiency(char['level'])+att[3],
    'skill42': char['skills'][8]*prof_gen.proficiency(char['level'])+att[3],
    'skill43': char['skills'][9]*prof_gen.proficiency(char['level'])+att[3],
    'skill44': char['skills'][10]*prof_gen.proficiency(char['level'])+att[3],
    'skill45': char['skills'][11]*prof_gen.proficiency(char['level'])+att[3],
    'skill46': char['skills'][12]*prof_gen.proficiency(char['level'])+att[3],
    'skill51': char['skills'][13]*prof_gen.proficiency(char['level'])+att[4],
    'skill52': char['skills'][14]*prof_gen.proficiency(char['level'])+att[4],
    'skill53': char['skills'][15]*prof_gen.proficiency(char['level'])+att[4],
    'skill54': char['skills'][16]*prof_gen.proficiency(char['level'])+att[4],
    'skill55': char['skills'][17]*prof_gen.proficiency(char['level'])+att[4],
    'skill56': char['skills'][18]*prof_gen.proficiency(char['level'])+att[4],
    'skill61': char['skills'][19]*prof_gen.proficiency(char['level'])+att[5],
    'skill62': char['skills'][20]*prof_gen.proficiency(char['level'])+att[5],
    'skill63': char['skills'][21]*prof_gen.proficiency(char['level'])+att[5],
    'skill64': char['skills'][22]*prof_gen.proficiency(char['level'])+att[5],
    'skill65': char['skills'][23]*prof_gen.proficiency(char['level'])+att[5],
    'passiveperception': prof_gen.proficiency(char['level']) + att[4] + 10,
    'speed': char['speed'],
    'hitDice': prof_gen.hit_dice(),
    'traits': '\\\\ \n'.join(char['features']),
    'personality': char['personality'],
    'ideals': char['ideals'],
    'bonds':char['bonds'],
    'flaws':char['flaws'],
    'languages': '\\\\ \n'.join(char['languages'])
  }

  prof_gen.generate(char_dict, args.outfile)
