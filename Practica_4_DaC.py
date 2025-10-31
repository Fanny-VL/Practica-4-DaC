import random
import time
import tracemalloc
import pandas as pd
import math
from collections import namedtuple
import warnings

warnings.filterwarnings("ignore", category=RuntimeWarning) # Ignorar advertencias de tiempo de ejecución.


# ----> Quick Select (DaC) para k-ésimo elemento más pequeño <----

def encontrar_k_esimo_menor(arr, k):
    """
    Encuentra el k-ésimo elemento más pequeño en un arreglo 'arr'.
    'k' es 1-indexado (ej. k=1 es el más pequeño, k=5 es el 5to más pequeño).

    Args:
        arr (list): Lista de números.
        k (int): La posición del elemento a encontrar (1-indexado).
    """
    # Convertimos k a 0-indexado para el algoritmo.
    k_index = k - 1
    
    # Copiamos para no modificar el arreglo original.
    arr_copia = list(arr)
    
    return quick_select(arr_copia, 0, len(arr_copia) - 1, k_index) 
    # 0 = índice inicial, índice final = len(arr)-1, k_index = índice del k-ésimo elemento.
 

def quick_select(arr, izquierda, derecha, k_index):
    """
    Función recursiva de DaC que busca el k_index en el sub-arreglo.

    Args:
        arr (list): Lista de números.
        izquierda (int): Índice izquierdo del sub-arreglo.
        derecha (int): Índice derecho del sub-arreglo.
        k_index (int): Índice del k-ésimo elemento a encontrar (0-indexado).
    """
    # -> Caso Base <-
    # Si el sub-arreglo tiene un solo elemento, es el que buscamos.
    if izquierda == derecha:
        return arr[izquierda]
    
    # -> Divide <-
    # Elige un pivote (aquí uno aleatorio para buen rendimiento promedio).
    pivote_idx_aleatorio = random.randint(izquierda, derecha)

    # Mueve el pivote al final para facilitar la partición.
    arr[pivote_idx_aleatorio], arr[derecha] = arr[derecha], arr[pivote_idx_aleatorio]
    
    # Llama a la partición.
    pivote_idx_final = particion(arr, izquierda, derecha)
    
    # -> Vence y Combina (Selecciona) <-
    # Compara el índice del pivote con k_index.
    if k_index == pivote_idx_final:
        # Hemos encontrado, el pivote está en la posición k que buscábamos.
        return arr[k_index]
    
    # Si no, decide en qué sub-arreglo continuar la búsqueda.
    elif k_index < pivote_idx_final:
        # El k-ésimo elemento está en el sub-arreglo de la izquierda.
        return quick_select(arr, izquierda, pivote_idx_final - 1, k_index)
    else:
        # El k-ésimo elemento está en el sub-arreglo de la derecha.
        return quick_select(arr, pivote_idx_final + 1, derecha, k_index) # regresa el valor encontrado en la llamada recursiva.

def particion(arr, izquierda, derecha):
    """
    Función auxiliar de Quick Sort. 
    Mueve todos los elementos menores que el pivote a su izquierda
    y los mayores a su derecha. Devuelve el índice final del pivote.

    Args:
        arr (list): Lista de números.
        izquierda (int): Índice izquierdo del sub-arreglo.
        derecha (int): Índice derecho del sub-arreglo.
    """
    # Elegimos el pivote como el último elemento del sub-arreglo.
    pivote_valor = arr[derecha]
    # Inicializamos el puntero para los menores.
    puntero_menores = izquierda
    
    # Recorremos el sub-arreglo y reordenamos.
    for i in range(izquierda, derecha):
        
        if arr[i] < pivote_valor:
            # Encontramos un elemento menor, lo movemos a la parte izquierda
            arr[i], arr[puntero_menores] = arr[puntero_menores], arr[i]
            puntero_menores += 1
            
    # Coloca el pivote en su posición final correcta
    arr[puntero_menores], arr[derecha] = arr[derecha], arr[puntero_menores]
    return puntero_menores # Devuelve el índice del pivote.

# ----> Contar inversiones usando DaC <----

def contar_inversiones(arr):
    """
    Función principal que inicia el conteo de inversiones.
    Devuelve solo el número total de inversiones.

    Args:
        arr (list): Lista de números.
    """
    # Llama a la función recursiva auxiliar
    _, conteo_total = _merge_sort_y_contar(list(arr))
    return conteo_total

