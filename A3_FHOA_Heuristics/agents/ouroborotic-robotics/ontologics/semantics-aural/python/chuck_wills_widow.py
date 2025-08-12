import wave
import struct
import math

# --- Parameters ---
FILENAME = "chuck_wills_widow_soft.py"
SAMPLE_RATE = 44100
AMPLITUDE = 24000.0

# --- Composition ---
# The original note parameters for a single call
CHUCK_DUR = 0.08
WILLS_DUR = 0.15
WID_DUR = 0.20
OW_DUR = 0.25
PAUSE_DUR = 0.05

CHUCK_FREQ = 180.0
WILLS_START_FREQ = 440.0 # A4
WILLS_END_FREQ = 523.0   # C5
WID_FREQ = 587.0         # D5
OW_START_FREQ = 523.0    # C5
OW_END_FREQ = 440.0      # A4

def generate_soft_tone(freq, duration, amp):
    """
    The revised function with a soft sine-based envelope to prevent pops/clicks.
    """
    num_samples = int(duration * SAMPLE_RATE)
    byte_data = bytearray()
    for i in range(num_samples):
        value = math.sin(2 * math.pi * freq * (i / SAMPLE_RATE))
        progress = i / num_samples
        envelope = math.sin(progress * math.pi) # Soft attack and decay
        packed_value = struct.pack('h', int(value * envelope * amp))
        byte_data.extend(packed_value)
    return byte_data

def generate_soft_glide(start_freq, end_freq, duration, amp):
    """
    The revised glide function with the new soft envelope.
    """
    num_samples = int(duration * SAMPLE_RATE)
    byte_data = bytearray()
    for i in range(num_samples):
        progress = i / num_samples
        current_freq = start_freq + (end_freq - start_freq) * progress
        value = math.sin(2 * math.pi * current_freq * (i / SAMPLE_RATE))
        envelope = math.sin(progress * math.pi) # Soft attack and decay
        packed_value = struct.pack('h', int(value * envelope * amp))
        byte_data.extend(packed_value)
    return byte_data

def generate_silence(duration):
    """Generates byte data for silence."""
    num_samples = int(duration * SAMPLE_RATE)
    return bytearray(num_samples * 2)

# --- Main Synthesis ---
print(f"Generating the soft-edged Chuck-will's-widow into '{FILENAME}'...")

final_wav_data = bytearray()

# Assemble the original four-syllable call using the improved functions
final_wav_data.extend(generate_soft_tone(CHUCK_FREQ, CHUCK_DUR, AMPLITUDE * 0.4))
final_wav_data.extend(generate_silence(PAUSE_DUR))
final_wav_data.extend(generate_soft_glide(WILLS_START_FREQ, WILLS_END_FREQ, WILLS_DUR, AMPLITUDE * 0.9))
final_wav_data.extend(generate_silence(0.01))
final_wav_data.extend(generate_soft_tone(WID_FREQ, WID_DUR, AMPLITUDE))
final_wav_data.extend(generate_silence(0.01))
final_wav_data.extend(generate_soft_glide(OW_START_FREQ, OW_END_FREQ, OW_DUR, AMPLITUDE * 0.9))

# --- Write the final .wav file ---
with wave.open(FILENAME, 'wb') as wav_file:
    wav_file.setnchannels(1)
    wav_file.setsampwidth(2)
    wav_file.setframerate(int(SAMPLE_RATE))
    wav_file.writeframes(final_wav_data)

print("Synthesis complete.")