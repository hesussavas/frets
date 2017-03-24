# ===========================
# Modules
# ===========================
import itertools
import copy
import numpy as np
from operator import itemgetter
##### Home-made modules #####
from utils.model_functions import fret_model_func, muted_model_func
from utils import utilities


# ===========================
# Functions
# ===========================
def predict_fingering(fret_positions, strummable=True):
    """
    Predict the fingering of a chord given its fret positions.

    Parameters
    ----------
    fret_positions : list
        List of the fret positions on the strings.

    Returns
    -------
    best_fingering : list
        List of the finger positions matching best the chord.
    best_cost : int
        Cost of the best fingering for the chord.
    """

    ### get fret numbers where to put fingers
    fingered_frets = [i for i, f in enumerate(fret_positions) if
                      f.lower() != 'x' and f != '0']

    ### generate all possible fingerings (without taking into account human playability)
    possible_fingerings = itertools.product(utilities.fingers,
                                            repeat=len(fingered_frets))

    ### compute cost of each fingering and keep the best
    best_cost = np.inf
    best_fingering = None
    for fgr in possible_fingerings:
        fgr = list(fgr)
        fgr = [fgr.pop(0) if i in fingered_frets else f for i, f in
               enumerate(fret_positions)]
        current_cost = compute_cost(fgr, fret_positions, best_cost=best_cost,
                                    strummable=strummable)
        if current_cost < best_cost:
            best_fingering = fgr
            best_cost = current_cost

    ### if the best fingering is still bad, take thumb into account
    if best_cost > utilities.cost_threshold:
        possible_fingerings = itertools.product(utilities.all_fingers, repeat=len(fingered_frets))
        for fgr in possible_fingerings:
            fgr = list(fgr)
            fgr = [fgr.pop(0) if i in fingered_frets else f for i,f in enumerate(fret_positions)]
            if fgr[0] == '5' and '5' not in fgr[2:]: # only check for the 2 lowest-pitched strings
                current_cost = compute_cost(fgr, fret_positions, best_cost=best_cost)
                if current_cost < best_cost:
                    best_fingering = fgr
                    best_cost = current_cost

    return best_fingering, best_cost



