import pathlib
import json
import string

class sheet:
    def __init__(self, directory):
        self.sheet_dir = pathlib.Path(directory)
        with open(directory/'lines.json', 'r') as f:
            self.lines = json.load(f)


    def format_general(self, character_dict):
        return string.Template('\n'.join(self.lines['general'])).safe_substitute(character_dict)
    
    def format_reaction(self, character_dict):
        react = []
        if 'appearance' in character_dict:
            d = character_dict['appearance']
            if 'other' in d:
                d['other'] = '({})'.format(d['other'])
            react.append(string.Template(self.lines['appearance']['appear']).safe_substitute(d))
        if 'charisma' in character_dict:
            d = character_dict['charisma']
            react.append(string.Template(self.lines['appearance']['charisma']).safe_substitute(d))
        return (self.lines['appearance']['begin'] + '\n' + 
                '\n'.join(react) + "\n" +
                self.lines['appearance']['end'])
    '''
    advantage_dict = {'name': 'foo', 
                      'points': 10}
    '''
    def format_advantage(self, advantage_dict):
        return string.Template(self.lines['advantages']['line']).safe_substitute(advantage_dict)
    
    def format_advantages(self, advantage_dict_list):
        ad = []
        dis = []
        for a in advantage_dict_list:
            if a['points'] > 0:
                ad.append(self.format_advantage(a))
            else:
                dis.append(self.format_advantage(a))
        while(len(ad) < len(dis)):
            ad.append(self.lines['advantages']['empty'])
        while(len(ad) > len(dis)):
            dis.append(self.lines['advantages']['empty'])
        return (self.lines['advantages']['page-begin'] + '\n' +
                string.Template(self.lines['advantages']['table-begin']).safe_substitute({'type': 'ADVANTAGES'}) + '\n' +
                '\n'.join(ad) +
                self.lines['advantages']['table-end'] + '\n' +
                string.Template(self.lines['advantages']['table-begin']).safe_substitute({'type': 'DISADVANTAGES'}) + '\n' +
                '\n'.join(dis) +
                self.lines['advantages']['table-end'] + '\n' +
                self.lines['advantages']['page-end'])

    '''
    attribute_dict = {
        'strength': {'v': 10, 'pt': 0},
        'dexterity': {'v': 10, 'pt': 0},
        'intelligence': {'v': 10, 'pt': 0},
        'health': {'v': 10, 'pt': 0},
        'fatigue': {'v': 10, 'pt': 0},
        'will': {'v': 10, 'pt': 0},
        'perception': {'v': 10, 'pt': 0},
        'hits': {'v': 10, 'pt': 0}
    }
    '''
    def format_attributes(self, attribute_dict_list):
        subst = {'strength': attribute_dict_list['strength']['v'],
                 'strengthpt': attribute_dict_list['strength']['pt'],
                 'dexterity': attribute_dict_list['dexterity']['v'],
                 'dexteritypt': attribute_dict_list['dexterity']['pt'],
                 'intelligence': attribute_dict_list['intelligence']['v'],
                 'intelligencept': attribute_dict_list['intelligence']['pt'],
                 'constitution': attribute_dict_list['constitution']['v'],
                 'constitutionpt': attribute_dict_list['constitution']['pt'],
                 'hits': attribute_dict_list['hits']['v'],
                 'hitspt': attribute_dict_list['hits']['pt'],
                 'will': attribute_dict_list['will']['v'],
                 'willpt': attribute_dict_list['will']['pt'],
                 'perception': attribute_dict_list['perception']['v'],
                 'perceptionpt': attribute_dict_list['perception']['pt'],
                 'fatigue': attribute_dict_list['fatigue']['v'],
                 'fatiguept': attribute_dict_list['fatigue']['pt']}
        return string.Template('\n'.join(self.lines['attributes'])).safe_substitute(subst)

    '''
    language_dict = {'pt': 1
                     'name': 'foo', 
                     'is_written': True,
                     'is_spoken': False,
                     'value': 15,
                     'attribute_value': 'IQ+1'}
    '''
    def format_language(self, language_dict):
        return string.Template(self.lines['language']['line']).safe_substitute({
            'pt': language_dict['pt'], 
            'name': language_dict['name'], 
            'is_written': self.lines['language']['is_learned'] if language_dict['is_written'] else self.lines['language'] ['not_learned'],
            'is_spoken': self.lines['language']['is_learned'] if language_dict['is_spoken'] else self.lines['language'] ['not_learned'],
            'attribute_value': language_dict['attribute_value'],
            'value': language_dict['value']
        })

    def format_language_table(self, language_dict_list):
        all_languages = []
        for l in language_dict_list:
            all_languages.append(self.format_language(l))
        return (self.lines['language']['table-begin'] + '\n' +
                '\n'.join(all_languages) + '\n' +
                self.lines['language']['table-end'])

    '''
    skill_dict = {'pt': 0, 
                  'name': 'foo', 
                  'type': 'm/d', 
                  'attribute_value': 'IQ+10', 
                  'value': '20'}
    '''
    def format_skill(self, skill_dict):
        return string.Template(self.lines['skill']['line']).safe_substitute(skill_dict)
    
    def format_skill_table(self, skill_dict_list):
        formatted_skill_list = []
        for s in skill_dict_list:
            formatted_skill_list.append(self.format_skill(s))
        return (self.lines['skill']['table-begin'] + '\n' +
               '\n'.join(formatted_skill_list) + '\n' + 
               self.lines['skill']['table-end'])
    
    '''
    spell_dict = {'pt': 0, 
                  'name': 'foo', 
                  'college': 'Water',
                  'type': 'm/d', 
                  'attribute_value': 'IQ+10', 
                  'value': '20'}
    '''
    def format_spell(self, spell_dict):
        return string.Template(self.lines['spell']['line']).safe_substitute(spell_dict)
    
    def format_spell_table(self, spell_dict_list):
        if len(spell_dict_list) == 0:
            return ''
        formatted_spell_dict = {}
        for s in spell_dict_list:
            if not s['college'] in formatted_spell_dict:
                formatted_spell_dict[s['college']] = []
            formatted_spell_dict[s['college']].append(self.format_spell(s))
        all_spells = []
        for c in formatted_spell_dict:
            all_spells.append(string.Template(self.lines['spell']['college-begin']).safe_substitute({'college': c}) +
                              '\n'.join(formatted_spell_dict[c]) + '\n' +
                              self.lines['spell']['college-end'])
        return (self.lines['spell']['page-begin'] + '\n' + 
                '\n'.join(all_spells) + '\n' + 
                self.lines['spell']['page-end'])
    
    '''
    psi_skill_dict = {'pt': 0, 
                      'name': 'foo', 
                      'type': 'm/d', 
                      'attribute_value': 'IQ+10', 
                      'value': '20'.
                      'psi': 'ESP'}
    '''
    def format_psi_skill(self, psi_skill_dict):
        return string.Template(self.lines['psi']['line']).safe_substitute(psi_skill_dict)
    
    '''
    psi_list = [ {'pt': 25,
                  'name': 'foo',
                  'level_cost': '5/lvl',
                  'value': 5,
    } ]
    '''
    def format_psi_table(self, psi_list):
        if len(psi_list) == 0:
            return ''
        formatted_psi_list = []
        for p in psi_list:
            formatted_psi_list.append(string.Template(self.lines['psi']['psi-line']).safe_substitute(p))
        return (self.lines['psi']['psi-table-begin'] + '\n' +
                '\n'.join(formatted_psi_list) + '\n' +
                self.lines['psi']['psi-table-end'])

        
    def format_psi_page(self, psi_skill_dict_list, psi_list):
        psi_skills = ''
        if len(psi_skill_dict_list) > 0:
            formatted_psi_dict = {}
            for s in psi_skill_dict_list:
                if not s['psi'] in formatted_psi_dict:
                    formatted_psi_dict[s['psi']] = []
                formatted_psi_dict[s['psi']].append(self.format_psi_skill(s))
            all_psi_skills = []
            for p in formatted_psi_dict:
                all_psi_skills.append(string.Template(self.lines['psi']['table-begin']).safe_substitute({'psi_type': p}) +
                                  '\n'.join(formatted_psi_dict[p]) +
                                  self.lines['psi']['table-end'])
            psi_skills = (string.Template(self.lines['psi']['page-begin']).safe_substitute({'psitable':self.format_psi_table(psi_list)}) + '\n' + 
                    '\n'.join(all_psi_skills) + '\n' +
                    self.lines['psi']['page-end'])
        return psi_skills
        
    def write_sheet(self, character, outfile):
        template_path = self.sheet_dir/'GURPS_template.tex'
        with open(template_path, 'r') as tf:
            t = string.Template(tf.read())
            subst = {'commands': '\n'.join(self.lines['commands']),
                     'general': self.format_general(character),
                     'totalpoints': character['totalpoints'],
                     'unspentpoints': character['unspentpoints'],
                     'attributes': self.format_attributes(character['attributes']),
                     'languages': self.format_language_table(character['languages']),
                     'advantages': self.format_advantages(character['advantages']),
                     'reaction': self.format_reaction(character),
                     'skills': self.format_skill_table(character['skills']),
                     'spells': "",
                     'psionics': "",
                     'melee': character['melee'],
                     'ranged': character['ranged'],
                     'armor': character['armor'],
                     'inventory': character['inventory'],
                     'basicspeedpt': character['basicspeedpt'],
                     'basicspeed': character['basicspeed'],
                     'basicmovept': character['basicmovept'],
                     'basicmove': character['basicmove'],
                     'basiclift': character['basiclift'],
                     'parrying': character['parrying'],
                     'damageresistance': character['damageresistance'],
                     'damageswing': character['damageswing'],
                     'damagethrust': character['damagethrust'],
                     'dodge1': character['dodge1'],
                     'dodge2': character['dodge2'],
                     'dodge3': character['dodge3'],
                     'dodge4': character['dodge4'],
                     'dodge0': character['dodge0'],
                     'bl0': character['bl0'],
                     'bl1': character['bl1'],
                     'bl2': character['bl2'],
                     'bl3': character['bl3'],
                     'bl4': character['bl4'],
                     'mv0': character['mv0'],
                     'mv1': character['mv1'],
                     'mv2': character['mv2'],
                     'mv3': character['mv3'],
                     'mv4': character['mv4']}
            if 'psionics' in character:
                subst['psionics'] = self.format_psi_page(character['psionics'], character['psi'])
            if 'spells' in character:
                subst['spells'] = self.format_spell_table(character['spells'])
            character_sheet = t.safe_substitute(subst)
            print('Writing character to file {}'.format(outfile))
            with open(outfile,'w') as output:
                output.write(character_sheet)
