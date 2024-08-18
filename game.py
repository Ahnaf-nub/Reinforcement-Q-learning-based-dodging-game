import pygame
import random
pygame.init()

# Screen dimensions
WIDTH, HEIGHT = 800, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Dodge and Escape")

# Colors
WHITE = (255, 255, 255)
RED = (255, 0, 0)
GREEN = (0, 255, 0)

# Player settings
player_width, player_height = 50, 50
player_x, player_y = WIDTH // 2, HEIGHT - player_height - 10
player_speed = 5
player_jump = -15
player_velocity_y = 0
gravity = 1

# Kunai settings
kunai_width, kunai_height = 20, 60
kunai_speed = 5
falling_objects = []

running = True
clock = pygame.time.Clock()
screen.fill((5, 255, 255))

def draw_player():
    pygame.draw.rect(screen, GREEN, (player_x, player_y, player_width, player_height))

def create_kunai():
    x = random.randint(0, WIDTH - kunai_width)
    y = -kunai_height
    falling_objects.append([x, y])

def draw_kunai():
    for obj in falling_objects:
        pygame.draw.rect(screen, RED, (obj[0], obj[1], kunai_width, kunai_height))

def update_kunai():
    for obj in falling_objects:
        obj[1] += kunai_speed
        if obj[1] > HEIGHT:
            falling_objects.remove(obj)

def check_collision():
    global running
    for obj in falling_objects:
        if player_x < obj[0] + kunai_width and player_x + player_width > obj[0] and player_y < obj[1] + kunai_height and player_y + player_height > obj[1]:
            running = False  # End game if collision detected

def move_player(keys_pressed):
    global player_x, player_y, player_velocity_y, door_reached

    # Move left and right
    if keys_pressed[pygame.K_LEFT] and player_x - player_speed > 0:
        player_x -= player_speed
    if keys_pressed[pygame.K_RIGHT] and player_x + player_speed + player_width < WIDTH:
        player_x += player_speed

    # Jump mechanics
    if keys_pressed[pygame.K_UP]:
        if player_velocity_y == 0:  # Can only jump if not already in the air
            player_velocity_y = player_jump
    
    player_y += player_velocity_y
    player_velocity_y += gravity  # Apply gravity

    # Prevent falling through the floor
    if player_y > HEIGHT - player_height:
        player_y = HEIGHT - player_height
        player_velocity_y = 0

while running:
    clock.tick(60)
    screen.fill(WHITE)
    
    # Handle events
    for event in pygame.event.get():
        if event.type == pygame.QUIT or event.type == pygame.K_ESCAPE: running = False

    # Create new kunai at random intervals
    if random.randint(1, 20) == 1:
        create_kunai()

    # Update and draw everything
    keys_pressed = pygame.key.get_pressed()
    move_player(keys_pressed)
    update_kunai()
    check_collision()
    draw_player()
    draw_kunai()
    pygame.display.update()

pygame.quit()
