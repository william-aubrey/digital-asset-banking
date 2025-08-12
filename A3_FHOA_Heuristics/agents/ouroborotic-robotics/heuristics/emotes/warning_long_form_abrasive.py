import wave
import struct
import math

# --- Parameters ---
FILENAME = "warning_long_form.wav"
SAMPLE_RATE = 44100
AMPLITUDE = 18000.0

# --- Composition ---
TONE_DURATION = 0.7  # seconds for each "long" beep
PAUSE_DURATION = 0.25 # seconds of silence between beeps
FREQUENCY = 880.0    # A5 note, a common alert pitch

def generate_square_wave(freq, duration, amp):
    """Generates byte data for a square wave of a given frequency and duration."""
    num_samples = int(duration * SAMPLE_RATE)
    period_in_samples = SAMPLE_RATE / freq
    byte_data = bytearray()
    
    for i in range(num_samples):
        # The core of a square wave: one value for the first half of the period,
        # and the opposite value for the second half.
        if (i % period_in_samples) < (period_in_samples / 2):
            value = amp
        else:
            value = -amp
        
        packed_value = struct.pack('h', int(value))
        byte_data.extend(packed_value)
        
    return byte_data

def generate_silence(duration):
    """Generates byte data for silence."""
    num_samples = int(duration * SAMPLE_RATE)
    return bytearray(num_samples * 2) # 2 bytes per sample for 16-bit audio

# --- Main Synthesis ---
print(f"Generating the 'Warning' emote into '{FILENAME}'...")

# 1. First tone
wav_data = generate_square_wave(FREQUENCY, TONE_DURATION, AMPLITUDE)

# 2. Pause
wav_data.extend(generate_silence(PAUSE_DURATION))

# 3. Second tone
wav_data.extend(generate_square_wave(FREQUENCY, TONE_DURATION, AMPLITUDE))

# --- Write the .wav file ---
with wave.open(FILENAME, 'wb') as wav_file:
    wav_file.setnchannels(1)
    wav_file.setsampwidth(2)
    wav_file.setframerate(int(SAMPLE_RATE))
    wav_file.writeframes(wav_data)

print("Synthesis complete.")