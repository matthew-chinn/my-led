import config
import time
import numpy as np
from scipy.ndimage.filters import gaussian_filter1d
import microphone
import dsp
import led
import util
import gui


mel_gain = dsp.ExpFilter(np.tile(1e-1, config.N_FFT_BINS),
                         alpha_decay=0.01, alpha_rise=0.99)
mel_smoothing = dsp.ExpFilter(np.tile(1e-1, config.N_FFT_BINS),
                         alpha_decay=0.5, alpha_rise=0.99)
fft_window = np.hamming(int(config.MIC_RATE / config.FPS) * config.N_ROLLING_HISTORY)

# Number of audio samples to read every time frame
samples_per_frame = int(config.MIC_RATE / config.FPS)

# Array containing the rolling audio sample window
y_roll = np.random.rand(config.N_ROLLING_HISTORY, samples_per_frame) / 1e16

def microphone_callback(effect):
  def microphone_update(audio_samples):
      global y_roll
      # Normalize samples between 0 and 1
      y = audio_samples / 2.0**15
      # Construct a rolling window of audio samples
      y_roll[:-1] = y_roll[1:]
      y_roll[-1, :] = np.copy(y)
      y_data = np.concatenate(y_roll, axis=0).astype(np.float32)
      
      vol = np.max(np.abs(y_data))
      if vol < config.MIN_VOLUME_THRESHOLD:
          print('No audio input. Volume below threshold. Volume:', vol)
          led.pixels = np.tile(0, (3, config.N_PIXELS))
          led.update()
      else:
          # Transform audio input into the frequency domain
          N = len(y_data)
          N_zeros = 2**int(np.ceil(np.log2(N))) - N
          # Pad with zeros until the next power of two
          y_data *= fft_window
          y_padded = np.pad(y_data, (0, N_zeros), mode='constant')
          YS = np.abs(np.fft.rfft(y_padded)[:N // 2])
          # Construct a Mel filterbank from the FFT data
          mel = np.atleast_2d(YS).T * dsp.mel_y.T
          # Scale data to values more suitable for visualization
          # mel = np.sum(mel, axis=0)
          mel = np.sum(mel, axis=0)
          mel = mel**2.0
          # Gain normalization
          mel_gain.update(np.max(gaussian_filter1d(mel, sigma=1.0)))
          mel /= mel_gain.value
          mel = mel_smoothing.update(mel)
          # Map filterbank output onto LED strip
          output = effect(mel)
          led.pixels = output
          led.update()
          if config.USE_GUI:
              gui.update(mel)
      if config.USE_GUI:
          app.processEvents()
  return microphone_update
      
