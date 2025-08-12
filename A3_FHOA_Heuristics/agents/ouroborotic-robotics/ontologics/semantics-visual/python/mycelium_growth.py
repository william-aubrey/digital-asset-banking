import math
import random
from PIL import Image, ImageDraw

# --- Image Parameters ---
FILENAME = "mycelium_growth.png"
IMG_WIDTH, IMG_HEIGHT = 1200, 1200
BACKGROUND_COLOR = (10, 8, 15) # Very dark blue-purple
MYCELIUM_COLOR = (200, 210, 255) # Light, glowing blue-white

# --- Simulation Parameters ---
NUM_ATTRACTORS = 3000  # Number of "nutrient" points
INFLUENCE_RADIUS = 80  # How far a mycelium node can "see"
KILL_RADIUS = 20       # How close a node must be to "consume" a nutrient
STEP_SIZE = 5          # How long each new branch segment is
NUM_ITERATIONS = 200   # How many growth steps to simulate

class MyceliumNode:
    """A simple class to hold the position of a node and its parent."""
    def __init__(self, x, y, parent=None):
        self.x = x
        self.y = y
        self.parent = parent

def distance(p1, p2):
    """Calculates the Euclidean distance between two points."""
    return math.sqrt((p1[0] - p2[0])**2 + (p1[1] - p2[1])**2)

# --- Main Execution ---
if __name__ == "__main__":
    print(f"Beginning mycelium simulation for '{FILENAME}'...")

    image = Image.new("RGB", (IMG_WIDTH, IMG_HEIGHT), BACKGROUND_COLOR)
    draw = ImageDraw.Draw(image)

    # 1. Create the attractors (nutrient points)
    attractors = [(random.uniform(0, IMG_WIDTH), random.uniform(0, IMG_HEIGHT)) for _ in range(NUM_ATTRACTORS)]

    # 2. Create the root nodes of the mycelium
    mycelium_nodes = [MyceliumNode(IMG_WIDTH / 2, IMG_HEIGHT - 10)]

    # 3. Run the growth simulation
    print("Growing the mycelium network...")
    for i in range(NUM_ITERATIONS):
        if not attractors:
            break # Stop if all nutrients are consumed

        # For each attractor, find the closest mycelium node
        attractor_to_node_map = {}
        for attractor in attractors:
            closest_node = None
            min_dist = float('inf')
            for node in mycelium_nodes:
                d = distance((node.x, node.y), attractor)
                if d < min_dist:
                    min_dist = d
                    closest_node = node
            if closest_node:
                attractor_to_node_map[attractor] = closest_node
        
        # For each mycelium node, find its attractors and grow towards them
        new_nodes = []
        for node in mycelium_nodes:
            influenced_attractors = []
            for attractor, closest_node in attractor_to_node_map.items():
                if closest_node == node and distance((node.x, node.y), attractor) < INFLUENCE_RADIUS:
                    influenced_attractors.append(attractor)

            if influenced_attractors:
                # Calculate the average direction towards the influencing attractors
                avg_dir_x, avg_dir_y = 0, 0
                for ax, ay in influenced_attractors:
                    avg_dir_x += ax - node.x
                    avg_dir_y += ay - node.y
                
                magnitude = math.sqrt(avg_dir_x**2 + avg_dir_y**2)
                if magnitude > 0:
                    # Create a new node in the calculated direction
                    new_x = node.x + (avg_dir_x / magnitude) * STEP_SIZE
                    new_y = node.y + (avg_dir_y / magnitude) * STEP_SIZE
                    new_nodes.append(MyceliumNode(new_x, new_y, parent=node))

        mycelium_nodes.extend(new_nodes)

        # Remove attractors that have been reached
        attractors_to_remove = set()
        for attractor in attractors:
            for node in mycelium_nodes:
                if distance((node.x, node.y), attractor) < KILL_RADIUS:
                    attractors_to_remove.add(attractor)
                    break
        attractors = [a for a in attractors if a not in attractors_to_remove]


    # 4. Draw the final mycelium network
    print("Simulation complete. Drawing the final image...")
    for node in mycelium_nodes:
        if node.parent:
            draw.line([(node.parent.x, node.parent.y), (node.x, node.y)], fill=MYCELIUM_COLOR, width=1)

    image.save(FILENAME)
    print(f"'{FILENAME}' has been generated.")