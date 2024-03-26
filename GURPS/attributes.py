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
    out_dict['strength'] = self.att[0]
    out_dict['dexterity'] = self.att[1]
    out_dict['intelligence'] = self.att[2]
    out_dict['constitution'] = self.att[3]
    out_dict['hits'] = self.att[4]
    out_dict['will'] = self.att[5]
    out_dict['perception'] = self.att[6]
    out_dict['fatigue'] = self.att[7]
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
