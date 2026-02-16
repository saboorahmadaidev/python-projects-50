import pygame
import random
import sys

pygame.init()
clock = pygame.time.Clock()

WIN_W, WIN_H = 640, 480
SNAKE_BLOCK = 20
BASE_FPS = 10
FPS_INCREASE_EVERY = 3
MAX_FPS = 25

WHITE   = (255, 255, 255)
BLACK   = (  0,   0,   0)
RED     = (220,  20,  60)
GREEN   = ( 34, 139,  34)
DARK    = (  8,  62,  24)
YELLOW  = (255, 215,   0)
BG_COL  = (18, 18, 28)

screen = pygame.display.set_mode((WIN_W, WIN_H))
pygame.display.set_caption("Snake — Saboor's Edition")

small_font = pygame.font.SysFont(None, 20)
mid_font   = pygame.font.SysFont(None, 28)
big_font   = pygame.font.SysFont(None, 48)


def draw_text(text, font, color, center):
    surf = font.render(text, True, color)
    rect = surf.get_rect(center=center)
    screen.blit(surf, rect)


def grid_random_position(snake):
    cols = WIN_W // SNAKE_BLOCK
    rows = WIN_H // SNAKE_BLOCK
    while True:
        x = random.randint(0, cols - 1) * SNAKE_BLOCK
        y = random.randint(0, rows - 1) * SNAKE_BLOCK
        if (x, y) not in snake:
            return (x, y)


def draw_snake(snake):
    for i, (x, y) in enumerate(snake):
        rect = pygame.Rect(x, y, SNAKE_BLOCK, SNAKE_BLOCK)
        if i == 0:
            pygame.draw.rect(screen, YELLOW, rect)
            eye_w = SNAKE_BLOCK // 6
            eyex = x + (SNAKE_BLOCK - eye_w) if direction == "LEFT" else x + eye_w
            eye_y1 = y + SNAKE_BLOCK // 4
            eye_y2 = y + (SNAKE_BLOCK * 3 // 4) - eye_w
            pygame.draw.rect(screen, BLACK, (eyex, eye_y1, eye_w, eye_w))
            pygame.draw.rect(screen, BLACK, (eyex, eye_y2, eye_w, eye_w))
        else:
            pygame.draw.rect(screen, GREEN, rect)
            pygame.draw.rect(screen, DARK, rect, 1)


def show_score(score, highscore):
    txt = f"Score: {score}   High: {highscore}"
    surf = mid_font.render(txt, True, WHITE)
    screen.blit(surf, (10, 10))


def start_screen():
    screen.fill(BG_COL)
    draw_text("SNAKE", big_font, YELLOW, (WIN_W//2, WIN_H//2 - 60))
    draw_text("Arrow keys to move", mid_font, WHITE, (WIN_W//2, WIN_H//2 - 10))
    draw_text("P = Pause   Q = Quit", small_font, WHITE, (WIN_W//2, WIN_H//2 + 20))
    draw_text("Press any arrow key to start", small_font, WHITE, (WIN_W//2, WIN_H//2 + 60))
    pygame.display.update()

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key in (pygame.K_LEFT, pygame.K_RIGHT, pygame.K_UP, pygame.K_DOWN):
                    return
                if event.key == pygame.K_q:
                    pygame.quit()
                    sys.exit()
        clock.tick(10)


def game_over_screen(score):
    screen.fill(BG_COL)
    draw_text("GAME OVER", big_font, RED, (WIN_W//2, WIN_H//2 - 50))
    draw_text(f"Score: {score}", mid_font, WHITE, (WIN_W//2, WIN_H//2 + 0))
    draw_text("Press R to play again  •  Q to quit", small_font, WHITE, (WIN_W//2, WIN_H//2 + 50))
    pygame.display.update()

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_r:
                    return True
                elif event.key == pygame.K_q:
                    pygame.quit()
                    sys.exit()
        clock.tick(10)


def main():
    global direction
    snake = [
        (WIN_W // 2, WIN_H // 2),
        (WIN_W // 2 - SNAKE_BLOCK, WIN_H // 2),
        (WIN_W // 2 - 2 * SNAKE_BLOCK, WIN_H // 2),
    ]

    direction = "RIGHT"
    score = 0
    highscore = 0

    start_screen()

    running = True
    paused = False

    food_pos = grid_random_position(snake)

    fps = BASE_FPS

    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
                break
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_p:
                    paused = not paused
                if event.key == pygame.K_q:
                    running = False
                    break
                if event.key == pygame.K_LEFT and direction != "RIGHT":
                    direction = "LEFT"
                elif event.key == pygame.K_RIGHT and direction != "LEFT":
                    direction = "RIGHT"
                elif event.key == pygame.K_UP and direction != "DOWN":
                    direction = "UP"
                elif event.key == pygame.K_DOWN and direction != "UP":
                    direction = "DOWN"

        if not running:
            break

        if paused:
            draw_text("PAUSED", big_font, WHITE, (WIN_W//2, WIN_H//2))
            pygame.display.update()
            clock.tick(5)
            continue

        head_x, head_y = snake[0]
        if direction == "RIGHT":
            head_x += SNAKE_BLOCK
        elif direction == "LEFT":
            head_x -= SNAKE_BLOCK
        elif direction == "UP":
            head_y -= SNAKE_BLOCK
        elif direction == "DOWN":
            head_y += SNAKE_BLOCK

        new_head = (head_x, head_y)

        if (head_x < 0) or (head_x >= WIN_W) or (head_y < 0) or (head_y >= WIN_H):
            if score > highscore:
                highscore = score
            again = game_over_screen(score)
            if again:
                main()
            return

        if new_head in snake:
            if score > highscore:
                highscore = score
            again = game_over_screen(score)
            if again:
                main()
            return

        snake.insert(0, new_head)

        if new_head == food_pos:
            score += 1
            fps = min(MAX_FPS, BASE_FPS + score // FPS_INCREASE_EVERY)
            food_pos = grid_random_position(snake)
        else:
            snake.pop()

        screen.fill(BG_COL)

        for gx in range(0, WIN_W, SNAKE_BLOCK):
            pygame.draw.line(screen, (20, 20, 30), (gx, 0), (gx, WIN_H))
        for gy in range(0, WIN_H, SNAKE_BLOCK):
            pygame.draw.line(screen, (20, 20, 30), (0, gy), (WIN_W, gy))

        fx, fy = food_pos
        food_rect = pygame.Rect(fx, fy, SNAKE_BLOCK, SNAKE_BLOCK)
        pygame.draw.ellipse(screen, RED, food_rect)

        draw_snake(snake)
        show_score(score, highscore)

        draw_text("P: Pause  •  R: Restart after Game Over", small_font, WHITE, (WIN_W//2, WIN_H - 12))

        pygame.display.update()
        clock.tick(fps)

    pygame.quit()
    sys.exit()


if __name__ == "__main__":
    main()
