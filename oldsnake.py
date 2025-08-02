import pygame, random

pygame.init()

#Font initialization
pygame.font.init()
font = pygame.font.SysFont("comicsansms", 25)

#Screen display settings
WIDTH = 600
HEIGHT = 650
screen = pygame.display.set_mode((WIDTH,HEIGHT))
pygame.display.set_caption("Snake Game")
background = pygame.image.load('background.png')
background = pygame.transform.scale(background, (600, 600))

#Apple image
apple_image = pygame.image.load('apple.png')
apple_image = pygame.transform.scale(apple_image, (35, 35))


#SnakeHeadImage
head_down = pygame.image.load('head_down.png')
head_down = pygame.transform.scale(head_down, (20, 20))
head_up = pygame.transform.rotate(head_down, 180)
head_right = pygame.transform.rotate(head_down, 90)
head_left = pygame.transform.rotate(head_down, -90)

#SnakeTailImage
tail_down = pygame.image.load('tail_down.png')
tail_down = pygame.transform.scale(tail_down, (20, 20))
tail_up = pygame.transform.rotate(tail_down, 180)
tail_right = pygame.transform.rotate(tail_down, -90)
tail_left = pygame.transform.rotate(tail_down, 90)

# Colors
BLACK = (0, 0, 0)
GREEN = (0, 255, 0)
RED = (255, 0, 0)
WHITE = (255, 255, 255)
BLUE = (102, 140, 255)

#Snake components
snake_head = pygame.Rect(300, 300, 20, 20)
snake = [snake_head, pygame.Rect(280, 300, 20, 20), pygame.Rect(260, 300, 20, 20)]
directCoord = (0, 0)


clock = pygame.time.Clock()
running = True

globalheadimage=head_right
globaltailimage=tail_right
def event_handler():
    global directCoord, running, globalheadimage, globaltailimage
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_DOWN:
                directCoord = (0, 20)
                globalheadimage = head_down
            elif event.key == pygame.K_UP:
                directCoord = (0, -20)
                globalheadimage = head_up
            elif event.key == pygame.K_RIGHT:
                directCoord = (20, 0)
                globalheadimage = head_right
            elif event.key == pygame.K_LEFT:
                directCoord = (-20, 0)
                globalheadimage = head_left



def newApple():
    x = random.randint(30, WIDTH - 30)
    y = random.randint(30, HEIGHT - 80)
    return pygame.Rect(x, y, 30, 30)

def foodCollisionHandler():
    global apple, foodCollision, score
    if snake_head.colliderect(apple):
        score+=1
        apple = newApple()
        foodCollision = True



score = 0
foodCollision = False
apple = newApple()
while running:
    
    
    
    event_handler()
    

    oldCoordinates = [(part.x, part.y) for part in snake]
    if directCoord != (0,0):
        snake[0].x += directCoord[0]
        snake[0].y += directCoord[1]
        for i in range(1, len(snake)):
            snake[i].x = oldCoordinates[i-1][0]
            snake[i].y = oldCoordinates[i-1][1]
    
    # snake_head.x += directCoord[0]
    # snake_head.y += directCoord[1]
    
    clock.tick(10)

    foodCollisionHandler()
    if foodCollision:
        last_x = oldCoordinates[-1][0]
        last_y = oldCoordinates[-1][1]
        snake.append(pygame.Rect(last_x, last_y, 20, 20))
        foodCollision = False

    if snake_head.x >= 600:
        snake_head.x = 0

    if snake_head.x < 0:
        snake_head.x = 600 


    if snake_head.y >= 600:
        snake_head.y = 0
        
    if snake_head.y < 0:
        snake_head.y = 580 
        

    for part in snake[1:]:
        if snake_head.colliderect(part):
            running = False
        
    
    # Determine tail direction
    tail = snake[-1]
    pre_tail = snake[-2]

    if tail.x < pre_tail.x:
        globaltailimage = tail_right
    elif tail.x > pre_tail.x:
        globaltailimage = tail_left
    elif tail.y < pre_tail.y:
        globaltailimage = tail_down
    elif tail.y > pre_tail.y:
        globaltailimage = tail_up

    # Black surface and draw the snake head
    screen.fill((BLACK))
    screen.blit(background, (0, 0))


    screen.blit(globalheadimage, (snake_head.x, snake_head.y))
    screen.blit(globaltailimage, (snake[-1].x, snake[-1].y))
    for part in snake[1:-1]:
        pygame.draw.rect(screen, BLUE, part)

    # pygame.draw.rect(screen, GREEN, snake_head) --- might use these later
    # pygame.draw.rect(screen, RED, apple)
    screen.blit(apple_image, (apple.x, apple.y))

    score_text = font.render(f"Score: {score}", True, (255, 255, 255)) 
    score_rect = score_text.get_rect(center=(300, 625))
    screen.blit(score_text, score_rect)

    pygame.display.update()

pygame.quit()