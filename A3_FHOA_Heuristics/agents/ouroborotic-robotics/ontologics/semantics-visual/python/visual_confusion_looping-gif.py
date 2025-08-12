import math
import random
from PIL import Image, ImageDraw

# --- Image Parameters ---
FILENAME = "visual_confusion_looping.gif"
IMG_WIDTH, IMG_HEIGHT = 600, 600
BACKGROUND_COLOR = (20, 20, 30)
LINE_COLOR = (220, 230, 255)
LINE_WIDTH = 2

# --- Animation Parameters ---
NUM_FRAMES = 60
BLEND_FRAMES = 20 # Number of frames at the end to use for the crossfade back to the start
FRAME_DURATION_MS = 60

# --- Grid and Distortion Parameters ---
GRID_SIZE = 30
DISTORTION_STRENGTH = 60.0

# --- 3D Noise Generation (Unchanged) ---
NOISE_GRID_SIZE = 5
noise_grid = []
for _ in range(NOISE_GRID_SIZE ** 3):
    angle1, angle2 = random.uniform(0, 2 * math.pi), random.uniform(0, 2 * math.pi)
    x = math.sin(angle1) * math.cos(angle2)
    y = math.sin(angle1) * math.sin(angle2)
    z = math.cos(angle1)
    noise_grid.append((x, y, z))

def smoothstep(t):
    return t * t * (3 - 2 * t)

def get_noise_3d(x, y, z):
    """Gets a smooth noise value from a 3D field."""
    gs = NOISE_GRID_SIZE
    # ... (Rest of the noise function is the same as the previous non-looping version)
    x0, y0, z0 = int(x), int(y), int(z)
    xf, yf, zf = x - x0, y - y0, z - z0
    x0, y0, z0 = x0 % gs, y0 % gs, z0 % gs
    x1, y1, z1 = (x0 + 1) % gs, (y0 + 1) % gs, (z0 + 1) % gs
    tx, ty, tz = smoothstep(xf), smoothstep(yf), smoothstep(zf)
    vectors = []
    for k in [y0, y1]:
        for j in [z0, z1]:
            for i in [x0, x1]:
                vectors.append(noise_grid[k * gs * gs + j * gs + i])
    ix1 = vectors[0][0]*xf + vectors[0][1]*yf + vectors[0][2]*zf
    ix2 = vectors[1][0]*(xf-1) + vectors[1][1]*yf + vectors[1][2]*zf
    iy1 = ix1 + tx * (ix2 - ix1)
    ix1 = vectors[2][0]*xf + vectors[2][1]*(yf-1) + vectors[2][2]*zf
    ix2 = vectors[3][0]*(xf-1) + vectors[3][1]*(yf-1) + vectors[3][2]*zf
    iy2 = ix1 + tx * (ix2 - ix1)
    return iy1 + ty * (iy2 - iy1)

# --- Main Execution ---
if __name__ == "__main__":
    print(f"Generating {NUM_FRAMES} frames for looping GIF '{FILENAME}'...")
    frames = []

    for frame_num in range(NUM_FRAMES):
        print(f"  - Rendering frame {frame_num + 1}/{NUM_FRAMES}")
        image = Image.new("RGB", (IMG_WIDTH, IMG_HEIGHT), BACKGROUND_COLOR)
        draw = ImageDraw.Draw(image)
        
        time_z_current = frame_num / NUM_FRAMES

        points = []
        for y_idx in range(GRID_SIZE + 1):
            row = []
            for x_idx in range(GRID_SIZE + 1):
                norm_x = x_idx / GRID_SIZE
                norm_y = y_idx / GRID_SIZE
                px = norm_x * IMG_WIDTH
                py = norm_y * IMG_HEIGHT
                
                offset_x = get_noise_3d(norm_x * 2, norm_y * 2, time_z_current) * DISTORTION_STRENGTH
                offset_y = get_noise_3d(norm_x * 2 + 5.2, norm_y * 2 + 1.3, time_z_current) * DISTORTION_STRENGTH

                # --- SEAMLESS LOOP LOGIC ---
                if frame_num >= NUM_FRAMES - BLEND_FRAMES:
                    # Calculate the blend ratio (from 0.0 to 1.0)
                    blend_ratio = (frame_num - (NUM_FRAMES - BLEND_FRAMES)) / BLEND_FRAMES
                    blend_ratio = smoothstep(blend_ratio) # Smooth the blend

                    # Also calculate the offsets for the very first frame (time_z = 0)
                    offset_x_start = get_noise_3d(norm_x * 2, norm_y * 2, 0) * DISTORTION_STRENGTH
                    offset_y_start = get_noise_3d(norm_x * 2 + 5.2, norm_y * 2 + 1.3, 0) * DISTORTION_STRENGTH
                    
                    # Interpolate between the current offsets and the start offsets
                    offset_x = offset_x * (1 - blend_ratio) + offset_x_start * blend_ratio
                    offset_y = offset_y * (1 - blend_ratio) + offset_y_start * blend_ratio

                row.append((px + offset_x, py + offset_y))
            points.append(row)

        for y_idx in range(GRID_SIZE):
            for x_idx in range(GRID_SIZE):
                p1, p2, p3 = points[y_idx][x_idx], points[y_idx][x_idx+1], points[y_idx+1][x_idx]
                draw.line([p1, p2], fill=LINE_COLOR, width=LINE_WIDTH)
                draw.line([p1, p3], fill=LINE_COLOR, width=LINE_WIDTH)
        
        frames.append(image)

    print(f"Saving frames to '{FILENAME}'...")
    frames[0].save(
        FILENAME,
        save_all=True,
        append_images=frames[1:],
        duration=FRAME_DURATION_MS,
        loop=0
    )
    print("Generation complete.")