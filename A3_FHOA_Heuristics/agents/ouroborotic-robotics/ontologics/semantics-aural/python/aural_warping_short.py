import wave
import struct
import math

# --- Parameters ---
FILENAME = "aural_warping_short.wav"
DURATION = 5
SAMPLE_RATE = 44100
MASTER_AMPLITUDE = 22000.0

# --- Composition ---
DRONE_FREQ_1 = 65.41
DRONE_FREQ_2 = 130.81
DRONE_AMP = 0.25

VOICE_1_FREQ = 493.88
VOICE_2_FREQ = 523.25
VOICES_AMP = 0.35

EVENT_START_TIME = 1.0
EVENT_DURATION = 2.5
FADE_IN_TIME = 0.5
FADE_OUT_TIME = 1.0

# --- Main Synthesis ---
if __name__ == "__main__":
    print(f"Generating the short-form 'Warping Reality' into '{FILENAME}'...")
    num_samples = int(DURATION * SAMPLE_RATE)
    
    mix_buffer = [0.0] * num_samples

    # 1. Generate the continuous drone
    for i in range(num_samples):
        val1 = math.sin(2 * math.pi * DRONE_FREQ_1 * (i / SAMPLE_RATE))
        val2 = math.sin(2 * math.pi * DRONE_FREQ_2 * (i / SAMPLE_RATE))
        mix_buffer[i] += (val1 + val2) / 2 * DRONE_AMP

    # 2. Generate and mix the dissonant, warbling event
    event_start_sample = int(EVENT_START_TIME * SAMPLE_RATE)
    num_event_samples = int(EVENT_DURATION * SAMPLE_RATE)

    for i in range(num_event_samples):
        if event_start_sample + i >= num_samples:
            break
        
        progress = i / num_event_samples
        
        envelope = 0.0
        time_in_event = i / SAMPLE_RATE
        if time_in_event < FADE_IN_TIME:
            envelope = time_in_event / FADE_IN_TIME
        elif time_in_event > EVENT_DURATION - FADE_OUT_TIME:
            envelope = 1.0 - ((time_in_event - (EVENT_DURATION - FADE_OUT_TIME)) / FADE_OUT_TIME)
        else:
            envelope = 1.0
        
        vibrato1 = math.sin(2 * math.pi * 5.0 * (i / SAMPLE_RATE)) * 15.0
        vibrato2 = math.sin(2 * math.pi * 4.5 * (i / SAMPLE_RATE)) * 18.0
        
        val1 = math.sin(2 * math.pi * (VOICE_1_FREQ + vibrato1) * (i / SAMPLE_RATE))
        val2 = math.sin(2 * math.pi * (VOICE_2_FREQ + vibrato2) * (i / SAMPLE_RATE))

        mix_buffer[event_start_sample + i] += ((val1 + val2) / 2) * envelope * VOICES_AMP
        
    # 3. Normalize and convert to 16-bit PCM
    print("Mixing and normalizing...")
    # --- FIX STARTS HERE ---
    # Find the maximum absolute value for normalization
    max_abs_val = max(abs(s) for s in mix_buffer)
    # Ensure max_abs_val is at least 1.0 to prevent division by a very small number
    if max_abs_val < 1.0:
        max_abs_val = 1.0
    
    normalization_factor = MASTER_AMPLITUDE / max_abs_val
    # --- FIX ENDS HERE ---
    
    wav_data = bytearray()
    for sample in mix_buffer:
        wav_data.extend(struct.pack('h', int(sample * normalization_factor)))

    # 4. Write the final .wav file
    print(f"Saving to '{FILENAME}'...")
    with wave.open(FILENAME, 'wb') as wav_file:
        wav_file.setnchannels(1)
        wav_file.setsampwidth(2)
        wav_file.setframerate(int(SAMPLE_RATE))
        wav_file.writeframes(wav_data)

    print("Generation complete.")