import os

def verificar_protocolos(ruta_transcript, ruta_diccionarios, ruta_reporte):
    """
    Verifica si se cumplieron los protocolos de atención en la transcripción.
    
    Args:
        ruta_transcript (str): Ruta al archivo de texto con la transcripción
        ruta_diccionarios (str): Ruta al directorio con los archivos de protocolos
        ruta_reporte (str): Ruta donde guardar el reporte de protocolos
    """
    # Leer la transcripción
    with open(ruta_transcript, 'r', encoding='utf-8') as f:
        texto = f.read().lower()
    
    # Cargar listas de palabras/frases para cada protocolo
    protocolos = {
        'saludo': cargar_palabras(os.path.join(ruta_diccionarios, 'saludos.txt')),
        'identificacion': cargar_palabras(os.path.join(ruta_diccionarios, 'identificacion.txt')),
        'despedida': cargar_palabras(os.path.join(ruta_diccionarios, 'despedidas.txt')),
        'prohibidas': cargar_palabras(os.path.join(ruta_diccionarios, 'prohibidas.txt'))
    }
    
    # Verificar cada protocolo
    resultados = {
        'saludo': verificar_protocolo(texto, protocolos['saludo']),
        'identificacion': verificar_protocolo(texto, protocolos['identificacion']),
        'despedida': verificar_protocolo(texto, protocolos['despedida']),
        'prohibidas': verificar_palabras_prohibidas(texto, protocolos['prohibidas'])
    }
    
    # Generar reporte
    generar_reporte(resultados, ruta_reporte)

def cargar_palabras(ruta_archivo):
    """Carga palabras/frases de un archivo de texto"""
    try:
        with open(ruta_archivo, 'r', encoding='utf-8') as f:
            return [line.strip().lower() for line in f if line.strip()]
    except FileNotFoundError:
        return []

def verificar_protocolo(texto, palabras_clave):
    """Verifica si alguna de las palabras clave aparece en el texto"""
    for palabra in palabras_clave:
        if palabra in texto:
            return {'cumplido': True, 'palabra_encontrada': palabra}
    return {'cumplido': False, 'palabra_encontrada': None}

def verificar_palabras_prohibidas(texto, palabras_prohibidas):
    """Verifica si hay palabras prohibidas en el texto"""
    encontradas = [palabra for palabra in palabras_prohibidas if palabra in texto]
    return {
        'cumplido': len(encontradas) == 0,
        'palabras_encontradas': encontradas if encontradas else None
    }

def generar_reporte(resultados, ruta_reporte):
    """Genera el reporte de verificación de protocolos"""
    with open(ruta_reporte, 'w', encoding='utf-8') as f:
        f.write("=== Reporte de Verificación de Protocolos ===\n\n")
        
        # Saludo
        saludo = resultados['saludo']
        f.write(f"Fase de saludo: {'OK' if saludo['cumplido'] else 'Faltante'}")
        if saludo['cumplido']:
            f.write(f" (Palabra encontrada: '{saludo['palabra_encontrada']}')")
        f.write("\n")
        
        # Identificación
        identificacion = resultados['identificacion']
        f.write(f"Identificación del cliente: {'OK' if identificacion['cumplido'] else 'Faltante'}")
        if identificacion['cumplido']:
            f.write(f" (Palabra encontrada: '{identificacion['palabra_encontrada']}')")
        f.write("\n")
        
        # Palabras prohibidas
        prohibidas = resultados['prohibidas']
        f.write(f"Uso de palabras rudas: {'Ninguna detectada' if prohibidas['cumplido'] else 'Detectadas'}")
        if not prohibidas['cumplido']:
            f.write(f" (Palabras encontradas: {', '.join(prohibidas['palabras_encontradas'])})")
        f.write("\n")
        
        # Despedida
        despedida = resultados['despedida']
        f.write(f"Despedida amable: {'OK' if despedida['cumplido'] else 'Faltante'}")
        if despedida['cumplido']:
            f.write(f" (Palabra encontrada: '{despedida['palabra_encontrada']}')")
        f.write("\n")