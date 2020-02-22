import numpy as np
import dsp
import config
import util

# Matches row index to the data
prev_spectrums = {}
r_filts = {}
b_filts = {}
common_modes = {}
def effect(y, num_pixels, row_index):
    """Effect that maps the Mel filterbank frequencies onto the LED strip"""
    global prev_spectrums
    if row_index not in prev_spectrums:
      prev_spectrums[row_index] = np.tile(0.01, num_pixels // 2)

    if row_index not in r_filts:
      r_filts[row_index] = dsp.ExpFilter(np.tile(0.01, num_pixels // 2),
                             alpha_decay=0.2, alpha_rise=0.99)
    if row_index not in b_filts:
      b_filts[row_index] = dsp.ExpFilter(np.tile(0.01, num_pixels // 2),
                             alpha_decay=0.1, alpha_rise=0.5)
    if row_index not in common_modes:
      common_modes[row_index] = dsp.ExpFilter(np.tile(0.01, num_pixels // 2),
                             alpha_decay=0.99, alpha_rise=0.01)

    y = np.copy(util.interpolate(y, num_pixels // 2))
    common_modes[row_index].update(y)
    diff = y - prev_spectrums[row_index]
    prev_spectrums[row_index] = np.copy(y)
    # Color channel mappings
    r = r_filts[row_index].update(y - common_modes[row_index].value)
    g = np.abs(diff)
    b = b_filts[row_index].update(np.copy(y))
    # Mirror the color channels for symmetric output
    r = np.concatenate((r[::-1], r))
    g = np.concatenate((g[::-1], g))
    b = np.concatenate((b[::-1], b))
    output = np.array([r, g,b]) * 255
    return output