def _merge_sort_y_contar(arr):
    """
    Función recursiva de DaC que devuelve dos cosas:
    1. Una versión ordenada del arreglo 'arr'.
    2. El número de inversiones dentro de 'arr'.

    Args:
        arr (list): Lista de números.
    """
    # -> Caso Base <-
    # Un arreglo de 0 o 1 elemento no tiene inversiones y ya está ordenado.
    if len(arr) <= 1:
        return arr, 0
    
    # -> Divide <-
    medio = len(arr) // 2
    mitad_izquierda = arr[:medio]
    mitad_derecha = arr[medio:]
    
    # -> Vence (Recursión) <-
    # Llama recursivamente para ordenar cada mitad y contar sus inversiones internas.
    izquierda_ordenada, inv_izquierda = _merge_sort_y_contar(mitad_izquierda)
    derecha_ordenada, inv_derecha = _merge_sort_y_contar(mitad_derecha)
    
    # -> Combina <-
    # Fusiona las dos mitades ordenadas y cuenta las "inversiones divididas".
    arr_fusionado = []
    inv_divididas = 0
    
    i = 0 # Puntero para la mitad izquierda.
    j = 0 # Puntero para la mitad derecha.
    
    # Recorremos ambas mitades y las fusionamos.
    while i < len(izquierda_ordenada) and j < len(derecha_ordenada): # Mientras haya elementos en ambas mitades.
        # Comparamos los elementos actuales de ambas mitades.
        if izquierda_ordenada[i] <= derecha_ordenada[j]:
            # No hay inversión, el elemento de la izquierda es más pequeño.
            arr_fusionado.append(izquierda_ordenada[i]) # utilizamos .append para agregar el elemento a la lista fusionada.
            i += 1 # Avanzamos el puntero de la mitad izquierda.
        else:
            # Inversión encontrada.
            # Si arr[i] > arr[j], entonces arr[i] también es mayor que
            # TODOS los elementos restantes en la mitad izquierda, porque 
            # la mitad izquierda ya está ordenada.
            arr_fusionado.append(derecha_ordenada[j])
            inv_divididas += (len(izquierda_ordenada) - i) # Contamos las inversiones.
            j += 1 # Avanzamos el puntero de la mitad derecha.
            
    # Añadir los elementos restantes de cualquiera de las listas,
    # usando extend para agregar múltiples elementos a la lista fusionada.
    arr_fusionado.extend(izquierda_ordenada[i:]) 
    arr_fusionado.extend(derecha_ordenada[j:]) 
    
    # El total de inversiones es la suma de las tres partes.
    conteo_total = inv_izquierda + inv_derecha + inv_divididas
    
    return arr_fusionado, conteo_total # Devuelve el arreglo fusionado y el conteo total de inversiones.

# ----> Par de puntos mas cercanos DaC en 2D <----

# Usamos namedtuple para que el código sea más legible
Point = namedtuple('Point', ['x', 'y']) # Definimos un punto en 2D.

def distancia_euclidiana(p1, p2):
    """Calcula la distancia euclidiana entre dos puntos.
    
    Args:
        p1 (Point): Primer punto.
        p2 (Point): Segundo punto.
    """
    return math.dist((p1.x, p1.y), (p2.x, p2.y)) # Usamos math.dist para calcular la distancia euclidiana.

def encontrar_par_mas_cercano(puntos):
    """
    Función principal que inicia la búsqueda.
    'puntos' debe ser una lista de tuplas (x, y) o Puntos.

    Args:
        puntos (list): Lista de puntos en 2D.
    """

    # Convertir a Puntos si son tuplas.
    puntos_obj = [Point(p[0], p[1]) for p in puntos]
    
    # -> Pre-procesamiento <-
    # El algoritmo DaC requiere que los puntos estén ordenados por la cordenada 'x'.
    px = sorted(puntos_obj, key=lambda p: p.x)
    
    return _closest_pair_recursive(px) 

