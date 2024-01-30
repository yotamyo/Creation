import pygame
scrwidth, scrheight = 900, 500
screen = pygame.display.set_mode((scrwidth, scrheight))
pygame.display.set_caption("myowngame")

imkapi = pygame.image.load('C:\\Users\\mzsga\\OneDrive\\Desktop\\Pythonpics\\kapi.jpg')
imram = pygame.image.load('C:\\Users\\mzsga\\OneDrive\\Pictures\\Screenshot 2023-10-22 135114.png')

kapi = pygame.transform.scale(imkapi, (200, 200))
ram = pygame.transform.scale(imram, (200, 200))

reckapi = pygame.Rect(30, 250, 200, 200)
recram = pygame.Rect(scrwidth - 230, 250, 200, 200)
fps = 120


def print_menu():
    screen.fill((255, 255, 255))
    screen.blit(kapi, (reckapi.x, reckapi.y))
    screen.blit(ram, (recram.x, recram.y))
    pygame.display.update()
    return
def movement(keys_pressed):
    if keys_pressed[pygame.K_a]:
        reckapi.x -= 1
    if keys_pressed[pygame.K_d]:
        reckapi.x += 1
    if keys_pressed[pygame.K_w]:
        reckapi.y -= 1
    if keys_pressed[pygame.K_s]:
        reckapi.y += 1
    if keys_pressed[pygame.K_LEFT]:
        recram.x -= 1
    if keys_pressed[pygame.K_RIGHT]:
        recram.x += 1
    if keys_pressed[pygame.K_UP]:
        recram.y -= 1
    if keys_pressed[pygame.K_DOWN]:
        recram.y += 1
    return


fps = 120

def main():


    running = True
    clock = pygame.time.Clock()
    while running:
        clock.tick(fps)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        keys_pressed = pygame.key.get_pressed()
        movement(keys_pressed)
        print_menu()

    pygame.quit()

main()
























class Player:
    # Assuming the Player class has attributes like x, y, and rect
    def __init__(self, x, y, keys, image):
        self.x = x
        self.y = y
        self.vel = 5
        self.isJump = False
        self.jumpCount = 10
        self.rect = pygame.Rect(x, y, image.get_width(), image.get_height())
        self.image = image

    def Move_Player_Gravity(self, keys, gravity, platforms):
        # Left and Right Movement
        if keys[pygame.K_a]:
            self.x -= self.vel
        if keys[pygame.K_d]:
            self.x += self.vel

        # Update the rect for collision detection
        self.rect.x = self.x

        # Gravity and Jumping
        if not self.isJump:
            if keys[pygame.K_w]:
                self.isJump = True
        else:
            if self.jumpCount >= -10:
                neg = 1
                if self.jumpCount < 0:
                    neg = -1
                self.y -= (self.jumpCount ** 2) * 0.5 * neg
                self.jumpCount -= 1
            else:
                self.isJump = False
                self.jumpCount = 10

        # Apply gravity
        self.y += gravity
        # Update the rect for collision detection
        self.rect.y = self.y

        # Collision detection with platforms
        for platform in platforms:
            if self.rect.colliderect(platform):
                self.y = platform.top - self.rect.height
                self.isJump = False
                self.jumpCount = 10

        # Update the rect position
        self.rect.topleft = (self.x, self.y)

# Your Day_Three function
def Day_Three():
    # ... your existing code ...

    # Create platforms list if there are any platforms
    platforms = []

    # Main game loop
    while True:
        # ... your existing code ...

        # Move the player with gravity
        ghost.Move_Player_Gravity(keyspressed, 2, platforms)

        # ... your existing code ...
