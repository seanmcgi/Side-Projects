#Run this file

import pygame
import random
import sys
import playinggame as pg

pg.reset()

samples = 70

NN = []

prop = []

flag = []

control = []

    
for j in range(0,samples-1):
    NN.append(j)
    prop.append(j)
    flag.append(True)
    control.append(False)
control[-1] = True #1st on list is control



h = 200

w = 60

speed = 3

a = .05

x = 600

y = 500 

r = 25

jumpspeed = -150

class rectangle:
    def __init__(self,y1,y2,s):
        self.bottom_rect_h = y1
        self.top_rect_h = y2
        self.start_frame = s
        
    def setframe(self,s):
        self.start_frame = s
        
    def setheight(self,h1,h2):
        self.bottom_rect_h = h1
        self.top_rect_h = h2
        
    def getframe(self,s):
        return(x-3*(s-self.start_frame)) 
    
    def drawrect(self,s):
        pygame.draw.rect(display,(0,0,255),(x-speed*(s-self.start_frame),y-self.top_rect_h,w,self.top_rect_h),0)
        pygame.draw.rect(display,(0,255,0),(x-speed*(s-self.start_frame),0,w,self.bottom_rect_h),0)
    
    def get_hitbox(self,s):
        #xr,xl,yt,yb
        return([x-speed*(s-self.start_frame),x-speed*(s-self.start_frame)+w,y-self.top_rect_h,self.bottom_rect_h])
        

class player:
    def __init__(self,cont):
        self.frame = 0
        self.vel = 0
        self.accel = a
        self.yp = y/2
        if cont is False:
            self.color = [255,0,0]
        else:
            self.color = [0,255,0]
    
    def drawplayer(self,s):
        pygame.draw.circle(display,(self.color),(int(x/2),self.gety(s)),r)
        
    def gety(self,s):
        t = s-self.frame
        height = (self.accel*t*t+self.vel*t/20+self.yp)
        self.vel = self.vel +2*self.accel*t
        return int(height)
    
    def jump(self,s):
        self.yp = self.gety(s)
        self.frame = s
        self.vel = jumpspeed
    
    def get_hitbox(self,s):
        return [x/2,self.gety(s),r]
    
    def get_vel(self,s):
        return self.vel
        

def hitbox(play,rect1,rect2,s):
    p_hit = play.get_hitbox(s)
    rect1hit = rect1.get_hitbox(s)
    rect2hit = rect2.get_hitbox(s)
    if p_hit[1]>y-r or p_hit[1] < r:
        return True
    if p_hit[0]-p_hit[2] < rect1hit[1] and p_hit[0]+p_hit[2] > rect1hit[0]:
        return compare(p_hit,rect1hit)
    if p_hit[0]-p_hit[2] < rect2hit[1] and p_hit[0]+p_hit[2] > rect2hit[0]:
        return compare(p_hit,rect2hit)
    else:
        return False
#xr,xl,yt,yb
def compare(play,p):
    if play[0]-play[2]<p[1] and play[0]+play[2] > p[0]: 
        if play[1]+play[2]<p[2] and play[1]-play[2]>p[3]:
            return False
        else:
            return True
    return False

def randomheight():
    return random.randint(r,y-r-h)
    
random.seed()

pygame.init()

clock = pygame.time.Clock()

display = pygame.display.set_mode([x,y])

def game(gens):
    
    gens +=1
    print('Generation = ',gens)
    
    for j in range(0,samples-1):
        NN[j] = pg.NeuralNetwork(control[j],gens)
        prop[j] = player(control[j])
        flag[j] = True

    score = 0
    
    a = randomheight()    
    rect2 = rectangle(a,y-h-a,(x+w)/2/speed)
    rect1 = rectangle((y-h)/2,(y-h)/2,0)

    
    running = True
    i = 0
    
    
    while running:
        
        
        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_q:
                    pygame.quit()
                    sys.exit()
        display.fill([255,255,255])
        
        rect1frame = rect1.getframe(i)
        rect2frame = rect2.getframe(i)
        if rect1frame == x/2 or rect2frame == x/2:
            score += 1
        
        if rect1frame < -w:
            rect1.setframe(i)
            a = randomheight()
            rect1.setheight(a,y-h-a)
        if rect2frame < -w:
            rect2.setframe(i)
            a = randomheight()
            rect2.setheight(a,y-h-a)

        for j in range(0,samples-1):
            if flag[j]:
                
                #jump
                if pg.jump(prop[j].get_hitbox(i),rect1.get_hitbox(i),rect2.get_hitbox(i),prop[j].get_vel(i),i,y,NN[j]):
                    prop[j].jump(i)
        
                if hitbox(prop[j],rect1,rect2,i):
                    flag[j] = False
                    print (score,i)
                    if all(k == False for k in flag):
                        if j != samples-1:
                            pg.end(i,NN[j])
                        game(gens)

        
                prop[j].drawplayer(i)
        
            if all(k == False for k in flag):
                game(gens)
        
        
        rect1.drawrect(i)
        rect2.drawrect(i)
        
        pygame.display.flip()

            
        i = (1+i)
        mselapsed = clock.tick(60)

game(0)