def _closest_pair_recursive(px):
    """
    Función recursiva de DaC.
    'px' es una lista de puntos ordenada por su coordenada 'x'.
    Devuelve la distancia mínima.

    Args:
        px (list): Lista de puntos ordenada por 'x'.
    """
    # -> Caso Base <-
    # Si hay muy pocos puntos (<= 3), usamos fuerza bruta.
    if len(px) <= 3:
        return _fuerza_bruta(px)
    
    # -> Divide <-
    medio = len(px) // 2
    punto_medio = px[medio]
    
    # Divide los puntos en dos mitades por la línea 'x' media.
    px_izquierda = px[:medio]
    px_derecha = px[medio:] 
    
    # -> Vence (Recursión) <-
    # Encuentra la distancia mínima en la mitad izquierda y derecha.
    dist_izq = _closest_pair_recursive(px_izquierda)
    dist_der = _closest_pair_recursive(px_derecha)
    
    dist_min = min(dist_izq, dist_der)
    
    # -> Combina <-
    # El paso más difícil: encontrar el par más cercano que "cruza" la línea media.
    
    # a) Crear una "franja" (strip) de puntos que están a una
    #    distancia 'dist_min' de la línea media.
    franja = []
    # Recorremos todos los puntos para ver cuáles están en la franja.
    for punto in px:
        # Si la distancia en 'x' al punto medio es menor que dist_min,
        # entonces el punto está en la franja.
        if abs(punto.x - punto_medio.x) < dist_min:
            franja.append(punto)
            
    # b) Ordenar la franja por la coordenada 'y'.
    franja.sort(key=lambda p: p.y) 
    
    # c) Buscar un par más cercano dentro de la franja.
    dist_min_franja = dist_min

    for i in range(len(franja)):
        # Comparamos cada punto 'i' solo con sus vecinos de abajo.
        # Se puede demostrar que solo necesitamos revisar un número
        # constante de vecinos (aprox. 7) porque la franja está 
        # ordenada por 'y'. Si un punto está más lejos, su distancia 'y'
        # por sí sola ya sería mayor que dist_min.

        # Recorremos los siguientes puntos en la franja.
        for j in range(i + 1, min(i + 8, len(franja))):
            # Calculamos la distancia entre los puntos i y j.
            dist = distancia_euclidiana(franja[i], franja[j])
            if dist < dist_min_franja:
                dist_min_franja = dist # Actualizamos la distancia mínima en la franja.
                
    # El resultado final es el mínimo entre las mitades y la franja
    return min(dist_min, dist_min_franja)

def _fuerza_bruta(puntos):
    """Función auxiliar: caso base, compara todos contra todos.
    Args:
        puntos (list): Lista de puntos en 2D.
    """

    # Comparamos todos contra todos.
    dist_min = float('inf')

    # Recorremos todos los pares de puntos.
    for i in range(len(puntos)):
        # Comparamos el punto i con todos los puntos j > i.
        for j in range(i + 1, len(puntos)):
            
            dist = distancia_euclidiana(puntos[i], puntos[j])
            if dist < dist_min:
                dist_min = dist # Actualizamos la distancia mínima.

    return dist_min # Devolvemos la distancia mínima encontrada.

# ----> Preparacion de datos de prueba <----

# Definir los tamaños de los arreglos.
tamaños = [ 10**2, 10**3, 10**5]

# Generar los arreglos con números aleatorios.
arreglos = {} 
for n in tamaños: 
    # Crea una lista de 'n' números enteros aleatorios entre 1 y 1,000,000.
    arreglos[n] = [random.randint(1, 1000000) for _ in range(n)]

# Acceso a los arreglos generados.
arreglo_100 = arreglos[100]
arreglo_1000 = arreglos[1000]
arreglo_100000 = arreglos[100000]

# Generar puntos aleatorios para el problema de par más cercano.

#  Define los tamaños que te pide la práctica
tamaños_para_puntos = [10, 10**2, 10**3, 10**5]

def generar_puntos_de_prueba(tamaños):
    """
    Genera un diccionario de listas de puntos 2D aleatorios 
    para cada tamaño especificado.

    Args:
        tamaños (list): Una lista de enteros

    Returns:
        dict: Un diccionario donde la clave es el tamaño (n) y
              el valor es la lista de n puntos (tuplas).
    """
    
    # Define el rango para las coordenadas de 0 a 1,000,000).
    # Un rango grande evita que muchos puntos caigan en el mismo lugar.
    MIN_COORD = 0
    MAX_COORD = 1_000_000 
    
    # Diccionario para almacenar los puntos generados.
    puntos_generados = {}
    
    print("Generando puntos de prueba...")
    # Recorremos cada tamaño solicitado.
    for n in tamaños:
        # Usamos una "list comprehension" para generar n puntos (tuplas)
        # cada punto es una tupla (x, y) con valores aleatorios.
        puntos = [(random.randint(MIN_COORD, MAX_COORD), 
                   random.randint(MIN_COORD, MAX_COORD)) 
                  for _ in range(n)]
        
        puntos_generados[n] = puntos
        print(f"  -> Se generó un conjunto de {n} puntos.")
        
    print("¡Generación de datos completada!")
    return puntos_generados

# Llama a la función para crear tus datos
puntos_de_prueba = generar_puntos_de_prueba(tamaños_para_puntos)

