# Pong AI Using NEAT (Python)

This project implements a classic **Pong game** where the **right paddle is controlled by a neural network evolved using NEAT (NeuroEvolution of Augmenting Topologies)**.  
During training, the left paddle is controlled by a simple heuristic AI. During gameplay, the left paddle is controlled by the player.

The neural network learns how to play Pong by evolving its structure and weights over generations—**no backpropagation or labeled data required**.

---

## Features

- Classic Pong game built on **Pygame**
- AI paddle trained using **NEAT (neat-python)**
- Feed-forward neural network with **7 normalized inputs**
- Fitness function rewards survival, ball tracking, and scoring
- Human vs AI gameplay after training

---

## Setup

```bash
python3 -m venv .venv source .venv/bin/activate
pip install -r requirements.txt
```

---

## Training the AI

```bash
python train_neat.py
```

---

## Playing Against the AI

```bash
python play.py
```

### Controls (Left Paddle)

- `W` / `Up Arrow` → move up  
- `S` / `Down Arrow` → move down  

