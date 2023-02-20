from time import sleep
import pygame
from scipy.__config__ import show
from scipy.fftpack import ss_diff

# defining path for buttons
visualize_buttonPath = 'C:/Users/Abdul/Desktop/programs/ai lab/DFS-Visualizer/Sources/visualize_button.png'
clear_buttonPath = 'C:/Users/Abdul/Desktop/programs/ai lab/DFS-Visualizer/Sources/clear_button.png'

pygame.font.init()
myfont = pygame.font.SysFont('Futura Medium', 30)
myfont2 = pygame.font.SysFont('Futura Medium', 30)

# gameloop variable
run = True

# colours
white = (255, 255, 255)
black = (0, 0, 0)

# screen setup
screen = pygame.display.set_mode((800, 600))
screen_width, screen_height = pygame.display.get_surface().get_size()

# list of all vertices
vertices = []

# circle radius
circles_radius = 20
# vertex currently held by user used to make edges
held_vertix = -1

# list of visited vertices
visited = []
# list of unvisited vertices
stack = []

# visualisation activation variable
visualize_start = False
# no of iterations
iterations = 0

# loading buttons
visualize_button = pygame.image.load(visualize_buttonPath).convert_alpha()
visualize_button = pygame.transform.scale(visualize_button, (115, 34))

clear_button = pygame.image.load(clear_buttonPath).convert_alpha()
clear_button = pygame.transform.scale(clear_button, (79, 34))


def show_current():
    for vertix in vertices:
        print("vertix number: ", str(vertix.number),
              " has ")
        for x in vertix.adjacent_vertices:
            print(x, " ")
        print("/n")


def draw_vertices():
    for vertex in vertices:
        for adjacent_vertix in vertex.adjacent_vertices:
            pygame.draw.line(screen, black, vertex.position,vertices[adjacent_vertix].position)
    for vertix in vertices:
        if held_vertix == vertix.number:
            pygame.draw.circle(screen, (255, 0, 0),
                               vertix.position, circles_radius, 0)
            textsurface = myfont.render(str(vertix.number), False, (255, 255, 255))
            screen.blit(
                textsurface, (vertix.position[0]-textsurface.get_width()/2, vertix.position[1]-textsurface.get_height()/2))
        else:
            pygame.draw.circle(
                screen, white, vertix.position, circles_radius, 0)
            pygame.draw.circle(
                screen, black, vertix.position, circles_radius, 1)
            textsurface = myfont.render(str(vertix.number), False, (0, 0, 0))
            screen.blit(
                textsurface, (vertix.position[0]-textsurface.get_width()/2, vertix.position[1]-textsurface.get_height()/2))
        if visualize_start:
            visited_text = myfont2.render(
                "Visited: " + str(", ".join(str(x) for x in visited)), False, (0, 0, 0))
            stack_text = myfont2.render(
                "Stacked: " + str(", ".join(str(x) for x in stack)), False, (0, 0, 0))
            iterations_text = myfont2.render(
                "Iterations: " + str(iterations), False, (0, 0, 0))
            screen.blit(iterations_text, (650, 570 -
                        iterations_text.get_height()/2))
            screen.blit(
                visited_text, (screen_width/2 - 250, 520-visited_text.get_height()/2))
            screen.blit(
                stack_text, (screen_width/2 - 250, 570-stack_text.get_height()/2))

# draws the screen
def setup_screen():
    screen.fill((253, 246, 236))
    pygame.draw.rect(screen, (240, 165, 0), pygame.Rect((0, screen_height-115), (screen_width, 115)))
    screen.blit(clear_button, (13, 547))
    screen.blit(visualize_button, (13, 503))
    draw_vertices()

# checks if the used is trying to make vertices to close
def vertix_in_radius(position, times_radius):
    x = 0
    for vertix in vertices:
        x_diff = abs(vertix.position[0]-position[0])
        y_diff = abs(vertix.position[1]-position[1])
        if (x_diff**2+y_diff**2)**0.5 < circles_radius*times_radius:
            return x
        x += 1
    x = -1
    return x


def clean_stack(stack, visited):
    new_stack = stack
    temp_stack = []
    for x in new_stack:
        found = False
        for b in temp_stack:
            if b == x:
                found = True
        for v in visited:
            if v == x:
                found = True
        if not found:
            temp_stack.append(x)
    return temp_stack

