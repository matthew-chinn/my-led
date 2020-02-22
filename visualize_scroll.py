import config
import numpy as np
import dsp
from scipy.ndimage.filters import gaussian_filter1d

gain = dsp.ExpFilter(np.tile(0.01, config.N_FFT_BINS),
                 alpha_decay=0.001, alpha_rise=0.99)

# Maps rows to their p array.
p_vals = {}
"""Effect that originates in the center and scrolls outwards"""
def effect(y, num_pixels, row_index):
    if row_index not in p_vals:
      p_vals[row_index] = np.tile(1.0, (3, num_pixels // 2))
    y = y**2.0
    gain.update(y)
    y /= gain.value
    y *= 255.0
    r = int(np.max(y[:len(y) // 3]))
    g = int(np.max(y[len(y) // 3: 2 * len(y) // 3]))
    b = int(np.max(y[2 * len(y) // 3:]))
    # Scrolling effect window
    p_vals[row_index][:, 1:] = p_vals[row_index][:, :-1]
    p_vals[row_index] *= 0.98
    p_vals[row_index] = gaussian_filter1d(p_vals[row_index], sigma=0.2)
    # Create new color originating at the center
    p_vals[row_index][0, 0] = r
    p_vals[row_index][1, 0] = g
    p_vals[row_index][2, 0] = b
    # Update the LED strip
    return np.concatenate((p_vals[row_index][:, ::-1], p_vals[row_index]), axis=1)

