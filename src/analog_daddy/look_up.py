"""
This module contains the look_up function, which is used to extract a desired
subset from the 4-dimensional simulation data and potentially interpolates if
the requested points aren't directly on the simulation grid.
"""
import numpy as np
from scipy.interpolate import RegularGridInterpolator, PchipInterpolator, interp1d
from analog_daddy.conf import (
    LENGTH_KEY, GS_KEY, DS_KEY, SB_KEY,
    DB_KEY, GB_KEY, METHOD_KEY, WARNING_KEY)

# don't warn user about bad divisions
np.seterr(divide="ignore", invalid="ignore")

def look_upVGS(data, **kwargs): #UNTESTED
    # Set values either using kwargs.get
    L = kwargs.get(LENGTH_KEY, min(data[LENGTH_KEY]))
    vds = kwargs.get(DS_KEY, max(data[DS_KEY]) / 2)
    vdb = kwargs.get(DB_KEY)
    vgb = kwargs.get(GB_KEY)
    gm_id = kwargs.get('gm_id')
    id_w = kwargs.get('id_w')
    vsb = kwargs.get(SB_KEY, 0)
    method = kwargs.get(METHOD_KEY, 'pchip')

    # Determine usage mode
    if vgb is None and vdb is None:
        mode = 1
    elif vgb is not None and vdb is not None:
        mode = 2
    else:
        print('Invalid syntax or usage mode!')
        return []

    # Check whether GM_ID or ID_W was passed to function
    if id_w is not None:
        ratio_string = 'id_w'
        ratio_data = id_w
    elif gm_id is not None:
        ratio_string = 'gm_id'
        ratio_data = gm_id
    else:
        print('look_upVGS: Invalid syntax or usage mode!')
        return []

    if mode == 1:
        vgs = data[GS_KEY]
        ratio = look_up(data, ratio_string, gs=vgs, ds=vds, sb=vsb, length=L)
    else:  # mode == 2
        step = data[GS_KEY][0] - data[GS_KEY][1]
        vsb = np.arange(max(data[SB_KEY]), min(data[SB_KEY]) - step, -step)
        vgs = vgb - vsb
        vds = vdb - vsb
        ratio = look_up(data, ratio_string, gs=vgs, ds=vds, sb=vsb, length=np.ones(len(vsb)) * L)

    # Interpolation loop
    s = np.shape(ratio)
    output = np.full((s[1], len(ratio_data)), np.nan)
    for j in range(s[1]):
        ratio_range = ratio[:, j]
        VGS_range = vgs
        if ratio_string == 'gm_id':
            idx = np.argmax(ratio_range)
            VGS_range = VGS_range[idx:]
            ratio_range = ratio_range[idx:]
            if max(ratio_data) > ratio_range[0]:
                print('look_upVGS: gm_id input larger than maximum!')
        f = interp1d(ratio_range, VGS_range, kind=method, bounds_error=False, fill_value=np.nan)
        output[j, :] = f(ratio_data)
    
    return output.flatten()

# result = look_upVGS(nch, GM_ID=[10,15], ds=0.6, sb=0.1, length=0.1)

def look_up(data, outvar, **kwargs):
    """
    Extracts a desired subset from the 4-dimensional simulation data and
    potentially interpolates if the requested points aren't directly on the simulation grid.
    """
    # Making the outvar lowercase to avoid case sensitivity
    outvar = outvar.lower()
    # Extracting parameters from kwargs or using default values
    length = kwargs.get(LENGTH_KEY, min(data[LENGTH_KEY]))
    vgs = kwargs.get(GS_KEY, data[GS_KEY])
    vds = kwargs.get(DS_KEY, max(data[DS_KEY])/2)
    vsb = kwargs.get(SB_KEY, 0)
    method = kwargs.get(METHOD_KEY, 'linear')
    warning = kwargs.get(WARNING_KEY, 'on')

    # Determine mode
    if '_' in outvar and any('_' in key for key in kwargs.keys()):
        # both output and input are ratios
        mode = 3
    elif '_' in outvar:
        # output is a ratio
        mode = 2
    else:
        # no ratio. simple lookup.
        mode = 1

    # Data extraction and interpolation for mode 1 and mode 2
    if mode in [1, 2]:

        # Extract ydata based on outvar
        if '_' in outvar:
            numerator, denominator = outvar.split('_')
            # making ydata as a ratio as requested.
            ydata = data[numerator] / data[denominator]
        else:
            ydata = data[outvar]

        # Linear Interpolation using RegularGridInterpolator
        if len(data[SB_KEY]) > 1:
            interpolator = RegularGridInterpolator((data[DS_KEY], data[GS_KEY], data[LENGTH_KEY], data[SB_KEY]), ydata)
            output = interpolator((vds, vgs, length, vsb))
        else:
            # If VSB isn't considered a dimension in data
            interpolator = RegularGridInterpolator((data[DS_KEY], data[GS_KEY], data[LENGTH_KEY]), ydata)
            output = interpolator((vds, vgs, length))
        
        
    # Mode 3
    if mode == 3:
        # extracting the invar from kwargs and making it lowercase to avoid case sensitivity
        invar = (next(key for key in kwargs.keys() if '_' in key)).lower()
        invals = kwargs[invar]
        # Interpolating the outvar data across VGS
        # both the outvar and invar are ratios hence making sure to use that ratio by splitting it.
        outvar_numerator, outvar_denominator = outvar.split('_')
        ydata_outvar = data[outvar_numerator] / data[outvar_denominator]
        outvar_interpolator = RegularGridInterpolator((data[DS_KEY], data[GS_KEY], data[LENGTH_KEY], data[SB_KEY]), ydata_outvar)
        invar_numerator, invar_denominator = invar.split('_')
        ydata_invar = data[invar_numerator] / data[invar_denominator]
        invar_interpolator = RegularGridInterpolator((data[DS_KEY], data[GS_KEY], data[LENGTH_KEY], data[SB_KEY]), ydata_invar)

        vgs_vals = np.linspace(min(data[GS_KEY]), max(data[GS_KEY]), len(data[GS_KEY]))
        outvar_values = outvar_interpolator((vds, vgs_vals, length, vsb))
        invar_values = invar_interpolator((vds, vgs_vals, length, vsb))

        if invar == "gm_id":
            # If gm_id is passed as the third
            # argument, special care is taken to look only "to the right" of the
            # maximum gm/ID value in the gm/ID vs. VGS plane.
            idx = np.argmax(invar_values)
            invar_values = invar_values[idx:]
            outvar_values = outvar_values[idx:]

        elif invar in ["gm_cgg", "gm_css"]:
            # If gm_cgg or gm_css is passed as the third
            # argument, special care is taken to look only "to the left" of the
            # maximum gm/cgg or gm/css value in the gm/cgg and gm/css vs. VGS plane.
            idx = np.argmax(invar_values)
            invar_values = invar_values[:idx+1]
            outvar_values = outvar_values[:idx+1]

        interpolator = PchipInterpolator(invar_values, outvar_values) if method == 'pchip' else interp1d(invar_values, outvar_values, kind=method)
        output = interpolator(invals)

    # Ensure the output is a column vector if one-dimensional
    if output.ndim == 2 and min(output.shape) == 1:
        output = output.flatten()
    return output
