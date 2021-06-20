import pygame
import assets
import random

class SnakeGame:

    def __init__(self):
        pygame.init()
        pygame.font.init()
        self.myfont = pygame.font.SysFont("Comic Sans MS", 30)
        self.px_size = 32
        self.board_size = (10,10)
        self.clock = pygame.time.Clock()
        self.dim = (self.px_size*self.board_size[0], self.px_size*self.board_size[1])
        self.screen = pygame.display.set_mode(self.dim)
        self.load_assets()

    def load_assets(self):

        self.assets_all = pygame.sprite.Group()
        self.assets_ui = pygame.sprite.Group()
        self.assets_sprites = pygame.sprite.Group()
        self.assets_bg = pygame.sprite.Group()
        self.assets_tiles = pygame.sprite.Group()
        self.assets_head = pygame.sprite.Group()
        self.assets_snake = pygame.sprite.Group()
        
        self.asset_layers = [
            self.assets_bg,
            self.assets_sprites,
            self.assets_ui,
        ]

        bg_raw = pygame.image.load("images/background_tile.png")
        background_scaled = pygame.transform.scale(bg_raw, (self.px_size, self.px_size))

        bg = assets.Background(background_scaled, self.board_size)
        bg.add(self.assets_bg, self.assets_all)

        tile_img_raw = pygame.image.load("images/snake.png")
        self.tile_img = pygame.transform.scale(tile_img_raw, (self.px_size, self.px_size))

        head_img_raw = pygame.image.load("images/snake.png")
        self.head_img = pygame.transform.scale(head_img_raw, (self.px_size, self.px_size))

        self.head = assets.Snake(self.head_img, self.px_size, self)
        self.head.add(self.assets_sprites, self.assets_head, self.assets_snake, self.assets_all)

        apple_img_raw = pygame.image.load("images/apple.png")
        self.apple_img = pygame.transform.scale(apple_img_raw, (self.px_size, self.px_size))
        self.apple = assets.Apple(self.apple_img, self.px_size)
        self.apple.add(self.assets_sprites, self.assets_all)
        self.__pos_apple(self.apple)

    def __pos_apple(self, apple):
        apple.set_pos(random.randrange(self.board_size[0]), random.randrange(self.board_size[1]))
        while(pygame.sprite.spritecollideany(apple, self.assets_snake)):
            apple.set_pos(random.randrange(self.board_size[0]), random.randrange(self.board_size[1]))
        


    def loop(self):
        self.running = True
        while True:
            self.__handle_events()
            
            if (self.running):
                self.update()
            self.draw()

            self.clock.tick(12)

    def update(self):
        for layer in self.asset_layers:
            layer.update()

        head = self.head
            
        self.tile = assets.SnakeTile(self.tile_img, head)
        self.tile.add(self.assets_sprites, self.assets_tiles, self.assets_snake)

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

        if (pygame.sprite.collide_rect(head, self.apple)):
            self.__pos_apple(self.apple)
            head.length += 1

        if (pygame.sprite.spritecollide(head, self.assets_tiles, False)):
            print("dead")
            self.running = False
            ts = self.myfont.render("text", False, (0,0,0))
            self.screen.blit(ts, (0,0))


        

        

    def draw(self):
        for layer in self.asset_layers:
            layer.draw(self.screen)

        pygame.display.update()

    def __handle_events(self):
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
            





if __name__ == "__main__":
    sg = SnakeGame()
    sg.loop()