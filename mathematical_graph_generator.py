import pygame
from easygui import enterbox
from os import environ as osEnviron

WIDTH = int(enterbox('','Please input the width below.',strip=True))
EQUATIONS = enterbox('Seperate by comma and space, e.g: \'y=1x, y=2x\'','Please input the equations below.',strip=True).split(', ')
# Initialize Pygame
pygame.init()
HEIGHT = 0
MAX_WIDTH = pygame.display.Info().current_w - 200
MAX_HEIGHT = pygame.display.Info().current_h - 200
osEnviron['SDL_VIDEO_CENTERED'] = '1'
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Mathematical Graph")
clock = pygame.time.Clock()

printed_errors = []
def run_equations(x: int):
    global printed_errors
    y_values = []
    for equation in EQUATIONS:
        equation = equation.replace('^', '**')
        if equation.split('=')[0] == 'iy':
            equation = equation.replace('x', str(WIDTH-x))
        elif equation.split('=')[0] == 'y':
            equation = equation.replace('x', str(x))
        equation = equation.replace('{', '(').replace('}', ')').replace('\\cdot','*')
        try:
            y = eval(equation.split('=')[1])
            if y == float('inf'):
                return 'inf'
            elif y == float('-inf'):
                y_values.append(0)
            elif y != y:
                y_values.append(0)
            else:
                y_values.append(y)
        except ZeroDivisionError:
            return 'inf'
        except:
            if not equation in printed_errors:
                print(f"Error evaluating equation: {equation}")
                printed_errors.append(equation)
                y_values.append(0)
    
    return int(max(y_values))

graph_data = []

# Run the simulation and collect data
for x in range(WIDTH):
    graph_data.append(run_equations(x))
for i,y in enumerate(graph_data):
    if y == 'inf':
        graph_data[i] = max([item for item in graph_data if item != 'inf'])
HEIGHT = max(graph_data)
screen = pygame.display.set_mode((WIDTH, HEIGHT))

def draw_graph():
    screen.fill((255, 255, 255))  # Clear screen with white
    # Draw the graph
    for x in range(WIDTH):
        pygame.draw.line(screen, (0, 0, 0), (x, HEIGHT-graph_data[x]), (x, HEIGHT), 1)

    pygame.display.flip()

draw_graph()
graph = screen.copy()
checkered_graph = pygame.Surface(graph.get_size(),pygame.SRCALPHA)
i = 0
ii = 0
for y in range(checkered_graph.get_height()):
    for x in range(checkered_graph.get_width()):
        color = None
        bc = (64,64,64,64)
        wc = (192,192,192,64)
        if i == 0:
            if ii == 0:
                color = wc
                ii = 1
            else:
                color = bc
                ii = 0
        else:
            if ii == 0:
                color = bc
                ii = 1
            else:
                color = wc
                ii = 0
        pygame.draw.line(checkered_graph,color,(x,y),(x,y),1)
    if i == 0:
        i = 1
    else:
        i = 0

new_size = (0,0)
scale = 0
mode = max(WIDTH,HEIGHT)
if mode == WIDTH:
    scale = max(MAX_WIDTH // WIDTH,1)
else:
    scale = max(MAX_HEIGHT // HEIGHT,1)
new_size = (scale*WIDTH,scale*HEIGHT)
screen = pygame.display.set_mode(new_size)
screen.blit(pygame.transform.scale(graph,new_size),(0,0))
screen.blit(pygame.transform.scale(checkered_graph,new_size),(0,0))

print(f'graph size: {len(graph_data)}x{max(graph_data)}')

# Main loop
running = True
while running:
    clock.tick(60)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_s:
                pygame.image.save(graph,f'images/curves/{enterbox('','Please input the curve name below.',strip=True)}.png')
            running = False
    pygame.display.flip()
pygame.quit()