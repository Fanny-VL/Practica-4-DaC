// ---------------------------------------------------------------
// Divide y Vencerás (DaC):
// 1) Quickselect (k-ésimo menor en un arreglo)
// 2) Conteo de inversiones (modificación de mergesort)
// 3) Par de puntos más cercanos en 2D
//
// Este programa ejecuta los 3 algoritmos en varios tamaños y
// muestra tiempos y resultados en tablas.
//
// Compilar:  gcc -O2 -std=c11 dac_all_comentado.c -o dac_all
// Ejecutar:  ./dac_all
// ---------------------------------------------------------------
#include <stdio.h>
#include <stdlib.h>
#include <time.h>
#include <math.h>

/* ======================= Utilidades pequeñas ======================= */
// Intercambia dos enteros (lo usamos en quickselect)
static inline void swap_int(int *a, int *b){ int t=*a; *a=*b; *b=t; }

// Comparador para qsort con enteros (solo para verificar resultados)
static int cmp_int(const void* a, const void* b){ return (*(const int*)a - *(const int*)b); }

// Mínimo entre dos doubles (evita escribir ifs repetidos)
static inline double min_d(double a, double b){ return a < b ? a : b; }

/* ======================= 1) Quickselect (DaC) ======================= */
/*
  Idea: elegir un pivote, particionar el arreglo en <= pivote y > pivote
  y decidir en qué lado está el k-ésimo. Complejidad promedio O(n).
*/

// Particiona [l..r] usando Lomuto; deja el pivote en su posición final
static int partition(int arr[], int l, int r){
    int x = arr[r], i = l;
    for(int j=l;j<r;++j){
        if(arr[j] <= x){ swap_int(&arr[i], &arr[j]); i++; }
    }
    swap_int(&arr[i], &arr[r]);
    return i; // índice donde quedó el pivote
}

// Elige pivote aleatorio para evitar peores casos frecuentes
static int random_partition(int arr[], int l, int r){
    int p = l + rand() % (r - l + 1);
    swap_int(&arr[p], &arr[r]);
    return partition(arr,l,r);
}

// Devuelve el k-ésimo menor (k es 1..n) en el subarreglo [l..r]
int quickselect_kth(int arr[], int l, int r, int k){
    if(l==r) return arr[l];              // caso base: 1 elemento
    int pos = random_partition(arr,l,r); // posición final del pivote
    int rank = pos - l + 1;              // cuántos hay <= pivote
    if(rank == k) return arr[pos];       // justo el k-ésimo
    else if(k < rank)                    // está a la izquierda
        return quickselect_kth(arr,l,pos-1,k);
    else                                 // está a la derecha (ajustar k)
        return quickselect_kth(arr,pos+1,r,k-rank);
}

/* =================== 2) Conteo de inversiones (DaC) ================== */
/*
  Inversión: par (i,j) con i<j y a[i] > a[j].
  Truco: durante el merge de mergesort, cuando tomamos algo del derecho,
  significa que lo que queda en la izquierda forma inversiones.
  Complejidad O(n log n).
*/

// Une dos mitades ya ordenadas y cuenta inversiones nuevas
long long merge_and_count(int a[], int tmp[], int l, int m, int r){
    int i=l, j=m+1, k=l;
    long long inv=0;

    // Mezcla ordenada y suma inversiones cuando toma del derecho
    while(i<=m && j<=r){
        if(a[i]<=a[j]) tmp[k++]=a[i++];
        else{
            tmp[k++]=a[j++];
            inv += (long long)(m - i + 1); // todo lo que queda a[i..m] > a[j tomado]
        }
    }
    // Copiar sobrantes
    while(i<=m) tmp[k++]=a[i++];
    while(j<=r) tmp[k++]=a[j++];

    // Copiar de vuelta al arreglo original
    for(i=l;i<=r;++i) a[i]=tmp[i];
    return inv;
}

// Mergesort recursivo que, además, regresa el total de inversiones
long long sort_count(int a[], int tmp[], int l, int r){
    if(l>=r) return 0;                     // 0 o 1 elemento → 0 inversiones
    int m = l + (r-l)/2;
    long long inv=0;
    inv += sort_count(a,tmp,l,m);          // inversiones en la izquierda
    inv += sort_count(a,tmp,m+1,r);        // inversiones en la derecha
    inv += merge_and_count(a,tmp,l,m,r);   // inversiones “cruzadas”
    return inv;
}

