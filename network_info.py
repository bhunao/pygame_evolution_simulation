from multiprocessing import connection
import pygame
from config import WHITE, BLACK, GREEN, RED, BLUE, SCREEN_WIDTH

SIZE = 15
BREAK_LINE_IN_PX = SIZE * 1.5

def draw_network(screen, cell):
    try:
        inputs = cell.config.genome_config.input_keys
        outputs = cell.config.genome_config.output_keys
        connections = cell.genome.connections
        net = cell.net
        pygame.draw.rect(screen,  "blue", cell.sprite, 3)
        # print("##############")
        # print(inputs)
        # print(outputs)
        # print(connections)
        # print("##############")

        x = SCREEN_WIDTH + 50
        y = 150

        color_list = []

        input_list = []

        for i, input in enumerate(inputs):
            adj = i * BREAK_LINE_IN_PX
            inp = pygame.Rect(x, y + adj, SIZE, SIZE)
            input_list.append(inp)
            pygame.draw.rect(screen, WHITE,
                            (x, y+adj, SIZE, SIZE),
                            border_radius=2)

        output_list = []
        x_out = x + 200
        y = 200
        for i, output in enumerate(outputs):
            adj = i * BREAK_LINE_IN_PX
            out = pygame.Rect(x_out, y + adj, SIZE, SIZE)
            output_list.append(out)

            activate = net.activate(cell.get_output())
            color = GREEN if activate[i] >= 0.5 else BLUE
            color_list.append(color)

            pygame.draw.rect(
                screen,
                color,
                (x_out, y+adj, SIZE, SIZE),
                border_radius=1
            )

        for i in range(len(inputs)):
            input = input_list[i]
            for j in range(len(outputs)):
                output = output_list[j]
                # pygame.draw.ine(
                #     screen,
                #     RED,
                #     start_pos=input.center,
                #     end_pos=output.center,
                #     width=1
                # )

        aa = [f"{cg.key} : {cg.enabled} : {cg.weight}\n" for cg in connections.values()]
        # print(f"connections.values():\n {aa}")
        activate = net.activate(cell.get_output())
        for cg in connections.values():
            a, b = cg.key
            enabled = cg.enabled
            weight = cg.weight
            abs_a = abs(a)
            abs_b = abs(b)
            if not weight >= .5:
                continue

            input = input_list[abs_a-1]
            output = output_list[abs_b-1]
            color = color_list[abs_b-1]

            pygame.draw.line(
                screen,
                color,
                start_pos=input.center,
                end_pos=output.center,
                width=int(max([1 + weight * 3, 1]))
            )
    except Exception as e:
        print(e)