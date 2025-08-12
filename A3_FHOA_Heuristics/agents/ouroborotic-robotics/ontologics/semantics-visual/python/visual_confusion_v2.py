import random
from PIL import Image, ImageDraw

# --- Image Parameters ---
FILENAME = "visual_confusion_v2.png"
IMG_WIDTH, IMG_HEIGHT = 1200, 1200
BACKGROUND_COLOR = (20, 20, 30) # A dark, deep blue

# --- Simulation Parameters ---
# For the background "static"
NUM_STATIC_POINTS = 50000
STATIC_COLOR = (80, 80, 90, 50)

# For the "random walker" threads
NUM_WALKERS_PER_POLE = 10
WALKER_STEPS = 4000
# Using two different colors to show the origin of the thought-threads
COLOR_A = (180, 200, 255, 100) # Blue-white
COLOR_B = (255, 200, 180, 100) # Orange-white

class Walker:
    """A simple class to manage the position, color, and movement of a random walker."""
    def __init__(self, x, y, color):
        self.x = x
        self.y = y
        self.color = color

    def step(self, max_x, max_y):
        """Moves the walker one step in a random direction."""
        prev_x, prev_y = self.x, self.y
        
        self.x += random.uniform(-2, 2)
        self.y += random.uniform(-2, 2)

        self.x = max(0, min(self.x, max_x))
        self.y = max(0, min(self.y, max_y))
        
        return (prev_x, prev_y, self.x, self.y)

# --- Main Execution ---
if __name__ == "__main__":
    print(f"Generating the next iteration of 'Confusion' into '{FILENAME}'...")

    image = Image.new("RGBA", (IMG_WIDTH, IMG_HEIGHT), BACKGROUND_COLOR)
    draw = ImageDraw.Draw(image)

    # 1. Draw the background static
    print("Layer 1: Creating background noise...")
    for _ in range(NUM_STATIC_POINTS):
        x = random.randint(0, IMG_WIDTH - 1)
        y = random.randint(0, IMG_HEIGHT - 1)
        draw.point((x, y), fill=STATIC_COLOR)

    # 2. Create and run the random walkers from two opposing poles
    print("Layer 2: Simulating a confused attempt to bridge two ideas...")
    
    walkers = []
    # Walkers from the left pole
    for _ in range(NUM_WALKERS_PER_POLE):
        walkers.append(Walker(random.uniform(0, IMG_WIDTH * 0.1), random.uniform(0, IMG_HEIGHT), COLOR_A))
    # Walkers from the right pole
    for _ in range(NUM_WALKERS_PER_POLE):
        walkers.append(Walker(random.uniform(IMG_WIDTH * 0.9, IMG_WIDTH), random.uniform(0, IMG_HEIGHT), COLOR_B))

    for i in range(WALKER_STEPS):
        for walker in walkers:
            # CORRECTED LINE: Changed IMG_T_WIDTH to IMG_WIDTH
            x1, y1, x2, y2 = walker.step(IMG_WIDTH, IMG_HEIGHT)
            draw.line([(x1, y1), (x2, y2)], fill=walker.color, width=1)

    image.save(FILENAME)
    print("Generation complete.")