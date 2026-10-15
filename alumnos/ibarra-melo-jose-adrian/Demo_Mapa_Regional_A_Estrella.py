"""
Comparación A* vs. búsqueda no informada sobre un mapa de la región
Inteligencia Artificial · Unidad 1 · Actividad de cierre
Instituto Tecnológico de Pinotepa

Ruta: Pinotepa Nacional -> Orizaba, Veracruz

Poblaciones principales de la ruta:

  Pinotepa Nacional
  San Juan Cacahuatepec
  Putla Villa de Guerrero
  San Andrés Chicahuaxtla
  Heroica Ciudad de Tlaxiaco
  Yucudaa
  Heroica Ciudad de Huajuapan de León
  Santa María Camotlán
  Cuyotepeji
  Santiago Miltepec
  Santiago Chazumba
  Tehuacán (Santa María Coapan)
  Santiago Miahuatlán
  Acultzingo
  Ciudad Mendoza
  Nogales
  Río Blanco
  Orizaba

Heurística h(n):
Distancia aproximada en línea recta desde cada población hacia
Orizaba, Veracruz.

A* utiliza esta información para orientar la búsqueda hacia la meta,
mientras que la búsqueda no informada solamente utiliza el costo
acumulado de los caminos recorridos.
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

            heapq.heappush(
                frontera,
                (
                    nuevo_f,
                    vecino,
                    camino + [vecino],
                    nuevo_g
                )
            )

    return None, float("inf"), nodos_expandidos, orden_expansion


def busqueda_no_informada(grafo, inicio, meta):
    """
    Búsqueda de costo uniforme SIN heurística.
    h(n) = 0 para todos los nodos.
    """

    heuristica_cero = {nodo: 0 for nodo in grafo}

    return a_estrella(
        grafo,
        heuristica_cero,
        inicio,
        meta
    )


# ============================================================
# MAPA
# Ruta Pinotepa Nacional -> Orizaba
# ============================================================
# Grafo no dirigido:
# se agregan conexiones en ambas direcciones.

mapa = {

    "Pinotepa Nacional": [
        ("San Juan Cacahuatepec", 38)
    ],

    "San Juan Cacahuatepec": [
        ("Pinotepa Nacional", 38),
        ("Putla Villa de Guerrero", 70)
    ],

    "Putla Villa de Guerrero": [
        ("San Juan Cacahuatepec", 70),
        ("San Andres Chicahuaxtla", 35)
    ],

    "San Andres Chicahuaxtla": [
        ("Putla Villa de Guerrero", 35),
        ("Heroica Ciudad de Tlaxiaco", 45)
    ],

    "Heroica Ciudad de Tlaxiaco": [
        ("San Andres Chicahuaxtla", 45),
        ("Yucudaa", 32)
    ],

    "Yucudaa": [
        ("Heroica Ciudad de Tlaxiaco", 32),
        ("Heroica Ciudad de Huajuapan de Leon", 92)
    ],

    "Heroica Ciudad de Huajuapan de Leon": [
        ("Yucudaa", 92),
        ("Santa Maria Camotlan", 8)
    ],

    "Santa Maria Camotlan": [
        ("Heroica Ciudad de Huajuapan de Leon", 8),
        ("Cuyotepeji", 18)
    ],

    "Cuyotepeji": [
        ("Santa Maria Camotlan", 18),
        ("Santiago Miltepec", 20)
    ],

    "Santiago Miltepec": [
        ("Cuyotepeji", 20),
        ("Santiago Chazumba", 30)
    ],

    "Santiago Chazumba": [
        ("Santiago Miltepec", 30),
        ("Tehuacan", 55)
    ],

    "Tehuacan": [
        ("Santiago Chazumba", 55),
        ("Santiago Miahuatlan", 18)
    ],

    "Santiago Miahuatlan": [
        ("Tehuacan", 18),
        ("Acultzingo", 55)
    ],

    "Acultzingo": [
        ("Santiago Miahuatlan", 55),
        ("Ciudad Mendoza", 25)
    ],

    "Ciudad Mendoza": [
        ("Acultzingo", 25),
        ("Nogales", 7)
    ],

    "Nogales": [
        ("Ciudad Mendoza", 7),
        ("Rio Blanco", 5)
    ],

    "Rio Blanco": [
        ("Nogales", 5),
        ("Orizaba", 8)
    ],

    "Orizaba": [
        ("Rio Blanco", 8)
    ]
}


# ============================================================
# HEURÍSTICA HACIA ORIZABA
# ============================================================
# h(n) representa una distancia aproximada en línea recta
# desde cada población hasta Orizaba.
#
# Mientras más cerca esté la población de Orizaba,
# menor será su valor heurístico.

heuristica_hacia_orizaba = {

    "Pinotepa Nacional": 400,

    "San Juan Cacahuatepec": 370,

    "Putla Villa de Guerrero": 320,

    "San Andres Chicahuaxtla": 290,

    "Heroica Ciudad de Tlaxiaco": 260,

    "Yucudaa": 230,

    "Heroica Ciudad de Huajuapan de Leon": 190,

    "Santa Maria Camotlan": 180,

    "Cuyotepeji": 165,

    "Santiago Miltepec": 150,

    "Santiago Chazumba": 130,

    "Tehuacan": 75,

    "Santiago Miahuatlan": 65,

    "Acultzingo": 35,

    "Ciudad Mendoza": 20,

    "Nogales": 15,

    "Rio Blanco": 8,

    "Orizaba": 0
}


# ============================================================
# PROGRAMA PRINCIPAL
# ============================================================

if __name__ == "__main__":

    inicio = "Pinotepa Nacional"
    meta = "Orizaba"

    print("=" * 75)
    print(f"RUTA: {inicio} -> {meta}, Veracruz")
    print("=" * 75)


    # ========================================================
    # ALGORITMO A*
    # ========================================================

    camino_a, costo_a, exp_a, orden_a = a_estrella(
        mapa,
        heuristica_hacia_orizaba,
        inicio,
        meta
    )

    print("\n--- A* (con heurística) ---")

    print("\nRuta encontrada:")

    print(" -> ".join(camino_a))

    print("\nCosto total     :", costo_a, "km")

    print("Nodos expandidos:", exp_a)

    print("Orden de expansión:")

    print(orden_a)


    # ========================================================
    # BÚSQUEDA NO INFORMADA
    # ========================================================

    camino_b, costo_b, exp_b, orden_b = busqueda_no_informada(
        mapa,
        inicio,
        meta
    )

    print(
        "\n--- Búsqueda no informada "
        "(costo uniforme, sin heurística) ---"
    )

    print("\nRuta encontrada:")

    print(" -> ".join(camino_b))

    print("\nCosto total     :", costo_b, "km")

    print("Nodos expandidos:", exp_b)

    print("Orden de expansión:")

    print(orden_b)


    # ========================================================
    # COMPARACIÓN
    # ========================================================

    print("\n" + "=" * 75)

    print("COMPARACIÓN")

    print("=" * 75)

    print(
        f"{'Algoritmo':<28}"
        f"{'Costo (km)':<14}"
        f"{'Nodos expandidos':<18}"
    )

    print(
        f"{'A* (informada)':<28}"
        f"{costo_a:<14}"
        f"{exp_a:<18}"
    )

    print(
        f"{'No informada':<28}"
        f"{costo_b:<14}"
        f"{exp_b:<18}"
    )


    # ========================================================
    # CONCLUSIÓN
    # ========================================================

    print("\nCONCLUSIÓN:")

    print(
        "A* utiliza la distancia estimada hacia Orizaba "
        "para decidir qué población explorar primero."
    )

    print(
        "La búsqueda no informada no conoce la dirección "
        "de la meta y solamente considera el costo acumulado."
    )

    print(
        "Ambos algoritmos buscan encontrar la ruta de menor "
        "costo entre Pinotepa Nacional y Orizaba."
    )