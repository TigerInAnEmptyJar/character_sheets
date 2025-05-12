from basic import basic

class attributes:
  damage_table = [ [],
    [[1, -6],[1, -5]],
    [[1, -6],[1, -5]],
    [[1, -5],[1, -4]],
    [[1, -5],[1, -4]],
    [[1, -4],[1, -3]],
    [[1, -4],[1, -3]],
    [[1, -3],[1, -2]],
    [[1, -3],[1, -2]],
    [[1, -2],[1, -1]],
    [[1, -2],[1, 0]],
    [[1, -1],[1, 1] ],
    [[1, -1],[1, 2] ],
    [[1, 0] ,[2, -1]],
    [[1, 0] ,[2, 0]],
    [[1, 1] ,[2, 1]],
    [[1, 1] ,[2, 2]],
    [[1, 2] ,[3, -1]],
    [[1, 2] ,[3, 0] ],
    [[2, -1],[3, 1] ],
    [[2, -1],[3, 2] ],
    [[2, 0] ,[4, -1]]
  ]

  def __init__(self):
    self.total_points = 0
  
  def damageString(self, st, index):
    tab = attributes.damage_table[st][index]
    add_value = tab[1]
    add_string = basic.valueWithSign(add_value)
    return '{}d{}'.format(tab[0], add_string)

  def process(self, character_dict):
    self.att = [
      int(10 + character_dict['attributes']['strength']/10),
      int(10 + character_dict['attributes']['dexterity']/20),
      int(10 + character_dict['attributes']['intelligence']/20),
      int(10 + character_dict['attributes']['constitution']/10)
    ]
    self.att.append(int(self.att[0]+character_dict['attributes']['hp']/2))
    self.att.append(int(self.att[2]+character_dict['attributes']['will']/5))
    self.att.append(int(self.att[2]+character_dict['attributes']['perception']/5))
    self.att.append(int(self.att[3]+character_dict['attributes']['fatigue']/3))

    for i in character_dict['attributes']:
      self.total_points += character_dict['attributes'][i]

    self.basic_speed = (self.att[1]+self.att[3])/4 + (character_dict['attributes']['speed']/20)
    self.basic_move = int(self.basic_speed + character_dict['attributes']['move']/5)
    self.basic_lift = int(0.5+self.att[0]*self.att[0]/5)
    self.damage_swing = self.damageString(self.att[0], 1)
    self.damage_thrust = self.damageString(self.att[0], 0)
    self.dodge = int((self.att[1]+self.att[3])/4 + (character_dict['attributes']['speed']/20)) +3 + character_dict['attributes']['dodge']/15
    self.block = character_dict['attributes']['block']/5
    self.parry = character_dict['attributes']['block']/5

  def addToDict(self, out_dict):
    out_dict['attributes']['strength']['v'] = self.att[0]
    out_dict['attributes']['dexterity']['v'] = self.att[1]
    out_dict['attributes']['intelligence']['v'] = self.att[2]
    out_dict['attributes']['constitution']['v'] = self.att[3]
    out_dict['attributes']['hits']['v'] = self.att[4]
    out_dict['attributes']['will']['v'] = self.att[5]
    out_dict['attributes']['perception']['v'] = self.att[6]
    out_dict['attributes']['fatigue']['v'] = self.att[7]
    out_dict['basicspeed'] = self.basic_speed
    out_dict['basicmove'] = self.basic_move
    out_dict['basiclift'] = self.basic_lift
    out_dict['damageswing'] = self.damage_swing
    out_dict['damagethrust'] = self.damage_thrust
    out_dict['dodge1'] = self.dodge-1
    out_dict['dodge2'] = self.dodge-2
    out_dict['dodge3'] = self.dodge-3
    out_dict['dodge4'] = self.dodge-4
    out_dict['dodge0'] = self.dodge
    out_dict['bl0'] = self.basic_lift*1
    out_dict['bl1'] = self.basic_lift*2
    out_dict['bl2'] = self.basic_lift*3
    out_dict['bl3'] = self.basic_lift*6
    out_dict['bl4'] = self.basic_lift*10
    out_dict['mv0'] = int(self.basic_move)
    out_dict['mv1'] = int(self.basic_move*0.8)
    out_dict['mv2'] = int(self.basic_move*0.6)
    out_dict['mv3'] = int(self.basic_move*0.4)
    out_dict['mv4'] = int(self.basic_move*0.2)
    if hasattr(self, 'appearance'):
      out_dict['appearance']=self.appearance
    if hasattr(self, 'charisma'):
      out_dict['charisma']=self.charisma

