"""
Actividad 1 (RESUELTA) · A* vs. búsqueda no informada sobre un mapa real de la región
Inteligencia Artificial · Unidad 1 · Actividad de cierre
Instituto Tecnológico de Pinotepa

Cambios respecto al script original:
  - Se agregó UNA población real: Santa María Huazolotitlán (reto de la actividad).
  - Se agregó la función correr_ruta() para ejecutar y comparar varias rutas.
  - Se ejecutan las 3 rutas que pide la tabla de la actividad.

Distancias por carretera (km):
  Pinotepa Nacional - Pinotepa de Don Luis ........ 18  (verificado)
  Pinotepa Nacional - Santiago Jamiltepec ......... 30  (verificado, Carretera Federal 200)
  Pinotepa de Don Luis - Santiago Jamiltepec ...... 20  (estimado)
  Santiago Jamiltepec - Santa Catarina Juquila .... 65  (estimado)
  Pinotepa Nacional - Santa María Huazolotitlán ... 12  (ESTIMADO: ~9.6 km en línea recta + curvas de la carretera)
  Santa María Huazolotitlán - Santiago Jamiltepec . 18  (ESTIMADO: ~12.5 km en línea recta + curvas)

Heurística h(n): distancia en línea recta hacia Santa Catarina Juquila.
  Huazolotitlán: ~67 km (calculado con coordenadas; se redondea hacia abajo para que
  siga siendo admisible y consistente: 67 <= 12.5 + 55).
  RECOMENDACIÓN: verifiquen las distancias estimadas en Google Maps antes de entregar.
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


# ---- Mapa ORIGINAL (4 poblaciones) ----
mapa_original = {
    "Pinotepa Nacional": [("Pinotepa de Don Luis", 18), ("Santiago Jamiltepec", 30)],
    "Pinotepa de Don Luis": [("Pinotepa Nacional", 18), ("Santiago Jamiltepec", 20)],
    "Santiago Jamiltepec": [("Pinotepa Nacional", 30), ("Pinotepa de Don Luis", 20), ("Santa Catarina Juquila", 65)],
    "Santa Catarina Juquila": [("Santiago Jamiltepec", 65)],
}

heuristica_original = {
    "Pinotepa Nacional": 77,
    "Pinotepa de Don Luis": 69,
    "Santiago Jamiltepec": 55,
    "Santa Catarina Juquila": 0,
}

# ---- Mapa AMPLIADO (5 poblaciones): se agrega Santa María Huazolotitlán ----
mapa_ampliado = {
    "Pinotepa Nacional": [("Pinotepa de Don Luis", 18), ("Santiago Jamiltepec", 30), ("Santa María Huazolotitlán", 12)],
    "Pinotepa de Don Luis": [("Pinotepa Nacional", 18), ("Santiago Jamiltepec", 20)],
    "Santiago Jamiltepec": [("Pinotepa Nacional", 30), ("Pinotepa de Don Luis", 20),
                            ("Santa María Huazolotitlán", 18), ("Santa Catarina Juquila", 65)],
    "Santa María Huazolotitlán": [("Pinotepa Nacional", 12), ("Santiago Jamiltepec", 18)],
    "Santa Catarina Juquila": [("Santiago Jamiltepec", 65)],
}

heuristica_ampliada = dict(heuristica_original)
heuristica_ampliada["Santa María Huazolotitlán"] = 67


def correr_ruta(titulo, mapa, heuristica, inicio, meta):
    print("=" * 70)
    print(f"{titulo}\n{inicio}  ->  {meta}")
    print("=" * 70)

    camino_a, costo_a, exp_a, orden_a = a_estrella(mapa, heuristica, inicio, meta)
    camino_b, costo_b, exp_b, orden_b = busqueda_no_informada(mapa, inicio, meta)

    print("A*           :", " -> ".join(camino_a), f"| {costo_a} km | {exp_a} nodos")
    print("  expansión  :", orden_a)
    print("No informada :", " -> ".join(camino_b), f"| {costo_b} km | {exp_b} nodos")
    print("  expansión  :", orden_b)
    print(f"¿Misma ruta y costo? {camino_a == camino_b and costo_a == costo_b}\n")
    return camino_a, costo_a, exp_a, exp_b


if __name__ == "__main__":
    meta = "Santa Catarina Juquila"

    r1 = correr_ruta("RUTA 1 (la del ejemplo)", mapa_original, heuristica_original,
                     "Pinotepa Nacional", meta)
    r2 = correr_ruta("RUTA 2 (cambio de inicio)", mapa_original, heuristica_original,
                     "Pinotepa de Don Luis", meta)
    r3 = correr_ruta("RUTA 3 (con Santa María Huazolotitlán agregada)", mapa_ampliado, heuristica_ampliada,
                     "Santa María Huazolotitlán", meta)

    print("=" * 70)
    print("TABLA RESUMEN")
    print("=" * 70)
    print(f"{'Ruta':<8}{'Costo (km)':<13}{'Nodos A*':<11}{'Nodos no informada':<20}")
    for nombre, (camino, costo, ea, eb) in zip(["Ruta 1", "Ruta 2", "Ruta 3"], [r1, r2, r3]):
        print(f"{nombre:<8}{costo:<13}{ea:<11}{eb:<20}")
