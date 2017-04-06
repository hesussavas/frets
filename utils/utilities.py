# notes
notes_sharp = ['A', 'A#', 'B', 'C', 'C#', 'D', 'D#', 'E', 'F', 'F#', 'G', 'G#']
notes_flat = ['A', 'Bb', 'B', 'C', 'Db', 'D', 'Eb', 'E', 'F', 'Gb', 'G', 'Ab']
natural_notes = ['A', 'B', 'C', 'D', 'E', 'F', 'G']
accidental_notes = ['A#', 'Bb', 'C#', 'Dd', 'D#', 'Eb', 'F#', 'Gb', 'G#', 'Ab']
accidental_notes_sharp = ['A#', 'C#', 'D#', 'F#', 'G#']
accidental_notes_flat = ['Bb', 'Db', 'Eb', 'Gb', 'Ab']

steps = ['1', 'b2', '2', 'b3',  '3',  '4',  'b5',  '5',  'b6',  '6',  'b7',  '7',
         '1', 'b9', '9', 'b10', '10', '11', 'b12', '12', 'b13', '13', 'b14', '14', 'b15', '15']
steps_sharp = ['1', '#1', '2', '#2', '3',  '4',  '#4',  '5',  '#5',  '6',  '#6',  '7',
               '1', '#8', '9', '#9', '10', '11', '#11', '12', '#12', '13', '#13', '14', '#14', '15']
steps_octave = ['1', 'b2', '2', 'b3',  '3',  '4',  'b5',  '5',  'b6',  '6',  'b7',  '7',
                '8', 'b9', '9', 'b10', '10', '11', 'b12', '12', 'b13', '13', 'b14', '14', 'b15', '15']

steps_all = ['1', '#1', '2', '#2',  '3',  '4',  '#4',  '5',  '#5',  '6',  '#6',  '7',
             '8', '#8', '9', '#9',  '10', '11', '#11', '12', '#12', '13', '#13', '14',
             '1', 'b2', '2', 'b3',  '3',  '4',  'b5',  '5',  'b6',  '6',  'b7',  '7',
             '8', 'b9', '9', 'b10', '10', '11', 'b12', '12', 'b13', '13', 'b14', '14']

steps_interval = ['uni', 'min2', 'maj2', 'min3', 'maj3', 'per4', 'aug4', 'per5', 'min6', 'maj6', 'min7', 'maj7', 'oct']

steps_natural = ['1', '2', '3', '4', '5', '6', '7', '9', '10', '11', '12', '13', '14', '15']
steps_accidental = ['b2', 'b3', 'b5', 'b6', 'b7', 'b9', 'b10', 'b12', 'b13', 'b14', 'b15']

steps_1octave = ['1', 'b2', '2', 'b3', '3', '4', 'b5', '5', 'b6', '6', 'b7', '7', '8']
steps_2octave = ['8', 'b9', '9', 'b10', '10', '11', 'b12', '12', 'b13', '13', 'b14', '14', 'b15']
steps_natural_1octave = ['1', '2', '3', '4', '5', '6', '7', '8']
steps_natural_2octave = ['8', '9', '10', '11', '12', '13', '14']
steps_accidental_1octave = ['b2', 'b3', 'b5', 'b6', 'b7']
steps_accidental_2octave = ['b9', 'b10', 'b12', 'b13', 'b14', 'b15']

notes_dots = ['     ', '       ', '     ', '  O  ', '     ', '  O  ', '     ', '  O  ', '     ', '  O  ', '     ',
              '     ', ' OO  ']

# semitones offset depending on string
semitones_offsets = [7,0,5,10,2,7]

# define cost threshold
cost_threshold = 10000

# string names
string_names = ['E', 'A', 'D', 'G', 'B', 'e']