// Función cómoda: reserva temporal y llama al recursivo
long long count_inversions(int a[], int n){
    int *tmp = (int*)malloc(n*sizeof(int));
    if(!tmp){ fprintf(stderr,"mem error\n"); exit(1); }
    long long ans = sort_count(a,tmp,0,n-1);
    free(tmp);
    return ans;
}

/* ============ 3) Par de puntos más cercanos en 2D (DaC) ============== */
/*
  Algoritmo clásico O(n log n):
  - Ordenar por X.
  - Dividir en izquierda/derecha y obtener mínima distancia d.
  - Considerar una franja alrededor de la línea media y checar
    pocos vecinos ordenados por Y.
*/
typedef struct { double x,y; } Pt;

// Comparadores para ordenar puntos
static int cmp_x(const void* A, const void* B){
    double d = ((const Pt*)A)->x - ((const Pt*)B)->x;
    return (d<0)?-1:(d>0);
}
static int cmp_y(const void* A, const void* B){
    double d = ((const Pt*)A)->y - ((const Pt*)B)->y;
    return (d<0)?-1:(d>0);
}

// Distancia al cuadrado (evita sqrt hasta el final)
static inline double dist2(Pt a, Pt b){
    double dx=a.x-b.x, dy=a.y-b.y;
    return dx*dx + dy*dy;
}

/*
  closest_rec:
  - px: puntos (trabajados) que terminamos dejando ordenados por Y al volver
  - py/tmp: buffers auxiliares
  - n: cantidad de puntos en este subproblema
  Devuelve la distancia mínima AL CUADRADO en este subproblema.
*/
double closest_rec(Pt px[], Pt py[], Pt tmp[], int n){
    // Casos muy pequeños: fuerza bruta y reordenar por Y
    if(n <= 3){
        double best = INFINITY;
        for(int i=0;i<n;i++) for(int j=i+1;j<n;j++)
            best = min_d(best, dist2(px[i],px[j]));
        qsort(px, n, sizeof(Pt), cmp_y); // dejar ordenado por Y
        for(int i=0;i<n;i++) py[i]=px[i];
        return best;
    }

    int mid = n/2;
    double midx = px[mid].x; // línea vertical que divide

    // Resolver izquierda y derecha
    double dl = closest_rec(px,     py,     tmp, mid);
    double dr = closest_rec(px+mid, py+mid, tmp, n-mid);
    double d = min_d(dl, dr); // mejor de ambos lados

    // Mezcla por Y: generamos 'py' ordenado por Y con todos los puntos
    int i=0, j=mid, k=0;
    while(i<mid && j<n) py[k++] = (px[i].y < px[j].y) ? px[i++] : px[j++];
    while(i<mid) py[k++] = px[i++];
    while(j<n)   py[k++] = px[j++];

    // Construir franja de ancho 2*sqrt(d) centrada en x=midx
    int sz=0;
    for(int t=0;t<n;t++){
        double dx = py[t].x - midx;
        if(dx*dx < d) tmp[sz++] = py[t];
    }

    // En la franja, basta comparar con unos pocos vecinos por Y
    for(i=0;i<sz;i++){
        for(j=i+1;j<sz; j++){
            double dy = tmp[j].y - tmp[i].y;
            if(dy*dy >= d) break;               // muy lejos en Y → cortar
            double cand = dist2(tmp[i], tmp[j]);
            if(cand < d) d = cand;              // mejor distancia encontrada
        }
    }

    // Dejar 'px' ordenado por Y para el nivel superior
    for(i=0;i<n;i++) px[i]=py[i];
    return d;
}

// Envoltura: ordena por X al inicio y devuelve distancia (ya con sqrt)
double closest_pair(Pt pts[], int n){
    Pt *px = (Pt*)malloc(n*sizeof(Pt));
    Pt *py = (Pt*)malloc(n*sizeof(Pt));
    Pt *tmp= (Pt*)malloc(n*sizeof(Pt));
    for(int i=0;i<n;i++) px[i]=pts[i];
    qsort(px, n, sizeof(Pt), cmp_x);       // ordenar por X una sola vez
    double d2 = closest_rec(px, py, tmp, n);
    free(px); free(py); free(tmp);
    return sqrt(d2);                       // sacar raíz al final
}

/* ======================= Relleno de datos ======================= */
// Llena un arreglo de enteros con aleatorios en [0, maxv)
void fill_random_ints(int *a, int n, int maxv){
    for(int i=0;i<n;i++) a[i] = rand() % maxv;
}
// Genera puntos aleatorios (coordenadas en [0, maxv))
void fill_random_points(Pt *p, int n, int maxv){
    for(int i=0;i<n;i++){
        p[i].x = (double)(rand() % maxv);
        p[i].y = (double)(rand() % maxv);
    }
}

