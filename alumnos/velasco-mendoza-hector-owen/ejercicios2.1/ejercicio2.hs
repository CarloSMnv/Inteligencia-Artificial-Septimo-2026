
-- Ejercicio 2 (medio) — Tema 2.1: Introducción al modelo funcional
--
-- Implementa agregarAlFinal, que regresa una lista NUEVA
-- con el elemento agregado al final.
-- Ejemplo: agregarAlFinal [1,2,3] 4 == [1,2,3,4]

module Ejercicio2 (agregarAlFinal) where

agregarAlFinal :: [Int] -> Int -> [Int]
agregarAlFinal [] elemento = [elemento]
agregarAlFinal (x:xs) elemento = x : agregarAlFinal xs elemento
