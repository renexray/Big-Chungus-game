import pygame
import random
from os import path

TITLE = "Big Chungus!"
WIDTH = 1200
HEIGHT = 900
FPS = 60
FONT_NAME = 'arial'
HS_FILE = "hs.txt"

kebab_speed = 5
alien_y=-50
alien_x=random.randrange(0,WIDTH)
PLAYER_ACC = 1
PLAYER_FRICTION = -0.12
PLAYER_GRAV = 0.8
Alien_GRAV = 0.15
Lives = 3

PLATFORM_LIST = [(0, 890, 1200, 20)]

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
YELLOW = (255, 255, 0)
LIGHTBLUE = (0, 155, 155)
BGCOLOR = LIGHTBLUE


kebab="Carrot.png"
zaidejas="BC.png"
background_imge = pygame.image.load("bg.jpeg")
eating_sound="eat.mp3"

background_imge = pygame.transform.scale(background_imge, (WIDTH , HEIGHT))
vec = pygame.math.Vector2

class Player(pygame.sprite.Sprite):
    def __init__(self, game):
        pygame.sprite.Sprite.__init__(self)
        self.game = game
        self.image = pygame.Surface((30, 40))
        self.image = pygame.image.load(zaidejas)
        self.image = pygame.transform.scale(self.image, (200,320))
        self.rect = self.image.get_rect()
        self.rect.center = (WIDTH / 2, HEIGHT / 2)
        self.pos = vec(WIDTH / 2, HEIGHT / 2)
        self.vel = vec(0, 0)
        self.acc = vec(0, 0)

    def jump(self):

        self.rect.x += 1
        hits = pygame.sprite.spritecollide(self, self.game.platforms, False)
        self.rect.x -= 1
        if hits:
            self.vel.y = -20

    def update(self):
        self.acc = vec(0, PLAYER_GRAV)
        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT]:
            self.acc.x = -PLAYER_ACC
        if keys[pygame.K_RIGHT]:
            self.acc.x = PLAYER_ACC

        self.acc.x += self.vel.x * PLAYER_FRICTION

        self.vel += self.acc
        self.pos += self.vel + 0.5 * self.acc

        if self.pos.x > WIDTH:
            self.pos.x = 0
        if self.pos.x < 0:
            self.pos.x = WIDTH

        self.rect.midbottom = self.pos

class Kebab(pygame.sprite.Sprite):
    def __init__(self, game):
        pygame.sprite.Sprite.__init__(self)
        self.game = game
        self.image = pygame.Surface((30, 40))
        self.image = pygame.image.load(kebab)
        self.image = pygame.transform.scale(self.image, (70, 90))
        self.rect = self.image.get_rect()
        self.pos = vec(random.randrange(0,WIDTH))
        self.vel = vec(0, 0)
        self.acc = vec(0, 0)

    def update(self):
        self.acc = vec(0, Alien_GRAV)
        self.acc.x += self.vel.x * PLAYER_FRICTION
        self.vel += self.acc
        self.pos += self.vel + 0.5 * self.acc
        self.rect.midbottom = self.pos

class Platform(pygame.sprite.Sprite):
    def __init__(self, x, y, w, h):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.Surface((w, h))
        self.image.fill(BLACK)
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y

