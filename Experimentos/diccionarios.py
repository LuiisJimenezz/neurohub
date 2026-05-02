
# ─────────────────────────────────────────────────────────────────
# DICCIONARIO — Registro de dispositivos IoT
# ─────────────────────────────────────────────────────────────────
dispositivos: dict[str, dict] = {
    "node_01": {"nombre": "Sala Servidores", "activo": True,  "temp": 24.5},
    "node_02": {"nombre": "Cuarto Frío",     "activo": True,  "temp": 8.1},
    "node_03": {"nombre": "Oficina",         "activo": False, "temp": 22.0},
}

# Acceso O(1)
print(dispositivos["node_01"])

# Actualizar temperatura
dispositivos["node_01"]["temp"] = 25.8

# dict.get() — evita KeyError
info = dispositivos.get("node_99", {"nombre": "Desconocido"})

# Iteración
for device_id, info in dispositivos.items():
    estado = "🟢" if info["activo"] else "🔴"
    print(f"  {estado} {device_id}: {info['nombre']} — {info['temp']}°C")

# Dictionary comprehension — filtrar activos
activos = {k: v for k, v in dispositivos.items() if v["activo"]}
print(f"\nDispositivos activos: {list(activos.keys())}")

# ─────────────────────────────────────────────────────────────────
# CONJUNTO — Deduplicación de alertas enviadas
# ─────────────────────────────────────────────────────────────────
# Evitar enviar la misma alerta dos veces al dashboard
alertas_enviadas: set[str] = set()

def enviar_alerta(device_id: str, tipo: str) -> bool:
    """Retorna True si la alerta es nueva (no se había enviado)."""
    clave = f"{device_id}:{tipo}"
    if clave in alertas_enviadas:           # O(1)
        return False
    alertas_enviadas.add(clave)            # O(1)
    return True

print(enviar_alerta("node_01", "anomaly"))   # True  — nueva
print(enviar_alerta("node_01", "anomaly"))   # False — duplicada
print(enviar_alerta("node_02", "critical"))  # True  — nueva
print(f"Alertas únicas registradas: {alertas_enviadas}")