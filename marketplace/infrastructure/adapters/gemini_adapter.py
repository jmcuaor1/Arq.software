"""
Adapter concreto para Google Gemini AI (google-genai SDK).
Implementa DescriptionGeneratorPort (Dependency Inversion Principle).
El dominio depende del puerto abstracto; esta clase es la implementación concreta de infraestructura.
"""
import os
from google import genai

from marketplace.domain.ports import DescriptionGeneratorPort


class GeminiAdapter(DescriptionGeneratorPort):
    """
    Llama a Google Gemini Flash para generar descripciones de productos.
    GEMINI_API_KEY debe estar en variables de entorno.
    """

    PROMPT_TEMPLATE = (
        "Eres un experto en marketing para un marketplace vecinal colombiano llamado VecinoMarket. "
        "Genera una descripción atractiva de 2 a 3 oraciones en español para vender el siguiente producto o servicio: '{nombre}'. "
        "La descripción debe ser clara, honesta y motivar al comprador. "
        "Solo retorna el texto de la descripción, sin comillas ni encabezados."
    )

    def __init__(self):
        api_key = os.environ.get("GEMINI_API_KEY", "")
        self._client = genai.Client(api_key=api_key) if api_key else None

    def generar_descripcion(self, nombre_producto: str) -> str:
        if not self._client:
            return ""

        try:
            prompt = self.PROMPT_TEMPLATE.format(nombre=nombre_producto)
            response = self._client.models.generate_content(
                model="gemini-2.0-flash",
                contents=prompt,
            )
            return response.text.strip()
        except Exception as e:
            print(f"[GeminiAdapter] Error al generar descripción: {e}")
            return ""
