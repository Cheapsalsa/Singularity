from functions import *
import sys, os.path
import pygame
import pygame.gfxdraw
import random
import time
import pygame.mixer

# Initialize Project
if sys.platform in ["win32", "win64"]:
    os.environ["SDL_VIDEO_CENTERED"] = "1"
icon = pygame.image.load('singularity.png')
arrow = pygame.image.load('arrow.png')


class Player(object):
    def __init__(self, x, y, mass, num):
        self.mass = mass
        self.x = x
        self.y = y
        self.num = num
        self.acceleration = [0, 0]
        self.velocity = [0, 0]
        self.maxVelocity = 0.5
        self.friction = 0.98
        self.effects = []
        self.angle = 0
        self.show = True

        # Character Effects
        for i in range(10):
            self.create_effect()

        # Labeling
        if num == 1:
            self.name = font.render('P1', 1, (255, 255, 255))
        else:
            self.name = font.render('P2', 1, (255, 255, 255))

    def render(self, surface):
        if self.show:
            # Render Effects
            for i in range(len(self.effects)):
                self.effects[i].render(surface)

            # Render Player
            pygame.draw.circle(surface, (0, 0, 0), (int(self.x), int(self.y)), int(self.mass))
            pygame.draw.circle(surface, (222, 0, 0), (int(self.x), int(self.y)), int(self.mass), 1)

            # Render Label
            if game:
                surface.blit(self.name, (int(self.x - 8), int(self.y - 13)))

    def update(self):
        for i in range(len(projectiles)):
            px = projectiles[i].x
            py = projectiles[i].y
            pr = projectiles[i].mass
            if collidingCircles(self.x, self.y, self.mass, px, py, pr):
                if projectiles[i].velocity[0] > 0:
                    vx = 2
                else:
                    vx = -2
                if projectiles[i].velocity[1] > 0:
                    vy = 2
                else:
                    vy = 2
                self.set_force([(projectiles[i].velocity[0] + vx) * min(self.mass, 30) , (projectiles[i].velocity[1] + vy) * min(self.mass,30)])

        # Update position
        self.move()

        # Update Effects
        remove_list = []

        for i in range(len(self.effects)):
            self.effects[i].update()
            if self.effects[i].opacity <= 50:
                remove_list.append(self.effects[i])

        if len(remove_list) > 0:
            for i in range(len(remove_list)):
                self.effects.remove(remove_list[i])
                self.create_effect()

    def set_force(self, force):
        self.acceleration[0] = force[0] / min(self.mass,30)
        self.acceleration[1] = force[1] / min(self.mass,30)

        self.velocity[0] += min(self.acceleration[0], self.maxVelocity)
        self.velocity[1] += min(self.acceleration[1], self.maxVelocity)

    def move(self):
        self.velocity[0] *= self.friction
        self.velocity[1] *= self.friction

        self.velocity[0] += self.acceleration[0]
        self.velocity[1] += self.acceleration[1]

        self.x += self.velocity[0]
        self.y += self.velocity[1]

        if self.x + self.mass > screen_width:
            self.x = screen_width - self.mass
        if self.x - self.mass < 0:
            self.x = 0 + self.mass
        if self.y + self.mass > screen_height:
            self.y = screen_height - self.mass
        if self.y - self.mass < 0:
            self.y = 0 + self.mass

    def create_effect(self):
        self.effects.append(SingularityEffect(self.x, self.y, (222, 0, 0), random.randint(int(self.mass - int(self.mass / 4)), int(self.mass + int(self.mass / 5))), random.randint(90, 100), random.randint(1, 2)))

    def launch_projectile(self):
        shoot_s.play()
        angrad = math.radians(self.angle)
        self.mass -= self.mass / 2
        projectiles.append(Projectile(self.angle, int(self.mass / 1.5), self.x + (math.cos(angrad) * (self.mass * 6.2)), self.y - (math.sin(angrad) * (self.mass * 6.2))))

    def set_rotation(self, sin_value, cos_value):
        if cos_value != 0:
            if right_y_axis < 0:
                self.angle = math.degrees(math.atan(cos_value / sin_value)) - 270
            else:
                self.angle = math.degrees(math.atan(cos_value / sin_value)) - 90

    def pop(self):
        angle = 0
        for i in range(24):
            angle = (angle + 15) % 360
            burst_particles.append(BurstParticle(self.x, self.y, angle))

    def death_pop(self):
        score_s.play()
        flash.append(FlashEffect())
        angle = 0
        for i in range(120):
            angle = (angle + 3) % 360
            burst_particles.append(DeathParticle(self.x + (math.cos(math.radians(angle)) * (self.mass * 2)), self.y - (math.sin(math.radians(angle) * (self.mass * 2))), angle))
 

