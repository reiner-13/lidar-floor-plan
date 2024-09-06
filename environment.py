import math
import pygame

class BuildEnvironment:
    def __init__(self, map_dim : list[int]):
        pygame.init()
        pygame.font.init()

        self.point_cloud = []
        self.external_map = pygame.image.load("map1.png")
        self.map_height, self.map_width = map_dim

        pygame.display.set_caption("Simulated Lidar - SLAM")
        self.map = pygame.display.set_mode((self.map_width, self.map_height))
        self.map.blit(self.external_map, (0,0))
        self.font1 = pygame.font.SysFont("Courier", 25)
        self.debug_text_surf = self.font1.render(str(len(self.point_cloud)), False, (255,255,255))
    
    def angle_data_to_position(self, distance, angle, position):
        x = distance * math.cos(angle) + position[0]
        y = -distance * math.sin(angle) + position[1]
        return (int(x), int(y))
    
    def data_storage(self, data):
        print(len(self.point_cloud))
        for element in data:
            point = self.angle_data_to_position(element[0], element[1], element[2])
            if point not in self.point_cloud:
                self.point_cloud.append(point)

    def show_sensor_data(self):
        self.info_map = self.map.copy()
        for point in self.point_cloud:
            self.info_map.set_at((int(point[0]), int(point[1])), (255,0,0))