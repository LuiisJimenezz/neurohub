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


# ─────────────────────────────────────────────────────────────────
# PILA (LIFO) — Historial de alertas
# ─────────────────────────────────────────────────────────────────
class AlertStack:
    """
    Pila LIFO para el historial de alertas.
    La última alerta generada es la primera en consultarse.
    """

    def __init__(self):
        self._stack: list[dict] = []

    def push(self, alert: dict):
        """Agrega alerta al tope. O(1)."""
        self._stack.append(alert)

    def pop(self) -> dict | None:
        """Extrae la alerta más reciente. O(1)."""
        return self._stack.pop() if self._stack else None

    def peek(self) -> dict | None:
        """Consulta la alerta más reciente sin extraerla. O(1)."""
        return self._stack[-1] if self._stack else None

    def __len__(self): return len(self._stack)


# ─────────────────────────────────────────────────────────────────
# COLA (FIFO) — Cola de mensajes MQTT pendientes
# ─────────────────────────────────────────────────────────────────
class MessageQueue:
    """
    Cola FIFO para mensajes MQTT por procesar.
    El primer mensaje recibido es el primero en procesarse.
    """

    def __init__(self):
        self._queue: deque[dict] = deque()

    def enqueue(self, msg: dict):
        """Agrega al final. O(1)."""
        self._queue.append(msg)

    def dequeue(self) -> dict | None:
        """Extrae del inicio. O(1) con deque."""
        return self._queue.popleft() if self._queue else None

    def is_empty(self) -> bool:
        return len(self._queue) == 0

    def __len__(self): return len(self._queue)


# ─────────────────────────────────────────────────────────────────
# DEMO
# ─────────────────────────────────────────────────────────────────
if __name__ == "__main__":
    import random

    print("── SensorBuffer (list) ──────────────────")
    buf = SensorBuffer(max_size=5)
    for t in [22.1, 22.4, 23.0, 24.5, 25.1, 26.3]:
        buf.push(t)
    print(f"  Buffer (máx 5): {buf._data}")
    print(f"  Promedio:       {buf.promedio():.2f}°C")

    print("\n── EfficientSensorBuffer (deque) ────────")
    ebuf = EfficientSensorBuffer(max_size=5)
    for t in [22.1, 22.4, 23.0, 24.5, 25.1, 26.3]:
        ebuf.push(t)
    print(f"  Buffer (máx 5): {list(ebuf._data)}")

    print("\n── AlertStack (LIFO) ────────────────────")
    stack = AlertStack()
    stack.push({"tipo": "anomaly",   "msg": "temp > 35°C"})
    stack.push({"tipo": "threshold", "msg": "hum > 90%"})
    stack.push({"tipo": "critical",  "msg": "temp + hum críticos"})
    print(f"  Alertas en pila: {len(stack)}")
    print(f"  Última alerta:   {stack.peek()}")
    print(f"  Procesando...    {stack.pop()}")
    print(f"  Quedan:          {len(stack)}")

    print("\n── MessageQueue (FIFO) ──────────────────")
    q = MessageQueue()
    for i in range(3):
        q.enqueue({"device": "node_01", "seq": i, "temp": round(random.uniform(20,30), 1)})
    print(f"  Mensajes en cola: {len(q)}")
    while not q.is_empty():
        print(f"  Procesando: {q.dequeue()}")
