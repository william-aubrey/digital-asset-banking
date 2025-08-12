import wave
import struct
import random
import math

# --- Parameters ---
FILENAME = "page_turn_long_form_v2.wav"
DURATION = 1.5  # seconds, providing space for the sound to exist
SAMPLE_RATE = 44100
MASTER_AMPLITUDE = 28000.0

# --- Sound Event Timing (in samples) ---
# Total samples in the file
total_samples = int(DURATION * SAMPLE_RATE)
# Act 1: The Lift
lift_start = int(0.2 * SAMPLE_RATE)
lift_end = int(0.4 * SAMPLE_RATE)
# Act 2: The Release (the "zip")
release_start = lift_end
release_end = int(0.85 * SAMPLE_RATE)
# Act 3: The Settle
settle_start = release_end
settle_end = int(1.0 * SAMPLE_RATE)

# --- Synthesis ---
# Using 2 channels for stereo to simulate movement
n_channels = 2
sampwidth = 2
wav_data = bytearray()

# Leaky integrators for a more natural "pinkish" noise
# This prevents the raw noise from sounding too electronic
prev_noise_l, prev_noise_r = 0.0, 0.0

print(f"Synthesizing the sound of a page turning into '{FILENAME}'...")

for t in range(total_samples):
    # Default amplitude is zero (silence)
    amp_l, amp_r = 0.0, 0.0

    # Generate the noise source
    # A simple low-pass filter on white noise to make it sound more natural
    raw_noise = random.uniform(-1.0, 1.0)
    filtered_noise = (prev_noise_l * 0.6) + (raw_noise * 0.4)
    prev_noise_l = filtered_noise
    
    # --- Amplitude Envelope: The Three-Act Structure ---
    
    # Act 1: The Lift - A gentle swell, slightly on the right
    if lift_start <= t < lift_end:
        progress = (t - lift_start) / (lift_end - lift_start)
        amp_r = math.sin(progress * math.pi) * 0.2 # A gentle sine-based swell
        amp_l = amp_r * 0.7 # Quieter on the left

    # Act 2: The Release - The sharp, moving "zip"
    elif release_start <= t < release_end:
        progress = (t - release_start) / (release_end - release_start)
        # Main crisp sound with a fast decay
        main_amp = (1.0 - progress) ** 2.5 
        # Panning: Start loud on the right, end loud on the left
        amp_r = main_amp * (1 - progress)
        amp_l = main_amp * progress

    # Act 3: The Settle - A final soft thump, mostly on the left
    elif settle_start <= t < settle_end:
        progress = (t - settle_start) / (settle_end - settle_start)
        amp_l = math.sin(progress * math.pi) * 0.25 # A final soft swell
        amp_r = amp_l * 0.7

    # --- Final Sample Calculation ---
    # Combine the noise source with the calculated amplitude for each channel
    val_l = filtered_noise * amp_l * MASTER_AMPLITUDE
    val_r = filtered_noise * amp_r * MASTER_AMPLITUDE

    # Pack the stereo samples and append to the byte array
    # '<hh' means 2 little-endian short integers
    packed_value = struct.pack('<hh', int(val_l), int(val_r))
    wav_data.extend(packed_value)


# --- Write the .wav file ---
with wave.open(FILENAME, 'wb') as wav_file:
    wav_file.setnchannels(n_channels)
    wav_file.setsampwidth(sampwidth)
    wav_file.setframerate(int(SAMPLE_RATE))
    wav_file.writeframes(wav_data)

print("Synthesis complete.")