class Projectile(object):

    def __init__(self, rot, mass, x, y):
        self.mass = mass
        self.x = x
        self.y = y
        self.heading = rot
        self.angle = 0
        self.velocity = [0, 0]
        self.multi = 2
        self.speed = 5 * (1 + (70 - self.mass * 2) / 70)
        if self.speed > 5:
            self.speed = 5
        self.rot = random.uniform(-1, 1)
        self.rot -= 1 - (self.mass / 200)
        points = random.randint(5, 8)
        self.color = (255, 255, 255)
        self.real_points = []
        self._points = []
        for i in range(points):
            angle = (i * 2 * math.pi) / points
            point = []
            point.append(math.cos(angle))
            point.append(math.sin(angle))
            self._points.append(point)

        self.get_points()

    def update(self):
        self.move()
        if self.speed < 1:
            rot2 = self.rot * self.speed
        else:
            rot2 = self.rot
        self.angle = (self.angle + rot2) % 360
        self.get_points()

    def get_points(self):
        self.real_points = []
        angle_rad = math.radians(self.angle)
        for x, y in self._points:
            rotated = self.rotate([self.mass * self.multi * x, self.mass * self.multi * y], angle_rad)
            self.real_points.append([(rotated[0] + self.x),
                                     (rotated[1] + self.y)])

    def rotate(self, point, angle_rad):
        return [math.cos(angle_rad) * point[0] - math.sin(angle_rad) * point[1],
                math.sin(angle_rad) * point[0] + math.cos(angle_rad) * point[1]]

    def move(self):
        self.velocity[0] = self.speed * math.cos(math.radians(self.heading))
        self.velocity[1] = -1 * self.speed * math.sin(math.radians(self.heading))
        self.speed *= 0.996
        self.x += self.velocity[0]
        self.y += self.velocity[1]

    def is_out_screen(self):
        if self.x > screen_width or self.x < 0 or self.y > screen_height or self.y < 0:
            return True
        return False

    def pop(self):
        explosion_s.play()
        angle = 0
        m = 1.30 - ((25.0 - self.mass) / 25.0)
        for i in range(random.randint(int(10 * m) + 2, int(30 * m))):
            angle = (angle + 36) % 360
            burst_particles.append(BurstParticle(self.x, self.y, angle))

    def render(self, surface):
        pygame.draw.aalines(surface, self.color, True, self.real_points)


class World(object):
    def __init__(self, width, height):
        self.width = width
        self.height = height
        self.particles = []

    def render(self, surface):
        # Render Grid Lines
        for c2 in range(0, self.width, int(self.width/50)):
            pygame.draw.line(surface, (11, 11, 11), (c2, 0), (c2, self.height), 1)
        for r2 in range(0, self.height, int(self.height/30)):
            pygame.draw.line(surface, (11, 11, 11), (0, r2), (self.width, r2), 1)
        for c1 in range(0, self.width, int(self.width/25)):
            pygame.draw.line(surface, (23, 23, 23), (c1, 0), (c1, self.height), 1)
        for r1 in range(0, self.height, int(self.height/15)):
            pygame.draw.line(surface, (23, 23, 23), (0, r1), (self.width, r1), 1)

        # Render Particles
        for i in range(len(self.particles)):
            self.particles[i].render(surface)

    def update(self, inn):
        # Update Effects
        remove_list = []

        for i in range(len(self.particles)):
            self.particles[i].update(inn)
            p = self.particles[i]
            if collidingCircles(p.x, p.y, p.radius, singularities[0].x, singularities[0].y, 105):
                remove_list.append(self.particles[i])

        if len(remove_list) > 0:
            for i in range(len(remove_list)):
                self.particles.remove(remove_list[i])

    def spawn_particle(self):
        # Create World Particles
        gen_x = random.randint(-300, screen_width + 300)
        gen_y = random.randint(-300, screen_height + 300)
        a = random.randint(100, 225)
        self.particles.append(SingularityParticle(gen_x, gen_y, random.randint(1, 3), (a, a, a)))


