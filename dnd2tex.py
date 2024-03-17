import pathlib
import argparse
import json
import string

template_sheet=pathlib.Path('DnD_template.tex')

parser = argparse.ArgumentParser(prog='dnd2tex', description='Converts a DnD json sheet to tex', add_help=True)
parser.add_argument('filename')
parser.add_argument('--outfile', action='store', required=True)

args = parser.parse_args()

print('Convert character in {} to tex in file {}.'.format(args.filename, args.outfile))

with open(args.filename) as f:
  char = json.load(f)
  prof = char['profession']
  prof_sheet=pathlib.Path('DnD_{}_tables.json'.format(prof.lower()))
  proficiency = 2
  speed = 45
  hits_at_start = 8
  traits=char['traits']
  hit_dice = 8
  weapons=[]
  att=[int((char['attributes']['strength']-10)/2),
    int((char['attributes']['dexterity']-10)/2),
    int((char['attributes']['constitution']-10)/2),
    int((char['attributes']['intelligence']-10)/2),
    int((char['attributes']['wisdom']-10)/2),
    int((char['attributes']['charisma']-10)/2)
  ]
  if prof_sheet.exists():
    prof_f=open(prof_sheet, 'r')
    pr = json.load(prof_f)
    proficiency=pr['table'][char['level']]['pr']
    speed=35+pr['table'][char['level']]['mv']
    hits_at_start = pr['ht_at_start']
    hit_dice = pr['hitDice']
    for f in pr['features']:
      traits.append(f)
    for l in range(char['level']):
      for f in pr['table'][l]['feat']:
        traits.append(f)
    if char['school'] != '':
      if char['school'] in pr['schools']:
        for l in range(char['level']):
          for f in pr['schools'][char['school']]['features'][l]:
            traits.append(f)
        
    if prof.lower() == 'monk':
      weapons.append('{}&{}&d{}+{}&{}\\\\'.format('Unarmed', att[1]+proficiency, pr['table'][char['level']]['d'], att[1], 'cr'))
  for w in char['weapons']:
    weapons.append('{}&{}&d{}+{}&{}\\\\'.format(w['name'], att[w['a']]+proficiency, w['d'], att[w['a']], w['t']))
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
    'hits': (att[2]+5)*(char['level']-1)+att[2]+hits_at_start,
    'proficiency': proficiency,
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
    'skill11': char['skills'][0]+(proficiency if char['skills'][0]>0 else 0)+att[0],
    'skill12': char['skills'][1]+(proficiency if char['skills'][1]>0 else 0)+att[0],
    'skill21': char['skills'][2]+(proficiency if char['skills'][2]>0 else 0)+att[1],
    'skill22': char['skills'][3]+(proficiency if char['skills'][3]>0 else 0)+att[1],
    'skill23': char['skills'][4]+(proficiency if char['skills'][4]>0 else 0)+att[1],
    'skill24': char['skills'][5]+(proficiency if char['skills'][5]>0 else 0)+att[1],
    'skill31': char['skills'][6]+(proficiency if char['skills'][6]>0 else 0)+att[2],
    'skill41': char['skills'][7]+(proficiency if char['skills'][7]>0 else 0)+att[3],
    'skill42': char['skills'][8]+(proficiency if char['skills'][8]>0 else 0)+att[3],
    'skill43': char['skills'][9]+(proficiency if char['skills'][9]>0 else 0)+att[3],
    'skill44': char['skills'][10]+(proficiency if char['skills'][10]>0 else 0)+att[3],
    'skill45': char['skills'][11]+(proficiency if char['skills'][11]>0 else 0)+att[3],
    'skill46': char['skills'][12]+(proficiency if char['skills'][12]>0 else 0)+att[3],
    'skill51': char['skills'][13]+(proficiency if char['skills'][13]>0 else 0)+att[4],
    'skill52': char['skills'][14]+(proficiency if char['skills'][14]>0 else 0)+att[4],
    'skill53': char['skills'][15]+(proficiency if char['skills'][15]>0 else 0)+att[4],
    'skill54': char['skills'][16]+(proficiency if char['skills'][16]>0 else 0)+att[4],
    'skill55': char['skills'][17]+(proficiency if char['skills'][17]>0 else 0)+att[4],
    'skill56': char['skills'][18]+(proficiency if char['skills'][18]>0 else 0)+att[4],
    'skill61': char['skills'][19]+(proficiency if char['skills'][19]>0 else 0)+att[5],
    'skill62': char['skills'][20]+(proficiency if char['skills'][20]>0 else 0)+att[5],
    'skill63': char['skills'][21]+(proficiency if char['skills'][21]>0 else 0)+att[5],
    'skill64': char['skills'][22]+(proficiency if char['skills'][22]>0 else 0)+att[5],
    'skill65': char['skills'][23]+(proficiency if char['skills'][23]>0 else 0)+att[5],
    'passiveperception': proficiency + att[4] + 10,
    'speed': speed,
    'hitDice': hit_dice,
    'traits': '\\\\ \n'.join(traits),
    'personality': char['personality'],
    'ideals': char['ideals'],
    'bonds':char['bonds'],
    'flaws':char['flaws'],
    'languages': '\\\\ \n'.join(char['languages'])
  }
  print('Open template file {}'.format(template_sheet))
  if not template_sheet.exists():
    print('template doesn\'t exist!')
  with open(template_sheet,'r') as tf:
    t = string.Template(tf.read())
    sheet = t.safe_substitute(char_dict)
    print('Writing character to file {}.'.format(args.outfile))
    with open(args.outfile, 'w') as output:
      output.write(sheet)
