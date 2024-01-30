import pygame
import random
import time
pygame.init()
path = "C:\\Users\\Yotam\\New folder\\Tanach\\Tanach\\images\\"
scrwidth, scrheight, fps = 900, 500, 120
arial40 = pygame.font.SysFont("Arial", 40)
arial35 = pygame.font.SysFont("Arial", 35)
arial30 = pygame.font.SysFont("Arial", 30)
arial25 = pygame.font.SysFont("Arial", 25)

colors = {
    "black": (0, 0, 0),
    "darkblue": (0, 0, 51),
    "gold": (191, 146, 23),
    "red": (255, 0, 0),
    "lightblue": (102, 255, 255),
    "purple":(75,0,130),
    "white": (255, 255, 255)
}
screenedges = [pygame.Rect((0,5,900,1)), pygame.Rect((0,495,900,1)),pygame.Rect((895,0,1,500)),pygame.Rect((5,0,1,500))]
screen = pygame.display.set_mode((scrwidth, scrheight))
pygame.display.set_caption("Creation!")
clock = pygame.time.Clock()



def Tick(fps):
    clock.tick(fps)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            return False
    return True


def Fade(color,width):
        for collum in range(scrwidth // width):
            if Tick(fps) == False:
                return False
            screen.fill(color, rect=(width * collum, 0, width, 500))
            pygame.display.update()
        return True

def Push_Box(Player, Object, bgcolor):
        if Player.rect.colliderect(Object.rect) == True:

            if Player.rect.right >= Object.rect.left and Player.rect.left < Object.rect.left:
                pygame.draw.rect(screen, bgcolor, Object.rect)
                Object.rect.x += (Player.rect.right - Object.rect.left) + 1
                screen.blit(Object.img, (Object.rect.x, Object.rect.y))
                pygame.display.update()
                return

            elif Player.rect.left <= Object.rect.right and Player.rect.left > Object.rect.left:
                pygame.draw.rect(screen, bgcolor, Object.rect)
                Object.rect.x -= (Object.rect.right - Player.rect.left) + 1
                screen.blit(Object.img, (Object.rect.x, Object.rect.y))
                pygame.display.update()
                return
        else:
            return False



class Player(pygame.sprite.Sprite):
    def __init__(self, x, y, keys, img):
        super().__init__()

        self.img = img
        self.rect = self.img.get_rect()
        self.isjump = False
        self.jumpcount = 60
        self.rect.x = x
        self.rect.y = y
        self.base = y + self.rect.h
        self.keys = keys



    def Get_Base(self, bases):
        for key in bases:
            if key[0] <= self.rect.x <= key[1]:
                return bases[key]
        else:
            return False

    def Move_Player(self, keyspressed, speed, barriers, vertical = True):
        x, y = self.rect.x, self.rect.y

        if keyspressed[self.keys[0]] and vertical:
            self.rect.y -= speed
            for barrier in barriers:
                if barrier.colliderect(self.rect):
                    self.rect.y += speed

        if keyspressed[self.keys[1]] and vertical:
            self.rect.y += speed
            for barrier in barriers:
                if barrier.colliderect(self.rect):
                    self.rect.y -= speed


        if keyspressed[self.keys[2]]:
            self.rect.x += speed
            for barrier in barriers:
                if barrier.colliderect(self.rect):
                    self.rect.x -= speed


        if keyspressed[self.keys[3]]:
            self.rect.x -= speed
            for barrier in barriers:
                if barrier.colliderect(self.rect):
                    self.rect.x += speed

        return 1

    def Move_Player_Gravity(self, keyspressed, speed, gravity, barriers, bases):
        if keyspressed[self.keys[3]]:
            self.rect.x -= speed
            for barrier in barriers:
                if barrier.colliderect(self.rect):
                    self.rect.x += speed
        if keyspressed[self.keys[2]]:
            self.rect.x += speed
            for barrier in barriers:
                if barrier.colliderect(self.rect):
                    self.rect.x -= speed

        base = self.Get_Base(bases)



        formerjmp = self.jumpcount
        if base > self.rect.bottom:
            self.isjump = True
            self.jumpcount = 30
        if keyspressed[self.keys[0]] == True:
            self.isjump = True
            self.jumpcount = formerjmp


        if self.isjump:
            vec = 1 - 2 * int(self.jumpcount <= 30)
            self.rect.y -= vec * gravity
            for barrier in barriers:
                if barrier.colliderect(self.rect):
                    self.rect.y += vec * gravity
            self.jumpcount -= 1
            if self.rect.bottom >= base:
                self.isjump = False
                self.jumpcount = 60

        return





def Print_Day_One_A(genesisdelay, fadewidth):
    t = time.perf_counter()
    while time.perf_counter() - t < genesisdelay + 3:
        if Tick(fps) == False:
            return False

        screen.fill(colors["black"])
        screen.blit(arial40.render("בְּרֵאשִׁית, בָּרָא אֱלֹהִים, אֵת הַשָּׁמַיִם, וְאֵת הָאָרֶץ."[::-1], True, colors["gold"]), (100, 200))
        pygame.display.update()

    if Fade(colors["darkblue"], fadewidth) == False:
        return False
    else:
        pygame.draw.rect(screen, colors["black"],(0,75,900,5))
        pygame.draw.rect(screen, colors["red"], (850,150,50,50))
        pygame.draw.rect(screen, colors["red"], (850,300,50,50))
        screen.blit(arial30.render("וְחֹשֶׁךְ, עַל-פְּנֵי תְהוֹם; וְרוּחַ אֱלֹהִים, מְרַחֶפֶת עַל-פְּנֵי הַמָּיִם"[::-1], True, colors["gold"]), (140, 25))
        pygame.display.update()
    return True



def Play_Day_One_A(ghost, barriers): #closed game -> false, onto b-> true
    barriers += [pygame.Rect((850,150,50,50)), pygame.Rect((850,300,50,50))]
    while True:
        if Tick(fps) == False:
            return False
        else:
            keyspressed = pygame.key.get_pressed()
            pygame.draw.rect(screen,colors["darkblue"], ghost.rect)
            ghost.Move_Player(keyspressed,6, barriers)
            screen.blit(ghost.img, (ghost.rect.x, ghost.rect.y))
            pygame.display.update()

            if ghost.rect.right >= 892 and ghost.rect.bottom <= 300 and ghost.rect.top >= 200:
                ghost.rect.x  = 6
                break
    return True


def Print_Day_One_B(buttonimg):
    if Tick(fps) == False:
        return False
    screen.fill(colors["darkblue"])
    pygame.draw.rect(screen, colors["black"], (0, 75, 900, 5))
    pygame.draw.rect(screen, colors["red"], (850, 150, 50, 50))
    pygame.draw.rect(screen, colors["red"], (850, 300, 50, 50))
    screen.blit(arial35.render("וַיֹּאמֶר אֱלֹהִים, יְהִי אוֹר;"[::-1], True, colors["gold"]), (395, 25))
    screen.blit(buttonimg, (550, 465))
    pygame.display.update()
    return True


def Play_Day_One_B(ghost,box, barriers):
    barriers  = [pygame.Rect((box.rect.x, box.rect.y, box.rect.w, 2)), pygame.Rect(550,465,80,50)] + barriers
    bgcolor = colors["darkblue"]
    cntr = 1
    pressed = False
    while True:
        if Tick(fps) == False:
            return False
        else:
            screen.blit(box.img, (box.rect.x, box.rect.y))
            barriers[0].x = box.rect.x
            boxedge = []
            if box.rect.left <= 10:
                boxedge.append(pygame.Rect(box.rect))

            pygame.draw.rect(screen,bgcolor, ghost.rect)
            keyspressed = pygame.key.get_pressed()
            ghost.Move_Player(keyspressed,6, barriers + boxedge)
            Push_Box(ghost,box, bgcolor)
            screen.blit(ghost.img, (ghost.rect.x, ghost.rect.y))
            pygame.display.update()

            if box.rect.left >= 545 and cntr == 1:
                pressed = True
                cntr += 1
                barriers.append(box.rect)
                bgcolor = colors["lightblue"]
                screen.fill(bgcolor)
                screen.blit(ghost.img, (ghost.rect.x, ghost.rect.y))
                screen.blit(box.img, (box.rect.x, box.rect.y))
                pygame.draw.rect(screen, colors["black"], (0, 75, 900, 5))
                pygame.draw.rect(screen, colors["red"], (850, 150, 50, 50))
                pygame.draw.rect(screen, colors["red"], (850, 300, 50, 50))
                screen.blit( arial35.render("וַיֹּאמֶר אֱלֹהִים, יְהִי אוֹר; וַיְהִי-אוֹר"[::-1], True, colors["gold"]), (280, 25))
                pygame.display.update()

            if ghost.rect.right >= 889 and ghost.rect.bottom <= 300 and ghost.rect.top >= 200 and pressed:
                ghost.rect.x  = 6
                return True








def Day_One():
    dayonebarriers = [pygame.Rect((0, 75, 900, 5))] + screenedges
    ghostimg = pygame.image.load(path + "ghostnobg.png")
    ghostimg = pygame.transform.flip(ghostimg, True, False)
    ghostimg = pygame.transform.scale(ghostimg, (80, 80))
    boximg = pygame.image.load(path + "boxnobg.png")
    boximg = pygame.transform.scale(boximg, (90,90))
    buttonimg = pygame.image.load(path + "buttonnobg.png")
    buttonimg = pygame.transform.scale(buttonimg, (80,30))


    ghost = Player(70,200,[pygame.K_w, pygame.K_s,pygame.K_d, pygame.K_a], ghostimg)
    box = Player(350,405,[], boximg)


    if Print_Day_One_A(3, 8) == False:
        return 0
    else:
        if Play_Day_One_A(ghost, dayonebarriers) == False:
            return 0
        else:
            if Print_Day_One_B(buttonimg) == False:
                return 0
            else:
                if Play_Day_One_B(ghost,box, dayonebarriers) == False:
                    return 0
                else:
                    return 1
    return



def Print_Day_Two():
    if Tick(fps) == False:
        return False
    screen.fill(colors["lightblue"])
    pygame.draw.rect(screen, colors["black"], (0, 75, 900, 5))
    screen.blit(arial30.render("וַיֹּאמֶר אֱלֹהִים, יְהִי רָקִיעַ בְּתוֹךְ הַמָּיִם, וִיהִי מַבְדִּיל, בֵּין מַיִם לָמָיִם."[::-1], True, colors["gold"]), (115, 25))
    pygame.draw.rect(screen, colors["red"], (850,150,50,50))
    pygame.draw.rect(screen, colors["red"], (850,300,50,50))
    pygame.display.update()
    return True





def Play_Day_Two(ghost, wave, waterimg, barriers):
    barriers += [pygame.Rect((850,150,50,50)), pygame.Rect((850,300,50,50))]
    wavespeed = 0

    while True:
        if Tick(fps) == False:
            return 0
        else:
            wavespeed += 1/fps
            keyspressed = pygame.key.get_pressed()
            pygame.draw.rect(screen,colors["lightblue"], ghost.rect)
            pygame.draw.rect(screen,colors["lightblue"], wave.rect)
            ghost.Move_Player(keyspressed,6, barriers)
            wave.rect.x = (wave.rect.x - wavespeed) % 630
            screen.blit(ghost.img, (ghost.rect.x, ghost.rect.y))
            screen.blit(wave.img, (wave.rect.x, wave.rect.y))
            screen.blit(waterimg, (0, 350))
            pygame.display.update()

            waveborder = pygame.Rect((wave.rect.x + 50, wave.rect.y + 50, wave.rect.w - 80, wave.rect.h - 80))
            if ghost.rect.colliderect(waveborder):
                return 2


            if ghost.rect.right >= 892 and ghost.rect.bottom <= 300 and ghost.rect.top >= 200:
                ghost.rect.x  = 6
                return 1


def Day_Two():
    daytwobarriers = [pygame.Rect((0, 75, 900, 5)), pygame.Rect((0, 350, 900, 5))] + screenedges
    waterimg = pygame.image.load(path + "waternobg.jpg")
    waterimg = pygame.transform.scale(waterimg, (900, 150))
    waveimg = pygame.image.load(path + "wavenobg.png")
    waveimg = pygame.transform.flip(waveimg, True, False)
    waveimg = pygame.transform.scale(waveimg, (220,220))
    ghostimg = pygame.image.load(path + "ghostnobg.png")
    ghostimg = pygame.transform.flip(ghostimg, True, False)
    ghostimg = pygame.transform.scale(ghostimg, (80, 80))

    wave = Player(500,208,[], waveimg)
    ghost = Player(70,270,[pygame.K_w, pygame.K_s,pygame.K_d, pygame.K_a], ghostimg)

    if Print_Day_Two() == False:
        return 0
    else:
        return Play_Day_Two(ghost, wave,waterimg, daytwobarriers)




def Print_Day_Three(groundimg, waterimg):
    if Tick(fps) == False:
        return False
    screen.fill(colors["lightblue"])
    pygame.draw.rect(screen, colors["black"], (0, 75, 900, 5))
    screen.blit(arial30.render("וַיֹּאמֶר אֱלֹהִים, יִקָּווּ הַמַּיִם מִתַּחַת הַשָּׁמַיִם אֶל-מָקוֹם אֶחָד, וְתֵרָאֶה, הַיַּבָּשָׁה"[::-1], True, colors["gold"]), (70, 25))
    screen.blit(groundimg, (0, 400))
    screen.blit(groundimg, (650, 400))
    screen.blit(waterimg, (250, 400))
    pygame.display.update()
    return True


def Play_Day_Three(ghost, platform1, platform2, barriers, bases, grassimg):



    while True:
        if Tick(fps) == False:
            return 0
        else:
            pygame.draw.rect(screen,colors["black"], platform1)
            pygame.draw.rect(screen,colors["black"], platform2)
            pygame.draw.rect(screen,colors["lightblue"], ghost.rect)
            keyspressed = pygame.key.get_pressed()
            ghost.Move_Player_Gravity(keyspressed, 5, 7, barriers, bases)
            screen.blit(ghost.img, (ghost.rect.x, ghost.rect.y))
            pygame.display.update()
            if ghost.rect.colliderect(pygame.Rect(255, 395, 390, 5)):
                return 2
            if ghost.rect.left > 450:
                pygame.draw.rect(screen,colors["lightblue"], (0,0,900,75))
                screen.blit(grassimg, (0, 400))
                screen.blit(grassimg, (650, 400))
                screen.blit(arial30.render("וַתּוֹצֵא הָאָרֶץ דֶּשֶׁא עֵשֶׂב מַזְרִיעַ זֶרַע, לְמִינֵהוּ"[::-1], True, colors["gold"]), (225, 25))
            if ghost.rect.left > 810:
                return 1




def Day_Three():
    groundimg = pygame.image.load(path + "ground.jpeg")
    groundimg = pygame.transform.scale(groundimg, (250, 100))
    waterimg = pygame.image.load(path + "waternobg.jpg")
    waterimg = pygame.transform.scale(waterimg, (400, 100))
    grassimg = pygame.image.load(path + "grassnobg.png")
    grassimg = pygame.transform.scale(grassimg, (250, 100))
    ghostimg = pygame.image.load(path + "ghostnobg.png")
    ghostimg = pygame.transform.flip(ghostimg, True, False)
    ghostimg = pygame.transform.scale(ghostimg, (80, 80))

    ghost = Player(70, 320, [pygame.K_w, pygame.K_s, pygame.K_d, pygame.K_a], ghostimg)


    platform1 = pygame.Rect(300, 275, 100,50)
    platform2 = pygame.Rect(500, 275, 100,50)
    daythreebarriers = screenedges + [platform1, platform2, pygame.Rect(0, 75, 900, 5)]
    daythreebases = {(0,219):400, (220,399):275, (400, 419):400, (420, 599):275,(600, 900):400}


    if Print_Day_Three(groundimg, waterimg) == False:
        return 0
    else:
        return Play_Day_Three(ghost, platform1, platform2, daythreebarriers, daythreebases, grassimg)


def Print_Day_Four(darkskyimg, lightskyimg, grassimg, light = False):
    if light:
        sky = lightskyimg
    else:
        sky = darkskyimg

    if Tick(fps) == False:
            return False
    screen.blit(sky, (0,0))
    screen.blit(grassimg, (0,400))

    pygame.draw.rect(screen, colors["black"], (0, 75, 900, 5))
    screen.blit(arial30.render("וַיֹּאמֶר אֱלֹהִים, יְהִי מְאֹרֹת בִּרְקִיעַ הַשָּׁמַיִם, לְהַבְדִּיל, בֵּין הַיּוֹם וּבֵין הַלָּיְלָה"[::-1], True, colors["gold"]), (75, 25))
    pygame.display.update()
    return True




def Play_Day_Four(ghost, button, barriers, bases, darkskyimg, lightskyimg, grassimg):
    light = False
    while True:
        if Tick(fps) == False:
            return False
        else:
            Print_Day_Four(darkskyimg, lightskyimg, grassimg, light)
            screen.blit(button.img, (button.rect.x, button.rect.y))
            keyspressed = pygame.key.get_pressed()
            ghost.Move_Player_Gravity(keyspressed, 6, 7, barriers, bases)
            screen.blit(ghost.img, (ghost.rect.x, ghost.rect.y))
            pygame.display.update()
            if ghost.rect.bottom <= button.rect.top and ghost.rect.right >= button.rect.left and ghost.rect.left <= button.rect.right and ghost.rect :
                light = True
            if ghost.rect.left > 810 and light == True:
                return 1




def Day_Four():

    darkskyimg = pygame.image.load(path + "darkskynobg.png")
    darkskyimg = pygame.transform.scale(darkskyimg, (900, 400))
    lightskyimg = pygame.image.load(path + "lightskynobg.png")
    lightskyimg = pygame.transform.scale(lightskyimg, (900, 500))
    grassimg = pygame.image.load(path + "grassnobg.png")
    grassimg = pygame.transform.scale(grassimg, (900, 100))
    buttonimg = pygame.image.load(path + "buttonnobg.png")
    buttonimg = pygame.transform.scale(buttonimg, (80,30))
    ghostimg = pygame.image.load(path + "ghostnobg.png")
    ghostimg = pygame.transform.flip(ghostimg, True, False)
    ghostimg = pygame.transform.scale(ghostimg, (80, 80))

    button = Player(380, 250, [], buttonimg)
    ghost = Player(70, 320, [pygame.K_w, pygame.K_s, pygame.K_d, pygame.K_a], ghostimg)

    dayfourbarriers = screenedges + [button.rect]
    dayfourbases = {(0,299):400, (300,459):300, (460, 900):400}
    if Print_Day_Four(darkskyimg, lightskyimg, grassimg) == False:
        return 0
    else:
        return Play_Day_Four(ghost, button, dayfourbarriers, dayfourbases, darkskyimg, lightskyimg, grassimg)





def Print_Day_Five(skyimg, grassimg, croc = False):
    if Tick(fps) == False:
            return False
    screen.blit(skyimg, (0,0))
    screen.blit(grassimg, (0,400))

    pygame.draw.rect(screen, colors["black"], (0, 75, 900, 5))
    if croc:
        screen.blit(arial30.render("וַיִּבְרָא אֱלֹהִים, אֶת-הַתַּנִּינִם הַגְּדֹלִים"[::-1], True, colors["gold"]), (250, 25))
    else:
        screen.blit(arial25.render("יֹּאמֶר אֱלֹהִים--יִשְׁרְצוּ הַמַּיִם, שֶׁרֶץ נֶפֶשׁ חַיָּה; וְעוֹף יְעוֹפֵף עַל-הָאָרֶץ, עַל-פְּנֵי רְקִיעַ הַשָּׁמָיִם."[::-1], True, colors["gold"]), (20, 25))
    pygame.display.update()
    return True


def Play_Day_Five(ghost, crocodile, bird, platform, barriers, skyimg, grassimg):
    cntr = 0
    croc = False
    while True:
        if Tick(fps) == False:
            return 0
        else:
            cntr += 1
            barriers[-1] = crocodile.rect
            bases = {(0, crocodile.rect.left - 81):400, (crocodile.rect.left - 80, crocodile.rect.right):crocodile.rect.top,
                    (crocodile.rect.right + 1, 780):400, (781, 900):300}

            Print_Day_Five(skyimg, grassimg, croc)
            pygame.draw.rect(screen,colors["red"], platform)
            keyspressed = pygame.key.get_pressed()
            ghost.Move_Player_Gravity(keyspressed, 2, 5, barriers, bases)
            crocodile.Move_Player(keyspressed, 2, barriers[:-1], False)
            screen.blit(crocodile.img, (crocodile.rect.x, crocodile.rect.y))
            screen.blit(ghost.img, (ghost.rect.x, ghost.rect.y))
            screen.blit(bird.img, (bird.rect.x, bird.rect.y))
            bird.rect.x = (bird.rect.x  - 5) % 700
            pygame.display.update()
            if ghost.rect.colliderect(bird.rect):
                return 2
            pygame.display.update()
            if cntr > 180:
                croc = True
            if ghost.rect.right > 880 and ghost.rect.bottom >= platform.top:
                return 1



def Day_Five():
    crocodileimg = pygame.image.load(path + "crocodilenobg.png")
    crocodileimg = pygame.transform.scale(crocodileimg, (100, 100))
    birdimg = pygame.image.load(path + "birdnobg.png")
    birdimg = pygame.transform.scale(birdimg, (80, 80))
    grassimg = pygame.image.load(path + "grassnobg.png")
    grassimg = pygame.transform.scale(grassimg, (900, 100))
    lightskyimg = pygame.image.load(path + "lightskynobg.png")
    lightskyimg = pygame.transform.scale(lightskyimg, (900, 500))
    ghostimg = pygame.image.load(path + "ghostnobg.png")
    ghostimg = pygame.transform.flip(ghostimg, True, False)
    ghostimg = pygame.transform.scale(ghostimg, (80, 80))

    ghost = Player(70, 320, [pygame.K_w, pygame.K_s, pygame.K_d, pygame.K_a], ghostimg)
    crocodile = Player(300, 300, [pygame.K_UP, pygame.K_DOWN, pygame.K_RIGHT, pygame.K_LEFT], crocodileimg)
    bird = Player(700, 150, [], birdimg)
    platform = pygame.Rect(850,200,50,50)

    dayfivebarriers = screenedges + [platform, crocodile.rect]


    if Print_Day_Five(lightskyimg, grassimg) == False:
        return 0
    else:
        return Play_Day_Five(ghost,crocodile,bird, platform, dayfivebarriers, lightskyimg, grassimg)


def Print_Day_Six(skyimg, grassimg, talkingbubbleimg, talk = False):
    if Tick(fps) == False:
            return False
    screen.blit(skyimg, (0,0))
    screen.blit(grassimg, (0,400))
    pygame.draw.rect(screen, colors["black"], (0, 75, 900, 5))
    screen.blit(arial35.render("יֹּאמֶר אֱלֹהִים, נַעֲשֶׂה אָדָם בְּצַלְמֵנוּ כִּדְמוּתֵנוּ"[::-1], True, colors["gold"]), (200, 25))
    if talk:
        pygame.draw.rect(screen, colors["white"],(280, 110, talkingbubbleimg.get_rect().w - 50, talkingbubbleimg.get_rect().h - 30))
        screen.blit(talkingbubbleimg, (250, 100))
        screen.blit(arial35.render("תודה ששיחקתם!"[::-1], True, colors["gold"]), (325,  125))
    pygame.display.update()
    return True


def Play_Day_Six(ghost, adamandeve, skyimg, grassimg, talkingbubbleimg, barriers, bases):
    talk = False
    while True:

        if Tick(fps) == False:
            return 0
        Print_Day_Six(skyimg, grassimg, talkingbubbleimg, talk)
        keyspressed = pygame.key.get_pressed()
        ghost.Move_Player_Gravity(keyspressed, 5, 7, barriers, bases)
        screen.blit(ghost.img, (ghost.rect.x, ghost.rect.y))
        screen.blit(adamandeve.img, (adamandeve.rect.x, adamandeve.rect.y))
        pygame.display.update()
        if talk == True:
            time.sleep(3)
            return 1
        if ghost.rect.colliderect(adamandeve.rect):
            talk = True

def Day_Six():
    grassimg = pygame.image.load(path + "grassnobg.png")
    grassimg = pygame.transform.scale(grassimg, (900, 100))
    lightskyimg = pygame.image.load(path + "lightskynobg.png")
    lightskyimg = pygame.transform.scale(lightskyimg, (900, 500))
    adamandeveimg = pygame.image.load(path + "adamandevenobg.png")
    adamandeveimg = pygame.transform.scale(adamandeveimg, (200, 200))
    talkingbubbleimg = pygame.image.load(path + "talkingbubblenobg.png")
    talkingbubbleimg = pygame.transform.scale(talkingbubbleimg, (400, 100))
    talkingbubbleimg = pygame.transform.flip(talkingbubbleimg, True, False)
    ghostimg = pygame.image.load(path + "ghostnobg.png")
    ghostimg = pygame.transform.flip(ghostimg, True, False)
    ghostimg = pygame.transform.scale(ghostimg, (80, 80))

    ghost = Player(70, 320, [pygame.K_w, pygame.K_s, pygame.K_d, pygame.K_a], ghostimg)
    adamandeve = Player(600, 200, [], adamandeveimg)
    daysixbases = {(0, 900):400}
    daysixbarriers = screenedges

    if Print_Day_Six(lightskyimg, grassimg, talkingbubbleimg) == False:
        return 0
    else:
        return Play_Day_Six(ghost, adamandeve, lightskyimg, grassimg, talkingbubbleimg, daysixbarriers, daysixbases)




def Print_Credits():
    while True:
        if Tick(fps) == False:
            return False
        else:
            screen.fill(colors["white"])
            screen.blit(arial35.render("Coded by yotamyo", True, colors["gold"]), (300, 100))
            screen.blit(arial35.render("& took way too long", True, colors["gold"]), (300, 300))
            pygame.display.update()


    return

def Main():
    status = Day_One()
    if status == 2:
        while status == 2:
            status = Day_One()
    if status == 1:
        status = Day_Two()
        if status == 2:
            while status == 2:
                status = Day_Two()
        if status == 1:
            status = Day_Three()
            if status == 2:
                while status == 2:
                    status = Day_Three()
            if status == 1:
                status = Day_Four()
                if status == 2:
                    while status == 2:
                        status = Day_Four()
                if status == 1:
                    status = Day_Five()
                    if status == 2:
                        while status == 2:
                            status = Day_Five()
                    if status == 1:
                        status = Day_Six()
                        if status == 1:
                            Print_Credits()


    return status





Main()