/* ======================= Programa principal ======================= */
/*
  - Define los tamaños de prueba.
  - Para cada tamaño de ARREGLOS: ejecuta quickselect e inversiones
    y mide los tiempos con clock().
  - Para cada tamaño de PUNTOS: ejecuta par más cercano.
  - Imprime tablas con resultados y una verificación sencilla.
*/
int main(void){
    // Semilla fija para que los números se repitan entre corridas (útil para comparar)
    // Cambia a time(NULL) si quieres datos distintos cada ejecución.
    srand(12345u);

    // Tamaños de prueba pedidos por la consigna
    int sizes_arr[] = {100, 1000, 10000, 100000}; // arreglos (enteros)
    int sizes_pts[] = {10, 100, 1000, 100000};    // puntos 2D

    int SA = sizeof(sizes_arr)/sizeof(sizes_arr[0]);
    int SP = sizeof(sizes_pts)/sizeof(sizes_pts[0]);

    printf("=============================================================\n");
    printf(" DIVIDE & VENCERÁS: Quickselect, Inversiones, Par más cercano\n");
    printf("=============================================================\n\n");

    /* --------- Tabla: Quickselect e Inversiones (arreglos) --------- */
    printf("Resultados para ARREGLOS (tamaños: 100, 1000, 10000, 100000)\n");
    printf("--------------------------------------------------------------------------\n");
    printf("%10s | %10s | %18s | %18s\n","N","k","t(Quickselect) [s]","t(Inversiones) [s]");
    printf("--------------------------------------------------------------------------\n");

    for(int idx=0; idx<SA; ++idx){
        int n = sizes_arr[idx];

        // Reservas de memoria para el arreglo original y una copia auxiliar
        int *arr = (int*)malloc(n*sizeof(int));
        int *copy = (int*)malloc(n*sizeof(int));
        if(!arr || !copy){ fprintf(stderr,"mem error\n"); return 1; }

        // Generamos datos aleatorios
        fill_random_ints(arr, n, 1000000);

        // Elegimos un k representativo: un cuarto del arreglo
        int k = (n+3)/4;

        // ---------- Quickselect ----------
        // Trabajamos con una copia para no modificar 'arr' original
        for(int i=0;i<n;i++) copy[i]=arr[i];
        clock_t a0 = clock();
        int kth = quickselect_kth(copy, 0, n-1, k);
        clock_t a1 = clock();

        // ---------- Conteo de inversiones ----------
        // Volvemos a copiar desde el original para empezar “limpio”
        for(int i=0;i<n;i++) copy[i]=arr[i];
        clock_t b0 = clock();
        long long invs = count_inversions(copy, n);
        clock_t b1 = clock();

        // Impresión de tiempos y pequeña verificación con qsort
        printf("%10d | %10d | %18.6f | %18.6f   ",
               n, k,
               (double)(a1-a0)/CLOCKS_PER_SEC,
               (double)(b1-b0)/CLOCKS_PER_SEC);

        // Verificación: ordenar todo y mirar el elemento de la posición k
        qsort(arr, n, sizeof(int), cmp_int);
        printf("<= verif: quickselect=%d, ordenado[k]=%d, invs=%lld\n",
               kth, arr[k-1], invs);

        free(arr); free(copy);
    }
    printf("--------------------------------------------------------------------------\n\n");

    /* ----------------- Tabla: Par de puntos más cercanos ------------------ */
    printf("Resultados para PUNTOS 2D (tamaños: 10, 100, 1000, 100000)\n");
    printf("---------------------------------------------------------------\n");
    printf("%10s | %25s | %18s\n","N","distancia mínima","t(Par más cercano) [s]");
    printf("---------------------------------------------------------------\n");

    for(int idx=0; idx<SP; ++idx){
        int n = sizes_pts[idx];

        // Reservamos arreglo de puntos y lo llenamos
        Pt *pts = (Pt*)malloc(n*sizeof(Pt));
        if(!pts){ fprintf(stderr,"mem error\n"); return 1; }
        fill_random_points(pts, n, 1000000);

        // Ejecutamos el algoritmo DaC y medimos
        clock_t c0 = clock();
        double dmin = closest_pair(pts, n);
        clock_t c1 = clock();

        // Imprimir distancia mínima y tiempo
        printf("%10d | %25.6f | %18.6f\n",
               n, dmin, (double)(c1-c0)/CLOCKS_PER_SEC);

        free(pts);
    }
    printf("---------------------------------------------------------------\n");
    return 0;
}