# needed columns in dataframe in order
data_columns = ['Chord Name', 'Alt Chord Name', 'Fundamental', 'Chord Type',
                'Ft-E', 'Ft-A', 'Ft-D', 'Ft-G', 'Ft-B', 'Ft-e',
                'Fg-E', 'Fg-A', 'Fg-D', 'Fg-G', 'Fg-B', 'Fg-e',
                'Fi-E', 'Fi-A', 'Fi-D', 'Fi-G', 'Fi-B', 'Fi-e',
                'Fn-E', 'Fn-A', 'Fn-D', 'Fn-G', 'Fn-B', 'Fn-e',
                'Fret Positions', 'Finger Positions', 'Notes',
                'Sorted Intervals', 'Grouping', 'Overall Cost',
                'Rule Costs', 'Worst Rule', 'Strummable']

# needed columns in dataframe in order
data_pred_columns = ['Chord Name', 'Alt Chord Name', 'Fundamental', 'Chord Type',
                    'Ft-E', 'Ft-A', 'Ft-D', 'Ft-G', 'Ft-B', 'Ft-e',
                    'Fg-E', 'Fg-A', 'Fg-D', 'Fg-G', 'Fg-B', 'Fg-e',
                    'Fp-E', 'Fp-A', 'Fp-D', 'Fp-G', 'Fp-B', 'Fp-e',
                    'Fi-E', 'Fi-A', 'Fi-D', 'Fi-G', 'Fi-B', 'Fi-e',
                    'Fn-E', 'Fn-A', 'Fn-D', 'Fn-G', 'Fn-B', 'Fn-e',
                    'Fret Positions', 'Finger Positions', 'Pred Finger Positions', 'Notes',
                    'Sorted Intervals', 'Grouping', 'Fret Model Cost', 'Muted Model Cost', 'Overall Cost', 'Pred Cost', 'Diff Cost', 'Diff Score',
                    'Original row id', 'Worst R', 'Worst R Score',
                    'Worst pR', 'Worst pR Score',
                    'R1', 'R1bis', 'R2', 'R2bis', 'R2ter', 'R3',
                    'R4', 'R4bis', 'R5', 'R6', 'R6bis', 'R7', 'R8',
                    'R9', 'R10', 'R11', 'R13', 'R14', 'R15',
                    'R16', 'R17', 'R18', 'R19', 'R20', 'R21', 'R22',
                    'R23', 'R24', 'R26', 'R27', 'R28', 'R29', 'R30', 'R31',
                    'pR1', 'pR1bis', 'pR2', 'pR2bis', 'pR2ter', 'pR3',
                    'pR4', 'pR4bis', 'pR5', 'pR6', 'pR6bis', 'pR7', 'pR8',
                    'pR9', 'pR10', 'pR11', 'pR13', 'pR14', 'pR15',
                    'pR16', 'pR17', 'pR18', 'pR19', 'pR20', 'pR21', 'pR22',
                    'pR23', 'pR24', 'pR26', 'pR27', 'pR28', 'pR29', 'pR30', 'pR31']

# finger numbers
fingers = ['1', '2', '3', '4']
all_fingers = ['1', '2', '3', '4', '5']

# Maximum span between finger 1 and finger 4 depending on the position on the guitar
finger_span = {0:5, 1:5, 2:5, 3:5, 4:5,
               5:6, 6:6, 7:6, 8:6, 9:6, 10:6, 11:6, 12:6, 13:6, 14:6, 15:6,
               16:7, 17:7, 18:7, 19:7, 20:7, 21:7, 22:7, 23:7, 24:7}

finger_span_cost = [0, 150, 260, 500, 1000, 2050, 4280, 9000]

# column names of ugly csv database format ("Difficult_Chords.csv")
ugly_columns = ['Fundamental', 'Chord Type', 'Chord Name',
                'LSB', 'Ft-E', 'Ft-A', 'Ft-D', 'Ft-G', 'Ft-B', 'Ft-e', 'LSR',
                'LSB', 'Fg-E', 'Fg-A', 'Fg-D', 'Fg-G', 'Fg-B', 'Fg-e', 'LSR',
                'Finger Positions', 'Smallest Moveable Shape', 'Comments']

