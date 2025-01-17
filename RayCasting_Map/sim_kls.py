from importlib.resources import path
from tarfile import PAX_FIELDS
import pygame
import numpy as np
import numpy.linalg as la
from util import CI_COLORS
import random
from tcod import path



class Map:
    def __init__(self, shape: tuple[int, int], cell_size: int, statusbar_height: int) -> None: #TODO: Hier Screen ergänzen konstruktor und gridsize 
        self.max_x, self.max_y = shape
        self.statusbar_height=statusbar_height
        self.cell_size = cell_size
        self.cells = np.loadtxt("store.csv", delimiter=",").astype("int").T
        self.rects = np.empty(self.max_x*self.max_y, dtype=pygame.Rect).reshape(shape)
        
        # init rects
        for x in range(self.max_x):
            for y in range(self.max_y):
                left = x * cell_size + 1
                top = y * cell_size
                self.rects[x,y] = pygame.Rect(left, top, cell_size - 1, cell_size - 1)
        
        self.cell_type_dict = { "blocked"       : 0,
                                "free"          : 1,
                                "start"         : -999,
                                "end"           : -998,
                                "sample_path"   : -997} # path wieder löschen!!!


    # setters

    def set_cell(self, cell_coord: tuple[int, int], cell_type: str) -> None:
        if cell_coord is not None:
            x, y = cell_coord
            self.cells[x, y] = self.cell_type_dict.get(cell_type)
            print(cell_type, self.cell_type_dict.get(cell_type), self.cells[x, y])
    
    def set_cell_from_mouse(self, cell_type: str) -> None:
        cell_coord = self.mouse_to_cell()
        self.set_cell(cell_coord=cell_coord, cell_type=cell_type)
    
    # getters

    def get_cells_from_type(self, cell_type:str) -> list[tuple[int, int]]:
        y_index, x_index = np.where(self.cells == self.cell_type_dict[cell_type])
        return list(zip(y_index, x_index))
    
    def get_blocked_cells(self):
        blocked_cells = self.cells.copy()
        blocked_cells[self.cells < 0] = 1
        return blocked_cells

    # converters and utils
    

    def mouse_to_cell(self) -> tuple[int, int]:
        """Converts mouse position as cell coordinates.

        Returns:
            tuple[int, int]: cell coordinates
            None: when out of draw_area
        """
        mouse_x, mouse_y = pygame.mouse.get_pos()
        cell_x = mouse_x // self.cell_size
        cell_y = (mouse_y - self.statusbar_height) // self.cell_size
        if cell_y >= 0:
            return cell_x, cell_y

    # drawing methods

    def draw_grid(self, screen: pygame.Surface):
        width, height = screen.get_size()
        v_points = np.linspace(0, height, self.max_y+1)
        h_points = np.linspace(0, width,  self.max_x+1)
        for v in v_points:
            pygame.draw.line(screen, CI_COLORS.GREY_LIGHT.value, (0, v), (width, v))
        for h in h_points:
            pygame.draw.line(screen, CI_COLORS.GREY_LIGHT.value, (h, 0), (h, height))
        # print(v_points)

    def draw_cells(self, screen: pygame.Surface):
        for x in range(self.max_x):
            for y in range(self.max_y):
                if self.cells[x, y] == 0:
                    pygame.draw.rect(surface=screen, color=CI_COLORS.BLACK.value, rect=self.rects[x, y])
                elif self.cells[x, y] == -999:
                    pygame.draw.rect(surface=screen, color=CI_COLORS.GREEN.value, rect=self.rects[x, y])
                elif self.cells[x, y] == -998:
                    pygame.draw.rect(surface=screen, color=CI_COLORS.RED.value, rect=self.rects[x, y])
                elif self.cells[x, y] == -997:
                    pygame.draw.rect(surface=screen, color=CI_COLORS.GREY_LIGHT.value, rect=self.rects[x, y])

    def draw(self, screen: pygame.Surface) -> None:
        self.draw_grid(screen=screen)
        self.draw_cells(screen=screen)


