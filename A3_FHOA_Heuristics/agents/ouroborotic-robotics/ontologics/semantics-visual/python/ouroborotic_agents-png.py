import math
from PIL import Image, ImageDraw

# --- Image Parameters ---
FILENAME = "ouroborotic_agents.png"
IMG_WIDTH, IMG_HEIGHT = 1200, 1200
BACKGROUND_COLOR = (225, 225, 225) # Light grey background
AGENT_COLOR = (235, 200, 50)     # The golden-yellow agent color

# --- Scene Parameters ---
NUM_AGENTS = 24
CIRCLE_RADIUS = 400
CIRCLE_CENTER = (IMG_WIDTH / 2, IMG_HEIGHT / 2)
FADE_LENGTH = 4 # How many agents at the end of the cycle will fade

def draw_agent(draw, center_x, center_y, angle_deg, pose, color):
    """Draws a single blocky agent at a specific location and rotation."""
    
    # Define the agent's body parts as simple rectangles [x0, y0, x1, y1]
    # relative to a (0,0) center point.
    torso = [-10, -20, 10, 20]
    head = [-8, -38, 8, -22]
    
    # Define two different poses for the limbs to create a running animation
    if pose == 0:
        # Pose 1
        leg1 = [-8, 20, 0, 45]
        leg2 = [0, 20, 8, 40]
    else:
        # Pose 2
        leg1 = [-8, 20, 0, 40]
        leg2 = [0, 20, 8, 45]
        
    body_parts = [torso, head, leg1, leg2]
    
    # Convert rotation angle to radians for math functions
    angle_rad = math.radians(angle_deg)
    
    for part in body_parts:
        # Get the corners of the rectangle part
        x0, y0, x1, y1 = part
        
        # Define the 4 corners to be rotated
        corners = [(x0, y0), (x1, y0), (x1, y1), (x0, y1)]
        
        rotated_corners = []
        for x, y in corners:
            # Rotate each corner around the agent's (0,0) center
            x_rot = x * math.cos(angle_rad) - y * math.sin(angle_rad)
            y_rot = x * math.sin(angle_rad) + y * math.cos(angle_rad)
            
            # Translate the rotated corner to the agent's position on the main circle
            final_x = x_rot + center_x
            final_y = y_rot + center_y
            rotated_corners.append((final_x, final_y))
            
        # Draw the rotated polygon
        draw.polygon(rotated_corners, fill=color)

# --- Main Execution ---
if __name__ == "__main__":
    print(f"Generating the Ouroborotic agent cycle into '{FILENAME}'...")

    image = Image.new("RGB", (IMG_WIDTH, IMG_HEIGHT), BACKGROUND_COLOR)
    drawer = ImageDraw.Draw(image)

    for i in range(NUM_AGENTS):
        # Calculate the position and rotation for each agent on the circle
        percent_of_circle = i / NUM_AGENTS
        angle_rad = percent_of_circle * 2 * math.pi
        angle_deg = math.degrees(angle_rad)

        agent_x = CIRCLE_CENTER[0] + CIRCLE_RADIUS * math.cos(angle_rad)
        agent_y = CIRCLE_CENTER[1] + CIRCLE_RADIUS * math.sin(angle_rad)
        
        # Determine the running pose
        pose = i % 2
        
        # Determine the color (for the fade effect)
        current_color = AGENT_COLOR
        if i >= NUM_AGENTS - FADE_LENGTH:
            # This agent is in the "fading" section
            fade_progress = (i - (NUM_AGENTS - FADE_LENGTH)) / FADE_LENGTH
            
            # Interpolate color from AGENT_COLOR to BACKGROUND_COLOR
            r = int(AGENT_COLOR[0] * (1 - fade_progress) + BACKGROUND_COLOR[0] * fade_progress)
            g = int(AGENT_COLOR[1] * (1 - fade_progress) + BACKGROUND_COLOR[1] * fade_progress)
            b = int(AGENT_COLOR[2] * (1 - fade_progress) + BACKGROUND_COLOR[2] * fade_progress)
            current_color = (r, g, b)

        # Draw the agent with the calculated properties
        # The rotation is offset by -90 degrees to make the agents face along the circle path
        draw_agent(drawer, agent_x, agent_y, angle_deg - 90, pose, current_color)

    image.save(FILENAME)
    print("Generation complete.")