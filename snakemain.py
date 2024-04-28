import pygame
import sys
import time
import random


BLACK = pygame.Color(0, 0, 0)  # map
WHITE = pygame.Color(255, 255, 255)  # táo
RED = pygame.Color(255, 0, 0)  # over
GREEN = pygame.Color(0, 255, 0) # rắn

# Kích thước khung hình
FRAME_SIZE_X = 720
FRAME_SIZE_Y = 480

# Hướng di chuyển
UP = (0, -10)
DOWN = (0, 10)
LEFT = (-10, 0)
RIGHT = (10, 0)

class Snake:
    def __init__(self, start_pos):
        self.body = [start_pos, (start_pos[0] - 10, start_pos[1]), (start_pos[0] - 20, start_pos[1])]
        # hướng ban đầu đi là bên phải
        self.direction = RIGHT
        self.change_to = self.direction

    def update_direction(self, event_key):
    
        if event_key in [pygame.K_UP, ord('w')] and self.direction != DOWN:
            self.change_to = UP
        elif event_key in [pygame.K_DOWN, ord('s')] and self.direction != UP:
            self.change_to = DOWN
        elif event_key in [pygame.K_LEFT, ord('a')] and self.direction != RIGHT:
            self.change_to = LEFT
        elif event_key in [pygame.K_RIGHT, ord('d')] and self.direction != LEFT:
            self.change_to = RIGHT
        # điều khiển hướng đi
        self.direction = self.change_to
    # di chuyển
    def move(self):
        head = self.body[0]
        new_head = (head[0] + self.direction[0], head[1] + self.direction[1])
        self.body.insert(0, new_head)
    # co lại 
    def shrink(self):
        self.body.pop()

     # kiểm tra xem rắn có đâm dính người nó hay k
    def has_collided(self):
        head = self.body[0]
        return head in self.body[1:]

class Food:
    def __init__(self):
        self.position = self.randomize_position()
    # xuất hiện ngẫu nhiên trong map
    def randomize_position(self):
        x = random.randrange(1, FRAME_SIZE_X // 10) * 10
        y = random.randrange(1, FRAME_SIZE_Y // 10) * 10
        return (x, y)
    # hồi sinh lai táo
    def respawn(self):
        self.position = self.randomize_position()

class Game:
    def __init__(self):
        pygame.init()
        self.window = pygame.display.set_mode((FRAME_SIZE_X, FRAME_SIZE_Y))
        pygame.display.set_caption('Snake Eat')
        self.level = pygame.time.Clock()
        self.snake = Snake((100, 50))
        
        self.food = Food()
        self.score = 0
    
    def game_over(self):
        # hiển thị khi thua
        font = pygame.font.SysFont('times new roman', 90)
        text_surface = font.render('Bạn đã chết', True, RED)
        text_rect = text_surface.get_rect()
        # nơi xuất hiện chữ
        text_rect.midtop = (FRAME_SIZE_X // 2, FRAME_SIZE_Y // 3)
        self.window.fill(BLACK)
        self.window.blit(text_surface, text_rect)
        pygame.display.flip()
        time.sleep(3)
        pygame.quit()
        sys.exit()
    
    def show_score(self):
        font = pygame.font.SysFont('consolas', 20)
        score_surface = font.render(f'Score: {self.score}', True, RED)
        score_rect = score_surface.get_rect()
        score_rect.midtop = (FRAME_SIZE_X // 10, 15)
        self.window.blit(score_surface, score_rect)
    
    
    def run(self):
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                elif event.type == pygame.KEYDOWN:
                    self.snake.update_direction(event.key)
            
            # Di chuyển 
            self.snake.move()
            
            # Nếu rắn ăn táo
            if self.snake.body[0] == self.food.position:
                self.score += 1
                self.food.respawn()
            else:
                self.snake.shrink()  #
            
            # Kiểm tra va chạm
            if (
                self.snake.body[0][0] < 0 or
                self.snake.body[0][0] >= FRAME_SIZE_X or
                self.snake.body[0][1] < 0 or
                self.snake.body[0][1] >= FRAME_SIZE_Y or
                self.snake.has_collided()
            ):
                self.game_over()
            
            # Làm sạch và vẽ lại màn hình
            self.window.fill(BLACK)
            for segment in self.snake.body:
                pygame.draw.rect(self.window, GREEN, pygame.Rect(segment[0], segment[1], 10, 10))
            pygame.draw.rect(self.window, WHITE, pygame.Rect(self.food.position[0], self.food.position[1], 10, 10))
            
            self.show_score()
            pygame.display.update()
            mucdo= 10
            # Độ khó của game
            self.level.tick(mucdo)

# Khởi động trò chơi
if __name__ == "__main__":
    game = Game()
    game.run()
