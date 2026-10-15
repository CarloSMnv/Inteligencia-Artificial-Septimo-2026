"""Actividad 2A: función con varios picos.
Funciones y semilla conservadas del archivo Demo_A_Estrella_Busqueda_Local.py
Repositorio del profesor: https://github.com/CarlosMnv/Inteligencia-Artificial-Septimo-2026
"""
import math
import random


def funcion_objetivo(x):
    return math.sin(x) + 0.3 * math.sin(3 * x) - 0.05 * (x - 5) ** 2


def vecinos(x, paso=0.1):
    return [x - paso, x + paso]


def ascenso_de_colina(x_inicial, paso=0.1, max_iter=1000):
    actual = x_inicial
    valor_actual = funcion_objetivo(actual)
    for _ in range(max_iter):
        candidatos = vecinos(actual, paso)
        mejor_vecino = max(candidatos, key=funcion_objetivo)
        valor_vecino = funcion_objetivo(mejor_vecino)
        if valor_vecino <= valor_actual:
            break
        actual, valor_actual = mejor_vecino, valor_vecino
    return actual, valor_actual


def temple_simulado(x_inicial, temp_inicial=10.0, enfriamiento=0.995, temp_minima=0.01):
    actual = x_inicial
    valor_actual = funcion_objetivo(actual)
    mejor, valor_mejor = actual, valor_actual
    temperatura = temp_inicial
    while temperatura > temp_minima:
        candidato = actual + random.uniform(-0.5, 0.5)
        valor_candidato = funcion_objetivo(candidato)
        delta = valor_candidato - valor_actual
        if delta > 0 or random.random() < math.exp(delta / temperatura):
            actual, valor_actual = candidato, valor_candidato
            if valor_actual > valor_mejor:
                mejor, valor_mejor = actual, valor_actual
        temperatura *= enfriamiento
    return mejor, valor_mejor


if __name__ == "__main__":
    print("ACTIVIDAD 2A - FUNCIÓN CON VARIOS PICOS")
    print("ASCENSO DE COLINA")
    for x0 in [-8, 0, 8]:
        x, f = ascenso_de_colina(x0)
        print(f"Inicio x={x0:>3}: x final = {x:6.2f} | f(x) = {f:.3f}")
    print("\nTEMPLE SIMULADO (semilla 42)")
    random.seed(42)
    for x0 in [-8, 0, 8]:
        x, f = temple_simulado(x0)
        print(f"Inicio x={x0:>3}: x final = {x:6.2f} | f(x) = {f:.3f}")
