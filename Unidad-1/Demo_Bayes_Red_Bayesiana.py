"""
Teorema de Bayes y red bayesiana de diagnóstico
Inteligencia Artificial · Unidad 2 · 2.7 y 2.8 · Reto R2.4
Instituto Tecnológico de Pinotepa

Solo usa la biblioteca estándar de Python (no necesitas instalar nada).

PARTE 1: Teorema de Bayes (el examen "muy preciso" que se equivoca el 50 %).
PARTE 2: Red bayesiana de diagnóstico de una computadora que no arranca,
         con inferencia por ENUMERACIÓN (suma sobre todas las combinaciones).
"""
from itertools import product


# =====================================================================
# PARTE 1 · TEOREMA DE BAYES
# =====================================================================
def bayes(prior, sensibilidad, especificidad):
    """P(A|B) = P(B|A)·P(A) / P(B)
    prior          = P(A)        (qué tan común es la enfermedad)
    sensibilidad   = P(B|A)      (positivo si SÍ la tiene)
    especificidad  = P(¬B|¬A)    (negativo si NO la tiene)
    """
    p_b_dado_a = sensibilidad
    p_b_dado_no_a = 1 - especificidad                      # falsos positivos
    p_b = p_b_dado_a * prior + p_b_dado_no_a * (1 - prior)  # probabilidad total de la evidencia
    return p_b_dado_a * prior / p_b


def parte1():
    print("=" * 68)
    print("PARTE 1 · TEOREMA DE BAYES")
    print("=" * 68)
    post = bayes(prior=0.01, sensibilidad=0.99, especificidad=0.99)
    print(f"Examen de 99 % de sensibilidad y 99 % de especificidad, enfermedad del 1 %:")
    print(f"  P(enfermo | positivo) = {post:.4f}  ->  {post:.0%}\n")

    print("Mismo examen, distinta frecuencia de la enfermedad (la probabilidad PREVIA importa):")
    print(f"  {'Prevalencia':<14}{'P(enfermo | positivo)':<24}")
    for prev in [0.001, 0.01, 0.10, 0.50]:
        print(f"  {prev:<14.1%}{bayes(prev, 0.99, 0.99):<24.1%}")

    print("\nEn frecuencias naturales (10,000 personas):")
    enfermos = 10000 * 0.01
    sanos = 10000 - enfermos
    vp, fp = enfermos * 0.99, sanos * 0.01
    print(f"  Enfermos: {enfermos:.0f} -> dan positivo: {vp:.0f}")
    print(f"  Sanos:    {sanos:.0f} -> dan positivo (falsos positivos): {fp:.0f}")
    print(f"  De {vp + fp:.0f} positivos, solo {vp:.0f} están realmente enfermos = {vp/(vp+fp):.0%}")


# =====================================================================
# PARTE 2 · RED BAYESIANA
# =====================================================================
# Cada nodo: lista de padres y su tabla de probabilidad condicional (CPT):
#   cpt[(valores de los padres)] = P(nodo = verdadero | padres)
# Los nodos están en ORDEN TOPOLÓGICO (los padres aparecen antes que los hijos).
RED = {
    "Fuente":        {"padres": [],                  "cpt": {(): 0.08}},     # falla de la fuente de poder
    "Disco":         {"padres": [],                  "cpt": {(): 0.05}},     # falla del disco duro
    "LucesApagadas": {"padres": ["Fuente"],          "cpt": {(True,): 0.95, (False,): 0.02}},
    "RuidoDisco":    {"padres": ["Disco"],           "cpt": {(True,): 0.80, (False,): 0.03}},
    "NoArranca":     {"padres": ["Fuente", "Disco"], "cpt": {(True, True): 0.99, (True, False): 0.95,
                                                             (False, True): 0.90, (False, False): 0.02}},
}


def prob_nodo(red, nodo, valor, asignacion):
    """P(nodo = valor | sus padres, según la asignación)."""
    info = red[nodo]
    clave = tuple(asignacion[p] for p in info["padres"])
    p_verdadero = info["cpt"][clave]
    return p_verdadero if valor else 1 - p_verdadero


def prob_conjunta(red, asignacion):
    """P(todas las variables) = producto de P(nodo | padres)."""
    p = 1.0
    for nodo in red:
        p *= prob_nodo(red, nodo, asignacion[nodo], asignacion)
    return p


def consulta(red, variable, evidencia):
    """P(variable = verdadero | evidencia), por enumeración de todas las combinaciones."""
    nodos = list(red)
    num = den = 0.0
    for valores in product([True, False], repeat=len(nodos)):
        asig = dict(zip(nodos, valores))
        if any(asig[k] != v for k, v in evidencia.items()):
            continue                      # esta combinación contradice la evidencia
        p = prob_conjunta(red, asig)
        den += p
        if asig[variable]:
            num += p
    return num / den


def parte2():
    print("\n" + "=" * 68)
    print("PARTE 2 · RED BAYESIANA: ¿POR QUÉ NO ARRANCA LA COMPUTADORA?")
    print("=" * 68)

    # --- Autoverificación: la enumeración debe coincidir con un cálculo manual ---
    p_f, p_d = RED["Fuente"]["cpt"][()], RED["Disco"]["cpt"][()]
    p_a_manual = 0.0
    for f, d in product([True, False], repeat=2):
        pf = p_f if f else 1 - p_f
        pd = p_d if d else 1 - p_d
        p_a_manual += pf * pd * RED["NoArranca"]["cpt"][(f, d)]
    # P(NoArranca) por enumeración = P(NoArranca | sin evidencia) calculado con 'consulta'
    assert abs(consulta(RED, "NoArranca", {}) - p_a_manual) < 1e-12, "La enumeración no coincide"

    escenarios = [
        ("Sin evidencia (probabilidades previas)",                     {}),
        ("Evidencia: no arranca",                                      {"NoArranca": True}),
        ("+ las luces están apagadas",                                 {"NoArranca": True, "LucesApagadas": True}),
        ("+ se oye ruido en el disco (y luces apagadas)",              {"NoArranca": True, "LucesApagadas": True, "RuidoDisco": True}),
        ("Solo: no arranca + ruido en el disco (luces encendidas)",    {"NoArranca": True, "LucesApagadas": False, "RuidoDisco": True}),
    ]
    print(f"{'Evidencia observada':<58}{'P(Fuente)':>10}{'P(Disco)':>10}")
    print("-" * 78)
    for titulo, ev in escenarios:
        print(f"{titulo:<58}{consulta(RED, 'Fuente', ev):>10.1%}{consulta(RED, 'Disco', ev):>10.1%}")

    print("\nOBSERVA: al saber que las luces están apagadas, P(Fuente) sube y P(Disco) BAJA:")
    print("la fuente 'explica' por sí sola que no arranque (explaining away).")


if __name__ == "__main__":
    parte1()
    parte2()