class Singularity(object):
    def __init__(self,mass, x, y, canSuck, life_time):
        self.mass = mass
        self.x = x
        self.y = y
        self.effects = []
        self.canSuck = canSuck
        self.life_time = life_time


        # Create Effects
        for i in range(10):
            self.create_effect()

    def render(self, surface):
        # Render Effects
        for i in range(len(self.effects)):
            self.effects[i].render(surface)

        # Render Singularity
        if self.canSuck:
            c = (255, 255, 255)
        else:
            c = (155, 0, 0)
        pygame.draw.circle(surface, (0, 0, 0), (int(self.x), int(self.y)), int(self.mass))
        pygame.draw.circle(surface, c, (int(self.x), int(self.y)), int(self.mass), 1)

    def update(self):
        # Update Effects
        remove_list = []

        for i in range(len(self.effects)):
            self.effects[i].update()
            if self.effects[i].opacity <= 10:
                remove_list.append(self.effects[i])

        if len(remove_list) > 0:
            for i in range(len(remove_list)):
                self.effects.remove(remove_list[i])
                self.create_effect()

    def create_effect(self):
        if self.canSuck:
            c = (255, 255, 255)
        else:
            c = (155, 0, 0)
        self.effects.append(
            SingularityEffect(self.x, self.y, c, random.randint(int(self.mass) - int(round(self.mass/10)), int(self.mass) + int(round(self.mass/10))), random.randint(85, 95),random.randint(1, 2)))

    def pop(self):
        angle = 0
        m = 1.30 - ((25.0 - self.mass) / 25.0)
        for i in range(random.randint(int(10 * m) + 2, int(30 * m))):
            angle = (angle + 36) % 360
            burst_particles.append(BurstParticle(self.x, self.y, angle))


class SingularityEffect(object):
    def __init__(self, x, y, color, radius, opacity, type):
        self.x = x
        self.y = y
        self.color = color
        self.radius = radius
        self.opacity = opacity
        self.type = type

    def render(self, surface):
        # Render Effect (filled or line)
        pygame.gfxdraw.circle(surface, int(self.x), int(self.y), self.radius, (self.color[0], self.color[1], self.color[2], self.opacity))

    def update(self):
        # Update Position
        self.x += random.uniform(-1, 1) * random.randint(int(self.radius / 13), int(self.radius / 12))
        self.y += random.uniform(-1, 1) * random.randint(int(self.radius / 13), int(self.radius / 12))

        # Update Opacity
        self.opacity -= random.randint(2, 6)


class DeathParticle(object):
    def __init__(self, x, y, angle):
        self.x = x
        self.y = y
        self.heading = angle
        self.speed = 12 + random.randint(-4, 4)
        self.velocity = [0, 0]
        self.suck = False
        self.x_step = 0
        self.y_step = 0
        self.color = (200 + random.randint(0, 55), 0, 0)

    def update(self):
        if not self.suck:
            self.velocity[0] = self.speed * math.cos(math.radians(self.heading))
            self.velocity[1] = -1 * self.speed * math.sin(math.radians(self.heading))
            self.speed *= 0.991
            self.x += self.velocity[0]
            self.y += self.velocity[1]
        else:
            self.x += self.x_step
            self.y += self.y_step

    def suckon(self):
        self.suck = True
        self.x_step = (singularities[0].x - self.x) / 100
        self.y_step = (singularities[0].y - self.y) / 100

    def render(self, surface):
        pygame.draw.circle(surface, self.color, (int(self.x), int(self.y)), 3, 0)


