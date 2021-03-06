import os.path
import random
import sys
import math
import pygame
import pygame.gfxdraw
import pygame.mixer
import time
import externals.keyFunctions as keyFuncs
from externals.resolutions import resolutions

# Initialize Project
if sys.platform in ["win32", "win64"]:
    os.environ["SDL_VIDEO_CENTERED"] = "1"
icon = pygame.image.load('Assets/Images/singularity_icon.png')
arrow = pygame.image.load('Assets/Images/arrow.png')


class Player(object):
    def __init__(self, x, y, mass, num):
        self.mass = mass
        self.ready = False
        self.a = False
        self.num = num
        self.has_won = False
        self.color = (55, 55, 55)
        self.score = 0
        self.x = x
        self.last_shot = 0
        self.y = y
        self.acceleration = [0, 0]
        self.velocity = [0, 0]
        self.maxVelocity = 0.5
        self.friction = 0.98
        self.effects = []
        self.angle = 0
        self.show = True
        self.on_game = False

        self.init_x = x
        self.init_y = y
        self.init_mass = mass

        # Character Effects
        for i in range(10):
            self.create_effect()

        # Labeling
        st = "P" + str(num)
        self.name = font.render(st, 1, (255, 255, 255))

    def render(self, surface):
        if self.show:
            # Render Effects
            for i in range(len(self.effects)):
                self.effects[i].render(surface)

            # Render Player
            pygame.draw.circle(surface, (0, 0, 0), (int(self.x), int(self.y)), int(self.mass))
            pygame.draw.circle(surface, self.color, (int(self.x), int(self.y)), int(self.mass), 1)

            # Render Label
            if self.color != (55, 55, 55):
                surface.blit(self.name, (int(self.x - 8), int(self.y - 13)))

    def update(self):
        for i in range(len(projectile_list)):
            px = projectile_list[i].x
            py = projectile_list[i].y
            pr = projectile_list[i].mass
            if projectile_list[i].color != self.color and colliding_circles(self.x, self.y, self.mass, px, py, pr):
                if projectile_list[i].velocity[0] > 0:
                    vx = 2
                else:
                    vx = -2
                if projectile_list[i].velocity[1] > 0:
                    vy = 2
                else:
                    vy = 2
                self.set_force([(projectile_list[i].velocity[0] + vx) * min(self.mass, 30),
                                (projectile_list[i].velocity[1] + vy) * min(self.mass, 30)])

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
        self.acceleration[0] = force[0] / min(self.mass, 30)
        self.acceleration[1] = force[1] / min(self.mass, 30)

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
        self.effects.append(SingularityEffect(self.x, self.y, self.color,
                                              random.randint(int(self.mass - int(self.mass / 4)),
                                                             int(self.mass + int(self.mass / 5))),
                                              random.randint(90, 100)))

    def launch_projectile(self):
        shoot_s.play()
        angle_radians = math.radians(self.angle)
        self.mass -= self.mass / 2
        projectile_list.append(Projectile(self.angle, int(self.mass / 1.5),
                                          self.x + (math.cos(angle_radians) * (self.mass * 1)),
                                          self.y - (math.sin(angle_radians) * (self.mass * 1)),
                                          self.color))

    def set_rotation(self, sin_value, cos_value):
        if sin_value != 0:
            if right_y_axis < 0:
                self.angle = math.degrees(math.atan(cos_value / sin_value)) - 270
            else:
                self.angle = math.degrees(math.atan(cos_value / sin_value)) - 90

    def next_color(self):
        if self.color == colors_pool[len(colors_pool)-1]:
            self.color = colors_pool[0]
        else:
            for ind in range(len(colors_pool)):
                if colors_pool[ind] == self.color:
                    self.color = colors_pool[ind+1]
                    break


