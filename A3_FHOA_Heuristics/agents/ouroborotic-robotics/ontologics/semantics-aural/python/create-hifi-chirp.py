import wave
import math
import struct

# --- Parameters for the High-Quality Chirp ---
filename = "chirp_hq.wav"
sample_rate = 44100.0  # Hz, CD quality
duration = 0.25        # seconds
frequency_start = 500  # Hz, starting pitch
frequency_end = 2000   # Hz, ending pitch
amplitude = 32767.0    # Max amplitude for 16-bit audio
n_samples = int(duration * sample_rate)
n_channels = 1         # Mono
sampwidth = 2          # 16-bit audio = 2 bytes

# --- Generate the Waveform Data ---
# This creates a sine wave that sweeps from the start to the end frequency.
wav_data = bytearray()
for i in range(n_samples):
    # Calculate the current frequency in the sweep
    current_freq = frequency_start + (frequency_end - frequency_start) * (i / n_samples)
    
    # Calculate the sine wave value for this sample
    value = math.sin(2 * math.pi * current_freq * (i / sample_rate))
    
    # Scale to 16-bit integer range and pack as a binary value
    packed_value = struct.pack('h', int(amplitude * value))
    wav_data.extend(packed_value)

# --- Write the .wav file ---
with wave.open(filename, 'wb') as wav_file:
    wav_file.setnchannels(n_channels)
    wav_file.setsampwidth(sampwidth)
    wav_file.setframerate(sample_rate)
    wav_file.writeframes(wav_data)

print(f"File '{filename}' created successfully ({len(wav_data) + 44} bytes).")