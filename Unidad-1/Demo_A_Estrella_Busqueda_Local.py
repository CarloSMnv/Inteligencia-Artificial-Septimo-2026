"""
Implementación didáctica de algoritmos de búsqueda en espacio de estados
Inteligencia Artificial · Unidad 1 (1.8 El papel de la heurística)
Instituto Tecnológico de Pinotepa

Incluye:
1. Algoritmo A* sobre un grafo con heurística (el ejemplo del mapa del compendio)
2. Ascenso de colina (Hill Climbing)
3. Temple simulado (Simulated Annealing)

Cómo usar en clase: corre el archivo completo (python demo_busqueda.py) y ve
comentando cada bloque de salida con el grupo. Cada sección es independiente,
así que también puedes copiar solo una función a la vez si prefieres ir
construyendo el código en vivo junto con los alumnos.
"""

import heapq
import math
import random


# =====================================================================
# 1. ALGORITMO A*
# =====================================================================

def a_estrella(grafo, heuristica, inicio, meta):
    """
    Búsqueda A* sobre un grafo dirigido con costos y heurística.

    grafo:      dict {nodo: [(vecino, costo), ...]}
    heuristica: dict {nodo: valor_h}   (debe ser ADMISIBLE: nunca sobreestimar)
    inicio, meta: nodos del grafo

    Devuelve: (camino_optimo, costo_total, nodos_expandidos)
    """
    # Cola de prioridad ordenada por f(n) = g(n) + h(n)
    # Cada elemento: (f, nodo, camino_hasta_aqui, g_acumulada)
    frontera = [(heuristica[inicio], inicio, [inicio], 0)]
    mejor_g_visto = {}
    nodos_expandidos = 0

    while frontera:
        f, nodo, camino, g = heapq.heappop(frontera)
        nodos_expandidos += 1

        if nodo == meta:
            return camino, g, nodos_expandidos

        # Si ya llegamos antes a este nodo con menor o igual costo, no repetir
        if nodo in mejor_g_visto and mejor_g_visto[nodo] <= g:
            continue
        mejor_g_visto[nodo] = g

        for vecino, costo in grafo.get(nodo, []):
            nuevo_g = g + costo
            nuevo_f = nuevo_g + heuristica[vecino]
            heapq.heappush(frontera, (nuevo_f, vecino, camino + [vecino], nuevo_g))

    return None, float("inf"), nodos_expandidos  # no se encontró camino


def busqueda_costo_uniforme(grafo, inicio, meta):
    """
    La misma búsqueda pero SIN heurística (h(n) = 0 para todos los nodos).
    Sirve para comparar cuántos nodos expande de más A* evita gracias a la heurística.
    """
    heuristica_cero = {nodo: 0 for nodo in grafo}
    return a_estrella(grafo, heuristica_cero, inicio, meta)


# ---- Ejemplo: el mapa de ciudades del compendio (Unidad 1.8.2) ----
mapa = {
    "A": [("B", 4), ("C", 2)],
    "B": [("D", 5)],
    "C": [("D", 7)],
    "D": [],
}

# Heurística: distancia en línea recta estimada hacia D (es admisible:
# la línea recta nunca es más larga que la ruta real)
heuristica_mapa = {
    "A": 8,
    "B": 4,
    "C": 6,
    "D": 0,
}


# =====================================================================
# 2. ASCENSO DE COLINA (Hill Climbing)
# =====================================================================

def funcion_objetivo(x):
    """
    Función con varios picos (óptimos locales) a propósito, para que el
    ascenso de colina se quede atrapado según de dónde arranque.
    """
    return math.sin(x) + 0.3 * math.sin(3 * x) - 0.05 * (x - 5) ** 2


def vecinos(x, paso=0.1):
    return [x - paso, x + paso]