# ---> Rendimiento y medición de memoria <----

def medir_rendimiento(funcion, *args, **kwargs):
    """
    Mide el tiempo de ejecución y el uso pico de memoria de una función.
    
    Devuelve un diccionario con el resultado de la función, el tiempo y la memoria.
    Args:
        funcion: La función a medir.
        *args: Argumentos posicionales para la función.
        **kwargs: Argumentos nombrados para la función.
    """
    tracemalloc.start() 
    
    tiempo_inicio = time.perf_counter() 
    
    # Ejecuta la función con sus argumentos.
    resultado_funcion = funcion(*args, **kwargs) 
    
    tiempo_fin = time.perf_counter() 
    
    # 1. Obtenemos la memoria PICO ANTES de detener el rastreo.
    memoria_pico_bytes = tracemalloc.get_traced_memory()[1]
    
    tracemalloc.stop()
    
    # 2. Calculamos los resultados finales.
    tiempo_ejecucion_segundos = tiempo_fin - tiempo_inicio
    memoria_pico_kb = memoria_pico_bytes / 1024
    
    # 3. Devolvemos un diccionario para mayor claridad.
    return {
        "resultado": resultado_funcion,
        "tiempo_s": tiempo_ejecucion_segundos,
        "memoria_pico_kb": memoria_pico_kb
    }

# ----> Ejecucion de pruebas <----

if __name__ == "__main__":
    
    # Lista para guardar todos los reportes de rendimiento
    resultados_completos = []

    print("\n--- INICIANDO PRUEBAS DE RENDIMIENTO (DaC) ---")
    print("Esto puede tardar varios segundos, especialmente con 100,000 elementos...")

    # --->  Pruebas de Quick Select <---
    print("\nProbando Quick Select (k-ésimo menor)...")
    # 'tamaños' ya está definido en tu script como [100, 1000, 100000]
    for n in tamaños: 
        print(f"  -> Tamaño: {n} elementos")
        arr = arreglos[n]
        # Buscamos la mediana (k = n // 2) como un buen caso de prueba
        k = n // 2
        reporte = medir_rendimiento(encontrar_k_esimo_menor, arr, k)
        
        resultados_completos.append({
            "Algoritmo": "Quick Select",
            "Tamaño (n)": n,
            "Tiempo (μs)": reporte['tiempo_s'] * 1e6, # Convertir a microsegundos
            "Memoria (KB)": reporte['memoria_pico_kb'],
            "Resultado": f"k={k}, valor={reporte['resultado']}"
        })

    # ---> Pruebas de Contar Inversiones <---
    print("\nProbando Contar Inversiones...")
    for n in tamaños:
        print(f"  -> Tamaño: {n} elementos")
        arr = arreglos[n]
        reporte = medir_rendimiento(contar_inversiones, arr)
        
        resultados_completos.append({
            "Algoritmo": "Contar Inversiones",
            "Tamaño (n)": n,
            "Tiempo (μs)": reporte['tiempo_s'] * 1e6, # Convertir a microsegundos
            "Memoria (KB)": reporte['memoria_pico_kb'],
            "Resultado": f"{reporte['resultado']} inv."
        })

    # ---> Pruebas de Par de Puntos Más Cercanos <---
    print("\nProbando Par de Puntos Más Cercanos...")
    # 'tamaños_para_puntos' ya está definido como [10, 100, 1000, 100000]
    for n in tamaños_para_puntos:
        print(f"  -> Tamaño: {n} puntos")
        puntos = puntos_de_prueba[n]
        reporte = medir_rendimiento(encontrar_par_mas_cercano, puntos)
        
        resultados_completos.append({
            "Algoritmo": "Par Puntos Cercanos",
            "Tamaño (n)": n,
            "Tiempo (μs)": reporte['tiempo_s'] * 1e6, # Convertir a microsegundos
            "Memoria (KB)": reporte['memoria_pico_kb'],
            "Resultado": f"dist={reporte['resultado']:.4f}" # Formatear la distancia
        })

    print("\n--- PRUEBAS COMPLETADAS ---")

    # ---> Mostrar Resultados en una Tabla <---
    
    # Convertir la lista de resultados en un DataFrame de Pandas
    df_resultados = pd.DataFrame(resultados_completos)
    
    # Ajustar el formato de los números para mejor legibilidad en la tabla
    pd.options.display.float_format = '{:,.2f}'.format
    
    print("\n--- TABLA DE RENDIMIENTO ---")
    print(df_resultados.to_string())