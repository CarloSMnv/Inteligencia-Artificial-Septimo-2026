
-- Ejercicio 3 (más difícil) — Tema 2.1: Introducción al modelo funcional
--
-- Implementa aplicarNVeces, que aplica una función pura f,
-- n veces seguidas sobre un valor inicial x.
-- Ejemplo: aplicarNVeces 3 (*2) 1 == 8

module Ejercicio3 (aplicarNVeces) where

aplicarNVeces :: Int -> (a -> a) -> a -> a
aplicarNVeces n f x
    | n <= 0    = x
    | otherwise = aplicarNVeces (n - 1) f (f x)