def compute_cost(finger_positions, fret_positions, return_rules_importance=False, best_cost=np.inf, strummable=True):
    """
    Compute the cost of a given fingering.
    The lower the cost is, the better the fingering is.

    Parameters
    ----------
    finger_positions : list
        List of the finger positions.
    fret_positions : list
        List of the fret positions.
    return_rules_importance : bool
        Return rules importance if True.

    Returns
    -------
    cost : int
        Cost of the finger positions according to the fret positions.
  ( dict_rules : dictionary
        Dictionary with rules as keys and costs as values. )
    """

    ### Store finger positions in a dictionary
    # with finger numbers as keys and order number as values
    # pos 0 is string E, 1 is A, 2 is D, 3 is G, 4 is B and 5 is e
    # max(pos_dict[fg]) is high-pitched
    # min(pos_dict[fg]) is low-pitched
    pos_dict = {}
    for i,fg in enumerate(finger_positions):
        pos_dict.setdefault(fg,[]).append(i)
    # store finger unique numbers (without open strings)
    fingers_used = set([int(fg) for fg in finger_positions if fg!='0' and fg.lower()!='x'])
    # store fret unique numbers (without open strings)
    frets_used = set([int(ft) for i,ft in enumerate(fret_positions) if ft!='0' and ft.lower()!='x' and finger_positions[i] != '5'])

    ### Initialize cost to be increased when rules are not well-followed
    cost = 0

    ### Initialize rules_dict with zeros
    if return_rules_importance:
        rules_dict = dict([ (R,0) for R in utilities.rule_names ])


    ################################## Rules ##################################
    for R in utilities.rule_names:

        # break loop as soon as cost is too large
        if cost > best_cost:
            break

        if R == 'R1':
            ### R1: An open string cannot be surrounded with the same finger
            # and a barre is rarely surrounded by open strings (especially not under it: R1bis)
            Rc1 = 100000
            Rc2 = 10000
            if '0' in pos_dict:
                for pos_0 in pos_dict['0']:
                    for fg in utilities.fingers:
                        if fg in pos_dict and len(pos_dict[fg]) > 1:
                            if pos_0 < max(pos_dict[fg]) and pos_0 > min(pos_dict[fg]):
                                cost += Rc1
                                if return_rules_importance: rules_dict['R1'] += Rc1
                            if pos_0 > max(pos_dict[fg]):
                                cost += Rc2
                                if return_rules_importance: rules_dict['R1bis'] += Rc2

        elif R == 'R2':
            ### R2: Fingers identified with small numbers tend to be used on smaller fret
            # numbers than the other fingers and those with high numbers on higher fret numbers.
            ### R2bis: Fingers with small numbers tend to be used on low-pitched strings
            # and those with high numbers tend to be used on high-pitched strings.
            ### R2ter: little penalty for two fingers on the same fret number
            # and much higher penalty when one is doing a barre and penalty increased
            # even more if fingers are not close one to another on the hand.
            Rc1 = 100
            Rc2 = 200000
            Rc4 = 80
            for fg1,pos1 in pos_dict.items():
                if fg1 != 'x' and fg1 != '0' and fg1 != '5':
                    for p1 in pos1:
                        for fg2 in utilities.fingers:
                            if fg2 in pos_dict:
                                if int(fg1) < int(fg2):
                                    for p2 in pos_dict[fg2]:
                                        if p1 > p2: # R2bis
                                            cost += Rc1
                                            if return_rules_importance: rules_dict['R2bis'] += Rc1
                                        if int(fret_positions[p1]) > int(fret_positions[p2]): # R2
                                            cost += Rc2
                                            if return_rules_importance: rules_dict['R2'] += Rc2
                                        elif fret_positions[p1] == fret_positions[p2]: # R2ter
                                            Rc3 = (max(pos1)-min(pos1)+1)**4 * (max(pos_dict[fg2])-min(pos_dict[fg2])+1)**4 * (int(fg2) - int(fg1))
                                            cost += Rc3
                                            if return_rules_importance: rules_dict['R2ter'] += Rc3
                                            if p1 > p2: # R2bis
                                                cost += Rc4
                                                if return_rules_importance: rules_dict['R2bis'] += Rc4

        elif R == 'R3':
            ### R3: The span between Finger 1 and Finger 4 must be 5 or less when on the first
            # 4 frets, 6 or less when on 5-15 frets, and 7 or less when on 16-24 frets.
            Rc1 = 100000
            try:
                fret_first = min(frets_used)
                fret_last = max(frets_used)
                if fret_last - fret_first > utilities.finger_span[fret_first]:
                    cost += Rc1
                    if return_rules_importance: rules_dict['R3'] += Rc1
                else:
                    Rc2 = utilities.finger_span_cost[fret_last - fret_first]
                    cost += Rc2
                    if return_rules_importance: rules_dict['R3'] += Rc2
            except ValueError:
                # all played frets are open
                fret_first = 0
                fret_last = 0
                pass

        elif R == 'R4':
            ### R4: Finger 1 is often used for barre chords, so can cover anywhere
            # between 1-6 strings on the same fret. While other fingers can also
            # bar several strings, they tend to cover only 2 or 3 strings.
            # Fingers 1 & 2, tend to be the most strong and dominant,
            # with 4 being the weakest and least dominant, hence there tends to be
            # little bar function for fingers 3 & 4.
            ### R4bis: Barre rule for 3-6 strings. Slight penalty for having a
            # barre chord going over 3-6 strings. Higher cost for each higher
            # finger number.
            for i,fg in enumerate(utilities.fingers):
                if fg in pos_dict:
                    len_barre = max(pos_dict[fg])-min(pos_dict[fg])+1
                    Rc1 = (len_barre**2+1)*int(fg)*5
                    cost += Rc1
                    if return_rules_importance: rules_dict['R4'] += Rc1
                    if len_barre >= 3:
                        Rc2 = (int(fg)-1)*20 * (len_barre-3)*20
                        cost += Rc2
                        if return_rules_importance: rules_dict['R4bis'] += Rc2

        elif R == 'R5':
            ### R5: One finger cannot barre different fret numbers.
            Rc = 100000
            for fg in fingers_used:
                if len(set([fret_positions[p] for p in pos_dict[str(fg)]])) > 1:
                    cost += Rc
                    if return_rules_importance: rules_dict['R5'] += Rc

        elif R == 'R6':
            ### R6: A barre chord is impossible if other smaller fret numbers
            # are being played on strings inside barre or under it (R6bis).
            Rc1 = 100000
            Rc2 = 500
            for fg in fingers_used:
                if len(pos_dict[str(fg)]) > 1:
                    for i,ft in enumerate(fret_positions):
                        if i not in pos_dict[str(fg)] and ft.lower()!='x' and ft!='0':
                            if int(ft) <= int(fret_positions[min(pos_dict[str(fg)])]):
                                if i > min(pos_dict[str(fg)]) and i < max(pos_dict[str(fg)]):
                                    cost += Rc1
                                    if return_rules_importance: rules_dict['R6'] += Rc1
                                elif i > max(pos_dict[str(fg)]):
                                    if i > max(pos_dict[str(fg)]) + 1 and finger_positions[i-1] != 'x' and finger_positions[i-1] != '0':
                                        pass
                                    elif i > max(pos_dict[str(fg)]) + 2 and finger_positions[i-2] != 'x' and finger_positions[i-2] != '0':
                                        pass
                                    elif i > max(pos_dict[str(fg)]) + 3 and finger_positions[i-3] != 'x' and finger_positions[i-3] != '0':
                                        pass
                                    else:
                                        cost += Rc2
                                        if return_rules_importance: rules_dict['R6bis'] += Rc2

        elif R == 'R7':
            ### R7: Fingers tend to be in their natural position from first fret,
            # that is 1 per fret interval.
            for fg in fingers_used:
                if fg != 5:
                    for p in pos_dict[str(fg)]:
                        Rc = ( ( (int(fret_positions[p]) - fret_first) - (fg - 1) )**2 ) *150
                        cost += Rc
                        if return_rules_importance: rules_dict['R7'] += Rc
            """
            for fg in fingers_used:
                if fg != 5:
                    for p in pos_dict[str(fg)]:
                        if fg == 1 or fg == 2:
                            Rc = ( ( (int(fret_positions[p]) - fret_first) - (fg - 1) )**2 ) *150
                            cost += Rc
                            if return_rules_importance: rules_dict['R7'] += Rc
                        elif fg == 3:
                            if '2' not in pos_dict:
                                Rc = ( ( (int(fret_positions[p]) - fret_first) - (fg - 1) )**2 ) *150
                                cost += Rc
                                if return_rules_importance: rules_dict['R7'] += Rc
                            else:
                                Rc = ( ( (int(fret_positions[p]) - int(fret_positions[pos_dict['2'][0]])) - (fg - 2) )**2 ) *150
                                cost += Rc
                                if return_rules_importance: rules_dict['R7'] += Rc
                        elif fg == 4:
                            if '2' not in pos_dict and '3' not in pos_dict:
                                Rc = ( ( (int(fret_positions[p]) - fret_first) - (fg - 1) )**2 ) *150
                                cost += Rc
                                if return_rules_importance: rules_dict['R7'] += Rc
                            elif '3' in pos_dict:
                                Rc = ( ( (int(fret_positions[p]) - int(fret_positions[pos_dict['3'][0]])) - (fg - 3) )**2 ) *150
                                cost += Rc
                                if return_rules_importance: rules_dict['R7'] += Rc
                            else:
                                Rc = ( ( (int(fret_positions[p]) - int(fret_positions[pos_dict['2'][0]])) - (fg - 2) )**2 ) *150
                                cost += Rc
                                if return_rules_importance: rules_dict['R7'] += Rc
            """


        elif R == 'R8':
            ### R8: If you have 3-4 different frets being used,
            # it's good to use one finger per fret
            Rc = 1000
            if len([ft for ft in fret_positions if ft != '0' and ft != 'x']) <= 4:
                if len(fingers_used) < 4:
                    if any([len(pos_dict[str(fg)]) > 1 for fg in fingers_used if fg != 1 and fg != 5]):
                        cost += Rc
                        if return_rules_importance: rules_dict['R8'] += Rc

        elif R == 'R9':
            ### R9: Finger 2 and 3 are more difficult to make barre if other fingers after it (eg finger 3 and 4) are more than 2 strings physically above it.
            Rc1 = 10000
            Rc2 = 2000
            for fg in ['2','3']:
                if fg in pos_dict:
                    if len(pos_dict[fg]) > 1 :
                        for i,ft in enumerate(fret_positions):
                            if i not in pos_dict[fg] and ft.lower()!='x' and ft!='0':
                                if i < min(pos_dict[fg]) - 3 or i < max(pos_dict[fg]) - 4 and finger_positions[i] != '5':
                                    cost += Rc1
                                    if return_rules_importance: rules_dict['R9'] += Rc1
                                elif i < min(pos_dict[fg]) - 2 or i < max(pos_dict[fg]) - 3 and finger_positions[i] != '5':
                                    cost += Rc2
                                    if return_rules_importance: rules_dict['R9'] += Rc2

        elif R == 'R10':
            ### R10: Fingers 1 and 2 hardly make simultaneous barre.
            Rc = 5000
            if '1' in pos_dict and '2' in pos_dict:
                if len(pos_dict['1']) > 1 and len(pos_dict['2']) > 1 :
                    cost += Rc
                    if return_rules_importance: rules_dict['R10'] += Rc

        elif R == 'R11':
            ### R11: It is hard for finger 3 and 4 to cover more than a 4-strings gap.
            Rc = 10000
            if '4' in pos_dict:
                for i,ft in enumerate(fret_positions):
                    if finger_positions[i] == '3':
                        if i not in pos_dict['4'] and ft!='x' and ft!='0':
                            if i > min(pos_dict['4']) + 4:
                                cost += Rc
                                if return_rules_importance: rules_dict['R11'] += Rc

        elif R == 'R12':
            ### R12: Chord is harder to play if muted strings are surrounded by played ones.
            """
            Rc = 1500
            for i,ft in enumerate(fret_positions):
                if ft.lower() == 'x' and i!=0 and i!=5:
                    if fret_positions[i-1].lower()!='x':
                        if any( [ ft2.lower()!='x' for ft2 in fret_positions[i:] ] ):
                            cost += Rc
                            if return_rules_importance: rules_dict['R12'] += Rc
            """
            Rc = int(muted_model_func(fret_positions)/10)
            cost += Rc
            if return_rules_importance: rules_dict['R12'] += Rc

        elif R == 'R13':
            ### R13: The span between 2 consecutive fingers must be 3 or less when on the first
            # 4 frets, 4 or less when on 5-15 frets, and 5 or less when on 16-24 frets.
            for fg1 in fingers_used:
                for fg2 in fingers_used:
                    if fg2-1 == fg1 and fg2 != 5:
                        if ( int(fret_positions[pos_dict[str(fg2)][0]])
                             - int(fret_positions[pos_dict[str(fg1)][0]]) ) \
                             > utilities.finger_span[fret_first] - 3:
                            Rc = (utilities.finger_span[fret_first] - 3)**2 * 100 * abs( int(fret_positions[pos_dict[str(fg2)][0]]) - int(fret_positions[pos_dict[str(fg1)][0]]) ) * 2
                            cost += Rc
                            if return_rules_importance: rules_dict['R13'] += Rc
                        if fg1 == 1:
                            if int(fret_positions[pos_dict[str(fg2)][0]]) - int(fret_positions[pos_dict[str(fg1)][0]]) > 0:
                                Rc = ( abs( int(fret_positions[pos_dict[str(fg2)][0]]) - int(fret_positions[pos_dict[str(fg1)][0]]) ) - 1 ) * 100
                                cost += Rc
                                if return_rules_importance: rules_dict['R13'] +=  Rc

        elif R == 'R14':
            ### R14: It's very hard or impossible to hold down more than 3 strings with
            # finger 3 and also have finger 4 over it.
            Rc = 10000
            if '3' in pos_dict and '4' in pos_dict:
                if max(pos_dict['3'])-min(pos_dict['3']) > 1 :
                    if min(pos_dict['4']) < max(pos_dict['3']):
                        cost += Rc
                        if return_rules_importance: rules_dict['R14'] += Rc

        elif R == 'R15':
            ### R15: Pinky on high frets rule. If you are barring all strings with
            # the first finger, and you are using the fourth finger, it becomes
            # increasigly difficult to reach the higher string numbers (5=A, 6=E)
            # as you go up the frets around fret 10 with the pinky finger.
            Rc = fret_last**2
            if '4' in pos_dict and '1' in pos_dict:
                if max(pos_dict['1'])-min(pos_dict['1']) == 5:
                    Rc += (6-min(pos_dict['4']))**4 * 0.5
            cost += Rc
            if return_rules_importance: rules_dict['R15'] += Rc

        elif R == 'R16':
            ### R16: 4th finger cannot be higher in strings than 2nd or 3rd fingers
            # when 1st finger is far behind 2nd or 3rd (and same if fg4 vertically
            # higher than fg3 and fg2 far behind).
            Rc = 4000
            if '4' in pos_dict and '1' in pos_dict:
                for fg in ['2','3']:
                    if fg in pos_dict:
                        if abs(int(fret_positions[pos_dict['1'][0]]) - int(fret_positions[pos_dict[fg][0]])) > 2:
                            if min(pos_dict['4']) < max(pos_dict[fg]):
                                cost += Rc
                                if return_rules_importance: rules_dict['R16'] += Rc
            if '4' in pos_dict and '2' in pos_dict and '3' in pos_dict:
                    if abs(int(fret_positions[pos_dict['2'][0]]) - int(fret_positions[pos_dict['3'][0]])) > 1:
                        if min(pos_dict['4']) < max(pos_dict['3']):
                            cost += Rc
                            if return_rules_importance: rules_dict['R16'] += Rc

        elif R == 'R17':
            ### R17: Limited finger rule: You can only have fingers 1-5.
            Rc = 500000
            for fg in fingers_used:
                if fg < 0 or fg > 5:
                    cost += Rc
                    if return_rules_importance: rules_dict['R17'] += Rc

        elif R == 'R18':
            ### R18: Thumb can cover only string 6, 5 and 4, with barre only.
            # For each extra string from 6 to 5 to 4 add a small penalty.
            Rc1 = 200000
            if '5' in pos_dict:
                if all( [ p5<3 for p5 in pos_dict['5'] ] ):
                    if 0 in pos_dict['5']:
                        if 2 in pos_dict['5'] and 1 not in pos_dict['5']:
                            cost += Rc1
                            if return_rules_importance: rules_dict['R18'] += Rc1
                        else:
                            Rc2 = ( len(pos_dict['5'])**2 ) * 1000
                            cost += Rc2
                            if return_rules_importance: rules_dict['R18'] += Rc2
                    else:
                        cost += Rc1
                        if return_rules_importance: rules_dict['R18'] += Rc1
                else:
                    cost += Rc1
                    if return_rules_importance: rules_dict['R18'] += Rc1

        elif R == 'R19':
            ### R19: Finger sequence rule b): if f5 is in use then: f5<=f4
            # and f5 can\'t be less than 2 frets less than f1.
            # For each fret that f5 is higher up in frets from f1, add a penalty,
            # and a high penalty if fret on f5= fret on f4.
            Rc1 = 100000
            Rc2 = 5000
            if '5' in pos_dict:
                for pos5 in pos_dict['5']:
                    if len(fingers_used) > 1:
                        fg_max = str(max([fu for fu in fingers_used if fu != 5]))
                        for pos4 in pos_dict[fg_max]:
                            if int(fret_positions[pos5]) > int(fret_positions[pos4]):
                                cost += Rc1
                                if return_rules_importance: rules_dict['R19'] += Rc1
                            elif int(fret_positions[pos5]) == int(fret_positions[pos4]):
                                cost += Rc2
                                if return_rules_importance: rules_dict['R19'] += Rc2
                            elif int(fret_positions[pos5]) < int(fret_positions[pos4]) - 4:
                                cost += Rc1
                                if return_rules_importance: rules_dict['R19'] += Rc1
                            elif int(fret_positions[pos5]) < int(fret_positions[pos4]) - 3:
                                cost += Rc2
                                if return_rules_importance: rules_dict['R19'] += Rc2
                    pos_min = pos_dict[str(min(fingers_used))][0]
                    if int(fret_positions[pos5]) < int(fret_positions[pos_min]) - 2:
                        cost += Rc1
                        if return_rules_importance: rules_dict['R19'] += Rc1
                    if int(fret_positions[pos_min]) < int(fret_positions[pos5]):
                        Rc3 = ( int(fret_positions[pos5]) - int(fret_positions[pos_min]) )**3 * 1000
                        cost += Rc3
                        if return_rules_importance: rules_dict['R19'] += Rc3

        elif R == 'R20':
            ### R20: Finger gap (horizontal) difficulty rule when consecutive fingers
            # are one string appart (vertical). For the same gap between any two
            # consecutive fingers eg f1 and f2, f2 and f3, f3 and f4, there are
            # different costs because the flexibility between fingers is different.
            # (For example, if f1 and f2 are on frets=4 and fret=6 and string 6 and 5,
            # then that is easier to play than if you were to use finger f2 and f3 on
            # the same frets. Lets say the penalty for one fret_gap_cost=200 (this
            # depends on the fret number). Give the finger difficulty between
            # f1 and f2 = 1 x fret_gap_cost
            # f2 and f3 = 1.5 x fret_gap_cost
            # f3 and f4 = 1.3 x fret_gap_cost
            coef = 0.25
            for fg1 in fingers_used:
                for fg2 in fingers_used:
                    if fg2-1 == fg1:
                        pos1 = pos_dict[str(fg1)][0]
                        pos2 = pos_dict[str(fg2)][0]
                        if fg1 == 1:
                            Rc = int( ( 40 - int(fret_positions[pos1]) ) * abs( int(fret_positions[pos2]) - int(fret_positions[pos1]) - 1 ) * 1 * coef )
                            cost += Rc
                            if return_rules_importance: rules_dict['R20'] += Rc
                        elif fg1 == 2:
                            Rc = int( ( 40 - int(fret_positions[pos1]) ) * abs( int(fret_positions[pos2]) - int(fret_positions[pos1]) - 1 ) * 1.5 * coef )
                            cost += Rc
                            if return_rules_importance: rules_dict['R20'] += Rc
                        elif fg1 == 3:
                            Rc = int( ( 40 - int(fret_positions[pos1]) ) * abs( int(fret_positions[pos2]) - int(fret_positions[pos1]) - 1 ) * 1.3 * coef )
                            cost += Rc
                            if return_rules_importance: rules_dict['R20'] += Rc
                    if fg2-2 == fg1:
                        pos1 = pos_dict[str(fg1)][0]
                        pos2 = pos_dict[str(fg2)][0]
                        if fg1 == 1:
                            Rc = int( ( 40 - int(fret_positions[pos1]) ) * abs( int(fret_positions[pos2]) - int(fret_positions[pos1]) - 2 ) * 1 * coef * 0.5 )
                            cost += Rc
                            if return_rules_importance: rules_dict['R20'] += Rc
                        elif fg1 == 2:
                            Rc = int( ( 40 - int(fret_positions[pos1]) ) * abs( int(fret_positions[pos2]) - int(fret_positions[pos1]) - 2 ) * 1 * coef * 0.5 )
                            cost += Rc
                            if return_rules_importance: rules_dict['R20'] += Rc
                    if fg2-3 == fg1:
                        pos1 = pos_dict[str(fg1)][0]
                        pos2 = pos_dict[str(fg2)][0]
                        if fg1 == 1:
                            Rc = int( ( 40 - int(fret_positions[pos1]) ) * abs( int(fret_positions[pos2]) - int(fret_positions[pos1]) - 3 ) * 1 * coef * 0.25 )
                            cost += Rc
                            if return_rules_importance: rules_dict['R20'] += Rc


        elif R == 'R21':
            ### R21: Three finger crowding rule for low and high fret numbers:
            # If you have three consecutive fingers on the same fret, next to each
            # other on 3 adjacent strings, on frets<=9 then the smallest finger number
            # should be in the middle (eg string 3), with the second largest finger
            # number on lower sounding string number (eg string 4) and the third
            # largest finger number on the highest sounding string (eg string 2).
            # For fret>9 the lowest finger number should be on the highest string
            # number (eg string 4), the second lowest finger should be on the second
            # highest string number (eg string 3) and the third lowest finger should
            # be on the lowest string number (eg string 2).
            Rc = 100
            for i in range(2,6):
                if fret_positions[i] == fret_positions[i-1] and fret_positions[i-2] == fret_positions[i-1] and fret_positions[i] != 'x' and fret_positions[i] != '0':
                    if finger_positions[i] != finger_positions[i-1] and finger_positions[i] != finger_positions[i-2] and finger_positions[i-1] != finger_positions[i-2]:
                        concerned_fingers = [int(finger_positions[i-2]), int(finger_positions[i-1]), int(finger_positions[i])]
                        ordered_concerned_fingers = sorted(concerned_fingers)
                        fg1, fg2, fg3 = ordered_concerned_fingers
                        if int(fret_positions[i]) <= 9:
                            if concerned_fingers[1] != fg1:
                                cost += Rc
                                if return_rules_importance: rules_dict['R21'] += Rc
                            if concerned_fingers[0] != fg2:
                                cost += Rc
                                if return_rules_importance: rules_dict['R21'] += Rc
                            if concerned_fingers[2] != fg3:
                                cost += Rc
                                if return_rules_importance: rules_dict['R21'] += Rc
                        else:
                            if concerned_fingers[2] != fg1:
                                cost += Rc
                                if return_rules_importance: rules_dict['R21'] += Rc
                            if concerned_fingers[1] != fg2:
                                cost += Rc
                                if return_rules_importance: rules_dict['R21'] += Rc
                            if concerned_fingers[0] != fg3:
                                cost += Rc
                                if return_rules_importance: rules_dict['R21'] += Rc

        elif R == 'R22':
            ### R22: The rule is about using as few unique fingers as possible.
            # For example if you can play a chord with 3 fingers, instead of 4,
            # then you should, even if it includes barres. A little penalty is
            # added for each finger that is used, very slightly increasing
            # as the finger number gets higher, including the thumb.
            if len(fingers_used) > 0:
                Rc = sum( [4*fg for fg in list(fingers_used)] )
                cost += Rc
                if return_rules_importance: rules_dict['R22'] += Rc


        elif R == 'R23':
            ### R23: Occam's Razor: The fewer fingers you can use, the better.
            Rc = 0
            for i,fg in enumerate(utilities.fingers):
                if fg in pos_dict:
                    len_barre = max(pos_dict[fg])-min(pos_dict[fg])+1
                    Rc += (int(fg) + 11) * (1 + len_barre/6.)
            Rc = int(Rc)
            cost += Rc
            if return_rules_importance: rules_dict['R23'] += Rc


        elif R == 'R24':
            ### R24: Null finger on Fretboard Rule: If a fret on a string is
            # larger than zero, then the finger cannot be zero, and the reverse
            # (as well as muted string or else).
            Rc = 500000
            if len([0 for fgp, ftp in zip(finger_positions, fret_positions) if ( fgp != ftp and ( fgp == '0' or ftp == '0' or fgp == 'x' or ftp == 'x' ) )]) > 0:
                cost += Rc
                if return_rules_importance: rules_dict['R24'] += Rc

        elif R == 'R25':
            ### R25: Shape Complexity Rule:
            """
            # When moving from string to string
            # (eg string 6 to string 1), count the direction changes (similar
            # to zig zags) and add them to the cost with a factor.
            ordered_frets = [int(ft) for ft in fret_positions if ft.lower() != 'x' and ft != '0']
            if len(ordered_frets) > 2:
                direction_changes = sum( [ (ft2 > ft1 and ft2 > ft3) or (ft2 < ft1 and ft2 < ft3)
                                            for ft1, ft2, ft3
                                            in zip(ordered_frets[:-2], ordered_frets[1:-1], ordered_frets[2:]) ] )
            else:
                direction_changes = 0
            Rc = direction_changes * 100
            cost += Rc
            if return_rules_importance: rules_dict['R25'] += Rc
            """
            Rc = int(fret_model_func(fret_positions)/10)
            cost += Rc
            if return_rules_importance: rules_dict['R25'] += Rc

        elif R == 'R26':
            ### R26: Finger 3 is the better middle finger. If you are using
            # finger 1 and finger 4, and the fret inbetween f1 and f4 is
            # more than halfway towards f4, then use f3, otherwise use f2.
            Rc = 100
            if '1' in fingers_used and '4' in fingers_used:
                ft1 = fret_positions[pos_dict['1'][0]]
                ft4 = fret_positions[pos_dict['4'][0]]
                if ft1 != ft4:
                    if min(pos_dict['1']) < min(pos_dict['4']):
                        thres = 0.5001
                    else:
                        #thres = 0.4999
                        thres = 0.5001
                    if '3' in fingers_used and '2' not in fingers_used:
                        ft3 = fret_positions[pos_dict['3'][0]]
                        if (ft3 - ft1)/float(ft4 - ft1) > thres:
                            Rc -= 50
                    elif '2' in fingers_used and '3' not in fingers_used:
                        ft2 = fret_positions[pos_dict['2'][0]]
                        if (ft2 - ft1)/float(ft4 - ft1) < thres:
                            Rc -= 50
            cost += Rc
            if return_rules_importance: rules_dict['R26'] += Rc

        elif R == 'R27':
            ### R27: A finger of higher number cannot be over a barre of another
            # finger on the same fret number.
            Rc = 3200
            for fg1 in fingers_used:
                if len(pos_dict[str(fg1)]) > 1:
                    for fg2 in fingers_used:
                        if int(fg2) > int(fg1):
                            if fret_positions[pos_dict[str(fg1)][0]] == fret_positions[pos_dict[str(fg2)][0]] and pos_dict[str(fg2)][0] < pos_dict[str(fg1)][0]-1:
                                cost += Rc
                                if return_rules_importance: rules_dict['R27'] += Rc

        elif R == 'R28':
            ### R28: Using different fingers under and over a 'x' is better than
            # a barre (strumming vs plucking)
            """
            if strummable:
                if 'x' in pos_dict:
                    pos_xp = 0
                    for pos_x in pos_dict['x']:
                        if pos_x > pos_xp and pos_x != 5 and pos_x != 0:
                            pos_xm = pos_x-1
                            pos_xp = pos_x+1
                            while finger_positions[pos_xm] == 'x' and pos_xm > 0:
                                pos_xm -= 1
                            while finger_positions[pos_xp] == 'x' and pos_xp < 5:
                                pos_xp += 1
                            if finger_positions[pos_xm] == finger_positions[pos_xp] and finger_positions[pos_xm] != 'x' and (pos_xp - pos_xm <= 3 or (pos_xp < 5 and finger_positions[pos_xp] == finger_positions[pos_xp+1] and pos_xp - pos_xm <= 4)):
                                if len([fg for fg in finger_positions if fg.lower() != 'x' and fg != '0' and fg != '5']) <= 4:
                                    Rc = 3200
                                else:
                                    Rc = 100
                                cost += Rc
                                if return_rules_importance: rules_dict['R28'] += Rc
            """
            if strummable:
                Rc = 0
                for fg in fingers_used:
                    if len(pos_dict[str(fg)]) > 1:
                        sensible_positions = [ix for ix in range(min(pos_dict[str(fg)]), max(pos_dict[str(fg)])+1) if ix not in pos_dict[str(fg)]]
                        for pos in sensible_positions:
                            if finger_positions[pos] == 'x':
                                if len([fg for fg in finger_positions if fg.lower() != 'x' and fg != '0' and fg != '5']) <= 4:
                                    Rc = 3200
                                else:
                                    Rc = 100
                cost += Rc
                if return_rules_importance: rules_dict['R28'] += Rc


        elif R == 'R29':
            ### R29: Check if thumb should be used when strings A and D are x or 0 and E is used.
            #Rc = 8200
            Rc = 0
            pdict = []
            if '0' in pos_dict:
                pdict += pos_dict['0']
            if 'x' in pos_dict:
                pdict += pos_dict['x']
            if 1 in pdict and 2 in pdict and 0 not in pdict:
                cost += Rc
                if return_rules_importance: rules_dict['R29'] += Rc

        elif R == 'R30':
            ### R30: Add big penalty when using thumb while a finger is on the string just under it.
            #Rc = 5000
            Rc = 0
            if '5' in pos_dict:
                if 1 in pos_dict['5']:
                    if fret_positions[2] != '0' and fret_positions[2] != 'x':
                        cost += Rc
                        if return_rules_importance: rules_dict['R30'] += Rc
                elif 0 in pos_dict['5']:
                    if fret_positions[1] != '0' and fret_positions[1] != 'x':
                        cost += Rc
                        if return_rules_importance: rules_dict['R30'] += Rc

        elif R == 'R31':
            ### R31: High pitched pivot finger one rule: If finger 1 is on a high sounding string,
            # f2 is not in use and 3 and 4 are on lower sounding strings, add a penalty.
            #Rc = 400
            Rc = 0
            if '1' in pos_dict and '3' in pos_dict and '4' in pos_dict and '2' not in pos_dict:
                if min(pos_dict['1']) > max(pos_dict['3']+pos_dict['4']):
                    cost += Rc
                    if return_rules_importance: rules_dict['R31'] += Rc


    # Returns
    if return_rules_importance:
        return cost, rules_dict
    else:
        return cost



