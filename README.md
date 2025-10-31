Escuela Superior de Cómputo
Práctica 4: Divide y Vencerás (DaC)

Materia: Análisis y Diseño de Algoritmos  
Profesor: García Floriano Andrés  
Alumnas: Mata González Elena Carmina, Valderrama López Fanny  
Grupo: 3AV1  


Descripción General
Esta práctica implementa tres algoritmos bajo el paradigma *Divide y Vencerás (DaC)*:
1. Quickselect: encuentra el k-ésimo elemento menor en un arreglo.
2. Conteo de inversiones: determina cuántos pares (i, j) están desordenados en un arreglo.
3. Par de puntos más cercanos: calcula la distancia mínima entre dos puntos en un plano 2D.

Los programas fueron desarrollados en C y Python para analizar diferencias en rendimiento, tiempo de ejecución y uso de memoria.


Objetivo
Aplicar el enfoque de *Divide y Vencerás* en problemas clásicos para comparar su eficiencia computacional y su implementación entre lenguajes de alto y bajo nivel.


Integración y Ejecución
- Lenguajes utilizados: Python 3.11 y C (gcc)
- Librerías principales:`math`, `time`, `random`, `pandas` (para la tabla de resultados en Python).
- Modo de ejecución:
  - Python: `python Practica_4_DaC.py`
  - C: `gcc dac_all.c -o dac_all && ./dac_all`


Resultados Esperados
- Verificar la correcta aplicación del paradigma *Divide y Vencerás*.
- Observar las diferencias de rendimiento entre Python y C.
- Comprobar que los algoritmos presentan la complejidad esperada:
  - Quickselect: O(n) promedio
  - Conteo de inversiones: O(n log n)
  - Par más cercano: O(n log n)


© Escuela Superior de Cómputo — IPN, 2025.