class Projectile(object):
    def __init__(self, rot, mass, x, y, color):
        self.mass = mass
        self.x = x
        self.color = color
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
        self.angle = (self.angle + self.rot) % 360
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
        if self.x + self.mass > screen_width or self.x < 0 or self.y > screen_height or self.y - self.mass < 0:
            return True
        return False

    def render(self, surface):
        pygame.draw.aalines(surface, self.color, True, self.real_points)


class World(object):
    def __init__(self):
        self.particles = []

    def render(self, surface):
        # Render Grid Lines
        for c2 in range(0, screen_width, int(screen_width / resolution.xEven)):
            pygame.draw.line(surface, (11, 11, 11), (c2, 0), (c2, screen_height), 1)
        for r2 in range(0, screen_height, int(screen_height / resolution.yEven)):
            pygame.draw.line(surface, (11, 11, 11), (0, r2), (screen_width, r2), 1)
        for c1 in range(0, screen_width, int(screen_width / (resolution.xEven/2))):
            pygame.draw.line(surface, (53, 53, 53), (c1, 0), (c1, screen_height), 1)
        for r1 in range(0, screen_height, int(screen_height / (resolution.yEven/2))):
            pygame.draw.line(surface, (53, 53, 53), (0, r1), (screen_width, r1), 1)
        pygame.draw.line(surface, (53, 53, 53), (screen_width-1, 0), (screen_width-1, screen_height), 1)
        pygame.draw.line(surface, (53, 53, 53), (0, screen_height-1), (screen_width, screen_height-1), 1)

        if paused:
            pygame.gfxdraw.box(screen, (0, 0, screen_width, screen_height), (0, 0, 0, 200))

        # Render Particles
        for i in range(len(self.particles)):
            self.particles[i].render(surface)

    def update(self, inn):
        # Update Effects
        remove_list = []

        for i in range(len(self.particles)):
            self.particles[i].update(inn)
            p = self.particles[i]
            if colliding_circles(p.x, p.y, p.size, singularity_list[0].x, singularity_list[0].y, 105):
                remove_list.append(self.particles[i])

        if len(remove_list) > 0:
            for i in range(len(remove_list)):
                self.particles.remove(remove_list[i])

    def spawn_particle(self):
        # Create World Particles
        ran = random.randint(0, 3)
        if player_list[ran].num == 1:
            gen_x = random.randint(-300, screen_width / 2)
            gen_y = random.randint(-300, screen_height / 2)
        elif player_list[ran].num == 2:
            gen_x = random.randint(screen_width / 2, screen_width)
            gen_y = random.randint(-300, screen_height / 2)
        elif player_list[ran].num == 3:
            gen_x = random.randint(-300, screen_width / 2)
            gen_y = random.randint(screen_height / 2, screen_height)
        else:
            gen_x = random.randint(screen_width / 2, screen_width)
            gen_y = random.randint(screen_height / 2, screen_height)

        colorr = player_list[ran].color
        if colorr == (55, 55, 55):
            colorr = (255, 255, 255)
        temp_part = PhysParticle(gen_x, gen_y, 0, random.randint(1, 3), random.randint(2, 3), True, color=colorr)
        temp_part.attract()
        self.particles.append(temp_part)


class Singularity(object):
    def __init__(self, mass, x, y, color, canSuck, life_time):
        self.mass = mass
        self.x = x
        self.y = y
        self.effects = []
        self.canSuck = canSuck
        self.color = color
        self.life_time = life_time

        # Initialize Ring Effects
        for i in range(10):
            self.create_effect()

    def render(self, surface):
        # Render Effects
        for i in range(len(self.effects)):
            self.effects[i].render(surface)

        # Render Singularity
        pygame.draw.circle(surface, (0, 0, 0), (int(self.x), int(self.y)), int(self.mass))
        pygame.draw.circle(surface, self.color, (int(self.x), int(self.y)), int(self.mass), 1)

    def update(self):
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
        self.effects.append(
            SingularityEffect(self.x, self.y, self.color,
                              random.randint(int(self.mass) - int(round(self.mass / 10)),
                                             int(self.mass) + int(round(self.mass / 10))),
                              random.randint(95, 100)))


