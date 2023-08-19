import pygame
import sys
import random

class Disign():
    def __init__(self):
            #BILDER:
        self.obstacle_img = pygame.image.load("Assets\\textures\\Obstacle.png").convert_alpha()
        self.wyvern_img = pygame.image.load("Assets\\textures\\Wyvern.png").convert_alpha()
        self.wyvern_phasing_img = pygame.image.load("Assets\\textures\\Wyvern(Phasing).png").convert_alpha()
        self.powerup_img = pygame.image.load("Assets\\textures\\PowerUp_Phasing.png").convert_alpha()
        self.heart_img = pygame.image.load("Assets\\textures\\Heart.png").convert_alpha()
        self.end_img = pygame.image.load("Assets\\textures\\End.png").convert_alpha()
        self.background_img = pygame.image.load("Assets\\textures\\Background.png").convert_alpha()
        self.teleport_img = pygame.image.load("Assets\\textures\\PowerUp_Teleport.png").convert_alpha()
        self.bomb_img = pygame.image.load("Assets\\textures\\Bomb.png").convert_alpha()
        self.startbutton_img = pygame.image.load("Assets\\textures\\Startbutton.png").convert_alpha()
        self.greystartbutton_img = pygame.image.load("Assets\\textures\\Startbutton(grey).png").convert_alpha()
            #BUFFER LOCATIONS:
        self.wyvern_buffer_location = (0, -1)
        self.phasing_buffer_location = (1, -1)
        self.end_buffer_location = (2, -1)
        self.teleport_buffer_location = (3, -1)
            #FONTS:
        self.subscore_font = pygame.font.Font("Assets\\fonts\\Vermin Vibes 1989.ttf", 50)
        self.highscore_font = pygame.font.Font("Assets\\fonts\\Vermin Vibes 1989.ttf", 80)
        number_spritesheet = pygame.image.load("Assets\\fonts\\Numbers.png").convert_alpha()
        heart_number_spritesheet = pygame.image.load("Assets\\fonts\\HeartNumbers.png").convert_alpha()
        self.numbers_list = []
        for i in range(10):
            number = number_spritesheet.subsurface(pygame.Rect(i * 25, 0, 25, 25))
            self.numbers_list.append(number)
        self.heart_numbers_list = []
        for i in range(10):
            number = heart_number_spritesheet.subsurface(pygame.Rect(i * 25, 0, 25, 25))
            self.heart_numbers_list.append(number)

class Tile: #nur zum inheriten für alles andere
        def draw_tile(self, position, disign):
            # Zeichnet die Wyvern an ihrer aktuellen Position auf dem Spielfeld
            x, y = position
            if type(disign) is tuple:
                pygame.draw.rect(game.display, disign, (game.cell_size * (x - 1), game.cell_size * (y - 1), game.cell_size, game.cell_size))
            else:
                game.display.blit(disign, (game.cell_size * (x - 1), game.cell_size * (y - 1), game.cell_size, game.cell_size))

class Background(Tile):
    def draw(self): 
        game.display.fill(disign.background_color) # white background color
        for x in range(0, game.window_width, game.cell_size):
            pygame.draw.line(game.display, disign.grid_color, (x, 0), (x, game.window_height))
        for y in range(0, game.window_height, game.cell_size):
            pygame.draw.line(game.display, disign.grid_color, (0, y), (game.window_width, y))

