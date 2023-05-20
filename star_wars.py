# Libraries.
import pygame
import os

pygame.init()   # To initialize the game
pygame.font.init()  # To load the font library
pygame.mixer.init() # To load the sounds.

# We load the theme music and play while it runs.
pygame.mixer.music.load("Img/theme_music.mp3")
pygame.mixer.music.play(-1)

# We define the width and height of the game.
WIDTH, HEIGHT = 1000,600
WIN = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Stormtrooper VS Han Solo")

# We define the colors to have a clear code since it uses RGB.
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
YELLOW = (255, 255, 0)
BLUE = (0, 170, 255)

# We define the rectangle that acts as the border for the characters.
BORDER = pygame.Rect(WIDTH//2 - 5, 0, 10, HEIGHT)

# We add the sound variables
BULLET_HIT_SOUND = pygame.mixer.Sound(os.path.join('Img', 'Grenade+1.mp3'))
BULLET_FIRE_SOUND = pygame.mixer.Sound(os.path.join('Img', 'Gun+Silencer.mp3'))
VICTORY_SOUND = pygame.mixer.Sound(os.path.join('Img', 'victory.mp3'))


# We define the font used to show the health.
HEALTH_FONT = pygame.font.SysFont('Fixedsys', 40)
# We define the font used to show the winner.
WINNER_FONT = pygame.font.SysFont('Fixedsys', 100)

# We define this in order for the game to not depend on how fast our system can run it. We define how often we want the game to update.
FPS = 60
# We define the velocity they are moving when they press keys.
VEL = 5
# We define the velocity of the bullets.
BULLET_VEL = 6
# We define the max bullets each player can use.
MAX_BULLETS = 10
SOLDIER_WIDTH, SOLDIER_HEIGHT = 90, 140
SOLO_WIDTH, SOLO_HEIGHT = 150, 120

# We create the event of getting hit by the bullet.
SOLDIER_HIT = pygame.USEREVENT + 1
SOLO_HIT = pygame.USEREVENT + 2

# Import the images for the characters.
SOLDIER_IMAGE = pygame.image.load(os.path.join('Img', 'soldier.png'))
SOLDIER = pygame.transform.scale(SOLDIER_IMAGE, (SOLDIER_WIDTH, SOLDIER_HEIGHT))

SOLO_IMAGE = pygame.image.load(os.path.join('Img', 'Han-Solo.png'))
SOLO = pygame.transform.scale(SOLO_IMAGE, (SOLO_WIDTH, SOLO_HEIGHT))

# We generate the backround because we checked white and the yellow bullets were hard to see.
SPACE = pygame.transform.scale(pygame.image.load(os.path.join('Img', 'star_wars.png')), (WIDTH, HEIGHT))

def draw_window(solo, soldier, solo_bullets, soldier_bullets, solo_health, soldier_health):
    WIN.blit(SPACE, (0, 0)) # Fill the background.
    pygame.draw.rect(WIN, WHITE, BORDER)
    
    # We define the text and position of the health.
    solo_health_text = HEALTH_FONT.render("Han Solo: " + str(solo_health), 1, WHITE, BLACK)
    soldier_health_text = HEALTH_FONT.render("Stormtrooper: " + str(soldier_health), 1, WHITE, BLACK)
    WIN.blit(solo_health_text, (WIDTH - solo_health_text.get_width() - 10, 10))
    WIN.blit(soldier_health_text, (10, 10))
    
    WIN.blit(SOLDIER, (soldier.x, soldier.y)) 
    WIN.blit(SOLO, (solo.x, solo.y))
    
    # We define the rectangle that represents the bullet and color for each character.
    for bullet in soldier_bullets:
        pygame.draw.rect(WIN, BLUE, bullet)
    for bullet in solo_bullets:
        pygame.draw.rect(WIN, RED, bullet)
    
    pygame.display.update() # We always need to update pygame to display our changes.

# We create a function to not repeat it every time.
def soldier_handle_movement(keys_pressed, soldier):
    if keys_pressed[pygame.K_a] and soldier.x - VEL > 0:    # LEFT
        soldier.x -= VEL
    if keys_pressed[pygame.K_d] and soldier.x + VEL  + soldier.width < BORDER.x:    # RIGHT
        soldier.x += VEL
    if keys_pressed[pygame.K_w] and soldier.y - VEL > 0:    # UP    # We subtract when going up because in pygame the top left corner is (0,0)
        soldier.y -= VEL
    if keys_pressed[pygame.K_s] and soldier.y + VEL + soldier.height < HEIGHT - 15:    # DOWN # We make sure we don't allow it to go of the border with (-15).
        soldier.y += VEL
# We do the same with the other character.
def solo_handle_movement(keys_pressed, solo):
    if keys_pressed[pygame.K_LEFT] and solo.x - VEL > BORDER.x + BORDER.width:    # LEFT
        solo.x -= VEL
    if keys_pressed[pygame.K_RIGHT] and solo.x + VEL  + solo.width < WIDTH:    # RIGHT
        solo.x += VEL
    if keys_pressed[pygame.K_UP] and solo.y - VEL > 0:    # UP    
        solo.y -= VEL
    if keys_pressed[pygame.K_DOWN] and solo.y + VEL + solo.height < HEIGHT - 15:    # DOWN
        solo.y += VEL

# We define the function for the bullets movement.
def handle_bullets(soldier_bullets, solo_bullets, soldier, solo):
    for bullet in soldier_bullets:
        bullet.x += BULLET_VEL
        if solo.colliderect(bullet):
            pygame.event.post(pygame.event.Event(SOLO_HIT))
            soldier_bullets.remove(bullet)
        elif bullet.x > WIDTH:
            soldier_bullets.remove(bullet)

    for bullet in solo_bullets:
        bullet.x -= BULLET_VEL
        if soldier.colliderect(bullet):
            pygame.event.post(pygame.event.Event(SOLDIER_HIT))
            solo_bullets.remove(bullet)
        elif bullet.x < 0:
            solo_bullets.remove(bullet)
# We define the function to show the winner and restart the game.
def draw_winner(text):
    draw_text = WINNER_FONT.render(text, 1, RED, BLACK)
    WIN.blit(draw_text, (WIDTH/2 - draw_text.get_width()/2, HEIGHT/2 - draw_text.get_height()/2))
    
    pygame.display.update()
    pygame.time.delay(4000)
    
# Our main function for the game.
def main():
    solo = pygame.Rect(700, 300, SOLO_WIDTH, SOLO_HEIGHT) # we define the spaceships position
    soldier = pygame.Rect(100, 300, SOLDIER_WIDTH, SOLDIER_HEIGHT)
    
    solo_bullets = []
    soldier_bullets = []
    
    # We define the health of players.
    solo_health = 10
    soldier_health = 10
    
    clock = pygame.time.Clock()    
    run = True
    while run:
        clock.tick(FPS) # Ensures our game runs maximum at 60 FPS(defined at the begining)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_CAPSLOCK and len(soldier_bullets) < MAX_BULLETS: # We add the condition to not shoot bulllets if its over the limit we defined.
                    bullet = pygame.Rect(soldier.x + soldier.width, soldier.y + soldier.height//2 - 2, 10, 5)   # We define where the bullets come from which is at the edge of the character and the middle.
                    soldier_bullets.append(bullet)
                    BULLET_FIRE_SOUND.play()
                                                        
                if event.key == pygame.K_SPACE and len(solo_bullets) < MAX_BULLETS:
                    bullet = pygame.Rect(solo.x, solo.y + solo.height//2 - 2, 10, 5)   
                    solo_bullets.append(bullet)
                    BULLET_FIRE_SOUND.play()
            
            if event.type == SOLO_HIT:
                solo_health -= 1
                BULLET_HIT_SOUND.play()
                
            if event.type == SOLDIER_HIT:
                soldier_health -= 1
                BULLET_HIT_SOUND.play()     
        
        # We define the text depending on the character that wins.
        winner_text = ""
        if solo_health <= 0:
            winner_text = "Stormtrooper Wins!"
        
        if soldier_health <= 0:
            winner_text = "Han Solo Wins!"
        
        if winner_text != "":
            pygame.mixer.music.stop() # We stop the theme music.
            draw_winner(winner_text)
            VICTORY_SOUND.play()  # Reproduce the sound of victory.
            pygame.time.delay(4000)  # We add delay so it gives it time to sound and restart.
            VICTORY_SOUND.stop() 
            break
                
            
        keys_pressed = pygame.key.get_pressed() # to know the keys are currently being pressed.
        soldier_handle_movement(keys_pressed, soldier)
        solo_handle_movement(keys_pressed, solo)
        
        handle_bullets(soldier_bullets, solo_bullets, soldier, solo)
        
        
        draw_window(solo, soldier, solo_bullets, soldier_bullets, solo_health, soldier_health)
        
main()

# We define this in order for the game to run when we execute this file.    
if __name__ == "__main__":
    main()
    