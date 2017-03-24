import csv
from collections import deque


def get_column_with_key(filename, key):
    columnData = list()
    with open(filename, 'r', newline='') as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            columnData.append(row[key])
    return columnData


def write_new_column(outputfile, data):
    with open(outputfile, 'wb') as csvoutput:
        writer = csv.writer(csvoutput)
        writer.writerow(data)


def distanceBetween(noteA, noteB):
    counter = 0
    notes = ['C', 'C#', 'D', 'D#', 'E', 'F', 'F#', 'G', 'G#', 'A', 'A#', 'B']
    indexA = notes.index(noteA)
    indexB = notes.index(noteB)
    if indexA < indexB:
        return indexB - indexA
    else:
        return indexB - indexA + len(notes)


class Identify:
    def __init__(self):
        # eb g b f#
        # b d# g e
        # 3 7  11
        # c d f# a
        MAJOR = 'major'
        MINOR = 'm'
        AUG = '+'
        DIM = 'dim'
        FLAT = 'b'
        SHARP = '#'
        S2 = 'sus2'
        S4 = 'sus4'

        self.notes = ['C', 'C#', 'D', 'D#', 'E', 'F', 'F#', 'G', 'G#', 'A',
                      'A#', 'B']
        self.tuning = ['E', 'A', 'D', 'G', 'B', 'E']

        self.fith_interval_profile = [(set([5]), 0, '5')]
        self.flat_fith_omit3_profile = [(set([6]), 0, '(b5, omit 3)')]
        self.two_note_profiles = [self.fith_interval_profile,
                                  self.flat_fith_omit3_profile]
        self.major_profile = (set([4, 7]), 0, MAJOR)
        self.major_profile_inverted = (set([5, 9]), 5, MAJOR)
        self.major_profile_inverted_second = (set([3, 8]), -4, MAJOR)

        self.minor_profile = (set([3, 7]), 0, MINOR)
        self.minor_profile_inverted = (set([4, 9]), -3, MINOR)
        self.minor_profile_inverted_second = (set([5, 8]), 5, MINOR)

        self.aug_profile = (set([4, 8]), 0, AUG)
        self.aug_profile_inverted = (set([4, 8]), -4, AUG)
        self.aug_profile_inverted_second = (set([4, 8]), -8, AUG)

        self.maj7_sus4_profile = [(set([5, 1]), 0, 'maj7sus4(omit 5)'),
                                  (set([6, 7]), -5, 'maj7sus4(omit 5)'),
                                  (set([1, 6]), 1, 'maj7sus4(omit 5)')]
        self.dim_profiles = [(set([3, 6]), 0, DIM), (set([3, 9]), -3, DIM),
                             (set([9, 6]), -6, DIM)]

        self.sus_two_profile = [(set([2, 7]), 0, S2), (set([5, 10]), -2, S2),
                                (set([5, 7]), 5, S2)]
        self.sus_two_flat_five_profile = [(set([2, 6]), 0, S2 + '(b5)')]

        self.sus_four_profile = [(set([5, 7]), 0, S4), (set([2, 7]), -5, S4),
                                 (set([5, 10]), 5, S4)]

        self.aug_sus_4_profiles = [(set([5, 8]), 0, AUG + S4),
                                   (set([3, 7]), -5, AUG + S4),
                                   (set([4, 9]), 4, AUG + S4)]

        self.sixth_omit_5_profiles = [(set([4, 9]), 0, '6(omit 5)'),
                                      (set([5, 8]), 8, '6(omit 5)'),
                                      (set([3, 7]), 3, '+sus4')]

        self.seventh_omit_5_profiles = [(set([4, 10]), 0, '7(omit 5)'),
                                        (set([6, 8]), -4, '7(omit 5)'),
                                        (set([2, 6]), 2, '7(omit 5)')]

        self.seventh_sus4_omit_5_profiles = [
            (set([5, 10]), 0, '7sus4(omit 5)')]

        self.aug_flat_fifth_omit_3 = [(set([6, 8]), 0, '+(5b, omit 3)')]
        self.five_sharp_elev_omit_3_profile = [
            (set([6, 7]), 0, '5(#11, omit 3)'),
            (set([5, 11]), -7, '5(#11, omit 3)'),
            (set([1, 6]), -6, '5(#11, omit 3)')]

        self.minor_sixth_omit_fith_profiles = [(set([3, 9]), 0, 'm6(omit 5)'),
                                               (set([6, 9]), -3, 'm6(omit 5)'),
                                               (set([3, 6]), 3, 'm6(omit 5)')]

        self.minor_sharp_fith_profiles = [(set([3, 8]), 0, 'm(#5)'),
                                          (set([5, 9]), -3, 'm(#5)'),
                                          (set([4, 7]), 4, 'm(#5)')]

        self.sixth_flat_fith_omit_third_profiles = [
            (set([6, 9]), 0, '6(b5,omit 3)'), (set([3, 6]), 6, '6(b5,omit 3)'),
            (set([3, 9]), 3, 'm6(omit 5)')]

        self.major_profiles = [self.major_profile, self.major_profile_inverted,
                               self.major_profile_inverted_second]
        self.minor_profiles = [self.minor_profile, self.minor_profile_inverted,
                               self.minor_profile_inverted_second]
        self.aug_profiles = [self.aug_profile]
        self.profiles_to_check_with_out_bass = [self.major_profiles,
                                                self.minor_profiles,
                                                self.dim_profiles,
                                                self.aug_profiles,
                                                self.aug_sus_4_profiles,
                                                self.sus_two_flat_five_profile]
        self.major_seventh_profiles = [(set([4, 7, 10]), 0, '7'),
                                       (set([3, 6, 8]), -4, '7'),
                                       (set([3, 5, 9]), -7, '7'),
                                       (set([2, 6, 9]), 2, '7')]

        self.ma7_sharp_fith_profile = [(set([4, 8, 11]), 0, 'maj7(#5)'),
                                       (set([4, 7, 8]), -4, 'maj7(#5)'),
                                       (set([3, 4, 8]), 4, 'maj7(#5)'),
                                       (set([1, 5, 9]), 1, 'maj7(#5)')]

        self.sev_sharp_fith_profile = [(set([4, 8, 10]), 0, '7(#5)'),
                                       (set([6, 4, 8]), -4, '7(#5)'),
                                       (set([2, 4, 8]), -8, '7(#5)')]

        self.major_seventh_sus4_profiles = [(set([5, 7, 10]), 0, '7sus4'),
                                            (set([2, 5, 7]), -5, '7sus4'),
                                            (set([3, 5, 10]), 5, '7sus4'),
                                            (set([2, 7, 8]), 2, '7sus4')]

        self.major_seventh_sharp_fith_profiles = [
            (set([5, 7, 10]), 0, '7sus4'), (set([2, 5, 7]), -5, '7sus4'),
            (set([3, 5, 10]), 5, '7sus4'), (set([2, 7, 8]), 2, '7sus4')]

        self.aug_add_nine_profiles = [(set([4, 8, 2]), 0, '+add9'),
                                      (set([4, 10, 8]), -4, '+add9'),
                                      (set([6, 4, 8]), 4, 'add9'),
                                      (set([10, 2, 6]), -2, 'add9')]

        self.aug_sharp_nine_profiles = [(set([4, 8, 3]), 0, '+(#9)')]
        self.minor_sixth_add_eleven_omit_five = [
            (set([3, 9, 5]), 0, 'm6add11(omit 5)'),
            (set([6, 9, 2]), -3, 'm6add11(omit 5)'),
            (set([8, 3, 6]), -9, 'm6add11(omit 5)')]
        self.major_sixth_flat_fith_profile = [(set([4, 6, 9]), 0, '6(b5)')]
        self.major_sixth_sharp_fith_profile = [(set([4, 8, 9]), 0, '6(#5)'),
                                               (set([4, 5, 8]), -4, '6(#5)'),
                                               (set([1, 4, 8]), -8, '6(#5)')]

        # 4 8 2 check
        self.major_aug_seventh_profile = [(set([4, 8, 10]), 0, '+7'),
                                          (set([4, 6, 8]), -4, '+7'),
                                          (set([2, 4, 8]), -8, '+7'),
                                          (set([2, 6, 10]), 2, '+7')]

        self.minor_seventh_profile = [(set([3, 7, 10]), 0, 'm7'),
                                      (set([4, 7, 9]), -3, 'm7'),
                                      (set([3, 5, 8]), 5, 'm7'),
                                      (set([2, 5, 9]), 2, 'm7')]

        self.minor_major_seventh_profile = [(set([3, 7, 11]), 0, 'm(maj7)')]

        self.dim_seventh_profile = [(set([3, 6, 9]), 0, 'dim7'),
                                    (set([3, 6, 9]), -3, 'dim7'),
                                    (set([3, 6, 9]), -6, 'dim7')]
        self.dim_sharp_fifth = [(set([3, 6, 8]), 0, 'dim(#5)'),
                                (set([3, 5, 9]), -3, 'dim(#5)'),
                                (set([2, 6, 9]), -6, 'dim(#5)')]
        self.seventh_flat_five_profile = [(set([4, 6, 10]), 0, '7(b5)'),
                                          (set([2, 6, 8]), -4, '7(b5)'),
                                          (set([4, 6, 10]), -6, '7(b5)')]

        self.minor_seventh_flat_fith_profile = [(set([3, 6, 10]), 0, 'm7b5'),
                                                (set([3, 7, 9]), -3, 'm7b5'),
                                                (set([4, 6, 9]), -6, 'm7b5'),
                                                (set([2, 5, 8]), -10, 'm7b5')]

        self.major_sixth_profile = [(set([4, 7, 9]), 0, '6'),
                                    (set([2, 5, 9]), 5, '6'),
                                    (set([3, 5, 8]), -4, '6')]

        self.major_sixth_sus_two_profile = [(set([2, 7, 10]), 0, '6sus2'),
                                            (set([5, 7, 10]), -2, '6sus2'),
                                            (set([2, 5, 7]), -7, '6sus2'),
                                            (set([3, 5, 10]), 3, '6sus2')]
        # self.auth_sixth_sus_two_profiles = [(set([2,8,10]),0,'+sus2')]
        self.aug_sus_two_flat_five = [(set([2, 6, 8]), 0, '+sus2(b5)')]
        self.major_sixth_sus_two_flat_fith_profile = [
            (set([2, 6, 9]), 0, '6sus2(b5)'),
            (set([4, 7, 10]), -2, '6sus2(b5)'),
            (set([3, 6, 8]), -6, '6sus2(b5)')]
        self.aug_add_elev_profiles = [(set([4, 5, 8]), 0, '+add11'),
                                      (set([4, 1, 8]), -4, '+add11'),
                                      (set([9, 4, 8]), -8, '+add11'),
                                      (set([3, 7, 11]), -5, '+add11')]
        self.three_note_profiles = [self.major_profiles, self.minor_profiles,
                                    self.aug_profiles, self.dim_profiles,
                                    self.sus_two_profile,
                                    self.sus_four_profile,
                                    self.aug_sus_4_profiles,
                                    self.sixth_omit_5_profiles,
                                    self.seventh_sus4_omit_5_profiles,
                                    self.minor_sixth_omit_fith_profiles,
                                    self.sixth_flat_fith_omit_third_profiles,
                                    self.minor_sharp_fith_profiles,
                                    self.maj7_sus4_profile,
                                    self.seventh_omit_5_profiles,
                                    self.sus_two_flat_five_profile,
                                    self.aug_flat_fifth_omit_3,
                                    self.major_sixth_sharp_fith_profile,
                                    self.five_sharp_elev_omit_3_profile]
        self.four_note_profiles = [self.major_seventh_profiles,
                                   self.major_aug_seventh_profile,
                                   self.minor_seventh_profile,
                                   self.major_sixth_profile,
                                   self.minor_seventh_flat_fith_profile,
                                   self.major_sixth_flat_fith_profile,
                                   self.major_sixth_sus_two_flat_fith_profile,
                                   self.aug_add_nine_profiles,
                                   self.major_seventh_sus4_profiles,
                                   self.major_sixth_sus_two_profile,
                                   self.dim_seventh_profile,
                                   self.ma7_sharp_fith_profile,
                                   self.minor_major_seventh_profile,
                                   self.aug_sharp_nine_profiles,
                                   self.aug_add_elev_profiles,
                                   self.major_sixth_sharp_fith_profile,
                                   self.seventh_flat_five_profile,
                                   self.aug_sus_two_flat_five,
                                   self.dim_sharp_fifth,
                                   self.minor_sixth_add_eleven_omit_five,
                                   self.sev_sharp_fith_profile]

    def identify_chord(self, distances, cleaned_notes):
        profiles = list()
        if len(cleaned_notes) <= 3:
            profiles = self.three_note_profiles
            chord_list = self.check_profiles(distances, profiles)
            return chord_list
        else:
            profiles = self.four_note_profiles
            chord_list = self.check_profiles(distances, profiles)
            return chord_list

    def identify_chord_triad(self, distances, cleaned_notes):
        profiles = self.profiles_to_check_with_out_bass
        chord_list = list()
        for i in range(0,len(profiles)):
            shift = self.label_chord_with_no_inverstion(distances,profiles[i])
            if shift != -1:
                note = self.get_root_note(distances[-1],shift)
                chord = note + profiles[i][0][2]
                if chord not in chord_list:
                    chord_list.append(chord)
        return chord_list

    def identify_chord_interval(self, distances, cleaned_notes):
        profiles = self.two_note_profiles
        chord_list = list()
        for i in range(0,len(profiles)):
            shift = self.label_chord_with_no_inverstion(distances,profiles[i])
            if shift != -1:
                note = self.get_root_note(distances[-1],shift)
                chord = note + profiles[i][0][2]
                if chord not in chord_list:
                    chord_list.append(chord)
        return chord_list

    def label_chord_with_no_inverstion(self, distances, profiles):
        distance = set(distances[0])
        if profiles[0][0].issubset(distance):
            return profiles[0][1]
        return -1

    def check_profiles(self, distances, profiles):
        chord_list = list()
        for i in range(0, len(profiles)):
            for j in range(0, len(profiles[i])):
                shift = self.label_chord(distances, profiles[i])
                if shift != -1:
                    note = self.get_root_note(distances[-1], shift)
                    chord = note + profiles[i][0][2]
                    if chord not in chord_list:
                        chord_list.append(chord)
        return chord_list

    def get_notes(self, frets):
        return self.noteForStrings(frets.split("-"))

    def noteForStrings(self, fret_data):
        played_notes = list()
        for string_number in range(0, len(fret_data)):
            fret = fret_data[string_number]
            if fret != 'x':
                open_note_index = self.notes.index(self.tuning[string_number])
                note_index = open_note_index + int(fret)
                if note_index < len(self.notes):
                    played_notes.append(self.notes[note_index])
                else:
                    played_notes.append(
                        self.notes[note_index - len(self.notes)])
        return played_notes

    def get_root_note(self, note, shift):
        note_index = self.notes.index(note) + shift
        while note_index >= len(self.notes):
            note_index = note_index - len(self.notes)
        note = self.notes[note_index]
        return note

    def label_chord(self, distances, profiles):
        distance = set(distances[0])
        for profile in profiles:
            if profile[0].issubset(distance):
                return profile[1]
        return -1


