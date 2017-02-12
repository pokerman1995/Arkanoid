import pygame
import sys
from pygame.locals import *


class PlayerSprite(pygame.sprite.Sprite):
    def __init__(self, x, y, width, height):
        pygame.sprite.Sprite.__init__(self)
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.rect = pygame.Rect(x, y, width, height)

    def move(self, dx):
        if self.rect.x + dx + self.rect.width < 800 and self.rect.x + dx > 0:
            self.rect.x += dx
            self.x += dx


class BallSprite(pygame.sprite.Sprite):
    def __init__(self, x, y, radius, dx, dy):
        pygame.sprite.Sprite.__init__(self)
        self.x = x
        self.y = y
        self.radius = radius
        self.dx = dx
        self.dy = dy
        self.rect = pygame.Rect(x - radius, y - radius, 2 * radius, 2 * radius)

    def move(self):
        hit = 0

        if self.y + self.dy + self.radius / 2 > screen_rect.y + screen_rect.height and screen_rect.x < self.x < screen_rect.x + screen_rect.width:
            self.dy *= 1
            global end_screen
            end_screen = True

        elif self.y + self.dy - self.radius / 2 < screen_rect.y and screen_rect.x < self.x < screen_rect.x + screen_rect.width:
            self.dy *= -1

        elif self.x + self.dx + self.radius / 2 > screen_rect.x + screen_rect.width or self.x + self.dx - self.radius / 2 < screen_rect.x:
            self.dx *= -1

        elif player.y + player.y >= self.y + self.dy + self.radius / 2 >= player.y and player.x <= self.x + self.dx <= player.x + player.width:
            dist = self.x - player.rect.centerx
            self.dy *= -1
            self.dx = int((10 * dist) / 75)

        for wall in bricks:
            rect = pygame.Rect(self.rect.x + self.dx, self.rect.y + self.dy, self.rect.width, self.rect.height)
            if rect.colliderect(wall.rect):
                if self.rect.y + self.radius * 2 <= wall.y or self.rect.y >= wall.y + wall.height:
                    self.dy *= -1
                    index = bricks.index(wall)
                    bricks.remove(wall)
                    increase_score()
                    del colors[index]
                    break
                else:
                    self.dx *= -1
                    index = bricks.index(wall)
                    bricks.remove(wall)
                    del colors[index]
                    break

        self.x += self.dx
        self.y += self.dy
        self.rect = self.rect.move(self.dx, self.dy)


class BrickSprite(pygame.sprite.Sprite):
    def __init__(self, x, y, width, height):
        pygame.sprite.Sprite.__init__(self)
        bricks.append(self)
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.rect = pygame.Rect(x, y, width, height)


pygame.init()
screen = pygame.display.set_mode((800, 600), DOUBLEBUF)
pygame.display.set_caption('Arkanoid')

background = pygame.image.load('stars.jpg')
screen.blit(background, (0, 0))

clock = pygame.time.Clock()

BLUE = (0, 0, 200)

player_position_x = 350
player_position_y = 550
player_width = 150
player_height = 20
player_position_x_change = 0

ball_position_x = 400
ball_position_y = 400
ball_position_dx = 0
ball_position_dy = 5
ball_radius = 10


player = PlayerSprite(player_position_x, player_position_y, player_width, player_height)
ball = BallSprite(ball_position_x, ball_position_y, ball_radius, ball_position_dx, ball_position_dy)

end_screen = False


def end_game(counter):
    font = pygame.font.SysFont(None, 80)
    text = font.render("Game Over", True, (255, 255, 255))
    screen.blit(text, (800 / 2 - text.get_width() / 2, 250))
    font = pygame.font.SysFont(None, 60)
    text = font.render("Punktzahl: " + str(counter), True, (255, 255, 255))
    screen.blit(text, (800 / 2 - text.get_width() / 2, 320))


def bricks_removed(counter):
    font = pygame.font.SysFont(None, 50)
    text = font.render("Punkte: " + str(counter), True, (255, 255, 255))
    screen.blit(text, ((790 - text.get_width()), 550))


def increase_score():
    global score
    score += 10


bricks, colors = [], []
for x in range(15, 775, 51):
    for y in range(15, 215, 50):
        brick = BrickSprite(x, y, 50, 20)
        colors.append(((x * 0.2) % 256, (y * 1.5) % 256))
obstacles = bricks[:]
screen_rect = pygame.Rect(0, 0, 800, 600)
# obstacles.append(screen_rect)

gameExit = False
score = 0

while not gameExit:
    clock.tick(50)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            gameExit = True
        if event.type == KEYDOWN:
            if event.key == K_LEFT:
                player_position_x_change = -10
            elif event.key == K_RIGHT:
                player_position_x_change = +10
            elif event.key == K_ESCAPE:
                sys.exit(0)
        if event.type == KEYUP:
            player_position_x_change = 0

    screen.blit(background, (0, 0))
    player.move(player_position_x_change)
    ball.move()
    if end_screen:
        end_game(score)
        pygame.display.update()
    else:
        for brick, (a, b) in zip(bricks, colors):
            pygame.draw.rect(screen, (200, a, b), brick)
        pygame.draw.rect(screen, (0, 0, 0), screen_rect, 1)
        pygame.draw.circle(screen, (255, 255, 255), (ball.x, ball.y), ball.radius)
        pygame.draw.rect(screen, BLUE, player)
        bricks_removed(score)
        pygame.display.update()

pygame.quit()
quit()
