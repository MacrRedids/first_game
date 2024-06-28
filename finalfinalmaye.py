import os
import random
import pygame
from pygame.locals import *


# Constants and Initialization
FPS = 60
SCREENWIDTH = 700
SCREENHEIGHT = 700

# Colors
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
BLUE = (0, 0, 255)
LIGHT_BLUE = (173, 216, 230)

# Initialization
pygame.init()
FPSCLOCK = pygame.time.Clock()
pygame.mixer.init()
pygame.font.init()

# Setting File Directories
imgf = 'assets/cardassets/'
img = 'assets/'
musicf = 'assets/music/'

# Load and play background music
pygame.mixer.music.load(musicf + 'game-music-loop-19-153393.mp3')
pygame.mixer.music.set_volume(0.5)
pygame.mixer.music.play(-1)

# Setting the Screen
sc = pygame.display.set_mode((SCREENWIDTH, SCREENHEIGHT))
title = pygame.image.load(img + "title1.png")
title = pygame.transform.scale(title, (300, 200))
pygame.display.set_caption("PURRFECT PAIRS")
pygame.display.set_icon(title)

# Loading the Images for the Memory Game
cardlist1 = []
for u in os.listdir('assets/cardassets/'):
    cardlist1.append(u.split(".")[0])
cardlist1copy = cardlist1.copy()
cardlist1.extend(cardlist1copy)
cardlist1copy.clear()

# Game Variables
gamecolmn = 4
gamerows = 3
padding = 10
title_height = 200
available_height = SCREENHEIGHT - title_height - padding * 2
available_width = SCREENWIDTH - padding * 2

# Calculate optimal card size
card_width = available_width // gamecolmn - padding
card_height = available_height // gamerows - padding

# Loading images in list
cardpics = []  # CARD pictures
cardstate = []  # CARD if open or not
cardhb = []  # CARD hitbox
cardlist = []  # CARD PAIR indexes
cardface = []  # CARD phase

for t in cardlist1:
    pc = pygame.image.load(imgf + t + ".png")
    pc = pygame.transform.scale(pc, (card_width, card_height))
    cardpics.append(pc)
    cardrect = pc.get_rect()
    cardhb.append(cardrect)

# Face and Base Sync Shuffler
randomizer = list(range(len(cardlist1)))
random.shuffle(randomizer)

def shuffler(lst, face, randlist):
    for o in randlist:
        cardlist.insert(o, lst[o])
        cardface.insert(o, face[o])
    print(cardlist)
    print(cardface)

# Importing IMG Assets
bg = pygame.image.load(img + 'bgmenu.png')
bgg = pygame.image.load(img + 'bg5.png')
stbt = pygame.image.load(img + 'stbt.png')
cb = pygame.image.load(img + 'cardback.png')
cb = pygame.transform.scale(cb, (card_width, card_height))
stb = pygame.image.load(img + 'stbt.png')
stb = pygame.transform.scale(stb, (150, 155))
credit_button = pygame.image.load(img + 'credit2.png')
tutorial_button = pygame.image.load(img + 'tutorial (2).png')
mute_button = pygame.image.load(img + 'mute_button.png')

# Load the new music track for when the game is completed
complete_music = musicf + 'game-complete.mp3'

# Font settings
font = pygame.font.SysFont(None, 40)

def draw_text(text, font, color, surface, x, y):
    textobj = font.render(text, True, color)
    textrect = textobj.get_rect()
    textrect.center = (x, y)
    surface.blit(textobj, textrect)