class SingularityEffect(object):
    def __init__(self, x, y, color, radius, opacity):
        self.x = x
        self.y = y
        self.color = color
        self.radius = radius
        self.opacity = opacity

    def render(self, surface):
        # Render Effect (filled or line)
        pygame.gfxdraw.circle(surface, int(self.x), int(self.y), self.radius,
                              (self.color[0], self.color[1], self.color[2], self.opacity))

    def update(self):
        # Update Position
        self.x += random.uniform(-1, 1) * random.randint(int(self.radius / 13), int(self.radius / 12))
        self.y += random.uniform(-1, 1) * random.randint(int(self.radius / 13), int(self.radius / 12))

        # Update Opacity
        self.opacity -= random.randint(2, 6)


class PhysParticle(object):
    def __init__(self, x, y, angle, size, speed, solid, color=None):
        self.x = x
        self.y = y
        self.heading = angle
        self.speed = speed + random.randint(-4, 4)
        if self.speed < 2:
            self.speed = 2
        self.velocity = [0, 0]
        self.attracted = False
        self.x_step = 0
        self.y_step = 0
        self.size = size

        # Selected or Random Color
        if color is not None:
            if solid:
                self.color = color
            else:
                c = random.randint(0, 1)
                if c == 0:
                    a = 150 + random.randint(0, 100)
                    self.color = (a, a, a)
                else:
                    self.color = color
        else:
            a = 150 + random.randint(0, 100)
            self.color = (a, a, a)

    def update(self, inn):
        if not self.attracted:
            self.velocity[0] = self.speed * math.cos(math.radians(self.heading))
            self.velocity[1] = -1 * self.speed * math.sin(math.radians(self.heading))
            self.speed *= 0.992
            self.x += self.velocity[0]
            self.y += self.velocity[1]
        else:
            if inn:
                self.x += self.x_step
                self.y += self.y_step

    def attract(self):
        self.attracted = True
        self.x_step = (singularity_list[0].x - self.x) / 100
        self.y_step = (singularity_list[0].y - self.y) / 100

    def render(self, surface):
        pygame.draw.circle(surface, self.color, (int(self.x), int(self.y)), self.size, 0)


class FlashEffect(object):
    def __init__(self):
        self.opacity = 100

    def render(self, surface):
        # Flash Flash
        if game_stage:
            if self.opacity < 10:
                self.opacity -= 0.05
            else:
                self.opacity -= 2.25
        else:
            self.opacity -= 2.25

        pygame.gfxdraw.box(surface, (0, 0, screen_width, screen_height), (255, 255, 255, self.opacity))


def colliding_circles(c1x, c1y, c1r, c2x, c2y, c2r):
    if (int(c1x) - int(c2x)) ** 2 + (int(c1y) - int(c2y)) ** 2 <= (int(c1r) + int(c2r)) ** 2:
        return True
    return False


def create_explosion(x, y, mass, num_parts, speed=2, part_size=2, part_solid=False, part_color=None, create_center=False, create_flash=False, sound=None):
    angle = 0
    factor_n = 1.30 - ((25.0 - mass) / 25.0)

    # Play a sound if we are suppose to
    if sound is not None:
        sound.play()

    # Create a flash if we're suppose to
    if create_flash:
        flash_list.append(FlashEffect())

    # Create specified number of particles
    for part in range(random.randint(int((num_parts - 20) * factor_n) + 2, int(num_parts * factor_n))):
        angle = (angle + (360 / num_parts)) % 360
        if create_center:
            particle_list.append(PhysParticle(x + (math.cos(math.radians(angle)) * (mass * 2)),
                                              y - (math.sin(math.radians(angle) * (mass * 2))),
                                              angle, part_size, speed, part_solid, part_color))
        else:
            particle_list.append(PhysParticle(x, y, angle, part_size, speed, part_solid, part_color))


