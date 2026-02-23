import random
from dataclasses import dataclass

import pygame

WIDTH, HEIGHT = 900, 600
PADDLE_WIDTH, PADDLE_HEIGHT = 16, 120
BALL_SIZE = 16
PADDLE_SPEED = 7
BALL_BASE_SPEED = 6
WHITE = (245, 245, 245)
BLACK = (18, 18, 18)
ACCENT = (80, 220, 255)


@dataclass
class Paddle:
    x: int
    y: float
    speed: int = PADDLE_SPEED

    def move_up(self):
        self.y = max(0, self.y - self.speed)

    def move_down(self):
        self.y = min(HEIGHT - PADDLE_HEIGHT, self.y + self.speed)

    @property
    def rect(self):
        return pygame.Rect(self.x, int(self.y), PADDLE_WIDTH, PADDLE_HEIGHT)


@dataclass
class Ball:
    x: float
    y: float
    vx: float
    vy: float

    def update(self):
        self.x += self.vx
        self.y += self.vy

        if self.y <= 0:
            self.y = 0
            self.vy *= -1
        elif self.y >= HEIGHT - BALL_SIZE:
            self.y = HEIGHT - BALL_SIZE
            self.vy *= -1

    @property
    def rect(self):
        return pygame.Rect(int(self.x), int(self.y), BALL_SIZE, BALL_SIZE)


class PongGame:
    def __init__(self):
        self.left = Paddle(30, HEIGHT / 2 - PADDLE_HEIGHT / 2)
        self.right = Paddle(WIDTH - 30 - PADDLE_WIDTH, HEIGHT / 2 - PADDLE_HEIGHT / 2)
        self.left_score = 0
        self.right_score = 0
        self.rally_hits = 0
        self.ball = self._new_ball(random.choice([-1, 1]))

    def _new_ball(self, direction: int):
        angle = random.uniform(-0.6, 0.6)
        vx = direction * BALL_BASE_SPEED
        vy = BALL_BASE_SPEED * angle
        return Ball(WIDTH / 2 - BALL_SIZE / 2, HEIGHT / 2 - BALL_SIZE / 2, vx, vy)

    def reset_ball(self, direction: int):
        self.rally_hits = 0
        self.ball = self._new_ball(direction)

    def ai_follow_ball(self, paddle: Paddle):
        center = paddle.y + PADDLE_HEIGHT / 2
        target = self.ball.y + BALL_SIZE / 2
        if target < center - 10:
            paddle.move_up()
        elif target > center + 10:
            paddle.move_down()

    def step(self):
        self.ball.update()

        if self.ball.rect.colliderect(self.left.rect) and self.ball.vx < 0:
            self.ball.x = self.left.x + PADDLE_WIDTH
            self.ball.vx *= -1.03
            offset = ((self.ball.y + BALL_SIZE / 2) - (self.left.y + PADDLE_HEIGHT / 2)) / (PADDLE_HEIGHT / 2)
            self.ball.vy += offset * 1.6
            self.rally_hits += 1

        if self.ball.rect.colliderect(self.right.rect) and self.ball.vx > 0:
            self.ball.x = self.right.x - BALL_SIZE
            self.ball.vx *= -1.03
            offset = ((self.ball.y + BALL_SIZE / 2) - (self.right.y + PADDLE_HEIGHT / 2)) / (PADDLE_HEIGHT / 2)
            self.ball.vy += offset * 1.6
            self.rally_hits += 1

        if self.ball.x < -BALL_SIZE:
            self.right_score += 1
            self.reset_ball(direction=-1)
            return "right_scores"

        if self.ball.x > WIDTH:
            self.left_score += 1
            self.reset_ball(direction=1)
            return "left_scores"

        return "in_play"


def draw_game(screen, game: PongGame):
    screen.fill(BLACK)

    for y in range(0, HEIGHT, 28):
        pygame.draw.rect(screen, (50, 50, 50), (WIDTH // 2 - 2, y, 4, 14))

    pygame.draw.rect(screen, ACCENT, game.left.rect)
    pygame.draw.rect(screen, WHITE, game.right.rect)
    pygame.draw.rect(screen, WHITE, game.ball.rect)

    font = pygame.font.SysFont("consolas", 48)
    left_text = font.render(str(game.left_score), True, ACCENT)
    right_text = font.render(str(game.right_score), True, WHITE)
    screen.blit(left_text, (WIDTH // 2 - 90, 30))
    screen.blit(right_text, (WIDTH // 2 + 50, 30))
