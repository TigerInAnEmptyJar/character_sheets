import pathlib
import argparse
import json
import string
import inspect
import os
import subprocess
import shutil

import race
import profession

template_sheet=pathlib.Path('DnD_template.tex')

parser = argparse.ArgumentParser(prog='dnd2tex', description='Converts a DnD json sheet to tex', add_help=True)
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
  prof = char['profession']
  c_race = char['race']
  
  match(c_race.lower()):
    case 'wood elf':
      race_gen = race.woodelf()
    case 'high elf':
      race_gen = race.highelf()
    case 'dark elf':
      race_gen = race.darkelf()
    case 'hill dwarf':
      race_gen = race.hilldwarf()
    case 'mountain dwarf':
      race_gen = race.mountaindwarf()
    case _:
      print('Race {} not found'.format(c_race))
      exit(1)

  match(prof.lower()):
    case 'monk':
      prof_gen = profession.monk()
    case 'cleric':
      prof_gen = profession.priest()
    case _:
      print('Profession {} not found'.format(prof))
      exit(1)

  race_gen.addStuff(char)
  prof_gen.addStuff(char)

  char_dict = prof_gen.convert(char)


  prof_gen.generate(char_dict, out_tex_file)
  
  print('Generate pdf {}'.format(out_path))
  current = pathlib.Path().cwd()
  scriptPath = pathlib.Path(inspect.getfile(inspect.currentframe()))
  os.chdir(out_parent / 'build')
  proc = subprocess.run(['pdflatex', out_tex_file], capture_output=True)
  os.chdir(current)

  shutil.copyfile(out_parent/'build'/out_path.name, out_path)
