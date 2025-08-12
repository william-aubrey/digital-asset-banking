import wave
import struct
import math

# --- Parameters ---
FILENAME = "warning_mellow_long_form.wav"
SAMPLE_RATE = 44100
AMPLITUDE = 22000.0

# --- Composition ---
# Using a pleasant C-Major third interval for a "chime" effect
FREQ_1 = 261.63  # C4
FREQ_2 = 329.63  # E4

NOTE_DURATION = 0.35  # seconds for each note
PAUSE_DURATION = 0.15 # seconds of silence between notes

def generate_mellow_tone(freq, duration, amp):
    """
    Generates byte data for a sine wave with a soft volume envelope,
    making it sound like a chime or a soft bell.
    """
    num_samples = int(duration * SAMPLE_RATE)
    byte_data = bytearray()
    
    for i in range(num_samples):
        # The core sine wave for the tone's pitch
        sine_value = math.sin(2 * math.pi * freq * (i / SAMPLE_RATE))
        
        # The volume envelope: a sine function from 0 to Pi.
        # This makes the volume swell up and down smoothly, creating a soft attack and decay.
        progress = i / num_samples
        envelope = math.sin(progress * math.pi)
        
        # Combine the tone with the volume envelope
        value = sine_value * envelope * amp
        
        packed_value = struct.pack('h', int(value))
        byte_data.extend(packed_value)
        
    return byte_data

def generate_silence(duration):
    """Generates byte data for silence."""
    num_samples = int(duration * SAMPLE_RATE)
    return bytearray(num_samples * 2)

# --- Main Synthesis ---
print(f"Generating the 'Mellow Warning' emote into '{FILENAME}'...")

# 1. First tone (C4)
wav_data = generate_mellow_tone(FREQ_1, NOTE_DURATION, AMPLITUDE)

# 2. Pause
wav_data.extend(generate_silence(PAUSE_DURATION))

# 3. Second tone (E4)
wav_data.extend(generate_mellow_tone(FREQ_2, NOTE_DURATION, AMPLITUDE))

# --- Write the .wav file ---
with wave.open(FILENAME, 'wb') as wav_file:
    wav_file.setnchannels(1)
    wav_file.setsampwidth(2)
    wav_file.setframerate(int(SAMPLE_RATE))
    wav_file.writeframes(wav_data)

print("Synthesis complete.")