import math
import random
from PIL import Image, ImageDraw

# --- Image Parameters ---
FILENAME = "mycelium_fast.png"
IMG_WIDTH, IMG_HEIGHT = 1200, 1200
BACKGROUND_COLOR = (10, 8, 15)
MYCELIUM_COLOR = (200, 210, 255)

# --- Simulation Parameters ---
# More walkers create a denser structure
NUM_WALKERS = 20000
# The maximum number of steps a walker can take before being reset
MAX_STEPS = 150

def distance_sq(p1, p2):
    """
    Calculates the squared Euclidean distance.
    This is faster than full distance as it avoids the square root.
    """
    return (p1[0] - p2[0])**2 + (p1[1] - p2[1])**2

# --- Main Execution ---
if __name__ == "__main__":
    print(f"Generating fast mycelium growth into '{FILENAME}'...")

    image = Image.new("RGB", (IMG_WIDTH, IMG_HEIGHT), BACKGROUND_COLOR)
    draw = ImageDraw.Draw(image)

    # The list of "stuck" points that form the mycelium
    stuck_points = []
    
    # Create the initial seed/root of the mycelium in the center
    center_point = (IMG_WIDTH / 2, IMG_HEIGHT / 2)
    stuck_points.append(center_point)
    draw.point(center_point, MYCELIUM_COLOR)

    for i in range(NUM_WALKERS):
        # Create a new walker at a random position
        walker_x = random.uniform(0, IMG_WIDTH)
        walker_y = random.uniform(0, IMG_HEIGHT)
        
        # Let the walker move randomly for a number of steps
        for step in range(MAX_STEPS):
            # Move the walker
            walker_x += random.uniform(-1, 1)
            walker_y += random.uniform(-1, 1)

            # Check if the walker is out of bounds
            if not (0 < walker_x < IMG_WIDTH and 0 < walker_y < IMG_HEIGHT):
                break # Reset this walker

            # Check if the walker is close enough to any stuck point
            is_stuck = False
            for sp_x, sp_y in stuck_points:
                # We check against the squared distance to avoid a slow square root calculation
                if distance_sq((walker_x, walker_y), (sp_x, sp_y)) < 4:
                    draw.line([(walker_x, walker_y), (sp_x, sp_y)], fill=MYCELIUM_COLOR, width=1)
                    stuck_points.append((walker_x, walker_y))
                    is_stuck = True
                    break
            
            if is_stuck:
                # Print progress to the console
                if i % 500 == 0:
                    print(f"  ... {i} / {NUM_WALKERS} particles attached.")
                break # Move to the next walker
    
    image.save(FILENAME)
    print("Generation complete.")