class Chord:
    def __init__(self, notes):
        self.notes = notes
        self.all_notes = ['C', 'C#', 'D', 'D#', 'E', 'F', 'F#', 'G', 'G#', 'A',
                          'A#', 'B']
        self.major = False
        self.minor = False
        self.chord_name = ''
        self.chord_list = list()
        self.chord_low_note = notes[0]
        self.cleaned_notes = deque(self.remove_duplicates(notes))
        self.distances = self.get_chord_distances(self.cleaned_notes)
        self.notes_withoutbase = deque(self.remove_duplicates(notes[1:]))
        self.distances_withoutbase = self.get_chord_distances(
            self.notes_withoutbase)

    def add_bass_to_list(self):
        chord_list_with_bass = list()
        for chord in self.chord_list:
            if chord[1] == '#':
                note = chord[0:2]
            else:
                note = chord[0]
            if note != self.chord_low_note:
                chord = chord + '/' + self.chord_low_note
            chord_list_with_bass.append(chord)
        return chord_list_with_bass

    def get_chord_distances(self, cleaned_notes):
        distances_matrix = list()
        note_row = cleaned_notes
        for j in range(0, len(note_row)):
            distances = list()
            if j != 0:
                note_row.rotate(1)
            for i in range(0, len(note_row)):
                distance = self.get_distance_from_note(note_row[0],
                                                       note_row[i])
                if distance >= len(self.all_notes):
                    distance = distance - len(self.all_notes)
                distances.append(distance)
            distances_matrix.append((distances, note_row[0]))
        return distances_matrix

    def get_distance_from_note(self, noteA, noteB):
        if noteA == noteB:
            return 0
        root_index = self.all_notes.index(noteA)
        other_index = self.all_notes.index(noteB)
        if root_index < other_index:
            return other_index - root_index
        else:
            return other_index - root_index + len(self.all_notes)

    def remove_duplicates(self, values):
        output = []
        seen = set()
        for value in values:
            if value not in seen:
                output.append(value)
                seen.add(value)
        return output


