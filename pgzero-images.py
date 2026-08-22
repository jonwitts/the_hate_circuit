import pgzrun

# Match these dimensions to your display resolution
WIDTH = 1920
HEIGHT = 1080

# Initial default background image
current_image = 'hate-circuit-bg'

def draw():
    screen.clear()
    # Draw the current background starting from the top-left corner
    screen.blit(current_image, (0, 0))

def update():
    global current_image

    # Check arrow key inputs to change the displayed image
    if keyboard.up:
        current_image = 'hate'
    elif keyboard.down:
        current_image = 'love'
    elif keyboard.right:
        current_image = 'unsure'
    else:
        current_image = 'hate-circuit-bg'  # Reverts to default when no tracked keys are held

pgzrun.go()
