import wave
import struct
import math

# --- Parameters ---
FILENAME = "warning_urgent_long_form.wav"
SAMPLE_RATE = 44100
AMPLITUDE = 22000.0

# --- Composition ---
# A descending pattern to create a feeling of insistence rather than pleasantness.
FREQ_1 = 329.63  # E4
FREQ_2 = 277.18  # C#4
FREQ_3 = 220.00  # A3

# Faster tempo to increase urgency
NOTE_DURATION_FAST = 0.20  # seconds for the first two notes
NOTE_DURATION_SLOW = 0.35  # seconds for the final, declarative note
PAUSE_DURATION = 0.05      # A very short pause

def generate_mellow_tone(freq, duration, amp):
    """
    Generates byte data for a sine wave with a soft volume envelope,
    making it sound like a chime or a soft bell. (Unchanged from previous version)
    """
    num_samples = int(duration * SAMPLE_RATE)
    byte_data = bytearray()
    
    for i in range(num_samples):
        sine_value = math.sin(2 * math.pi * freq * (i / SAMPLE_RATE))
        progress = i / num_samples
        envelope = math.sin(progress * math.pi)
        value = sine_value * envelope * amp
        
        packed_value = struct.pack('h', int(value))
        byte_data.extend(packed_value)
        
    return byte_data

def generate_silence(duration):
    """Generates byte data for silence."""
    num_samples = int(duration * SAMPLE_RATE)
    return bytearray(num_samples * 2)

# --- Main Synthesis ---
print(f"Generating the 'Urgent Mellow Warning' emote into '{FILENAME}'...")

# The three-note phrase
wav_data = generate_mellow_tone(FREQ_1, NOTE_DURATION_FAST, AMPLITUDE)
wav_data.extend(generate_silence(PAUSE_DURATION))
wav_data.extend(generate_mellow_tone(FREQ_2, NOTE_DURATION_FAST, AMPLITUDE))
wav_data.extend(generate_silence(PAUSE_DURATION))
wav_data.extend(generate_mellow_tone(FREQ_3, NOTE_DURATION_SLOW, AMPLITUDE))


# --- Write the .wav file ---
with wave.open(FILENAME, 'wb') as wav_file:
    wav_file.setnchannels(1)
    wav_file.setsampwidth(2)
    wav_file.setframerate(int(SAMPLE_RATE))
    wav_file.writeframes(wav_data)

print("Synthesis complete.")