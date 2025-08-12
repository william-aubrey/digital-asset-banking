import random
from PIL import Image, ImageDraw

# --- Image Parameters ---
FILENAME = "barnsley_fern.png"
IMG_WIDTH, IMG_HEIGHT = 1200, 1600
BACKGROUND_COLOR = (12, 25, 18) # A dark, organic green
FERN_COLOR = (120, 220, 130)   # A vibrant, light green

# Number of points to plot. More points create a denser, more detailed fern.
ITERATIONS = 200000

def transform(p):
    """Applies one of the four weighted transformations to a point."""
    x, y = p
    rand_val = random.random()

    if rand_val < 0.01:
        # Transformation 1: Creates the "stem" (1% probability)
        x_new = 0.0
        y_new = 0.16 * y
    elif rand_val < 0.86:
        # Transformation 2: Creates the successive, smaller leaflets (85% probability)
        x_new = 0.85 * x + 0.04 * y
        y_new = -0.04 * x + 0.85 * y + 1.6
    elif rand_val < 0.93:
        # Transformation 3: Creates the largest left-hand leaflet (7% probability)
        x_new = 0.2 * x - 0.26 * y
        y_new = 0.23 * x + 0.22 * y + 1.6
    else:
        # Transformation 4: Creates the largest right-hand leaflet (7% probability)
        x_new = -0.15 * x + 0.28 * y
        y_new = 0.26 * x + 0.24 * y + 0.44
        
    return (x_new, y_new)

def draw_fern(draw, iterations):
    """Plots all the points to draw the fern."""
    # Start at the origin
    p = (0, 0)
    
    for i in range(iterations):
        # Apply a transformation to get the next point
        p = transform(p)
        
        # Translate the mathematical coordinates to image pixel coordinates
        # The values are scaled and shifted to fit nicely within the image canvas
        plot_x = int(p[0] * (IMG_WIDTH / 10) + (IMG_WIDTH / 2))
        plot_y = int(p[1] * (IMG_HEIGHT / 12) + (IMG_HEIGHT * 0.05))
        
        # We only draw the point if it's within the image boundaries
        if 0 <= plot_x < IMG_WIDTH and 0 <= plot_y < IMG_HEIGHT:
            draw.point((plot_x, plot_y), FERN_COLOR)

# --- Main Execution ---
if __name__ == "__main__":
    print(f"Beginning procedural generation of '{FILENAME}'...")
    print(f"This will plot {ITERATIONS} points. Please be patient.")

    # Create a new image with a dark background
    image = Image.new("RGB", (IMG_WIDTH, IMG_HEIGHT), BACKGROUND_COLOR)
    drawer = ImageDraw.Draw(image)

    # Run the generation algorithm
    draw_fern(drawer, ITERATIONS)

    # Save the final image
    # We flip it vertically because the mathematical coordinates are bottom-up
    image.transpose(Image.FLIP_TOP_BOTTOM).save(FILENAME)

    print("Generation complete. The artifact has been manifested.")