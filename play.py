import os
import pickle

import neat
import pygame

from pong_core import HEIGHT, PADDLE_HEIGHT, PongGame, WIDTH, draw_game

CONFIG_PATH = os.path.join(os.path.dirname(__file__), "neat_config.txt")
WINNER_PATH = os.path.join(os.path.dirname(__file__), "winner.pkl")


def load_ai():
    if not os.path.exists(WINNER_PATH):
        raise FileNotFoundError("winner.pkl not found. Run `python train_neat.py` first.")

    config = neat.Config(
        neat.DefaultGenome,
        neat.DefaultReproduction,
        neat.DefaultSpeciesSet,
        neat.DefaultStagnation,
        CONFIG_PATH,
    )

    with open(WINNER_PATH, "rb") as f:
        winner = pickle.load(f)

    return neat.nn.FeedForwardNetwork.create(winner, config)


def main():
    net = load_ai()

    pygame.init()
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption("Pong vs NEAT AI")
    clock = pygame.time.Clock()

    game = PongGame()
    running = True

    while running:
        clock.tick(60)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        keys = pygame.key.get_pressed()
        if keys[pygame.K_w] or keys[pygame.K_UP]:
            game.left.move_up()
        if keys[pygame.K_s] or keys[pygame.K_DOWN]:
            game.left.move_down()

        right_center = game.right.y + PADDLE_HEIGHT / 2
        ball_center_y = game.ball.y + 8

        inputs = (
            game.right.y / HEIGHT,
            right_center / HEIGHT,
            game.ball.x / WIDTH,
            game.ball.y / HEIGHT,
            game.ball.vx / 12.0,
            game.ball.vy / 12.0,
            (ball_center_y - right_center) / HEIGHT,
        )

        out = net.activate(inputs)[0]
        if out < 0.4:
            game.right.move_up()
        elif out > 0.6:
            game.right.move_down()

        game.step()
        draw_game(screen, game)
        pygame.display.flip()

    pygame.quit()


if __name__ == "__main__":
    main()
