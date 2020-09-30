"""A simple Shooting game using pygame libraries"""

#in-built modules

#3rd party modules  
import pygame
#local modules
from game_objects import screen_size, SKY_BLUE, BackgroundEffects, Targets, Projectiles

pygame.init()




def get_background():
    """Creating background picture
    
    Returns:
    -------
    background: pygame.Surface object
    """
    
    background = pygame.Surface(screen_size)
    background.fill(SKY_BLUE)
    #green strip
    background.fill((65, 242, 34), pygame.Rect((0, 640), (screen_size[0], screen_size[1] - 640)))
    #brown soil
    # background.fill((184, 95, 7), pygame.Rect((0, 650), (screen_size[0], 150)))        
    #Drawing Mountains and Sun
    pygame.draw.polygon(background, (150, 150, 150), [(100, 640), (300, 200), (500, 640)])
    pygame.draw.polygon(background, (128, 128, 128), [(400, 640), (550, 175), (700, 640)]) 
    pygame.draw.circle(background, (248, 255, 48), (10,10), (50)) 
    return background

def game_over(screen, background, bge_group):
    """ this method should be called at the end of a session."""
    
    sound = pygame.mixer.Sound("sounds\oh_no.ogg")
    sound.play()
    # bge_group.cannon.kill()
    for i in range(22):
        # stamp = pygame.Surface(screen_size)
        bge_group.score_board.scale(4*i+1)
        bge_group.clear(screen, background)
        bge_group.draw(screen)
        pygame.display.update()
        pygame.time.delay(250)
        

screen = pygame.display.set_mode(screen_size)
pygame.display.set_caption("cannon shooter")

background = get_background()
screen.blit(background, (0,0))
#clouds,etc
scenary = BackgroundEffects()
# mosquitoes
enemies = Targets()
#bullets from cannon
bullets = Projectiles()

try:
    with open("records.txt", 'r+') as f:
        high_score = list(f)[1].strip("\n")     #Read highscore from file.
except FileNotFoundError:
    with open("records.txt", 'w+') as f:
        f.write('high_score:\n0')
        high_score = "0"
    print("Creating record file")

done = False
charge = 0
score = 0
flag = False

while not done:
    #this is input processing part of game loop.
    if flag == True:        #flag stores True if specific keys are pressed and held.
        charge += 5 
        # print(charge)
        charge = charge%100
    for s in enemies.sprites():
        if s.rect[0] < 0:
            done = True
            game_over(screen, background, scenary)
            enemies.empty()

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            done = True
        elif event.type == pygame.KEYDOWN:
            if event.key in [pygame.K_SPACE, pygame.K_KP_ENTER]:
                # print("space bar is pressed")
                flag = True
        elif event.type == pygame.KEYUP:
            if event.key in [pygame.K_SPACE, pygame.K_KP_ENTER]:
                bullets.add_ammo(1, charge)
                flag = False
                charge = 0
    #This updates game
    if int(high_score) < score:
        high_score = str(score)
        
    scenary.update(cannon_charge_level = charge, high_score = high_score, score = score)
    bullets.update()
    score += enemies.update(bullets)

    #Rendering part of the loop
    enemies.clear(screen, background)
    bullets.clear(screen, background)
    scenary.clear(screen, background)
    scenary.draw(screen)
    enemies.draw(screen)
    bullets.draw(screen)
    pygame.display.update() 
    #This tracks fps
    pygame.time.delay(40)
    

with open("records.txt", 'r+') as f:
    f.seek(13)
    f.write(high_score)

pygame.quit()