def reset_game():
    for player in player_list:
        player.x = player.init_x
        player.y = player.init_y
        player.show = True
        player.velocity = [0, 0]
        player.acceleration = [0, 0]
        player.mass = player.init_mass
    singularity_list[0].x = screen_width / 2
    singularity_list[0].y = screen_height / 2
    #player_list[2].ready = True  # debug
    for player in null_players:
        player_list.append(player)


# Game Initialization
pygame.init()
resolution = resolutions.get('1280x720')
screen_width = resolution.width
screen_height = resolution.height

flags = pygame.HWSURFACE | pygame.DOUBLEBUF #| pygame.FULLSCREEN
screen = pygame.display.set_mode((screen_width, screen_height), flags, 32)
pygame.display.set_caption("Singularity")
pygame.display.set_icon(icon)

count_1_s = pygame.mixer.Sound('Assets/Audio/count.wav')
explosion_s = pygame.mixer.Sound('Assets/Audio/explosion.wav')
score_s = pygame.mixer.Sound('Assets/Audio/score.wav', )
shoot_s = pygame.mixer.Sound('Assets/Audio/shoot.wav')
music_s = pygame.mixer.music.load('Assets/Audio/music.wav')
suck_s = pygame.mixer.Sound('Assets/Audio/suck.wav')
count_1_s.set_volume(0.95)
explosion_s.set_volume(0.25)
score_s.set_volume(1)
shoot_s.set_volume(0.25)

# Variable Initialization
max_fps = 240
tick = 0
start_counter = 0
timer = 0
clock = pygame.time.Clock()
pygame.joystick.init()
flash_list = []
player_list = []
null_players = []
projectile_list = []
particle_list = []
singularity_list = []
colors_pool = [(255, 0, 0), (25, 255, 0), (30, 140, 255), (255, 215, 0)]
colors_used = [0, 0, 0, 0]
in_game = True
in_play = True
menu_stage = True
game_stage = False
paused = False
p = False

# Scene Asset Initialization
font = pygame.font.Font('Assets/Fonts/Singularity.ttf', int(34 * (resolution.UIscale - 0.10)))
menu_font = pygame.font.Font('Assets/Fonts/Singularity.ttf', 72)
counter_font = pygame.font.Font('Assets/Fonts/Singularity.ttf', 164)
title_font = pygame.font.Font('Assets/Fonts/Singularity.ttf', int(262 * (resolution.UIscale - 0.10)))
splash = font.render("     PRESS 'A' TO READY UP", 1, (255, 255, 255))
select = font.render("<- AND -> TO SELECT A TEAM COLOR", 1, (255, 255, 255))
splash2 = font.render("   PRESS 'START' FOR SETTINGS", 1, (255, 255, 255))
splash3 = font.render("   PRESS 'Y' TO START TUTORIAL", 1, (155, 155, 155))
title = title_font.render("SINGULARITY", 1, (255, 255, 255))
winner = menu_font.render('WINNER!!!', 1, (255, 255, 255))
loser = menu_font.render('Loser!!!', 1, (255, 255, 255))
ready = font.render('READY', 1, (255, 255, 255))
player1_mass = menu_font.render('PLAYER 1', 1, (215, 0, 0))
player2_mass = menu_font.render('PLAYER 2', 1, (215, 0, 0))
player3_mass = menu_font.render('PLAYER 3', 1, (215, 0, 0))
player4_mass = menu_font.render('PLAYER 4', 1, (215, 0, 0))
count_down_1 = counter_font.render('1', 1, (255, 255, 255))
count_down_2 = counter_font.render('2', 1, (255, 255, 255))
count_down_3 = counter_font.render('3', 1, (255, 255, 255))
made_by = font.render('By: Carlos Hernandez and Dalton Fox', 1, (255, 255, 255))

