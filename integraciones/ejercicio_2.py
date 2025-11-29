import os
import requests
import json
import time
from pinecone import Pinecone
from sentence_transformers import SentenceTransformer
from dotenv import load_dotenv

load_dotenv()

class RecetasRAG:

    
    def __init__(self):
        self.pc = Pinecone(api_key=os.getenv('PINECONE_API_KEY'))
        self.embedder = SentenceTransformer('all-MiniLM-L6-v2')
        self.index_name = os.getenv('PINECONE_API_INDEX')
        self.setup_pinecone()

    
    def setup_pinecone(self):
        """ Conectar con el índice de Pinecone """
        try:
            if self.index_name not in self.pc.list_indexes().names():
                print(f"El índice '{self.index_name}' no existe")
                return False
            self.index = self.pc.Index(self.index_name)
            print(f"Conectado al índice: {self.index_name}")
            return True
        except Exception as e:
            print(f"Error conectando a Pinecone: {e}")
            return False

    
    def limpiar_y_cargar_desde_json(self, ruta_archivo=None):
        """ Borra Todas las recetas y carga desde JSON - Ideal para datos actualizados """
        if ruta_archivo is None:
            ruta_archivo="static/json/recetas.json"

        try:
            print("Iniciando refresh completo de la base de datos")

            #1 Cargar el JSON actualizado primero
            base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
            ruta_completa = os.path.join(base_dir, ruta_archivo)

            print(f"Cargando recetas desde : {ruta_completa}")

            with open(ruta_completa, 'r', encoding='utf-8') as f:
                recetas_actualizadas = json.load(f)

            
            print(f"JSON cargando con {len(recetas_actualizadas)} recetas actualizadas")

            #2. Borrar todo el contenido del índice
            print("Eliminando todas las recetas existentes")
            self.index.delete(delete_all=True)

            #pequeña pausa para asegurar que la eliminación se procese
            time.sleep(2)

            #3. Cargar las recetas actualizadas
            vertors = []
            for receta in recetas_actualizadas:
                #crear texto para embedding
                texto = f"{receta['nombre']} {receta['ingredientes']} {receta['categoria']}"
                embedding = self.embedder.encode(texto).tolist()

                vertors.append({
                    "id": receta["id"],
                    "values": embedding,
                    "metadata": receta
                })
            
            #4. Insertar en Pinecone
            self.index.upsert(vectors=vertors)

            #5. Verificar carga exitosa
            stats_final = self.index.describe_index_stats()

            mensaje = f"Base de datos actualizada: {len(recetas_actualizadas)} recetas cargadas desde JSON"
            print(mensaje)
            return mensaje


        except FileNotFoundError:
            error_msg = f"Archivo no encontrado"
            print(error_msg)
            return error_msg
        except json.JSONDecodeError as e:
            error_msg = f"Error decodificando JSON {e}"
            print(error_msg)
            return error_msg
        except Exception as e:
            error_msg = f"Error en refresh {e}"
            print(error_msg)
            return error_msg
        
    
    def buscar_recetas_similares(self, consulta, top_k=5):
        """ Busca recetas similares usando embeddings"""
        try:
            #generar embedding de la consulta
            query_embedding = self.embedder.encode(consulta).tolist()
            #buscar en Pinecone | especie de query sql select * from tabla
            results = self.index.query(
                vector= query_embedding,
                top_k= top_k,
                include_metadata = True
            )
            recetas_encontradas = []
            for result in results.matches:
                receta = result.metadata
                receta['score'] = result.score
                recetas_encontradas.append(receta)
            
            
            return recetas_encontradas
        
        except Exception as e:
            print(f"Error buscando recetas: {e}")
            return []
        

    def obtener_estadisticas(self):
        """ obtiene estadísticas de la base de datos """
        try:
            stats = self.index.describe_index_stats()
            return {
                'total_recetas': stats.total_vector_count,
                'dimension': stats.dimension,
                'index_fullness': stats.index_fullness
            }
        except Exception as e:
            print(f"Error obteniendo estadísticas: {e}")
            return None


#functión principal
def get_recetas_rag(ia, consulta):
    rag_recetas = RecetasRAG()

    #verificar conexión
    if not hasattr(rag_recetas, 'index') or rag_recetas.index is None:
        return "Error: No se pudo conectar a la base de datos de recetas"
    
    #verificar si hay datos
    try:
        stats = rag_recetas.obtener_estadisticas()
        if stats and stats['total_recetas'] ==0:
            return "La base de datos está vacía. Por favor, actualiza los datos"
        else:
            print(f"Buscando en {stats['total_recetas']} recetas...")

    except Exception as e:
        return "Error accediendo a la base de datos"
    
    #buscar recetas similares
    recetas_encontradas = rag_recetas.buscar_recetas_similares(consulta)

    if not recetas_encontradas:
        return "No encontré recetas simulares en la base de datos. Intenta con otro ingredientes o categorías"
    
    #usa la IA selecciona
    if ia =="Mistral":
        return buscar_recetas_mistral(consulta, recetas_encontradas)
    if ia =="Gemini":
        return "sss"
    if ia =="Claude":
        return "sss"
    if ia =="Deepseek":
        return "sss"
    if ia =="OpenAI":
        return "sss"
    
    return "IA no implentada aún"


def buscar_recetas_mistral(consulta, recetas_contexto):
    prompt=f"""
    Eres un chef asistente. Basándote en estas recetas encontradas:

    {json.dumps(recetas_contexto, indent=2, ensure_ascii=False)}

    Responde a: "{consulta}"
    INSTRUCCIONES:
    - Recomienda recetas relevantes de la lista
    - Si no hay coincidencias, sugiere alternativas
    - Incluye información práctica como tiempo y dificultad
    - Responde en español de forma clara y profesional
    """
    data = {
        "model": "mistral-small",
        "messages": [{"role": "user", "content": prompt}],
        "temperature": 0.3,
        "max_tokens": 500
    }
    try:
        response = requests.post(
            f"{os.getenv('MISTRAL_BASE_URL')}chat/completions",
            headers={
                "Content-Type":"application/json",
                "Authorization": f"Bearer {os.getenv('MISTRAL_API_KEY')}"
            },
            json = data,
            timeout= 60
        )
        if response.status_code==200:
            return response.json()['choices'][0]["message"]["content"]
        else:
            return f"Error en la búsqueda: {response.status_code} - {response.text}"
    except Exception as e:
        return f"Error de conexión con Mistral: {str(e)}"