class BurstParticle(object):
    def __init__(self, x, y, angle):
        self.x = x
        self.y = y
        self.heading = angle
        self.speed = 2 + random.randint(-2, 2)
        self.velocity = [0, 0]
        self.suck = False
        self.x_step = 0
        self.y_step = 0
        c = random.randint(0, 1)
        if c == 0:
            a = 150 + random.randint(0, 100)
            self.color = (a, a, a)
        else:
            self.color = (155 + random.randint(0, 55), 55, 55)

    def update(self):
        if not self.suck:
            self.velocity[0] = self.speed * math.cos(math.radians(self.heading))
            self.velocity[1] = -1 * self.speed * math.sin(math.radians(self.heading))
            self.speed *= 0.992
            self.x += self.velocity[0]
            self.y += self.velocity[1]
        else:
            self.x += self.x_step
            self.y += self.y_step

    def suckon(self):
        self.suck = True
        self.x_step = (singularities[0].x - self.x) / 100
        self.y_step = (singularities[0].y - self.y) / 100

    def render(self, surface):
        pygame.draw.circle(surface, self.color, (int(self.x), int(self.y)), 2, 0)


class SingularityParticle(object):
    def __init__(self, x, y, radius, color):
        self.x = x
        self.y = y
        self.x_step = (singularities[0].x + 50 - self.x) / 100
        self.y_step = (singularities[0].y + 50 - self.y) / 100
        self.radius = radius
        self.color = color

    def render(self, surface):
        # Render Self
        pygame.draw.circle(surface, self.color, (int(self.x), int(self.y)), self.radius)

    def update(self, inn):
        if inn:
            self.x += self.x_step
            self.y += self.y_step


class BorderEffect(object):
    def __init__(self, opacity):
        self.x = 0
        self.y = 0
        self.opacity = opacity

    def render(self, surface):
        # Render Border Shaky Thing
        self.x = random.uniform(-1, 1) * random.randint(0, 7)
        self.y = random.uniform(-1, 1) * random.randint(0, 7)
        pygame.draw.rect(surface, (215 - self.opacity, 0, 0), (self.x, self.y, screen_width, screen_height), 1)


class FlashEffect(object):
    def __init__(self):
        self.opacity = 100

    def render(self, surface):
        # Flash Flash
        if game:
            if self.opacity < 10:
                self.opacity -= 0.05
            else:
                self.opacity -= 2.25
        else:
            self.opacity -= 2.25

        pygame.gfxdraw.box(surface, (0, 0, screen_width, screen_height), (255, 255, 255, self.opacity))


def reset():
    player1.x = 160
    player1.show = True
    player2.show = True
    player2.x = screen_width - 160
    player1.y = screen_height / 2
    player2.y = screen_height / 2
    player1.mass = 25
    player2.mass = 25
    player1.velocity = [0, 0]
    player2.velocity = [0, 0]
    player1.acceleration = [0, 0]
    player2.acceleration = [0, 0]
    singularities[0].x = screen_width / 2
    singularities[0].y = screen_height / 2


# Scene Initialization
pygame.init()
screen_width = 1600
screen_height = 900
flags = pygame.FULLSCREEN | pygame.DOUBLEBUF
screen = pygame.display.set_mode((screen_width, screen_height), flags, 32)
pygame.display.set_caption("Singularity")
pygame.display.set_icon(icon)

count_1_s = pygame.mixer.Sound('count_1.wav')
explosion_s = pygame.mixer.Sound('explosion.wav')
score_s = pygame.mixer.Sound('score.wav', )
shoot_s = pygame.mixer.Sound('shoot.wav')
music_s = pygame.mixer.music.load('music.wav')
suck_s = pygame.mixer.Sound('suck.wav')
count_1_s.set_volume(0.95)
explosion_s.set_volume(0.25)
score_s.set_volume(1)
shoot_s.set_volume(0.25)


