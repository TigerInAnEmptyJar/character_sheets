from basic import basic

class advantages(basic):
  def __init__(self):
    super().__init__('advantages')
    self.advantages = []
    self.disadvantages = []

  def find_advantage(self, name):
    for a in self.table:
      if a['name'] == name:
        return a
    return None 
 
  def calc_advantage(self, adv, lookup):
    points = 0
    name = adv['name']
    lookup = self.find_advantage(name)
    specs = []
    if lookup != None:
      points = lookup['points']
      if 'level' in lookup and lookup['level'] and 'level' in adv:
        points = points * adv['level']
        specs.append('lvl {}'.format(adv['level']))
      if 'typed' in lookup and lookup['typed'] and 'is' in adv:
        specs.append(adv['is'])
    add = ''
    if len(specs) > 0:
      add = ' ({})'.format(', '.join(specs)) 
    return {'name': '{}{}'.format(name, add), 'points': points}

  def process(self, character_dict):
    for a in character_dict['advantages']:
      lookup = self.find_advantage(a['name'])
      if lookup != None:
        adv = self.calc_advantage(a, lookup)
        self.total_points += adv['points']
        self.advantages.append(adv)
    for a in character_dict['disadvantages']:
      lookup = self.find_advantage(a['name'])
      if lookup != None:
        adv = self.calc_advantage(a, lookup)
        self.total_points += adv['points']
        self.advantages.append(adv)

  def addToDict(self, out_dict):
    out_dict['advantages'] = self.advantages
