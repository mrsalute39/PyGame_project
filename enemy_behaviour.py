from collections import deque

# алгоритм передвижения противника по карте


class PathFinding:
    def __init__(self, game):
        self.game = game
        self.map = game.map.layout
        self.ways = [-1, 0], [0, -1], [1, 0], [0, 1], [-1, -1], [1, -1], [1, 1], [-1, 1]
        self.graph = {}
        self.get_graph()

    def b_f_s(self, start, goal, graph):  # -- > алгоритм поиска в ширину (breadth first search)
        q = deque([start])
        visited = {start: None}

        while q:
            cur_node = q.popleft()
            if cur_node == goal:
                break
            next_nodes = graph[cur_node]

            for next_node in next_nodes:
                if next_node not in visited and next_node not in self.game.creator.enemy_positions:
                    q.append(next_node)
                    visited[next_node] = cur_node
        return visited

    def get_path(self, start, goal):
        self.visited = self.b_f_s(start, goal, self.graph)
        path = [goal]
        step = self.visited.get(goal, start)

        while step and step != start:
            path.append(step)
            step = self.visited[step]
        return path[-1]

    def get_graph(self):
        for y, row in enumerate(self.map):
            for x, col in enumerate(row):
                if not col:
                    self.graph[(x, y)] = self.graph.get((x, y), []) + self.get_next_nodes(x, y)

    def get_next_nodes(self, x, y):
        return [(x + dx, y + dy) for dx, dy in self.ways if (x + dx, y + dy) not in self.game.map.wmap]
