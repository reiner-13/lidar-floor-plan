import pygame
import math
import numpy as np


def add_uncertainty(distance, angle, sigma):
    mean = np.array([distance, angle])
    covariance = np.diag(sigma**2)
    distance, angle = np.random.multivariate_normal(mean, covariance)

    distance = max(0, distance)
    angle = max(0, angle)
    return [distance, angle]

class LaserSensor:

    def __init__(self, range, map, uncertainty):
        self.range = range
        self.map = map
        self.sigma = np.array([uncertainty[0], uncertainty[1]])
        self.position = (0,0)
        self.speed = 4  # rounds per second
        self.width, self.height = pygame.display.get_surface().get_size()
        self.sensed_points = []
        self.sample_count = 60

    def get_distance(self, point):
        dx = (point[0] - self.position[0])**2
        dy = (point[1] - self.position[1])**2
        return math.sqrt(dx+dy)

    def sense_obstacles(self):
        data = []
        x1, y1 = self.position[0], self.position[1]

        for angle in np.linspace(0, 2*math.pi, self.sample_count, False):
            x2 = x1 + self.range * math.cos(angle)
            y2 = y1 - self.range * math.sin(angle)
            
            for i in range(0, 100):  # 100 is number of samples within line segment
                u = i / 100
                x = int(x2 * u + x1 * (1 - u))
                y = int(y2 * u + y1 * (1 - u))
                
                if 0 < x < self.width and 0 < y < self.height:
                    color = self.map.get_at((x, y))
                    if (color[0], color[1], color[2]) == (0,0,0):
                        distance = self.get_distance((x, y))
                        output = add_uncertainty(distance, angle, self.sigma)
                        output.append(self.position)

                        # store the measurements
                        data.append(output)
                        break
        if len(data) > 0:
            return data
        return False