class Game:
    def __init__(self):

        pygame.init()
        pygame.mixer.init()
        self.screen = pygame.display.set_mode((WIDTH, HEIGHT))
        self.music = pygame.mixer.music.load(eating_sound)
        pygame.display.set_caption(TITLE)
        self.clock = pygame.time.Clock()
        self.running = True
        self.font_name = pygame.font.match_font(FONT_NAME)
        self.load_data()

    def load_data(self):
        self.dir = path.dirname(__file__)
        with open(path.join(self.dir, HS_FILE), 'r') as f:
            try:
                self.highscore = int(f.read())
            except:
                self.highscore = 0
    def new(self):

        self.score = 0
        self.lives = 3
        self.all_sprites = pygame.sprite.Group()
        self.platforms = pygame.sprite.Group()
        self.player = Player(self)
        self.alien = Kebab(self)
        self.all_sprites.add(self.player)
        self.all_sprites.add(self.alien)
        for plat in PLATFORM_LIST:
            p = Platform(*plat)
            self.all_sprites.add(p)
            self.platforms.add(p)
        self.run()

    def run(self):

        self.playing = True
        while self.playing:
            self.clock.tick(FPS)
            self.events()
            self.update()
            self.draw()

    def update(self):

        self.all_sprites.update()

        if self.player.vel.y > 0:
            hits = pygame.sprite.spritecollide(self.player, self.platforms, False)
            if hits:
                self.player.pos.y = hits[0].rect.top
                self.player.vel.y = 0

        if self.alien.vel.y > 0:
            hits = pygame.sprite.spritecollide(self.alien, self.platforms, False)
            if hits:
                self.alien.pos.x = random.randrange(0, WIDTH)
                self.alien.pos.y = -25
                self.alien.vel.y = 0.1
                self.alien.vel.y = 0.1
                self.lives -= 1
            hits = pygame.sprite.collide_rect(self.player, self.alien)
            if hits:
                pygame.mixer.music.play()
                self.alien.pos.x = random.randrange(0, WIDTH)
                self.alien.pos.y = -25
                self.alien.vel.x = 0.1
                self.alien.vel.y = 0.1
                self.score += 1

        if self.lives < 0:
            self.playing = False


    def events(self):

        for event in pygame.event.get():

            if event.type == pygame.QUIT:
                if self.playing:
                    self.playing = False
                self.running = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    self.player.jump()


    def draw(self):

        self.screen.fill(BLACK)
        self.screen.blit(background_imge, [0, 0])
        self.all_sprites.draw(self.screen)
        self.draw_text(str(self.score), 22, WHITE, WIDTH / 2, 15)
        self.draw_text("Lives: "+str(self.lives), 22, WHITE, 50 , 15)

        pygame.display.flip()

    def show_start_screen(self):

        self.screen.fill(BGCOLOR)
        self.draw_text(TITLE, 48, WHITE, WIDTH / 2, HEIGHT / 4)
        self.draw_text("Arrows to move, Space to jump", 22, WHITE, WIDTH / 2, HEIGHT / 2)
        self.draw_text("Press a key to play", 22, WHITE, WIDTH / 2, HEIGHT * 3 / 4)
        self.draw_text("High Score: " + str(self.highscore), 22, WHITE, WIDTH / 2, 15)
        pygame.display.flip()
        self.wait_for_key()

    def show_go_screen(self):
        if not self.running:
            return
        self.screen.fill(BGCOLOR)
        self.draw_text("GAME OVER", 48, WHITE, WIDTH / 2, HEIGHT / 4)
        self.draw_text("Score: " + str(self.score), 22, WHITE, WIDTH / 2, HEIGHT / 2)
        self.draw_text("Press a key to play again", 22, WHITE, WIDTH / 2, HEIGHT * 3 / 4)
        if self.score > self.highscore:
            self.highscore = self.score
            self.draw_text("NEW HIGH SCORE!", 22, WHITE, WIDTH / 2, HEIGHT / 2 + 40)
            with open(path.join(self.dir, HS_FILE), 'w') as f:
                f.write(str(self.score))
        else:
            self.draw_text("High Score: " + str(self.highscore), 22, WHITE, WIDTH / 2, HEIGHT / 2 + 40)
            pygame.display.flip()
        self.wait_for_key()

    def wait_for_key(self):
        waiting = True
        while waiting:
            self.clock.tick(FPS)
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    waiting = False
                    self.running = False
                if event.type == pygame.KEYUP:
                    waiting = False

    def draw_text(self, text, size, color, x, y):
        font = pygame.font.Font(self.font_name, size)
        text_surface = font.render(text, True, color)
        text_rect = text_surface.get_rect()
        text_rect.midtop = (x, y)
        self.screen.blit(text_surface, text_rect)


g = Game()
g.show_start_screen()
while g.running:
    g.new()
    g.show_go_screen()

pygame.quit()