# Variable Initialization
fps = 60
tick = 0
start_counter = 0
timer = 0
clock = pygame.time.Clock()
pygame.joystick.init()
flash = []
player1_score = 0
player2_score = 0
border_effect = []
projectiles = []
burst_particles = []
singularities = []
in_game = True
in_play = True
menu = True
game = False
p1_ready = False
p2_ready = False
p1_a = False
p2_a = False
has_won = 'None'

# Scene Asset Initialization
font = pygame.font.SysFont('singularity', 36)
menu_font = pygame.font.SysFont('singularity', 72)
counter_font = pygame.font.SysFont('singularity', 164)
title_image = pygame.image.load('title.png')
splash = menu_font.render("PRESS 'A' TO READY UP", 1, (255, 255, 255))
winner = menu_font.render('WINNER!!!', 1, (255, 255, 255))
loser = menu_font.render('Loser!!!', 1, (255, 255, 255))
ready = font.render('READY', 1, (255, 255, 255))
player1_mass = menu_font.render('PLAYER 1', 1, (215, 0, 0))
player2_mass = menu_font.render('PLAYER 2', 1, (215, 0, 0))
count_down_1 = counter_font.render('1', 1, (255, 255, 255))
count_down_2 = counter_font.render('2', 1, (255, 255, 255))
count_down_3 = counter_font.render('3', 1, (255, 255, 255))
made_by = font.render('By: Carlos Hernandez and Dalton Fox', 1, (255, 255, 255))
score_counter = counter_font.render(str(player1_score) + ' : ' + str(player2_score), 1, (255, 255, 255))

# Object Initialization
world = World(screen_width, screen_height)
singularities.append(Singularity(100, screen_width / 2, screen_height / 2, False, -1))
for i in range(4):
    border_effect.append(BorderEffect(35 * i))
player1 = Player(160, screen_height / 2, 25, 1)
player2 = Player(screen_width - 160, screen_height / 2, 25, 2)
player2.angle = 180
# Menu Loop
pygame.mixer.music.play(-1)
pygame.mixer.music.set_volume(0.20)

p1_lastshot = 0
p2_lastshot = 0
reload = 0.3