# implements the algorithm
def visualize():
    global visualize_start, visited, stack, iterations
    iterations = 1
    visualize_start = True
    # held vertex, vertex currently being highlighted #local
    held_vertix = 0

    # put 0 in visited list, start from 0, initialise the visited list
    visited = [0]
    working = True

    # put adjacent vertices of the held vertices in stack
    stack = stack + vertices[held_vertix].adjacent_vertices
    
    # clean_stack removes already visited nodes
    stack = clean_stack(stack, visited)
    
    # refreshing the screen
    setup_screen()

    # highlighting held vertex
    vertix = vertices[held_vertix]
    pygame.draw.circle(screen, (255, 0, 0),vertix.position, circles_radius, 0)
    textsurface = myfont.render(str(vertix.number), False, (255, 255, 255))
    screen.blit(textsurface, (vertix.position[0]-textsurface.get_width()/2, vertix.position[1]-textsurface.get_height()/2))

    pygame.display.flip()
    sleep(1)

    # printing
    print("Visiting: ")
    for v in visited:
        print(" ", v)
    print("\nStack: ")
    for s in stack:
        print(" ", s)

    # all nodes exhausted
    if len(visited) == len(vertices):
        working = False
    
    # while nodes are left, and no of nodes greater than 0
    while not len(stack) == 0 and working:
        # increase the number of iterations
        iterations += 1
        
        # pop the held vertex from stack
        held_vertix = stack.pop(0)
        # append the held vertex to visited
        visited.append(held_vertix)
        # refresh the screen
        setup_screen()

        # highlight the held vertex
        vertix = vertices[held_vertix]
        pygame.draw.circle(screen, (255, 0, 0),vertix.position, circles_radius, 0)
        textsurface = myfont.render(str(vertix.number), False, (255, 255, 255))
        screen.blit(textsurface, (vertix.position[0]-textsurface.get_width()/2, vertix.position[1]-textsurface.get_height()/2))

        pygame.display.flip()
        sleep(1)

        # stack = stack + vertices[held_vertix].adjacent_vertices
        # stack = clean_stack(stack, visited)
        
        # add the adjacent vertices of the held vertex to front of stack
        stack = vertices[held_vertix].adjacent_vertices + stack
        stack = clean_stack(stack, visited)


        # printing
        print("Visiting: ")
        for v in visited:
            print(" ", v)
        print("\nStack: ")
        for s in stack:
            print(" ", s)

        # all nodes exhausted
        if len(visited) == len(vertices):
            working = False

        # loop ends
        
    print("Number of iterations: ", str(iterations))

# defines the properties of vertex
class vertix:

    def __init__(self, position):
        self.position = position
        self.number = len(vertices)
        self.adjacent_vertices = []
        vertices.append(self)
        print(str(len(self.adjacent_vertices)))

    def add_vertix(self, vertix):
        x = True
        for adjacent_vertix in self.adjacent_vertices:
            if adjacent_vertix == vertix:
                x = False
        if x:
            self.adjacent_vertices.append(vertix)

# game loop
while run:
    # Setting up white background
    setup_screen()
    
    for e in pygame.event.get():
        # check if user quitted
        if e.type == pygame.QUIT:
            raise StopIteration
        if e.type == pygame.KEYDOWN:
            if e.key == pygame.K_q:
                run = False

        # if clear button is pressed
        if e.type == pygame.MOUSEBUTTONDOWN and pygame.Rect((13, 547), (79, 34)).collidepoint(e.pos):
            vertices = []
            iterations = 0
            visited = []
            stack = []
            held_vertix = -1
            pygame.display.flip()

        # if visualise button is pressed
        if e.type == pygame.MOUSEBUTTONDOWN and pygame.Rect((13, 503), (115, 34)).collidepoint(e.pos):
            visited = []
            stack = []
            visualize()

        # Creating a new vertix once you click on screen
        if e.type == pygame.MOUSEBUTTONDOWN and e.pos[1] < screen_height-135 and vertix_in_radius(e.pos, 3) == -1:
            vertix(e.pos)
            held_vertix = -1
            pygame.draw.circle(screen, black, e.pos, circles_radius, 1)
        
        # user has not pressed anything
        else:
            if e.type == pygame.MOUSEBUTTONDOWN and not vertix_in_radius(e.pos, 1) == -1:

                if held_vertix == -1:
                    held_vertix = vertices[vertix_in_radius(e.pos, 1)].number
                else:
                    if held_vertix == vertices[vertix_in_radius(e.pos, 1)].number:
                        held_vertix = -1
                    else:
                        vertices[held_vertix].add_vertix(
                            vertices[vertix_in_radius(e.pos, 1)].number)
                        vertices[vertices[vertix_in_radius(e.pos, 1)].number].add_vertix(
                            held_vertix)
                        print("connected ", held_vertix, " with ",
                              vertices[vertix_in_radius(e.pos, 1)].number)
                        held_vertix = -1
                        show_current()

    pygame.display.flip()