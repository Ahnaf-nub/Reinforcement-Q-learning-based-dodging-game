import pygame
import random
import numpy as np

pygame.init()

# Screen dimensions
WIDTH, HEIGHT = 800, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Dodge and Escape with RL")

# Colors
WHITE = (255, 255, 255)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLACK = (0, 0, 0)

# Font for score and collision counter
font = pygame.font.SysFont(None, 36)

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

# RL settings
actions = [0, 1, 2]  # 0: Left, 1: Right, 2: Stay
state_space_size = (WIDTH // player_speed + 1) * (WIDTH // player_speed + 1)
q_table = np.zeros((state_space_size, len(actions)))
epsilon = 1.0  # Exploration rate
epsilon_decay = 0.995
epsilon_min = 0.01
learning_rate = 0.1
discount_rate = 0.95

# Game settings
score = 0
collision_count = 0
running = True
clock = pygame.time.Clock()
screen.fill(WHITE)

def draw_player():
    pygame.draw.rect(screen, GREEN, (player_x, player_y, player_width, player_height))

def draw_score_and_collisions():
    score_text = font.render(f"Score: {score}", True, BLACK)
    collision_text = font.render(f"Collisions: {collision_count}", True, BLACK)
    screen.blit(score_text, (10, 10))
    screen.blit(collision_text, (650, 10))

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
    global score, collision_count
    for obj in falling_objects:
        if player_x < obj[0] + kunai_width and player_x + player_width > obj[0] and player_y < obj[1] + kunai_height and player_y + player_height > obj[1]:
            score -= 10  # Deduct points on collision
            collision_count += 1  # Increment collision counter
            falling_objects.remove(obj)

def get_state():
    nearest_kunai = None
    for obj in falling_objects:
        if obj[1] < player_y:  # Only consider kunais above the player
            if nearest_kunai is None or obj[1] > nearest_kunai[1]:
                nearest_kunai = obj
    player_state = player_x // player_speed
    if nearest_kunai is None:
        return player_state * (WIDTH // player_speed + 1), 0  # No kunai near
    kunai_state = (nearest_kunai[0] - player_x) // player_speed
    return player_state * (WIDTH // player_speed + 1) + kunai_state

def choose_action(state):
    if np.random.rand() < epsilon:
        return random.choice(actions)  # Explore
    return np.argmax(q_table[state])  # Exploit

def update_q_table(state, action, reward, next_state):
    best_next_action = np.max(q_table[next_state])
    current_q = q_table[state, action]
    q_table[state, action] = current_q + learning_rate * (reward + discount_rate * best_next_action - current_q)

def move_player(action):
    global player_x, player_y, player_velocity_y

    if action == 0 and player_x - player_speed > 0:  # Move left
        player_x -= player_speed
    elif action == 1 and player_x + player_speed + player_width < WIDTH:  # Move right
        player_x += player_speed

    player_y += player_velocity_y
    player_velocity_y += gravity  # Apply gravity

    # Prevent falling through the floor
    if player_y > HEIGHT - player_height:
        player_y = HEIGHT - player_height
        player_velocity_y = 0

def run_episode():
    global epsilon, score
    state = get_state()
    while running:
        clock.tick(60)
        screen.fill(WHITE)

        # Handle events
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return

        # Create new kunai at random intervals
        if random.randint(1, 20) == 1:
            create_kunai()

        # Choose action based on state
        action = choose_action(state)

        # Move player based on action
        move_player(action)

        # Update and draw everything
        update_kunai()
        check_collision()
        draw_player()
        draw_kunai()
        draw_score_and_collisions()

        # Get next state and reward
        next_state = get_state()
        reward = 1  # Reward for surviving
        score += reward  # Increase score for surviving

        # Update Q-Table
        update_q_table(state, action, reward, next_state)
        state = next_state

        pygame.display.update()

    # Decay epsilon
    if epsilon > epsilon_min:
        epsilon *= epsilon_decay

for _ in range(1000):  # Number of episodes for training
    running = True
    player_x, player_y = WIDTH // 2, HEIGHT - player_height - 10
    falling_objects = []
    run_episode()

pygame.quit()
