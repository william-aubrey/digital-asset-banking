import wave
import struct
import math

# --- Parameters ---
FILENAME = "chuck_wills_widow_rock.wav"
SAMPLE_RATE = 44100
AMPLITUDE = 24000.0

# --- Composition ---
# A i-iv-v chord progression in A minor. Each root note is the base for one call.
CHORD_PROGRESSION = [
    220.00, # A3 (i)
    293.66, # D4 (iv)
    329.63  # E4 (v)
]

# Durations are kept consistent
CHUCK_DUR = 0.08
WILLS_DUR = 0.15
WID_DUR = 0.20
OW_DUR = 0.25
PAUSE_DUR = 0.05
PAUSE_BETWEEN_CALLS = 0.6

def generate_soft_tone(freq, duration, amp):
    """
    REVISED function with a soft sine-based envelope to prevent pops/clicks.
    """
    num_samples = int(duration * SAMPLE_RATE)
    byte_data = bytearray()
    for i in range(num_samples):
        value = math.sin(2 * math.pi * freq * (i / SAMPLE_RATE))
        
        # This new envelope swells up and down, ensuring no abrupt start/end
        progress = i / num_samples
        envelope = math.sin(progress * math.pi)

        packed_value = struct.pack('h', int(value * envelope * amp))
        byte_data.extend(packed_value)
    return byte_data

def generate_soft_glide(start_freq, end_freq, duration, amp):
    """
    REVISED glide function with the new soft envelope.
    """
    num_samples = int(duration * SAMPLE_RATE)
    byte_data = bytearray()
    for i in range(num_samples):
        progress = i / num_samples
        current_freq = start_freq + (end_freq - start_freq) * progress
        value = math.sin(2 * math.pi * current_freq * (i / SAMPLE_RATE))
        
        envelope = math.sin(progress * math.pi)
        
        packed_value = struct.pack('h', int(value * envelope * amp))
        byte_data.extend(packed_value)
    return byte_data

def generate_silence(duration):
    """Generates byte data for silence."""
    num_samples = int(duration * SAMPLE_RATE)
    return bytearray(num_samples * 2)

# --- Main Synthesis ---
print(f"Generating the 'Rock and Roll' Chuck-will's-widow into '{FILENAME}'...")

final_wav_data = bytearray()

for root_note in CHORD_PROGRESSION:
    print(f"Generating call in the key of {int(root_note)} Hz...")
    
    # Define the notes of the call relative to the current chord's root note
    # Using musical ratios: 1=root, 1.25=major third, 1.33=perfect fourth, 1.5=perfect fifth
    chuck_freq = root_note * 0.8
    wills_start = root_note * 1.0
    wills_end = root_note * 1.25
    wid_freq = root_note * 1.33
    ow_start = root_note * 1.25
    ow_end = root_note * 1.0
    
    # --- Assemble one full call in the current key ---
    final_wav_data.extend(generate_soft_tone(chuck_freq, CHUCK_DUR, AMPLITUDE * 0.4))
    final_wav_data.extend(generate_silence(PAUSE_DUR))
    final_wav_data.extend(generate_soft_glide(wills_start, wills_end, WILLS_DUR, AMPLITUDE * 0.9))
    final_wav_data.extend(generate_silence(0.01))
    final_wav_data.extend(generate_soft_tone(wid_freq, WID_DUR, AMPLITUDE))
    final_wav_data.extend(generate_silence(0.01))
    final_wav_data.extend(generate_soft_glide(ow_start, ow_end, OW_DUR, AMPLITUDE * 0.9))
    final_wav_data.extend(generate_silence(PAUSE_BETWEEN_CALLS))

# --- Write the final .wav file ---
with wave.open(FILENAME, 'wb') as wav_file:
    wav_file.setnchannels(1)
    wav_file.setsampwidth(2)
    wav_file.setframerate(int(SAMPLE_RATE))
    wav_file.writeframes(final_wav_data)

print("Synthesis complete.")