def ascenso_de_colina(x_inicial, paso=0.1, max_iter=1000):
    """
    Se mueve siempre al vecino con mejor valor. Se detiene en cuanto
    ningún vecino mejora el estado actual (posible óptimo local).
    """
    actual = x_inicial
    valor_actual = funcion_objetivo(actual)

    for _ in range(max_iter):
        candidatos = vecinos(actual, paso)
        mejor_vecino = max(candidatos, key=funcion_objetivo)
        valor_vecino = funcion_objetivo(mejor_vecino)

        if valor_vecino <= valor_actual:
            break  # ningún vecino mejora: nos quedamos aquí

        actual, valor_actual = mejor_vecino, valor_vecino

    return actual, valor_actual


# =====================================================================
# 3. TEMPLE SIMULADO (Simulated Annealing)
# =====================================================================

def temple_simulado(x_inicial, temp_inicial=10.0, enfriamiento=0.995, temp_minima=0.01):
    """
    Como el ascenso de colina, pero permite aceptar temporalmente un
    movimiento PEOR con una probabilidad que depende de la temperatura
    actual. La temperatura baja poco a poco (enfriamiento), así que al
    principio explora mucho y al final se comporta casi como ascenso puro.
    """
    actual = x_inicial
    valor_actual = funcion_objetivo(actual)
    mejor, valor_mejor = actual, valor_actual
    temperatura = temp_inicial

    while temperatura > temp_minima:
        candidato = actual + random.uniform(-0.5, 0.5)
        valor_candidato = funcion_objetivo(candidato)
        delta = valor_candidato - valor_actual

        # Si mejora, siempre se acepta. Si empeora, se acepta con
        # probabilidad exp(delta / temperatura) -- entre más "caliente",
        # más se aceptan movimientos malos, lo cual ayuda a escapar de
        # óptimos locales.
        if delta > 0 or random.random() < math.exp(delta / temperatura):
            actual, valor_actual = candidato, valor_candidato
            if valor_actual > valor_mejor:
                mejor, valor_mejor = actual, valor_actual

        temperatura *= enfriamiento

    return mejor, valor_mejor


# =====================================================================
# DEMOSTRACIÓN EN CLASE
# =====================================================================

if __name__ == "__main__":
    print("=" * 60)
    print("1. ALGORITMO A*  (mapa de ciudades, meta: llegar a D)")
    print("=" * 60)
    camino, costo, expandidos = a_estrella(mapa, heuristica_mapa, "A", "D")
    print(f"Camino óptimo encontrado : {camino}")
    print(f"Costo total del camino   : {costo}")
    print(f"Nodos expandidos con A*  : {expandidos}")

    _, _, expandidos_sin_h = busqueda_costo_uniforme(mapa, "A", "D")
    print(f"Nodos expandidos SIN heurística (costo uniforme): {expandidos_sin_h}")
    print("-> La heurística ayuda a A* a explorar menos nodos para llegar")
    print("   al mismo resultado óptimo.")

    print()
    print("=" * 60)
    print("2. ASCENSO DE COLINA  (atrapado en óptimos locales distintos)")
    print("=" * 60)
    for x0 in [-8, 0, 8]:
        x_final, valor = ascenso_de_colina(x0)
        print(f"  Inicio en x={x0:5.1f}  ->  óptimo encontrado x={x_final:6.2f}   f(x)={valor:.3f}")
    print("-> Nota cómo el resultado CAMBIA según el punto de partida:")
    print("   cada corrida se queda atrapada en el pico más cercano.")

    print()
    print("=" * 60)
    print("3. TEMPLE SIMULADO  (mismo problema, con posibilidad de escapar)")
    print("=" * 60)
    random.seed(42)  # para que la demo sea reproducible en clase
    for x0 in [-8, 0, 8]:
        x_final, valor = temple_simulado(x0)
        print(f"  Inicio en x={x0:5.1f}  ->  óptimo encontrado x={x_final:6.2f}   f(x)={valor:.3f}")
    print("-> Compara estos resultados con los del ascenso de colina:")
    print("   el temple simulado tiende a encontrar valores más altos")
    print("   (mejores) o más parecidos entre sí, sin importar dónde arrancó.")
