"""
Comparación A* vs. búsqueda no informada sobre un mapa real de la región
Inteligencia Artificial · Unidad 1 · Actividad de cierre
Instituto Tecnológico de Pinotepa

Ruta: Pinotepa Nacional -> Santa Catarina Juquila

Distancias por carretera:
  Pinotepa Nacional - Pinotepa de Don Luis .... 18 km  (verificado)
  Pinotepa Nacional - Santiago Jamiltepec ..... 30 km  (verificado, Carretera Federal 200)
  Pinotepa de Don Luis - Santiago Jamiltepec .. 20 km  (estimado a partir de distancia en línea recta)
  Santiago Jamiltepec - Santa Catarina Juquila  65 km  (estimado a partir de distancia en línea recta)

Heurística h(n): distancia en línea recta de cada población hacia Santa Catarina Juquila
(estos valores SÍ son datos verificados de distancia en línea recta, por eso son confiables
como heurística admisible: la línea recta nunca es más larga que la carretera real).
"""

import heapq


def a_estrella(grafo, heuristica, inicio, meta):
    frontera = [(heuristica[inicio], inicio, [inicio], 0)]
    mejor_g_visto = {}
    nodos_expandidos = 0
    orden_expansion = []

    while frontera:
        f, nodo, camino, g = heapq.heappop(frontera)
        nodos_expandidos += 1
        orden_expansion.append(nodo)

        if nodo == meta:
            return camino, g, nodos_expandidos, orden_expansion

        if nodo in mejor_g_visto and mejor_g_visto[nodo] <= g:
            continue
        mejor_g_visto[nodo] = g

        for vecino, costo in grafo.get(nodo, []):
            nuevo_g = g + costo
            nuevo_f = nuevo_g + heuristica[vecino]
            heapq.heappush(frontera, (nuevo_f, vecino, camino + [vecino], nuevo_g))

    return None, float("inf"), nodos_expandidos, orden_expansion


def busqueda_no_informada(grafo, inicio, meta):
    """Búsqueda de costo uniforme SIN heurística (h = 0 para todos los nodos)."""
    heuristica_cero = {nodo: 0 for nodo in grafo}
    return a_estrella(grafo, heuristica_cero, inicio, meta)


# ---- El mapa real ----
# grafo no dirigido: se agregan ambas direcciones
mapa = {
    "Pinotepa Nacional": [("Pinotepa de Don Luis", 18), ("Santiago Jamiltepec", 30)],
    "Pinotepa de Don Luis": [("Pinotepa Nacional", 18), ("Santiago Jamiltepec", 20)],
    "Santiago Jamiltepec": [("Pinotepa Nacional", 30), ("Pinotepa de Don Luis", 20), ("Santa Catarina Juquila", 65)],
    "Santa Catarina Juquila": [("Santiago Jamiltepec", 65)],
}

# Heurística: distancia en línea recta hacia Santa Catarina Juquila (meta)
heuristica_hacia_juquila = {
    "Pinotepa Nacional": 77,
    "Pinotepa de Don Luis": 69,
    "Santiago Jamiltepec": 55,
    "Santa Catarina Juquila": 0,
}


if __name__ == "__main__":
    inicio, meta = "Pinotepa Nacional", "Santa Catarina Juquila"

    print("=" * 68)
    print(f"RUTA: {inicio}  ->  {meta}")
    print("=" * 68)

    camino_a, costo_a, exp_a, orden_a = a_estrella(mapa, heuristica_hacia_juquila, inicio, meta)
    print("\n--- A* (con heurística) ---")
    print("Ruta encontrada :", " -> ".join(camino_a))
    print("Costo total     :", costo_a, "km")
    print("Nodos expandidos:", exp_a)
    print("Orden de expansión:", orden_a)

    camino_b, costo_b, exp_b, orden_b = busqueda_no_informada(mapa, inicio, meta)
    print("\n--- Búsqueda no informada (costo uniforme, sin heurística) ---")
    print("Ruta encontrada :", " -> ".join(camino_b))
    print("Costo total     :", costo_b, "km")
    print("Nodos expandidos:", exp_b)
    print("Orden de expansión:", orden_b)

    print("\n" + "=" * 68)
    print("COMPARACIÓN")
    print("=" * 68)
    print(f"{'Algoritmo':<28}{'Costo (km)':<14}{'Nodos expandidos':<18}")
    print(f"{'A* (informada)':<28}{costo_a:<14}{exp_a:<18}")
    print(f"{'No informada':<28}{costo_b:<14}{exp_b:<18}")
    print("\nAmbas encuentran la MISMA ruta óptima (la heurística es admisible),")
    print("pero A* llega expandiendo menos nodos porque prioriza las poblaciones")
    print("geográficamente más cercanas a la meta.")
