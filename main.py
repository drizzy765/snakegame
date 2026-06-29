from random import randrange

import pygame as pg

# --- Configuration ---
WINDOW = 1000
TITLE_SIZE = 50
RANGE = (TITLE_SIZE // 2, WINDOW - TITLE_SIZE // 2, TITLE_SIZE)
get_random_position = lambda: (randrange(*RANGE), randrange(*RANGE))

pg.init()
screen = pg.display.set_mode((WINDOW, WINDOW))
pg.display.set_caption("Snake Game")
clock = pg.time.Clock()
font = pg.font.SysFont("Arial", 30, bold=True)

# --- Initial State ---
# Create snake head
snake = pg.Rect(0, 0, TITLE_SIZE - 2, TITLE_SIZE - 2)
snake.center = get_random_position()
length = 1
segments = [snake.copy()]
snake_direction = (0, 0)
time, time_step = 0, 150

# Create food
food = snake.copy()
food.center = get_random_position()

running = True
while running:
    # --- Event Handling ---
    for event in pg.event.get():
        if event.type == pg.QUIT:
            running = False
        # Handle direction changes
        if event.type == pg.KEYDOWN:
            if event.key == pg.K_w and snake_direction != (0, 1):
                snake_direction = (0, -1)
            elif event.key == pg.K_s and snake_direction != (0, -1):
                snake_direction = (0, 1)
            elif event.key == pg.K_a and snake_direction != (1, 0):
                snake_direction = (-1, 0)
            elif event.key == pg.K_d and snake_direction != (-1, 0):
                snake_direction = (1, 0)

    # --- Drawing ---
    screen.fill((0, 0, 0))
    # Draw food
    pg.draw.rect(screen, "red", food)
    # Draw snake segments
    for segment in segments:
        pg.draw.rect(screen, "green", segment)

    # Display score
    score_text = font.render(f"Score: {length - 1}", True, (255, 255, 255))
    screen.blit(score_text, (10, 10))

    # --- Game Logic ---
    time_now = pg.time.get_ticks()
    if time_now - time > time_step:
        time = time_now
        # Move the head
        snake.move_ip(snake_direction[0] * TITLE_SIZE, snake_direction[1] * TITLE_SIZE)

        # Add new segment to the list and trim to maintain length
        segments.append(snake.copy())
        segments = segments[-length:]

        # Check Food Collision
        if snake.center == food.center:
            food.center = get_random_position()
            length += 1
            time_step = max(50, time_step - 2)  # Speed up slightly

        # Check Self/Boundary Collision
        if (
            snake.left < 0
            or snake.right > WINDOW
            or snake.top < 0
            or snake.bottom > WINDOW
            or snake in segments[:-1]
        ):
            # Reset
            snake.center, food.center = get_random_position(), get_random_position()
            length, segments = 1, [snake.copy()]
            snake_direction = (0, 0)
            time_step = 150

    pg.display.flip()
    clock.tick(60)

pg.quit()
