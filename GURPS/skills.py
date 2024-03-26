from basic import basic

class skills(basic):
  def __init__(self, name = 'skills'):
    self.skills = []
    self.skills2 = []
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
          lst.append(a)
        aa = spells.findElement(a['name'], disadv)
        if aa != None:
          lst.append(a)
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
    spent = aSkill['points']
    lookup = self.findSkill(name)
    if lookup != None:
      attIndex = lookup['attribute']
      attValue = self.getAttributeValue(attIndex, adv, disadv)
      addon = 0
      if 'adds' in lookup:
        for a in self.allAdvantages(lookup['adds'], adv, disadv):
          addon += a['level']
      level = skills.skillLevel(spent, lookup['difficulty'], attValue) + addon
      return '{}&{}&{}&{}'.format(spent, name, '{}{}'.format(basic.att_names[attIndex], basic.valueWithSign(level - self.att[attIndex])), level)
    else:
      print('Skill {} not found'.format(name))
    return '&&&'

  def process(self, character_dict):
    for s in character_dict[self.name]:
      skillString = self.calcSkill(s, character_dict['advantages'], character_dict['disadvantages'])
      if len(self.skills) <50:
        self.skills.append(skillString)
      else:
        self.skills2.append(skillString)
      self.total_points += s['points']
    basic.expandList(self.skills, 50, '&&&')
    basic.expandList(self.skills2, 50, '&&&')
  
  def addToDict(self, out_dict):
    out1 = '{}1'.format(self.name)
    out2 = '{}2'.format(self.name)
    out_dict[out1] = '\\\\ \\hline\n'.join(self.skills)
    out_dict[out2] = '\\\\ \\hline\n'.join(self.skills2)

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
      addition += a['level']
    return self.att[index] + addition 
