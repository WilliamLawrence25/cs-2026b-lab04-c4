from diagrams import Diagram, Cluster, Edge
from diagrams.onprem.client import Users
from diagrams.onprem.network import Nginx
from diagrams.programming.framework import Django
from diagrams.onprem.database import PostgreSQL
from diagrams.onprem.network import Internet
from diagrams.generic.device import Mobile

# Configuración visual del diagrama
graph_attr = {"fontsize": "20", "bgcolor": "white", "pad": "0.3"}

# El filename="img/despliegue" hará que se guarde automáticamente en la carpeta img/
with Diagram("BiblioUNSA - Vista de despliegue", filename="img/despliegue", show=False, direction="LR", graph_attr=graph_attr, outformat="png"):
    
    usuarios = Users("Estudiantes y\nBibliotecarios")
    dispositivo = Mobile("Navegador Web /\nMóvil")
    
    with Cluster("Servidor VPS (Un solo nodo)"):
        proxy = Nginx("Nginx Proxy\n(HTTPS)")
        
        with Cluster("Monolito en Capas"):
            app = Django("App BiblioUNSA\n(Lógica y Catálogo)")
            
        db = PostgreSQL("PostgreSQL\n(Datos transaccionales)")
        
    sso = Internet("Google Workspace\n(SSO UNSA)")
    api_academico = Internet("API Sistema\nAcadémico")
    
    # Conexiones
    usuarios >> dispositivo >> proxy >> app
    app >> Edge(label="Lectura/Escritura") >> db
    
    # Integraciones externas
    app >> Edge(label="Autenticación", style="dashed") >> sso
    app >> Edge(label="Validación Matrícula", style="dashed") >> api_academico