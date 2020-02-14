import led
import config
import gui
import microphone
import visualization

# Main program logic follows:
if __name__ == '__main__':
    print ('Press Ctrl-C to quit.')
    led.start()
    if config.USE_GUI:
        gui.create()
    # Initialize LEDs
    led.update()
    # Start listening to live audio stream
    microphone.start_stream(visualization.microphone_update)
