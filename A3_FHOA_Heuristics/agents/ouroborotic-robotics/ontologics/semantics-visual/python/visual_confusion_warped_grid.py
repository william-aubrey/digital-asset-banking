import math
import random
from PIL import Image, ImageDraw

# --- Image Parameters ---
FILENAME = "visual_confusion_warped_grid.png"
IMG_WIDTH, IMG_HEIGHT = 1200, 1200
BACKGROUND_COLOR = (20, 20, 30)
LINE_COLOR = (220, 230, 255) 
LINE_WIDTH = 2

# --- Grid and Distortion Parameters ---
GRID_SIZE = 40
DISTORTION_STRENGTH = 120.0

# --- Noise Generation ---
NOISE_GRID_SIZE = 8
noise_grid = []
for _ in range(NOISE_GRID_SIZE * NOISE_GRID_SIZE):
    angle = random.uniform(0, 2 * math.pi)
    noise_grid.append((math.cos(angle), math.sin(angle)))

def smoothstep(t):
    """A smoothing function for interpolation."""
    return t * t * (3 - 2 * t)

def get_noise(x, y):
    """
    REWRITTEN noise function that correctly handles tiling/wrapping coordinates
    to prevent all out-of-bounds errors.
    """
    # Integer coordinates of the grid cell
    x0_raw, y0_raw = int(x), int(y)
    
    # Fractional coordinates within the cell
    xf, yf = x - x0_raw, y - y0_raw
    
    # Wrap the integer coordinates to ensure they are always valid indices
    x0 = x0_raw % NOISE_GRID_SIZE
    y0 = y0_raw % NOISE_GRID_SIZE
    x1 = (x0 + 1) % NOISE_GRID_SIZE
    y1 = (y0 + 1) % NOISE_GRID_SIZE

    # Smoothed fractional coordinates for interpolation
    tx, ty = smoothstep(xf), smoothstep(yf)

    # Get gradient vectors from the four corners of the cell using wrapped indices
    v00 = noise_grid[y0 * NOISE_GRID_SIZE + x0]
    v10 = noise_grid[y0 * NOISE_GRID_SIZE + x1]
    v01 = noise_grid[y1 * NOISE_GRID_SIZE + x0]
    v11 = noise_grid[y1 * NOISE_GRID_SIZE + x1]
    
    # Compute dot products with vectors from the point to each corner
    dp00 = v00[0] * xf + v00[1] * yf
    dp10 = v10[0] * (xf - 1) + v10[1] * yf
    dp01 = v01[0] * xf + v01[1] * (yf - 1)
    dp11 = v11[0] * (xf - 1) + v11[1] * (yf - 1)

    # Bilinear interpolation
    ix1 = dp00 + tx * (dp10 - dp00)
    ix2 = dp01 + tx * (dp11 - dp01)
    return ix1 + ty * (ix2 - ix1)

# --- Main Execution ---
if __name__ == "__main__":
    print("Generating the 'Warped Grid' visualization into '" + FILENAME + "'...")

    image = Image.new("RGB", (IMG_WIDTH, IMG_HEIGHT), BACKGROUND_COLOR)
    draw = ImageDraw.Draw(image)

    points = []
    for y_idx in range(GRID_SIZE + 1):
        row = []
        for x_idx in range(GRID_SIZE + 1):
            norm_x = x_idx / GRID_SIZE
            norm_y = y_idx / GRID_SIZE
            px = norm_x * IMG_WIDTH
            py = norm_y * IMG_HEIGHT
            
            # Sample from different parts of the infinite, tiling noise field
            offset_x = get_noise(norm_x * 5, norm_y * 5) * DISTORTION_STRENGTH
            offset_y = get_noise(norm_x * 5 + 5.2, norm_y * 5 + 1.3) * DISTORTION_STRENGTH
            
            row.append((px + offset_x, py + offset_y))
        points.append(row)

    print("Warping grid and drawing...")
    for y_idx in range(GRID_SIZE):
        for x_idx in range(GRID_SIZE):
            p1 = points[y_idx][x_idx]
            p2 = points[y_idx][x_idx+1]
            p3 = points[y_idx+1][x_idx]
            
            if x_idx < GRID_SIZE:
                draw.line([p1, p2], fill=LINE_COLOR, width=LINE_WIDTH)
            if y_idx < GRID_SIZE:
                draw.line([p1, p3], fill=LINE_COLOR, width=LINE_WIDTH)

    image.save(FILENAME)
    print("Generation complete.")