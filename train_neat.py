import os
import pickle

import neat
import pygame

from pong_core import HEIGHT, PADDLE_HEIGHT, PongGame, WIDTH

CONFIG_PATH = os.path.join(os.path.dirname(__file__), "neat_config.txt")
WINNER_PATH = os.path.join(os.path.dirname(__file__), "winner.pkl")


def eval_genome(genome, config):
    net = neat.nn.FeedForwardNetwork.create(genome, config)
    game = PongGame()

    fitness = 0.0
    frames = 0
    max_frames = 4000

    while frames < max_frames:
        frames += 1

        game.ai_follow_ball(game.left)

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

        status = game.step()
        fitness += 0.02

        if status == "right_scores":
            fitness += 4.0
        elif status == "left_scores":
            fitness -= 6.0
            break

        if game.ball.vx > 0:
            distance = abs((game.right.y + PADDLE_HEIGHT / 2) - (game.ball.y + 8))
            fitness += max(0, 1.2 - distance / HEIGHT) * 0.01

    genome.fitness = fitness
    return fitness


def eval_genomes(genomes, config):
    for _, genome in genomes:
        eval_genome(genome, config)


def run_training(generations=40):
    config = neat.Config(
        neat.DefaultGenome,
        neat.DefaultReproduction,
        neat.DefaultSpeciesSet,
        neat.DefaultStagnation,
        CONFIG_PATH,
    )

    p = neat.Population(config)
    p.add_reporter(neat.StdOutReporter(True))
    p.add_reporter(neat.StatisticsReporter())

    winner = p.run(eval_genomes, generations)

    with open(WINNER_PATH, "wb") as f:
        pickle.dump(winner, f)

    print(f"Saved trained genome to: {WINNER_PATH}")


def preview_winner():
    if not os.path.exists(WINNER_PATH):
        print("No winner.pkl found. Run training first.")
        return

    config = neat.Config(
        neat.DefaultGenome,
        neat.DefaultReproduction,
        neat.DefaultSpeciesSet,
        neat.DefaultStagnation,
        CONFIG_PATH,
    )

    with open(WINNER_PATH, "rb") as f:
        winner = pickle.load(f)

    net = neat.nn.FeedForwardNetwork.create(winner, config)

    pygame.init()
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption("NEAT Pong - Winner Preview")
    clock = pygame.time.Clock()

    from pong_core import draw_game

    game = PongGame()
    running = True

    while running:
        clock.tick(60)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        game.ai_follow_ball(game.left)

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
    run_training(generations=50)
    #preview_winner()