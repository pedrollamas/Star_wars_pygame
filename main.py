import pygame
import os

pygame.init()   # To initialize the game
pygame.font.init()  # To load the font library
pygame.mixer.init() # To load the sounds.

# We define the width and height of the game
WIDTH, HEIGHT = 1000,600
WIN = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Zombies")

# We define the color to have a clear code since it uses RGB.
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
YELLOW = (255, 255, 0)

# We define the rectangle that acts as the border for the spaceships
BORDER = pygame.Rect(WIDTH//2 - 5, 0, 10, HEIGHT)

# We add the sound variables
BULLET_HIT_SOUND = pygame.mixer.Sound(os.path.join('Assets', 'Grenade+1.mp3'))
BULLET_FIRE_SOUND = pygame.mixer.Sound(os.path.join('Assets', 'Gun+Silencer.mp3'))


# We define the font used to show the health
HEALTH_FONT = pygame.font.SysFont('Verdana', 40)
# We define the font used to show the winner.
WINNER_FONT = pygame.font.SysFont('Verdana', 100)

# We define this in order for the game to not depend on how fast our system can run it. We define how often we want the game to update.
FPS = 60
# We define the velocity they are moving when they press keys.
VEL = 5
# We define the velocity of the bullets.
BULLET_VEL = 6
# We define the max bullets each player can use.
MAX_BULLETS = 10
SPACESHIP_WIDTH, SPACESHIP_HEIGHT = 55, 40

# We create the event of getting hit by the bullet.
YELLOW_HIT = pygame.USEREVENT + 1
RED_HIT = pygame.USEREVENT + 2

# Import the images for the spaceships. We do it with os so people in different systems can copy it.
YELLOW_SPACESHIP_IMAGE = pygame.image.load(os.path.join('Assets', 'spaceship_yellow.png'))
YELLOW_SPACESHIP = pygame.transform.rotate(pygame.transform.scale(YELLOW_SPACESHIP_IMAGE, 
                                                              (SPACESHIP_WIDTH, SPACESHIP_HEIGHT)), 90)

RED_SPACESHIP_IMAGE = pygame.image.load(os.path.join('Assets', 'spaceship_red.png'))
RED_SPACESHIP = pygame.transform.rotate(pygame.transform.scale(RED_SPACESHIP_IMAGE, (SPACESHIP_WIDTH, SPACESHIP_HEIGHT)), 270)

# We generate the backround because we checked white and the yellow bullets were hard to see.
SPACE = pygame.transform.scale(pygame.image.load(os.path.join('Assets', 'space.png')), (WIDTH, HEIGHT))

def draw_window(red, yellow, red_bullets, yellow_bullets, red_health, yellow_health):
    WIN.blit(SPACE, (0, 0)) # fill the background
    pygame.draw.rect(WIN, BLACK, BORDER)
    
    red_health_text = HEALTH_FONT.render("Health: " + str(red_health), 1, WHITE)
    yellow_health_text = HEALTH_FONT.render("Health: " + str(yellow_health), 1, WHITE)
    WIN.blit(red_health_text, (WIDTH - red_health_text.get_width() - 10, 10))
    WIN.blit(yellow_health_text, (10, 10))
    
    WIN.blit(YELLOW_SPACESHIP, (yellow.x, yellow.y)) # whwn you want to draw a surface
    WIN.blit(RED_SPACESHIP, (red.x, red.y))
    
    for bullet in red_bullets:
        pygame.draw.rect(WIN, RED, bullet)
    for bullet in yellow_bullets:
        pygame.draw.rect(WIN, YELLOW, bullet)
    
    pygame.display.update() # We always need to update pygame to display our changes

# We did it before without defining it so we create a function to not repeat it every time.
def yellow_handle_movement(keys_pressed, yellow):
    if keys_pressed[pygame.K_a] and yellow.x - VEL > 0:    # LEFT
        yellow.x -= VEL
    if keys_pressed[pygame.K_d] and yellow.x + VEL  + yellow.width < BORDER.x:    # RIGHT
        yellow.x += VEL
    if keys_pressed[pygame.K_w] and yellow.y - VEL > 0:    # UP    # We subtract when going up because in pygame the top left corner is (0,0)
        yellow.y -= VEL
    if keys_pressed[pygame.K_s] and yellow.y + VEL + yellow.height < HEIGHT - 15:    # DOWN # We make sure we don't allow it to go of the border (-15 is because a wing was allowed outside)
        yellow.y += VEL

def red_handle_movement(keys_pressed, red):
    if keys_pressed[pygame.K_LEFT] and red.x - VEL > BORDER.x + BORDER.width:    # LEFT
        red.x -= VEL
    if keys_pressed[pygame.K_RIGHT] and red.x + VEL  + red.width < WIDTH:    # RIGHT
        red.x += VEL
    if keys_pressed[pygame.K_UP] and red.y - VEL > 0:    # UP    # We subtract when going up because in pygame the top left corner is (0,0)
        red.y -= VEL
    if keys_pressed[pygame.K_DOWN] and red.y + VEL + red.height < HEIGHT - 15:    # DOWN
        red.y += VEL
 
def handle_bullets(yellow_bullets, red_bullets, yellow, red):
    for bullet in yellow_bullets:
        bullet.x += BULLET_VEL
        if red.colliderect(bullet):
            pygame.event.post(pygame.event.Event(RED_HIT))
            yellow_bullets.remove(bullet)
        elif bullet.x > WIDTH:
            yellow_bullets.remove(bullet)

    for bullet in red_bullets:
        bullet.x -= BULLET_VEL
        if yellow.colliderect(bullet):
            pygame.event.post(pygame.event.Event(YELLOW_HIT))
            red_bullets.remove(bullet)
        elif bullet.x < 0:
            red_bullets.remove(bullet)

def draw_winner(text):
    draw_text = WINNER_FONT.render(text, 1, WHITE)
    WIN.blit(draw_text, (WIDTH/2 - draw_text.get_width()/2, HEIGHT/2 - draw_text.get_height()/2))
    
    pygame.display.update()
    pygame.time.delay(4000)
    

def main():
    red = pygame.Rect(700, 300, SPACESHIP_WIDTH, SPACESHIP_HEIGHT) # we define the spaceships position
    yellow = pygame.Rect(100, 300, SPACESHIP_WIDTH, SPACESHIP_HEIGHT)
    
    red_bullets = []
    yellow_bullets = []
    
    # We define the health of players.
    red_health = 9
    yellow_health = 9
    
    clock = pygame.time.Clock()    
    run = True
    while run:
        clock.tick(FPS) # Ensures our game runs maximum at 60 FPS
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_CAPSLOCK and len(yellow_bullets) < MAX_BULLETS: # We add the condition to not shoot bulllets if its over the limit we defined.
                    bullet = pygame.Rect(yellow.x + yellow.width, yellow.y + yellow.height//2 - 2, 10, 5)   # We define where the bullets come from which is at the edge of the spaceship and the middle
                    yellow_bullets.append(bullet)
                    BULLET_FIRE_SOUND.play()
                                                        
                if event.key == pygame.K_SPACE and len(red_bullets) < MAX_BULLETS:
                    bullet = pygame.Rect(red.x, red.y + red.height//2 - 2, 10, 5)   
                    red_bullets.append(bullet)
                    BULLET_FIRE_SOUND.play()
            
            if event.type == RED_HIT:
                red_health -= 1
                BULLET_HIT_SOUND.play()
                
            if event.type == YELLOW_HIT:
                yellow_health -= 1
                BULLET_HIT_SOUND.play()     
        
        winner_text = ""
        if red_health <= 0:
            winner_text = "Yellow Wins!"
        
        if yellow_health <= 0:
            winner_text = "Red Wins!"
        
        if winner_text != "":
            draw_winner(winner_text)
            break
                
            
        keys_pressed = pygame.key.get_pressed() # to know the keys are currently being pressed.
        yellow_handle_movement(keys_pressed, yellow)
        red_handle_movement(keys_pressed, red)
        
        handle_bullets(yellow_bullets, red_bullets, yellow, red)
        
        
        draw_window(red, yellow, red_bullets, yellow_bullets, red_health, yellow_health)
        
main()

# We define this in order for the game to run when we execute this file.    
if __name__ == "__main__":
    main()
    