# Just for Fun. 
# Vibe Coded by https://x.com/WowCoolTh4nks
# Inspired by https://x.com/klara_sjo/status/2019504853605548254
# 10:25 CET - 5 February 2026

import subprocess
import threading
import re
import pygame
import time
import random

progress = [0]
scan_complete = [False]
running = [True]
last_lines = []

def clean_line(line):
    if not line:
        return ""
    # Remove null bytes first
    line = line.replace('\x00', '')
    # Collapse all whitespace (including the weird spacing)
    line = re.sub(r'\s+', ' ', line.strip())
    return line

def parse_progress(line):
    line = clean_line(line)
    if not line:
        return None

    # Tolerant English parser
    m = re.search(r'Verification\s*(\d+)\s*%\s*complete', line, re.IGNORECASE)
    if m:
        return int(m.group(1))

    if "Windows Resource Protection did not find any integrity violations" in line:
        return 100
    return None

def run_sfc():
    proc = subprocess.Popen(
        ['sfc', '/scannow'],
        stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT,
        text=True,
        bufsize=1,
        universal_newlines=True,
        encoding='utf-8',
        errors='replace'   # ← helps with bad chars
    )
    for raw_line in iter(proc.stdout.readline, ''):
        clean = clean_line(raw_line)
        print(clean)
        last_lines.append(clean)
        if len(last_lines) > 6:
            last_lines.pop(0)
        pct = parse_progress(raw_line)  # pass original for parsing safety
        if pct is not None:
            progress[0] = max(progress[0], pct)
    proc.wait()
    scan_complete[0] = True

def main():
    pygame.init()
    WIDTH, HEIGHT = 920, 640
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption("Retro SFC Defragmenter")
    clock = pygame.time.Clock()
    font = pygame.font.SysFont(None, 36)
    font_small = pygame.font.SysFont(None, 24)
    font_tiny = pygame.font.SysFont(None, 20)

    ROWS, COLS = 24, 68
    BLOCK_W = WIDTH // COLS
    BLOCK_H = 14

    # Windows 95 Defrag colors
    BG_COLOR = (192, 192, 192)      # Win95 gray background
    DARK_BLUE = (0, 0, 128)        # Defragged blocks
    RED = (255, 0, 0)               # Reading head (snake)
    LIGHT_CYAN = (0, 255, 255)      # Fragmented blocks (to be defragged)
    WHITE = (255, 255, 255)         # Free space
    PROGRESS_COLOR = (0, 220, 180)
    TEXT_COLOR = (0, 0, 0)          # Black text for gray background

    # Initial grid - 90% light cyan, 10% white at the end
    total_blocks = ROWS * COLS
    white_blocks_count = int(total_blocks * 0.10)
    
    grid = []
    for r in range(ROWS):
        row = []
        for c in range(COLS):
            block_index = r * COLS + c
            # Last 10% are white (free space)
            if block_index >= (total_blocks - white_blocks_count):
                row.append(WHITE)
            else:
                row.append(LIGHT_CYAN)
        grid.append(row)

    # Snake head (red blocks) - 10 red blocks
    RED_BLOCKS_COUNT = 10
    snake_positions = []
    
    # Blinking effect for last red block
    blink_timer = 0
    blink_on = True

    while running[0]:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running[0] = False

        # Update blink timer (blink every ~500ms)
        blink_timer += 1
        if blink_timer >= 7:  # 7 frames at 15 FPS = ~466ms
            blink_timer = 0
            blink_on = not blink_on

        current_pct = progress[0]
        progress_ratio = current_pct / 100.0
        
        # Calculate how many blocks should be dark blue based on progress
        target_dark_blue_blocks = int(total_blocks * progress_ratio * 0.90)  # 90% of total
        
        # Instantly update all blocks up to target
        for block_num in range(target_dark_blue_blocks):
            r = block_num // COLS
            c = block_num % COLS
            if r < ROWS and c < COLS and grid[r][c] != DARK_BLUE:
                grid[r][c] = DARK_BLUE
        
        # Calculate snake head positions (10 red blocks after the dark blue area)
        snake_positions = []
        for i in range(RED_BLOCKS_COUNT):
            block_num = target_dark_blue_blocks + i
            if block_num < total_blocks:
                r = block_num // COLS
                c = block_num % COLS
                snake_positions.append((r, c))

        # === Drawing ===
        screen.fill(BG_COLOR)
        for r in range(ROWS):
            for c in range(COLS):
                color = grid[r][c]
                
                # Override with red if this position is in snake
                if (r, c) in snake_positions:
                    # Check if this is the LAST red block (index 9)
                    if (r, c) == snake_positions[-1] and len(snake_positions) == RED_BLOCKS_COUNT:
                        # Blink effect - show red when blink_on, otherwise show underlying color
                        color = RED if blink_on else grid[r][c]
                    else:
                        color = RED
                
                pygame.draw.rect(screen, color, (c * BLOCK_W, r * BLOCK_H + 60, BLOCK_W, BLOCK_H))
                pygame.draw.rect(screen, (5, 15, 40), (c * BLOCK_W, r * BLOCK_H + 60, BLOCK_W, BLOCK_H), 1)

        # Progress bar
        bar_y = HEIGHT - 150
        pygame.draw.rect(screen, (50, 50, 90), (60, bar_y, WIDTH - 120, 28))
        fill_w = int((WIDTH - 120) * progress_ratio)
        pygame.draw.rect(screen, PROGRESS_COLOR, (60, bar_y, fill_w, 28))
        status = font.render(f"Verification {current_pct}% complete", True, TEXT_COLOR)
        screen.blit(status, (60, bar_y - 45))

        # Legend (where debug panel was)
        legend_y = bar_y + 50
        font_legend = pygame.font.SysFont(None, 18)
        
        leg_x = 60
        # Title
        screen.blit(font_small.render("Legend:", True, TEXT_COLOR), (leg_x, legend_y))
        
        # Fragmented files
        pygame.draw.rect(screen, LIGHT_CYAN, (leg_x, legend_y + 25, 16, 16))
        screen.blit(font_legend.render("Fragmented files", True, TEXT_COLOR), (leg_x + 25, legend_y + 26))
        
        # Reading
        pygame.draw.rect(screen, RED, (leg_x + 180, legend_y + 25, 16, 16))
        screen.blit(font_legend.render("Reading", True, TEXT_COLOR), (leg_x + 205, legend_y + 26))
        
        # Defragmented files
        pygame.draw.rect(screen, DARK_BLUE, (leg_x + 300, legend_y + 25, 16, 16))
        screen.blit(font_legend.render("Defragmented files", True, TEXT_COLOR), (leg_x + 325, legend_y + 26))
        
        # Free space
        pygame.draw.rect(screen, WHITE, (leg_x + 480, legend_y + 25, 16, 16))
        screen.blit(font_legend.render("Free space", True, TEXT_COLOR), (leg_x + 505, legend_y + 26))

        pygame.display.flip()
        clock.tick(15)

        if scan_complete[0] and current_pct >= 100:
            time.sleep(3)
            running[0] = False

    pygame.quit()

if __name__ == "__main__":
    threading.Thread(target=run_sfc, daemon=True).start()
    main()