"""
NeuroHub - Sesión 2: Demostración empírica de complejidad temporal O(n)

Ejecutar: python backend/benchmarks/complexity_demo.py
"""

import timeit
import math


# ============================================================
# CONFIGURACIÓN
# ============================================================

SIZES = [100, 500, 1_000, 5_000, 10_000, 50_000, 100_000]


def medir(funcion: str, setup: str, repeticiones: int = 100) -> float:
    """Retorna el tiempo promedio en microsegundos."""
    t = timeit.timeit(funcion, setup=setup, number=repeticiones)
    return (t / repeticiones) * 1_000_000  # convertir a µs


# ============================================================
# EXPERIMENTO 1: list.append O(1) amortizado vs list.insert(0) O(n)
# ============================================================

def experimento_insercion():
    print("\n" + "=" * 60)
    print("  EXPERIMENTO 1: append O(1) vs insert(0) O(n)")
    print("=" * 60)
    print(f"{'n':>10} {'append µs':>12} {'insert(0) µs':>14} {'ratio':>8}")
    print(" " + "-" * 54)

    for n in SIZES:
        setup = f"lst = list(range({n}))"
        t_append = medir("lst.append(999)", setup)
        t_insert = medir("lst.insert(0, 999)", setup)
        ratio = t_insert / t_append if t_append > 0 else 0
        print(f"{n:>10,} {t_append:>12.2f} {t_insert:>14.2f} {ratio:>7.1f}x")


# ============================================================
# EXPERIMENTO 2: Búsqueda en list O(n) vs dict O(1)
# ============================================================

def experimento_busqueda():
    print("\n" + "=" * 60)
    print("  EXPERIMENTO 2: búsqueda list O(n) vs dict O(1)")
    print("=" * 60)
    print(f"{'n':>10} {'list µs':>10} {'dict µs':>10} {'speedup':>10}")
    print(" " + "-" * 46)

    for n in SIZES:
        setup_list = f"lst = list(range({n})); target = {n - 1}"
        setup_dict = f"dct = {{i: i for i in range({n})}}; target = {n - 1}"

        t_list = medir("target in lst", setup_list)
        t_dict = medir("target in dct", setup_dict)

        speedup = t_list / t_dict if t_dict > 0 else 0

        print(f"{n:>10,} {t_list:>10.2f} {t_dict:>10.2f} {speedup:>9.0f}x")


# ============================================================
# EXPERIMENTO 3: Timsort O(n log n) - sorting
# ============================================================

def experimento_sort():
    print("\n" + "=" * 60)
    print("  EXPERIMENTO 3: sort O(n log n) - Timsort nativo")
    print("=" * 60)
    print(f"{'n':>10} {'tiempo µs':>12} {'n·log(n)':>12} {'ratio µs/op':>14}")
    print(" " + "-" * 54)

    prev_t = None

    for n in SIZES:
        import random

        setup = f"import random; lst = random.sample(range({n * 10}), {n})"
        t = medir("sorted(lst)", setup, repeticiones=20)

        nlogn = n * math.log2(n)
        ratio = t / nlogn if nlogn > 0 else 0
        growth = f"{t / prev_t:.2f}x" if prev_t else "--"

        print(f"{n:>10,} {t:>12.2f} {nlogn:>12.0f} {ratio:>12.6f}  crecimiento: {growth}")

        prev_t = t


# ============================================================
# GRÁFICA ASCII en terminal
# ============================================================

def grafica_ascii(titulo: str, datos: dict, ancho: int = 40):
    """Genera una gráfica de barras horizontal en ASCII."""
    print(f"\n📊 {titulo}")
    print(" " + "-" * (ancho + 20))

    max_val = max(datos.values()) if datos else 1

    for label, valor in datos.items():
        barra_len = int((valor / max_val) * ancho)
        barra = "█" * barra_len
        print(f"{label:>12} | {barra:<{ancho}} {valor:>8.1f} µs")

    print(" " + "-" * (ancho + 20))


def demo_grafica():
    """Muestra visualmente la diferencia de rendimiento."""
    n = 50_000

    setup_list = f"lst = list(range({n})); target = {n - 1}"
    setup_dict = f"dct = {{i: i for i in range({n})}}; target = {n - 1}"
    setup_set = f"s = set(range({n})); target = {n - 1}"

    datos = {
        f"list[{n // 1000}k]": medir("target in lst", setup_list),
        f"dict[{n // 1000}k]": medir("target in dct", setup_dict),
        f"set[{n // 1000}k]": medir("target in s", setup_set),
    }

    grafica_ascii(f"Búsqueda del elemento (n-1) en n={n:,}", datos)


# ============================================================
# MAIN
# ============================================================

if __name__ == "__main__":
    print("\n" + "╔" + "═" * 58 + "╗")
    print("║       NeuroHub — Benchmarks de Complejidad Temporal       ║")
    print("╚" + "═" * 58 + "╝")

    experimento_insercion()
    experimento_busqueda()
    experimento_sort()
    demo_grafica()

    print("\n✅ Benchmark completado.\n")