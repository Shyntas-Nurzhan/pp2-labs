import pygame
import pygame.image
import pygame.math

pygame.init()
def blitRotate(surf, image, pos, originPos, angle):

    image_rect = image.get_rect(topleft = (pos[0] - originPos[0], pos[1]-originPos[1]))
    offset_center_to_pivot = pygame.math.Vector2(pos) - image_rect.center
    
    rotated_offset = offset_center_to_pivot.rotate(-angle)

    rotated_image_center = (pos[0] - rotated_offset.x, pos[1] - rotated_offset.y)

    rotated_image = pygame.transform.rotate(image, angle)
    rotated_image_rect = rotated_image.get_rect(center = rotated_image_center)

    surf.blit(rotated_image, rotated_image_rect)

screen = pygame.display.set_mode((800,600))

done = False
angle = 0
angle1 = 0
clock = pygame.time.Clock()
clock_image = pygame.image.load("clock.png")
min_hand = pygame.image.load("min_hand.png")
sec_hand = pygame.image.load("sec_hand.png")


w, h = sec_hand.get_size()
w1, h1 = min_hand.get_size()
while not done:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            done = True
    
    pos = (screen.get_width()/2, screen.get_height()/2)

    
    screen.fill((255,255,255))
    
    screen.blit(clock_image, (0,0))
    blitRotate(screen, sec_hand, pos, (w/2, h/2), angle)
    angle -= 1
    
    blitRotate(screen , min_hand, pos, (w1/2,h1/2), angle1)    
    angle1 -= 1/60
    pygame.display.flip()
    clock.tick(60)