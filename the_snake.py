from random import choice, randint
from abc import ABC, abstractmethod

import pygame
import random

# Константы для размеров поля и сетки:
SCREEN_WIDTH, SCREEN_HEIGHT = 640, 480
GRID_SIZE = 20
GRID_WIDTH = SCREEN_WIDTH // GRID_SIZE
GRID_HEIGHT = SCREEN_HEIGHT // GRID_SIZE

# Направления движения:
UP = (0, -1)
DOWN = (0, 1)
LEFT = (-1, 0)
RIGHT = (1, 0)

# Цвет фона - черный:
BOARD_BACKGROUND_COLOR = (0, 0, 0)

# Цвет границы ячейки
BORDER_COLOR = (93, 216, 228)

# Цвет яблока
APPLE_COLOR = (255, 0, 0)

# Цвет змейки
SNAKE_COLOR = (0, 255, 0)

# Скорость движения змейки:
SPEED = 5

# Настройка игрового окна:
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT), 0, 32)

# Заголовок окна игрового поля:
pygame.display.set_caption('Змейка')

# Настройка времени:
clock = pygame.time.Clock()


# Все классы игры:
class GameObject(ABC):
    # Основной абстрактный класс, объед. все объекты игры.
    def __init__(self, position, body_color):
        self.position = position
        self.body_color = body_color
    
    @abstractmethod
    def draw(self):
        pass

class Apple(GameObject):
    # Класс объекта Яблоко.
    def __init__(self, body_color = APPLE_COLOR):
        super().__init__((0,0), body_color)
        self.randomize_position()

    def randomize_position(self):
        # Рандомно определяем новую позицию для Яблока на полотне.
        rand_row = random.randint(0, GRID_HEIGHT - 1)
        rand_col = random.randint(0, GRID_WIDTH - 1)
        self.position = (rand_col * GRID_SIZE, rand_row * GRID_SIZE)

    def draw(self):
        # Отрисовка Яблока(взято из задания).
        rect = pygame.Rect(self.position, (GRID_SIZE, GRID_SIZE))
        pygame.draw.rect(screen, self.body_color, rect)
        pygame.draw.rect(screen, BORDER_COLOR, rect, 1)

class Snake(GameObject):
    # Класс объекта Змейка.
    def __init__(self, position, body_color = SNAKE_COLOR):
        super().__init__(position, body_color)
        self.length = 1
        self.positions = [position]
        self.direction = RIGHT
        self.next_direction = None
        self.last = None
    
    def update_direction(self):
        # Изменяем направление Змейки на новое, задаваемое пользователем.
        if self.next_direction:
            self.direction = self.next_direction
            self.next_direction = None

    def move(self):
        # Перемещение Змейки на одну позицию в соотв. с новым направлением.
        self.update_direction()

        head_x, head_y = self.positions[0]
        dir_x, dir_y = self.direction
        new_head = (head_x + dir_x * GRID_SIZE, head_y + dir_y * GRID_SIZE)

        self.positions.insert(0, new_head)

        if len(self.positions) > self.length:
            self.last = self.positions.pop()
        else:
            self.last = None

    def draw(self):
        # Отрисовка Змейки(взято из задания).
        for position in self.positions[:-1]:
            rect = (pygame.Rect(position, (GRID_SIZE, GRID_SIZE)))
            pygame.draw.rect(screen, self.body_color, rect)
            pygame.draw.rect(screen, BORDER_COLOR, rect, 1)

        # Отрисовка головы змейки
        head_rect = pygame.Rect(self.positions[0], (GRID_SIZE, GRID_SIZE))
        pygame.draw.rect(screen, self.body_color, head_rect)
        pygame.draw.rect(screen, BORDER_COLOR, head_rect, 1)

        # Затирание последнего сегмента
        if self.last:
            last_rect = pygame.Rect(self.last, (GRID_SIZE, GRID_SIZE))
            pygame.draw.rect(screen, BOARD_BACKGROUND_COLOR, last_rect)

    def get_head_position(self):
        # Получаем след. позицию головы.
        return  self.positions[0]

    def reset(self):
        # Полный сброс Змейки.
        self.length = 1
        self.positions = [self.position]
        self.direction = RIGHT
        self.next_direction = None
        self.last = None

def handle_keys(game_object):
    # Обработка нажатий (взято из задания).
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            raise SystemExit
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_UP and game_object.direction != DOWN:
                game_object.next_direction = UP
            elif event.key == pygame.K_DOWN and game_object.direction != UP:
                game_object.next_direction = DOWN
            elif event.key == pygame.K_LEFT and game_object.direction != RIGHT:
                game_object.next_direction = LEFT
            elif event.key == pygame.K_RIGHT and game_object.direction != LEFT:
                game_object.next_direction = RIGHT






def main():
    # Инициализация PyGame:
    pygame.init()
    # Экземпляры классов:
    snake = Snake((SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2), SNAKE_COLOR)
    apple = Apple(APPLE_COLOR)
    
    # Беск. цикл с игрой:
    while True:
        clock.tick(SPEED)
        
        handle_keys(snake)
        snake.update_direction()
        snake.move()

        # Змейка кушает Яблоко и растет жестко.
        if snake.get_head_position() == apple.position:
            snake.length += 1
            apple.randomize_position()

            # Только если Яблоко не спавнится на ее голове.
            while apple.position in snake.positions:
                apple.randomize_position()

        # Змейка врезается в себя(
        if snake.get_head_position() in snake.positions[1:]:
            snake.reset()
        
        # Змейка сбегает(
        head_x, head_y = snake.get_head_position()
        if head_x < 0 or head_x >= SCREEN_WIDTH or head_y < 0 or head_y >= SCREEN_HEIGHT:
            snake.reset()

        screen.fill(BOARD_BACKGROUND_COLOR)

        apple.draw()
        snake.draw()

        pygame.display.update()


if __name__ == '__main__':
    main()
