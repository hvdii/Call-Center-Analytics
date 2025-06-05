"""
Módulo de conversión de voz a texto.

Utiliza el modelo Vosk para transcribir audio a texto, con preprocesamiento
para asegurar compatibilidad con el formato requerido (16-bit PCM mono a 16kHz).

Características:
- Conversión automática de formatos usando pydub/FFmpeg
- Manejo de errores robusto
- Soporte para modelos Vosk en español
"""

import os
import wave
import json
import shutil
from vosk import Model, KaldiRecognizer
from pydub import AudioSegment

def convert_to_vosk_format(input_path, output_path):
    """
    Convierte cualquier archivo de audio al formato compatible con Vosk (16-bit PCM mono).
    
    Args:
        input_path (str): Ruta al archivo de entrada
        output_path (str): Ruta para el archivo convertido
        
    Returns:
        str: Ruta al archivo convertido
        
    Raises:
        RuntimeError: Si falla la conversión
    """
    try:
        audio = AudioSegment.from_file(input_path)
        audio = audio.set_channels(1).set_frame_rate(16000).set_sample_width(2)
        audio.export(output_path, format="wav")
        return output_path
    except Exception as e:
        raise RuntimeError(f"Error converting audio: {str(e)}")

def transcribir_audio(ruta_audio, ruta_modelo, ruta_salida):
    """
    Transcribe un archivo de audio a texto usando el modelo Vosk.
    
    Args:
        ruta_audio (str): Ruta al archivo de audio a transcribir
        ruta_modelo (str): Ruta al directorio del modelo Vosk
        ruta_salida (str): Ruta donde guardar la transcripción
        
    Returns:
        str: Texto transcrito
        
    Raises:
        RuntimeError: Si FFmpeg no está instalado
        FileNotFoundError: Si el modelo Vosk no existe
        ValueError: Si el audio no está en el formato correcto
    """
    temp_audio = None
    
    try:
        # Verificar disponibilidad de FFmpeg
        if not shutil.which("ffmpeg"):
            raise RuntimeError("FFmpeg no encontrado. Instalar con: brew install ffmpeg")

        # Convertir audio si es necesario
        temp_audio = "temp_converted.wav"
        converted_audio = convert_to_vosk_format(ruta_audio, temp_audio)
        
        # Cargar modelo Vosk
        if not os.path.exists(ruta_modelo):
            raise FileNotFoundError(f"Modelo Vosk no encontrado en {ruta_modelo}")

        model = Model(ruta_modelo)
        
        # Procesar audio
        with wave.open(converted_audio, "rb") as wf:
            if wf.getnchannels() != 1 or wf.getsampwidth() != 2:
                raise ValueError("El audio debe ser PCM mono de 16-bit")
            
            rec = KaldiRecognizer(model, wf.getframerate())
            rec.SetWords(True)
            
            results = []
            while True:
                data = wf.readframes(4000)
                if len(data) == 0:
                    break
                if rec.AcceptWaveform(data):
                    results.append(json.loads(rec.Result()))
            
            results.append(json.loads(rec.FinalResult()))
        
        # Combinar resultados
        full_text = " ".join([r.get("text", "") for r in results])
        
        # Crear directorio de salida si no existe
        os.makedirs(os.path.dirname(ruta_salida), exist_ok=True)
        
        # Guardar transcripción
        with open(ruta_salida, "w", encoding="utf-8") as f:
            f.write(full_text)
            
        return full_text
        
    finally:
        # Limpiar archivo temporal
        if temp_audio and os.path.exists(temp_audio):
            os.remove(temp_audio)