# Card Settings
for item in range(len(cardhb)):
    cardhb[item][0] = padding + ((card_width + padding) * (item % gamecolmn))
    cardhb[item][1] = title_height + padding + ((card_height + padding) * (item // gamecolmn))
    cardstate.append(False)

# Mute Button Settings
mute_button_img = pygame.image.load(img + 'mute_button.png')
mute_button_img = pygame.transform.scale(mute_button_img, (50, 50))
mute_button_rect = mute_button_img.get_rect()
mute_button_rect.bottomright = (SCREENWIDTH - 20, SCREENHEIGHT - 20)
mute = False  # Initially sound is not muted

def toggle_sound():
    global mute
    if mute:
        pygame.mixer.music.unpause()
        mute = False
    else:
        pygame.mixer.music.pause()
        mute = True

# Confetti Effect Settings
class ConfettiParticle:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.color = random.choice([WHITE, BLUE, LIGHT_BLUE])  # Random confetti color
        self.vel_x = random.randint(-3, 3)  # Random horizontal velocity
        self.vel_y = random.randint(-5, -1)  # Random vertical velocity

    def move(self):
        self.x += self.vel_x
        self.y += self.vel_y

    def draw(self, surface):
        pygame.draw.circle(surface, self.color, (int(self.x), int(self.y)), 3)

confetti_particles = []

def create_confetti(num_particles, x, y):
    global confetti_particles
    for _ in range(num_particles):
        particle = ConfettiParticle(x, y)
        confetti_particles.append(particle)

def update_confetti():
    global confetti_particles
    for particle in confetti_particles:
        particle.move()
        particle.draw(sc)

def reset_confetti():
    global confetti_particles
    confetti_particles = []

# GAME PROPER
def gamemain():
    gameloop = True
    shuffler(cardlist1, cardpics, randomizer)

    sel1 = None
    sel2 = None
    while gameloop:
        sc.blit(bgg, (0, 0))
        sc.blit(title, (SCREENWIDTH // 2 - 150, 0))

        for event in pygame.event.get():
            if event.type == QUIT:
                return
            if event.type == MOUSEBUTTONDOWN and event.button == 1:
                print(event.pos)
                for box in cardhb:
                    if box.collidepoint(event.pos):
                        if not cardstate[cardhb.index(box)]:
                            if sel1 is not None:
                                sel2 = cardhb.index(box)
                                cardstate[sel2] = True
                                print(cardstate)
                            else:
                                sel1 = cardhb.index(box)
                                cardstate[sel1] = True
                                print(cardstate)
            # Check if mute button is clicked
            if event.type == MOUSEBUTTONDOWN and event.button == 1:
                if mute_button_rect.collidepoint(event.pos):
                    toggle_sound()

        # Draw mute button
        sc.blit(mute_button_img, mute_button_rect)

        for k in range(len(cardlist)):
            if cardstate[k]:
                sc.blit(cardface[k], cardhb[k])
            else:
                sc.blit(cb, cardhb[k])

        pygame.display.update()

        if sel1 is not None and sel2 is not None:
            if cardlist[sel1] == cardlist[sel2]:
                sel1, sel2 = None, None
            else:
                pygame.time.wait(1000)
                print(cardlist[sel1], cardlist[sel2])
                cardstate[sel1] = False
                cardstate[sel2] = False
                sel1, sel2 = None, None

        # Check if all pairs are matched
        if all(cardstate):
            gameloop = False
            pygame.mixer.music.stop()
            pygame.mixer.music.load(complete_music)
            pygame.mixer.music.play(-1)
            create_confetti(200, SCREENWIDTH // 2, SCREENHEIGHT // 2)  # Create confetti at the center
            game_end_screen()

        update_confetti()  # Update and draw confetti particles
        pygame.display.update()

def game_end_screen():
    end_loop = True
    while end_loop:
        sc.blit(bgg, (0, 0))
        sc.blit(title, (SCREENWIDTH // 2 - 150, 0))
        draw_text('You Win!', font, BLACK, sc, SCREENWIDTH // 2, 200)
        mouse_pos = pygame.mouse.get_pos()
        try_again_color = BLACK  # No hover effect, so set to BLACK directly
        home_color = BLACK  # No hover effect, so set to BLACK directly
        try_again_rect = pygame.draw.rect(sc, (0, 0, 255), pygame.Rect((SCREENWIDTH // 2) - 75, 300, 150, 50))
        home_rect = pygame.draw.rect(sc, (0, 0, 255), pygame.Rect((SCREENWIDTH // 2) - 75, 400, 150, 50))

        draw_text('Restart', font, WHITE, sc, SCREENWIDTH // 2, 325)
        draw_text('Quit', font, WHITE, sc, SCREENWIDTH // 2, 425)

        for event in pygame.event.get():
            if event.type == QUIT:
                end_loop = False
            if event.type == MOUSEBUTTONDOWN and event.button == 1:
                if try_again_rect.collidepoint(event.pos):
                    reset_game()
                    end_loop = False
                if home_rect.collidepoint(event.pos):
                    pygame.mixer.music.stop()
                    pygame.mixer.music.load(musicf + 'game-music-loop-19-153393.mp3')
                    pygame.mixer.music.play(-1)
                    end_loop = False

        update_confetti()  # Update and draw confetti particles

        pygame.display.update()

def reset_game():
    global cardstate, cardlist, cardface, randomizer
    cardstate = [False] * len(cardlist)
    cardlist = []
    cardface = []
    reset_confetti()  # Reset confetti particles
    random.shuffle(randomizer)
    pygame.mixer.music.stop()
    pygame.mixer.music.load(musicf + 'game-music-loop-19-153393.mp3')
    pygame.mixer.music.play(-1)
    gamemain()

def show_new_image(image_name):
    new_image_loop = True
    while new_image_loop:
        if image_name == "credit2.png":
            sc.blit(credit_button, (0, 0))
        elif image_name == "tutorial (2).png":
            sc.blit(tutorial_button, (0, 0))
        for event in pygame.event.get():
            if event.type == QUIT:
                new_image_loop = False
            if event.type == KEYDOWN and event.key == K_ESCAPE:
                new_image_loop = False

        pygame.display.update()

maingameloop = True
while maingameloop:
    sc.blit(bgg, (0, 0))
    sc.blit(title, ((SCREENWIDTH // 2) - 150, 0))
    stbtt = pygame.draw.rect(sc, (0, 0, 0), pygame.Rect((SCREENWIDTH // 2) - 45, 340, 90, 80))
    mouse_pos = pygame.mouse.get_pos()
    credit_button_color = BLACK  # No hover effect, so set to BLACK directly
    credit_button_rect = pygame.draw.rect(sc, (9,13, 239), pygame.Rect((SCREENWIDTH // 2) - 75, 450, 150, 50))

    sc.blit(stb, ((SCREENWIDTH // 2) - 75, 300))
    draw_text('Credit', font, WHITE, sc, (SCREENWIDTH // 2), 475)

    tutorial_rect = pygame.draw.rect(sc, (9,13, 239), pygame.Rect((SCREENWIDTH // 2) - 75, 550, 150, 50))
    draw_text('Tutorial', font, WHITE, sc, (SCREENWIDTH // 2), 575)

    for event in pygame.event.get():
        if event.type == QUIT:
            maingameloop = False
        if event.type == MOUSEBUTTONDOWN and event.button == 1:
            if stbtt.collidepoint(event.pos):
                gamemain()
            if credit_button_rect.collidepoint(event.pos):
                show_new_image("credit2.png")
            if tutorial_rect.collidepoint(event.pos):
                show_new_image("tutorial (2).png")  # Display tutorial image on clicking "Tutorial" button
            # Check if mute button is clicked
            if mute_button_rect.collidepoint(event.pos):
                toggle_sound()

    # Draw mute button
    sc.blit(mute_button_img, mute_button_rect)

    pygame.display.update()

pygame.quit()











