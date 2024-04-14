from random import randint
from pygame import *
import pickle
init()
mixer.init()
font.init()

screen_info = display.Info()
WIDTH, HEIGHT = screen_info.current_w, screen_info.current_h
flags = FULLSCREEN
window = display.set_mode((WIDTH, HEIGHT), flags)
display.set_caption("Race")
FPS = 60

font1 = font.SysFont("Impact", 35)
font2 = font.SysFont("Impact", 55)

sprites = sprite.Group()

#mixer.music.load("space.ogg")
#mixer.music.set_volume(0.2)
#mixer.music.play(loops=-1)

#winner_sound = mixer.Sound('S31-Winning the Race.ogg')


clock = time.Clock()
bg = image.load("background-1.png")
bg = transform.scale(bg, (WIDTH, HEIGHT))
bg_y1 = 0
bg_y2 = -HEIGHT

finish = False

player_img = image.load('car1.png')
enemy_img = image.load('car1_spr.png')

sprites = sprite.Group()
class GameSprite(sprite.Sprite):
    def __init__(self, sprite_image, width, height, x, y):
        super().__init__()
        self.image = transform.scale(sprite_image, (width, height))
        self.original = self.image
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        sprites.add(self)

    def draw(self, window):
        window.blit(self.image, self.rect)


class Player(GameSprite):
    def __init__(self, sprite_image, width, height, x, y):
        super().__init__(sprite_image, width, height, x, y)   
        self.points = 0
        self.speed = 5
        self.bg_speed = 2
        self.max_speed = 20
        self.mask = mask.from_surface(self.image)
                
    def update(self):
        self.old_pos = self.rect.x, self.rect.y

        keys = key.get_pressed()
        if keys[K_w] and self.rect.y > 0:
            #self.rect.y -= self.speed
            if self.bg_speed < self.max_speed:
                self.bg_speed += 0.090
    
        if keys[K_s]:
            if self.bg_speed >0:
                self.bg_speed -= 0.10
                if self.bg_speed > 10:
                    self.bg_speed -=10
            if self.rect.bottom < HEIGHT-100:
                 self.rect.y += self.speed
        # else:
        #     self.bg_speed = 2
        if keys[K_a] and self.rect.left > 0:
        
            self.rect.x -= self.speed
        if keys[K_d] and self.rect.right < WIDTH:
        
            self.rect.x += self.speed


player = Player(player_img,90,160,300,300)
while True:
#оброби подію «клік за кнопкою "Закрити вікно"»
    for e in event.get():
        if e.type == QUIT:
            quit()
        if e.type == KEYDOWN:
            if e.key == K_ESCAPE:
                quit()
           
    if not finish:
        sprites.update()
        window.blit(bg, (0,bg_y1))
        window.blit(bg, (0,bg_y2))
        bg_y1+=player.bg_speed
        bg_y2+=player.bg_speed
        if bg_y1 > HEIGHT:
            bg_y1 = -HEIGHT
        if bg_y2 > HEIGHT:
            bg_y2 = -HEIGHT

       
    sprites.draw(window)
    display.update()
    clock.tick(FPS)