import pygame
import assets
import random

class SnakeGame:
    """
    The main game. Hosts the game loop, initialization of everything etc.
    """

    def __init__(self):
        pygame.init()

        """
        Determines the size of each grid cell
        """
        self.px_size = 32

        """
        The size of the game board
        """
        self.board_size = (10,10)

        """
        The game clock, used to normalize the speed the game is running on
        """
        self.clock = pygame.time.Clock()

        """
        The overall window dimensions (board size * cell size)
        """
        self.dim = (self.px_size*self.board_size[0], self.px_size*self.board_size[1])

        #creating the main window
        self.screen = pygame.display.set_mode(self.dim)

        #load all required assets
        self.load_assets()

    def load_assets(self):
        """
        Loads all required assets and puts them into categories
        (I currently don't know how the buildin layer system works, but may use them in the future, though not for this project)
        """

        """
        Creating all layers and other groups of sprites
        """
        self.assets_all = pygame.sprite.Group()
        self.assets_ui = pygame.sprite.Group()
        self.assets_sprites = pygame.sprite.Group()
        self.assets_bg = pygame.sprite.Group()
        self.assets_tiles = pygame.sprite.Group()
        self.assets_head = pygame.sprite.Group()
        self.assets_snake = pygame.sprite.Group()
        
        """
        ordering all layers, in which the sprites are getting painted in
        """
        self.asset_layers = [
            self.assets_bg,
            self.assets_sprites,
            self.assets_ui,
        ]

        #Loading the background and creating it
        bg_raw = pygame.image.load("images/background_tile.png")
        background_scaled = pygame.transform.scale(bg_raw, (self.px_size, self.px_size))

        bg = assets.Background(background_scaled, self.board_size)
        bg.add(self.assets_bg, self.assets_all)

        #creation of the snake tiles
        tile_img_raw = pygame.image.load("images/snake.png")
        self.tile_img = pygame.transform.scale(tile_img_raw, (self.px_size, self.px_size))

        #creating the snake head
        head_img_raw = pygame.image.load("images/snake.png")
        self.head_img = pygame.transform.scale(head_img_raw, (self.px_size, self.px_size))

        self.head = assets.Snake(self.head_img, self.px_size, self)
        self.head.add(self.assets_sprites, self.assets_head, self.assets_snake, self.assets_all)

        #creating the apple
        apple_img_raw = pygame.image.load("images/apple.png")
        self.apple_img = pygame.transform.scale(apple_img_raw, (self.px_size, self.px_size))
        self.apple = assets.Apple(self.apple_img, self.px_size)
        self.apple.add(self.assets_sprites, self.assets_all)
        #initially positioning the apple on the game board
        self.__pos_apple(self.apple)

    def __pos_apple(self, apple):
        """
        putting the apple on the map at a random position where none of the snake is
        !!!may result in an infite loop when the game is won (board is full)!!!
        """
        apple.set_pos(random.randrange(self.board_size[0]), random.randrange(self.board_size[1]))
        while(pygame.sprite.spritecollideany(apple, self.assets_snake)):
            apple.set_pos(random.randrange(self.board_size[0]), random.randrange(self.board_size[1]))
        


    def loop(self):
        """
        The main game loop. 
        Ticking mode is wait (ticks will be fully processed and then the next tick starts even when taking too long)
        """
        self.running = True
        while True:
            self.__handle_events()
            
            if (self.running):
                self.update()
            self.draw()

            self.clock.tick(12)

    def update(self):
        """
        the main processing of the ticks, where all assets are updated.
        """

        #updating each layer, for sprite internal processing
        for layer in self.asset_layers:
            layer.update()

        #updating snake head
        head = self.head
            
        #creating a new tile at the current head position
        self.tile = assets.SnakeTile(self.tile_img, head)
        self.tile.add(self.assets_sprites, self.assets_tiles, self.assets_snake)

        #moving the snake head
        dx = 0
        dy = 0
        if (head.dir == 0):
            dx += self.px_size
        elif (head.dir == 1):
            dy += self.px_size
        elif (head.dir == 2):
            dx -= self.px_size
        elif (head.dir == 3):
            dy -= self.px_size

        head.rect.center = (head.rect.center[0]+dx)%self.dim[0], (head.rect.center[1]+dy)%self.dim[1]

        #checking if one ate an apple
        if (pygame.sprite.collide_rect(head, self.apple)):
            self.__pos_apple(self.apple)
            head.length += 1

        #checking if one lost.
        if (pygame.sprite.spritecollide(head, self.assets_tiles, False)):
            print("dead")
            self.running = False
            ts = self.myfont.render("text", False, (0,0,0))
            self.screen.blit(ts, (0,0))

    def draw(self):
        """
        Drawing all assets onto the screen
        """
        #drawing each layer in order, so that background is in the back and ui in front
        for layer in self.asset_layers:
            layer.draw(self.screen)

        pygame.display.update()

    def __handle_events(self):
        """
        Handles all pygame events like quit and key presses etc
        """
        new_dir = None
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                self.running = False
            
            if event.type == pygame.KEYDOWN:

                if (new_dir == None):
                    if (event.key == pygame.K_d):
                        if (self.head.dir != 2):
                            new_dir = 0
                    elif (event.key == pygame.K_s):
                        if (self.head.dir != 3):
                            new_dir = 1
                    elif (event.key == pygame.K_a):
                        if (self.head.dir != 0):
                            new_dir = 2
                    elif (event.key == pygame.K_w):
                        if (self.head.dir != 1):
                            new_dir = 3
                    if (new_dir != None):
                        self.head.set_dir(new_dir)
            
"""
executed if this is the main module, starts the game.
"""
if __name__ == "__main__":
    sg = SnakeGame()
    sg.loop()