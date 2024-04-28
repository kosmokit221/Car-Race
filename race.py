from random import randint
from pygame import *
import pickle
init()
mixer.init()
font.init()


screen_info = display.Info()
WIDTH, HEIGHT = screen_info.current_w, screen_info.current_h
LINE_WIDTH = WIDTH/8
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
enemy_car_img = image.load('car.png')

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



enemys = sprite.Group()

class Enemy(GameSprite):
    def __init__(self):
        rand_line = randint(1,2)
        x = WIDTH/2-LINE_WIDTH*rand_line
        y = -150
        super().__init__(enemy_img, 100, 150, x, y)   
        self.speed = 5
        enemys.add(self)
        
    def update(self):
        self.rect.y += self.speed + player.bg_speed
        if self.rect.y > HEIGHT:
            self.kill()


class Enemy2(GameSprite):
    def __init__(self):
        rand_line = randint(1,2)
        x = WIDTH/2+LINE_WIDTH*rand_line - 100
        y = -150
        super().__init__(enemy_car_img, 100, 150, x, y)   
        self.speed = 5
        enemys.add(self)
    
    def update(self):
        self.rect.y -= self.speed - player.bg_speed
        if self.rect.bottom < 0:
            self.kill()


class Player(GameSprite):
    def __init__(self, sprite_image, width, height, x, y):
        super().__init__(sprite_image, width, height, x, y)   
        self.points = 0
        self.speed = 5
        self.bg_speed = 2
        self.hp = 1
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
            self.image = transform.flip(self.original,True,False)
            self.rect.x -= self.speed

        if keys[K_d] and self.rect.right < WIDTH:
            self.image = self.original
            self.rect.x += self.speed
        


Enemy()
last_spawn_time = time.get_ticks()
spawn_interval = randint(1500, 4000)

Enemy2()
last_spawn_time = time.get_ticks()
spawn_interval = randint(1500, 4000)

player = Player(player_img,90,160,600,300)

finish_text = font2.render("GAME OVER", True, (255,0,0))
points_text = font1.render(f"score:{player.points}",True, (255,255,0))
max_points = 0
hp_text = font1.render(f"Hp:{player.hp}",True, (255,255,0))
max_points_text = font1.render(f"Max score: {max_points}", True , (255,255,255))


while True:
#оброби подію «клік за кнопкою "Закрити вікно"»
    for e in event.get():
        if e.type == QUIT:
            quit()
        if e.type == KEYDOWN:
            if e.key == K_ESCAPE:
                quit()
           
    if not finish:
        now = time.get_ticks()
        if now - last_spawn_time > spawn_interval:
            Enemy()
            last_spawn_time = time.get_ticks()
            spawn_interval = randint(1500, 4000)
            Enemy2()
            last_spawn_time = time.get_ticks()
            spawn_interval = randint(1500, 4000)
        sprites.update()
        player.points += player.bg_speed/100
        if player.rect.right<WIDTH/2:
            player.points += 0.5
        points_text = font1.render(f"score:{int(player.points)}",True, (255,255,0))

        collide_list = sprite.spritecollide(player, enemys, False, sprite.collide_mask)

        for enemy in collide_list:
            player.hp = 0

        if player.hp <= 0:
            finish = True

        window.blit(bg, (0,bg_y1))
        window.blit(bg, (0,bg_y2))
        bg_y1+=player.bg_speed
        bg_y2+=player.bg_speed
        if bg_y1 > HEIGHT:
            bg_y1 = -HEIGHT
        if bg_y2 > HEIGHT:
            bg_y2 = -HEIGHT
        

       
    sprites.draw(window)
    window.blit(points_text,(WIDTH-150,10))
    if finish:
        window.blit(finish_text,(WIDTH/2-100,HEIGHT/2))

    display.update()
    clock.tick(FPS)