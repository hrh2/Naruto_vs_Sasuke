import pygame
from joystick import ArduinoJoystick

pygame.init()

win_x = 1200
win_y = 800
win = pygame.display.set_mode((win_x,win_y))
pygame.display.set_caption("Naruto vs Sasuke")

walkRight = [pygame.image.load('pics\\NR2.png'), pygame.image.load('pics\\NR3.png'), pygame.image.load('pics\\NR1.png')]
walkLeft = [pygame.image.load('pics\\NL2.png'), pygame.image.load('pics\\NL3.png'), pygame.image.load('pics\\NL1.png')]

bg = pygame.image.load('pics\\bg3.jpg')
stan = pygame.image.load('pics\\Nstanding.png')

Nh = pygame.image.load('pics\\Nh.png')
Sh = pygame.image.load('pics\\Sh.png')

hitSound = pygame.mixer.Sound("pics\\draw-sword1.wav")
bgm = pygame.mixer.music.load("pics\\theme.wav")

pygame.mixer.music.play()

Clock = pygame.time.Clock()


class player():
    def __init__(self, x, y, width, height):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.speed = 15
        self.isjump = False
        self.jumpheight = 10
        self.left = False
        self.right = False
        self.walkCount = 0
        self.standing = True
        self.hitbox = (self.x + 10, self.y + 5, 80, 80)
        self.health = 500

    def draw(self, win):

        if self.health > 0:

            if self.walkCount + 1 >= 6:
                self.walkCount = 0

            if not self.standing:
                if self.left:

                    win.blit(walkLeft[self.walkCount // 2], (self.x, self.y))
                    self.walkCount += 1


                elif self.right:
                    win.blit(walkRight[self.walkCount // 2], (self.x, self.y))
                    self.walkCount += 1

            else:

                if self.right:
                    win.blit(pygame.image.load('pics\\NR1.png'), (self.x, self.y))
                else:
                    win.blit(pygame.image.load('pics\\NL1.png'), (self.x, self.y))

            self.hitbox = (self.x + 10, self.y + 5, 80, 80)
            Nbar2 = pygame.draw.rect(win, (255, 0, 0), (win_x*8/70, 40, win_x*21/70, 25))
            Nbar = pygame.draw.rect(win, (255, 255, 0), (win_x*8/70, 40, (self.health / 500) * (win_x * 21/70), 15))
        # pygame.draw.rect(win,(255,0,0),self.hitbox,2)

        else:
            text = font.render('Sasuke Wins', True, (255, 255, 255), (0, 0, 100))
            win.blit(text, (180, 200))
            win.blit(pygame.image.load('pics\\Nd.png'), (self.x, self.y))

    def hit(self):
        if self.health > 0:
            self.health -= 5
        else:
            print("Naruto died")


class weapons():
    def __init__(self, x, y, width, height, facing):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.facing = facing
        self.vel = 8 * facing
        self.hitbox = (self.x, self.y, 40, 40)

    def draw(self, win):
        win.blit(pygame.image.load('pics\\shur.png'), (self.x, self.y))

        self.hitbox = (self.x, self.y, 40, 40)

    # pygame.draw.rect(win,(255,0,0),self.hitbox,2)


class enemy():
    walkRightS = [pygame.image.load('pics\\SR2.png'), pygame.image.load('pics\\SR3.png'),
                  pygame.image.load('pics\\SR1.png')]
    walkLeftS = [pygame.image.load('pics\\SL2.png'), pygame.image.load('pics\\SL3.png'),
                 pygame.image.load('pics\\SL1.png')]

    def __init__(self, x, y, width, height, end):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.end = end
        self.path = [self.x, self.end]
        self.speed = 10
        self.walkCount = 0
        self.hitbox = (self.x + 10, self.y + 5, 80, 80)
        self.health = 500

    def draw(self, win):
        self.move()

        if self.health > 0:

            if self.walkCount + 1 >= 6:
                self.walkCount = 0

            if self.speed > 0:
                win.blit(self.walkRightS[self.walkCount // 2], (self.x, self.y))
                self.walkCount += 1

            else:
                win.blit(self.walkLeftS[self.walkCount // 2], (self.x, self.y))
                self.walkCount += 1

            self.hitbox = (self.x + 10, self.y + 5, 80, 80)
            Sbar2 = pygame.draw.rect(win, (255, 0, 0), (win_x*42/70, 40, win_x*21/70, 25))
            Sbar = pygame.draw.rect(win, (255, 255, 0), (win_x*42/70, 40, (self.health / 500) * (win_x * 21/70), 15))

        else:
            self.speed = 0
            text = font.render('Naruto Wins', True, (255, 100, 10), (0, 0, 100))
            win.blit(text, (180, 200))
            win.blit(pygame.image.load('pics\\Sd.png'), (self.x, self.y))

    # pygame.draw.rect(win, (255,0,0),self.hitbox,2)

    def move(self):

        if self.speed > 0:

            if self.x + self.speed < self.path[1]:
                self.x += self.speed
            else:
                self.speed = self.speed * -1
                self.walkCount = 0

        else:
            if self.x - self.speed > self.path[0]:
                self.x += self.speed

            else:
                self.speed = self.speed * -1
                self.walkCount = 0

    def hit(self):
        if self.health > 0:
            self.health -= 10
        else:
            print('sasuke died')


run = True


def redrawgamewindow():
    win.blit(bg, (0, 0))
    naruto.draw(win)
    sasuke.draw(win)
    win.blit(Nh, (win_x*4/70, 10))
    win.blit(Sh, (win_x*6/7, 10))

    for shuriken in shurikens:
        shuriken.draw(win)

    pygame.display.update()


font = pygame.font.SysFont('comicsans', 60, True)

naruto = player(win_x*(3/70), win_y*4/7, 100, 100)
sasuke = enemy(win_x*1/7, win_y*4/7, 100, 100, win_x*6/7)
shurikens = []
throwSpeed = 0
joystick = ArduinoJoystick()

while run:

    ######### FRAME RATE ############
    Clock.tick(25)
    ##########

    if throwSpeed > 0:
        throwSpeed += 1

    if throwSpeed > 3:
        throwSpeed = 0

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False

    # Checking collisions between Naruto and Sasuke
    if naruto.health > 0 and sasuke.health > 0:
        if naruto.hitbox[1] < sasuke.hitbox[1] + sasuke.hitbox[3] and naruto.hitbox[1] + naruto.hitbox[3] > sasuke.hitbox[1]:
            if naruto.hitbox[0] + naruto.hitbox[2] > sasuke.hitbox[0] and naruto.hitbox[0] < sasuke.hitbox[0] + sasuke.hitbox[2]:
                naruto.hit()
                hitSound.play()

    # Handle the movement of shurikens
    for shuriken in shurikens:
        if sasuke.health > 0:
            if sasuke.hitbox[1] < shuriken.hitbox[1] + round(shuriken.hitbox[3] / 2) < sasuke.hitbox[1] + sasuke.hitbox[3]:
                if  sasuke.hitbox[0] < shuriken.hitbox[0] + shuriken.hitbox[2] < sasuke.hitbox[0] + sasuke.hitbox[2]:
                    sasuke.hit()
                    hitSound.play()
                    shurikens.pop(shurikens.index(shuriken))

        if shuriken.x < win_x-1 and shuriken.x > 0:
            shuriken.x += shuriken.vel
        else:
            shurikens.pop(shurikens.index(shuriken))

    ########### KEYS and JOYSTICK CONTROLS ###########

    keys = pygame.key.get_pressed()
    result = joystick.read_arduino_data()

    ########### SHOOTING ################
    ########### SHOOTING ################
    if (keys[pygame.K_SPACE] or result == 2):
        if throwSpeed == 0:  # Only reset throwSpeed when starting to shoot
            facing = -1 if naruto.left else 1
            if len(shurikens) < 5:
                shurikens.append(weapons(round(naruto.x + 60), round(naruto.y + 30), 40, 40, facing))
            throwSpeed = 1
    else:
        throwSpeed = 0  # Reset throwSpeed when space key or joystick release

    ######## LEFT ###########
    if (keys[pygame.K_LEFT] or result == 3) and naruto.x > naruto.speed:
        naruto.x -= naruto.speed
        naruto.left = True
        naruto.right = False
        naruto.standing = False

    ######### RIGHT ##################
    elif (keys[pygame.K_RIGHT] or result == 4) and naruto.x < (win_x * 69 / 70) - naruto.width - naruto.speed:
        naruto.x += naruto.speed
        naruto.left = False
        naruto.right = True
        naruto.standing = False

    else:
        naruto.standing = True
        naruto.walkCount = 0

    ########## JUMP #############
    if not naruto.isjump:
        if keys[pygame.K_UP] or result == 1:
            naruto.isjump = True
            naruto.left = False
            naruto.right = False
            naruto.walkCount = 0
    else:
        if naruto.jumpheight >= -10:
            neg = 1
            if naruto.jumpheight < 0:
                neg = -1
            naruto.y -= (naruto.jumpheight ** 2) * 0.5 * neg
            naruto.jumpheight -= 1
        else:
            naruto.isjump = False
            naruto.jumpheight = 10

    redrawgamewindow()

pygame.quit()
