import heapq

# Mapa regional: distancias en kilómetros
mapa = {
    "Pinotepa Nacional": [
        ("Pinotepa de Don Luis", 18),
        ("Santiago Jamiltepec", 30),
        ("San Juan Cacahuatepec", 46)
    ],
    "Pinotepa de Don Luis": [
        ("Pinotepa Nacional", 18),
        ("Santiago Jamiltepec", 20)
    ],
    "Santiago Jamiltepec": [
        ("Pinotepa Nacional", 30),
        ("Pinotepa de Don Luis", 20),
        ("Santa Catarina Juquila", 65)
    ],
    "Santa Catarina Juquila": [
        ("Santiago Jamiltepec", 65)
    ],
    "San Juan Cacahuatepec": [
        ("Pinotepa Nacional", 46)
    ]
}


def a_estrella(mapa, inicio, objetivo, heuristica):
    abiertos = [(heuristica.get(inicio, 0), 0, inicio, [inicio])]
    mejor_g_visto = {inicio: 0}
    nodos_expandidos = 0

    while abiertos:
        f, g, nodo, camino = heapq.heappop(abiertos)
        nodos_expandidos += 1

        if nodo == objetivo:
            return camino, g, nodos_expandidos

        if g > mejor_g_visto.get(nodo, float("inf")):
            continue

        for vecino, costo in mapa.get(nodo, []):
            nuevo_g = g + costo

            if nuevo_g < mejor_g_visto.get(vecino, float("inf")):
                mejor_g_visto[vecino] = nuevo_g
                nuevo_f = nuevo_g + heuristica.get(vecino, 0)
                heapq.heappush(
                    abiertos,
                    (nuevo_f, nuevo_g, vecino, camino + [vecino])
                )

    return None, float("inf"), nodos_expandidos


def busqueda_no_informada(mapa, inicio, objetivo):
    heuristica_cero = {nodo: 0 for nodo in mapa}
    return a_estrella(mapa, inicio, objetivo, heuristica_cero)


# Heurística para llegar a Santa Catarina Juquila.
heuristica_juquila = {
    "Pinotepa Nacional": 77,
    "Pinotepa de Don Luis": 69,
    "Santiago Jamiltepec": 55,
    "Santa Catarina Juquila": 0,
    "San Juan Cacahuatepec": 0
}


def mostrar_resultados(titulo, inicio, objetivo, heuristica):
    print("\n" + titulo)

    camino, costo, nodos = a_estrella(
        mapa, inicio, objetivo, heuristica
    )
    print("\nA*")
    print("Ruta:", " -> ".join(camino) if camino else "No encontrada")
    print("Costo:", costo, "km")
    print("Nodos expandidos:", nodos)

    camino, costo, nodos = busqueda_no_informada(
        mapa, inicio, objetivo
    )
    print("\nBúsqueda no informada")
    print("Ruta:", " -> ".join(camino) if camino else "No encontrada")
    print("Costo:", costo, "km")
    print("Nodos expandidos:", nodos)


# Ruta 1
mostrar_resultados(
    "RUTA 1: PINOTEPA NACIONAL A SANTA CATARINA JUQUILA",
    "Pinotepa Nacional",
    "Santa Catarina Juquila",
    heuristica_juquila
)

# Ruta 2
heuristica_jamiltepec = {
    "Pinotepa Nacional": 30,
    "Pinotepa de Don Luis": 20,
    "Santiago Jamiltepec": 0,
    "Santa Catarina Juquila": 65,
    "San Juan Cacahuatepec": 46
}

mostrar_resultados(
    "RUTA 2: PINOTEPA NACIONAL A SANTIAGO JAMILTEPEC",
    "Pinotepa Nacional",
    "Santiago Jamiltepec",
    heuristica_jamiltepec
)

# Ruta 3
heuristica_pinotepa = {
    "San Juan Cacahuatepec": 32,
    "Pinotepa Nacional": 0,
    "Pinotepa de Don Luis": 0,
    "Santiago Jamiltepec": 0,
    "Santa Catarina Juquila": 0
}

mostrar_resultados(
    "RUTA 3: SAN JUAN CACAHUATEPEC A PINOTEPA NACIONAL",
    "San Juan Cacahuatepec",
    "Pinotepa Nacional",
    heuristica_pinotepa
)