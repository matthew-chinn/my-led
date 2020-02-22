import config
import numpy as np
import visualize_energy

""" A decorator that turns a 1-D effect into one that uses rows
  effect_fn: a reference to the function we want to decorate """
def to_2d(effect_fn):
    def run(y):
        y = np.copy(y)
        result = np.empty((3,0))
        for i in range(len(config.ROWS)):
            effect = effect_fn(y, config.ROWS[i], i)
            while len(effect[0]) < config.ROWS[i]:
              effect = np.hstack((effect, [[0],[0],[0]]))
            result = np.hstack((result, effect))
        return result
    return run

def to_1d(effect_fn):
  def run(y):
    result = effect_fn(y, config.N_PIXELS, 0)
    return result
  return run
