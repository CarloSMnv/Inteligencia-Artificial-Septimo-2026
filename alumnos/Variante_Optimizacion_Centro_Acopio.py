import random
import math


# Datos: (kilómetro, toneladas mensuales)
comunidades = [
    (0, 12),
    (18, 25),
    (30, 18),
    (65, 8)
]


def costo_transporte(x):
    costo = 0

    for km, toneladas in comunidades:
        costo += abs(x - km) * toneladas

    return costo


# Se maximiza el negativo del costo para encontrar
# la ubicación que minimiza el transporte.
def funcion_objetivo(x):
    return -costo_transporte(x)


def ascenso_de_colina(inicio):
    x = inicio
    paso = 0.5
    max_iteraciones = 1000

    for _ in range(max_iteraciones):
        vecinos = [
            max(0, min(65, x - paso)),
            max(0, min(65, x + paso))
        ]

        mejor_vecino = max(vecinos, key=funcion_objetivo)

        if funcion_objetivo(mejor_vecino) <= funcion_objetivo(x):
            break

        x = mejor_vecino

    return x, costo_transporte(x)


def temple_simulado(inicio):
    x = inicio
    temperatura = 50
    enfriamiento = 0.995
    temperatura_minima = 0.01

    while temperatura > temperatura_minima:
        candidato = x + random.uniform(-2, 2)
        candidato = max(0, min(65, candidato))

        diferencia = funcion_objetivo(candidato) - funcion_objetivo(x)

        if diferencia > 0:
            x = candidato
        else:
            probabilidad = math.exp(diferencia / temperatura)

            if random.random() < probabilidad:
                x = candidato

        temperatura *= enfriamiento

    return x, costo_transporte(x)


# Pruebas desde los kilómetros 0, 30 y 65
inicios = [0, 30, 65]

print("ASCENSO DE COLINA")
for inicio in inicios:
    x, costo = ascenso_de_colina(inicio)
    print(
        f"Inicio: {inicio} km | "
        f"Ubicación final: {x:.2f} km | "
        f"Costo: {costo:.2f}"
    )

print("\nTEMPLE SIMULADO")
random.seed(7)

for inicio in inicios:
    x, costo = temple_simulado(inicio)
    print(
        f"Inicio: {inicio} km | "
        f"Ubicación final: {x:.2f} km | "
        f"Costo: {costo:.2f}"
    )