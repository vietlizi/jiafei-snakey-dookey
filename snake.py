import pygame
import random

pygame.init()

WINDOW_SIZE = 500
WINDOW = pygame.display.set_mode((WINDOW_SIZE, WINDOW_SIZE))
pygame.display.set_caption("Jiafei's Snakey Dookey")

BACKGROUND = pygame.image.load("background.png")

WHITE = (255, 255, 255)
GREEN = (0, 255, 0)
RED = (255, 0, 0)
YELLOW = (255, 255, 0)
BLUE = (0, 0, 255)

class Snake:
    def __init__(self):
        self.body = [(250, 250)]
        self.direction = (1, 0)
        self.color = GREEN

    def move(self):
        head = self.body[-1]
        new_head = (head[0] + self.direction[0]*10, head[1] + self.direction[1]*10)
        self.body.append(new_head)
        self.body.pop(0)

    def grow(self):
        tail = self.body[0]
        new_tail = (tail[0] - self.direction[0]*10, tail[1] - self.direction[1]*10)
        self.body.insert(0, new_tail)

    def check_collision(self):
        head = self.body[-1]
        return head in self.body[:-1] or not (0 <= head[0] < WINDOW_SIZE and 0 <= head[1] < WINDOW_SIZE)

    def draw(self):
        for segment in self.body:
            pygame.draw.rect(WINDOW, self.color, (segment[0], segment[1], 10, 10))

class Food:
    def __init__(self):
        self.position = (random.randint(0, 49) * 10, random.randint(0, 49) * 10)

    def respawn(self):
        self.position = (random.randint(0, 49) * 10, random.randint(0, 49) * 10)

    def draw(self):
        pygame.draw.rect(WINDOW, RED, (*self.position, 10, 10))

class Score:
    def __init__(self):
        self.font = pygame.font.Font(None, 36)
        self.score = 0

    def increase(self):
        self.score += 1

    def draw(self):
        score_text = self.font.render("Score: " + str(self.score), True, WHITE)
        WINDOW.blit(score_text, (10, 10))

    def message(self, msg, color, position):
        text = self.font.render(msg, True, color)
        WINDOW.blit(text, position)

def main():
    snake = Snake()
    food = Food()
    score = Score()
    clock = pygame.time.Clock()
    game_over = False

    while not game_over:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP and snake.direction != (0, 1):
                    snake.direction = (0, -1)
                elif event.key == pygame.K_DOWN and snake.direction != (0, -1):
                    snake.direction = (0, 1)
                elif event.key == pygame.K_LEFT and snake.direction != (1, 0):
                    snake.direction = (-1, 0)
                elif event.key == pygame.K_RIGHT and snake.direction != (-1, 0):
                    snake.direction = (1, 0)

        if not game_over:
            snake.move()

            if snake.body[-1] == food.position:
                snake.grow()
                food.respawn()
                score.increase()

                if score.score == 50:
                    snake.color = YELLOW
                    score.message("Keep it up!", YELLOW, (200, 200))
                elif score.score == 100:
                    snake.color = BLUE
                    score.message("Keep it up!", BLUE, (200, 200))

            if snake.check_collision():
                game_over = True

            WINDOW.blit(BACKGROUND, (0, 0))
            snake.draw()
            food.draw()
            score.draw()
            pygame.display.update()
            clock.tick(10)

    score.message("Game Over", RED, (200, 200))
    pygame.display.update()
    pygame.time.wait(2000)

if __name__ == "__main__":
    main()
