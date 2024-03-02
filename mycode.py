import pygame as pg
import numpy as np
import sys 
import random 
import math as m 
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
BLUE = (0, 100, 255)
BABY_BLUE = (137, 207, 240)
GREEN = (50, 150, 50)
PURPLE = (130, 0, 130)
GREY = (230, 230, 230)
HORRIBLE_YELLOW = (190, 175, 50)
RED = (255,0,0)
BACKGROUND = WHITE

class population(pg.sprite.Sprite):
    def __init__(
            self,
            x,
            y,
            width,
            height,
            color,
            student, 
            age,
            size = 5,
            velocity = [0,0],
            random_vel = False,
            u_width = 80, 
            u_heigth = 80 ,
            random_move = False, 
            
    ):
        super().__init__ () #Calls init method of sprite.Sprite
        self.image = pg.Surface([size*2,size*2])
        
        pg.draw.circle(self.image, color, (size,size), size)
        
        self.rect = self.image.get_rect()
        self.pos = np.array([x,y], dtype = np.float64)
        self.vel = np.asarray(velocity, dtype = np.float64)


        self.WIDTH = width
        self.HEIGTH = height
        self.UNI_W = u_width
        self.UNI_H = u_heigth
        self.recovered = False
        self.checker = False
        self.random_move = random_move
        self.student = student
        self.age = age
        self.university = []
        self.target_x = ((self.WIDTH - self.UNI_W) // 2) + self.UNI_W* 0.5
        self.target_y = ((self.WIDTH - self.UNI_W) // 2) + self.UNI_H* 0.5
        self.university = [(self.WIDTH - self.UNI_W) // 2,  (self.WIDTH - self.UNI_W) // 2 + self.UNI_W,  (self.WIDTH - self.UNI_W) // 2,  (self.WIDTH - self.UNI_W) // 2 + self.UNI_H]
        self.arrived = False 

    def update(self):
        
        if self.student == False: 
            self.pos += self.vel
            x,y = self.pos
            #get more normalized velocity
            
            #vel_magnitude = np.linalg.norm(self.vel)

            #common_vel = 4
            #if vel_magnitude > 4:
                #self.vel /= vel_magnitude
            
            if self.random_move:
                self.vel += np.random.rand(2) * 1- 0.5

            #boundaries conditions. Remeber we are simulating a space with a university in the center. Initialy, dots must not be inside university 
            #external boundaries
            if x < 0:
                self.pos[0] = self.WIDTH
                x = self.WIDTH
            if x > self.WIDTH:
                self.pos[0] = 0
                x = 0
            if y < 0:
                self.pos[1] = self.HEIGTH
                y = self.HEIGTH
            if y > self.HEIGTH:
                self.pos[1] = 0
                y = 0

            #internal boundaries (University)

            if self.university[0]-50<x<self.university[1]+50  and  -50 + self.university[2]<y<self.university[3]+50:
                self.pos[0] =np.random.choice([0,self.WIDTH])
                x = np.random.choice([0,self.WIDTH])
                self.pos[1] =np.random.choice([0,self.HEIGTH])
                y = np.random.choice([0,self.HEIGTH])

        else: 
            self.pos += self.vel
            x,y = self.pos
            #get more normalized velocity
            
            #vel_magnitude = np.linalg.norm(self.vel)

            #common_vel = 4
            #if vel_magnitude > 4:
                #self.vel /= vel_magnitude
            if self.random_move:
                self.vel += np.random.rand(2) * 1- 0.5
            '''
            if m.sqrt((x-self.target_x)**2 + (y-self.target_y)**2) > 0.1 and self.arrived == False:
                dir_x = self.target_x-x
                dir_y = self.target_y-y
                #normalize direction
                magnitude = m.sqrt(dir_x**2 + dir_y**2)
                dir_x_norm = dir_x/magnitude
                dir_y_norm = dir_y/magnitude
                #direction
                self.vel *= dir_x_norm, dir_y_norm
            if  m.sqrt((x-self.target_x)**2 + (y-self.target_y)**2) < 0.1:
                self.arrived = True
                self.vel *= -1
            '''
            #boundaries conditions. Remeber we are simulating a space with a university in the center. Initialy, dots must not be inside university 
            #external boundaries
            if x < 0:
                self.pos[0] = self.WIDTH
                x = self.WIDTH
                self.arrived = False 
            if x > self.WIDTH:
                self.pos[0] = 0
                x = 0
                self.arrived = False
            if y < 0:
                self.pos[1] = self.HEIGTH
                y = self.HEIGTH
                self.arrived = False
            if y > self.HEIGTH:
                self.pos[1] = 0
                y = 0
                self.arrived = False 

        # rectangle sufarce position update
        self.rect.x = x
        self.rect.y = y 
            

        if self.checker:
            self.recovery_period -= 1
            if self.recovery_period <=0:
                self.checker = False
                chance = np.random.rand()
                if 25<=self.age<=50:
                    if self.mortality_rate[0] > chance:
                        self.kill() #remove the human from infected and susceptibles containers. 
                    else:
                        self.recovered = True
                elif 51<=self.age<=80:
                    if self.mortality_rate[1] > chance:
                        self.kill() #remove the human from infected and susceptibles containers. 
                    else:
                        self.recovered = True
                elif 10<=self.age<=24:
                    if self.mortality_rate[2] > chance:
                        self.kill() #remove the human from infected and susceptibles containers. 
                    else:
                        self.recovered = True


    def new_status(self, color, vel, size = 5):
        return population(
            self.rect.x,
            self.rect.y,
            self.WIDTH,
            self.HEIGTH,
            color,
            student = self.student,
            age = self.age,
            velocity= vel

        )
    def recovered_or_not(self, recovery_period = 100, mortality_rate = [0.1 , 0.2 , 0.35]):
        self.checker = True
        self.recovery_period = recovery_period 
        self.mortality_rate = mortality_rate #mortality_rate will depend on the age of the person. 
        

class running_model:
    
    def __init__(
            self,
            width = 800,
            heigth = 800,
            u_width = 20,
            u_heigth = 20
    ):
        
        self.WIDTH = width
        self.HEIGTH = heigth
        self.U_WIDTH = u_width
        self.U_HEIGTH = u_heigth
        self.COORD = (self.WIDTH - self.U_WIDTH) // 2
        self.susceptibles_container = pg.sprite.Group()
        self.infected_container = pg.sprite.Group()
        self.recovered_container = pg.sprite.Group()
        self.population__container = pg.sprite.Group() #susceptibles + infected + recovered - dead 
               
        self.susceptible = 100
        self.susceptible_student = 0.1 * self.susceptible
        self.infected = 1
        self.N = self.susceptible + self.infected #will be used to plot dead people. 
        self.Time = 3000
        self.recovery_period = 460
        self.mortality_rate = [0.1,0.2,0.35]
        self.std_cnt = 0
        
    def start(self, random_move =False):

        pg.init()
        screen = pg.display.set_mode([self.WIDTH,self.HEIGTH])
        
        def point_gen():
            university = [self.COORD-50,self.COORD+self.U_WIDTH+50, self.COORD-50, self.COORD + self.U_HEIGTH+50]
            while True:
                x = random.uniform(0, self.WIDTH+1)
                y = random.uniform(0, self.WIDTH+1)
            # Verificar si el punto está dentro de la zona de exclusión
                if not (university[0] < x < university[1] and university[2] < y < university[3]):
                    return x, y
        def age_distribuiton_gen():
            adults = np.random.normal(loc = 35,scale= 10, size= int(0.6 * self.susceptible))
            seniors = np.random.normal(loc= 65,scale= 15, size = int(0.2 * self.susceptible))
            teenagers = np.random.normal(loc= 18,scale= 6,size =int(0.2 * self.susceptible))
            all_ages = np.concatenate((adults, seniors, teenagers))
            all_ages_int = np.round(all_ages).astype(int)
            np.random.shuffle(all_ages_int)
            return all_ages_int
    
    
        for i in range(self.susceptible):
            x, y = point_gen()
            vel = np.random.rand(2) * 1-0.5 # generates random velocity vector with components between -1 and 1.
            std = np.random.choice([True,False]) 
            age = age_distribuiton_gen()[i]
            print(age)
            if std == True and self.std_cnt <= self.susceptible_student:
                self.std_cnt += 1
                human = population(x,y,self.WIDTH, self.HEIGTH, color = BABY_BLUE, velocity= vel, random_move = random_move, student= True, age = age)
            else:
                human = population(x,y,self.WIDTH, self.HEIGTH, color = BLUE, velocity= vel, random_move = random_move, student= False, age = age)
            self.susceptibles_container.add(human)
            self.population__container.add(human)
        
        for i in range(self.infected):
            x = np.random.randint(0,self.WIDTH+1)
            y = np.random.randint(0, self.HEIGTH + 1)
            vel = np.random.rand(2) * 1 - 0.5 # generates random velocity vector with components between -1 and 1. 
            human = population(x,y,self.WIDTH, self.HEIGTH, color = RED, velocity= vel, random_move= random_move, student=False, age = 25)
            self.infected_container.add(human)
            self.population__container.add(human)
        
        stats = pg.Surface((self.WIDTH // 2, self.HEIGTH // 8))
        stats.fill(GREY)
        stats.set_alpha(350) #aumenta la transparencia del fondo de la grafica 
        stats_pos = (0, 40)

        cnt = True
        clock = pg.time.Clock()

        #for i in range(self.Time):
        for i in range(self.Time):
            for event in pg.event.get():
                if event.type == pg.QUIT:
                    sys.exit()
            self.population__container.update()
            screen.fill(BACKGROUND)
        #plot
            stats_height = stats.get_height()
            stats_width = stats.get_width()
            n_inf_now = len(self.infected_container)
            n_pop_now = len(self.population__container) #si las personas mueren, este valor reduce por lo tanto se grafica como las personas muertas
            n_rec_now = len(self.recovered_container)
            if i % 66 ==0:
                t = int((i / self.Time) * stats_width) 
            #t = int((self.Time/30)) 
            y_infect = int(stats_height - (n_inf_now / n_pop_now) * stats_height) #si esa proporcion da 1 quiere decir que estamos en el pico 
                                                                                 #de infeccion lo cual significa una barra muy grande. Como la y disminuye hacia abajo en este UCS, y=0 representa el pico de contagios
            y_dead = int(((self.N - n_pop_now) / self.N) * stats_height) #si esa resta da 0 es porque todos murieron y por lo tanto la barra
                                                                        #tiene que llegar hasta abajo, es decir, el 0 de y. 
            y_recovered = int((n_rec_now / n_pop_now) * stats_height)
            stats_graph = pg.PixelArray(stats)
            stats_graph[t, y_infect:] = pg.Color(*GREEN)
            stats_graph[t, :y_dead] = pg.Color(*HORRIBLE_YELLOW)
            stats_graph[t, y_dead : y_dead + y_recovered] = pg.Color(*PURPLE)
            font = pg.font.SysFont(None,36)
            text_infected = font.render(f'Infected people : {n_inf_now}', True, GREEN)
            text_recovered = font.render(f'Recovered people: {n_rec_now}', True, PURPLE)
            text_deseased =font.render(f'Deseased people: {self.N-n_pop_now}', True, HORRIBLE_YELLOW)
        #collition detection
            inf_colli_susc = pg.sprite.groupcollide(self.susceptibles_container, self.infected_container, True,False) #True value is for deleting of susceptibles humans who collided with infecteds. False value is to not
        #delete infecteds who collided with susceptibles.        
            for i in inf_colli_susc:
                new_status = i.new_status(RED, vel= i.vel)
                clock.tick(30)
                new_status = i.new_status(RED,vel = [0,0])
                new_status.recovered_or_not(self.recovery_period, self.mortality_rate) #activate the recovered_or_not method to start counting recovery time for those who are infected
                self.infected_container.add(new_status)
                self.population__container.add(new_status)
        #Those who were infected are recovered? 
            recovered = []
            for i in self.infected_container:
                if i.recovered:
                    new_status = i.new_status(GREEN,vel =  i.vel)
                    self.recovered_container.add(new_status)
                    self.population__container.add(new_status)
                    recovered.append(i)
            if len(recovered) > 0:
                self.infected_container.remove(*recovered)
                self.population__container.remove(*recovered) #to avoid keep counting those infected people who are now recovered. 
            
            self.population__container.draw(screen)
            pg.draw.rect(screen,RED, (self.COORD,self.COORD,self.U_WIDTH,self.U_HEIGTH))
            del stats_graph
            stats.unlock()
            screen.blit(stats, stats_pos)
            screen.blit(text_infected, (10,10))
            screen.blit(text_recovered, (300,10))
            screen.blit(text_deseased, (600,10))
            pg.display.flip()

            clock.tick(30) #30 cycles rest

if __name__ == '__main__':
    desease = running_model(1000,1000)
    desease.start(random_move = True)






