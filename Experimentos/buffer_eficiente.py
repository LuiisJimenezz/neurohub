from collections import deque

# ─────────────────────────────────────────────────────────────────
# DEQUE — Buffer eficiente O(1) en ambos extremos
# ─────────────────────────────────────────────────────────────────
class EfficientSensorBuffer:
    """Buffer con deque. Mejor que list para inserciones al inicio."""

    def __init__(self, max_size: int = 200):
        self._data: deque[float] = deque(maxlen=max_size)

    def push(self, value: float):
        """O(1) — deque descarta el más antiguo automáticamente."""
        self._data.append(value)

    def last_n(self, n: int) -> list[float]:
        return list(self._data)[-n:]

    def promedio(self) -> float:
        return sum(self._data) / len(self._data) if self._data else 0.0

    def __len__(self): return len(self._data)
