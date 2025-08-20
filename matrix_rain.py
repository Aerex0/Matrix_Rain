#!/usr/bin/env python3
import pygame
import random
import string
import math  # for distance calculation

pygame.init()

# Fullscreen
screen = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
WIDTH, HEIGHT = screen.get_size()
pygame.display.set_caption("Matrix Rain (Pygame)")

# Colors
GREEN = (0, 255, 70)
DARK_GREEN = (0, 155, 40)
BLACK = (0, 0, 0)

# Font
font_size = 30
font = pygame.font.SysFont("Courier", font_size)

# Characters
chars = string.ascii_letters + string.digits + "@#$%^&*"

# One stream per column
columns = WIDTH // font_size
positions = [random.randint(0, HEIGHT // font_size) for _ in range(columns)]
# Each column has its own speed (how many rows per update)
speeds = [1 for _ in range(columns)]
# Each column has its own delay (frames before next move)
delays = [random.randint(2, 6) for _ in range(columns)]
# Track cooldown per column
cooldowns = [0 for _ in range(columns)]

# Glow radius
RADIUS = 100  

# Game loop
clock = pygame.time.Clock()
running = True
paused = False

while running:
    screen.fill(BLACK)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
            running = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                running = False
            elif event.key == pygame.K_UP:
                speeds = [s+1 for s in speeds]  # faster
            elif event.key == pygame.K_DOWN:
                speeds = [max(1, s-1) for s in speeds]  # slower
            elif event.key == pygame.K_c:  # toggle color mode
                GREEN = (random.randint(50,255), random.randint(50,255), random.randint(50,255))
                DARK_GREEN = tuple(max(0, c-100) for c in GREEN)
            elif event.key == pygame.K_SPACE:
                paused = not paused  # toggle pause

    mx, my = pygame.mouse.get_pos()

    for i in range(columns):
        x = i * font_size
        y = positions[i] * font_size

        # Draw head
        head_char = random.choice(chars)

        # Tail
        tail_length = random.choice([6, 8, 9, 11, 15, 20])
        for j in range(1, tail_length):
            tail_y = (positions[i] - j) * font_size
            if 0 <= tail_y < HEIGHT:
                tail_char = random.choice(chars)

                # Circular distance check for glow
                dist = math.sqrt((x - mx) ** 2 + (tail_y - my) ** 2)
                if dist < RADIUS:
                    color = (0, 255, 255)  # cyan glow
                else:
                    color = DARK_GREEN

                tail_surface = font.render(tail_char, True, color)
                screen.blit(tail_surface, (x, tail_y))

        # Head (after tail is drawn)
        dist = math.sqrt((x - mx) ** 2 + (y - my) ** 2)
        if dist < RADIUS:
            head_surface = font.render(head_char, True, (0, 255, 255))  # glow
        else:
            head_surface = font.render(head_char, True, GREEN)
        screen.blit(head_surface, (x, y))

        # Handle cooldown (slows streams individually)
        if not paused:
            if cooldowns[i] <= 0:
                positions[i] = (positions[i] + speeds[i]) % (HEIGHT // font_size)
                cooldowns[i] = delays[i]  # reset cooldown
            else:
                cooldowns[i] -= 1

    pygame.display.flip()
    clock.tick(30)  # keep smooth display
pygame.quit()
