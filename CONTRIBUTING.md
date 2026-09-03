# Guía de contribución para alumnos

Este repositorio se usa para practicar el flujo de trabajo real de Git/GitHub mientras entregan actividades. Sigan estos pasos para cada entrega.

## 1. Clonar el repositorio (solo la primera vez)

```bash
git clone https://github.com/CarloSMnv/Inteligencia-Artificial-Septimo-2026.git
cd Inteligencia-Artificial-Septimo-2026
```

## 2. Actualizar su copia local antes de empezar

```bash
git checkout main
git pull origin main
```

## 3. Crear una rama para la actividad

Usen el patrón `actividadN-su-nombre-de-carpeta` (el mismo nombre que su carpeta en `alumnos/`):

```bash
git checkout -b actividad1-nombre-apellido
```

## 4. Trabajar únicamente dentro de su carpeta

Su carpeta ya existe en `alumnos/<su-nombre>/`. Agreguen ahí sus archivos. No editen ni borren carpetas de otros compañeros ni archivos fuera de `alumnos/`.

## 5. Confirmar los cambios (commit)

```bash
git add alumnos/<su-nombre>/
git commit -m "Actividad 1: breve descripción de lo que entregas"
```

Mensajes de commit claros y descriptivos — evitar mensajes como "cambios" o "update".

## 6. Subir la rama

```bash
git push origin actividad1-nombre-apellido
```

## 7. Abrir un Pull Request

En GitHub, abran un Pull Request de su rama hacia `main`, describiendo brevemente qué actividad entregan. El profesor revisará y aprobará (o pedirá cambios) antes de mergear.

## Reglas

- No se permite hacer push directo a `main`; todo cambio entra por Pull Request.
- Cada actividad nueva puede ir en una rama nueva o reutilizar la misma rama de trabajo, según indique el profesor.
- Si su Pull Request tiene conflictos, deben resolverlos localmente (`git pull origin main` dentro de su rama y arreglar los conflictos) antes de que se pueda aprobar.
- Ante dudas de Git, revisen la [documentación oficial](https://git-scm.com/doc) o consulten en clase.
