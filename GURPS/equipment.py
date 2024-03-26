import pathlib
import json

from basic import basic
from skills import skills

class weapons(basic):
  def __init__(self):
    super().__init__('weapons')
    self.weapons = []
    self.ranged = []
    self.armor = []
    self.inventory = []
    self.parries = []
    self.blocks = []
    self.drs = []
    self.total_weight = 0

  def pre(self, advantages, skills, spells, attributes):
    self.advantages = advantages
    self.skills = skills
    self.spells = spells
    self.attributes = attributes

  def findItem(self, name):
    for i in self.table['melee']:
      if i['name'] == name:
        return i
    for i in self.table['ranged']:
      if i['name'] == name:
        return i
    for i in self.table['armor']:
      if i['name'] == name:
        return i
    return None


  def skillLevel(self, name, character_dict):
    aSkill = basic.findInList(name, character_dict['skills'])
    if aSkill == None:
      aSkill = basic.findInList(name, character_dict['spells'])
    lookup = self.skills.findSkill(name)
    if lookup == None:
      lookup = self.spells.findSkill(name)
    if lookup != None and aSkill != None:
      spent = aSkill['points']
      attIndex = lookup['attribute']
      attValue = self.skills.getAttributeValue(attIndex, [], [])
      return skills.skillLevel(spent, lookup['difficulty'], attValue)
    return 0

  def calculateMeleeProperties(self, name, character_dict):
    lookup = self.findItem(name)
    dam = []
    r = []
    if lookup != None:
      for i in range(len(lookup['damage'])):
        dd = self.attributes.damage_table[self.attributes.att[0]][lookup['damage'][i][0]][0]
        da = basic.valueWithSign(self.attributes.damage_table[self.attributes.att[0]][lookup['damage'][i][0]][1]+lookup['damage'][i][1])        
        dam.append('{}d{} ({})'.format(dd, da, lookup['type'][i]))
      for i in range(len(lookup['range'])):
        r.append(str(lookup['range'][i]))
      return {
        'damage': dam,
        'range': r,
        'attack': self.skillLevel(lookup['skill'], character_dict),
        'parry': 3+int(self.skillLevel(lookup['skill'], character_dict)/2)+lookup['parry']+self.attributes.parry,
       'weapon': lookup
      }
    return None

  def calculateRangedProperties(self, name, character_dict, strength):
    lookup = self.findItem(name)
    if lookup != None:
      if 'fixed' in lookup['damage'] and lookup['damage']['fixed']:
        damage = lookup['damage']['value']
      else:
        dam = lookup['damage']['value']
        dd = self.attributes.damage_table[strength][dam[0]][0]
        da = basic.valueWithSign(self.attributes.damage_table[strength][dam[0]][1]+dam[1])        
        damage = '{}d{}'.format(dd, da)
      return {
      'damage': damage,
      'attack': self.skillLevel(lookup['skill'], character_dict),
      'acc': lookup['acc'],
      'range': '{}/{}'.format(lookup['range'][0], lookup['range'][1]),
      'weapon': lookup
      }
    return None

  def process(self, character_dict):
    for w in character_dict["melee"]:
      props = self.calculateMeleeProperties(w, character_dict)
      if props != None:
        if len(props['damage']) == 1:
          weapon_string = '{}&{}&{}&{}&{}&{}&{}'.format(w,'/'.join(props['damage']), '/'.join(props['range']), 
                                                      props['attack'], int(props['parry']), 
                                                      props['weapon']['cost'], props['weapon']['weight'])
        else:
          number = len(props['damage'])
          firstline = '{}&{}&{}&{}&{}&{}&{}\\\\ \n'.format(
            '\\multirow{{{n}}}{{*}}{{{name}}}'.format(n=number, name =w),
            props['damage'][0],
            props['range'][0],
            '\\multirow{{{n}}}{{*}}{{{name}}}'.format(n=number, name=props['attack']),
            '\\multirow{{{n}}}{{*}}{{{name}}}'.format(n=number, name=props['parry']),
            '\\multirow{{{n}}}{{*}}{{{name}}}'.format(n=number, name=props['weapon']['cost']),
            '\\multirow{{{n}}}{{*}}{{{name}}}'.format(n=number, name=props['weapon']['weight'])
          )
          lines = []
          for i in range(number-1):
            lines.append('&{}&{}&&&&'.format(props['damage'][i+1], props['range'][i+1]))
          weapon_string = firstline + '\\\\ \n'.join(lines)
        self.weapons.append(weapon_string)
        self.total_weight += props['weapon']['weight']
        self.parries.append('\\scriptsize {}: \\normalsize {}'.format(w, int(props['parry'])))
    basic.expandList(self.weapons, 7, '&&&&&&')
    for w in character_dict["ranged"]:
      st = self.attributes.att[0] if w['st'] == None else w['st']
      props = self.calculateRangedProperties(w['name'], character_dict, st)
      if props != None:
        bulk = ''
        weapon_string = '{}&{}&{}&{}&{}&{}&{}&{}&{}&{}'.format(w['name'],
                                                               props['damage'], 
                                                               props['attack'], 
                                                               props['acc'],
                                                               props['range'], w['shots'],
                                                               st, bulk,
                                                               props['weapon']['cost'], 
                                                               props['weapon']['weight'])
        if props['weapon']['weight'] != None:
          self.total_weight += props['weapon']['weight'][0] + props['weapon']['weight'][1]*w['shots']
        self.ranged.append(weapon_string)
    basic.expandList(self.ranged, 7, '&&&&&&&&&')
    for w in character_dict["armor"]:
      lookup = self.findItem(w)
      if lookup != None:
        armor_string = '{}&{}&{}&{}&{}'.format(w, lookup['dr'], lookup['loc'], 
                                               lookup['cost'], lookup['weight'])
        self.armor.append(armor_string)
        self.total_weight += lookup['weight']
        self.drs.append('\\scriptsize {}: \\normalsize {}'.format(lookup['loc'], lookup['dr']))
    basic.expandList(self.armor, 7, '&&&&')
    basic.expandList(self.drs, 3, ' ')
    for w in character_dict["inventory"]:
      inventory_string = '{}&{}&{}'.format(w['name'], w['cost'], w['weight'])
      self.inventory.append(inventory_string)
      self.total_weight += w['weight']
    basic.expandList(self.inventory, 20, '&&')
    print('Total weight: {}'.format(self.total_weight))

  def addToDict(self, out_dict):
    out_dict['melee']='\\\\ \\hline\n'.join(self.weapons)
    out_dict['ranged']='\\\\ \\hline\n'.join(self.ranged)
    out_dict['armor']='\\\\ \\hline\n'.join(self.armor)
    out_dict['inventory']='\\\\ \\hline\n'.join(self.inventory)
    out_dict['damageresistance']='\\ \n'.join(self.drs)
    out_dict['parrying']='\\ \n'.join(self.parries)
