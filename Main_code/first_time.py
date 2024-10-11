import os
import json
import pygame

CONFIG_FILE = 'default.json'

# Default config structure
default_config = {
    "prefix": "$",
    "welcome_channel_id": None,  
    "mod_log_channel_id": None, 
    "debug_mode": False,
    "allowed_debug_user_id": None,
    "OfflineTimer": 10,
    "first_Time": True,
    "Bot_Token": None
}

# Load the configuration from the file or create a new one if missing
def load_config():
    if os.path.exists(CONFIG_FILE):
        with open(CONFIG_FILE, 'r') as file:
            return json.load(file)
    else:
        # If config doesn't exist, create a new one with default values
        save_config(default_config)
        return default_config

# Save configuration to the file
def save_config(data):
    with open(CONFIG_FILE, 'w') as file:
        json.dump(data, file, indent=4)

# Initialize pygame
pygame.init()

# Define the Pygame window setup
def pygame_setup_window():
    screen = pygame.display.set_mode((600, 400))
    pygame.display.set_caption('Discord Bot Setup')

    # Get the current directory of the script
    current_dir = os.path.dirname(os.path.abspath(__file__))
    
    # Construct the full path to the setup_logo.png image
    logo_path = os.path.join(current_dir, 'images', 'setup_logo.png')

    # Try to load the image and set the icon, handle errors if the image is not found
    try:
        pygame.display.set_icon(pygame.image.load(logo_path))
    except FileNotFoundError:
        print(f"Error: The image file at {logo_path} was not found.")
    except pygame.error as e:
        print(f"Pygame error: {e}")

    # Define colors
    WHITE = (255, 255, 255)
    BLACK = (0, 0, 0)
    color_inactive = pygame.Color('lightskyblue3')
    color_active = pygame.Color('dodgerblue2')
    color = color_inactive

    # Define fonts
    font = pygame.font.Font(None, 32)

    # Input box properties
    input_box = pygame.Rect(100, 100, 400, 32)
    active = False
    text = ''
    
    # Setup steps
    steps = [
        "Enter your Discord ID (for debug mode):",
        "Enter bot command prefix:",
        "Enter main channel ID:",
        "Enter mod log channel ID:",
        "Enter offline timer duration (in seconds):",
        "Enter Discord bot token:"
    ]
    
    current_step = 0
    inputs = {}

    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.MOUSEBUTTONDOWN:
                # Toggle input box active state
                if input_box.collidepoint(event.pos):
                    active = not active
                else:
                    active = False
                color = color_active if active else color_inactive
            if event.type == pygame.KEYDOWN:
                if active:
                    if event.key == pygame.K_RETURN:
                        if current_step < len(steps):
                            inputs[steps[current_step]] = text
                            current_step += 1
                            text = ''
                        if current_step == len(steps):
                            # All inputs complete, save config
                            config_data = {
                                'first_time': False,
                                "default_channel_id": 1233588735115919381,
                                "Owner_ids": [1225272276979810386],
                                'allowed_debug_user_id': inputs[steps[0]],
                                'prefix': inputs[steps[1]],
                                'welcome_channel_id': inputs[steps[2]],
                                'mod_log_channel_id': inputs[steps[3]],
                                'OfflineTimer': int(inputs[steps[4]]),
                                'Bot_Token': inputs[steps[5]],
                            }
                            save_config(config_data)
                            print("Configuration saved. Exiting setup.")
                            running = False
                    elif event.key == pygame.K_BACKSPACE:
                        text = text[:-1]
                    else:
                        text += event.unicode

        # Fill the screen with white
        screen.fill(WHITE)

        # Render the current step prompt
        if current_step < len(steps):
            step_surface = font.render(steps[current_step], True, BLACK)
            screen.blit(step_surface, (input_box.x, input_box.y - 50))

        # Render the current text input
        txt_surface = font.render(text, True, BLACK)
        
        # Resize the input box if the text is too long
        width = max(200, txt_surface.get_width()+10)
        input_box.w = width

        # Blit the text
        screen.blit(txt_surface, (input_box.x+5, input_box.y+5))

        # Draw the input box rect
        pygame.draw.rect(screen, color, input_box, 2)

        # Update the display
        pygame.display.flip()

    pygame.quit()

# Main logic
config = load_config()

# If first_time is True, run the Pygame setup window
if config.get('first_Time', True):  # Fixed the key capitalization
    print("First-time setup detected. Launching setup window...")
    pygame_setup_window()
else:
    print(f"Configuration loaded. Debug user ID: {config['allowed_debug_user_id']}")
