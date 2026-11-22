import os
import random
import sys
import pygame

WIDTH, HEIGHT = 960, 540
WHITE = (255, 255, 255)
RED = (200, 40, 50)
DARK_RED = (140, 25, 35)
GOLD = (255, 215, 90)

FONT_PATH = os.path.join(
    os.path.dirname(__file__), "..", "assets", "fonts", "PressStart2P-Regular.ttf"
)


def load_font(size):
    try:
        return pygame.font.Font(FONT_PATH, size)
    except (FileNotFoundError, OSError):
        return pygame.font.Font(None, size + 10)


def draw_text(screen, text, font, color, center, shadow=None):
    if shadow:
        shadow_surface = font.render(text, True, shadow)
        screen.blit(shadow_surface, shadow_surface.get_rect(center=(center[0] + 4, center[1] + 4)))
    surface = font.render(text, True, color)
    screen.blit(surface, surface.get_rect(center=center))


def draw_houses(bg):
    ground_y = 480
    pygame.draw.rect(bg, (225, 230, 240), (0, ground_y, WIDTH, HEIGHT - ground_y))
    for x in range(30, WIDTH, 170):
        w, h = 110, 70
        base = ground_y
        pygame.draw.rect(bg, (70, 40, 45), (x, base - h, w, h))
        pygame.draw.polygon(
            bg, (235, 240, 250),
            [(x - 10, base - h), (x + w + 10, base - h), (x + w // 2, base - h - 50)],
        )
        pygame.draw.rect(bg, (120, 50, 40), (x + w - 35, base - h - 40, 16, 30))
        pygame.draw.rect(bg, (235, 240, 250), (x + w - 38, base - h - 46, 22, 8))
        pygame.draw.rect(bg, GOLD, (x + 18, base - 50, 20, 20))
        pygame.draw.rect(bg, GOLD, (x + 60, base - 50, 20, 20))


def create_background():
    bg = pygame.Surface((WIDTH, HEIGHT))
    top, bottom = (10, 15, 45), (45, 70, 120)
    for y in range(HEIGHT):
        t = y / HEIGHT
        color = tuple(int(top[i] + (bottom[i] - top[i]) * t) for i in range(3))
        pygame.draw.line(bg, color, (0, y), (WIDTH, y))
    rng = random.Random(7)
    for _ in range(60):
        pygame.draw.rect(bg, WHITE, (rng.randint(0, WIDTH), rng.randint(0, 300), 2, 2))
    pygame.draw.circle(bg, (245, 240, 200), (830, 90), 36)
    draw_houses(bg)
    return bg


def make_snow(count=90):
    return [
        [random.randint(0, WIDTH), random.randint(0, HEIGHT),
         random.uniform(0.5, 2.0), random.choice([2, 3, 4])]
        for _ in range(count)
    ]


def update_snow(snow):
    for flake in snow:
        flake[1] += flake[2]
        flake[0] += 0.3
        if flake[1] > HEIGHT:
            flake[1] = -5
            flake[0] = random.randint(0, WIDTH)
        if flake[0] > WIDTH:
            flake[0] = 0


def draw_snow(screen, snow):
    for x, y, _, size in snow:
        pygame.draw.rect(screen, WHITE, (int(x), int(y), size, size))


def make_buttons():
    labels = ["Play", "How to Play", "Exit"]
    buttons = []
    for i, label in enumerate(labels):
        rect = pygame.Rect(0, 0, 360, 56)
        rect.center = (WIDTH // 2, 255 + i * 76)
        buttons.append((label, rect))
    return buttons


def get_clicked_button(buttons, pos):
    for label, rect in buttons:
        if rect.collidepoint(pos):
            return label
    return None


def draw_menu(screen, title_font, button_font, buttons):
    draw_text(screen, "Santa's Drop", title_font, WHITE, (WIDTH // 2, 110), shadow=RED)
    mouse_pos = pygame.mouse.get_pos()
    for label, rect in buttons:
        color = RED if rect.collidepoint(mouse_pos) else DARK_RED
        pygame.draw.rect(screen, color, rect, border_radius=8)
        pygame.draw.rect(screen, WHITE, rect, width=3, border_radius=8)
        draw_text(screen, label, button_font, WHITE, rect.center)


def draw_panel(screen):
    panel = pygame.Surface((800, 380), pygame.SRCALPHA)
    panel.fill((0, 0, 0, 150))
    screen.blit(panel, panel.get_rect(center=(WIDTH // 2, 270)))


def draw_how_to_play(screen, heading_font, small_font):
    draw_panel(screen)
    draw_text(screen, "How to Play", heading_font, GOLD, (WIDTH // 2, 110))
    lines = [
        "Up / Down arrows: move Santa",
        "Space bar: drop a present",
        "Avoid birds, power lines, planes",
        "Drop presents into chimneys",
        "Press ESC to go back",
    ]
    for i, line in enumerate(lines):
        draw_text(screen, line, small_font, WHITE, (WIDTH // 2, 180 + i * 50))


def main():
    pygame.init()
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption("Santa's Drop")
    clock = pygame.time.Clock()

    title_font = load_font(48)
    heading_font = load_font(32)
    button_font = load_font(22)
    small_font = load_font(16)

    background = create_background()
    snow = make_snow()
    buttons = make_buttons()

    state = "menu"
    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                state = "menu"
            elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                if state == "menu":
                    clicked = get_clicked_button(buttons, event.pos)
                    if clicked == "Play":
                        state = "play"
                    elif clicked == "How to Play":
                        state = "howto"
                    elif clicked == "Exit":
                        running = False

        update_snow(snow)
        screen.blit(background, (0, 0))
        draw_snow(screen, snow)

        if state == "menu":
            draw_menu(screen, title_font, button_font, buttons)
        elif state == "howto":
            draw_how_to_play(screen, heading_font, small_font)
        elif state == "play":
            draw_text(screen, "Coming soon! (ESC)", small_font, WHITE, (WIDTH // 2, HEIGHT // 2))

        pygame.display.flip()
        clock.tick(60)

    pygame.quit()
    sys.exit()


if __name__ == "__main__":
    main()