"""A module to hold all useful fns, sprite classes and group classes for cannon shooter game"""

import random
from math import sin, cos, tan, pi
#3rd party modules  
import pygame
#local modules
# from MyPyGames import my_graphics

SKY_BLUE = (72, 203, 247)
G_ACCEL = 1.8 #acceleration due to gravity


pygame.init()       #just for caution

screen_size = (1280, 720)


#Abandoned idea
# class ExtraEffects(pygame.sprite.Group):            #   ee_g means extra effects group
    # """ contains small details like smokes, shadows etc."""
    
    # def __init__(self):
        # super().__init__()

# class Smoke(pygame.sprite.Sprite):
    # """ """
    
    # def __init__(self):
        # super().__init__()
        

class BackgroundEffects(pygame.sprite.Group):
    """Includes all those sprites, that doesn't need collision detection. Layer 0"""
    
    def __init__(self):
        super().__init__()
        Cloud(self, 5)
        Cloud(self, 3)
        self.cannon = Cannon(self)
        self.score_board = ScoreBoard(self)
        
    def update(self, **kwargs):
        """takes key word arguments in dict format
        
        Parameters
        ----------
        kwargs: dict 
            keys: cannon_charge_level, high_score, score
        """
        
        super().update(kwargs['cannon_charge_level'], kwargs['high_score'], kwargs['score'])
        if random.random() < 0.005:
            Cloud(self)

class Cloud(pygame.sprite.Sprite):
    """ """
    
    def __init__(self, bge_group, forward = 0):       #bge_group means background effects group 
        super().__init__(bge_group)
        self.y = int(180 - random.random()*170)
        self.image = pygame.image.load("images\cloud.bmp")
        self.image.set_colorkey(0x6bb0cf)
        self.rect = pygame.Rect((screen_size[0] - 15 - forward*self.image.get_size()[0], self.y),(self.image.get_size()))
       
    def update(self, *args):
        """Slowly drifts the cloud towards left side
        
        Parameters:
        -----------
        *args:  
            cannon_charge_level, high_score, score respectively
        """
        
        self.rect.move_ip(-1, 0)
        if self.rect.right < 8:
            # print('dead cloud')
            self.kill()

class Cannon(pygame.sprite.Sprite):
    def __init__(self, bge_group):
        super().__init__(bge_group)
        self.rect = pygame.Rect((50, 350), (175, 300))
        self.image = pygame.image.load("images\cannon.bmp")
        self.image.set_colorkey(SKY_BLUE)
        self.level = pygame.Surface((50, 100))
        self.level.fill((150, 150, 150))
        
    def update(self, *args):
        charge_level = args[0]
        pygame.draw.rect(self.level, [charge_level + 100, 100, 0], pygame.Rect((0, int(100 - charge_level)), (50, 5)))
        if charge_level == 0:
            self.level.fill((150, 150, 150))
        self.image.blit(self.level, (30, 130))
    

class ScoreBoard(pygame.sprite.Sprite):
    """ maintains and prints current score and high score"""
    
    def __init__(self, bge_group):
        super().__init__(bge_group)
        self.myfont = pygame.font.SysFont('cambria', 24)
        self.image = pygame.Surface((300, 80))
        self.image.set_colorkey(SKY_BLUE)
        self.rect = pygame.Rect((980, 20), (300, 80))
        self.message = ""
    
    def get_stamp(self, font_obj, message_str):
        lines = [font_obj.render(message_str[i], True, (180, 20, 20)) for i in range(2)]
        # h = font_obj.get_height()
        (w, h) = lines[0].get_size()
        w2 = lines[1].get_width()
        stamp = pygame.Surface((max(w, w2)+4, 2*h+4))
        stamp.fill(SKY_BLUE)
        stamp.set_colorkey(SKY_BLUE)
        stamp.blit(lines[0], (h+8, 0))
        stamp.blit(lines[1], (2, h))
        
        return stamp
    
    def update(self, *args):
        self.message = ["HIGH SCORE: " + args[1], "CURRENT SCORE: " + str(args[2])]
        self.image = self.get_stamp(self.myfont, self.message)
    
    def scale(self, i):       
        
        self.myfont = pygame.font.SysFont('cambria', 24+i)
        self.image = self.get_stamp(self.myfont, self.message)
        i_size = self.image.get_size()
        pygame.draw.rect(self.image, (250, 120, 20), pygame.Rect((2,2), [i -4 for i in i_size]), 2)
        self.rect.move_ip((-40, 10))
        self.rect.size = i_size


class Projectiles(pygame.sprite.Group):
    """ """
    
    def __init__(self):
        super().__init__(self)
        
    def add_ammo(self, x, charge_level):
        if x ==1:
            # print("adding black ball")
            CannonBall(charge_level, self)
            firing_sound = pygame.mixer.Sound("sounds\Boom.wav")
            firing_sound.play()


