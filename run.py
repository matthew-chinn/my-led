import led
import sys
import config
import gui
import microphone
import visualization

import visualize_scroll
import visualize_energy
import visualize_spectrum
import original_visualize_spectrum
import effect_decorators

""" effects need a run(mel) method """
effects = {
  1: effect_decorators.to_1d(visualize_scroll.effect),
  2: effect_decorators.to_1d(visualize_energy.effect),
  3: effect_decorators.to_1d(visualize_spectrum.effect),
  4: effect_decorators.to_2d(visualize_scroll.effect),
  5: effect_decorators.to_2d(visualize_energy.effect),
  6: effect_decorators.to_2d(visualize_spectrum.effect),
  7: original_visualize_spectrum.effect
}

default_effect = 5
"""Visualization effect to display on the LED strip"""

# Main program logic follows:
if __name__ == '__main__':
    print ('Press Ctrl-C to quit.')
    led.start()
    if config.USE_GUI:
        gui.create()
    # Initialize LEDs
    led.update()
    effect_index = default_effect
    try:
      effect_index = int(sys.argv[1])
    except TypeError:
      print('Not valid effect index', sys.argv[1])
      effect_index = default_effect
    if effect_index > len(effects):
      effect_index = default_effect
    # Start listening to live audio stream
    microphone.start_stream(visualization.microphone_callback(effects[effect_index]))
