# ===========================
# Modules
# ===========================
import numpy as np


# ===========================
# Functions
# ===========================
def fret_model_func(fret_positions):
    """
    Compute the cost according to the fret model function fitted with Eureqa.

    Parameters
    ----------
    fret positions

    Returns
    -------
    fret model cost
    """

    fret_positions = [int(ft) if ft.lower() != 'x' and ft != '0' else -1 for ft in fret_positions]
    if -1 in fret_positions and len(set(fret_positions)) == 1:
        pass
    else:
        min_fret = min([ft for ft in fret_positions if ft != -1])
        fret_positions = [ft-min_fret+1 if ft != -1 else -1 for ft in fret_positions]
    FE, FA, FD, FG, FB, FF = fret_positions
    AG, AH, AI, AK, AL = FE, FA, FD, FB, FF

    cost_model_1 = 1370.27817079308 + 427.296945267095*FE + 8.09236623839701*np.exp(FG) + 8.09236623839701*np.exp(FF) + FB*3.58328953399011**FD + 2.56851522008576*FA*(np.exp(FA) if bool(FD) else 194.713555302073) - 112.21986727064*FE*FA
    cost_model_3 = 1234.53779811668 + AK + 224.984177214227 / AL + 3.8927560045366 ** AL + AK * np.exp(1.28792828818672 * AI) + np.exp(AH) * (15.9590836278352 if bool(AH) else 1450.20129647159 * AG) + ((AI if bool(AH) else 1291290.39337977 * AG) % 1141.96734977147)
    cost_model_4 = 361.697355619182*min([FA+FE**2, min([FF, FG*np.exp(FG) - np.exp(FG)])]) + (36.9031617309725*FA**2 if bool(FA + FE**2) else FG*np.exp(FG)) + max([987.770447556063 + 163.915238296089*FD, 987.770447556063 + 163.915238296089*FD + 120.609696934878*FE + 120.609696934878*FE*FB])
    cost_model_6 = 1244.63253441849 + 134.748547061397*FE + 83.0588918726727*FG + FD*FB+ 134.748547061397/FF + 14.4520624828296*np.exp(FA) + 3.85132078647912*np.exp(FG) + FD*FB*np.exp(FD) + np.exp(1.34841615089073*FF)
    model = [cost_model_1, cost_model_3, cost_model_4, cost_model_6]

    return min([(np.mean(model)), 16000.])
    #return min([(cost_model_1 + cost_model_4 + cost_model_6) / 3., 16000.])


def muted_model_func(fret_positions):
    """
    Compute the cost according to the fret model function for muted strings fitted with Eureqa.

    Parameters
    ----------
    fret positions

    Returns
    -------
    fret model cost for muted strings
    """

    # Muted Cost Estimation Model
    # This model takes the average of two models to estimate the difficulty of the simplified pattern of strings used, for example comparing frets of the pattern:

    # Model 3
    # This model is based on the sum of how many frets are larger than zero, how many frets are zero and how many are muted.
    sx = fret_positions.count('x') + fret_positions.count('X')
    s0 = fret_positions.count('0')
    s1 = len(fret_positions) - sx - s0

    # Model 3:
    cost_model_muted_3 = 482.531383355394 * s1 + s1 * s0 ** s1 + (11062.8091995312 - np.exp(s1) - 2.57328901853245 ** (s1 * s0 ** s1)) / (6.7925016865907 + 38.5756725842058 * s1 ** (63.1562092766299 - sx * s1 ** 3)) - 599.343247028422

    # Mute pattern model
    # This model is based on the muted string pattern for each of the six strings. It has 6 input parameters.
    fret_positions = [-2 if ft.lower() == 'x' else (-1 if int(ft) == 0 else 1) for ft in fret_positions]
    ME, MA, MD, MG, MB, MF = fret_positions
    DQ, DR, DS, DT, DU, DV = ME, MA, MD, MG, MB, MF

    cost_model_muted_pattern = 2425.41355619814 + 180.736631134003*DQ*DR**2 + 150.673682364912*DV*DU**2 - 44.9598296728239*DR*DV - 180.736631134003*DS*DT - 185.845209918433*DT*DU - 189.728614102185*DR*DS

    return ( cost_model_muted_3 if s0 > 0 else (cost_model_muted_3 + cost_model_muted_pattern)/2 )
