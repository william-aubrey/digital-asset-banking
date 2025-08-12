import wave
import struct
import math

# --- Parameters ---
FILENAME = "warning_critical_long_form.wav"
SAMPLE_RATE = 44100

# --- Amplitudes ---
SINE_AMP = 18000.0  # The primary "mellow" sine wave
SAW_AMP = 3000.0   # The secondary "critical edge" sawtooth wave

# --- Composition ---
# A dissonant tritone interval (C4 and F#4) to create tension and urgency
FREQ_1 = 261.63  # C4
FREQ_2 = 369.99  # F#4 (Tritone)

# A rapid triplet rhythm
NOTE_DURATION = 0.15   # seconds for each note
PAUSE_DURATION = 0.07  # A very short pause between notes

def generate_critical_tone(f1, f2, duration, sine_amp, saw_amp):
    """
    Generates a complex tone by layering a sine wave and a sawtooth wave.
    The soft envelope is preserved.
    """
    num_samples = int(duration * SAMPLE_RATE)
    byte_data = bytearray()
    
    period1 = SAMPLE_RATE / f1
    period2 = SAMPLE_RATE / f2
    
    for i in range(num_samples):
        # Sine wave components for the "mellow" body
        sine_val = math.sin(2 * math.pi * f1 * (i / SAMPLE_RATE)) + \
                   math.sin(2 * math.pi * f2 * (i / SAMPLE_RATE))
        
        # Sawtooth components for the "critical edge"
        saw_val1 = ((i % period1) / period1) * 2 - 1
        saw_val2 = ((i % period2) / period2) * 2 - 1
        saw_val = saw_val1 + saw_val2
        
        # Volume envelope for the soft attack/decay
        progress = i / num_samples
        envelope = math.sin(progress * math.pi)
        
        # Combine all components
        final_value = (sine_val * sine_amp + saw_val * saw_amp) * envelope / 2 # Divide by 2 to average the two notes
        
        packed_value = struct.pack('h', int(final_value))
        byte_data.extend(packed_value)
        
    return byte_data

def generate_silence(duration):
    """Generates byte data for silence."""
    num_samples = int(duration * SAMPLE_RATE)
    return bytearray(num_samples * 2)

# --- Main Synthesis ---
print(f"Generating the 'Friendly Critical Warning' emote into '{FILENAME}'...")

# The rapid three-note phrase
wav_data = generate_critical_tone(FREQ_1, FREQ_2, NOTE_DURATION, SINE_AMP, SAW_AMP)
wav_data.extend(generate_silence(PAUSE_DURATION))
wav_data.extend(generate_critical_tone(FREQ_1, FREQ_2, NOTE_DURATION, SINE_AMP, SAW_AMP))
wav_data.extend(generate_silence(PAUSE_DURATION))
wav_data.extend(generate_critical_tone(FREQ_1, FREQ_2, NOTE_DURATION, SINE_AMP, SAW_AMP))

# --- Write the .wav file ---
with wave.open(FILENAME, 'wb') as wav_file:
    wav_file.setnchannels(1)
    wav_file.setsampwidth(2)
    wav_file.setframerate(int(SAMPLE_RATE))
    wav_file.writeframes(wav_data)

print("Synthesis complete.")