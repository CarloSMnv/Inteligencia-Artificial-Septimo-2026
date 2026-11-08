import math
import random


def funcion_objetivo(x):
    return (
        math.sin(x)
        + 0.3 * math.sin(3 * x)
        - 0.05 * (x - 5) ** 2
    )


def ascenso_de_colina(inicio):
    x = inicio
    paso = 0.1
    max_iteraciones = 1000

    for _ in range(max_iteraciones):
        vecinos = [x - paso, x + paso]
        mejor_vecino = max(vecinos, key=funcion_objetivo)

        if funcion_objetivo(mejor_vecino) <= funcion_objetivo(x):
            break

        x = mejor_vecino

    return x, funcion_objetivo(x)


def temple_simulado(inicio):
    x = inicio
    temperatura = 10
    enfriamiento = 0.995
    temperatura_minima = 0.01

    while temperatura > temperatura_minima:
        candidato = x + random.uniform(-0.5, 0.5)
        diferencia = funcion_objetivo(candidato) - funcion_objetivo(x)

        if diferencia > 0:
            x = candidato
        else:
            probabilidad = math.exp(diferencia / temperatura)

            if random.random() < probabilidad:
                x = candidato

        temperatura *= enfriamiento

    return x, funcion_objetivo(x)


# Pruebas desde tres puntos iniciales
inicios = [-8, 0, 8]

print("ASCENSO DE COLINA")
for inicio in inicios:
    x, valor = ascenso_de_colina(inicio)
    print(
        f"Inicio: {inicio} | "
        f"x final: {x:.2f} | "
        f"Valor: {valor:.3f}"
    )

print("\nTEMPLE SIMULADO")
random.seed(42)

for inicio in inicios:
    x, valor = temple_simulado(inicio)
    print(
        f"Inicio: {inicio} | "
        f"x final: {x:.2f} | "
        f"Valor: {valor:.3f}"
    )