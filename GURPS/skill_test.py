
import json
import sys
from skills import skills, spells, skills_v3, spells_v3, psionics
#from attributes import attributes, attributes_v3
from advantages import advantages
import sheet
import pathlib


skill_list = ["test/skill_1.json", "test/skill_2.json", "test/languages_1.json"]
spell_list = ["test/spell_1.json"]

def test_skill_v4(char, filename):
    actual = {"name": "test"}
    for i in char["expected"]:
        try: 
            skill_table = skills()
            skill_table.pre(i["attr"], advantages_table)
            skill_table.process(char["input"])
            skill_table.addToDict(actual)
            if actual != i["out4"]:
                print("Skill_v4 Test failed in file {}\n  Actual:   {}\n  Expected: {}".format(file, actual, i["out4"]))
                raise Exception()
        except:
            print(repr(sys.exception()))

def test_skill_v3(char, filename):
    actual = {"name": "test"}
    for i in char["expected"]:
        try: 
            skill_table = skills_v3()
            skill_table.pre(i["attr"], advantages_table)
            skill_table.process(char["input"])
            skill_table.addToDict(actual)
            if actual != i["out3"]:
                print("Skill_v3 Test failed in file {}\n  Actual:   {}\n  Expected: {}".format(file, actual, i["out3"]))
                raise Exception()
            sheeter = sheet.sheet(pathlib.Path(__file__).parent/'templates'/'V3Orig')
            output = sheeter.format_spell_table(actual['spells'])
            if output != i["print3"]:
                print("Spell output failed in file {}\n  Actual:   {}\n  Expected: {}".format(file, output, i["print3"]))
                raise Exception()
        except:
            print(repr(sys.exception()))

def test_spell_v3(char, filename):
    actual = {"name": "test"}
    for i in char["expected"]:
        try: 
            spell_table = spells_v3()
            spell_table.pre(i["attr"], advantages_table)
            spell_table.process(char["input"])
            spell_table.addToDict(actual)
            if actual != i["out3"]:
                print("Spell_v3 Test failed in file {}\n  Actual:   {}\n  Expected: {}".format(file, actual, i["out3"]))
                raise Exception()
            sheeter = sheet.sheet(pathlib.Path(__file__).parent/'templates'/'V3Orig')
            output = sheeter.format_spell_table(actual['spells'])
            if output != i["print4"]:
                print("Spell output failed in file {}\n  Actual:   {}\n  Expected: {}".format(file, output, i["print4"]))
                raise Exception()
        except:
            print(repr(sys.exception()))

def test_spell_v4(char, filename):
    actual = {"name": "test"}
    for i in char["expected"]:
        try: 
            spell_table = spells_v3()
            spell_table.pre(i["attr"], advantages_table)
            spell_table.process(char["input"])
            spell_table.addToDict(actual)
            if actual != i["out4"]:
                print("Spell_v4 Test failed in file {}\n  Actual:   {}\n  Expected: {}".format(file, actual, i["out4"]))
                raise Exception()
        except:
            print(repr(sys.exception()))

advantages_table = advantages()
for file in skill_list:
    with open(pathlib.Path(__file__).parent/file) as f:
        char = json.load(f)
        test_skill_v4(char, file)
        test_skill_v3(char, file)

for file in spell_list:
    with open(pathlib.Path(__file__).parent/file) as f:
        char = json.load(f)
        test_spell_v3(char, file)
        test_spell_v4(char, file)