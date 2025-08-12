import wave
import struct
import math

# --- Parameters ---
FILENAME = "aural_surprise_doubletake.wav"
SAMPLE_RATE = 44100
AMPLITUDE = 22000.0

# --- Composition ---
PAUSE_DURATION = 0.1 # seconds

def generate_surprise_phrase(duration, start_freq, end_freq, vibrato_params):
    """A generalized function to create a surprise chirp with specified vibrato."""
    num_samples = int(duration * SAMPLE_RATE)
    byte_data = bytearray()
    phase = 0.0
    
    # Unpack vibrato parameters
    v_start_time, v_depth, v_rate, v_waveform = vibrato_params

    for i in range(num_samples):
        progress = i / num_samples
        
        # Calculate the instantaneous frequency for the glide
        current_freq = start_freq + (end_freq - start_freq) * progress
        
        # Apply vibrato at the end of the note
        if progress > v_start_time:
            vibrato = 0.0
            time_in_vibrato = (i - v_start_time * num_samples) / SAMPLE_RATE
            
            if v_waveform == 'sine':
                vibrato = math.sin(2 * math.pi * v_rate * time_in_vibrato) * v_depth
            elif v_waveform == 'square':
                if (time_in_vibrato * v_rate) % 1.0 < 0.5:
                    vibrato = v_depth
                else:
                    vibrato = -v_depth
            current_freq += vibrato

        # Calculate sample value using accumulated phase
        value = math.sin(phase)
        phase += 2 * math.pi * current_freq / SAMPLE_RATE
        
        # Apply envelope
        envelope = math.sin(progress * math.pi)
        
        packed_value = struct.pack('h', int(value * envelope * AMPLITUDE))
        byte_data.extend(packed_value)
        
    return byte_data

def generate_silence(duration):
    """Generates byte data for silence."""
    num_samples = int(duration * SAMPLE_RATE)
    return bytearray(num_samples * 2)

# --- Main Synthesis ---
if __name__ == "__main__":
    print(f"Generating the 'Double-Take Surprise' emote into '{FILENAME}'...")

    # Phrase 1: The gentle "What?" using a sine wave vibrato
    gentle_vibrato = (0.75, 20.0, 20.0, 'sine')
    phrase1_data = generate_surprise_phrase(0.5, 600.0, 1400.0, gentle_vibrato)
    
    # A short pause
    pause_data = generate_silence(PAUSE_DURATION)

    # Phrase 2: The heightened "WHAT?!?!" using a square wave vibrato
    heightened_vibrato = (0.75, 50.0, 40.0, 'square')
    phrase2_data = generate_surprise_phrase(0.6, 700.0, 1800.0, heightened_vibrato)

    # Concatenate all parts
    final_wav_data = phrase1_data + pause_data + phrase2_data

    # Write the final .wav file
    with wave.open(FILENAME, 'wb') as wav_file:
        wav_file.setnchannels(1)
        wav_file.setsampwidth(2)
        # --- CORRECTED LINE ---
        # Added the missing command to set the sample rate
        wav_file.setframerate(SAMPLE_RATE)
        wav_file.writeframes(final_wav_data)

    print("Aural emote generation complete.")