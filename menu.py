from pygame import *

init()

size = (800, 600)

Arial_50 = font.SysFont('arial', 50)

class Menu:
    def __init__(self):
        self._option_surfaces = []
        






while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()



    pygame.display.update()
    clock.tick(50)
