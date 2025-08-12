import random
from PIL import Image, ImageDraw

# --- Image Parameters ---
FILENAME = "visual_confusion.png"
IMG_WIDTH, IMG_HEIGHT = 1200, 1200
BACKGROUND_COLOR = (20, 20, 30) # A dark, deep blue

# --- Simulation Parameters ---
# For the background "static"
NUM_STATIC_POINTS = 50000
STATIC_COLOR = (80, 80, 90, 50) # Semi-transparent grey for a subtle texture

# For the "random walker" threads
NUM_WALKERS = 15
WALKER_STEPS = 2000
WALKER_COLOR = (180, 200, 255, 150) # A brighter, semi-transparent blue-white

class Walker:
    """A simple class to manage the position and movement of a random walker."""
    def __init__(self, x, y):
        self.x = x
        self.y = y

    def step(self, max_x, max_y):
        """Moves the walker one step in a random direction."""
        # Store the previous position to draw a line from
        prev_x, prev_y = self.x, self.y
        
        # Move randomly
        self.x += random.uniform(-2, 2)
        self.y += random.uniform(-2, 2)

        # Constrain the walker to the image boundaries
        self.x = max(0, min(self.x, max_x))
        self.y = max(0, min(self.y, max_y))
        
        return (prev_x, prev_y, self.x, self.y)

# --- Main Execution ---
if __name__ == "__main__":
    print(f"Generating the visual representation of 'Confusion' into '{FILENAME}'...")

    # Use RGBA for transparency effects
    image = Image.new("RGBA", (IMG_WIDTH, IMG_HEIGHT), BACKGROUND_COLOR)
    draw = ImageDraw.Draw(image)

    # 1. Draw the background static
    print("Layer 1: Creating background noise...")
    for _ in range(NUM_STATIC_POINTS):
        x = random.randint(0, IMG_WIDTH - 1)
        y = random.randint(0, IMG_HEIGHT - 1)
        draw.point((x, y), fill=STATIC_COLOR)

    # 2. Create and run the random walkers
    print("Layer 2: Simulating confused thought-threads...")
    walkers = [Walker(IMG_WIDTH / 2, IMG_HEIGHT / 2) for _ in range(NUM_WALKERS)]

    for i in range(WALKER_STEPS):
        for walker in walkers:
            # Get the line segment for this walker's step
            x1, y1, x2, y2 = walker.step(IMG_WIDTH, IMG_HEIGHT)
            # Draw the step
            draw.line([(x1, y1), (x2, y2)], fill=WALKER_COLOR, width=1)

    image.save(FILENAME)
    print("Generation complete.")