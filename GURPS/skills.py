from basic import basic
import json

class skills(basic):
  difficulty_string = ['e', 'd', 'h', 'x']

  def __init__(self, name = 'skills'):
    self.skills = []
    self.name = name
    super().__init__(name)

  def pre(self, att, advant):
    self.att = att
    self.advantages_table = advant

  def allAdvantages(self, property, adv, disadv):
    lst = []
    for a in self.advantages_table.table:
      if property in a:
        aa = spells.findElement(a['name'], adv)
        if aa != None:
          lst.append([a,aa])
        aa = spells.findElement(a['name'], disadv)
        if aa != None:
          lst.append([a,aa])
    return lst

  def getAttributeValue(self, index, adv, disadv):
    return self.att[index] 

  def findSkill(self, name):
    for i in self.table:
      if i['name'] == name:
        if not 'attribute' in i:
          i['attribute'] = 2
        if not 'difficulty' in i:
          if 'hard' in i and i['hard']:
            i['difficulty'] = 3
          else:
            i['difficulty'] = 2
        return i
    return None

  def skillLevel(points, difficulty, attribute):
    if points <= 0:
      return 0
    pt_add = 1
    match(points):
      case 1:
        pt_add = 0
      case 2:
        pt_add = 1
      case 4:
        pt_add = 2
      case _:
        pt_add = 2 + int((points -4)/4)
    return attribute-difficulty + pt_add

  def calcSkill(self, aSkill, adv, disadv):
    name = aSkill['name']
    lookup = self.findSkill(name)
    if lookup != None:
      is_mental = lookup['attribute'] == 2 or lookup['attribute'] == 6 or lookup['attribute'] == 5
      spent = aSkill['points']
      attIndex = lookup['attribute']
      attValue = self.getAttributeValue(attIndex, adv, disadv)
      addon = 0
      if 'adds' in lookup:
        for a in self.allAdvantages(lookup['adds'], adv, disadv):
          addon += a[0]['level']
      level = skills.skillLevel(spent, lookup['difficulty'], attValue) + addon
      skill = {'pt': spent, 
              'name': name, 
              'type': '{}/{}'.format('m' if is_mental else 'p', skills.difficulty_string[lookup['difficulty']]), 
              'attribute_value': '{}{}'.format(basic.att_names[attIndex], basic.valueWithSign(level - self.att[attIndex])), 
              'value': level}
      if 'college' in lookup:
        skill['college'] = lookup['college']
      if 'psi' in lookup:
        skill['psi'] = lookup['psi']
      return skill
    else:
      print('Skill {} not found'.format(name))
    return None

  def process(self, character_dict):
    for s in character_dict[self.name]:
      skill = self.calcSkill(s, character_dict['advantages'], character_dict['disadvantages'])
      if skill != None:
        self.skills.append(skill)
      self.total_points += s['points']
    self.languages = []
    for l in character_dict['languages']:
      att = self.getAttributeValue(2, character_dict['advantages'], character_dict['disadvantages'])
      level = skills.skillLevel(l['points'] * 1, 1, att)
      self.total_points += l['points']
      self.languages.append({'pt': l['points'], 
                           'name': l['name'], 
                           'is_spoken': l['spoken'], 
                           'is_written': l['written'], 
                           'value': level, 
                           'attribute_value': 'IQ{}'.format(basic.valueWithSign(level - att))})    
    print('{} points from skills'.format(self.total_points))  
  
  def addToDict(self, out_dict):
    out_dict[self.name]=self.skills
    if hasattr(self, 'languages'):
      out_dict['languages']=self.languages

class spells(skills):
  def __init__(self):
    super().__init__('spells')

  def findElement(name, lst):
    for i in lst:
      if i['name'] == name:
        return i
    return None
    
  def getAttributeValue(self, index, adv, disadv):
    addition = 0
    for a in self.allAdvantages('spells', adv, disadv):
      addition += a[0]['level']
    return self.att[index] + addition 

