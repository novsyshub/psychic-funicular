import random as r

class Scale():
    def __init__(self,scale_type,root,scale=None,chords=None,valid_notes=None):
        if scale_type.lower() == 'major' or scale_type.lower() == 'minor':
            self.scale_type = scale_type.lower()
        else:
            raise ValueError('scale_type accepts "major" or "minor" (case insensitive)')
        if root.lower().endswith('sharp') or root.lower() in ['a','b','c','d','e','f','g']:
            self.root = root.lower()
            self.valid_notes = {
            1:'c',
            2:'c_sharp',
            3:'d',
            4:'d_sharp',
            5:'e',
            6:'f',
            7:'f_sharp',
            8:'g',
            9:'g_sharp',
            10:'a',
            11:'a_sharp',
            12:'b'
            }
        elif root.lower().endswith('flat'):
            self.root = root.lower()
            self.valid_notes = {
            1:'c',
            2:'d_flat',
            3:'d',
            4:'e_flat',
            5:'e',
            6:'f',
            7:'g_flat',
            8:'g',
            9:'a_flat',
            10:'a',
            11:'b_flat',
            12:'b'
            }
        else:
            raise ValueError('root out of valid note range')
        if scale == None:
            self.scale = self.build_scale()
        else:
            self.scale = scale
        if chords == None:
            self.chords = self.compile_chords()
        else:
            self.chords = chords
    def __repr__(self):
        return f'{self.root} {self.scale_type}\nscale: {self.scale}\nchords: {self.chords}'
    def __str__(self):
        separator = ' '
        pretty_print_scale = self.pretty_print(self.scale)
        pretty_print_modes = []
        pretty_print_chords = []
        for key,value in self.chords.items():
            pretty_print_modes.append(key)
            pretty_print_chords.append(separator.join(self.pretty_print(value)))
        return f'''============================================================ {pretty_print_scale[0]} {self.scale_type} ============================================================
{separator.join(pretty_print_scale)}

[{pretty_print_modes[0]}] {pretty_print_chords[0]}
[{pretty_print_modes[1]}] {pretty_print_chords[1]}
[{pretty_print_modes[2]}] {pretty_print_chords[2]}
[{pretty_print_modes[3]}] {pretty_print_chords[3]}
[{pretty_print_modes[4]}] {pretty_print_chords[4]}
[{pretty_print_modes[5]}] {pretty_print_chords[5]}
[{pretty_print_modes[6]}] {pretty_print_chords[6]}
'''

    def build_scale(self):
        major_scale_steps = ['W','W','H','W','W','W']
        minor_scale_steps = ['W','H','W','W','H','W']
        scale = []
        note_index = 0
        if self.scale_type == 'minor':
            scale_steps = minor_scale_steps
        else:
            scale_steps = major_scale_steps
        scale.append(self.root)

        for key,value in self.valid_notes.items():
            if self.root == value:
                note_index = key

        for step in scale_steps:
            if step == 'W':
                note_index += 2
            if step == 'H':
                note_index += 1
            if note_index > 12:
                note_index -= 12
            scale.append(self.valid_notes[note_index])
        return scale
                
    def build_chord(self,chord_root,mode):
        difference = 0
        notes = []
        for note in self.scale:
            if note == chord_root:
                difference = self.scale.index(note)
        for index in [0,2,4]:
            new_index = index+difference
            if new_index < 7:
                notes.append(self.scale[new_index])
            else:
                notes.append(self.scale[new_index-7])

        return notes
    
    def compile_chords(self):
        chords_list = {}
        if self.scale_type == 'major':
            chord_modes = ['I','ii','iii','IV','V','vi','vii']
        if self.scale_type == 'minor':
            chord_modes = ['i','ii','III','iv','v','VI','VII']
        for chord in chord_modes:
            chord_structure = self.build_chord(self.scale[chord_modes.index(chord)],chord_modes[chord_modes.index(chord)])
            chords_list.update({chord:chord_structure})
        return chords_list

    def pretty_print(self,raw_input):
        if isinstance(raw_input,str):
            prettified = raw_input.replace(' ','')
            prettified = prettified.replace('_','')
            prettified = prettified.title()
            prettified = prettified.replace('flat','♭')
            prettified = prettified.replace('flat','♯')
        if isinstance(raw_input,list):
            prettified = []
            for item in raw_input:
                pretty = item.replace(' ','')
                pretty = pretty.replace('_','')
                pretty = pretty.title()
                pretty = pretty.replace('flat','♭')
                pretty = pretty.replace('flat','♯')
                prettified.append(pretty)
        return prettified


    @property
    def scale_type(self):
        return self._scale_type
    @property
    def root(self):
        return self._root
    @property
    def scale(self):
        return self._scale
    @property
    def chords(self):
        return self._chords
    @property
    def valid_notes(self):
        return self._valid_notes

    @scale_type.setter
    def scale_type(self,scale_type):
        self._scale_type = scale_type
    @root.setter
    def root(self,root):
        self._root = root
    @scale.setter
    def scale(self,scale):
        self._scale = scale
    @chords.setter
    def chords(self,chords):
        self._chords = chords
    @valid_notes.setter
    def valid_notes(self,valid_notes):
        self._valid_notes = valid_notes

def main():
    root = input('root note: ')
    major_minor = input('major/minor?: ')
    scale = Scale(scale_type=major_minor,root=root)
    print(scale)
    print(build_progression(scale))

def build_progression(scale,pretty_print=True,progression=[]):
    end_string = []
    progressions = {
        "minor":[['i','VI','VII'],['i','iv','VII'],['i','iv','v'],['i','VI','III','VII'],['ii','v','i'],['i','iv','v','i'],['VI','VII','i','i'],['i','VII','VI','VII'],['i','iv','i']],
        "major":[['I','IV','V'],['I','vi','IV','V'],['ii','V','I'],['I','vi','ii','V'],['I','V','vi','IV'],['I','IV','vi','V'],['I','iii','IV','V'],['I','IV','I','V'],['I','IV','ii','V']]
    }
    if progression == []:
        progression = progressions[scale.scale_type][r.randint(0,len(progressions[scale.scale_type])-1)]
    else:
        for chord in progression:
            if chord in scale.chords.keys():
                pass
            elif chord.lower() in ['i','ii','iii','iv','v','vi','vii']:
                for key,value in scale.chords.items():
                    if key == chord:
                        scale.build_chord(chord_root=scale.scale[scale.chords.keys().index(key)],mode=chord)
            else:
                raise ValueError('invalid chord: progression takes i-vii|I-VII format')
    chords_list = []
    for chord in progression:
            chord_name = scale.chords[chord][0].upper()
            chord_name = chord_name.replace('FLAT','♭')
            chord_name = chord_name.replace('SHARP','♯')
            chord_name = chord_name.replace('_','')
            chord_name = chord_name.replace(' ','')
            if chord.lower() == chord:
                chord_name = f'{chord_name}m'
            chords_list.append(chord_name)
    if pretty_print:
        separator = ' '
        return f'Your random progression in {scale.pretty_print(scale.root)} {scale.scale_type.title()} is: {separator.join(scale.pretty_print(chords_list))} ({separator.join(progression)})'
    else:
        return chords_list



if __name__ == '__main__':
    main()