original_keywords = ['original', 'originally']

ordered_useless_intervals = ['1','8',
                             '5','12','#5','#12','b5','b12',
                             '6','13','#6','#13','b6','b13',
                             '2','9','#2','#9','b2','b9',
                             '4','11','#4','#11',
                             '7','14','b7','b14',
                             '3','10','b3','b10']

# Changing this list order changes the rule computation order
rule_names = ['R1',
              'R1bis',
              'R2',
              'R2bis',
              'R2ter',
              'R3',
              'R4',
              'R4bis',
              'R5',
              'R6',
              'R6bis',
              'R7',
              'R8',
              'R9',
              'R10',
              'R11',
              #'R12',
              'R13',
              'R14',
              'R15',
              'R16',
              'R17',
              'R18',
              'R19',
              'R20',
              'R21',
              'R22',
              'R23',
              'R24',
              #'R25',
              'R26',
              'R27',
              'R28',
              'R29',
              'R30',
              'R31']

rule_descriptions = {'R1': 'An open string cannot be surrounded with the same finger.',
                     'R1bis': 'A barre is rarely surrounded by open strings (especially not under it).',
                     'R2': 'Fingers identified with small numbers tend to be used on smaller fret numbers than the other fingers and those with high numbers on higher fret numbers.',
                     'R2bis': 'Fingers with small numbers tend to be used on low-pitched strings and thoses with high numbers tend to be used on higher-pitched strings.',
                     'R2ter': 'Little penalty for two fingers on the same fret number and much higher penalty when one is doing a barre and penalty increased even more if fingers are not close one to another on the hand.',
                     'R3': 'The span between Finger 1 and Finger 4 must be 5 or less when on the first 4 frets, 6 or less when on 5-15 frets, and 7 or less when on 16-24 frets.',
                     'R4': 'Finger 1 is often used for barre chords, so can cover anywhere between 1-6 strings on the same fret. While other fingers can also bar several strings, they tend to cover only 2 or 3 strings. Fingers 1 & 2, tend to be the most strong and dominant, with 4 being the weakest and least dominant, hence there tends to be little bar function for fingers 3 & 4.',
                     'R4bis': 'Barre rule for 3-6 strings. Slight penalty for having a barre chord going over 3-6 strings. Higher cost for each higher finger number.',
                     'R5': 'One finger cannot barre different fret numbers.',
                     'R6': 'A barre chord is impossible if other smaller fret numbers are being played on strings inside barre',
                     'R6bis': 'A barre chord is impossible if other smaller fret numbers are being played on strings under barre',
                     'R7': 'Fingers tend to be in their natural position from first fret, that is 1 per fret interval.',
                     'R8': 'If you have 3-4 different frets being used, it\'s good to use one finger per fret',
                     'R9': 'Finger 2 and 3 cannot make barre if other fingers are more than 2 strings physically above it.',
                     'R10': 'Fingers 1 and 2 hardly make simultaneous barre.',
                     'R11': 'It is hard for finger 3 and 4 to cover more than a 4-strings gap.',
                     #'R12': 'Chord is harder to play if muted strings are surrounded by played ones.',
                     'R13': 'The span between 2 consecutive fingers must be 3 or less when on the first 4 frets, 4 or less when on 5-15 frets, and 5 or less when on 16-24 frets.',
                     'R14': 'It\'s very hard or impossible to hold down more than 3 strings with finger 3 and also have finger 4 under it.',
                     'R15': 'Pinky on high frets rule. If you are barring all strings with the first finger, and you are using the fourth finger, it becomes increasigly difficult to reach the higher string numbers (5=A, 6=E) as you go up the frets around fret 10 with the pinky finger.',
                     'R16': '4th finger cannot be higher in strings than 2nd or 3rd fingers when 1st finger is far behind 2nd and 3rd.',
                     'R17': 'Limited finger rule: You can only have fingers 1-5.',
                     'R18': 'Thumb can cover only string 6, 5 and 4, with barre only.',
                     'R19': 'Finger sequence rule b): if f5 is in use then: f5<=f4  and f5 can\'t be less than 2 frets less than f1 For each fret that f5 is higher up in frets from f1, add a penalty, and a high penalty if fret on f5= fret on f4.',
                     'R20': 'Finger gap (horizontal) difficulty rule when consecutive fingers are one string appart (vertical). For the same gap between any two consecutive fingers eg f1 and f2, f2 and f3, f3 and f4, there are different costs because the flexibility between fingers is different.',
                     'R21': 'Three finger crowding rule for low and high fret numbers: If you have three consecutive fingers on the same fret, next to each other on 3 adjacent strings',
                     'R22': 'The rule is about using as few unique fingers as possible. For example if you can play a chord with 3 fingers, instead of 4, then you should, even if it includes barres. A little penalty is added for each finger that is used, very slightly increasing as the finger number gets higher, including the thumb.',
                     'R23': 'Occam\'s Razor: The fewer fingers you can use, the better',
                     'R24': 'Null finger on Fretboard Rule: If a fret on a string is larger than zero, then the finger cannot be zero, and the reverse (as well as muted string or else).',
                     #'R25': 'Shape Complexity Rule: When moving from string to string (eg string 6 to string 1), count the direction changes (similar to zig zags) and add them to the cost with a factor.',
                     'R26': 'Finger 3 is the better middle finger. If you are using finger 1 and finger 4, and the fret inbetween f1 and f4 is halfway or more towards f4, then use f3, otherwise use f2.',
                     'R27': 'A finger of higher number cannot be over a barre of another finger on the same fret number',
                     'R28': 'Using different fingers under and over a \'x\' is better than a barre (strumming vs plucking)',
                     'R29': 'Check if thumb should be used when strings A and D are x or 0 and E is used',
                     'R30': 'Add big penalty when using thumb while a finger is on the string just under it',
                     'R31': 'High pitched pivot finger one rule: If finger 1 is on a high sounding string, f2 is not in use and 3 and 4 are on lower sounding strings, add a penalty'}

