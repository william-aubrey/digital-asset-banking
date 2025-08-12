import wave
import struct
import math

# --- Parameters ---
FILENAME = "inquiry_excited_long_form.wav"
SAMPLE_RATE = 44100
AMPLITUDE = 22000.0

# --- Composition ---
# A bright, ascending C-Major arpeggio to convey excitement
FREQ_1 = 523.25  # C5
FREQ_2 = 659.26  # E5
FREQ_3 = 783.99  # G5
FREQ_4 = 1046.50 # C6

# A rapid tempo with a final, sustained note to create anticipation
NOTE_DURATION_FAST = 0.12 # seconds
NOTE_DURATION_SUSTAIN = 0.4 # seconds
PAUSE_DURATION = 0.04     # seconds

def generate_mellow_tone(freq, duration, amp):
    """
    Generates byte data for a sine wave with a soft volume envelope.
    (Unchanged from previous versions)
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
print(f"Generating the 'Excited Inquiry' emote into '{FILENAME}'...")

# The ascending arpeggio phrase
wav_data = generate_mellow_tone(FREQ_1, NOTE_DURATION_FAST, AMPLITUDE)
wav_data.extend(generate_silence(PAUSE_DURATION))
wav_data.extend(generate_mellow_tone(FREQ_2, NOTE_DURATION_FAST, AMPLITUDE))
wav_data.extend(generate_silence(PAUSE_DURATION))
wav_data.extend(generate_mellow_tone(FREQ_3, NOTE_DURATION_FAST, AMPLITUDE))
wav_data.extend(generate_silence(PAUSE_DURATION))
wav_data.extend(generate_mellow_tone(FREQ_4, NOTE_DURATION_SUSTAIN, AMPLITUDE))

# --- Write the .wav file ---
with wave.open(FILENAME, 'wb') as wav_file:
    wav_file.setnchannels(1)
    wav_file.setsampwidth(2)
    wav_file.setframerate(int(SAMPLE_RATE))
    wav_file.writeframes(wav_data)

print("Synthesis complete.")