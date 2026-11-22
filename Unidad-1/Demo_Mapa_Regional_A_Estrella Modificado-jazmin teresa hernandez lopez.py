"""
Reconstrucción de la Actividad 2 (búsqueda local).
Cierre de Unidad 1 - Actividad 2 (Demo_A_Estrella_Busqueda_Local.py y
Variante_Optimizacion_Centro_Acopio.py).
OJO: NO son los scripts originales del profesor (Demo_A_Estrella_Busqueda_Local.py y
Variante_Optimizacion_Centro_Acopio.py); son problemas equivalentes escritos para poder llenar las tablas.
"""
import math, random

# ---------- Problema 1: función con varios picos (maximizar) ----------
def f(x):
    return math.sin(x) + 0.5 * math.sin(3 * x) - 0.02 * x ** 2 + 1

def ascenso_de_colina(fun, x0, paso=0.1, lo=-10, hi=10, maximizar=True):
    x = x0
    signo = 1 if maximizar else -1
    while True:
        vecinos = [v for v in (x - paso, x + paso) if lo <= v <= hi]
        mejor = max(vecinos, key=lambda v: signo * fun(v))
        if signo * fun(mejor) <= signo * fun(x):
            return round(x, 2), round(fun(x), 3)
        x = mejor

def temple_simulado(fun, x0, lo=-10, hi=10, maximizar=True, T0=2.0, enfr=0.995, pasos=4000, semilla=1):
    random.seed(semilla)
    signo = 1 if maximizar else -1
    x = x0; mejor_x = x
    T = T0
    for _ in range(pasos):
        nuevo = min(hi, max(lo, x + random.uniform(-1.0, 1.0)))
        d = signo * (fun(nuevo) - fun(x))
        if d > 0 or random.random() < math.exp(d / max(T, 1e-9)):
            x = nuevo
        if signo * fun(x) > signo * fun(mejor_x):
            mejor_x = x
        T *= enfr
    return round(mejor_x, 2), round(fun(mejor_x), 3)

# ---------- Problema 2: centro de acopio (minimizar costo) ----------
# Comunidades sobre una carretera (km) y toneladas que producen.
# Los nombres son poblaciones de la Costa de Oaxaca usadas en la Actividad 1;
# los km y las toneladas son ILUSTRATIVOS (no son distancias reales).
comunidades = [(0, 5), (18, 9), (30, 6), (50, 4), (65, 3)]
nombres = {0: "Pinotepa Nacional", 18: "Santiago Jamiltepec", 30: "Santa María Huazolotitlán",
           50: "Pinotepa de Don Luis", 65: "Santa Catarina Juquila"}
def costo(km):
    return sum(t * abs(km - pos) for pos, t in comunidades)

def reporte(titulo, inicios, corre_colina, corre_temple, fmt, conclusion):
    """Imprime un problema con el mismo formato de la Actividad 1 (A*):
    banner, una sección por algoritmo y una COMPARACIÓN final."""
    print("=" * 68)
    print(titulo)
    print("=" * 68)

    res_c = [corre_colina(x0) for x0 in inicios]
    res_t = [corre_temple(x0) for x0 in inicios]

    print("\n--- Ascenso de colina (solo acepta vecinos mejores) ---")
    for x0, r in zip(inicios, res_c):
        print(f"Desde {x0:>3} : {fmt(r)}")

    print("\n--- Temple simulado (acepta a veces vecinos peores) ---")
    for x0, r in zip(inicios, res_t):
        print(f"Desde {x0:>3} : {fmt(r)}")

    print("\n" + "=" * 68)
    print("COMPARACIÓN")
    print("=" * 68)
    print(f"{'Punto de partida':<20}{'Ascenso de colina':<30}{'Temple simulado':<30}")
    for x0, c, t in zip(inicios, res_c, res_t):
        print(f"{x0:<20}{fmt(c):<30}{fmt(t):<30}")
    cambia_c = len({round(r[0], 1) for r in res_c}) > 1
    cambia_t = len({round(r[0], 1) for r in res_t}) > 1
    print(f"\n¿Cambió con el punto de partida?  colina: {'SÍ' if cambia_c else 'NO'}"
          f"   temple: {'SÍ' if cambia_t else 'NO'}")
    print(conclusion + "\n")
    return res_c


if __name__ == "__main__":
    reporte("PROBLEMA 1: función con varios picos (maximizar)", (-8, 0, 8),
            lambda x0: ascenso_de_colina(f, x0),
            lambda x0: temple_simulado(f, x0),
            lambda r: f"x ≈ {r[0]:.1f}  (f ≈ {r[1]:.3f})",
            "La función NO es cóncava: el ascenso de colina se queda en el pico local\n"
            "más cercano, pero el temple simulado escapa y llega al pico global.")

    res = reporte("PROBLEMA 2: centro de acopio (minimizar costo)", (0, 30, 65),
                  lambda x0: ascenso_de_colina(costo, x0, 0.5, 0, 65, False),
                  lambda x0: temple_simulado(costo, x0, 0, 65, False, T0=50),
                  lambda r: f"km {r[0]:.0f}  (costo {r[1]:.0f})",
                  "El costo es convexo (un solo mínimo): ambos algoritmos llegan al\n"
                  "MISMO resultado sin importar el punto de partida.")
    km, c = res[0]
    print(f"Centro de acopio recomendado: km {km:.0f}, cerca de "
          f"{nombres.get(round(km), 'una comunidad')} (costo {c:.0f})")