class attributes_v3(attributes):
  damage_table = [ [],
    [[1, -6],[1, -5]],#1
    [[1, -6],[1, -5]],
    [[1, -5],[1, -4]],
    [[1, -5],[1, -4]],
    [[1, -4],[1, -3]],#5
    [[1, -4],[1, -3]],
    [[1, -3],[1, -2]],
    [[1, -3],[1, -2]],
    [[1, -2],[1, -1]],
    [[1, -2],[1, 0]],#10
    [[1, -1],[1, 1] ],
    [[1, -1],[1, 2] ],
    [[1, 0] ,[2, -1]],
    [[1, 0] ,[2, 0]],
    [[1, 1] ,[2, 1]],#15
    [[1, 1] ,[2, 2]],
    [[1, 2] ,[3, -1]],
    [[1, 2] ,[3, 0] ],
    [[2, -1],[3, 1] ],
    [[2, -1],[3, 2] ],#20
    [[2, 0] ,[4, -1]],
    [[2, 0],  [4, 0]],
    [[2, 1],  [4, 1]],
    [[2, 1],  [4, 2]],
    [[2, 2],  [5, -1]],#25
    [[2, 2],  [5, 0]],
    [[3, -1], [5, 1]],
    [[3, -1], [5, 1]],
    [[3, 0],  [5, 2]],
    [[3, 0],  [5, 2]],#30
    [[3, 1],  [6, -1]],
    [[3, 1],  [6, -1]],
    [[3, 2],  [6, 0]],
    [[3, 2],  [6, 0]],
    [[4, -1], [6, 1]],#35
    [[4, -1], [6, 1]],
    [[4, 0],  [6, 2]],
    [[4, 0],  [6, 2]],
    [[4, 1],  [7, -1]],
    [[4, 1],  [7, -1]]#40
  ]

  appears = [{'name': 'Abstoßend', 'pt': -20, 'bonus': -4},
             {'name': 'Hässlich', 'pt': -10, 'bonus': -2},
             {'name': 'Unattractive', 'pt': -5, 'bonus': -1},
             {},
             {'name': 'Attractive', 'pt': 5, 'bonus': 1},
             {'name': 'Sch\\"on', 'pt': 15, 'bonus': 2, 'other': 4},
             {'name': 'Wundersch\\"on', 'pt': 25, 'bonus': 2, 'other': 6}]

  costs = [-100, -80, -70, -60, -50, -40, -30, -20, -15, -10, 0,
           10, 20, 30, 45, 60, 80, 100, 125, 150, 175]

  def __init__(self):
    self.total_points = 0
  
  def _calc_value(self, pt):
    val = 0
    while pt > attributes_v3.costs[val]:
      val = val+1
    return val
    

  def process(self, character_dict):
    self.att = [self._calc_value(character_dict['attributes']['strength']),
                self._calc_value(character_dict['attributes']['dexterity']),
                self._calc_value(character_dict['attributes']['intelligence']),
                self._calc_value(character_dict['attributes']['constitution'])]
    self.att.append(int(self.att[0]+character_dict['attributes']['hp']/5))
    self.att.append(int(self.att[2]+character_dict['attributes']['will']/4))
    self.att.append(int(self.att[2]+character_dict['attributes']['perception']/5))
    self.att.append(int(self.att[3]+character_dict['attributes']['fatigue']/3))

    for i in character_dict['attributes']:
      self.total_points += character_dict['attributes'][i]

    self.basic_speed = (self.att[1]+self.att[3])/4 + (character_dict['attributes']['speed']/25)
    self.basic_move = int(self.basic_speed + character_dict['attributes']['move']/10)
    self.basic_lift = int(0.5+self.att[0]*self.att[0]/5)
    self.damage_swing = self.damageString(self.att[0], 1)
    self.damage_thrust = self.damageString(self.att[0], 0)
    self.dodge = self.basic_speed +3 + character_dict['attributes']['dodge']/15
    self.block = character_dict['attributes']['block']/5
    self.parry = character_dict['attributes']['block']/5
    if 'appearance' in character_dict and character_dict['appearance'] != 0:
      self.appearance = attributes_v3.appears[character_dict['appearance']+3]
      self.total_points += self.appearance['pt']
    if 'charisma' in character_dict:
      self.charisma = {'name': 'Charisma', 'pt': character_dict['charisma'], 'bonus': int(character_dict['charisma']/5)}
      self.total_points += character_dict['charisma']
    print('{} points from attributes'.format(self.total_points))  