greene_table = {
    'V-1': ['BTAS', 'SBTA', 'ASBT', 'TASB'],
    'V-2': ['TABS', 'STAB', 'BSTA', 'ABST'],
    'V-3': ['ABTS', 'SABT', 'TSAB', 'BTSA'],
    'V-4': ['STBA', 'ASTB', 'BAST', 'TBAS'],
    'V-5': ['BATS', 'SBAT', 'TSBA', 'ATSB'],
    'V-6': ['B-TAS', 'SB-TA', 'ASB-T', 'TASB-'],  # (V-1 with B an octave lower)
    'V-7': ['TAB-S', 'STAB-', 'B-STA', 'AB-ST'],  # (V-2 with B an octave lower)
    'V-8': ['TBSA', 'ATBS', 'SATB', 'BSAT'],
    'V-9': ['TABS+', 'S+TAB', 'BS+TA', 'ABS+T'],  # (V-2 with S an octave higher)
    'V-10': ['T-AB-S', 'ST-AB-', 'B-ST-A', 'AB-ST-', 'TA+BS+', 'S+TA+B', 'BS+TA+', 'A+BS+T'],
    # (V-2 with both B and T an octave lower, or A and S an octave higher)
    'V-11': ['S+TBA', 'AS+TB', 'BAS+T', 'TBAS+'],  # (V-4 with S an octave higher)
    'V-12': ['AB-TS', 'SAB-T', 'TSAB-', 'B-TSA'],  # (V-3 with B an octave lower)
    'V-13': ['B-T-AS', 'SB-T-A', 'ASB-T-', 'T-ASB-', 'BTA+S+', 'S+BTA+', 'A+S+BT', 'TA+S+B'],
    # (V-1 with both B and T an octave lower, or A and S an octave higher)
    'V-14': ['BTAS+', 'S+BTA', 'AS+BT', 'TAS+B']  # (V-1 with S an octave higher)
}