class Agent:
    def __init__(self, map: Map) -> None:
        self.pos = np.array((1.0, 1.0))
        self.color = CI_COLORS.BLUE_alpha.value
        self.radius = 10
        self.vel = np.array((1.0, 1.0))
        self.acc = np.array((0.0, 0.0))
        self.max_speed = 2
        self.max_force = 0.7
        self.cell_path = []
        self.px_path = []
        self.map = map
        self.shopping_list = []
        self.shopping_path = []
        self.EUCLIDEAN = [  # Approximate euclidean distance.
            [99, 70, 99],
            [70, 0, 70],
            [99, 70, 99],
        ]
        
        self.reset_graph()

    def reset_graph(self) -> None:
        self.graph = path.CustomGraph(self.map.cells.shape) # --> Wiederverwendung in weitere methode auslösen
        self.graph.add_edges(edge_map=self.EUCLIDEAN, cost=self.map.get_blocked_cells())
        self.graph.set_heuristic(cardinal=70, diagonal=99)

    def draw(self, screen) -> None:
        # pygame.draw.circle(screen, self.color, self.pos, self.radius)
        # pygame.draw.line(screen, CI_COLORS.GREEN.value, self.pos, self.pos + (self.vel * 10), width=3 )
        # pygame.draw.circle(screen, CI_COLORS.RED_DARK.value, self.pos, 1)
        if len(self.px_path) > 2:
            pygame.draw.lines(screen, color=CI_COLORS.BLUE_alpha.value, points=self.px_path, closed=False, width=1)
        # for 
        
    def calculate_random_shopping_trip(self, basket_size: int = 20, mode: str = "greedy") -> None:
        self.reset_graph()
        self.shopping_list = []
        self.shopping_path = []
        items = []
        s = random.choices(self.map.get_cells_from_type("start"), k=1)
        items = random.choices(self.map.get_cells_from_type("free") , k=basket_size)
        e = random.choices(self.map.get_cells_from_type("end")  , k=1)
        
        if mode == "chaotic":
            self.shopping_list = s + items + e
            for i in range(len(self.shopping_list) - 1):
                current_item = self.shopping_list[i]
                next_item = self.shopping_list[i+1]
                self.shopping_path.extend(self.calculate_cell_path(current_item, next_item))
        
        elif mode == "greedy":
            
            # vom start zum nächsten item der Shopping List
            pf = path.Pathfinder(self.graph)
            for root in items:
                pf.add_root(root)
            path_to_nearest_root = pf.path_from(s[0]).tolist()
            self.shopping_path.extend(path_to_nearest_root)

            # von item zum jeweils nächsten item
            while len(items) > 0 :
                next_item = tuple(self.shopping_path[-1])
                # print("next item", next_item)
                del pf
                pf = path.Pathfinder(self.graph)
                items.remove(next_item)
                for root in items:
                    pf.add_root(root)
                path_to_nearest_root = pf.path_from(next_item).tolist()
                self.shopping_path.extend(path_to_nearest_root)
                # print("path to nearest root", path_to_nearest_root)
            
            # vom letzten item zum ende
            del pf
            pf = path.Pathfinder(self.graph)
            pf.add_root(e[0])
            path_to_end = pf.path_from(tuple(self.shopping_path[-1])).tolist()
            self.shopping_path.extend(path_to_end)
            # print("path to nearest end", path_to_end)
        
    
    def calculate_cell_path(self, start_pos: tuple[int, int], end_pos: tuple[int, int]) -> list[tuple[int, int]]: # Abhängigkeit von map auflösen
        pf = path.Pathfinder(self.graph)
        pf.add_root(end_pos)
        path_list = pf.path_from(start_pos).tolist()
        del pf
        return path_list

    def set_path(self, shopping_path):
        self.cell_path = shopping_path.copy()
        self.px_path = [(self.map.rects[x, y].left + random.randint(0, self.map.cell_size), self.map.rects[x, y].top + random.randint(0, self.map.cell_size)) for x, y in self.cell_path]
        # print(self.cell_path)
        # print(self.px_path)
    
    def follow_path(self):
        if self.cell_path[0].is_within(self.pos) and len(self.cell_path) >= 2:
            self.cell_path.pop(0)
            self.px_path.pop(0)
        self.seek(self.px_path[0])
    def seek(self, target_pos: np.array) -> None:
        self.acc = (target_pos - self.pos) - self.vel
        self.update()
    
    def update(self) -> None:
        if np.linalg.norm(self.acc) > self.max_force: 
            self.acc = (self.acc / np.linalg.norm(self.acc)) * self.max_force
        self.vel += self.acc
        if np.linalg.norm(self.vel) > self.max_speed: 
            self.vel = (self.vel / np.linalg.norm(self.vel)) * self.max_speed
        self.pos += self.vel
        self.acc[0], self.acc[1] = 0.0, 0.0
        # hier raycasting
    
    def set_pos(self, pos: tuple[float]) -> None:
        self.pos = pos