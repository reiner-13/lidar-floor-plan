import environment
import sensor
import pygame

env = environment.BuildEnvironment((630, 840))
env.original_map = env.map.copy()
laser = sensor.LaserSensor(200, env.original_map, uncertainty=(0.5, 0.01))
env.map.fill((0,0,0))
env.info_map = env.map.copy()

running = True

while running:
    active_sensor = False

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if pygame.mouse.get_focused():
            active_sensor = True
        else:
            active_sensor = False
    
    if active_sensor:
        position = pygame.mouse.get_pos()
        laser.position = position
        sensor_data = laser.sense_obstacles()
        env.data_storage(sensor_data)
        env.show_sensor_data()
    env.map.blit(env.info_map, (0,0))
    pygame.display.update()


    pygame.display.update()

pygame.quit()
