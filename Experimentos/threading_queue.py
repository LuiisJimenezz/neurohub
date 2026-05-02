import threading
import queue
import time
import random
from datetime import datetime

# ─────────────────────────────────────────────────────────────────
# Cola thread-safe para comunicar hilos
# ─────────────────────────────────────────────────────────────────
sensor_queue: queue.Queue[dict] = queue.Queue(maxsize=100)
stop_event = threading.Event()

# ─────────────────────────────────────────────────────────────────
# Hilo productor — simula recepción de datos MQTT
# ─────────────────────────────────────────────────────────────────
def mqtt_listener(device_id: str, intervalo: float = 1.0):
    """Simula un listener MQTT que recibe datos de sensores."""
    print(f"  🔵 [{device_id}] Hilo MQTT iniciado (TID={threading.current_thread().ident})")
    while not stop_event.is_set():
        mensaje = {
            "device":      device_id,
            "temperature": round(random.uniform(18.0, 35.0), 2),
            "humidity":    round(random.uniform(40.0, 90.0), 1),
            "motion":      random.choice([True, False]),
            "timestamp":   datetime.now().isoformat(),
        }
        try:
            sensor_queue.put(mensaje, timeout=1.0)   # thread-safe
        except queue.Full:
            print(f"  ⚠️  [{device_id}] Cola llena — descartando mensaje")
        time.sleep(intervalo)
    print(f"  🔵 [{device_id}] Hilo MQTT terminado")

# ─────────────────────────────────────────────────────────────────
# Hilo consumidor — procesa y guarda los datos
# ─────────────────────────────────────────────────────────────────
def data_processor():
    """Procesa mensajes de la cola y simula guardar en base de datos."""
    print(f"   Procesador iniciado (TID={threading.current_thread().ident})")
    procesados = 0
    while not (stop_event.is_set() and sensor_queue.empty()):
        try:
            msg = sensor_queue.get(timeout=1.0)
            procesados += 1
            # Simular procesamiento (en producción: save_reading + AI)
            alerta = " ⚠️ ALERTA" if msg["temperature"] > 30 else ""
            print(f"  📊 [{msg['device']}] {msg['temperature']}°C | "
                  f"{msg['humidity']}% | {'🚶' if msg['motion'] else '—'}{alerta}")
            sensor_queue.task_done()
        except queue.Empty:
            continue
    print(f"   Procesador terminado. Total procesados: {procesados}")

# ─────────────────────────────────────────────────────────────────
# DEMO
# ─────────────────────────────────────────────────────────────────
if __name__ == "__main__":
    print("\n── Demo multihilo NeuroHub ──────────────────")
    print(f"   Hilos activos al inicio: {threading.active_count()}")

    # Crear hilos
    hilos = [
        threading.Thread(target=mqtt_listener, args=("node_01", 0.5), daemon=True),
        threading.Thread(target=mqtt_listener, args=("node_02", 0.8), daemon=True),
        threading.Thread(target=data_processor,                       daemon=True),
    ]

    for h in hilos: h.start()
    print(f"   Hilos activos en ejecución: {threading.active_count()}\n")

    time.sleep(5)   # Dejar correr 5 segundos
    stop_event.set()

    for h in hilos: h.join(timeout=3.0)
    print(f"\n   Hilos activos al final: {threading.active_count()}")
    print("── Demo completado ──────────────────────────\n")