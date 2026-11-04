-- Ejercicio 3 (más difícil) — Tema 2.3: Funciones
--
-- Si el valor cumple el predicado, aplica la función.
-- Si no lo cumple, devuelve el valor original.

module Ejercicio3 (aplicarSiCumple) where

aplicarSiCumple :: (a -> Bool) -> (a -> a) -> a -> a
aplicarSiCumple pred f x =
    if pred x
        then f x
        else x