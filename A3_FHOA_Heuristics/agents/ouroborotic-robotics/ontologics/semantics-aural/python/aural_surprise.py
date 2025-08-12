import wave
import struct
import math

# --- Parameters ---
FILENAME = "aural_surprise.wav"
DURATION = 1.0
SAMPLE_RATE = 44100
AMPLITUDE = 22000.0

# --- Composition ---
START_FREQ = 600.0
END_FREQ = 1600.0

VIBRATO_START_TIME = 0.75
VIBRATO_DEPTH = 20.0
VIBRATO_RATE = 20.0

# --- Main Synthesis ---
if __name__ == "__main__":
    print(f"Generating the corrected 'Surprise' aural emote into '{FILENAME}'...")
    num_samples = int(DURATION * SAMPLE_RATE)
    wav_data = bytearray()

    # --- CORRECTED LOGIC USING PHASE ACCUMULATION ---
    phase = 0.0 # Initialize phase to zero

    for i in range(num_samples):
        progress = i / num_samples
        
        # 1. Calculate the instantaneous frequency for this exact moment
        current_freq = START_FREQ + (END_FREQ - START_FREQ) * progress
        
        if progress > VIBRATO_START_TIME:
            vibrato_progress = (progress - VIBRATO_START_TIME) / (1 - VIBRATO_START_TIME)
            vibrato = math.sin(2 * math.pi * VIBRATO_RATE * vibrato_progress) * VIBRATO_DEPTH
            current_freq += vibrato

        # 2. Calculate the sample's value using the current accumulated phase
        value = math.sin(phase)
        
        # 3. Increment the phase for the *next* sample based on the current frequency
        phase += 2 * math.pi * current_freq / SAMPLE_RATE
        
        # Apply a soft envelope over the whole sound
        envelope = math.sin(progress * math.pi)
        
        packed_value = struct.pack('h', int(value * envelope * AMPLITUDE))
        wav_data.extend(packed_value)

    # Write the .wav file
    with wave.open(FILENAME, 'wb') as wav_file:
        wav_file.setnchannels(1)
        wav_file.setsampwidth(2)
        wav_file.setframerate(int(SAMPLE_RATE))
        wav_file.writeframes(wav_data)

    print("Aural emote generation complete.")