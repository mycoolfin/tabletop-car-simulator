import pygame
from pygame.locals import *

msgHeader = "[DISPLAY]: "

DISPLAY_WIDTH = 1600
DISPLAY_HEIGHT = 1200

DEFAULT_MAP_PATH = "./resources/maps/autocars_default/map_default.png"

class Display():
    def __init__(self, map_image_path=None):
        self.background_image_path = DEFAULT_MAP_PATH
        if map_image_path:
            self.background_image_path = map_image_path
        pygame.init()
        self.screen = pygame.display.set_mode((DISPLAY_WIDTH, DISPLAY_HEIGHT), pygame.FULLSCREEN)
        self.background_image = self.loadBackground()
        self.font = pygame.font.SysFont('Arial', 30)
        print(msgHeader + "Initialisation complete.")

    # Load and scale background image.
    def loadBackground(self):
        try:
            background_image = pygame.image.load(self.background_image_path)
            scale_factor = DISPLAY_WIDTH / background_image.get_rect().size[0]
            background_image = pygame.transform.rotozoom(background_image, 0, scale_factor)
            return background_image
        except:
            print(msgHeader + "Could not load map image from path " + self.background_image_path + ". (Fatal)")
            exit()

    # Create image from raw world data.
    def createImage(self, worldData):
        self.screen.blit(self.background_image, (0,0))
        yOffset = 0
        for vehicle in worldData['vehicles']:
            try:
                scaler = 1.333333333
                pos = (int(vehicle.position[0]*scaler), DISPLAY_HEIGHT - int((vehicle.position[1]*scaler)))
                angle = vehicle.orientation
                #width, length = vehicle.dimensions
                #template = pygame.Surface((width,length))
                #template.fill((255,255,255))
                #template.set_colorkey((255,0,0))
                #img = pygame.transform.rotate(template, angle)
                #img_rect = img.get_rect(center=pos)
                #self.screen.blit(img, img_rect)
                text = self.font.render("Agent " + str(vehicle.owner.ID) + ": " + str(pos) + ", " + str(angle), True, (255,255,255))
                self.screen.blit(text, (50, yOffset))
                yOffset += 30
                marker = self.font.render(str(vehicle.owner.ID), True, (255,255,255))
                self.screen.blit(marker, pos)
            except Exception as e:
                pass

    def loadingScreen(self):
        self.screen.fill((255,255,255))
        text = self.font.render("Connecting to cars...", True, (0,0,0))
        self.screen.blit(text, (DISPLAY_WIDTH-300,DISPLAY_HEIGHT-300))
        pygame.display.flip()

    def handle_input(self):
        for event in pygame.event.get():
            if event.type == QUIT or (event.type == KEYDOWN and event.key == K_ESCAPE):
                pygame.quit()
                exit()

    # Update the world display.
    def update(self, worldData):
        self.handle_input()
        self.createImage(worldData)
        pygame.display.flip()

