from collections import deque

# ─────────────────────────────────────────────────────────────────
# LISTA — Buffer de lecturas de temperatura
# ─────────────────────────────────────────────────────────────────
class SensorBuffer:
    """Buffer de lecturas usando list. Simula el temp_buffer del backend."""

    def __init__(self, max_size: int = 200):
        self._data: list[float] = []
        self.max_size = max_size

    def push(self, value: float):
        """Agrega una lectura. Si supera max_size, elimina la más antigua."""
        if len(self._data) >= self.max_size:
            self._data.pop(0)          # ⚠️  O(n) — costoso
        self._data.append(value)       # O(1) amortizado

    def last_n(self, n: int) -> list[float]:
        """Regresa las últimas n lecturas."""
        return self._data[-n:]         # O(k)

    def promedio(self) -> float:
        return sum(self._data) / len(self._data) if self._data else 0.0

    def __len__(self): return len(self._data)
    def __repr__(self): return f"SensorBuffer({self._data[-5:]}...)"