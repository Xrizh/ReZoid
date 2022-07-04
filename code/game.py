# CPT FINAL || Krish & Umer || Oct 29th, 2021


# Header Files
import sys
import random
import time
import pygame


# ======================================================= Global Variables

# declaring width and height and screen resolution
pygame.init()
pygame.mixer.init()

pygame.display.set_caption("ReZoid")
res = (720 , 600)
screen = pygame.display.set_mode(res)
WIDTH = screen.get_width()
HEIGHT = screen.get_height()
height = HEIGHT
playerImg = None
playerX = 370
playerY = 480
playerX_change = 0

# avoid these objects
obstacle = pygame.image.load("images/dustbin.png")
obstacle1 = pygame.image.load("images/rottenfood.png")
obstacle2 = pygame.image.load("images/dustbin.png")

# move towards these objects
cardboard_box = pygame.image.load("images/cardboardbox.png")
empty_jar = pygame.image.load("images/emptyjar.png")
pop_can = pygame.image.load("images/popcan.png")
milk_carton = pygame.image.load("images/milkcarton.png")

#Music
correct = pygame.mixer.Sound("correct.wav")
lost_life = pygame.mixer.Sound("lost_life.wav")

# Used to determine colour of rgb menu bars
c1 = random.randint(125, 255)
c2 = random.randint(0, 255)
c3 = random.randint(0, 255)
red = (255, 0, 0)
green = (0, 255, 0)
blue = (0, 0, 255)
color_list = [red, green, blue]
player_c = random.choice(color_list)
rezoid_c1 = 0
rezoid_c2 = 0
rezoid_c3 = 254
rezoid_c4 = 254

# light shade of menu buttons
startl = (169, 169, 169)

# dark shade of menu buttons
startd = (100, 100, 100)
white = (255, 255, 255)
start = (255, 255, 255)
width = screen.get_width()
height = screen.get_height()

# Other Variables
X = 300
Y = 290
width1 = 100
height1 = 40

# defining fonts
smallfont = pygame.font.SysFont('Corbel', 35)
smallsmallfont = pygame.font.SysFont('Corbel', 30)
ultrasmallfont = pygame.font.SysFont('Corbel', 25)
bigfont = pygame.font.SysFont('franklingothicmedium',175)

# texts to be rendered on the main menu
text = smallfont.render('Start', True, white)
text1 = smallfont.render('Options', True, white)
exit1 = smallfont.render('Exit', True, white)

# game title
rezoid = bigfont.render('ReZoid', True, (c3, c2, c1))

# =============================================================================== Functions

# Initializes the sprites (enemies, player, recyclables)
class Sprites:
    def __init__(self, x, y, lives = 3):
        self.x = x
        self.y = y
        self.health = lives
        self.garbage_img = None
        self.player_img = playerImg

    def draw(self, screen):
        screen.blit(self.player_img, (self.x, self.y))



class Player(Sprites):
    def __init__(self, x, y, lives = 3):
        super().__init__(x, y, lives)
        self.player_img = playerImg
        # Creates a pixel perfect hitbox of character
        self.mask = pygame.mask.from_surface(self.player_img)
        self.max_health = lives

class Enemy(Sprites):
    ENEMY_MAP = {"trashbag": (obstacle), "rottenfood": (obstacle1), "dustbin": (obstacle2)}

    def __init__(self, x, y, pic, lives = 3):
        super().__init__(x, y, lives)
        self.player_img = self.ENEMY_MAP[pic]
        self.mask = pygame.mask.from_surface(self.player_img)

    def move(self,vel):
        self.x += vel

class Recycable(Sprites):
    RECYCLABLE_MAP = {"emptyjar": (empty_jar), "cardboardbox": (cardboard_box), "popcan": (pop_can), "milkcarton":(milk_carton)}

    def __init__(self, x, y, good_pic, lives = 3):
        super().__init__(x, y, lives)
        self.player_img = self.RECYCLABLE_MAP[good_pic]
        self.mask = pygame.mask.from_surface(self.player_img)