class Maze(Tile):
    def __init__(self):
        self.start_end_length = ((0, 0), (0, 0), 0)

    def draw(self, disign):
        for x, y in game.obstacles:
            self.draw_tile((x, y), disign)

    def create(self):
        width = 34
        height = 20
        def create_grid():
            grid = {}
            for x in range(1, width+1):
                for y in range(1, height+1):
                    grid[(x, y)] = 1
            return grid

        def is_valid(x, y):
            return 0 < x <= width and 0 < y <= height

        def visit(x, y):
            grid[(x, y)] = 0
            directions = [(0, -2), (0, 2), (-2, 0), (2, 0)]
            random.shuffle(directions)

            for direction_x, direction_y in directions:
                new_x, new_y = x + direction_x, y + direction_y
                if is_valid(new_x, new_y) and grid[(new_x, new_y)] == 1:
                    grid[(x + direction_x // 2 + 2, y + direction_y // 2  + 2)] = 0
                    grid[(new_x, new_y)] = 0
                    visit(new_x, new_y)
        grid = create_grid()
        visit(x=1, y=1)
        game.obstacles = [(x-1, y-1) for y in range(height) for x in range(width) if grid[(x+1, y+1)] == 0] + gui.required_space
        game.occupied_levelstart_tiles = [(x-1, y-1) for y in range(height) for x in range(width) if grid[(x+1, y+1)] == 0] + gui.required_space

    def find_longest_path(self, start_x, start_y):
        lost_ends = []
        def is_valid(x, y, visited_list):
            if (1 <= x <= 32) and (1 <= y <= 18) and ((x,y) not in game.obstacles) and ((x,y) not in visited_list):
                return True
            else:
                return False
            
        def explore_path(x, y, visited_list):
            visited_list.append((x, y))
            max_path_length = 0
            found_end_point = False

            for dx, dy in [(1, 0), (-1, 0), (0, 1), (0, -1)]:
                new_x, new_y = x + dx, y + dy
                if is_valid(new_x, new_y, visited_list):
                    found_end_point = True
                    max_path_length = max(max_path_length, explore_path(new_x, new_y, visited_list))
            
            if not found_end_point:
                end_points[len(visited_list) - 1] = visited_list[-1]
                long_paths.append(len(visited_list) - 1)
                lost_ends.append((x, y))
            
            visited_list.pop()
            return max_path_length + 1

        visited = []
        end_points = {}
        long_paths = []
 

        explore_path(start_x, start_y, visited)

        return end_points[max(long_paths)], max(long_paths), lost_ends


    def reveal_path(self):
        for start in game.safe_tiles:
            _, _, old_path_lengh = self.start_end_length
            new_ednpoint, new_path_lengh, endpoints_of_the_iteration = maze.find_longest_path(start[0], start[1])
            game.endpoints.extend(endpoints_of_the_iteration)
            if old_path_lengh < new_path_lengh:
                self.start_end_length = start, new_ednpoint, new_path_lengh
        self.start_end_length =  self.start_end_length[0], self.start_end_length[1] #wichtig um den beseten weg zu berechnen
        game.endpoints = list(set(game.endpoints)) # bereinigt die liste von dupliakten
        wyvern.position = self.start_end_length[0]
        game.endpoints.remove(wyvern.position)
        end.position = self.start_end_length[1]
        game.endpoints.remove(end.position)
        game.occupied_levelstart_tiles.extend([wyvern.position, end.position])

class PowerUp_Phasing(Tile):
    def __init__(self):
        self.position = disign.phasing_buffer_location
        self.active = False
        self.available = True
        self.created = False
        self.start_time = 0
        self.fake_maze = game.obstacles
        self.possible_tiiles = []

    def draw(self):
        if self.created == False:
            for tile in game.all_tiles:
                if tile not in game.occupied_levelstart_tiles:
                    self.possible_tiiles.append(tile)
            self.position = random.choice(self.possible_tiiles)
            game.occupied_levelstart_tiles.append(self.position)
            if self.position in game.endpoints:
                game.endpoints.remove(self.position)
            self.created = True
        if self.available:
            phasing.draw_tile(phasing.position, disign.powerup_img)

    def use(self):
        # das maze ohne obsatcles nachmalen
        for x, y in self.fake_maze:
            maze.draw_tile((x, y), disign.obstacle_img)
        # nach dem einsammeln des poweer ups values changen
        if self.active == False:
            self.start_time = pygame.time.get_ticks()
            self.fake_maze = game.obstacles
            game.obstacles = []
        # blöcke entfernten über die gelaufen wird
        if wyvern.position in self.fake_maze:
            self.fake_maze.remove(wyvern.position)
            x, y = wyvern.position
            if (x+1, y) in self.fake_maze:
                self.fake_maze.remove((x+1, y))
            if (x-1, y) in self.fake_maze:    
                self.fake_maze.remove((x-1, y))
            if (x, y+1) in self.fake_maze:
                self.fake_maze.remove((x, y+1))
            if (x, y-1) in self.fake_maze:
                self.fake_maze.remove((x, y-1))

        # nach 3 sekunden deaktivieren
        if pygame.time.get_ticks() > self.start_time + 3000:
            self.deactivate()
    
    def deactivate(self):
        if self.active:
            game.obstacles = self.fake_maze
            self.active = False
            self.position = (2, 0)

class PowerUp_Teleport(Tile):
    #WICHITG: jedes teleport phasing, das erstellt wird MUSS in de move methode von wyvern nach jeder bewegung freigeschaltet werden (teleport_jsut_used = False)
    def __init__(self):
        self.position_a = disign.teleport_buffer_location
        self.position_b = disign.teleport_buffer_location
        self.created = False
        self.teleport_just_used = False


    def draw(self):
        if self.created == False:
            self.position_a = random.choice(game.endpoints)
            game.endpoints.remove(self.position_a)
            self.position_b = random.choice(game.endpoints)
            game.endpoints.remove(self.position_b)
            game.occupied_levelstart_tiles.extend([self.position_a, self.position_b])
            self.created = True
        self.draw_tile(self.position_a, disign.teleport_img)
        self.draw_tile(self.position_b, disign.teleport_img)

        
    def use(self, wyvern_position): #wyvern_position wichtig um genauere frameperfect tps zu machen
        if self.teleport_just_used == False:
            if wyvern_position == self.position_a:
                wyvern.position = self.position_b
                self.teleport_just_used = True
            elif wyvern_position == self.position_b:
                wyvern.position = self.position_a
                self.teleport_just_used = True
        
class Bomb(Tile):
    def __init__(self):
        self.list = [] # alle koords von boombs
        self.created = False
        self.exploded = 0

    def draw(self):
        if self.created == False:
            self.list = []
            for endpoint in game.endpoints:
                if random.random() <= game.bomb_spawn_chance:
                    self.list.append(endpoint)
            self.created = True

        for bomb_location in self.list:
            self.draw_tile(bomb_location, disign.bomb_img)

    def explode(self, position):
        x, y = position
        explosions_richtungen = [(-1, -1), (0, -1), (1, -1), (1, 0), (1, 1), (0, 1), (-1, 1), (-1, 0)]
        for i in range(len(explosions_richtungen)):
            explosions_x, explosions_y = explosions_richtungen[i]
            obstacle_to_remove = (x + explosions_x, y + explosions_y)
            if phasing.active:
                if obstacle_to_remove in phasing.fake_maze:
                    phasing.fake_maze.remove(obstacle_to_remove)
            else:
                if obstacle_to_remove in game.obstacles:
                    game.obstacles.remove(obstacle_to_remove)
        self.exploded += 1
        self.list.remove(position)

class Wyvern(Tile):
    def __init__(self):
        self.position = disign.wyvern_buffer_location

    def check_collision(self, obstacles):
        # Kollisionsprüfung mit Hindernissen (z.B. Wandblöcke und Power Ups)
        for obstacle in obstacles:
            if self.position == obstacle:
                return True
        return False

    def move(self, direction):
        x, y = self.position
        outdated_position = self.position
    
        if direction == 'up':
            y = max(1, y - 1)
        elif direction == 'down':
            y = min(18, y + 1)
        elif direction == 'left':
            x = max(1, x - 1)
        elif direction == 'right':
            x = min(32, x + 1)
        self.position = (x, y)
        if self.check_collision(game.obstacles):
            self.position = outdated_position
        else: # wenn gemoved wird:
            if teleport.teleport_just_used:
                teleport.teleport_just_used = False

class End(Tile):
    def __init__(self):
        self.position = disign.end_buffer_location

class GUI(Tile):
    def __init__(self):
        self.space_for_hearts = [(1, 1), (2, 1), (3, 1)]
        self.space_for_timer = [(32, 1), (31, 1), (30, 1), (29, 1)]
        self.required_space = self.space_for_hearts + self.space_for_timer
        self.time_left = 0
        self.heart_timer = False
    
    def draw(self):
        self.hearts()
        self.timer()

    def hearts(self):
        for i in range(game.hearts):
            self.draw_tile(self.space_for_hearts[i], disign.heart_img)

    def timer(self):
        self.time_left = (game.timer - (pygame.time.get_ticks() - game.start_time)) // 1000
        if self.heart_timer:
            for i in range(len(str(self.time_left))):
                letze_zahl = (self.time_left // 10 ** i) % 10
                self.draw_tile(self.space_for_timer[i], disign.heart_numbers_list[letze_zahl])
        elif self.time_left < 5:
            for i in range(len(str(self.time_left))):
                letze_zahl = (self.time_left // 10 ** i) % 10
                self.draw_tile(self.space_for_timer[i], disign.heart_numbers_list[letze_zahl])
        else:
            for i in range(len(str(self.time_left))):
                letze_zahl = (self.time_left // 10 ** i) % 10
                self.draw_tile(self.space_for_timer[i], disign.numbers_list[letze_zahl])

        # Text-Position auf dem Bildschirm

class Start_End_Screen():
    def __init__(self):
        pygame.init()
        self.running = True
        self.startbutton = disign.startbutton_img.get_rect() 
        self.startbutton.center = (game.display.get_width() // 2, game.display.get_height() // 2 + 100)
        self.game_just_startet = True
        self.new_highscore = False
        self.in_homescreen_since = 0

    def run(self):
        while self.running:
            for event in pygame.event.get(): #event handler
                if event.type == pygame.QUIT:
                    self.running = False
                    pygame.quit()
                    sys.exit()
                if (pygame.time.get_ticks() - self.in_homescreen_since) > 1000 and (event.type == pygame.MOUSEBUTTONDOWN or event.type == pygame.KEYDOWN):
                    mouse_x, mouse_y = pygame.mouse.get_pos()
                    if self.startbutton.collidepoint(mouse_x, mouse_y): # start game:
                        self.running = False
                        game.running = True
                        self.game_just_startet = False
                        game.level_created = False
                        game.start_time = pygame.time.get_ticks()
                        game.stages_completed = 0
                        game.timer = 0
                        game.hearts = 3
                        if self.new_highscore:
                            game.highest_score = score
                            self.new_highscore = False
                        game.run()


            game.display.fill((0, 0, 0))
            if (pygame.time.get_ticks() - self.in_homescreen_since) > 1000:
                game.display.blit(disign.startbutton_img, self.startbutton)
            else:
                game.display.blit(disign.greystartbutton_img, self.startbutton)

            if self.game_just_startet == False:
                wx, wy = wyvern.position
                ex, ey = end.position
                ax = abs(wx - ex)
                ay = abs(wx - ey)
                xy = (ax + ay) // 2# max = 48
                prozenschlecht = xy / 24
                prozentvomlevel = 1 - prozenschlecht
                score = round((game.stages_completed-1 + prozentvomlevel + 0.1*bombs.exploded), 3)
                highscore_text = disign.highscore_font.render(f"Score: {score}", True, (255, 255, 255))
                text_rect = highscore_text.get_rect(center=(game.display.get_width() // 2, game.display.get_height() // 2 - 100))
                game.display.blit(highscore_text, text_rect)

                if score <= game.highest_score:
                    subscore_text = disign.subscore_font.render(f"REKORD: {game.highest_score}", True, (255, 255, 255))
                    text_rect = subscore_text.get_rect(center=(game.display.get_width() // 2, game.display.get_height() // 2 - 160))
                    game.display.blit(subscore_text, text_rect)
                else:
                    subscore_text = disign.subscore_font.render(f"NEUER REKORD!", True, (255, 255, 255))
                    text_rect = subscore_text.get_rect(center=(game.display.get_width() // 2, game.display.get_height() // 2 - 160))
                    game.display.blit(subscore_text, text_rect)
                    self.new_highscore = True

            pygame.display.update()

class Game():
    def __init__(self):
        pygame.init()
        pygame.display.set_caption('Wyvern Game')
        self.running = True
        self.level_created = False
        # display atributes
        self.window_width = 800
        self.window_height = 450
        self.display = pygame.display.set_mode((self.window_width, self.window_height))
        self.cell_size = 25
        # to use later
        self.start_time = 0
        self.clock = pygame.time.Clock()
        self.obstacles = [] # eigentlich maze
        self.all_tiles = [] 
        self.safe_tiles = [] # eigentlich zu tiles
        self.occupied_levelstart_tiles = []
        self.endpoints = [] # eigentlich sollte es aivailable_endpoints heißen
        self.timer = 0
        self.stages_completed = 0
        self.hearts = 0
        self.highest_score = 0
        self.variable_für_plus_sekudnen_text = False
        self.stage_started_since = 0

        # game balancing
        self.bomb_spawn_chance = 0.4
        self.timer_dict = [30000, 25000, 20000, 15000, 10000, 9000, 8000, 7000, 6000, 5000, 4000, 3000]
        self.lifeloss_timerecharge = 5000

        # berechnugnen
        for x in range(1, 33):
            for y in range(1, 19):
                self.all_tiles.append((x, y))
                
        for x in range (1, 17):
            for y in range(1, 10):
                self.safe_tiles.append((x*2, y*2))

    def prepare(self):
        maze.create()
        maze.reveal_path()
        self.level_created = True
        self.occupied_levelstart_tiles.append(phasing.position)
        phasing.available = True
        if self.stages_completed < len(self.timer_dict):
            self.timer += self.timer_dict[self.stages_completed]
            self.bonus_time = self.timer_dict[self.stages_completed]
        else:
            self.timer += self.timer_dict[-1]
            self.bonus_time = self.timer_dict[-1]

    def reset(self):
        # alles in der alten stage deaktivieren
        phasing.deactivate()
        # stage update
        self.stages_completed += 1
        phasing.created = False
        teleport.created = False
        bombs.created = False
        self.variable_für_plus_sekudnen_text = True
        self.stage_started_since = -1
        if gui.heart_timer:
            game.timer -= gui.time_left * 1000
            gui.heart_timer = False

        # new stage start
        maze.start_end_length = (0, 0), (0, 0), 0
        self.obstacles = [] # eigentlich maze
        self.occupied_levelstart_tiles = []
        self.endpoints = []

    def update_game(self):
        background.draw_tile((1, 1), disign.background_img)  # Zeichne den Hintergrund
        maze.draw(disign.obstacle_img)
        phasing.draw()
        teleport.draw()
        bombs.draw()
        if phasing.active:
            phasing.use()
            wyvern.draw_tile(wyvern.position, disign.wyvern_phasing_img)
        else:
            wyvern.draw_tile(wyvern.position, disign.wyvern_img)

        end.draw_tile(end.position, disign.end_img)

        gui.draw()
        #für dieses # ?? auf dem screen
        if self.stages_completed > 0 and (((pygame.time.get_ticks() - self.stage_started_since) < 3000) or (self.stage_started_since == -1)):
            text = disign.subscore_font.render(f"+ {self.bonus_time//1000}", True, (255, 255, 255))
            text_rect = text.get_rect(center=(game.display.get_width() // 2, game.display.get_height() // 2))
            game.display.blit(text, text_rect)
            if self.variable_für_plus_sekudnen_text:
                self.stage_started_since = pygame.time.get_ticks()
                self.variable_für_plus_sekudnen_text = False

    def run(self):
        while self.running: #event handler
            #stage complete
            if self.timer < (pygame.time.get_ticks() - self.start_time):
                self.hearts -= 1
                gui.heart_timer = True
                self.timer += self.lifeloss_timerecharge
                if self.hearts <= 0:
                    self.reset()
                    self.running = False
                    homescreen.in_homescreen_since = pygame.time.get_ticks()
                    homescreen.running = True
                    break
            #position checks
            if wyvern.position == end.position:
                game.reset()
                self.level_created = False
            elif wyvern.position == phasing.position and phasing.active == False:
                phasing.use()
                phasing.active = True
                phasing.available = False
            elif (wyvern.position == teleport.position_a or wyvern.position == teleport.position_b) and teleport.teleport_just_used == False:
                teleport.use(wyvern.position)
            elif wyvern.position in bombs.list:
                bombs.explode(wyvern.position)
            #eventts
            for event in pygame.event.get(): 
                if event.type == pygame.QUIT:
                    if homescreen.running != True:
                        pygame.quit()
                        sys.exit()
                #input checks
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_UP or event.key == pygame.K_w:
                        wyvern.move('up')
                    elif event.key == pygame.K_DOWN or event.key == pygame.K_s:
                        wyvern.move('down')
                    elif event.key == pygame.K_LEFT or event.key == pygame.K_a:
                        wyvern.move('left')
                    elif event.key == pygame.K_RIGHT or event.key == pygame.K_d:
                        wyvern.move('right')

                    

            #level create
            if self.level_created == False:
                self.prepare()
            


            self.update_game()
            self.clock.tick(60)
            pygame.display.update()

if __name__ == "__main__":
    game = Game()
    disign = Disign()
    gui = GUI()

    homescreen = Start_End_Screen()

    background = Background()
    maze = Maze()
    wyvern = Wyvern()
    end = End()
    phasing = PowerUp_Phasing()
    teleport = PowerUp_Teleport()
    bombs = Bomb()

    homescreen.run()
    game.run()
    
