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
parser.add_argument('--list-races', action='store_true')
parser.add_argument('--list-professions', action='store_true')

args = parser.parse_args()

if args.list_races:
  print('Supported races are {}'.format([
 'Wood Elf',
 'High Elf',
 'Dark Elf',
 'Hill Dwarf',
 'Mountain Dwarf',
 'Halforc',
 'Dragonborn',
 'Halfelf',
 'Human',
 'Lightfoot Halfling',
 'Stout Halfling',
 'Forest Gnome',
 'Rock Gnome',
 'Tiefling',
]))
  exit(0)

if args.list_professions:
  print('Supported professions are {}'.format([
 'Barbarian',
 'Bard',
 'Cleric',
 'Druid',
 'Fighter',
 'Monk',
 'Paladin',
 'Ranger',
 'Rogue'
]))
  exit(0)

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
    case 'halforc':
      race_gen = race.halforc()
    case 'dragonborn':
      race_gen = race.dragonborn()
    case 'forest gnome':
      race_gen = race.forestgnome()
    case 'halfelf':
      race_gen = race.halfelf()
    case 'human':
      race_gen = race.human()
    case 'lightfoot halfling':
      race_gen = race.lightfoothalfling()
    case 'stout halfling':
      race_gen = race.stouthalfling()
    case 'rock gnome':
      race_gen = race.rockgnome()
    case 'tiefling':
      race_gen = race.tiefling()
    case _:
      print('Race {} not found'.format(c_race))
      exit(1)

  match(prof.lower()):
    case 'monk':
      prof_gen = profession.monk()
    case 'cleric':
      prof_gen = profession.priest()
    case 'bard':
      prof_gen = profession.bard()
    case 'barbarian':
      prof_gen = profession.barbarian()
    case 'fighter':
      if char['school'] == 'Eldrich Knight':
        prof_gen = profession.eldrichknight()
      else:
        prof_gen = profession.fighter()
    case 'ranger':
      prof_gen = profession.ranger()
    case 'druid':
      prof_gen = profession.druid()
    case 'paladin':
      prof_gen = profession.paladin()
    case 'rogue':
      if char['school'] == 'Arcane Trickster':
        prof_gen = profession.arcanetrickster()
      else:
        prof_gen = profession.rogue()
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
