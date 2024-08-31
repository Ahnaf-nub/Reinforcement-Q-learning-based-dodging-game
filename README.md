# Dodging game with Reinforcement Learning

This repository contains a simple Reinforcement Learning (RL) based game developed using Python and Pygame. The game simulates a scenario where the player controls a character that must dodge falling objects (kunai) to survive. The character's movements are controlled by a Q-learning algorithm, which allows it to learn and improve its ability to avoid collisions over time.

https://github.com/user-attachments/assets/8b7fa1e7-295b-4c41-a654-95633c5b1d84

Game Description
In the game, the player is represented by a green square at the bottom of the screen, and the falling objects are represented by red rectangles. The objective is to avoid as many falling objects as possible, maximizing the score. The player starts in the middle of the screen and can move left or right to avoid the falling objects.

The game uses Q-learning, a popular reinforcement learning algorithm, to train the player to make decisions based on the current state of the game. Over time, the player learns the best actions to take in different situations, improving its ability to survive.

How It Works
State Space: The state is represented by the player's position on the x-axis and the position of the nearest falling object. This state is used as input for the Q-learning algorithm.

Action Space: The player has three possible actions:

Move left
Move right
Stay in place
Rewards: The player receives a positive reward (+10) for surviving each time step without colliding with a falling object. A collision results in a significant negative reward (-100).

Q-learning Algorithm:

Q-Table: The algorithm maintains a Q-table that maps state-action pairs to expected future rewards.
Epsilon-Greedy Policy: During training, the player uses an epsilon-greedy policy to balance exploration (trying new actions) and exploitation (choosing the best-known action).
Learning and Decay: As the game progresses, the learning rate and epsilon value decay to fine-tune the model and reduce random actions.

You can install the required packages using pip:
```
pip install pygame numpy
```
How to Run the Game
Clone the repository:
```
git clone https://github.com/your-username/dodge-and-escape-rl.git
cd dodge-and-escape-rl
```
Run the game:

```
python dodge_and_escape.py
```
The game will automatically start, and the player will begin training to avoid the falling objects.

### Training Process
The game runs for a specified number of episodes (1000 by default), where each episode represents a full game run from start to finish. The Q-learning algorithm updates the Q-table after each action to improve future performance.

As the training progresses, the player will become better at avoiding falling objects, and the number of collisions should decrease. The epsilon value will decay over time, reducing random actions and focusing more on the learned strategy.
