import pathlib
import argparse
import json
import string
import inspect
import os
import subprocess
import shutil

from basic import basic
from advantages import advantages
from skills import skills, spells
from attributes import attributes
from equipment import weapons

template_sheet=pathlib.Path(__file__).parent/'GURPS_template.tex'

parser = argparse.ArgumentParser(prog='gurps2tex', description='Converts a GURPS json sheet to tex', add_help=True)
parser.add_argument('filename')
parser.add_argument('--outfile', action='store', required=True)

args = parser.parse_args()

out_path = pathlib.Path(args.outfile)
if not out_path.is_absolute():
  out_path = pathlib.Path().cwd() / out_path
if len(out_path.suffixes) == 0:
  out_path = out_path.parent / (out_path.name + '.pdf')
out_parent = out_path.parent 
out_tex_file=out_parent / 'build' / (out_path.stem + '.tex')

print('Convert character in {} to tex in file {}.'.format(args.filename, out_tex_file))


with open(args.filename) as f:
  char = json.load(f)
  
  attribute_table = attributes()
  advantages_table = advantages()
  skill_table = skills()
  spell_table = spells()
  attribute_table.process(char)
  skill_table.pre(attribute_table.att, advantages_table)
  spell_table.pre(attribute_table.att, advantages_table)
  advantages_table.process(char)
  skill_table.process(char)
  spell_table.process(char)
  total_points = attribute_table.total_points + advantages_table.total_points + skill_table.total_points + spell_table.total_points

  weapon_table = weapons()
  weapon_table.pre(advantages_table, skill_table, spell_table, attribute_table)
  weapon_table.process(char)

  print('Points in Sheet {} vs calculated {}'.format(char['total_points'], total_points))  
  char_dict = {
    'name': char['name'],
    'player': char['player'],
    'height': char['height'],
    'weight': char['weight'],
    'age': char['age'],
    'sizemodifier': char['size_mod'],
    'profession': char['profession'],
    'race': char['race'],
    'totalpoints': char['total_points'],
    'unspentpoints': char['unspent_points'],
    'strengthpt': char['attributes']['strength'],
    'dexteritypt': char['attributes']['dexterity'],
    'intelligencept': char['attributes']['intelligence'],
    'constitutionpt': char['attributes']['constitution'],
    'hitspt': char['attributes']['hp'],
    'willpt': char['attributes']['will'],
    'perceptionpt': char['attributes']['perception'],
    'fatiguept': char['attributes']['fatigue'],
    'basicspeedpt': char['attributes']['speed'],
    'basicmovept': char['attributes']['move']
  }
  attribute_table.addToDict(char_dict)
  skill_table.addToDict(char_dict)
  spell_table.addToDict(char_dict)
  advantages_table.addToDict(char_dict)
  weapon_table.addToDict(char_dict)

  with open(template_sheet,'r') as tf:
     t = string.Template(tf.read())
     sheet = t.safe_substitute(char_dict)
     print('Writing character to file {}.'.format(out_tex_file))
     with open(out_tex_file, 'w') as output:
       output.write(sheet)

  print('Generate pdf {}'.format(out_path))
  current = pathlib.Path().cwd()
  scriptPath = pathlib.Path(inspect.getfile(inspect.currentframe()))
  os.chdir(out_parent / 'build')
  proc = subprocess.run(['pdflatex', out_tex_file], capture_output=True)
  os.chdir(current)

  shutil.copyfile(out_parent/'build'/out_path.name, out_path)
