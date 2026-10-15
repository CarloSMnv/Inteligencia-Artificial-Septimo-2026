"""Actividad 2B: optimización del centro de acopio.
Funciones y semilla conservadas del archivo Variante_Optimizacion_Centro_Acopio.py
Repositorio del profesor: https://github.com/CarlosMnv/Inteligencia-Artificial-Septimo-2026
"""
import math
import random

# (kilómetro, volumen de producto en toneladas/mes)
comunidades = [(0, 12), (18, 25), (30, 18), (65, 8)]


def costo_transporte(x):
    total = sum(abs(x - km) * vol for km, vol in comunidades)
    return -total  # maximizar el negativo equivale a minimizar el costo


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
    return actual, -valor_actual


def temple_simulado(x_inicial, temp_inicial=50.0, enfriamiento=0.995, temp_minima=0.01):
    actual = x_inicial
    valor_actual = costo_transporte(actual)
    mejor, valor_mejor = actual, valor_actual
    temperatura = temp_inicial
    while temperatura > temp_minima:
        candidato = actual + random.uniform(-2, 2)
        candidato = max(0, min(65, candidato))
        valor_candidato = costo_transporte(candidato)
        delta = valor_candidato - valor_actual
        if delta > 0 or random.random() < math.exp(delta / temperatura):
            actual, valor_actual = candidato, valor_candidato
            if valor_actual > valor_mejor:
                mejor, valor_mejor = actual, valor_actual
        temperatura *= enfriamiento
    return mejor, -valor_mejor


if __name__ == "__main__":
    print("ACTIVIDAD 2B - CENTRO DE ACOPIO")
    print("ASCENSO DE COLINA")
    for km in [0, 30, 65]:
        centro, costo = ascenso_de_colina(km)
        print(f"Inicio km {km:>2}: centro = km {centro:5.2f} | costo = {costo:.1f} ton*km")
    print("\nTEMPLE SIMULADO (semilla 7)")
    random.seed(7)
    for km in [0, 30, 65]:
        centro, costo = temple_simulado(km)
        print(f"Inicio km {km:>2}: centro = km {centro:5.2f} | costo = {costo:.1f} ton*km")