def game(playerImg):

    run = True
    lost = False
    lost_count  = 0
    lives = 3
    player_vel = 10
    score = 0
    lost_font = pygame.font.SysFont("comicsans", 70)

    character = Player(width/2,height/2)
    recyclables  = []
    recycle_length = 3

    enemies = []
    wave_length = 6
    level = 0
    enemy_vel = 4
    FPS = 60

    pygame.mixer.music.load("bg.wav")
    pygame.mixer.music.play(-1)

    # Game Menu Bars
    def redraw_window(score, lives, level):
        mouse = pygame.mouse.get_pos()
        # game background
        bg = pygame.image.load("images/background.jpg")
        bg = pygame.transform.scale(bg, (res))
        screen.blit(bg,(0,0))

        for enemy in enemies:
            enemy.draw(screen)

        for recycable in recyclables:
            recycable.draw(screen)

        character.draw(screen)

        # Displays text on Menu Bars
        back = smallfont.render('Back', True, white)
        score = smallfont.render(f'Score: {score}', True, white)
        lives_label = smallfont.render(f'Lives: {lives}', True, white)
        level_label = smallfont.render(f'Level: {level}', True, white)
        pygame.draw.rect(screen, (c2, rezoid_c1, rezoid_c2), [0, 550, 720, 600])
        pygame.draw.rect(screen, (c2, rezoid_c1, rezoid_c2), [0, 0, 720, 50])

        if width-80 < mouse[0] < width and 0 < mouse[1] < 50:
            pygame.draw.rect(screen, startl, [width-90, 0, width, 50])
        else:
            pygame.draw.rect(screen, startd, [width-90, 0, width, 50])
        screen.blit(score, (width - 500, height - 40))
        screen.blit(back, (width - 80, 7))
        screen.blit(lives_label, (width - 120, height - 40))
        screen.blit(level_label, (width - 260, height - 40))
        clock.tick(FPS)


        # Exit button for game's menu
        pos = pygame.mouse.get_pos()
        pressed1 = pygame.mouse.get_pressed()[0]
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                if event.type == pygame.QUIT:
                        pygame.quit()
                        rule_start = False

        if (width-80 < pos[0] < width and 0 < pos[1] < 50) and pressed1:
            rule_start = False
            pygame.mixer.music.stop()
            intro(rezoid_c1,rezoid_c2,rezoid,exit1,text1,text,)
            clock.tick(FPS)
            pygame.display.update()

    # Actual Gameplay
    while run:
        clock = pygame.time.Clock()
        clock.tick(FPS)
        redraw_window(score, lives, level)

        # Checks if Player has lost
        if lives <= 0:
            lost = True
            lost_count += 1

        # Ends Gameplay when player has lost all lives
        if lost:
            pygame.mixer.music.stop()

            lost_label = lost_font.render("You Lost!!!", True, white)
            screen.blit(lost_label, (width/2 - 110, height/2))
            player_vel = 0
            enemy_vel = 0

        # Determines how many enemies will spawn
        if len(enemies) == 0:
            level += 1
            wave_length += 5
            for i in range(wave_length):
                enemy = Enemy(random.randrange(-3000, -50), random.randrange(70, height-70), random.choice(["trashbag","rottenfood","dustbin"]))
                enemies.append(enemy)

        # Determines how many recyclables will spawn
        if len(recyclables) == 0:
            recycle_length = random.randint(3, 7)

            for j in range(recycle_length):
                recyclable = Recycable(random.randrange(50, width-50), random.randrange(100, height-100), random.choice(["emptyjar","cardboardbox","popcan","milkcarton"]))
                recyclables.append(recyclable)

        # Determines player movement
        for ev in pygame.event.get():
            if ev.type == pygame.QUIT:
                pygame.quit()
        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT] and character.x - player_vel > 0: # left
            character.x -= player_vel
        if keys[pygame.K_RIGHT] and character.x + player_vel + 50 < width: # right
            character.x += player_vel
        if keys[pygame.K_UP] and character.y - player_vel > 50 : # up
            character.y -= player_vel
        if keys[pygame.K_DOWN] and character.y + player_vel + 100 < height: # down
            character.y += player_vel

        # Checks if enemy and player have collided, if yes, subtract 1 from lives
        for enemy in enemies[:]:
            enemy.move(enemy_vel)

            if (enemy.x > 720):
                enemies.remove(enemy)

            offset_x = enemy.x - character.x
            offset_y = enemy.y - character.y
            collide1 = character.mask.overlap(enemy.mask, ( int(offset_x), int(offset_y)))

            if (collide1 != None):
                pygame.mixer.music.pause()
                pygame.mixer.Sound.play(lost_life)

                lives -= 1
                enemies.remove(enemy)
                pygame.mixer.music.unpause()

        # Checks if recyclables and player have collided, if yes, add 1 to score
        for recyclable in recyclables[:]:

            offset_x = recyclable.x - character.x
            offset_y = recyclable.y - character.y
            collide2 = character.mask.overlap(recyclable.mask, ( int(offset_x), int(offset_y)))


            if (collide2 != None):
                if (collide2 != None):
                    pygame.mixer.music.pause()
                    pygame.mixer.Sound.play(correct)
                    score += 1
                    recyclables.remove(recyclable)
                    pygame.mixer.music.unpause()

        pygame.display.update()