class Controller:
    def __init__(self):
        self.identifier = Identify()
        self.filename = "test2.csv"
        self.outFile = "output.csv"
        self.key = "Fret Positions"
        self.fret_positions = get_column_with_key(filename=self.filename,
                                                  key=self.key)

    def writeFile(self, data):
        with open('test.csv', 'w') as fp:
            a = csv.writer(fp, delimiter=',')
            a.writerow(['Fret Positions', 'notes', 'chords', 'lowest note'])
            for i in data:
                a.writerow(i)

    def identify(self, index):
        notes = self.identifier.get_notes(self.fret_positions[index])
        chord = Chord(notes)
        chord_list = list()
        for distance in chord.distances:
            chord_list = chord_list + self.identifier.identify_chord(distance,
                                                                     chord.cleaned_notes)
        chord.chord_list = chord.remove_duplicates(chord_list)
        chord.chord_list = chord.add_bass_to_list()
        if len(chord.cleaned_notes) == 4 and chord.chord_low_note not in chord.notes_withoutbase:
            for distance in chord.distances_withoutbase:
                chord.chord_list = chord.chord_list + self.identifier.identify_chord_triad(distance, chord.notes_withoutbase)
        elif len(chord.cleaned_notes) == 3 and chord.chord_low_note not in chord.notes_withoutbase:
            chord.chord_list = chord.chord_list + self.identifier.identify_chord_interval(chord.distances_withoutbase[1], chord.notes_withoutbase)
        return (self.fret_positions[index], chord.notes, chord.cleaned_notes,
                chord.chord_list)


controller = Controller()
data_to_write = list()
length = len(controller.fret_positions)
for i in range(0, length):
    controller.identify(i)
    result = controller.identify(i)
    lowest_note = result[1][0]
    notes = result[2]
    chord_list = result[3]
    cleaned_output_string = ' '.join(
        str(chord) for chord in controller.identify(i)[3])
    notes_string = ' '.join(str(note) for note in notes)
    data_to_write.append(
        [controller.fret_positions[i], notes_string, cleaned_output_string,
         lowest_note])
    print(data_to_write[i])
controller.writeFile(data_to_write)