while in_game:
    clock.tick(fps)
    # Menu Loop
    while menu:
        # Start Block
        screen.fill((0, 0, 0))

        # Control Block
        pygame.event.pump()
        if KeyIsPressed('escape'):
            menu = False
            game = False
            end = False
            in_game = False

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                menu = False
                game = False
                in_game = False
            if event.type == pygame.JOYBUTTONUP:
                if p1_a:
                    p1_ready = not p1_ready
                if p2_a:
                    p2_ready = not p2_ready
                p1_a = False
                p2_a = False

        # World Effect Ticker
        if tick == 4:
            k = random.randint(0,6)
            if has_won == 'Player1' and k==4:
                player1.pop()
            elif has_won == 'Player2' and k==4:
                player2.pop()
            world.spawn_particle()
            tick = 0

        # Joystick Input https://www.pygame.org/docs/ref/joystick.html
        for i in range(pygame.joystick.get_count()):
            joystick = pygame.joystick.Joystick(i)
            joystick.init()

            buttons = joystick.get_numbuttons()
            for j in range(buttons):
                button = joystick.get_button(j)
                if button == 1 and j == 0:
                    if i == 0:
                        p1_a = True
                        has_won = 'None'
                    if i == 1:
                        p2_a = True
                        has_won = 'None'

        # Update Block
        for singularity in singularities:
            singularity.update()
        player1.update()
        world.update(in_play)
        player2.update()
        burst_dump = []
        for i in range(len(burst_particles)):
            burst_particles[i].update()
            if burst_particles[i].speed < 0.4:
                burst_dump.append(burst_particles[i])
            if collidingCircles(burst_particles[i].x, burst_particles[i].y, 2, singularities[0].x, singularities[0].y, 105):
                burst_dump.append(burst_particles[i])
        if len(burst_dump) > 0:
            for i in range(len(burst_dump)):
                burst_particles.remove(burst_dump[i])

        # Render Block
        world.render(screen)
        for singularity in singularities:
            singularity.render(screen)
        for i in range(len(burst_particles)):
            burst_particles[i].render(screen)
        player1.render(screen)
        player2.render(screen)
        screen.blit(title_image, (screen_width/2 - 320, screen_height/2 - 400))
        screen.blit(splash, (screen_width/2 - 205, screen_height - 238))
        screen.blit(made_by, (screen_width - 335, screen_height - 40))
        if has_won == 'Player1':
            screen.blit(winner, (int(player1.x - 65), int(player1.y - int(player1.mass * 3.5))))
            screen.blit(loser, (int(player2.x - 45), int(player2.y - int(player2.mass * 3.5))))
        elif has_won == 'Player2':
            screen.blit(winner, (int(player2.x - 65), int(player2.y - int(player2.mass * 3.5))))
            screen.blit(loser, (int(player1.x - 45), int(player1.y - int(player1.mass * 3.5))))
        if p1_ready and has_won == 'None':
            screen.blit(ready, (int(player1.x - 19), int(player1.y - int(player1.mass * 2.5))))
        if p2_ready and has_won == 'None':
            screen.blit(ready, (int(player2.x - 19), int(player2.y - int(player2.mass * 2.5))))
        if p1_ready and p2_ready:
            start_counter += 0.5
            if start_counter == 0.5 or start_counter == 100 or start_counter == 200 or start_counter == 290:
                flash.append(FlashEffect())
                count_1_s.play()
            if start_counter > 200:
                screen.blit(count_down_1, (int(screen_width/2) - 12, int(screen_height/2) - 61))
            elif start_counter > 100:
                screen.blit(count_down_2, (int(screen_width/2) - 25, int(screen_height/2) - 65))
            elif start_counter < 100:
                screen.blit(count_down_3, (int(screen_width/2) - 25, int(screen_height/2) - 65))
            if start_counter >= 310:
                flash = []
                score_counter = counter_font.render(str(player1_score) + ' : ' + str(player2_score), 1, (255, 255, 255))
                menu = False
                game = True
        else:
            start_counter = 0
            flash = []
        if len(flash) > 0:
            for i in range(len(flash)):
                if flash[i].opacity > 10:
                    flash[i].render(screen)

        # End Block
        tick += 1
        pygame.display.update()

    # Game Loop
    while game:
        # Start Block
        time_elapsed = clock.tick()
        timer += time_elapsed
        screen.fill((0, 0, 0))

        # Control Block
        pygame.event.pump()
        if KeyIsPressed('escape'):
            menu = False
            game = False
            end = False
            in_game = False
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                menu = False
                game = False
                in_game = False
            if in_play:
                if event.type == pygame.JOYBUTTONUP:
                    if p1_a and time.time() > p1_lastshot:
                        player1.launch_projectile()
                        p1_lastshot = time.time() + reload
                    if p2_a and time.time() > p2_lastshot:
                        player2.launch_projectile()
                        p2_lastshot = time.time() + reload
                    p1_a = False
                    p2_a = False

        for i in range(pygame.joystick.get_count()):
                joystick = pygame.joystick.Joystick(i)
                joystick.init()

                left_x_axis = joystick.get_axis(0)
                left_y_axis = joystick.get_axis(1)
                right_x_axis = joystick.get_axis(4)
                right_y_axis = joystick.get_axis(3)

                if i == 0:
                    if abs(left_x_axis) > 0.25 and abs(left_y_axis) > 0.25:
                        player1.set_force([left_x_axis, left_y_axis])
                    elif abs(left_x_axis) > 0.25:
                        player1.set_force([left_x_axis, 0])
                    elif abs(left_y_axis) > 0.25:
                        player1.set_force([0, left_y_axis])
                    else:
                        player1.set_force([0, 0])

                    if abs(right_y_axis) > 0.15 and abs(right_x_axis) > 0.15:
                        player1.set_rotation(right_y_axis, right_x_axis)
                if i == 1:
                    if abs(left_x_axis) > 0.25 and abs(left_y_axis) > 0.25:
                        player2.set_force([left_x_axis, left_y_axis])
                    elif abs(left_x_axis) > 0.25:
                        player2.set_force([left_x_axis, 0])
                    elif abs(left_y_axis) > 0.25:
                        player2.set_force([0, left_y_axis])
                    else:
                        player2.set_force([0, 0])

                    if abs(right_y_axis) > 0.15 and abs(right_x_axis) > 0.15:
                        player2.set_rotation(right_y_axis, right_x_axis)

                buttons = joystick.get_numbuttons()
                for j in range(buttons):
                    button = joystick.get_button(j)
                    if button == 1 and j == 5:
                        if i == 0:
                            p1_a = True
                        if i == 1:
                            p2_a = True

        # World Effect Counter
        if tick == 4:
            if in_play:
                world.spawn_particle()
            tick = 0

        for singularity in singularities:
            if collidingCircles(player1.x, player1.y, player1.mass, singularity.x, singularity.y, singularity.mass):
                player1.mass += 0.21
                if singularity.canSuck:
                    singularity.mass -= 0.21
            else:
                player1.mass -= 0.01
            if collidingCircles(player2.x, player2.y, player2.mass, singularity.x, singularity.y, singularity.mass):
                player2.mass += 0.21
                if singularity.canSuck:
                    singularity.mass -= 0.21
            else:
                player2.mass -= 0.01
            if singularity.canSuck:
                singularity.mass -= 0.08

        if collidingCircles(player1.x, player1.y, player1.mass, singularity.x, singularity.y, 100):
            player1.mass += 0.01
        else:
            player1.mass -= 0.01
        if collidingCircles(player2.x, player2.y, player2.mass, singularity.x, singularity.y, 100):
            player2.mass += 0.01
        else:
            player2.mass -= 0.01

        if player1.mass > 100:
            player1.mass = 100
        if player2.mass > 100:
            player2.mass = 100
        if player1.mass < 20:
            player1.mass = 20
        if player2.mass < 20:
            player2.mass = 20

        # Generating singularities
        if timer >= 3000:
            if in_play:
                singularities.append(Singularity(random.randint(30, 60),
                                                 random.randint(int(round(screen_width / 10)),
                                                                int(round(screen_width / 10 * 9))),
                                                 random.randint(int(round(screen_height / 10)),
                                                                int(round(screen_height / 10 * 9))),
                                                 True, random.randint(2000, 4000)))
            timer = 0

        # Update Block
        for singularity in singularities:
            singularity.update()
        for i in range(len(projectiles)):
            projectiles[i].update()
        player1.update()
        world.update(in_play)
        player2.update()
        projectile_dump = []
        burst_dump = []
        for i in range(len(projectiles)):
            if projectiles[i].speed < 0.1:
                projectile_dump.append(projectiles[i])
            elif collidingCircles(projectiles[i].x, projectiles[i].y, projectiles[i].mass+1, player1.x, player1.y, player1.mass):
                projectile_dump.append(projectiles[i])
            elif collidingCircles(projectiles[i].x, projectiles[i].y, projectiles[i].mass+1, player2.x, player2.y, player2.mass):
                projectile_dump.append(projectiles[i])
            elif projectiles[i].is_out_screen():
                projectile_dump.append(projectiles[i])

        for i in range(len(burst_particles)):
            burst_particles[i].update()
            if burst_particles[i].speed < 0.4:
                burst_particles[i].suckon()
            if collidingCircles(burst_particles[i].x, burst_particles[i].y, 2, singularities[0].x, singularities[0].y, 105):
                burst_dump.append(burst_particles[i])
        if len(burst_dump) > 0:
            for i in range(len(burst_dump)):
                burst_particles.remove(burst_dump[i])

        singularities_to_destroy = []
        for singularity in singularities:
            if singularity.canSuck:
                if singularity.mass <= 5:
                    singularities_to_destroy.append(singularity)

        for singularity in singularities_to_destroy:
            singularities.remove(singularity)

        # Render Block
        world.render(screen)
        for i in range(len(burst_particles)):
            burst_particles[i].render(screen)
        for singularity in singularities:
            singularity.render(screen)
        for i in range(len(projectiles)):
            projectiles[i].render(screen)
        player1.render(screen)
        player2.render(screen)
        #for i in range(len(border_effect)):
        #   border_effect[i].render(screen)
        if player1.show:
            x = player1.x - arrow.get_rect().size[0] / 2 + (math.cos(math.radians(player1.angle)) * (player1.mass * 2))
            y = player1.y - arrow.get_rect().size[1] / 2 - (math.sin(math.radians(player1.angle)) * (player1.mass * 2))
            screen.blit(pygame.transform.rotate(arrow, player1.angle), (x, y))
        if player2.show:
            x = player2.x - arrow.get_rect().size[0] / 2 + (math.cos(math.radians(player2.angle)) * (player2.mass * 2))
            y = player2.y - arrow.get_rect().size[1] / 2 - (math.sin(math.radians(player2.angle)) * (player2.mass * 2))
            screen.blit(pygame.transform.rotate(arrow, player2.angle), (x, y))
        screen.blit(player1_mass, (215, 12))
        screen.blit(player2_mass, (screen_width - 365, 12))
        screen.blit(score_counter, (screen_width/2 - 132, 12))
        pygame.draw.rect(screen, (180, 0, 0), (113, 75, 350 * (1 - (100 - player1.mass) / 83), 20), 0)
        pygame.draw.rect(screen, (180, 0, 0), (1137, 75, 350 * (1 - (100 - player2.mass) / 83), 20), 0)
        pygame.draw.rect(screen, (255, 255, 255), (113, 75, 350, 20), 1)
        pygame.draw.rect(screen, (255, 255, 255), (1137, 75, 350, 20), 1)

        if len(flash) > 0:
            for i in range(len(flash)):
                if flash[i].opacity > 0:
                    flash[i].render(screen)
                if flash[i].opacity < 5:
                    flash = []
                    burst_particles = []
                    projectiles = []
                    in_play = True
                    player1.x = 160
                    player1.show = True
                    player2.show = True
                    player2.x = screen_width - 160
                    player1.y = screen_height / 2
                    player2.y = screen_height / 2
                    player1.mass = 25
                    player2.mass = 25
                    player1.velocity = [0, 0]
                    player2.velocity = [0, 0]
                    player1.acceleration = [0, 0]
                    player2.acceleration = [0, 0]
                    singularities[0].x = screen_width / 2
                    singularities[0].y = screen_height / 2
                    break

        if player1.mass >= 99:
            player1_score += 1
            in_play = False
            score_counter = counter_font.render(str(player1_score) + ' : ' + str(player2_score), 1, (255, 255, 255))
            singularities[0].x = -3000
            singularities[0].y = -3000
            player1.death_pop()
            player1.mass = 1
            player1.show = False
            for i in range(len(singularities)):
                if i == 0:
                    continue
                singularities[i].pop()
            for i in range(len(projectiles)):
                projectile_dump.append(projectiles[i])
            singularities = [singularities[0]]

        elif player2.mass >= 99:
            player2_score += 1
            score_counter = counter_font.render(str(player1_score) + ' : ' + str(player2_score), 1, (255, 255, 255))
            in_play = False
            singularities[0].x = -3000
            singularities[0].y = -3000
            player2.death_pop()
            player2.mass = 1
            player2.show = False
            for i in range(len(singularities)):
                if i == 0:
                    continue
                singularities[i].pop()
            for i in range(len(projectiles)):
                projectile_dump.append(projectiles[i])
            singularities = [singularities[0]]

        if len(projectile_dump) > 0:
            for i in range(len(projectile_dump)):
                projectile_dump[i].pop()
                if projectile_dump[i] in projectiles:
                    projectiles.remove(projectile_dump[i])

        if player1_score == 5:
            has_won = 'Player1'
            player1_score = 0
            player2_score = 0
            reset()
            p1_ready = False
            p2_ready = True
            in_play = True
            game = False
            menu = True
        elif player2_score == 5:
            has_won = 'Player2'
            p2_ready = True
            p1_ready = False
            in_play = True
            player1_score = 0
            player2_score = 0
            reset()
            game = False
            menu = True

        # End Block
        tick += 1
        pygame.display.update()


pygame.quit()
