"""
Módulo de análisis de sentimiento para evaluar conversaciones en contact centers

Características:
- Carga diccionario de palabras con ponderaciones
- Analiza tokens y calcula puntuación de sentimiento
- Genera reporte detallado
"""

import os
from collections import defaultdict

class AnalizadorSentimiento:
    def __init__(self, ruta_diccionario):
        """
        Inicializa el analizador con el diccionario de palabras
        
        Args:
            ruta_diccionario (str): Ruta al archivo con palabras y ponderaciones
        """
        self.palabras_ponderadas = self._cargar_diccionario(ruta_diccionario)
    
    def _cargar_diccionario(self, ruta):
        """
        Carga el diccionario de palabras con sus ponderaciones
        
        Args:
            ruta (str): Ruta al archivo del diccionario
            
        Returns:
            dict: Diccionario {palabra: ponderación}
        """
        diccionario = {}
        try:
            with open(ruta, 'r', encoding='utf-8') as f:
                for linea in f:
                    linea = linea.strip()
                    if linea and ':' in linea:
                        palabra, ponderacion = linea.split(':')
                        diccionario[palabra.strip()] = int(ponderacion.strip())
        except FileNotFoundError:
            print(f"Error: No se encontró el archivo de diccionario en {ruta}")
        return diccionario
    
    def analizar_tokens(self, ruta_tokens, ruta_reporte):
        """
        Analiza los tokens y genera un reporte de sentimiento
        
        Args:
            ruta_tokens (str): Ruta al archivo con los tokens
            ruta_reporte (str): Ruta donde guardar el reporte
            
        Returns:
            dict: Resultados del análisis {
                'puntuacion_total': int,
                'palabras_positivas': dict,
                'palabras_negativas': dict,
                'palabra_mas_positiva': tuple,
                'palabra_mas_negativa': tuple
            }
        """
        resultados = {
            'puntuacion_total': 0,
            'palabras_positivas': defaultdict(int),
            'palabras_negativas': defaultdict(int),
            'palabra_mas_positiva': (None, 0),
            'palabra_mas_negativa': (None, 0)
        }
        
        # Leer tokens y calcular puntuaciones
        try:
            with open(ruta_tokens, 'r', encoding='utf-8') as f:
                for linea in f:
                    linea = linea.strip()
                    if linea and ',' in linea:
                        palabra, cantidad = linea.split(',')
                        palabra = palabra.strip()
                        cantidad = int(cantidad.strip())
                        
                        if palabra in self.palabras_ponderadas:
                            ponderacion = self.palabras_ponderadas[palabra]
                            puntuacion = ponderacion * cantidad
                            resultados['puntuacion_total'] += puntuacion
                            
                            if ponderacion > 0:
                                resultados['palabras_positivas'][palabra] += puntuacion
                                if puntuacion > resultados['palabra_mas_positiva'][1]:
                                    resultados['palabra_mas_positiva'] = (palabra, puntuacion)
                            else:
                                resultados['palabras_negativas'][palabra] += puntuacion
                                if puntuacion < resultados['palabra_mas_negativa'][1]:
                                    resultados['palabra_mas_negativa'] = (palabra, puntuacion)
        except FileNotFoundError:
            print(f"Error: No se encontró el archivo de tokens en {ruta_tokens}")
            return None
        
        # Generar reporte
        self._generar_reporte(resultados, ruta_reporte)
        
        return resultados
    
    def _generar_reporte(self, resultados, ruta_reporte):
        """
        Genera un reporte de análisis de sentimiento
        
        Args:
            resultados (dict): Resultados del análisis
            ruta_reporte (str): Ruta donde guardar el reporte
        """
        # Determinar sentimiento general
        if resultados['puntuacion_total'] > 0:
            sentimiento = "Positivo"
        elif resultados['puntuacion_total'] < 0:
            sentimiento = "Negativo"
        else:
            sentimiento = "Neutral"
        
        # Crear directorio si no existe
        os.makedirs(os.path.dirname(ruta_reporte), exist_ok=True)
        
        with open(ruta_reporte, 'w', encoding='utf-8') as f:
            f.write("=== Reporte de Análisis de Sentimiento ===\n\n")
            f.write(f"Sentimiento general: {sentimiento} ({resultados['puntuacion_total']})\n")
            f.write(f"Palabras positivas: {len(resultados['palabras_positivas'])}\n")
            if resultados['palabra_mas_positiva'][0]:
                f.write(f"Palabra más positiva: {resultados['palabra_mas_positiva'][0]}, {resultados['palabra_mas_positiva'][1]}\n")
            f.write(f"Palabras negativas: {len(resultados['palabras_negativas'])}\n")
            if resultados['palabra_mas_negativa'][0]:
                f.write(f"Palabra más negativa: {resultados['palabra_mas_negativa'][0]}, {resultados['palabra_mas_negativa'][1]}\n")
            
            # Detalle de palabras positivas
            f.write("\nDetalle palabras positivas:\n")
            for palabra, puntuacion in sorted(resultados['palabras_positivas'].items(), key=lambda x: x[1], reverse=True):
                f.write(f"- {palabra}: +{puntuacion}\n")
            
            # Detalle de palabras negativas
            f.write("\nDetalle palabras negativas:\n")
            for palabra, puntuacion in sorted(resultados['palabras_negativas'].items(), key=lambda x: x[1]):
                f.write(f"- {palabra}: {puntuacion}\n")

def analizar_sentimiento(ruta_tokens, ruta_diccionario, ruta_reporte):
    """
    Función principal para analizar sentimiento de tokens
    
    Args:
        ruta_tokens (str): Ruta al archivo con tokens
        ruta_diccionario (str): Ruta al diccionario de palabras ponderadas
        ruta_reporte (str): Ruta para guardar el reporte
    """
    analizador = AnalizadorSentimiento(ruta_diccionario)
    return analizador.analizar_tokens(ruta_tokens, ruta_reporte)