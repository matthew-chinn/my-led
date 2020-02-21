import config
import numpy as np
import visualize_energy

# Make this a decorator so it works for all of the single dimensional ones
def run(y):
    """Effect that expands from the center with increasing sound energy"""
    global p
        
    y = np.copy(y)
    result = np.empty((3,0))
    for row in config.ROWS:
        effect = visualize_energy.effect(y, row)
        result = np.hstack((result, effect))
    while len(result[0]) < config.N_PIXELS:
      result = np.hstack((result, [[0],[0],[0]]))
    return result


