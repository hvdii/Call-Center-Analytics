"""
Módulo principal - Punto de entrada del sistema de análisis de interacciones en contact centers.

Este módulo coordina el flujo completo del proceso:
1. Conversión de audio a texto
2. Tokenización del texto
3. Análisis de sentimiento
4. Verificación de protocolos
"""

import os
from modulos import speech_to_text, tokenizador, sentimiento, protocolos

def analizar_audio(ruta_audio):
    """
    Procesa un archivo de audio completo a través de todas las etapas del sistema.
    
    Args:
        ruta_audio (str): Ruta al archivo de audio a analizar
    """
    # Configuración de rutas
    base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    modelo_vosk = os.path.join(base_dir, "modelos", "vosk-model-small-es")
    diccionario_sentimiento = os.path.join(base_dir, "data", "diccionarios", "palabras_positivas-negativas.txt")
    diccionarios_protocolos = os.path.join(base_dir, "data", "diccionarios", "protocolos")
    
    # 1. Conversión de audio a texto
    nombre_audio = os.path.splitext(os.path.basename(ruta_audio))[0]
    ruta_transcript = os.path.join(base_dir, "outputs", "transcripts", f"{nombre_audio}.txt")
    texto = speech_to_text.transcribir_audio(ruta_audio, modelo_vosk, ruta_transcript)

    # 2. Tokenización
    ruta_tokens = os.path.join(base_dir, "outputs", "tokens", f"{nombre_audio}_tokens.txt")
    tokens = tokenizador.tokenizar_archivo(ruta_transcript, ruta_tokens)
    
    
    # 3. Análisis de sentimiento
    ruta_reporte_sentimiento = os.path.join(base_dir, "outputs", "reports", f"{nombre_audio}_sentimiento.txt")
    sentimiento.analizar_sentimiento(
    ruta_tokens, 
    diccionario_sentimiento, 
    ruta_reporte_sentimiento
    )

    # 4. Verificación de protocolos
    ruta_reporte_protocolos = os.path.join(base_dir, "outputs", "reports", f"{nombre_audio}_protocolos.txt")
    protocolos.verificar_protocolos(
        ruta_transcript,
        diccionarios_protocolos,
        ruta_reporte_protocolos
    )


if __name__ == "__main__":
    # Ejemplo de uso
    ruta_audio_ejemplo = os.path.join("data", "audios", "script1.wav")
    analizar_audio(ruta_audio_ejemplo)