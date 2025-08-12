import wave
import struct
import math

# --- Parameters ---
FILENAME = "whippoorwill_call.wav"
SAMPLE_RATE = 44100
AMPLITUDE = 24000.0

# --- Composition ---
# Durations for each part of the call
CLUCK_DUR = 0.05
WHIP_DUR = 0.15
WILL_DUR = 0.4
PAUSE_SHORT = 0.08
PAUSE_LONG = 0.5

# Frequencies for the different notes
CLUCK_FREQ = 300.0
WHIP_FREQ = 740.0  # F#5
WILL_FREQ_BASE = 988.0 # B5

# Parameters for the trill/vibrato on the final note
VIBRATO_DEPTH = 15.0  # How much the pitch will vary
VIBRATO_RATE = 20.0   # How fast the pitch will vary

def generate_tone(freq, duration, amp, vibrato_params=None):
    """
    Generates byte data for a sine wave. Can optionally add vibrato
    to create a trilling effect.
    """
    num_samples = int(duration * SAMPLE_RATE)
    byte_data = bytearray()
    
    for i in range(num_samples):
        current_freq = freq
        # If vibrato is enabled, modulate the frequency
        if vibrato_params:
            v_rate, v_depth = vibrato_params
            current_freq += math.sin(2 * math.pi * v_rate * (i / SAMPLE_RATE)) * v_depth

        # Generate the main sine wave value at the (possibly modulated) frequency
        value = math.sin(2 * math.pi * current_freq * (i / SAMPLE_RATE))
        
        # Apply a simple fade in/out to prevent clicks
        progress = i / num_samples
        envelope = min(1.0, progress * 20) * (1 - progress)
        
        packed_value = struct.pack('h', int(value * envelope * amp))
        byte_data.extend(packed_value)
        
    return byte_data

def generate_silence(duration):
    """Generates byte data for silence."""
    num_samples = int(duration * SAMPLE_RATE)
    return bytearray(num_samples * 2)

# --- Main Synthesis ---
print(f"Generating the sound of a whip-poor-will into '{FILENAME}'...")

# Start with a moment of silence
wav_data = generate_silence(PAUSE_LONG)

# 1. The introductory "cluck"
# Using a low-frequency tone with a very short duration and low amplitude
wav_data.extend(generate_tone(CLUCK_FREQ, CLUCK_DUR, AMPLITUDE * 0.5))
wav_data.extend(generate_silence(PAUSE_SHORT))

# 2. The "whip" note
# A clean, clear, steady tone
wav_data.extend(generate_tone(WHIP_FREQ, WHIP_DUR, AMPLITUDE))
wav_data.extend(generate_silence(0.02)) # Very short pause

# 3. The "WILL" note
# A higher-pitched note with a distinct trill (vibrato)
vibrato = (VIBRATO_RATE, VIBRATO_DEPTH)
wav_data.extend(generate_tone(WILL_FREQ_BASE, WILL_DUR, AMPLITUDE * 1.2, vibrato_params=vibrato))

# End with another long pause
wav_data.extend(generate_silence(PAUSE_LONG))

# --- Write the .wav file ---
with wave.open(FILENAME, 'wb') as wav_file:
    wav_file.setnchannels(1)
    wav_file.setsampwidth(2)
    wav_file.setframerate(int(SAMPLE_RATE))
    wav_file.writeframes(wav_data)

print("Synthesis complete.")