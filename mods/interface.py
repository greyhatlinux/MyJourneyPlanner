import tkinter as tk
import tkinter.messagebox as tkmsg
import datetime as dt
import routemap
import time

from collections import namedtuple, deque

# inf = float('inf')
# Edge = namedtuple('Edge', ['start', 'end', 'cost'])
 
# class Graph():
#     def __init__(self, edges):
#         self.edges = [Edge(*edge) for edge in edges]
#         # print(dir(self.edges[0]))
#         self.vertices = {e.start for e in self.edges} | {e.end for e in self.edges}
 
#     def dijkstra(self, source, dest):
#         assert source in self.vertices
#         dist = {vertex: inf for vertex in self.vertices}
#         previous = {vertex: None for vertex in self.vertices}
#         dist[source] = 0
#         q = self.vertices.copy()
#         neighbours = {vertex: set() for vertex in self.vertices}
#         for start, end, cost in self.edges:
#             neighbours[start].add((end, cost))

 
#         while q:
#             u = min(q, key=lambda vertex: dist[vertex])
#             q.remove(u)
#             if dist[u] == inf or u == dest:
#                 break
#             for v, cost in neighbours[u]:
#                 alt = dist[u] + cost
#                 if alt < dist[v]:                                  # Relax (u,v,a)
#                     dist[v] = alt
#                     previous[v] = u
#         s, u = deque(), dest
#         while previous[u]:
#             s.appendleft(u)
#             u = previous[u]
#         s.appendleft(u)
#         return s

inf = float('inf')
Edge = namedtuple('Edge', 'start, end, cost')


def make_edge(start, end, cost=1):
  return Edge(start, end, cost)


class Graph:
    def __init__(self, edges):
        # let's check that the data is right
        wrong_edges = [i for i in edges if len(i) not in [2, 3]]
        if wrong_edges:
            raise ValueError('Wrong edges data: {}'.format(wrong_edges))

        self.edges = [make_edge(*edge) for edge in edges]

    @property
    def vertices(self):
        return set(
            sum(
                ([edge.start, edge.end] for edge in self.edges), []
            )
        )

    def get_node_pairs(self, n1, n2, both_ends=True):
        if both_ends:
            node_pairs = [[n1, n2], [n2, n1]]
        else:
            node_pairs = [[n1, n2]]
        return node_pairs

    def remove_edge(self, n1, n2, both_ends=True):
        node_pairs = self.get_node_pairs(n1, n2, both_ends)
        edges = self.edges[:]
        for edge in edges:
            if [edge.start, edge.end] in node_pairs:
                self.edges.remove(edge)

    def add_edge(self, n1, n2, cost=1, both_ends=True):
        node_pairs = self.get_node_pairs(n1, n2, both_ends)
        for edge in self.edges:
            if [edge.start, edge.end] in node_pairs:
                return ValueError('Edge {} {} already exists'.format(n1, n2))

        self.edges.append(Edge(start=n1, end=n2, cost=cost))
        if both_ends:
            self.edges.append(Edge(start=n2, end=n1, cost=cost))

    @property
    def neighbours(self):
        neighbours = {vertex: set() for vertex in self.vertices}
        for edge in self.edges:
            neighbours[edge.start].add((edge.end, edge.cost))

        return neighbours

    def dijkstra(self, source, dest):
        assert source in self.vertices, 'Such source node doesn\'t exist'
        distances = {vertex: inf for vertex in self.vertices}
        previous_vertices = {
            vertex: None for vertex in self.vertices
        }
        distances[source] = 0
        vertices = self.vertices.copy()

        while vertices:
            current_vertex = min(
                vertices, key=lambda vertex: distances[vertex])
            vertices.remove(current_vertex)
            if distances[current_vertex] == inf:
                break
            for neighbour, cost in self.neighbours[current_vertex]:
                alternative_route = distances[current_vertex] + cost
                if alternative_route < distances[neighbour]:
                    distances[neighbour] = alternative_route
                    previous_vertices[neighbour] = current_vertex

        path, current_vertex = deque(), dest
        while previous_vertices[current_vertex] is not None:
            path.appendleft(current_vertex)
            current_vertex = previous_vertices[current_vertex]
        if path:
            path.appendleft(current_vertex)
        return path

        

graph = Graph([("a", "b", 7),  ("a", "c", 9),  ("a", "f", 14), ("b", "c", 10),
               ("b", "d", 15), ("c", "d", 11), ("c", "f", 2),  ("d", "e", 6),
               ("e", "f", 9),("b", "a", 7),  ("c", "a", 9),  ("f", "a", 14), ("c", "b", 10),
               ("d", "b", 15), ("d", "c", 11), ("f", "c", 2),  ("e", "d", 6),
               ("f", "e", 9)])


def ui():
    root = tk.Tk()
    root.title("My Journey Planner")
    w = root.winfo_screenwidth()
    h = root.winfo_screenheight()
    root.geometry('%dx%d+%d+%d' % (w/2, h/2, w/4, h/4))


    curr_time = time.strftime('%H:%M:%S %p')
    clock_label = tk.Label(root, padx=20, text=curr_time, pady=10, bg="green", fg="black")
    clock_label.pack()

    def update_time():
        curr_time = time.strftime('%H:%M:%S %p')
        clock_label.config(text="Time Now: " + str(curr_time))
        clock_label.after(1000, update_time)


    def showStops():
        mychoice = tk.Tk()
        mychoice.title("My Stops")
        w = mychoice.winfo_screenwidth()
        h = mychoice.winfo_screenheight()
        mychoice.geometry('%dx%d+%d+%d' % (w/3, h/3, w/3, h/3))

        raw_results = graph.dijkstra(str(from_var.get()),str(to_var.get()))
        results = list(raw_results)
        all_stops = "Starting Station : "
        for stop in results:
            all_stops = all_stops + stop + " --> "

        all_stops = all_stops + " Reached destination"
        result = tk.Label(mychoice, text = all_stops, padx=20, bg="orange")
        stopage_btn = tk.Button(mychoice, text="Show my stopages", command=result.pack)
        stopage_btn.pack()


        mychoice_close_btn = tk.Button(mychoice, text="Close", command=mychoice.destroy)
        mychoice_close_btn.pack()

    def howToPopup():
        with open ("howto.txt", "r") as f:
            help_msg = f.read()
        tkmsg.showinfo(title="How to Guide is here!", message=help_msg)


    global from_var
    global to_var


    from_var = tk.StringVar()
    from_var.set("a")
    from_station = tk.OptionMenu(root, from_var, "a", "b", "c", "d", "e", "f")
    from_station.pack()
    from_label = tk.Label(root, text="From", pady=10).pack()

    to_var = tk.StringVar()
    to_var.set("b")
    to_station = tk.OptionMenu(root, to_var, "a", "b", "c", "d", "e", "f")
    to_station.pack()
    to_label = tk.Label(root, text="To", pady=10).pack()

    at_var = tk.Entry(root, width=10)
    at_var.pack()
    at_var.insert(0,"02:00")
    at_label = tk.Label(root, text="At", pady=10).pack()


    submit_btn = tk.Button(root, text="Submit", command=showStops)
    submit_btn.pack()

    howTo_btn = tk.Button(root, text="How to guide", pady=15, command=howToPopup)
    howTo_btn.pack()

    btn = tk.Button(root, text="Close", width=25, command=root.quit)
    btn.pack()

    update_time()
    root.mainloop()