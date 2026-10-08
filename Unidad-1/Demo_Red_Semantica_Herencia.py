"""
Red semántica con herencia de propiedades
Inteligencia Artificial · Unidad 2 · 2.4 Redes semánticas
Instituto Tecnológico de Pinotepa

Una red semántica son nodos (conceptos) unidos por arcos etiquetados (relaciones).
Aquí se guarda como una lista de TRIPLETAS: (sujeto, relación, objeto).

Relaciones:
  es-un             -> clasificación / herencia
  tiene-parte       -> composición
  tiene-propiedad   -> atributo

Idea central: con pocas tripletas declaradas, el sistema INFIERE muchas más
por herencia (compacidad).
"""

RED = [
    ("canario",   "es-un", "pájaro"),
    ("pingüino",  "es-un", "pájaro"),
    ("pájaro",    "es-un", "animal"),
    ("perro",     "es-un", "animal"),
    ("animal",    "tiene-propiedad", "respira"),
    ("pájaro",    "tiene-parte", "alas"),
    ("pájaro",    "tiene-parte", "plumas"),
    ("canario",   "tiene-propiedad", "color amarillo"),
    ("perro",     "tiene-parte", "cola"),
]


def ancestros(nodo, red=RED):
    """Cadena de 'es-un' hacia arriba: canario -> pájaro -> animal."""
    cadena, actual = [], nodo
    while True:
        padre = next((o for s, r, o in red if s == actual and r == "es-un"), None)
        if padre is None:
            return cadena
        cadena.append(padre)
        actual = padre


def conocimiento(nodo, red=RED):
    """Devuelve [(relación, objeto, origen)]: propio o heredado de qué ancestro."""
    resultado = []
    for origen in [nodo] + ancestros(nodo, red):
        for s, r, o in red:
            if s == origen and r != "es-un":
                resultado.append((r, o, "propio" if origen == nodo else f"heredado de «{origen}»"))
    return resultado


if __name__ == "__main__":
    print("=" * 66)
    print("RED SEMÁNTICA: tripletas declaradas:", len(RED))
    print("=" * 66)

    for nodo in ["canario", "pingüino", "perro"]:
        print(f"\n--- Lo que se sabe de «{nodo}» ---")
        print("Cadena es-un:", " -> ".join([nodo] + ancestros(nodo)))
        for r, o, origen in conocimiento(nodo):
            print(f"  {nodo} {r} {o}   ({origen})")

    # Compacidad: cuántos hechos se infieren vs cuántos se declararon
    objetos = {s for s, r, o in RED if r == "es-un"}
    total_inferido = sum(len(conocimiento(n)) for n in objetos)
    print("\n" + "=" * 66)
    print("COMPACIDAD")
    print("=" * 66)
    declaradas_no_clasif = len([t for t in RED if t[1] != "es-un"])
    print(f"Hechos declarados (sin contar es-un): {declaradas_no_clasif}")
    print(f"Hechos que el sistema puede responder para {len(objetos)} objetos: {total_inferido}")
    print("-> Sin herencia habría que escribir cada uno de esos hechos a mano.")

    print("\nPregunta para pensar: según esta red, ¿el pingüino tiene alas?  ->",
          any(o == "alas" for r, o, _ in conocimiento("pingüino")))
