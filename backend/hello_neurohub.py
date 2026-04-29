"""
NeuroHub - Primer script del proyecto

Sesión 1: Verifica que el entorno de Python esté correctamente configurado.
"""

import sys
import platform
from datetime import datetime


def check_environment() -> dict:
    """Verifica las versiones del entorno de desarrollo."""
    return {
        "python_version": sys.version,
        "platform": platform.system(),
        "architecture": platform.architecture()[0],
        "timestamp": datetime.now().isoformat(),
    }


def print_banner():
    """Imprime el banner de bienvenida del proyecto."""
    banner = """
╔════════════════════════════════════╗
║        NeuroHub v1.0.0             ║
║   Plataforma IoT Inteligente       ║
╚════════════════════════════════════╝
"""
    print(banner)


def main():
    print_banner()

    env = check_environment()

    print("=== Información del entorno ===")
    for key, value in env.items():
        print(f"{key:<20} : {value}")

    print()

    # Verificación de versión mínima
    major, minor = sys.version_info[:2]

    if major == 3 and minor >= 11:
        print("✅ Python >= 3.11 detectado — entorno válido para NeuroHub")
    else:
        print("⚠️ Se recomienda Python 3.11 o superior")


if __name__ == "__main__":
    main()
    