import wave
import struct
import math
import random

# --- Parameters ---
FILENAME = "aural_warping_reality.wav"
DURATION = 15  # seconds
SAMPLE_RATE = 44100
MASTER_AMPLITUDE = 20000.0

# --- Composition ---
# Layer 1: The steady drone representing "firm reality"
DRONE_FREQ_1 = 65.41  # C2
DRONE_FREQ_2 = 130.81 # C3 (one octave up)
DRONE_AMP = 0.2 # Relative amplitude

# Layer 2: The warbling voices representing the "stretching mind"
VOICES = [
    # (start_time, duration, start_freq, end_freq, vibrato_rate, vibrato_depth, amp)
    (1.0, 8.0, 440.0, 466.1, 4.0, 15.0, 0.3), # A4 to A#4
    (3.0, 10.0, 587.3, 554.3, 3.5, 20.0, 0.25), # D5 to C#5
    (6.0, 7.0, 329.6, 349.2, 5.0, 10.0, 0.35)  # E4 to F4
]

# --- Main Synthesis ---
if __name__ == "__main__":
    print(f"Generating the 'Warping Reality' soundscape into '{FILENAME}'...")
    num_samples = int(DURATION * SAMPLE_RATE)
    
    # Create a buffer of floating point samples for mixing
    mix_buffer = [0.0] * num_samples

    # 1. Generate the drone layer
    print("  - Layer 1: Synthesizing the 'firm reality' drone...")
    for i in range(num_samples):
        val1 = math.sin(2 * math.pi * DRONE_FREQ_1 * (i / SAMPLE_RATE))
        val2 = math.sin(2 * math.pi * DRONE_FREQ_2 * (i / SAMPLE_RATE))
        mix_buffer[i] += (val1 + val2) / 2 * DRONE_AMP

    # 2. Generate and mix the warbling voices
    print("  - Layer 2: Synthesizing the 'stretching mind' warbles...")
    for voice in VOICES:
        start_time, dur, start_f, end_f, vib_r, vib_d, amp = voice
        
        start_sample = int(start_time * SAMPLE_RATE)
        num_voice_samples = int(dur * SAMPLE_RATE)

        for i in range(num_voice_samples):
            # Ensure we don't write past the end of the buffer
            if start_sample + i >= num_samples:
                break
            
            progress = i / num_voice_samples
            
            # The base pitch slowly glides from start to end
            current_base_freq = start_f + (end_f - start_f) * progress
            
            # The vibrato "warbles" the pitch
            vibrato = math.sin(2 * math.pi * vib_r * (i / SAMPLE_RATE)) * vib_d
            current_freq = current_base_freq + vibrato
            
            # The main sine wave for the voice's tone
            value = math.sin(2 * math.pi * current_freq * (i / SAMPLE_RATE))
            
            # A soft envelope to fade the voice in and out
            envelope = math.sin(progress * math.pi)
            
            mix_buffer[start_sample + i] += value * envelope * amp

    # 3. Normalize and convert to 16-bit PCM
    print("Mixing and normalizing...")
    # Find the maximum absolute value in the mix to prevent clipping
    max_val = max(abs(s) for s in mix_buffer)
    if max_val == 0: max_val = 1.0
    
    normalization_factor = MASTER_AMPLITUDE / max_val
    
    # Write to byte array
    wav_data = bytearray()
    for sample in mix_buffer:
        scaled_sample = int(sample * normalization_factor)
        wav_data.extend(struct.pack('h', scaled_sample))

    # 4. Write the final .wav file
    print(f"Saving to '{FILENAME}'...")
    with wave.open(FILENAME, 'wb') as wav_file:
        wav_file.setnchannels(1)
        wav_file.setsampwidth(2)
        wav_file.setframerate(int(SAMPLE_RATE))
        wav_file.writeframes(wav_data)

    print("Generation complete.")