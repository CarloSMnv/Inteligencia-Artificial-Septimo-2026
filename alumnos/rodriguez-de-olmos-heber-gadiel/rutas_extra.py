import copy
from Demo_Mapa_Regional_A_Estrella import (
    a_estrella, busqueda_no_informada, mapa, heuristica_hacia_juquila
)

META = "Santa Catarina Juquila"


def correr(titulo, grafo, heuristica, inicio, meta):
    camino_a, costo_a, exp_a, _ = a_estrella(grafo, heuristica, inicio, meta)
    camino_b, costo_b, exp_b, _ = busqueda_no_informada(grafo, inicio, meta)
    print("=" * 70)
    print(titulo)
    print("=" * 70)
    print("Ruta A*          :", " -> ".join(camino_a))
    print("Costo (km)       :", costo_a)
    print("Nodos A*         :", exp_a)
    print("Nodos no informada:", exp_b, "| costo:", costo_b)
    print()


# ---- Ruta 2: otro inicio ----
correr("RUTA 2: Pinotepa de Don Luis -> Juquila",
       mapa, heuristica_hacia_juquila, "Pinotepa de Don Luis", META)

# ---- Ruta 3: se agrega Puerto Escondido ----
mapa3 = copy.deepcopy(mapa)
h3 = dict(heuristica_hacia_juquila)

mapa3["Puerto Escondido"] = [("Santiago Jamiltepec", 110), ("Santa Catarina Juquila", 98)]
mapa3["Santiago Jamiltepec"].append(("Puerto Escondido", 110))
mapa3["Santa Catarina Juquila"].append(("Puerto Escondido", 98))
h3["Puerto Escondido"] = 48   # línea recta a Juquila (aprox.)

correr("RUTA 3: Pinotepa Nacional -> Juquila (con Puerto Escondido)",
       mapa3, h3, "Pinotepa Nacional", META)