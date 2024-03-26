import pathlib
import json

class basic:
  att_names = ["HT", "DX", 'IQ', 'HT', 'HP', 'WI', 'PER', 'FP']

  def __init__(self, name):
    print('Reading table {}'.format(name))
    path = pathlib.Path(__file__).parent/'tables/{}.json'.format(name)
    if not path.exists():
      print('File {} doesn\'t exist'.format(path))
      exit(1)
    with open(path) as f:
      self.table = json.load(f)
      self.total_points = 0
  
  def expandList(list, size, entry):
    if len(list) < size:
      for i in range(size-len(list)):
        list.append(entry)

  def valueWithSign(value):
    if value > 0:
      return '+{}'.format(value)
    elif value == 0:
      return ''
    return '{}'.format(value)

  def findInList(name, lst):
    for i in lst:
      if i['name'] == name:
        return i
    return None