# Object Initialization
world = World()
singularity_list.append(Singularity(100, screen_width / 2, screen_height / 2, (255, 255, 255), False, -1))
player_list.append(Player(screen_width * resolution.aspect.p1OF[0], screen_height * resolution.aspect.p1OF[1], 25, 1))
player_list.append(Player(screen_width * resolution.aspect.p2OF[0], screen_height * resolution.aspect.p2OF[1], 25, 2))
player_list.append(Player(screen_width * resolution.aspect.p3OF[0], screen_height * resolution.aspect.p3OF[1], 25, 3))
player_list.append(Player(screen_width * resolution.aspect.p4OF[0], screen_height * resolution.aspect.p4OF[1], 25, 4))

# Menu Loop
pygame.mixer.music.play(-1)
pygame.mixer.music.set_volume(0.00)

# TODO: Organize variables
# TODO: Clean Sweep Optimization
# TODO: Performance Optimization
reload = 0.3
max_score = 5
someone_won = False
on_game_players = 0
tween = 0
while in_game:
    # Menu Loop
    while menu_stage:

        # Start Block
        clock.tick(max_fps)
        screen.fill((0, 0, 0))
        active_players = 0
        on_game_players = 0
        for player in player_list:
            if player.ready:
                active_players += 1
            if player.on_game:
                on_game_players += 1

        #print(clock.get_fps())

        # Input Update Block
        pygame.event.pump()
        if keyFuncs.key_is_pressed('escape'):
            menu_stage = False
            game_stage = False
            end = False
            in_game = False

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                menu_stage = False
                game_stage = False
                end = False
                in_game = False
            if event.type == pygame.JOYBUTTONUP:
                for player in player_list:
                    if player is None:
                        continue
                    if player.a:
                        player.ready = not player.ready
                    player.a = False
                if p:
                    #TODO: reset game state stuff
                    paused = not paused
                    p = False
                    if paused:
                        tween += singularity_list[0].mass / 6
                    else:
                        singularity_list[0].mass = 100
                        tween = -1

        # World Block
        if tick == 3:
            k = random.randint(0, 6)
            if k == 4:
                for player in player_list:
                    if player.has_won:
                        create_explosion(player.x, player.y, player.mass, 25, speed=random.randint(1, 3), part_color=player.color)
            world.spawn_particle()
            tick = 0
        if tween >= 0:
            singularity_list[0].mass += 10
            tween -= 1

        # Joystick Input Block
        # changed
        for i in range(pygame.joystick.get_count()):
            joystick = pygame.joystick.Joystick(i)
            joystick.init()
            left_x_axis = joystick.get_axis(0)
            right_x_axis = joystick.get_axis(4)

            # changed
            for j in (0, 1, 2, 3, 4, 5, 6, 7):
                # we dont need check all the buttons //add to the tuple only the buttons to check
                # --> we really dont need that numbers, only the A and the Select for now
                # added all the numbers because can not iterate in a tuple of one value
                button = joystick.get_button(j)
                if button == 1 and j == 0:  # j= key , button = pressed or not --> if A pressed
                    for player in player_list:
                        if i == player.num - 1:
                            player.a = True
                            #active_players += 1
                            # debug
                            if player.color == (55, 55, 55):
                                for index in range(len(colors_used)):
                                    if colors_used[index] == 0:
                                        player.color = colors_pool[index]
                                        colors_used[index] = 1
                                        break
                            player.has_won = False
                            player.on_game = True
                if button == 1 and j == 7:
                    p = True

            if abs(left_x_axis) > 0.75 or abs(right_x_axis) > 0.75:  # added
                for player in player_list:
                    if i == player.num - 1 and not player.ready and player.can_change_color:
                        if player.color == (55, 55, 55):
                            for index in range(len(colors_used)):
                                if colors_used[index] == 0:
                                    player.color = colors_pool[index]
                                    colors_used[index] = 1
                                    break
                        else:
                            player.next_color()
                        player.has_won = False
                        player.can_change_color = False
                        player.on_game = True

            elif abs(left_x_axis) < 0.1 or abs(right_x_axis) < 0.1:
                for player in player_list:
                    if i == player.num - 1 and not player.ready:
                        player.can_change_color = True

        # Update Block
        for singularity in singularity_list:
            singularity.update()
        for player in player_list:
            player.update()
        world.update(in_play)
        burst_dump = []
        for i in range(len(particle_list)):
            particle_list[i].update(in_play)
            if particle_list[i].speed < 0.4:
                burst_dump.append(particle_list[i])
            if colliding_circles(particle_list[i].x, particle_list[i].y, 2, singularity_list[0].x, singularity_list[0].y, 105):
                burst_dump.append(particle_list[i])
        if len(burst_dump) > 0:
            for i in range(len(burst_dump)):
                particle_list.remove(burst_dump[i])

        for projectile in projectile_list:
            projectile.update()

        # Render Block
        world.render(screen)
        for singularity in singularity_list:
            singularity.render(screen)
        if not paused:
            for projectile in projectile_list:
                projectile.render(screen)
        for i in range(len(particle_list)):
            particle_list[i].render(screen)
        if not paused:
            for player in player_list:
                player.render(screen)

        if not paused:
            pygame.draw.rect(screen, (0, 0, 0), (screen_width * (resolution.aspect.rectLeftOF[0]),
                                        screen_height * (resolution.aspect.rectLeftOF[1]),
                                        screen_width * (resolution.aspect.rectRightOF[0]),
                                        screen_height * (resolution.aspect.rectRightOF[1])), 0)
            pygame.draw.rect(screen, (255, 255, 255), (screen_width * (resolution.aspect.rectLeftOF[0]),
                                                      screen_height * (resolution.aspect.rectLeftOF[1]),
                                                      screen_width * (resolution.aspect.rectRightOF[0]),
                                                      screen_height * (resolution.aspect.rectRightOF[1])), 1)
            screen.blit(title, (screen_width * resolution.aspect.titleOF[0], screen_height * resolution.aspect.titleOF[1]))
            screen.blit(splash, (screen_width * resolution.aspect.tipOF[0], screen_height * resolution.aspect.tipOF[1]))
            screen.blit(splash2, (screen_width * resolution.aspect.tipOF[0], screen_height * (resolution.aspect.tipOF[1] + 0.05)))
            screen.blit(select, (screen_width * resolution.aspect.tipOF[0], screen_height * (resolution.aspect.tipOF[1] + 0.1)))
            screen.blit(splash3, (screen_width * resolution.aspect.tipOF[0], screen_height * (resolution.aspect.tipOF[1] + 0.15)))
            screen.blit(made_by, (screen_width * resolution.aspect.credOF[0], screen_height * resolution.aspect.credOF[1]))
            for player in player_list:
                if player.has_won:
                    screen.blit(winner, (int(player.x - 65), int(player.y - int(player.mass * 3.5))))
            for player in player_list:
                if player.ready:
                    screen.blit(ready, (int(player.x - 19), int(player.y - int(player.mass * 2.5))))

        if len(flash_list) > 0:
            for i in range(len(flash_list)):
                if flash_list[i].opacity > 10:
                    flash_list[i].render(screen)

        # Exit Sequence Render
        if active_players == on_game_players and on_game_players != 1 and active_players != 0:
            start_counter += 0.5
            if start_counter == 0.5 or start_counter == 100 or start_counter == 200 or start_counter == 290:
                flash_list.append(FlashEffect())
                count_1_s.play()
            if start_counter > 200:
                screen.blit(count_down_1, (int(screen_width / 2) - 12, int(screen_height / 2) - 61))
            elif start_counter > 100:
                screen.blit(count_down_2, (int(screen_width / 2) - 25, int(screen_height / 2) - 65))
            elif start_counter < 100:
                screen.blit(count_down_3, (int(screen_width / 2) - 25, int(screen_height / 2) - 65))
            if start_counter >= 310:
                for player in player_list:
                    if not player.ready:
                        null_players.append(player)
                for player in null_players:
                    player_list.remove(player)
                flash_list = []
                score_string = ""
                for i in range(len(player_list)):
                    if i > 0:
                        score_string += " : "
                    if not player_list[i].ready:
                        continue
                    else:
                        score_string += str(player_list[i].score)
                score_counter = counter_font.render(score_string, 1, (255, 255, 255))
                text_width, text_height = counter_font.size(score_string)
                menu_stage = False
                game_stage = True
        else:
            start_counter = 0
            flash_list = []

        # End Block
        tick += 1
        pygame.display.update()

    # Game Loop
    while game_stage:
        # Start Block
        time_elapsed = clock.tick(max_fps)
        timer += time_elapsed
        screen.fill((0, 0, 0))

        # Control Block
        pygame.event.pump()
        if keyFuncs.key_is_pressed('escape'):
            menu_stage = False
            game_stage = False
            end = False
            in_game = False
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                menu_stage = False
                game_stage = False
                in_game = False
            if in_play:
                if event.type == pygame.JOYBUTTONUP:
                    for player in player_list:
                        if player.a and time.time() > player.last_shot:
                            player.launch_projectile()
                            player.last_shot = time.time() + reload
                        player.a = False

        # Joystick Input Block
        for i in range(pygame.joystick.get_count()):
                joystick = pygame.joystick.Joystick(i)
                joystick.init()

                left_x_axis = joystick.get_axis(0)
                left_y_axis = joystick.get_axis(1)
                right_x_axis = joystick.get_axis(4)
                right_y_axis = joystick.get_axis(3)

                for player in player_list:
                    if i == player.num - 1:
                        if abs(left_x_axis) > 0.25 and abs(left_y_axis) > 0.25:
                            player.set_force([left_x_axis, left_y_axis])
                        elif abs(left_x_axis) > 0.25:
                            player.set_force([left_x_axis, 0])
                        elif abs(left_y_axis) > 0.25:
                            player.set_force([0, left_y_axis])
                        else:
                            player.set_force([0, 0])

                        if abs(right_y_axis) > 0.25 or abs(right_x_axis) > 0.25:
                            player.set_rotation(right_y_axis, right_x_axis)

                buttons = joystick.get_numbuttons()
                for j in range(buttons):
                    button = joystick.get_button(j)
                    if button == 1 and j == 5:
                        for player in player_list:
                            if i == player.num - 1:
                                player.a = True

        # World Block
        if tick == 4:
            if in_play:
                world.spawn_particle()
            tick = 0
        for singularity in singularity_list:
            for player in player_list:
                if colliding_circles(player.x, player.y, player.mass, singularity.x, singularity.y, singularity.mass):
                    if in_play:
                        player.mass += 0.21
                        if singularity.canSuck:
                            singularity.mass -= 0.21
                else:
                    player.mass -= 0.073
                if player.mass > 100:
                    player.mass = 100
                if player.mass < 20:
                    player.mass = 20
            if singularity.canSuck:
                singularity.mass -= 0.08

        # Generating singularities
        if timer >= 3000:
            if in_play:
                timer = 0
                singularity_list.append(Singularity(random.randint(30, 60),
                                                    random.randint(int(round(screen_width / 10)), int(round(screen_width / 10 * 9))),
                                                    random.randint(int(round(screen_height / 10)), int(round(screen_height / 10 * 9))),
                                                    (255, 255, 255), True, random.randint(2000, 4000)))

        # Update Block
        for singularity in singularity_list:
            singularity.update()
        for i in range(len(projectile_list)):
            projectile_list[i].update()
        for player in player_list:
            player.update()
        world.update(in_play)
        projectile_dump = []
        burst_dump = []
        for i in range(len(projectile_list)):
            if projectile_list[i].speed < 0.1:
                projectile_dump.append(projectile_list[i])
            elif projectile_list[i].is_out_screen():
                projectile_dump.append(projectile_list[i])
            for player in player_list:
                if projectile_list[i].color != player.color and colliding_circles(projectile_list[i].x, projectile_list[i].y, projectile_list[i].mass + 1, player.x, player.y, player.mass):
                    projectile_dump.append(projectile_list[i])

        for i in range(len(particle_list)):
            particle_list[i].update(in_play)
            if particle_list[i].speed < 0.4:
                particle_list[i].attract()
            if colliding_circles(particle_list[i].x, particle_list[i].y, 2, singularity_list[0].x, singularity_list[0].y, 105):
                if in_play:
                    burst_dump.append(particle_list[i])
        if len(burst_dump) > 0:
            for i in range(len(burst_dump)):
                particle_list.remove(burst_dump[i])

        singularities_to_destroy = []
        for singularity in singularity_list:
            if singularity.canSuck:
                if singularity.mass <= 5:
                    singularities_to_destroy.append(singularity)

        for singularity in singularities_to_destroy:
            singularity_list.remove(singularity)

        # Render Block
        world.render(screen)
        for i in range(len(particle_list)):
            particle_list[i].render(screen)
        for singularity in singularity_list:
            if in_play:
                singularity.render(screen)
        for i in range(len(projectile_list)):
            projectile_list[i].render(screen)
        for player in player_list:
            player.render(screen)
            if player.show:
                x = player.x - arrow.get_rect().size[0] / 2 + (math.cos(math.radians(player.angle)) * (player.mass * 2))
                y = player.y - arrow.get_rect().size[1] / 2 - (math.sin(math.radians(player.angle)) * (player.mass * 2))
                screen.blit(pygame.transform.rotate(arrow, player.angle), (x, y))

        screen.blit(score_counter, (screen_width / 2 - text_width/2, 12))

        # Effect Update
        if len(flash_list) > 0:
            for i in range(len(flash_list)):
                if flash_list[i].opacity > 0:
                    flash_list[i].render(screen)
                if flash_list[i].opacity < 5:
                    flash_list = []
                    particle_list = []
                    projectile_list = []
                    in_play = True
                    for player in player_list:
                        player.x = player.init_x
                        player.y = player.init_y
                        player.show = True
                        player.mass = player.init_mass
                        player.velocity = [0, 0]
                        player.acceleration = [0, 0]
                    singularity_list[0].x = screen_width / 2
                    singularity_list[0].y = screen_height / 2
                    break

        # Score Block
        for player in player_list:
            if player.mass >= 99:
                player.score += 1
                in_play = False
                score_string = ""
                for i in range(len(player_list)):
                    if i > 0:
                        score_string += " : "
                    if not player_list[i].ready:
                        continue
                    else:
                        score_string += str(player_list[i].score)
                score_counter = counter_font.render(score_string, 1, (255, 255, 255))
                text_width, text_height = counter_font.size(score_string)
                create_explosion(player.x, player.y, player.mass, 45, speed=12, part_color=player.color, part_solid=True, create_flash=True, sound=score_s)
                player.mass = 1
                player.show = False
                for i in range(len(singularity_list)):
                    if i == 0:
                        continue
                    create_explosion(singularity_list[i].x, singularity_list[i].y, singularity_list[i].mass, 30)
                for i in range(len(projectile_list)):
                    projectile_dump.append(projectile_list[i])
                singularity_list = [singularity_list[0]]

        # Clean-up Block
        if len(projectile_dump) > 0:
            for i in range(len(projectile_dump)):
                create_explosion(projectile_dump[i].x, projectile_dump[i].y, projectile_dump[i].mass, 15, sound=explosion_s)
                if projectile_dump[i] in projectile_list:
                    projectile_list.remove(projectile_dump[i])

        # Exit Block
        for player in player_list:
            if player.score == max_score:
                player.has_won = True
                someone_won = True
        if someone_won:
            for player in player_list:
                player.score = 0
                player.ready = False
            reset_game()
            null_players = []
            in_play = True
            game_stage = False
            menu_stage = True
            someone_won = False

        # End Block
        tick += 1
        pygame.display.update()

pygame.display.quit()
pygame.quit()
