import pygame

class Background(pygame.sprite.Sprite):

    def __init__(self, scaled_image_tile, board_dim):
        super().__init__()
        self.orig_img = scaled_image_tile
        self.update_board(board_dim)

    def update_board(self, board_dim):
        iw = self.orig_img.get_width()
        img = pygame.Surface((iw*board_dim[0], iw*board_dim[1]))
        for x in range(board_dim[0]):
            for y in range(board_dim[1]):
                img.blit(self.orig_img, (x*iw, y*iw))
        self.image = img
        self.rect = img.get_rect()

class Apple(pygame.sprite.Sprite):

    def __init__(self, img, px_size):
        super().__init__()
        self.image = img
        self.rect = img.get_rect()
        self.px_size = px_size
        self.offset = px_size/2
    
    def set_pos(self, x, y):
        self.rect.center = x*self.px_size+self.offset, y*self.px_size+self.offset


class Snake(pygame.sprite.Sprite):

    def __init__(self, img, px_size, snakegame):
        super().__init__()
        self.orig_img = img
        self.dir = 0
        self.image = img
        self.rect = img.get_rect()
        self.px_size = px_size
        self.snakegame = snakegame
        self.length = 3

    def update(self):
        pass

    def set_dir(self, dir):
        self.dir = dir
        self.image = pygame.transform.rotate(self.orig_img, dir*90)


class SnakeTile(pygame.sprite.Sprite):

    def __init__(self, img, head):
        super().__init__()
        self.head = head
        self.image = img
        self.rect = img.get_rect()
        self.rect.center = head.rect.center
        self.living = 0
    
    def update(self):
        self.living += 1
        if (self.living > self.head.length):
            self.kill()