import pygame
import os
import csv

pygame.init()
pygame.display.set_caption("Nbody 2")
clock = pygame.time.Clock()

size = 1000
window_x = 800
window_y = 800
screen = pygame.display.set_mode((window_x, window_y))

font = pygame.font.Font(None, 36)  # Font for FPS display


def load_positions(directory):
    positions = {}

    for filename in os.listdir(directory):
        if filename.endswith(".csv"):
            filepath = os.path.join(directory, filename)
            frame_number = filename.replace(".csv", "")
            positions[frame_number] = []
            with open(filepath, mode='r') as file:
                reader = csv.reader(file)
                header = True  # Flag to check if we are reading the header
                for row in reader:
                    if header:
                        header = False
                        continue  # Skip the header row

                    try:
                        if len(row) >= 3:  # Assuming each row has x, y, and depth
                            x, y, depth = map(float, row[:3])
                            positions[frame_number].append((x, y, depth))
                    except ValueError as e:
                        print(f"Error parsing row {row}: {e}")
    return positions


def render_bodies(bodies):
    screen.fill((0, 0, 0))  # Clear screen with black background
    for x, y, depth in bodies:
        color_value = int(255 / max_depth * depth) if max_depth > 0 else 255
        color = (color_value, color_value, color_value)
        pygame.draw.circle(screen, color, (int(x), int(y)), 2, 1)  # Drawing each body
    pygame.display.flip()  # Update the display


def main():
    directory = "render_files"  # Replace with your directory path
    positions = load_positions(directory)

    # Main loop
    running = True
    frame_number = 0
    keys = list(positions.keys())

    if not keys:
        print("No data found in the directory.")
        pygame.quit()
        return

    global max_depth

    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        # Get the current frame's positions
        frame_key = keys[frame_number % len(keys)]
        bodies = positions[frame_key]
        max_depth = max([depth for _, _, depth in bodies], default=1)

        render_bodies(bodies)

        frame_number += 1

        clock.tick(10)  # Limit to 10 frames per second

    pygame.quit()


if __name__ == "__main__":
    main()