def rules_dict_to_str(rules_dict):
    """
    Return dictionary of rules as a string with costs associated in decreasing order.
    Do not print rules with null cost.

    Parameters
    ----------
    rules_dict : dict
        Dictionary with cost for each rule.

    Returns
    -------
    rules_str : str
        String with rules broken and costs in decreasing order.
    worst_rule : str
        Description of the least respected rule.
    """

    # sort rules
    sorted_rules = sorted([(rn,rc) for rn,rc in rules_dict.items() if rc!=0], key=itemgetter(1), reverse=True)
    # create string containing rules and costs
    rules_str = ", ".join(["%s: %d"%(rn, int(cost)) for rn, cost in sorted_rules])
    # get description of the least respected rule
    worst_rule = "%s: %s"%( sorted_rules[0][0], utilities.rule_descriptions[sorted_rules[0][0]] )

    return rules_str, worst_rule





# ===========================
# Main
# ===========================
if __name__=='__main__':

    #print compute_cost(['x','x','4','2','3','1'],['x','x','10','9','10','8'],True)
    #print compute_cost(['x','x','4','2','3','1'],['x','x','12','10','11','8'],True)
    #print compute_cost(['x','1','1','2','4','3'],['x','7','7','9','10','9'],True)
    #print compute_cost(['x','x','1','2','3','x'],['x','x','7','8','9','x'],True)
    #print compute_cost(['x','x','1','3','4','x'],['x','x','7','8','9','x'],True)
    cost, rules_dict = compute_cost(['1','2','2','2','3','4'],['10', '11', '11', '11', '11', '12'],True)
    rules =sorted(rules_dict.items(), key=itemgetter(1), reverse=True)
    print(cost, rules)
    cost, rules_dict = compute_cost(['1','2','2','2','2','3'],['10', '11', '11', '11', '11', '12'],True)
    rules =sorted(rules_dict.items(), key=itemgetter(1), reverse=True)
    print(cost, rules)
    print(predict_fingering(['9', '11', '11', '11', '11', '12']))
