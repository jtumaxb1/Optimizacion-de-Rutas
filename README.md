# 🗺️ Optimización de Rutas — Agente Inteligente
### Proyecto Final · Curso de Inteligencia Artificial

> Implementación y comparación visual de los algoritmos **BFS**, **DFS** y **A\*** aplicados a la búsqueda de rutas óptimas en un grafo de ciudades. Incluye interfaz gráfica animada desarrollada en Python con Tkinter.

---

## 📋 Descripción

Este proyecto implementa un **sistema de optimización de rutas** como agente inteligente, aplicando técnicas de búsqueda en espacios de estados. El sistema permite visualizar en tiempo real cómo cada algoritmo explora el grafo y encuentra una ruta entre dos ciudades, comparando su eficiencia y calidad de solución.

El grafo modela **8 ciudades** conectadas por **12 rutas** con distancias en kilómetros. El usuario puede seleccionar origen, destino y algoritmo, y observar la animación paso a paso.

---

## 🎯 Algoritmos implementados

| Algoritmo | Estructura | Óptimo en costo | Completo | Complejidad |
|-----------|-----------|-----------------|----------|-------------|
| **BFS** — Búsqueda en Amplitud | Cola FIFO | No (en grafos ponderados) | Sí | O(V + E) |
| **DFS** — Búsqueda en Profundidad | Pila LIFO | No | Sí | O(V + E) |
| **A\*** — Búsqueda Heurística | Min-heap | **Sí** | Sí | O(E log V) |

### Función de evaluación de A\*

```
f(n) = g(n) + h(n)
```

- `g(n)` — costo real acumulado desde el origen hasta el nodo n  
- `h(n)` — heurística: distancia euclidiana desde n hasta la meta  
- La heurística es **admisible**: nunca sobreestima el costo real, garantizando optimalidad

---

## 📊 Resultados (Ciudad A → Ciudad H)

| Algoritmo | Ruta encontrada | Costo | Saltos | ¿Óptimo? |
|-----------|----------------|-------|--------|----------|
| BFS | A → B → F → H | 165 km | 3 | ❌ |
| DFS | A → B → C → F → E → D → G → H | 323 km | 7 | ❌ |
| **A\*** | **A → D → G → H** | **137 km** | **3** | **✅** |

---

## 🖥️ Interfaz gráfica

La aplicación incluye una ventana interactiva con:

- **Menús desplegables** para seleccionar origen y destino
- **Selector de algoritmo**: BFS, DFS o A\*
- **Slider de velocidad** para controlar la animación
- **Botón ▶ Buscar Ruta** que lanza la exploración animada
- **Métricas en tiempo real**: distancia, saltos, nodos explorados y ruta encontrada
- **Registro de búsqueda** que describe cada paso del algoritmo

### Colores del grafo

| Color | Significado |
|-------|-------------|
| 🟢 Verde | Ciudad de inicio |
| 🔴 Rojo | Ciudad meta |
| 🟡 Amarillo | Nodo explorado |
| 🟣 Morado | Nodo en frontera (próximo a visitar) |
| 🔵 Azul | Ruta óptima encontrada |
| ⚫ Gris | Sin visitar |

---

## ⚙️ Instalación y ejecución

### Requisitos

- Python **3.10** o superior (recomendado: 3.14)
- No se requieren librerías externas — todo usa la biblioteca estándar de Python

### Librerías utilizadas

```
tkinter      → interfaz gráfica (incluida con Python)
math         → cálculo de distancia euclidiana para A*
heapq        → cola de prioridad para A*
collections  → deque (cola FIFO) para BFS
platform     → detección del sistema operativo
```

### Pasos para ejecutar

**1. Clonar el repositorio**
```bash
git clone https://github.com/usuario/optimizacion-rutas-ia.git
cd optimizacion-rutas-ia
```

**2. Ejecutar la aplicación**
```bash
python optimizacion_rutas_gui.py
```

> ✅ No necesitas instalar nada con `pip`. Tkinter ya viene incluido con Python.

### En Mac

Si usas macOS y la ventana aparece en negro, asegúrate de estar usando la versión corregida del archivo. El código detecta automáticamente si estás en Mac y aplica los ajustes necesarios.

---

## 📁 Estructura del proyecto

```
optimizacion-rutas-ia/
│
├── optimizacion_rutas_gui.py      # Aplicación principal con interfaz gráfica
├── optimizacion_rutas.py          # Script de análisis y comparación (genera gráficas)
├── README.md                      # Este archivo
│
└── docs/
    ├── Proyecto_IA_Optimizacion_Rutas.docx     # Documento técnico completo
    ├── Seccion6_Resultados_Interpretacion.docx  # Sección 6 del informe
    └── Guia_Presentacion_Defensa_IA.docx        # Guía de presentación y defensa
```

---

## 🧠 Estructura del código

### Representación del grafo

```python
# Coordenadas de cada ciudad en el canvas (usadas por la heurística de A*)
NODOS = {
    'Ciudad A': (100, 300),
    'Ciudad B': (260, 150),
    # ...
}

# Aristas con costo en km (bidireccionales)
ARISTAS = [
    ('Ciudad A', 'Ciudad B', 45),
    ('Ciudad A', 'Ciudad D', 32),
    # ...
]
```

### Implementación de A\*

```python
def astar(start, end):
    heap = [(heuristic(start, end), 0, start, [start])]
    visited = set()

    while heap:
        f, g, cur, path = heapq.heappop(heap)   # nodo con menor f(n)
        if cur in visited: continue
        visited.add(cur)

        if cur == end:
            return path, round(g), steps

        for nb, c in ADJ[cur]:
            if nb not in visited:
                ng = g + c
                heapq.heappush(heap, (ng + heuristic(nb, end), ng, nb, path + [nb]))
```

---

## 📐 Grafo del proyecto

```
    B ──38── C
   /|\       \
  45 25  88   55
 /   |    \    \
A    |     F ──40── H
 \   |    /         |
  32 |   35         |
   \ |  /           33
    D ──42── E      |
     \       \      |
      72      50    |
       \       \    |
        └── G ──────┘
```

**Ruta óptima (A\*):** A → D (32 km) → G (72 km) → H (33 km) = **137 km total**

---

## ⚖️ Aspectos éticos

- **Sesgo en datos**: si los costos no reflejan condiciones reales (seguridad, accesibilidad), el sistema puede discriminar rutas o zonas.
- **Impacto en tráfico**: una ruta óptima para muchos usuarios simultáneamente puede saturar arterias urbanas.
- **Privacidad**: los sistemas de navegación reales recopilan datos de ubicación sensibles que requieren anonimización y consentimiento.

---

## 👥 Equipo

Proyecto desarrollado como parte del curso de **Inteligencia Artificial**.

|           Integrante            |     Carné    |
|---------------------------------|--------------|
| Jeremy Alejandro de León Roa    | 0900 22 2413 |
| Santiago Benjamin Canel Escobar | 0900 22 1504 |
| Gabriel Figueros Cardona        | 0900 22 9287 |
| Josue Fernando Tumax Baquiax    | 0900 22 8742 |

---

## 📄 Licencia

Proyecto académico — Curso de Inteligencia Artificial.
