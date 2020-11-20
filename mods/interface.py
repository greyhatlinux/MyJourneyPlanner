import tkinter as tk
import tkinter.messagebox as tkmsg
import datetime as dt
import routemap
import time

from collections import namedtuple, deque


inf = float('inf')
Edge = namedtuple('Edge', 'start, end, cost')


def make_edge(start, end, cost=1):
  return Edge(start, end, cost)


class Network:
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
        assert source in self.vertices, 'Such point does not exist in the map'
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

        global from_src
        global to_dest

        from_src = tk.StringVar()
        to_dest = tk.StringVar()

        from_text = tk.Label(mychoice, text="Starting Point").pack()
        from_src = tk.Entry(mychoice,width=50, bd=5, fg="black")
        from_src.pack()

        to_text = tk.Label(mychoice, text="Final Point").pack()
        to_dest = tk.Entry(mychoice, text="From",width=50, bd=5)
        to_dest.pack()

        def direction():
            try:
                raw_results = graph.dijkstra(str(from_src.get()),str(to_dest.get()))
                results = list(raw_results)
                all_stops = "Starting Station : "
                for stop in results:
                    all_stops = all_stops + stop + " --> "

                all_stops = all_stops + " Reached destination"
                result = tk.Label(mychoice, text = all_stops, padx=20, bg="orange")
                result.pack()
            except:
                result = tk.Label(mychoice, text = "Check input values, no such path/stations", padx=20, bg="orange")
                result.pack()

        stopage_btn = tk.Button(mychoice, text="Show my stopages", command=direction)
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
    from_var.set("Bakerloo")
    from_line = tk.OptionMenu(root, from_var, "Bakerloo",
                                                    "Central",
                                                    "Circle",
                                                    "District",
                                                    "Hammersmith & City",
                                                    "Jubilee",
                                                    "Metropolitan",
                                                    "Northern",
                                                    "Piccadilly",
                                                    "Victoria",
                                                    "Waterloo & City")


    from_line.pack()
    from_label = tk.Label(root, text="From", pady=10).pack()

    to_var = tk.StringVar()
    to_var.set("Central")
    to_line = tk.OptionMenu(root, to_var, "Bakerloo",
                                                    "Central",
                                                    "Circle",
                                                    "District",
                                                    "Hammersmith & City",
                                                    "Jubilee",
                                                    "Metropolitan",
                                                    "Northern",
                                                    "Piccadilly",
                                                    "Victoria",
                                                    "Waterloo & City")
    to_line.pack()
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


