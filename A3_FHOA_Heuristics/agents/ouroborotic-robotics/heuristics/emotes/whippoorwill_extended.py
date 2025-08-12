import wave
import struct
import math
import random

# --- Parameters ---
FILENAME = "whippoorwill_extended.wav"
SAMPLE_RATE = 44100
BASE_AMPLITUDE = 24000.0
NUMBER_OF_CALLS = 5

# --- Composition ---
# Durations for each part of the call
CLUCK_DUR = 0.05
WHIP_DUR = 0.15
WILL_DUR = 0.4
PAUSE_SHORT = 0.08
PAUSE_BETWEEN_CALLS = 1.2 # The base pause duration between calls

# Frequencies for the different notes
CLUCK_FREQ = 300.0
WHIP_FREQ = 740.0  # F#5
WILL_FREQ_BASE = 988.0 # B5

# Parameters for the trill/vibrato on the final note
VIBRATO_DEPTH = 15.0
VIBRATO_RATE = 20.0

def generate_tone(freq, duration, amp, vibrato_params=None):
    """
    Generates byte data for a sine wave. Can optionally add vibrato
    to create a trilling effect.
    """
    num_samples = int(duration * SAMPLE_RATE)
    byte_data = bytearray()
    
    for i in range(num_samples):
        current_freq = freq
        if vibrato_params:
            v_rate, v_depth = vibrato_params
            current_freq += math.sin(2 * math.pi * v_rate * (i / SAMPLE_RATE)) * v_depth

        value = math.sin(2 * math.pi * current_freq * (i / SAMPLE_RATE))
        
        progress = i / num_samples
        envelope = min(1.0, progress * 20) * (1 - progress)
        
        packed_value = struct.pack('h', int(value * envelope * amp))
        byte_data.extend(packed_value)
        
    return byte_data

def generate_silence(duration):
    """Generates byte data for silence."""
    num_samples = int(duration * SAMPLE_RATE)
    # Ensure duration is not negative
    if num_samples < 0:
        return bytearray()
    return bytearray(num_samples * 2)

# --- Main Synthesis ---
print(f"Generating an extended whip-poor-will call into '{FILENAME}'...")

final_wav_data = bytearray()

for i in range(NUMBER_OF_CALLS):
    print(f"Generating call {i+1} of {NUMBER_OF_CALLS}...")
    
    # --- Introduce random variations for this specific call ---
    pitch_mod = random.uniform(0.98, 1.02) # Vary pitch by up to 2%
    amp_mod = random.uniform(0.90, 1.0)    # Vary amplitude
    
    # Start with a variable moment of silence
    pause_mod = random.uniform(-0.3, 0.3)
    final_wav_data.extend(generate_silence(PAUSE_BETWEEN_CALLS + pause_mod))

    # 1. The introductory "cluck"
    final_wav_data.extend(generate_tone(CLUCK_FREQ * pitch_mod, CLUCK_DUR, BASE_AMPLITUDE * 0.5 * amp_mod))
    final_wav_data.extend(generate_silence(PAUSE_SHORT))

    # 2. The "whip" note
    final_wav_data.extend(generate_tone(WHIP_FREQ * pitch_mod, WHIP_DUR, BASE_AMPLITUDE * amp_mod))
    final_wav_data.extend(generate_silence(0.02))

    # 3. The "WILL" note
    vibrato = (VIBRATO_RATE, VIBRATO_DEPTH)
    final_wav_data.extend(generate_tone(WILL_FREQ_BASE * pitch_mod, WILL_DUR, BASE_AMPLITUDE * 1.2 * amp_mod, vibrato_params=vibrato))

# --- Write the final .wav file ---
with wave.open(FILENAME, 'wb') as wav_file:
    wav_file.setnchannels(1)
    wav_file.setsampwidth(2)
    wav_file.setframerate(int(SAMPLE_RATE))
    wav_file.writeframes(final_wav_data)

print("Synthesis complete.")