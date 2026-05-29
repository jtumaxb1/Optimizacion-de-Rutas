# =============================================================================
#  PROYECTO FINAL – INTELIGENCIA ARTIFICIAL
#  Escenario 3: Optimización de Rutas — Interfaz Gráfica con Animación
#  Algoritmos: BFS, DFS, A*
#  Compatible: Windows, Mac, Linux
# =============================================================================

import tkinter as tk
from tkinter import ttk, messagebox
import math
import heapq
import platform
from collections import deque

# =============================================================================
# DATOS DEL GRAFO
# =============================================================================

NODOS = {
    'Ciudad A': (100, 300),
    'Ciudad B': (260, 150),
    'Ciudad C': (430, 100),
    'Ciudad D': (260, 380),
    'Ciudad E': (450, 320),
    'Ciudad F': (590, 160),
    'Ciudad G': (590, 420),
    'Ciudad H': (740, 290),
}

ARISTAS = [
    ('Ciudad A', 'Ciudad B', 45),
    ('Ciudad A', 'Ciudad D', 32),
    ('Ciudad B', 'Ciudad C', 38),
    ('Ciudad B', 'Ciudad D', 25),
    ('Ciudad B', 'Ciudad F', 88),
    ('Ciudad C', 'Ciudad F', 55),
    ('Ciudad D', 'Ciudad E', 42),
    ('Ciudad E', 'Ciudad F', 35),
    ('Ciudad E', 'Ciudad G', 50),
    ('Ciudad F', 'Ciudad H', 40),
    ('Ciudad G', 'Ciudad H', 33),
    ('Ciudad D', 'Ciudad G', 72),
]

# Colores
COLOR_BG      = '#1a1a2e'
COLOR_PANEL   = '#16213e'
COLOR_CARD    = '#0f3460'
COLOR_EDGE    = '#334155'
COLOR_NODE    = '#475569'
COLOR_START   = '#22c55e'
COLOR_END     = '#ef4444'
COLOR_VISITED = '#f59e0b'
COLOR_PATH    = '#3b82f6'
COLOR_FRONT   = '#a855f7'
COLOR_TEXT    = '#f1f5f9'
COLOR_MUTED   = '#94a3b8'
COLOR_BTN     = '#3b82f6'

IS_MAC = platform.system() == 'Darwin'

def build_adj():
    adj = {n: [] for n in NODOS}
    for a, b, w in ARISTAS:
        adj[a].append((b, w))
        adj[b].append((a, w))
    return adj

ADJ = build_adj()

# =============================================================================
# ALGORITMOS
# =============================================================================

def bfs(start, end):
    queue = deque([(start, [start], 0)])
    visited = set([start])
    steps = []
    while queue:
        cur, path, cost = queue.popleft()
        steps.append(('visit', cur, list(path), cost))
        if cur == end:
            return path, cost, steps
        for nb, c in ADJ[cur]:
            if nb not in visited:
                visited.add(nb)
                steps.append(('frontier', nb, list(path), cost))
                queue.append((nb, path + [nb], cost + c))
    return [], 0, steps

def dfs(start, end):
    stack = [(start, [start], 0)]
    visited = set()
    steps = []
    while stack:
        cur, path, cost = stack.pop()
        if cur in visited:
            continue
        visited.add(cur)
        steps.append(('visit', cur, list(path), cost))
        if cur == end:
            return path, cost, steps
        for nb, c in reversed(ADJ[cur]):
            if nb not in visited:
                steps.append(('frontier', nb, list(path), cost))
                stack.append((nb, path + [nb], cost + c))
    return [], 0, steps

def heuristic(a, b):
    x1, y1 = NODOS[a]
    x2, y2 = NODOS[b]
    return math.sqrt((x1-x2)**2 + (y1-y2)**2) * 0.08

def astar(start, end):
    heap = [(heuristic(start, end), 0, start, [start])]
    visited = set()
    steps = []
    while heap:
        f, g, cur, path = heapq.heappop(heap)
        if cur in visited:
            continue
        visited.add(cur)
        steps.append(('visit', cur, list(path), round(g)))
        if cur == end:
            return path, round(g), steps
        for nb, c in ADJ[cur]:
            if nb not in visited:
                ng = g + c
                steps.append(('frontier', nb, list(path), round(ng)))
                heapq.heappush(heap, (ng + heuristic(nb, end), ng, nb, path + [nb]))
    return [], 0, steps

# =============================================================================
# INTERFAZ GRÁFICA
# =============================================================================

class RouteApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Optimización de Rutas — IA")
        self.root.configure(bg=COLOR_BG)
        self.root.resizable(True, True)

        self.visited_nodes  = set()
        self.frontier_nodes = set()
        self.path_nodes     = []
        self.path_edges     = set()
        self.animating      = False
        self.anim_steps     = []
        self.anim_index     = 0
        self.anim_after     = None
        self.final_path     = []
        self.final_cost     = 0

        self._apply_styles()
        self._build_ui()
        # En Mac hay que esperar a que la ventana esté lista antes de dibujar
        self.root.after(100, self._draw_graph)

    def _apply_styles(self):
        style = ttk.Style()
        # Usar un tema compatible con Mac y Windows
        try:
            style.theme_use('clam')
        except Exception:
            pass
        style.configure('TCombobox',
                         fieldbackground=COLOR_CARD,
                         background=COLOR_CARD,
                         foreground=COLOR_TEXT,
                         selectbackground=COLOR_CARD,
                         selectforeground=COLOR_TEXT,
                         bordercolor=COLOR_PANEL,
                         arrowcolor=COLOR_TEXT)
        style.map('TCombobox',
                  fieldbackground=[('readonly', COLOR_CARD)],
                  selectbackground=[('readonly', COLOR_CARD)],
                  foreground=[('readonly', COLOR_TEXT)])

    def _build_ui(self):
        # ---- Título ----
        tk.Label(self.root,
                 text="Optimización de Rutas",
                 font=('Arial', 18, 'bold'),
                 bg=COLOR_BG, fg=COLOR_TEXT).pack(pady=(14, 2))

        tk.Label(self.root,
                 text="Proyecto Final IA — BFS | DFS | A*",
                 font=('Arial', 11),
                 bg=COLOR_BG, fg=COLOR_MUTED).pack(pady=(0, 10))

        # ---- Panel de controles ----
        ctrl = tk.Frame(self.root, bg=COLOR_PANEL, padx=14, pady=12)
        ctrl.pack(fill='x', padx=14, pady=(0, 8))

        ciudades = list(NODOS.keys())

        # Fila 1: selectores
        row1 = tk.Frame(ctrl, bg=COLOR_PANEL)
        row1.pack(fill='x', pady=(0, 8))

        self._lbl(row1, "Origen:").pack(side='left', padx=(0, 4))
        self.start_var = tk.StringVar(value=ciudades[0])
        self._combo(row1, self.start_var, ciudades).pack(side='left', padx=(0, 14))

        self._lbl(row1, "Destino:").pack(side='left', padx=(0, 4))
        self.end_var = tk.StringVar(value=ciudades[-1])
        self._combo(row1, self.end_var, ciudades).pack(side='left', padx=(0, 14))

        self._lbl(row1, "Algoritmo:").pack(side='left', padx=(0, 4))
        self.algo_var = tk.StringVar(value='A*')
        self._combo(row1, self.algo_var, ['BFS', 'DFS', 'A*']).pack(side='left', padx=(0, 14))

        self._lbl(row1, "Velocidad:").pack(side='left', padx=(0, 4))
        self.speed_var = tk.IntVar(value=60)
        tk.Scale(row1, from_=10, to=200, orient='horizontal',
                 variable=self.speed_var, bg=COLOR_PANEL, fg=COLOR_TEXT,
                 highlightthickness=0, troughcolor=COLOR_CARD,
                 activebackground=COLOR_BTN, length=110,
                 font=('Arial', 8), showvalue=False,
                 bd=0, relief='flat').pack(side='left', padx=(0, 14))

        # Botones
        self.btn_run = self._btn(row1, "▶  Buscar Ruta", self._start_search, COLOR_BTN)
        self.btn_run.pack(side='left', padx=(0, 8))
        self._btn(row1, "↺  Limpiar", self._reset, '#475569').pack(side='left')

        # Fila 2: métricas
        row2 = tk.Frame(ctrl, bg=COLOR_PANEL)
        row2.pack(fill='x')

        self.lbl_status = self._metric(row2, "Estado",           "—")
        self.lbl_km     = self._metric(row2, "Distancia",        "— km")
        self.lbl_pasos  = self._metric(row2, "Saltos",           "—")
        self.lbl_exp    = self._metric(row2, "Explorados",       "—")
        self.lbl_ruta   = self._metric(row2, "Ruta encontrada",  "—", wide=True)

        # ---- Canvas ----
        self.canvas = tk.Canvas(self.root, bg=COLOR_BG,
                                highlightthickness=0,
                                width=870, height=500)
        self.canvas.pack(padx=14, pady=(0, 6), fill='both', expand=True)

        # ---- Log ----
        log_frame = tk.Frame(self.root, bg=COLOR_PANEL, padx=10, pady=6)
        log_frame.pack(fill='x', padx=14, pady=(0, 12))

        tk.Label(log_frame, text="Registro de búsqueda:",
                 font=('Arial', 9, 'bold'),
                 bg=COLOR_PANEL, fg=COLOR_MUTED).pack(anchor='w')

        self.log_var = tk.StringVar(
            value="Selecciona origen, destino y algoritmo, luego presiona ▶ Buscar Ruta.")
        tk.Label(log_frame, textvariable=self.log_var,
                 font=('Arial', 9),
                 bg=COLOR_PANEL, fg=COLOR_TEXT,
                 wraplength=820, justify='left').pack(anchor='w')

        # Leyenda colores
        leg = tk.Frame(self.root, bg=COLOR_BG)
        leg.pack(pady=(0, 10))
        items = [
            (COLOR_START,   'Inicio'),
            (COLOR_END,     'Meta'),
            (COLOR_VISITED, 'Explorado'),
            (COLOR_FRONT,   'Frontera'),
            (COLOR_PATH,    'Ruta óptima'),
        ]
        for color, label in items:
            tk.Label(leg, text='●', font=('Arial', 16),
                     bg=COLOR_BG, fg=color).pack(side='left', padx=(6, 1))
            tk.Label(leg, text=label, font=('Arial', 9),
                     bg=COLOR_BG, fg=COLOR_MUTED).pack(side='left', padx=(0, 8))

    # ---- Helpers de widgets ----

    def _lbl(self, parent, text):
        return tk.Label(parent, text=text, font=('Arial', 10),
                        bg=COLOR_PANEL, fg=COLOR_MUTED)

    def _combo(self, parent, var, values):
        cb = ttk.Combobox(parent, textvariable=var, values=values,
                          state='readonly', width=12, font=('Arial', 10))
        return cb

    def _btn(self, parent, text, cmd, color):
        return tk.Button(parent, text=text, command=cmd,
                         font=('Arial', 10, 'bold'),
                         bg=color, fg='white',
                         activebackground='#1d4ed8',
                         activeforeground='white',
                         relief='flat', bd=0,
                         padx=12, pady=6,
                         cursor='hand2')

    def _metric(self, parent, label, value, wide=False):
        f = tk.Frame(parent, bg=COLOR_CARD, padx=10, pady=6)
        f.pack(side='left', padx=(0, 8), fill='y')
        tk.Label(f, text=label, font=('Arial', 8),
                 bg=COLOR_CARD, fg=COLOR_MUTED).pack(anchor='w')
        var = tk.StringVar(value=value)
        w = 26 if wide else 10
        tk.Label(f, textvariable=var, font=('Arial', 11, 'bold'),
                 bg=COLOR_CARD, fg=COLOR_TEXT,
                 width=w, anchor='w').pack()
        return var

    # ---- Dibujo del grafo ----

    def _draw_graph(self):
        self.canvas.delete('all')

        path_edge_set = set()
        if len(self.path_nodes) > 1:
            for a, b in zip(self.path_nodes[:-1], self.path_nodes[1:]):
                path_edge_set.add((a, b))
                path_edge_set.add((b, a))

        # Aristas
        for a, b, w in ARISTAS:
            x1, y1 = NODOS[a]
            x2, y2 = NODOS[b]
            is_path = (a, b) in path_edge_set
            color = COLOR_PATH if is_path else COLOR_EDGE
            width = 4   if is_path else 1.5
            self.canvas.create_line(x1, y1, x2, y2,
                                    fill=color, width=width, tags='edge')
            mx, my = (x1+x2)//2, (y1+y2)//2 - 10
            self.canvas.create_text(mx, my,
                                    text=f"{w} km",
                                    fill=COLOR_PATH if is_path else COLOR_MUTED,
                                    font=('Arial', 8,
                                          'bold' if is_path else 'normal'))

        # Nodos
        r = 24
        start_city = self.start_var.get()
        end_city   = self.end_var.get()

        for name, (x, y) in NODOS.items():
            if   name == start_city:          fill = COLOR_START
            elif name == end_city:            fill = COLOR_END
            elif name in self.path_nodes:     fill = COLOR_PATH
            elif name in self.frontier_nodes: fill = COLOR_FRONT
            elif name in self.visited_nodes:  fill = COLOR_VISITED
            else:                             fill = COLOR_NODE

            # Sombra
            self.canvas.create_oval(x-r+3, y-r+3, x+r+3, y+r+3,
                                    fill='#000000', outline='')
            # Círculo principal
            self.canvas.create_oval(x-r, y-r, x+r, y+r,
                                    fill=fill, outline='white', width=2)
            # Letra
            letra = name.split()[-1]
            self.canvas.create_text(x, y, text=letra,
                                    font=('Arial', 13, 'bold'),
                                    fill='white')
            # Nombre debajo
            self.canvas.create_text(x, y+r+12, text=name,
                                    font=('Arial', 7),
                                    fill=COLOR_MUTED)

    # ---- Lógica de búsqueda y animación ----

    def _start_search(self):
        if self.animating:
            return
        start = self.start_var.get()
        end   = self.end_var.get()
        algo  = self.algo_var.get()

        if start == end:
            messagebox.showwarning("Atención",
                                   "El origen y destino deben ser diferentes.")
            return

        self._reset(keep=True)
        self.animating = True
        self.btn_run.config(state='disabled')

        fns = {'BFS': bfs, 'DFS': dfs, 'A*': astar}
        path, cost, steps = fns[algo](start, end)
        self.final_path  = path
        self.final_cost  = cost
        self.anim_steps  = steps
        self.anim_index  = 0

        self.lbl_status.set(f"⏳ Ejecutando {algo}...")
        self.log_var.set(
            f"Iniciando {algo}: buscando ruta de {start} → {end}...")

        self._animate_step()

    def _animate_step(self):
        if self.anim_index >= len(self.anim_steps):
            self._finish()
            return

        action, node, path, cost = self.anim_steps[self.anim_index]
        self.anim_index += 1

        if action == 'visit':
            self.visited_nodes.add(node)
            self.frontier_nodes.discard(node)
            self.lbl_exp.set(str(len(self.visited_nodes)))
            self.lbl_km.set(f"{cost} km")
            self.log_var.set(
                f"Visitando: {node}  |  Costo acumulado: {cost} km  |  "
                f"Explorados: {len(self.visited_nodes)}")
        elif action == 'frontier':
            self.frontier_nodes.add(node)

        self._draw_graph()
        delay = max(10, 220 - self.speed_var.get())
        self.anim_after = self.root.after(delay, self._animate_step)

    def _finish(self):
        self.animating = False
        self.btn_run.config(state='normal')

        if self.final_path:
            self.path_nodes = self.final_path
            self.path_edges = set(
                zip(self.final_path[:-1], self.final_path[1:]))

            km_real = 0
            for a, b in zip(self.final_path[:-1], self.final_path[1:]):
                for x, y, w in ARISTAS:
                    if (x == a and y == b) or (x == b and y == a):
                        km_real += w
                        break

            self._draw_graph()
            self.lbl_status.set("✓ Ruta encontrada")
            self.lbl_km.set(f"{km_real} km")
            self.lbl_pasos.set(str(len(self.final_path) - 1))
            self.lbl_exp.set(str(len(self.visited_nodes)))
            self.lbl_ruta.set("  →  ".join(self.final_path))
            self.log_var.set(
                f"✓ Ruta: {' → '.join(self.final_path)}  |  "
                f"Distancia: {km_real} km  |  "
                f"Saltos: {len(self.final_path)-1}  |  "
                f"Explorados: {len(self.visited_nodes)}")
        else:
            self.lbl_status.set("✗ Sin ruta")
            self.log_var.set("No se encontró ruta entre los nodos seleccionados.")

    def _reset(self, keep=False):
        if self.anim_after:
            self.root.after_cancel(self.anim_after)
            self.anim_after = None
        self.animating      = False
        self.btn_run.config(state='normal')
        self.visited_nodes  = set()
        self.frontier_nodes = set()
        self.path_nodes     = []
        self.path_edges     = set()
        self.anim_steps     = []
        self.anim_index     = 0
        self.final_path     = []
        self.final_cost     = 0
        self.lbl_status.set("—")
        self.lbl_km.set("— km")
        self.lbl_pasos.set("—")
        self.lbl_exp.set("—")
        self.lbl_ruta.set("—")
        self.log_var.set(
            "Selecciona origen, destino y algoritmo, luego presiona ▶ Buscar Ruta.")
        self._draw_graph()

# =============================================================================
# MAIN
# =============================================================================

if __name__ == '__main__':
    root = tk.Tk()
    root.geometry('920x760')

    # En Mac, forzar que la ventana aparezca al frente
    if IS_MAC:
        root.lift()
        root.attributes('-topmost', True)
        root.after(200, lambda: root.attributes('-topmost', False))

    app = RouteApp(root)
    root.mainloop()
