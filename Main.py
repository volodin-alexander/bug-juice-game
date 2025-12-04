import pygame
import random
pygame.mixer.init()
pygame.font.init()
sc = pygame.display.set_mode([800, 600])  #Creating window
pygame.display.set_caption("Bug Juice")
player_left = pygame.image.load("player-left.png")
player_right = pygame.image.load("player-right.png")
music = pygame.mixer.music.load("Music.mp3")    #Loading music and images
bg = pygame.image.load("background.png")
ground = pygame.image.load("Ground.png")
explotion = pygame.image.load("explosion.png")
explotion = pygame.transform.scale(explotion, (150, 150))

ladybug = pygame.image.load("ladybug.png")
spider = pygame.image.load("spider.png")
caterpillar = pygame.image.load("caterpillar.png")
score = 0
class Bug():     #Class for bugs
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.b_x = x
        self.b_y = y
        self.lives = 20
        self.alive = True
        self.shoot = False
        self.side = random.choice(("left", "right"))
        self.look = random.choice((ladybug, caterpillar, spider))
    
    def update(self):
        sh = random.randint(1, 4)
        mv = random.randint(1, 3)
        if sh == 3:
            self.shoot = True
        if mv == 1:
            if self.side == 'left':
                self.x -= 15
                u = random.randint(1, 2)
                if u == 2:
                    self.y -= 0.2
                else:
                    self.y += 0.2
            elif self.side == 'right':
                self.x += 15
                u = random.randint(1, 2)
                if u == 2:
                    self.y -= 0.2
                else:
                    self.y += 0.2
        if self.lives < 0:
            self.x = 800
            mv = 1
    def draw(self):
        sc.blit(self.look, (self.x, self.y))
        pygame.display.update()

side = random.choice(('left', 'right'))
shoot = False
x = 50
y = 400
b_x = x
b_y = y + 65     #Player and bullet coordinatons
p2 = False
p3 = False     #Parts of level
p4 = False
pygame.mixer.music.play(-1)
bugs = []
for bug in range(10):
    bug = Bug(800, random.randint(400, 500))
    bugs.append(bug)
num_bugs = len(bugs)
player_lives = 100
clock = pygame.time.Clock()
while 1:
    a = pygame.font.Font(None, 50)
    text2 = a.render(f'score {score}', 1, (255, 255, 255))
    sc.blit(text2, (200, 40))
    pygame.display.update()
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            quit()

    pressed_keys = pygame.key.get_pressed()              #Events of keyboard
    if pressed_keys[pygame.K_d]:
        x += 5
        side = 'right'
    elif pressed_keys[pygame.K_a]:
        x -= 5
        side = 'left'
    elif pressed_keys[pygame.K_SPACE]:
        shoot = True
    elif pressed_keys[pygame.K_w]:
        y -= 5
        b_x = x
        b_y = y + 65
    elif pressed_keys[pygame.K_s]:
        y += 5
        b_x = x
        b_y = y + 65

    for i in bugs:
        i.update()

    def distance(x1, y1, x2, y2):
        return ((x1 - x2)**2 + (y1 - y2)**2)**0.5

    # Checking bullet moving
    if shoot == True:
        if side == 'left':
            b_x -= 100
            bullet_rect = pygame.Rect(b_x - 10, b_y - 10, 20, 20)  # bullet hitbox-rect
            pygame.draw.circle(sc, (0, 0, 255), (b_x, b_y), 10)
            pygame.display.update()
            if b_x < 0:
                b_x = x
                shoot = False
        elif side == 'right':
            b_x += 100
            bullet_rect = pygame.Rect(b_x - 10, b_y - 10, 20, 20)  # bullet hitbox-rect
            pygame.draw.circle(sc, (0, 0, 255), (b_x, b_y), 10)
            pygame.display.update()
            if b_x > 800:
                b_x = x
                shoot = False

        # Checking bullet position
        for i in bugs:
            insect_rect = pygame.Rect(i.x, i.y, 50, 50)  # Bug hitbox-rect
            if bullet_rect.colliderect(insect_rect):
                
                # Decreased bug lives
                i.lives -= 5
               
                # blink effect
                blink_color = (random.randint(100, 255), random.randint(100, 255), random.randint(100, 255))
                pygame.draw.rect(sc, blink_color, (i.x, i.y, 50, 50))
                pygame.display.update()
                pygame.time.wait(50)

                # checking bug lives
                if i.lives <= 0:
                    score += 10
                    i.alive = False
                    i.x = 1000  # Kick the bug out screen 

    for i in bugs:
        i.draw()    #Draw all bugs

    for i in bugs:
        if i.x < x:
            player_lives -= random.randint(1, 10)    #If player passed the bug
            i.x = 600

    if x > 800:
        player_lives += 30
        x = 50
        bugs = []
        for bug in range(10):
            bug = Bug(320, random.randint(400, 500))    #Next parts level
            bug.lives += 10
            bugs.append(bug)
        p2 = True
    if p2:
    
        for i in bugs:
            i.draw()

        for i in bugs:
            if i.x < x:
                player_lives -= random.randint(1, 10)
                x -= 10
                i.x = 1000
        for i in bugs:
            i.update()

        if x > 800:
            x = 50
            bugs = []
            for bug in range(10):
                bug = Bug(320, random.randint(400, 500))
                bug.lives += 25
                bugs.append(bug)
            p3 = True
            p3 = False
    if p3:
        for i in bugs:
            i.draw()

        for i in bugs:
            if i.x < x:
                player_lives -= random.randint(1, 10)
                i.x = 600
        for i in bugs:
            i.update()

        if x > 800:
            p3 = True
            p2 = False

    if player_lives <= 0: #If lives of player is 0
        sc.blit(explotion, (x, y))
        pygame.display.update()
        pygame.time.delay(50)
        explotion = pygame.transform.scale(explotion, (200, 200))
        sc.blit(explotion, (x - 40, y))
        pygame.display.update()     #Animation of explotion
        pygame.time.delay(50)
        explotion = pygame.transform.scale(explotion, (250, 250))
        sc.blit(explotion, (x - 65, y))
        pygame.display.update()
        pygame.time.delay(50)
        pygame.time.delay(1000)
        sc.fill((0, 0, 0))
        a = pygame.font.Font(None, 50)
        text2 = a.render(f'Game Over! Your score was: {score}', 1, (255, 255, 255))
        sc.blit(text2, (200, 40))
        pygame.display.update()
        pygame.time.delay(3000)
        quit()
    elif y <= 250:
        y = 249

    if b_x > 800:
        b_x = x
    elif b_x < 0:     #Checking bullet coordinations
        b_x = x
    sc.fill((0,0,0))
    sc.blit(bg, (0, 0))
    sc.blit(ground, (0, 400))
    if side == 'right':
        sc.blit(player_right, (x, y))
    else:
        sc.blit(player_left, (x, y))
    pygame.draw.rect(sc, (255, 0, 0), (50, 50, 100, 10))
    pygame.draw.rect(sc, (255, 255, 0), (50, 50, player_lives, 10))      #Draw all
    pygame.display.update()
    clock.tick(60)
 