"""
Variante regional del problema de optimización para búsqueda local
Ubicación óptima de un centro de acopio a lo largo de la carretera

Cuatro comunidades productoras están a distintos kilómetros sobre una misma
carretera. Cada una genera una cantidad distinta de producto que hay que
transportar al centro de acopio. Buscamos el punto sobre la carretera (km)
que MINIMIZA el costo total de transporte (distancia x volumen de cada
comunidad hasta el centro).

Esto reutiliza EXACTAMENTE las mismas funciones ascenso_de_colina y
temple_simulado del script anterior -- solo cambia la función objetivo.
"""

import math
import random

# (posición en km sobre la carretera, volumen de producto en toneladas/mes)
comunidades = [
    (0,  12),   # Comunidad A, km 0
    (18, 25),   # Comunidad B, km 18 (ej. Pinotepa de Don Luis)
    (30, 18),   # Comunidad C, km 30 (ej. Santiago Jamiltepec)
    (65, 8),    # Comunidad D, km 65 (ej. Santa Catarina Juquila)
]


def costo_transporte(x):
    """Costo total = suma de (distancia al centro) x (volumen) de cada comunidad.
    Como es un COSTO, lo que queremos es MINIMIZAR -- así que para reutilizar
    el mismo 'ascenso de colina' (que maximiza), devolvemos el costo en negativo."""
    total = sum(abs(x - km) * vol for km, vol in comunidades)
    return -total  # negativo: maximizar esto = minimizar el costo real


def vecinos(x, paso=0.5):
    return [x - paso, x + paso]


def ascenso_de_colina(x_inicial, paso=0.5, max_iter=2000):
    actual = x_inicial
    valor_actual = costo_transporte(actual)
    for _ in range(max_iter):
        candidatos = vecinos(actual, paso)
        mejor_vecino = max(candidatos, key=costo_transporte)
        valor_vecino = costo_transporte(mejor_vecino)
        if valor_vecino <= valor_actual:
            break
        actual, valor_actual = mejor_vecino, valor_vecino
    return actual, -valor_actual  # regresamos el costo real (positivo)


def temple_simulado(x_inicial, temp_inicial=50.0, enfriamiento=0.995, temp_minima=0.01):
    actual = x_inicial
    valor_actual = costo_transporte(actual)
    mejor, valor_mejor = actual, valor_actual
    temperatura = temp_inicial
    while temperatura > temp_minima:
        candidato = actual + random.uniform(-2, 2)
        candidato = max(0, min(65, candidato))  # no salirse de la carretera
        valor_candidato = costo_transporte(candidato)
        delta = valor_candidato - valor_actual
        if delta > 0 or random.random() < math.exp(delta / temperatura):
            actual, valor_actual = candidato, valor_candidato
            if valor_actual > valor_mejor:
                mejor, valor_mejor = actual, valor_actual
        temperatura *= enfriamiento
    return mejor, -valor_mejor


if __name__ == "__main__":
    print("Comunidades (km, toneladas/mes):", comunidades)
    print()
    for x0 in [0, 30, 65]:
        xa, ca = ascenso_de_colina(x0)
        print(f"Ascenso de colina desde km {x0:>3}: centro óptimo en km {xa:6.2f}  (costo: {ca:8.1f} ton*km)")
    print()
    random.seed(7)
    for x0 in [0, 30, 65]:
        xt, ct = temple_simulado(x0)
        print(f"Temple simulado  desde km {x0:>3}: centro óptimo en km {xt:6.2f}  (costo: {ct:8.1f} ton*km)")