# intro/game-menu
def intro(
    rezoid_c1,
    rezoid_c2,
    rezoid,
    exit1,
    text1,
    text,
    ):
    start = True
    rule_start = True
    game_play = True

    global event
    while start:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()

        screen.fill((0,0,0))
        mouse = pygame.mouse.get_pos()


        # start screen
        if X < mouse[0] < X + width1 and Y < mouse[1] < Y + height1:

            # if mouse is hovered on a button
            # its colour shade becomes lighter
            pygame.draw.rect(screen, startl, [X, Y, width1, height1])
        else:
            if X < mouse[0] < X + width1 + 40 and Y + 70 < mouse[1] < Y + 70 + height1:
                pygame.draw.rect(screen, startl, [X, Y + 70, width1,height1])
            else:

                if X < mouse[0] < width1 + X and Y + 140 < mouse[1] < Y + 140 + height1:
                    pygame.draw.rect(screen, startl, [X, Y + 140,width1,height1])
                else:
                    pygame.draw.rect(screen, startd, [X, Y, width1,height1])
                    pygame.draw.rect(screen, startd, [X, Y + 70, width1, height1])
                    pygame.draw.rect(screen, startd, [X, Y + 140,width1, height1])


        # start button
        if event.type == pygame.MOUSEBUTTONDOWN:
            if X < mouse[0] < X + width1 and Y < mouse[1] < Y + height1:

                game(playerImg)
        if event.type == pygame.MOUSEBUTTONDOWN:
            if X < mouse[0] < width1 + X and Y + 140 < mouse[1] < Y + 140 + height1:
                pygame.quit()

        if event.type == pygame.MOUSEBUTTONDOWN:
            if X < mouse[0] < width1 + X and Y + 70 < mouse[1] < Y + 70 + height1:
                while rule_start:
                    screen.fill((0,0,0))
                    mouse = pygame.mouse.get_pos()

                    if 0 <= rezoid_c1 <= 254 or 0 <= rezoid_c2 <= 254:
                        rezoid_c1 += 1
                        rezoid_c2 += 1

                    if rezoid_c1 >= 254 or rezoid_c2 >= 254:
                        rezoid_c1 = c3
                        rezoid_c2 = c3

                    rules = bigfont.render('Rules:', True, (c1, rezoid_c1, rezoid_c2))
                    rules_para1 = ultrasmallfont.render("1. Avoid touching garbage.", True, white)
                    rules_para2 = ultrasmallfont.render("2. You should move towards recyclable items to collect points.", True, white)
                    rules_para3 = ultrasmallfont.render("3. Use arrow keys to move.", True, white)
                    rules_para4 = ultrasmallfont.render("4. You have three lives when starting off. When you bump into", True, white)
                    rules_para5 = ultrasmallfont.render("      a garbage, you'll lose a life. If you lose all 3 lives, you lose.", True, white)
                    screen.blit(rules_para1, (50, 270))
                    screen.blit(rules_para2, (50, 320))
                    screen.blit(rules_para3, (50, 370))
                    screen.blit(rules_para4, (50, 420))
                    screen.blit(rules_para5, (50, 470))
                    screen.blit(rules, (120, 70))
                    exit1 = smallfont.render('Exit', True, white)
                    pygame.draw.rect(screen, (c2, rezoid_c1, rezoid_c2), [0, 550, 720, 600])
                    pygame.draw.rect(screen, (c2, rezoid_c1, rezoid_c2), [0, 0, 720, 50])
                    # exit button for rules menu


                    if 630 < mouse[0] < 720 and 550 < mouse[1] < 720:
                        pygame.draw.rect(screen, startl, [630, 550, 640, 555])
                    else:
                        pygame.draw.rect(screen, startd, [630, 550, 640, 555])
                    screen.blit(exit1, (640, 560))
                    clock = pygame.time.Clock()
                    clock.tick(50)
                    pygame.display.update()

                    pos = pygame.mouse.get_pos()
                    pressed1 = pygame.mouse.get_pressed()[0]

                    for event in pygame.event.get():
                        if event.type == pygame.QUIT:
                            if event.type == pygame.QUIT:
                                pygame.quit()
                                rule_start = False

                    if (630 < pos[0] < 720 and 550 < pos[1] < 720) and pressed1:
                        rule_start = False
                        intro(rezoid_c1,rezoid_c2,rezoid,exit1,text1,text,)
                        clock = pygame.time.Clock()
                        clock.tick(50)
                        pygame.display.update()

        # this handles the colour breezing effect
        if 0 <= rezoid_c1 <= 254 or 0 <= rezoid_c2 <= 254:
            rezoid_c1 += 1
            rezoid_c2 += 1
        if rezoid_c1 >= 254 or rezoid_c2 >= 254:
          rezoid_c1 = c3
          rezoid_c2 = c3

        pygame.draw.rect(screen, (c2, rezoid_c1, rezoid_c2), [0, 0, 40,height])
        pygame.draw.rect(screen, (c2, rezoid_c1, rezoid_c2), [width - 40, 0, 40, height])
        smallfont = pygame.font.SysFont('Corbel', 35)
        sig = smallsmallfont.render('Designed by: Krish and Umer', True, (128,128,128))
        text = smallfont.render('Start', True, white)
        text1 = smallfont.render('Rules', True, white)
        exit1 = smallfont.render('Exit', True, white)
        rezoid = bigfont.render('ReZoid', True, (c1, rezoid_c1, rezoid_c2))
        screen.blit(rezoid, (100, 75))
        screen.blit(text, (312, 295))
        screen.blit(text1, (312, 365))
        screen.blit(exit1, (312, 435))
        screen.blit(sig, (190, 70))
        clock = pygame.time.Clock()
        clock.tick(50)
        pygame.display.update()




#================================================================== MAIN  FUNCTION===============================
user_name = input("Hello! What is your name? ")
print("Nice to meet you {0}!".format(user_name))
user_gender = input("What gender do you want your character to be? (male/female): ")

while (user_gender != "male" and user_gender != "female"):
    user_gender = input("What gender do you want your character to be? ")

if user_gender == "male":
    playerImg = pygame.image.load("images/male.png")
elif user_gender == "female":
    playerImg = pygame.image.load("images/female.png")

intro(rezoid_c1,rezoid_c2,rezoid,exit1,text1,text)
