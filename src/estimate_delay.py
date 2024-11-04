import sounddevice as sd
import numpy as np
import time

# Configuración
frecuencia_muestreo = 44100  # Frecuencia de muestreo en Hz
frecuencia_pitido = 1000  # Frecuencia del pitido en Hz
duracion_pitido = 1  # Duración del pitido en segundos
tiempo_espera = 0  # Tiempo de espera antes de grabar

# Generar el pitido con mayor amplitud
t = np.linspace(0, duracion_pitido, int(frecuencia_muestreo * duracion_pitido), False)
pitido = 0.9 * np.sin(2 * np.pi * frecuencia_pitido * t)  # 0.9 para asegurar un sonido fuerte

# Función para detectar el tiempo de llegada del pitido
def detectar_inicio_señal(señal, umbral=0.1):
    indices = np.where(np.abs(señal) > umbral)[0]
    if indices.size > 0:
        return indices[0] / frecuencia_muestreo
    return None

# Emitir y capturar sonido
print("Preparado para emitir el pitido...")
time.sleep(tiempo_espera)  # Espera antes de iniciar

# Emitimos el pitido
print("Emitiendo pitido...")
inicio_emision = time.time()
sd.play(pitido, samplerate=frecuencia_muestreo)  # Emitir pitido
sd.wait()  # Esperamos a que termine el pitido
fin_emision = time.time()
print("Pitido emitido.")

# Capturamos el sonido justo después de emitirlo
print("Iniciando grabación...")
grabacion = sd.rec(int((duracion_pitido + 0.5) * frecuencia_muestreo), samplerate=frecuencia_muestreo, channels=1)  # Grabar
sd.wait()  # Esperar a que termine la grabación
print("Grabación completa.")

# Calcular el tiempo de inicio del sonido en la señal grabada
inicio_pitido_emitido = detectar_inicio_señal(pitido)
inicio_pitido_recibido = detectar_inicio_señal(grabacion[:, 0])

# Calcular tiempo de viaje
if inicio_pitido_recibido is not None:
    tiempo_viaje = inicio_pitido_recibido - inicio_pitido_emitido
    print(f"Tiempo de viaje del sonido: {tiempo_viaje:.4f} segundos")
else:
    print("No se detectó el pitido en la grabación. Ajusta el umbral o verifica el micrófono y el altavoz.")
