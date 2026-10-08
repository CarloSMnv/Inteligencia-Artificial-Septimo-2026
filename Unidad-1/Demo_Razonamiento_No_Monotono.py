"""
Razonamiento monótono vs. no-monótono: el pingüino que no vuela.

MONÓTONO: al agregar información, las conclusiones solo pueden CRECER.
NO-MONÓTONO: al agregar información, una conclusión previa puede RETIRARSE.
"""

# Reglas ESTRICTAS (siempre se cumplen): (si_hecho, entonces_hecho)
ESTRICTAS = [
    ("pingüino", "pájaro"),
    ("pingüino", "no_vuela"),
]
# Reglas POR DEFECTO (suelen cumplirse): (si_hecho, entonces_hecho)
DEFECTO = [
    ("pájaro", "vuela"),
]
CONTRARIO = {"vuela": "no_vuela", "no_vuela": "vuela"}


def cierre_estricto(hechos, reglas):
    """Encadenamiento hacia adelante hasta que no se pueda derivar nada nuevo."""
    concl = set(hechos)
    cambio = True
    while cambio:
        cambio = False
        for si, entonces in reglas:
            if si in concl and entonces not in concl:
                concl.add(entonces)
                cambio = True
    return concl


def razona_monotono(hechos):
    """Lógica clásica: 'pájaro -> vuela' se trata como regla ESTRICTA."""
    return cierre_estricto(hechos, ESTRICTAS + DEFECTO)


def razona_no_monotono(hechos):
    """Primero lo estricto; después los valores por defecto, salvo que haya excepción."""
    concl = cierre_estricto(hechos, ESTRICTAS)
    for si, entonces in DEFECTO:
        if si in concl and CONTRARIO.get(entonces) not in concl:
            concl.add(entonces)
    return concl


def mostrar(titulo, hechos, razonador):
    concl = razonador(hechos)
    inconsistente = any(CONTRARIO.get(c) in concl for c in concl)
    print(f"  Hechos: {sorted(hechos)}")
    print(f"  Conclusiones: {sorted(concl)}", "  <-- ¡CONTRADICCIÓN!" if inconsistente else "")
    return concl


if __name__ == "__main__":
    pasos = [
        ("Paso 1: solo sabemos que Tweety es un pájaro", {"pájaro"}),
        ("Paso 2: llega información nueva: Tweety es un pingüino", {"pájaro", "pingüino"}),
    ]

    print("=" * 66)
    print("RAZONAMIENTO MONÓTONO (lógica clásica)")
    print("=" * 66)
    previas = set()
    for titulo, hechos in pasos:
        print(titulo)
        c = mostrar(titulo, hechos, razona_monotono)
        print("  ¿Se retiró alguna conclusión previa?", bool(previas - c))
        previas = c

    print("\n" + "=" * 66)
    print("RAZONAMIENTO NO-MONÓTONO (reglas por defecto + excepciones)")
    print("=" * 66)
    previas = set()
    for titulo, hechos in pasos:
        print(titulo)
        c = mostrar(titulo, hechos, razona_no_monotono)
        retiradas = previas - c
        print("  Conclusiones retiradas:", sorted(retiradas) if retiradas else "ninguna")
        previas = c

    print("\nIdea clave: el razonamiento no-monótono REVISA creencias ante evidencia")
    print("nueva, como hacemos las personas. El monótono no puede retractarse.")
