import wave
import math
import struct

# --- Parameters ---
FILENAME = "thinking_long_form.wav"
DURATION = 10  # seconds
SAMPLE_RATE = 44100.0
AMPLITUDE_TICK = 12000.0 # Loudness of the main "tick"
AMPLITUDE_TOCK = 8000.0  # Loudness of the secondary "tock"
AMPLITUDE_HUM = 500.0    # Loudness of the background hum

# --- Composition ---
BPM = 150.0  # Beats per minute for the clock ticks
BEAT_INTERVAL_SAMPLES = int(SAMPLE_RATE * 60.0 / BPM)
CLICK_DURATION_SAMPLES = 200 # How long each click lasts

FREQ_TICK = 1200.0 # Pitch of the "tick"
FREQ_TOCK = 900.0  # Pitch of the "tock"
FREQ_HUM = 50.0    # Pitch of the background hum

# --- Generate Waveform ---
wav_data = bytearray()
num_samples = int(DURATION * SAMPLE_RATE)

for t in range(num_samples):
    # 1. Calculate the base background hum (a continuous sine wave)
    hum_val = math.sin(2 * math.pi * FREQ_HUM * (t / SAMPLE_RATE)) * AMPLITUDE_HUM

    # 2. Determine if a click should happen at this sample
    click_val = 0.0
    time_since_beat = t % BEAT_INTERVAL_SAMPLES
    
    if time_since_beat < CLICK_DURATION_SAMPLES:
        # Determine if it's a "tick" (even beat) or a "tock" (odd beat)
        current_beat = t // BEAT_INTERVAL_SAMPLES
        if current_beat % 2 == 0:
            # It's a "Tick"
            # Use a square wave for a sharp, digital sound
            click_val = 1 if (time_since_beat % 10 < 5) else -1
            click_val *= AMPLITUDE_TICK
        else:
            # It's a "Tock"
            click_val = 1 if (time_since_beat % 12 < 6) else -1
            click_val *= AMPLITUDE_TOCK
            
    # 3. Combine the hum and the click for the final sample
    final_value = hum_val + click_val
    
    # Pack and append the sample
    packed_value = struct.pack('h', int(final_value))
    wav_data.extend(packed_value)

# --- Write the .wav file ---
print(f"Generating '{FILENAME}'...")
with wave.open(FILENAME, 'wb') as wav_file:
    wav_file.setnchannels(1)
    wav_file.setsampwidth(2)
    wav_file.setframerate(int(SAMPLE_RATE))
    wav_file.writeframes(wav_data)

print("Process complete.")