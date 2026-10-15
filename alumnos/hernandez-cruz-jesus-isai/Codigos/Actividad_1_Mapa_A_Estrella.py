"""Actividad 1. Tres comparaciones A* / costo uniforme en mapa regional.
Adaptación didáctica del código del profesor:
https://github.com/CarlosMnv/Inteligencia-Artificial-Septimo-2026
Se conserva su definición del contador: cada extracción de la cola cuenta,
incluso si después se descarta una repetición. Para comparar con la tabla
entregada, ejecutar este archivo completo con Python 3.
La conexión Huaxpaltepec-Jamiltepec (14 km) es referencial para este modelo.
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
    """Búsqueda de costo uniforme; se establece h(n)=0."""
    heuristica_cero = {nodo: 0 for nodo in grafo}
    return a_estrella(grafo, heuristica_cero, inicio, meta)


mapa = {
    "Pinotepa Nacional": [("Pinotepa de Don Luis", 18), ("Santiago Jamiltepec", 30)],
    "Pinotepa de Don Luis": [("Pinotepa Nacional", 18), ("Santiago Jamiltepec", 20)],
    "Santiago Jamiltepec": [("Pinotepa Nacional", 30), ("Pinotepa de Don Luis", 20), ("Santa Catarina Juquila", 65)],
    "Santa Catarina Juquila": [("Santiago Jamiltepec", 65)],
}
heuristica_hacia_juquila = {
    "Pinotepa Nacional": 77,
    "Pinotepa de Don Luis": 69,
    "Santiago Jamiltepec": 55,
    "Santa Catarina Juquila": 0,
}

# Para la tercera ruta se amplía una copia del mapa original.
mapa_ampliado = {poblacion: vecinos.copy() for poblacion, vecinos in mapa.items()}
mapa_ampliado["San Andrés Huaxpaltepec"] = [("Santiago Jamiltepec", 14)]
mapa_ampliado["Santiago Jamiltepec"].append(("San Andrés Huaxpaltepec", 14))
heuristica_ampliada = heuristica_hacia_juquila.copy()
heuristica_ampliada["San Andrés Huaxpaltepec"] = 67.5  # estimación conservadora


def comparar(numero, grafo, heuristica, inicio, meta):
    a = a_estrella(grafo, heuristica, inicio, meta)
    b = busqueda_no_informada(grafo, inicio, meta)
    print(f"\nRUTA {numero}: {inicio} -> {meta}")
    for nombre, resultado in (("A*", a), ("Costo uniforme", b)):
        ruta, costo, extracciones, orden = resultado
        print(f"{nombre}: {' -> '.join(ruta)}")
        print(f"  Costo: {costo} km | Conteo original: {extracciones}")
        print(f"  Orden: {orden}")
    return numero, inicio, a[0], a[1], a[2], b[2]


if __name__ == "__main__":
    meta = "Santa Catarina Juquila"
    resultados = [
        comparar(1, mapa, heuristica_hacia_juquila, "Pinotepa Nacional", meta),
        comparar(2, mapa, heuristica_hacia_juquila, "Pinotepa de Don Luis", meta),
        comparar(3, mapa_ampliado, heuristica_ampliada, "San Andrés Huaxpaltepec", meta),
    ]
    print("\nTABLA RESUMEN - ACTIVIDAD 1")
    print(f"{'Ruta':<6}{'Costo km':<12}{'A*':<9}{'Sin heurística':<18}")
    for numero, inicio, ruta, costo, exp_a, exp_b in resultados:
        print(f"{numero:<6}{costo:<12}{exp_a:<9}{exp_b:<18}")
