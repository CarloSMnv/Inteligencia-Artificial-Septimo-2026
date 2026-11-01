-- Ejercicio 2 (medio) — Tema 2.3: Funciones
--
-- Implementa `componer`, que recibe dos funciones `f` y `g`
-- y regresa una función nueva que aplica primero `g` y luego `f`.

module Ejercicio2 (componer) where

componer :: (b -> c) -> (a -> b) -> a -> c
componer f g x = f (g x)