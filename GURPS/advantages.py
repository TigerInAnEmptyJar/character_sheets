from basic import basic

class advantages(basic):
  def __init__(self):
    super().__init__('advantages')
    self.advantages = []
    self.disadvantages = []

  def process(self, character_dict):
    for a in character_dict['advantages']:
      points = 0
      name = a['name']
      for aa in self.table:
        if aa['name'] == name:
          points = aa['points']
      if 'level' in a:
        points = points * a['level']
        name = '{} ({})'.format(name, a['level'])
      self.total_points += points
      self.advantages.append('{}&{}'.format(name, points))
    for a in character_dict['disadvantages']:
      points = 0
      for aa in self.table:
        if aa['name'] == a['name']:
          points = aa['points']
      if 'level' in a:
        points = points * a['level']
      self.total_points += points
      self.disadvantages.append('{}&{}'.format(a['name'], points))
    basic.expandList(self.advantages, 20, '&')
    basic.expandList(self.disadvantages, 20, '&')

  def addToDict(self, out_dict):
    out_dict['advantages'] = '\\\\ \\hline\n'.join(self.advantages)
    out_dict['disadvantages'] = '\\\\ \\hline\n'.join(self.disadvantages)