graph = Network([("Harrow & Wealdstone","Kenton", 2),
("Kenton","South Kenton",	2),
("South Kenton","North Wembley",	2),
("North Wembley","Wembley Central",	2),
("Wembley Central","Stonebridge Park",	2),
("Stonebridge Park","Harlesden",	2),
("Harlesden","Willesden Junction",	2),
("Willesden Junction","Kensal Green",	3),
("Kensal Green","Queen's Park",	2),
("Queen's Park","Kilburn Park",	2),
("Kilburn Park","Maida Vale",	2),
("Maida Vale","Warwick Avenue",	1),
("Warwick Avenue","Paddington",	2),
("Paddington","Edgware Road",	2),
("Edgware Road","Marylebone",	1),
("Marylebone","Baker Street",	2),
("Baker Street","Regent's Park",	2),
("Regent's Park","Oxford Circus", 2),
("Oxford Circus","Piccadilly Circus", 2),
("Piccadilly Circus","Charing Cross", 2),
("Charing Cross","Embankment", 1),
("Embankment","Waterloo",	2),
("Waterloo","Lambeth North",	2),
("Lambeth North","Elephant & Castle",	3),
("Epping","Theydon Bois",	3),
("Theydon Bois","Debden",3),
("Debden","Loughton", 	2),
("Loughton","Buckhurst Hill",	3),
("Buckhurst Hill","Woodford", 2),
("Woodford","South Woodford",3),
("South Woodford","Snaresbrook", 	2),
("Snaresbrook","Leytonstone",	2),
("Roding Valley","Woodford",	4),
("Roding Valley","Chigwell",	3),
("Chigwell","Grange Hill",	2),
("Grange Hill","Hainault",	5),
("Hainault","Fairlop",	2),
("Fairlop","Barkingside",	2),
("Barkingside","Newbury Park",	2),
("Newbury Park","Gants Hill",	3),
("Gants Hill","Redbridge",	2),
("Redbridge","Wanstead",	2),
("Wanstead","Leytonstone",	2),
("Leytonstone","Leyton",	2),
("Leyton","Stratford",	3),
("Stratford","Mile End",	4),
("Mile End","Bethnal Green",	2),
("Bethnal Green","Liverpool Street",	3),
("Liverpool Street","Bank",	2),
("Bank","St. Paul's",	2),
("St. Paul's","Chancery Lane",	2),
("Chancery Lane","Holborn",	1),
("Holborn","Tottenham",	2),
("Tottenham","Oxford Circus",	1),
("Oxford Circus","Bond Street",	2),
("Bond Street","Marble Arch",	2),
("Marble Arch","Lancaster Gate",	3),
("Lancaster Gate","Queensway",	2),
("Queensway","Notting Hill Gate",	2),
("Notting Hill Gate","Holland Park", 1),
("Holland Park","Shepherd's Bush",	2),
("Shepherd's Bush","White City",	3),
("White City","East Acton",	3),
("East Acton","North Acton",	2),
("North Acton","West Acton",	2),
("West Acton","Ealing Broadway",	3),
("Hanger Lane","	Perivale",	3),
("Perivale","Greenford",	2),
("Greenford","Northolt",	2),
("Northolt","South Ruislip",	3),
("South Ruislip","Ruislip Gardens",	2),
("Ruislip Gardens","West Ruislip",	2),
("Edgware Road","Paddington",	3),
("Paddington","Bayswater",	2),
("Bayswater","Notting Hill Gate",	2),
("Notting Hill Gate","High Street Kensington",	2),
("High Street Kensington","Gloucester Road",	3),
("Gloucester Road","South Kensington",	3),
("South Kensington","Sloane Square",	2),
("Sloane Square","Victoria",	2),
("Victoria","St. James's Park",	2),
("St. James's Park","Westminster",	2),
("Westminster","Embankment",	1),
("Embankment","Temple",	2),
("Temple","Blackfriars",	1),
("Blackfriars","Mansion House",	2),
("Mansion House","Cannon Street",	2),
("Cannon Street","Monument",	1),
("Monument","Tower Hill",	2),
("Tower Hill","Aldgate",	2),
("Aldgate","Liverpool Street",	3),
("Liverpool Street","Moorgate",	2),
("Moorgate","Barbican",	2),
("Barbican","Farringdon",	1),
("Farringdon","King's Cross St. Pancras",	4),
("King's Cross St. Pancras","Euston Square",	2),
("Euston Square","Great Portland Street",	2),
("Great Portland Street","Baker Street",	2),
("Baker Street","Edgware Road", 	3),
("Paddington","Royal Oak", 	2),
("Royal Oak","Westbourne Park", 	2),
("Westbourne Park","Ladbroke Grove", 	2),
("Ladbroke Grove","Latimer Road", 	2),
("Latimer Road","Wood Lane",	2),
("Wood Lane","Shepherd's Bush Market", 	2),
("Shepherd's Bush Market","Goldhawk Road", 	1),
("Goldhawk Road","Hammersmith",	2),
("Upminster","Upminster Bridge",	2),
("Upminster Bridge","Hornchurch",	2),
("Hornchurch","Elm Park",	2),
("Elm Park","Dagenham East",	3),
("Dagenham East","Dagenham Heathway",	2),
("Dagenham Heathway","Becontree",	3),
("Becontree","Upney",	2),
("Upney","Barking",	3),
("Barking","East Ham",	4),
("East Ham","Upton Park",	2),
("Upton Park","Plaistow",	2),
("Plaistow","West Ham",	2),
("West Ham","Bromley-by-Bow",	2),
("Bromley-by-Bow","Bow Road",	2),
("Bow Road","Mile End",	2),
("Mile End","Stepney Green",	2),
("Stepney Green","Whitechapel",	3),
("Whitechapel","Aldgate East",	2),
("Aldgate East","Tower Hill",	3),
("Tower Hill","Monument",	2),
("Monument","Cannon Street",	1),
("Cannon Street","Mansion House",	2),
("Mansion House","Blackfriars",	2),
("Blackfriars","Temple",	1),
("Temple","Embankment",	2),
("Embankment","Westminster",	1),
("Westminster","St. James's Park",	2),
("St. James's Park","Victoria",	2),
("Victoria","Sloane Square",	2),
("Sloane Square","South Kensington",	2),
("South Kensington","Gloucester Road",	3),
("Gloucester Road","Earl's Court",	2),
("Earl's Court","Kensington (Olympia)",	3),
("Earl's Court","High Street Kensington",	5),
("High Street Kensington","Notting Hill Gate",	2),
("Notting Hill Gate","Bayswater",	2),
("Bayswater","Paddington",	2),
("Paddington","Edgware Road",	3),
("Earl's Court","West Brompton",	2),
("West Brompton","Fulham Broadway",	2),
("Fulham Broadway","Parsons Green",	2),
("Parsons Green","Putney Bridge",	3),
("Putney Bridge","East Putney",	3),
("East Putney","Southfields",	2),
("Southfields","Wimbledon Park",	2),
("Wimbledon Park","Wimbledon",	4),
("Earl's Court","West Kensington",	2),
("West Kensington","Barons Court",	2),
("Barons Court","Hammersmith",	3),
("Hammersmith","Ravenscourt Park",	2),
("Ravenscourt Park","Stamford Brook",	2),
("Stamford Brook","Turnham Green",	1),
("Turnham Green","Gunnersbury",	3),
("Gunnersbury","Kew Gardens",	2),
("Kew Gardens","Richmond", 	4),
("Turnham Green","Chiswick Park",	2),
("Chiswick Park","Acton Town",	2),
("Acton Town","Ealing Common",	2),
("Ealing Common","Ealing Broadway",	5),
("Barking","East Ham",	4),
("East Ham","Upton Park",	2),
("Upton Park","Plaistow",	2),
("Plaistow","West Ham",	2),
("West Ham","Bromley-by-Bow",	2),
("Bromley-by-Bow","Bow Road",	2),
("Bow Road","Mile End",	2),
("Mile End","Stepney Green",	2),
("Stepney Green","Whitechapel",	3),
("Whitechapel","Aldgate East",	2),
("Aldgate East","Liverpool Street",	3),
("Liverpool Street","Moorgate",	2),
("Moorgate","Barbican",	2),
("Barbican","Farringdon",	1	),
("Farringdon","King's Cross St. Pancras",	4),
("King's Cross St. Pancras","Euston Square",	2),
("Euston Square","Great Portland Street",	2),
("Great Portland Street","Baker Street",	2),
("Baker Street","Edgware Road",	3),
("Edgware Road","Paddington",	3),
("Paddington","Royal Oak",	2),
("Royal Oak","Westbourne Park",	2),
("Westbourne Park","Ladbroke Grove",	2),
("Ladbroke Grove","Latimer Road",	2),
("Latimer Road","Wood Lane",	2),
("Wood Lane","Shepherd's Bush Market",	2),
("Shepherd's Bush Market","Goldhawk Road",	1),
("Goldhawk Road","Hammersmith",	2),
("Stanmore","Canons Park",	4),
("Canons Park","Queensbury",	3),
("Queensbury","Kingsbury",	2),
("Kingsbury","Wembley Park",	3),
("Wembley Park","Neasden",	4),
("Neasden","Dollis Hill",	2),
("Dollis Hill","Willesden Green",	2),
("Willesden Green","Kilburn",	2),
("Kilburn","West Hampstead",	2),
("West Hampstead","Finchley Road",	1),
("Finchley Road","Swiss Cottage",	2),
("Swiss Cottage","St. John's Wood",	2),
("St. John's Wood","Baker Street",	3),
("Baker Street","Bond Street",	2),
("Bond Street","Green Park",	2),
("Green Park","Westminster",	2),
("Westminster","Waterloo",2),
("Waterloo","Southwark",	2),
("Southwark","London Bridge",2),
("London Bridge","Bermondsey",2),
("Bermondsey","Canada Water",2),
("Canada Water","Canary Wharf",3),
("Canary Wharf","North Greenwich",3),
("North Greenwich","Canning Town",3),
("Canning Town","West Ham",	3),
("West Ham","Stratford",	2),
("Amersham","Chalfont & Latimer",	4),
("Chesham","Chalfont & Latimer",	9),
("Chalfont & Latimer","Chorleywood",	4),
("Chorleywood","Rickmansworth",4),
("Rickmansworth","Moor Park",	5),
("Watford","Croxley",	4),
("Croxley","Moor Park",4),
("Uxbridge","Hillingdon",	4),
("Hillingdon","Ickenham",	2),
("Ickenham","Ruislip",	2),
("Ruislip","Ruislip Manor",	2),
("Ruislip Manor","Eastcote",	2),
("Eastcote","Rayners Lane",	2),
("Rayners Lane","West Harrow",	3),
("West Harrow","Harrow-on-the-Hill",	2),
("Harrow-on-the-Hill","North Harrow",	3),
("North Harrow","Pinner",	2),
("Pinner","Northwood Hills",	3),
("Northwood Hills","Northwood",	3),
("Northwood","Moor Park",	3),
("Moor Park","Harrow-on-the-Hill",	14),
("Harrow-on-the-Hill","Finchley Road",	16),
("Harrow-on-the-Hill","Wembley Park",	9),
("Harrow-on-the-Hill","Northwick Park",	3),
("Northwick Park","Preston Road",	3),
("Preston Road","Wembley Park",	3),
("Wembley Park","Finchley Road",	7),
("Finchley Road","Baker Street",	5),
("Baker Street","Great Portland Street",	2),
("Great Portland Street","Euston Square",	2),
("Euston Square","King's Cross St. Pancras",	2),
("King's Cross St. Pancras","Farringdon",	2),
("Farringdon","Barbican",	4),
("Barbican","Moorgate",	2),
("Moorgate","Liverpool Street",	2),
("Liverpool Street","Aldgate",	3),
("High Barnet","Totteridge & Whetstone",	4),
("Totteridge & Whetstone","Woodside Park",	2),
("Woodside Park","West Finchley",	2),
("West Finchley","Finchley Central",	2),
("Mill Hill East","Finchley Central",	4),
("Finchley Central","East Finchley",	4),
("East Finchley","Highgate",	3),
("Highgate","Archway",3),
("Archway","Tufnell Park",2),
("Tufnell Park","Kentish Town",	1),
("Kentish Town","Camden Town",	2),
("Edgware","Burnt Oak",	4),
("Burnt Oak","Colindale",	2),
("Colindale","Hendon Central",	3),
("Hendon Central","Brent Cross",	2),
("Brent Cross","Golders Green",	3),
("Golders Green","Hampstead",	4),
("Hampstead","Belsize Park",	3),
("Belsize Park","Chalk Farm",	2),
("Chalk Farm","Camden Town",	1),
("Camden Town","Mornington Crescent",	2),
("Mornington Crescent","Euston",	2),
("Warren Street","Euston",	1),
("Warren Street","Goodge Street",	2),
("Goodge Street","Tottenham Court Road",	1),
("Tottenham Court Road","Leicester Square",	2),
("Leicester Square","Charing Cross",	1),
("Charing Cross","Embankment",1),
("Embankment","Waterloo",	2),
("Waterloo","Kennington",	3),
("Euston","Camden Town",	4),
("Euston","King's Cross St. Pancras",	2),
("King's Cross St. Pancras","Angel",	3),
("Angel","Old Street",	3),
("Old Street","Moorgate",	2),
("Moorgate","Bank",	2),
("Bank","London Bridge",	2),
("London Bridge","Borough",	2),
("Borough","Elephant & Castle",	2),
("Elephant & Castle","Kennington",	2),
("Kennington","Oval",	3),
("Oval","Stockwell",	2),
("Stockwell","Clapham North",	2),
("Clapham North","Clapham Common",	2),
("Clapham Common","Clapham South",	2),
("Clapham South","Balham",	2),
("Balham","Tooting Bec",	2),
("Tooting Bec","Tooting Broadway",	2),
("Tooting Broadway","Colliers Wood",	2),
("Colliers Wood","South Wimbledon",	2),
("South Wimbledon","Morden",	3),
("Cockfosters","Oakwood",	2),
("Oakwood","Southgate",	3),
("Southgate","Arnos Grove",	4),
("Arnos Grove","Bounds Green",	2),
("Bounds Green","Wood Green",	3),
("Wood Green","Turnpike Lane",	2),
("Turnpike Lane","Manor House",	4),
("Manor House","Finsbury Park Victoria",	2),
("Finsbury Park Victoria","Arsenal",	1),
("Arsenal","Holloway Road",	2),
("Holloway Road","Caledonian Road",	2),
("Caledonian Road","King's Cross St. Pancras",	4),
("King's Cross St. Pancras","Russell Square",	2),
("Russell Square","Holborn Central",	2),
("Holborn Central","Covent Garden",	2),
("Covent Garden","Leicester Square",	1),
("Leicester Square","Piccadilly Circus",	1),
("Piccadilly Circus","Green Park",	2),
("Green Park","Hyde Park Corner",	2),
("Hyde Park Corner","Knightsbridge",	2),
("Knightsbridge","South Kensington",	2),
("South Kensington","Gloucester Road",2),
("Gloucester Road","Earl's Court",	2),
("Earl's Court","Barons Court",	3),
("Barons Court","Hammersmith",	3),
("Hammersmith","Acton Town",	8),
("Hammersmith","Turnham Green",	4),
("Turnham Green","Acton Town",	4),
("Acton Town","South Ealing",	3),
("South Ealing","Northfields",	1),
("Northfields","Boston Manor",	2),
("Boston Manor","Osterley",	3),
("Osterley","Hounslow East",	2),
("Hounslow East","Hounslow Central",	1),
("Hounslow Central","Hounslow West",	3),
("Hounslow West","Hatton Cross",	4),
("Hatton Cross","Heathrow Terminals 1, 2, 3",	4),
("Heathrow Terminals 1, 2, 3","Heathrow Terminal 5",	4),
("Hatton Cross","Heathrow Terminal 4",	3),
("Acton Town","Ealing Common",	2),
("Ealing Common","North Ealing",	2),
("North Ealing","Park Royal",	2),
("Park Royal","Alperton",	2),
("Alperton","Sudbury Town",	3),
("Sudbury Town","Sudbury Hill",	2),
("Sudbury Hill","South Harrow",	3),
("South Harrow","Rayners Lane",	5),
("Rayners Lane","Eastcote",	2),
("Eastcote","Ruislip Manor",	2),
("Ruislip Manor","Ruislip",	2),
("Ruislip","Ickenham",	4),
("Ickenham","Hillingdon",	2),
("Hillingdon","Uxbridge",	4),
("Walthamstow Central","Blackhorse Road",	3),
("Blackhorse Road","Tottenham Hale",	3),
("Tottenham Hale","Seven Sisters",	2),
("Seven Sisters","Finsbury Park",	5),
("Finsbury Park","Highbury & Islington",	2),
("Highbury & Islington","King's Cross St. Pancras",	3),
("King's Cross St. Pancras","Euston",	2),
("Euston","Warren Street",	2),
("Warren Street","Oxford Circus",	2),
("Oxford Circus","Green Park",	2),
("Green Park","Victoria",	2),
("Victoria","Pimlico",	2),
("Pimlico","Vauxhall",	2),
("Vauxhall","Stockwell",	3),
("Stockwell","Brixton",2),
("Bank","Waterloo",	5)]
)
