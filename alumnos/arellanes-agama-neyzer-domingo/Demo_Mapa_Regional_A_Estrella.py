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



def correr(inicio, meta, titulo):
    ca, costo_a, ea, oa = a_estrella(mapa, heuristica_hacia_juquila, inicio, meta)
    cb, costo_b, eb, ob = busqueda_no_informada(mapa, inicio, meta)
    print("=" * 68)
    print(f"{titulo}: {inicio}  ->  {meta}")
    print("=" * 68)
    print("A*          :", " -> ".join(ca), "| costo:", costo_a, "km | nodos:", ea)
    print("No informada:", " -> ".join(cb), "| costo:", costo_b, "km | nodos:", eb)
    print()


if __name__ == "__main__":
    meta = "Santa Catarina Juquila"

    # Ruta 1: la del ejemplo
    correr("Pinotepa Nacional", meta, "RUTA 1")

    # Ruta 2: otro inicio, mismo mapa
    correr("Pinotepa de Don Luis", meta, "RUTA 2")

    # Ruta 3: se agrega una población real al mapa.
    # IMPORTANTE: los dos datos siguientes son PLACEHOLDERS. Reemplázalos con
    # la distancia por carretera y la distancia en línea recta que investigues.
    # La línea recta debe ser menor o igual que la distancia por carretera.
    nueva = "Santa María Huazolotitlán"
    km_carretera_a_jamiltepec = 15      # PLACEHOLDER
    km_linea_recta_a_juquila = 58       # PLACEHOLDER

    mapa[nueva] = [("Santiago Jamiltepec", km_carretera_a_jamiltepec)]
    mapa["Santiago Jamiltepec"].append((nueva, km_carretera_a_jamiltepec))
    heuristica_hacia_juquila[nueva] = km_linea_recta_a_juquila

    correr(nueva, meta, "RUTA 3")
