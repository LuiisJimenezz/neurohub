import bisect
import time

# ─────────────────────────────────────────────────────────────────
# BÚSQUEDA LINEAL — O(n)
# ─────────────────────────────────────────────────────────────────
def busqueda_lineal(lecturas: list[float], umbral: float) -> int:
    """Encuentra el índice de la primera lectura >= umbral. O(n)."""
    for i, valor in enumerate(lecturas):
        if valor >= umbral:
            return i
    return -1

# ─────────────────────────────────────────────────────────────────
# BÚSQUEDA BINARIA — O(log n) — requiere lista ordenada
# ─────────────────────────────────────────────────────────────────
def busqueda_binaria(lecturas_ordenadas: list[float], umbral: float) -> int:
    """Encuentra posición de inserción de umbral. O(log n)."""
    return bisect.bisect_left(lecturas_ordenadas, umbral)

# ─────────────────────────────────────────────────────────────────
# ORDENAMIENTO — Timsort nativo O(n log n)
# ─────────────────────────────────────────────────────────────────
def top_temperaturas(lecturas: list[float], n: int = 5) -> list[float]:
    """Regresa las n temperaturas más altas."""
    return sorted(lecturas, reverse=True)[:n]

def ordenar_dispositivos(dispositivos: list[dict]) -> list[dict]:
    """Ordena dispositivos por temperatura descendente."""
    return sorted(dispositivos, key=lambda d: d["temp"], reverse=True)

# ─────────────────────────────────────────────────────────────────
# DEMO
# ─────────────────────────────────────────────────────────────────
if __name__ == "__main__":
    import random
    N = 10_000
    lecturas = [round(random.uniform(15.0, 40.0), 2) for _ in range(N)]
    lecturas_ord = sorted(lecturas)
    umbral = 35.0

    # Benchmarking
    t0 = time.perf_counter()
    idx_lineal = busqueda_lineal(lecturas_ord, umbral)
    t_lineal = (time.perf_counter() - t0) * 1_000_000

    t0 = time.perf_counter()
    idx_binario = busqueda_binaria(lecturas_ord, umbral)
    t_binario = (time.perf_counter() - t0) * 1_000_000

    print(f"Búsqueda lineal:  índice {idx_lineal:>6}  |  {t_lineal:.2f} µs")
    print(f"Búsqueda binaria: índice {idx_binario:>6}  |  {t_binario:.2f} µs")
    print(f"Speedup: {t_lineal / t_binario:.1f}x más rápida la binaria (n={N:,})")

    print("\nTop 5 temperaturas más altas:")
    for i, t in enumerate(top_temperaturas(lecturas), 1):
        print(f"  {i}. {t}°C")