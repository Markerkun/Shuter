from pygame import *
from random import randint
from datetime import datetime, timedelta


# фонова музика
mixer.init()
mixer.music.load('space.ogg')
mixer.music.play()
fire_sound = mixer.Sound('fire.ogg')


# шрифти і написи
font.init()
score_text = font.Font(None, 36)
score = 0
lost_text = font.Font(None, 36)
lost = 0
win_text = font.Font(None, 36)
lose_text = font.Font(None, 36)
b_text = font.Font(None, 36)
b = 11  


win_width = 700
win_height = 500
display.set_caption("Shooter")
window = display.set_mode((win_width, win_height))


background = transform.scale(
    image.load("galaxy.jpg"),
    (win_width, win_height)
)






class GameSprite(sprite.Sprite):
    def __init__(self, player_image, player_x, player_y, size_x, size_y, player_speed):
        super().__init__()
        self.image = transform.scale(image.load(player_image), (size_x, size_y))    
        self.speed = player_speed
        self.rect = self.image.get_rect()
        self.rect.x = player_x
        self.rect.y = player_y
       
    def reset(self):
        window.blit(self.image, (self.rect.x, self.rect.y))


class Player(GameSprite):

    def __init__(self, player_image, player_x, player_y, size_x, size_y, player_speed):
        super().__init__(player_image, player_x, player_y, size_x, size_y, player_speed)

        self.num_bullets = 10
        self.next_time_for_shot = datetime.now()
        self.next_reload = datetime.now()

    def update(self):
        keys = key.get_pressed() 
        if keys[K_LEFT] and self.rect.x > 5:
            self.rect.x -= self.speed
        if keys[K_RIGHT] and self.rect.x < win_width - 80:
            self.rect.x += self.speed


    def fire(self):
        global b
        b = self.num_bullets
        if self.num_bullets <= 0 and self.next_reload <= datetime.now():
            self.num_bullets = 10
        if self.num_bullets > 0 and self.next_time_for_shot <= datetime.now():
            bullet = Bullet('bullet.png', self.rect.centerx, self.rect.top, 15, 20, -15)
            bullets.add(bullet)
            fire_sound.play()
            self.num_bullets -= 1
            self.next_time_for_shot = datetime.now() + timedelta(seconds=0.2)
            if self.num_bullets <= 0:
                self.next_reload = datetime.now() + timedelta(seconds=3)
        



# клас спрайта-ворога
class Enemy(GameSprite):
    # рух ворога
    def update(self):
        self.rect.y += self.speed
        global lost
        if self.rect.y > win_height:
            self.rect.x = randint(80, win_width - 80)
            self.rect.y = 0
            lost = lost + 1
           
# клас спрайта-кулі  
class Bullet(GameSprite):
    # рух ворога
    def update(self):
        self.rect.y += self.speed
        # зникає, якщо дійде до краю екрана
        if self.rect.y < 0:
            self.kill()


ship = Player("rocket.png", 5, win_height - 100, 80, 100, 10)


bullets = sprite.Group()
monsters = sprite.Group()
for i in range(1, 6):
    monster = Enemy("ufo.png", randint(80, win_width - 80), -40, 80, 50, randint(1, 5))
    monsters.add(monster)



run = True
game_over = False
is_win = False

while run:

    window.blit(background, (0, 0))
   
    text1 = score_text.render("Рахунок: " + str(score), 1, (0, 255, 0))
    window.blit(text1, (10, 20))
    text2 = lost_text.render("Пропущено: " + str(lost), 1, (255, 0, 0))
    window.blit(text2, (520, 20))
    text3 = b_text.render("кількість пуль: " + str(b), 1, (175, 175, 0))
    window.blit(text3, (250, 20))


    for e in event.get():
        if e.type == QUIT:
            run = False
        elif e.type == KEYDOWN:
            if game_over == False:
                if e.key == K_SPACE:
                    
                    ship.fire()


    if game_over == False:


        # перевірка зіткнення кулі та монстрів (і монстр, і куля при зіткненні зникають)
        collides = sprite.groupcollide(monsters, bullets, True, True)
        for c in collides:
            # цей цикл повториться стільки разів, скільки монстрів збито
            score = score + 1
            monster = Enemy('ufo.png', randint(80, win_width - 80), -40, 80, 50, randint(1, 5))
            monsters.add(monster)


        # можливий програш: пропустили занадто багато або герой зіткнувся з ворогом
        if sprite.spritecollide(ship, monsters, False) or lost >= 10:
            lost += 1
            game_over = True # програли, ставимо тло і більше не керуємо спрайтами.
            
        if score == 50:
            game_over = True
            is_win = True


        # рухи спрайтів
        ship.update()
        monsters.update()
        bullets.update()
        


        # оновлюємо їх у новому місці при кожній ітерації циклу
        ship.reset()
        monsters.draw(window)
        bullets.draw(window)
        
    else:
        if is_win == True:
            text4 = win_text.render("Ви перемогли", 1, (255, 255, 255))
            window.blit(text4, (255, 245))
        else:
            text3 = lose_text.render("Ви програли", 1, (255, 255, 255))
            window.blit(text3, (255, 245))


    display.update()
    time.delay(60)



