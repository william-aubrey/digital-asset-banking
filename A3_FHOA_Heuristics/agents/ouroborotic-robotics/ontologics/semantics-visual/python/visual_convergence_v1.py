import math
import random
from PIL import Image, ImageDraw

# --- Image Parameters ---
FILENAME = "visual_convergence_v1.png"
IMG_WIDTH, IMG_HEIGHT = 1200, 1200
BACKGROUND_COLOR = (20, 20, 30)

# --- Simulation Parameters ---
NUM_RAYS = 150
CENTER_POINT = (IMG_WIDTH / 2, IMG_HEIGHT / 2)
# Colors for the two halves of the canvas
COLOR_A = (180, 200, 255) # Blue-white
COLOR_B = (255, 200, 180) # Orange-white

# How much the lines will deviate from a straight path
JITTER_STRENGTH = 1.5
# The size of the central glowing point
CENTER_GLOW_RADIUS = 15

def draw_jittery_line(draw, start_pos, end_pos, color):
    """Draws a line from start to end with a random perpendicular jitter."""
    current_pos = list(start_pos)
    
    # Calculate the main vector from start to end
    dx = end_pos[0] - start_pos[0]
    dy = end_pos[1] - start_pos[1]
    dist = math.sqrt(dx*dx + dy*dy)
    
    # Normalize the main vector (unit vector)
    udx, udy = dx / dist, dy / dist
    
    # Get the perpendicular vector for the jitter
    pdx, pdy = -udy, udx
    
    step_size = 5
    num_steps = int(dist / step_size)

    for i in range(num_steps):
        prev_pos = tuple(current_pos)
        
        # Move along the main vector
        current_pos[0] += udx * step_size
        current_pos[1] += udy * step_size
        
        # Add perpendicular jitter
        jitter = random.uniform(-JITTER_STRENGTH, JITTER_STRENGTH)
        current_pos[0] += pdx * jitter
        current_pos[1] += pdy * jitter
        
        draw.line([prev_pos, tuple(current_pos)], fill=color, width=1)

# --- Main Execution ---
if __name__ == "__main__":
    print(f"Generating the 'Convergence' image into '{FILENAME}'...")

    image = Image.new("RGB", (IMG_WIDTH, IMG_HEIGHT), BACKGROUND_COLOR)
    draw = ImageDraw.Draw(image)

    # 1. Draw the central glowing point
    for i in range(CENTER_GLOW_RADIUS, 0, -1):
        # Create a layered glow effect with decreasing opacity
        alpha = int(255 * (1 - (i / CENTER_GLOW_RADIUS)) * 0.2)
        glow_color = (255, 255, 255, alpha)
        draw.ellipse(
            (CENTER_POINT[0]-i, CENTER_POINT[1]-i, CENTER_POINT[0]+i, CENTER_POINT[1]+i),
            fill=glow_color
        )

    # 2. Generate the converging rays
    for _ in range(NUM_RAYS):
        # Pick a random starting point on the edge of the image
        edge = random.randint(0, 3)
        if edge == 0: # Top
            start_x, start_y = random.uniform(0, IMG_WIDTH), 0
        elif edge == 1: # Right
            start_x, start_y = IMG_WIDTH, random.uniform(0, IMG_HEIGHT)
        elif edge == 2: # Bottom
            start_x, start_y = random.uniform(0, IMG_WIDTH), IMG_HEIGHT
        else: # Left
            start_x, start_y = 0, random.uniform(0, IMG_HEIGHT)
            
        # Choose color based on which side the ray starts from
        color = COLOR_A if start_x < IMG_WIDTH / 2 else COLOR_B
        
        draw_jittery_line(draw, (start_x, start_y), CENTER_POINT, color)
    
    image.save(FILENAME)
    print("Generation complete.")