class skills_v3(basic):

  def __init__(self, name = 'skills_v3'):
    self.skills = []
    self.name = name
    if name == 'skills_v3':
      self.name = 'skills'
    super().__init__(name)

  def pre(self, att, advant):
    self.att = att
    self.advantages_table = advant

  def allAdvantages(self, property, adv, disadv):
    lst = []
    for a in self.advantages_table.table:
      if property in a:
        aa = spells.findElement(a['name'], adv)
        if aa != None:
          lst.append([a,aa])
        aa = spells.findElement(a['name'], disadv)
        if aa != None:
          lst.append([a,aa])
    return lst

  def getAttributeValue(self, index, adv, disadv):
    return self.att[index] 

  def findSkill(self, name):
    for i in self.table:
      if i['name'] == name:
        if not 'attribute' in i:
          i['attribute'] = 2
        if not 'difficulty' in i:
          if 'hard' in i and i['hard']:
            i['difficulty'] = 3
          else:
            i['difficulty'] = 2
        return i
    return None

  def skillLevel(points, difficulty, attribute, is_mental):
    if points <= 0:
      return 0
    pt_add = 1
    match(points):
      case 1:
        pt_add = 0
      case 2:
        pt_add = 1
      case 4:
        pt_add = 2
      case _:
        if is_mental and difficulty < 3:
          pt_add = 2 + int((points -4)/2)
        elif is_mental:
          pt_add = 2 + int((points -4)/4)
        else:
          pt_add = 2 + int((points -4)/8)
    return attribute-difficulty + pt_add

  def calcSkill(self, aSkill, adv, disadv):
    name = aSkill['name']
    lookup = self.findSkill(name)
    if lookup != None:
      is_mental = True
      if 'mental' in lookup:
        is_mental = lookup['mental']
      spent = aSkill['points']
      attIndex = lookup['attribute']
      attValue = self.getAttributeValue(attIndex, adv, disadv)
      addon = 0
      if 'adds' in lookup:
        for a in self.allAdvantages(lookup['adds'], adv, disadv):
          addon += a[0]['level']
      level = skills_v3.skillLevel(spent * self.point_multiplier[0 if is_mental else 1], lookup['difficulty'], attValue, is_mental) + addon
      skill = {'pt': spent, 
              'name': name, 
              'type': '{}/{}'.format('m' if is_mental else 'p', skills.difficulty_string[lookup['difficulty']]), 
              'attribute_value': '{}{}'.format(basic.att_names[attIndex], basic.valueWithSign(level - self.att[attIndex])), 
              'value': level}
      if 'college' in lookup:
        skill['college'] = lookup['college']
      if 'psi' in lookup:
        skill['psi'] = lookup['psi']
      return skill
    else:
      print('Skill {} not found'.format(name))
    return None

  def process(self, character_dict):
    self.point_multiplier = [1, 1]
    for a in character_dict['advantages']:
      if a['name'] == 'Eidetic Memory':
        self.point_multiplier[0] = 2
      if a['name'] == 'Eidetic Memory 2':
        self.point_multiplier[0] = 4  
    for s in character_dict[self.name]:
      skill = self.calcSkill(s, character_dict['advantages'], character_dict['disadvantages'])
      if skill != None:
        self.skills.append(skill)
      self.total_points += s['points']
    self.languages = []
    for l in character_dict['languages']:
      att = self.getAttributeValue(2, character_dict['advantages'], character_dict['disadvantages'])
      level = skills_v3.skillLevel(l['points'] * self.point_multiplier[0], 1, att, True)
      self.total_points += l['points']
      self.languages.append({'pt': l['points'], 
                             'name': l['name'], 
                             'is_spoken': l['spoken'], 
                             'is_written': l['written'], 
                             'value': level, 
                             'attribute_value': 'IQ{}'.format(basic.valueWithSign(level - att))})    
    print('{} points from skills'.format(self.total_points))  

  
  def addToDict(self, out_dict):
    out_dict[self.name]=self.skills
    if hasattr(self, 'languages'):
      out_dict['languages']=self.languages

class spells_v3(skills_v3):
  def __init__(self):
    super().__init__('spells')

  def findElement(name, lst):
    for i in lst:
      if i['name'] == name:
        return i
    return None
    
  def getAttributeValue(self, index, adv, disadv):
    addition = 0
    for a in self.allAdvantages('spells', adv, disadv):
      addition += a[0]['level']
    return self.att[index] + addition 
  
  def process(self, character_dict):
    self.point_multiplier = [1, 1]
    for s in character_dict[self.name]:
      spell = self.calcSkill(s, character_dict['advantages'], character_dict['disadvantages'])
      if spell != None:
        for a in self.allAdvantages('college', character_dict['advantages'], character_dict['disadvantages']):
          if spell['college'] == a[1]['is']:
            spell['value'] += a[1]['level'] 
        self.skills.append(spell)
      self.total_points += s['points']
    print('{} points from spells'.format(self.total_points))  


class psionics(skills_v3):
   
  def __init__(self):
    super().__init__('psionics')
    self.psi = []

  def findSkill(self, name):
    for p in self.table:
      for i in self.table[p]['skills']:
        if i['name'] == name:
          if not 'attribute' in i:
            i['attribute'] = 2
          if not 'difficulty' in i:
            if 'hard' in i and i['hard']:
              i['difficulty'] = 3
            else:
              i['difficulty'] = 2
          if not 'psi' in i:
            i['psi'] = p
          return i
    return None

  def process(self, character_dict):
    self.point_multiplier = [1,1]
    for p in character_dict[self.name]:
      pt_per_level = self.table[p]['points']
      self.psi.append({'name': p, 'pt': character_dict[self.name][p]['points'], 'level_cost': '{}/lvl'.format(pt_per_level), 'value': int(character_dict[self.name][p]['points']/pt_per_level)})
      for s in character_dict[self.name][p]['skills']:
        skill = self.calcSkill(s, character_dict['advantages'], character_dict['disadvantages'])
        if skill != None:
          skill['psi'] = p
          self.skills.append(skill)
        self.total_points += s['points']
      self.total_points += character_dict[self.name][p]['points']
    print('{} points from psi'.format(self.total_points))  


  def addToDict(self, out_dict):
    out_dict[self.name]=self.skills
    out_dict['psi']=self.psi
