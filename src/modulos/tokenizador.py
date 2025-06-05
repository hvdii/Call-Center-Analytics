"""
Módulo de tokenización para español usando pyspellchecker

Características:
- Tokenización básica usando expresiones regulares
- Filtrado de palabras no reconocidas en español
- Conteo de frecuencias
- Persistencia de resultados
"""

import re
import os
from collections import Counter
from spellchecker import SpellChecker

class Tokenizador:
    def __init__(self):
        # Diccionario de español proporcionado por pyspellchecker
        self.spell = SpellChecker(language='es')
    
    def procesar_texto(self, texto, archivo_salida):
        """
        Procesa el texto y actualiza el archivo de conteo de tokens válidos
        
        Args:
            texto (str): Texto a tokenizar
            archivo_salida (str): Ruta al archivo de salida
            
        Returns:
            dict: Diccionario con palabras válidas y sus conteos
        """
        # Cargar conteos existentes
        conteos = self._cargar_conteos(archivo_salida)
        
        # Tokenizar: obtener palabras del texto
        palabras = re.findall(r'\b\w+\b', texto.lower())
        
        # Contar palabras válidas
        for palabra in palabras:
            if palabra.isalpha() and palabra in self.spell:
                conteos[palabra] += 1
        
        # Guardar resultados
        self._guardar_conteos(conteos, archivo_salida)
        
        return conteos
    
    def _cargar_conteos(self, archivo):
        """Cargar conteos existentes desde archivo"""
        conteos = Counter()
        if os.path.exists(archivo):
            with open(archivo, 'r', encoding='utf-8') as f:
                for linea in f:
                    palabra, cantidad = linea.strip().split(',')
                    conteos[palabra] = int(cantidad)
        return conteos
    
    def _guardar_conteos(self, conteos, archivo):
        """Guardar conteos en archivo"""
        os.makedirs(os.path.dirname(archivo), exist_ok=True)
        with open(archivo, 'w', encoding='utf-8') as f:
            for palabra, cantidad in sorted(conteos.items()):
                f.write(f"{palabra},{cantidad}\n")

def tokenizar_archivo(ruta_entrada, ruta_salida):
    """
    Función principal para tokenizar un archivo de texto
    
    Args:
        ruta_entrada (str): Ruta al archivo con el texto
        ruta_salida (str): Ruta para guardar los tokens
    """
    tokenizador = Tokenizador()
    
    with open(ruta_entrada, 'r', encoding='utf-8') as f:
        texto = f.read()
    
    return tokenizador.procesar_texto(texto, ruta_salida)