class CannonBall(pygame.sprite.Sprite):
    def __init__(self, charge_level, projectile_group):
        super().__init__(projectile_group)
        self.ball_size = (20, 20)
        self.init_pos = [163, 354]
        self.image = pygame.Surface(self.ball_size)
        self.image.fill(SKY_BLUE)
        self.image.set_colorkey(SKY_BLUE)
        pygame.draw.circle(self.image, (30, 30, 30), (10, 10), 8)
        self.mask = pygame.mask.from_surface(self.image)
        self.rect = pygame.Rect(self.init_pos, self.ball_size)
        self.vel = [9, -3]    
        self.vel = [int(i*charge_level*0.1) for i in self.vel]
        self.time = 0
    
    def path(self, time):
        # WIND_RESISTANCE = 0.0000000000000000001 #0 for no air-resistance and one means nothing will ever move 
        x = self.rect.left + self.vel[0]
        y = self.rect.top + self.vel[1]
        # self.vel[0] = self.vel[0] - WIND_RESISTANCE
        self.vel[1] += G_ACCEL*time
        trajectory = [int(x), int(y)]
        return trajectory
        
    def update(self):
        if self.rect.bottom < 630 and self.rect.right < screen_size[0]:
            self.time += 1
            self.rect = pygame.Rect(self.path(self.time), self.ball_size)
        else:
            self.kill()
    
    # def kill(self):
        # if self.rect.bottom < 630 and self.rect.right < screen_size[0]:     #This is a collision.
            # self.vel[0] = -0.1*self.vel[0]
            # self.vel[1] = 0.3
            # self.time = 0
        # else:
            # super().kill()                                            # This is out of bounds true death.
            
class Targets(pygame.sprite.Group):
    """
    simple group for cannon targets.
    """
    
    def __init__(self):       
        super().__init__()
        self.difficulty = 0.03 # determines how fast enemies pop up.
        self.mosquito_sound = pygame.mixer.Sound("sounds\mosquito.wav")
        self.mosquito_sound.set_volume(0)
        self.mosquito_sound.play(-1)
        
    def update(self, projectile_group):
        """ """
        
        
        if random.random() < self.difficulty:
            self.add(Mosquito())   
        crash = len(pygame.sprite.groupcollide(projectile_group, self, True, True, pygame.sprite.collide_mask))
        #remember to not add () to callback function name.
        v = len(self)
        if v > 10:
            v = 10
        self.mosquito_sound.set_volume(v*0.1)
        if self.difficulty < 1.0:
            self.difficulty += crash*0.001
            # print(self.difficulty)
        # print(v)
        super().update(self.difficulty)
        return crash
 
 
class Mosquito(pygame.sprite.Sprite):
    """
    class representing individual Mosquitos
    """
    
    def __init__(self):
        super().__init__()
        center_pos = [200*random.random() + 650, 200+ 230*random.random()]
        center_pos = [int(item) for item in center_pos]
        self.image = pygame.image.load("images\mosquito.bmp")
        self.image.set_colorkey(SKY_BLUE)   
        self.size = self.image.get_size()
        self.mask = pygame.mask.from_surface(self.image)
        available_area = [[250, screen_size[0] - self.size[0]], [120, 630 - self.size[1]]]
        available_radius = [abs(center_pos[i] - available_area[i][j]) for i in range(2) for j in range(2)]
        
        self.radius = int((min(available_radius))*(1 - 0.6*random.random()))
        # print(self.radius, "-----",available_radius)
        self.rect = pygame.Rect((center_pos[0] + self.radius, center_pos[1]), self.size)
        self.angle = 0
        self.rotat_speed = 0.7 - random.random()*0.6  #radians per frame
    
    # def shadow(self, background):
        # """ """
        # x = int(self.rect[0]*640/self.rect[1])
        # width = int(self.rect.width*640/self.rect[1])
        # pygame.draw.line(background, (66, 66, 66),(x, 640), (x + width, 640), 3)
    
    def update(self, difficulty):
        self.angle = (self.angle + self.rotat_speed)%(2*pi)
        instant_vel = [-sin(self.angle), -cos(self.angle)]   
        #since graphics has reversed y direction, there is a -ve before cos to get a counter clock wise rotation
        instant_vel = [int(self.radius*self.rotat_speed*i) for i in instant_vel]
        self.rect.move_ip(instant_vel)
        self.rect.move_ip((-(2 + int(difficulty*10)), 0))      #linear motion.
        # if self.rect.bottom > 640:
            # self.rect.move_ip((0, -8))
        # if random.random() < 0.4:
            # self.rect.move_ip((-4, 0))
        # elif random.random() < 0.01:
            # self.rect.move_ip(0, 1)
    
    def kill(self):
        splash = pygame.mixer.Sound("sounds\splash.wav")
        splash.set_volume(0.5)
        splash.play()
        # print("mosquito dead")
        super().kill()
