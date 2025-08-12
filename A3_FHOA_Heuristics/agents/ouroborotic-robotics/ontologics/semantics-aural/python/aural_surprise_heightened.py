import wave
import struct
import math

# --- Parameters ---
FILENAME = "aural_surprise_heightened.wav"
DURATION = 1.0
SAMPLE_RATE = 44100
AMPLITUDE = 22000.0

# --- Composition ---
START_FREQ = 600.0
END_FREQ = 1600.0

VIBRATO_START_TIME = 0.75
# --- Heightened Vibrato Parameters ---
VIBRATO_DEPTH = 50.0  # Increased depth for a wider pitch change
VIBRATO_RATE = 40.0   # Increased rate for a faster warble

# --- Main Synthesis ---
if __name__ == "__main__":
    print(f"Generating the 'Heightened Surprise' aural emote into '{FILENAME}'...")
    num_samples = int(DURATION * SAMPLE_RATE)
    wav_data = bytearray()

    phase = 0.0

    for i in range(num_samples):
        progress = i / num_samples
        
        # 1. Calculate the instantaneous frequency
        current_freq = START_FREQ + (END_FREQ - START_FREQ) * progress
        
        if progress > VIBRATO_START_TIME:
            # --- MODIFIED VIBRATO LOGIC ---
            # Use a square wave for a sharper, more electronic trill
            time_in_vibrato = (i - VIBRATO_START_TIME * num_samples) / SAMPLE_RATE
            if (time_in_vibrato * VIBRATO_RATE) % 1.0 < 0.5:
                vibrato = VIBRATO_DEPTH
            else:
                vibrato = -VIBRATO_DEPTH
            current_freq += vibrato

        # 2. Calculate the sample's value using the current accumulated phase
        value = math.sin(phase)
        
        # 3. Increment the phase for the next sample
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