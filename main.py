import csv
import matplotlib.pyplot as plt
from matplotlib.colors import LinearSegmentedColormap
from typing import List, Dict, Union
import seaborn as sns
import pandas as pd
import plotly.express as px


# ==============================
# Constantes y Configuración
# ==============================
ENCODING = 'utf-8'
FINALIDADES_EXCLUIR = '_T'
BBOX_STYLE = dict(facecolor='white', alpha=0.6, boxstyle='round,pad=0.5')
FIG_SIZE = (10, 6)
COLOR = '#ee9b00'
COLORES_PIE = ["#005f73", "#0a9396", "#94d2bd", "#e9d8a6", "#ee9b00"]
COLORES = ["#0a9396", "#94d2bd", "#e9d8a6", "#ee9b00"]
CMAP = LinearSegmentedColormap.from_list("mi_cmap", COLORES)

# ==============================
# Estructuras de Datos
# ==============================
class FinalidadStruct:
    """Almacena las finalidades y sus códigos abreviados."""
    FINALIDADES: Dict[str, str] = {
        "CUALQUIER_FIN_SERVICIO_CANARIAS": "CFSC",
        "MEJORAR_CALIDAD_ENTORNOS_TURISTICOS": "MCET",
        "MEJORAR_CONDICIONES_VIDA_CANARIAS": "MCVC",
        "MEJORAR_DESARROLLO_ECONOMICO_CANARIAS": "MDEC",
        "MEJORAR_PROTEGER_MEDIO_AMBIENTE_CANARIAS": "MPMAC",
        "_T": "T"
    }

class SexoStruct:
    """Almacena los sexos y sus códigos."""
    SEXO: Dict[str, str] = {
        "F": "Femenino",
        "M": "Masculino",
        "_T": "Total"
    }

class EdadStruct:
    """Almacena las edades y sus códigos."""
    EDAD: Dict[str, str] = {
        "Y_GE55": "> 55",
        "Y35T54": "35 - 54",
        "Y18T34": "18 - 34",
        "_T": "Total"
    }

class Entidad:
    """Clase base compartida entre Territorio y GrupoEdad."""
    def __init__(self):
        self.finalidades: Dict[str, Dict[str, Union[int, float]]] = {
            f: {"poblacion": 0, "porcentaje": 0.0} for f in FinalidadStruct.FINALIDADES
        }

    def actualizar_finalidad(self, finalidad: str, poblacion: int = None, porcentaje: float = None):
        """Actualiza los valores de población o porcentaje para una finalidad."""
        if finalidad in self.finalidades:
            if poblacion is not None:
                self.finalidades[finalidad]["poblacion"] = poblacion
            if porcentaje is not None:
                self.finalidades[finalidad]["porcentaje"] = porcentaje

class Territorio(Entidad):
    """Representa un territorio con sus finalidades y mantiene el mayor porcentaje registrado."""
    porcentaje_mas_alto: float = 0.0

    def __init__(self, nombre: str):
        super().__init__()
        self.nombre = nombre

    def actualizar_finalidad(self, finalidad: str, poblacion: int = None, porcentaje: float = None):
        super().actualizar_finalidad(finalidad, poblacion, porcentaje)
        if finalidad != FINALIDADES_EXCLUIR and porcentaje is not None:
            Territorio.porcentaje_mas_alto = max(Territorio.porcentaje_mas_alto, porcentaje)

class GrupoEdad(Entidad):
    """Representa un grupo de edad y sexo con sus finalidades."""
    def __init__(self, edad: str, sexo: str):
        super().__init__()
        self.edad = edad
        self.sexo = sexo

# ==============================
# Funciones de Lectura de Datos
# ==============================
def leer_csv(path: str, tipo: str) -> List[Union[Territorio, GrupoEdad]]:
    """Lee un CSV y crea una lista de objetos Territorio o GrupoEdad según el tipo."""
    entidades = {} if tipo == 'territorio' else []

    with open(path, newline='', encoding=ENCODING) as file:
        reader = csv.DictReader(file)

        for row in reader:
            nombre = row.get('TERRITORIO#es') if tipo == 'territorio' else EdadStruct.EDAD[row.get('EDAD_CODE')]
            sexo = SexoStruct.SEXO[row.get('SEXO_CODE')] if tipo == 'grupo_edad' else None
            finalidad = row['TASA_TURISTICA_FINALIDAD_CODE']
            valor = row['OBS_VALUE']

            entidad = None
            if tipo == 'territorio':
                entidad = entidades.get(nombre) or Territorio(nombre)
                entidades[nombre] = entidad
            else:
                entidad = next((e for e in entidades if e.edad == nombre and e.sexo == sexo), None)
                if not entidad:
                    entidad = GrupoEdad(nombre, sexo)
                    entidades.append(entidad)

            try:
                valor_int = int(valor)
                entidad.actualizar_finalidad(finalidad, poblacion=valor_int)
            except ValueError:
                entidad.actualizar_finalidad(finalidad, porcentaje=float(valor))
    
    return list(entidades.values()) if tipo == 'territorio' else entidades

# ==============================
# Funciones para Generar Leyendas
# ==============================
def _preparar_leyenda(
    nombres: List[str] = None, 
    x_labels: List[str] = None, 
    incluir_finalidades: bool = False
) -> str:
    """Genera una leyenda flexible que puede incluir nombres, etiquetas y abreviaciones."""
    partes_leyenda = ["Leyenda:"]

    # Agregar leyenda de nombres y etiquetas, si están presentes
    if nombres and x_labels:
        partes_leyenda.append("\n".join(f"· {x}: {n}" for x, n in zip(x_labels, nombres)))

    # Agregar leyenda de finalidades, si está activado
    if incluir_finalidades:
        finalidades = [
            f"· {valor}: {clave.replace('_', ' ').title()}"
            for clave, valor in FinalidadStruct.FINALIDADES.items()
            if clave != FINALIDADES_EXCLUIR
        ]
        partes_leyenda.append("\n".join(finalidades))

    # Combinar todas las partes con saltos de línea
    return "\n".join(partes_leyenda)

# ==============================
# Funciones para Graficar
# ==============================
def _graficar_barras(titulo: str, etiquetas: List[str], valores: List[float], leyenda: str, 
                     leyenda_pos_x: float, color: str, lim_y: Union[float, None] = None):
    """Grafica un gráfico de barras."""
    
    # Crear una nueva figura para el gráfico con el tamaño especificado por FIG_SIZE.
    plt.figure(figsize=FIG_SIZE)
    
    # Dibujar un gráfico de barras con las etiquetas en el eje X y los valores correspondientes.
    # El color de las barras es determinado por el parámetro 'color'.
    plt.bar(etiquetas, valores, color=color)
    
    # Configurar la rotación de las etiquetas del eje X en 0 grados (horizontal).
    plt.xticks(rotation=0)
    
    # Establecer el título del gráfico usando el valor del parámetro 'titulo'.
    plt.title(titulo)
    
    # Etiquetar del eje X como "Categorías" para indicar el tipo de datos.
    plt.xlabel("Categorías")
    
    # Etiquetar del eje Y como "Porcentaje (%)" para mostrar la métrica que se grafica.
    plt.ylabel("Porcentaje (%)")
    
    # Si se especifica un límite para el eje Y (lim_y), se establece de 0 al valor indicado.
    if lim_y:
        plt.ylim(0, lim_y)
    
    # Añadir la leyenda al gráfico en la posición (leyenda_pos_x, 0.5). 
    # Ajustar el tamaño de la fuente y estilo del cuadro de la leyenda con 'BBOX_STYLE'.
    plt.gcf().text(leyenda_pos_x, 0.5, leyenda, fontsize=10, va='center', ha='left', bbox=BBOX_STYLE)
    
    # Ajustar automáticamente los márgenes de la figura para que todo el contenido se muestre sin solapamientos.
    # El parámetro 'rect' ajusta el área de dibujo para que deje espacio según 'leyenda_pos_x'.
    plt.tight_layout(rect=[0, 0, leyenda_pos_x, 1])
    
    # Mostrar el gráfico generado en pantalla.
    plt.show()

def graficar_porcentajes_territorios(territorios: List[Territorio], escala: bool = True, color: str = COLOR):
    """Grafica los porcentajes por finalidad para cada territorio."""
    
    # Filtrar las finalidades excluyendo una específica definida por la constante 'FINALIDADES_EXCLUIR'.
    finalidades = [f for f in FinalidadStruct.FINALIDADES if f != FINALIDADES_EXCLUIR]
    
    nombres_territorios = [t.nombre for t in territorios]
    
    # Crear etiquetas abreviadas usando solo las letras mayúsculas de los nombres de los territorios.
    x_labels = [''.join(filter(str.isupper, t.nombre)) for t in territorios]
    
    leyenda = _preparar_leyenda(nombres_territorios, x_labels)

    for finalidad in finalidades:
        
        # Obtener los porcentajes asociados a la finalidad actual para cada territorio.
        porcentajes = [t.finalidades[finalidad]['porcentaje'] for t in territorios]
        
        # Calcular el límite superior del eje Y. Si 'escala' es True, usa el porcentaje más alto global;
        # si no, usa el mayor valor de los porcentajes actuales.
        max_limite = (Territorio.porcentaje_mas_alto if escala else max(porcentajes)) + 5

        _graficar_barras(
            f"Porcentaje de {finalidad} por Territorio", 
            x_labels, porcentajes, leyenda, 0.65, color, max_limite
        )

def graficar_media_porcentajes_territorios(territorios: List[Territorio], color: str = COLOR):
    """Grafica la media de porcentajes de finalidades entre los territorios."""
    
    # Filtra las finalidades excluyendo una específica definida por la constante 'FINALIDADES_EXCLUIR'.
    finalidades = [f for f in FinalidadStruct.FINALIDADES if f != FINALIDADES_EXCLUIR]
    
    # Calcular la media de los porcentajes para cada finalidad.
    # Crear un diccionario donde la clave es la abreviación de la finalidad y el valor es la media.
    media_porcentajes = {
        FinalidadStruct.FINALIDADES[f]: sum(t.finalidades[f]['porcentaje'] for t in territorios) / len(territorios)
        for f in finalidades
    }

    leyenda = _preparar_leyenda(incluir_finalidades=True)
    _graficar_barras("Media de Porcentajes por Finalidad (Territorios)", list(media_porcentajes.keys()), list(media_porcentajes.values()), leyenda, 0.55, color, max(media_porcentajes.values()) + 5)

def graficar_piechart_porcentajes(territorios: List[Territorio], pie_colors: List[str] = COLORES_PIE):
    """Genera un gráfico de pie que muestra la distribución de medias de porcentajes por finalidad."""

    # Inicializar diccionarios para almacenar las sumas de porcentajes y el recuento por finalidad
    media_porcentajes = {name: 0.0 for name in FinalidadStruct.FINALIDADES if name != FINALIDADES_EXCLUIR}
    divisor = {name: 0 for name in FinalidadStruct.FINALIDADES if name != FINALIDADES_EXCLUIR}

    # Recorrer todos los territorios para acumular los porcentajes y contar ocurrencias por finalidad
    for territorio in territorios:
        for finalidad in FinalidadStruct.FINALIDADES:
            if finalidad != FINALIDADES_EXCLUIR:
                porcentaje = territorio.finalidades[finalidad]['porcentaje']
                media_porcentajes[finalidad] += porcentaje
                divisor[finalidad] += 1

    # Calcular la media de porcentajes para cada finalidad
    for finalidad in media_porcentajes.keys():
        if divisor[finalidad] > 0:  # Evitar división por cero
            media_porcentajes[finalidad] /= divisor[finalidad]

    # Crear la figura y los ejes para el gráfico
    fig, ax = plt.subplots(figsize=FIG_SIZE)

    # Graficar el gráfico de pie
    wedges, texts, autotexts = ax.pie(
        media_porcentajes.values(),  # Valores que corresponden a los porcentajes medios
        autopct='%1.1f%%',  # Mostrar los porcentajes en el gráfico
        startangle=90,  # Iniciar el gráfico desde el ángulo de 90 grados
        colors=pie_colors[:len(media_porcentajes)]  # Usar solo los colores necesarios
    )

    # Igualar los ejes para que el gráfico tenga forma circular
    ax.axis('equal')

    # Añadir título al gráfico
    plt.title("Distribución de Medias de Porcentajes por Finalidad")

    # Crear una lista de etiquetas formateadas para la leyenda
    leyenda = [
        f"{finalidad.replace('_', ' ').title()}"  # Reemplazar guiones bajos y capitalizar palabras
        for finalidad in media_porcentajes
    ]

    # Añadir leyenda al gráfico, ubicada a la derecha del gráfico de pie
    ax.legend(
        leyenda,  # Utilizar las etiquetas formateadas
        title="Leyenda:",  # Título de la leyenda
        alignment="left",  # Alinear a la izquierda
        loc="center left",  # Ubicar en el centro a la izquierda del gráfico
        bbox_to_anchor=(1, 0.5),  # Anclar la leyenda a la derecha del gráfico
        ncol=1  # Mostrar en una columna
    )

    # Ajustar el diseño para evitar solapamientos
    plt.tight_layout()

    # Mostrar el gráfico
    plt.show()

def graficar_heatmap_territorios(territorios: List[Territorio]):
    """Genera un heatmap que visualiza los porcentajes por territorio y finalidad."""

    # Construir un diccionario de datos: las claves son las abreviaturas de los territorios 
    # y los valores son listas con los porcentajes de cada finalidad.
    data = {
        ''.join(filter(str.isupper, t.nombre)):  # Extraer las letras mayúsculas del nombre del territorio.
        [t.finalidades[f]['porcentaje'] for f in FinalidadStruct.FINALIDADES if f != FINALIDADES_EXCLUIR]
        for t in territorios  # Recorrer todos los territorios y almacenar los porcentajes.
    }

    # Crear un DataFrame de pandas para estructurar los datos (filas = finalidades, columnas = territorios).
    df = pd.DataFrame(
        data,
        index=[FinalidadStruct.FINALIDADES[f] for f in FinalidadStruct.FINALIDADES if f != FINALIDADES_EXCLUIR]
    )

    # Preparar los nombres completos y abreviados de los territorios.
    nombres = [t.nombre for t in territorios]
    x_labels = [''.join(filter(str.isupper, t.nombre)) for t in territorios]

    # Crear la figura del gráfico de heatmap.
    plt.figure(figsize=(10, 8))

    # Generar el heatmap utilizando seaborn.
    sns.heatmap(df, annot=True, cmap=CMAP, fmt=".1f")

    # Añadir título y etiquetas de los ejes.
    plt.title("Heatmap de Porcentajes por Territorio y Finalidad")
    plt.xlabel("Territorios")
    plt.ylabel("Finalidades")

    # Preparar la leyenda con los territorios y las finalidades.
    leyenda = _preparar_leyenda(nombres=nombres, x_labels=x_labels, incluir_finalidades=True)

    # Añadir la leyenda a la figura en la posición especificada.
    plt.gcf().text(0.7, 0.5, leyenda, fontsize=10, va='center', ha='left', bbox=BBOX_STYLE)

    # Ajustar el diseño para evitar solapamientos.
    plt.tight_layout(rect=[0, 0, 0.7, 1])

    # Mostrar el gráfico.
    plt.show()

def graficar_interactivo_edad_sexo(grupos: List[GrupoEdad], mostrar_total: bool = False, mostrar_solo_edades: bool = False):
    """Genera un gráfico interactivo de porcentajes por edad y sexo con texturas.
    
    Args:
        grupos (List[GrupoEdad]): Lista de grupos de edad y sexo.
        mostrar_total (bool): Si es True, muestra solo el total; si es False, muestra Masculino y Femenino.
        mostrar_solo_edades (bool): Si es True, muestra solo los grupos de edad sin el total; 
                                     si es False, incluye el total.
    """
    data = []

    # Recopilar los datos de cada grupo de edad y sexo
    for grupo in grupos:
        for finalidad in FinalidadStruct.FINALIDADES:
            # Excluir finalidades según la constante FINALIDADES_EXCLUIR
            if finalidad == FINALIDADES_EXCLUIR:
                continue
            
            porcentaje = grupo.finalidades[finalidad]['porcentaje']
            data.append({
                "Edad": grupo.edad,
                "Sexo": grupo.sexo,
                "Finalidad": FinalidadStruct.FINALIDADES[finalidad],  # Usar el nombre completo de la finalidad
                "Porcentaje": porcentaje
            })

    df = pd.DataFrame(data)

    # Comprobar si hay datos disponibles para evitar errores
    if df.empty:
        print("No hay datos para graficar.")
        return

    # Definir el orden deseado para los grupos de edad
    orden_edad = ["18 - 34", "35 - 54", "> 55", "Total"]
    
    # Convertir la columna 'Edad' a tipo categórico con el orden específico
    df['Edad'] = pd.Categorical(df['Edad'], categories=orden_edad, ordered=True)

    # Definir el orden específico para las finalidades
    orden_finalidades = [
        "MEJORAR_CALIDAD_ENTORNOS_TURISTICOS",  # MCET
        "MEJORAR_CONDICIONES_VIDA_CANARIAS",    # MCVC
        "MEJORAR_DESARROLLO_ECONOMICO_CANARIAS", # MDEC
        "MEJORAR_PROTEGER_MEDIO_AMBIENTE_CANARIAS", # MPMAC
        "CUALQUIER_FIN_SERVICIO_CANARIAS"       # CFSC
    ]
    
    # Convertir la columna 'Finalidad' a tipo categórico con el orden específico
    df['Finalidad'] = pd.Categorical(df['Finalidad'], categories=[FinalidadStruct.FINALIDADES[f] for f in orden_finalidades], ordered=True)

    # Filtrar los datos según el parámetro mostrar_total
    if mostrar_total:
        df = df[df['Sexo'] == 'Total']
    else:
        df = df[df['Sexo'].isin(['Masculino', 'Femenino'])]

    # Filtrar los datos según el parámetro mostrar_solo_edades
    if mostrar_solo_edades:
        df = df[df['Edad'] != "Total"]

    # Asegurarse de que el orden de los datos se aplique al DataFrame
    df = df.sort_values(by=['Edad', 'Finalidad'])

    # Crear el gráfico de barras interactivo
    fig = px.bar(
        df, 
        x='Edad', 
        y='Porcentaje', 
        color='Finalidad', 
        barmode='group', 
        facet_col='Sexo' if not mostrar_total else None,  # Eliminar facet_col si mostrar_total es True
        title="Porcentajes por Edad, Sexo y Finalidad",
        labels={"Porcentaje": "Porcentaje (%)", "Edad": "Grupos de Edad"},
        pattern_shape='Finalidad',  # Agregar texturas en función de la finalidad
        pattern_shape_sequence=["/", "+", "\\", "x", "."]  # Diferentes patrones/texturas
    )
    
    # Ajustar el diseño del gráfico
    fig.update_layout(
        xaxis_title="Grupos de Edad",
        yaxis_title="Porcentaje (%)",
        legend_title="Finalidad",
        height=600,  # Ajusta la altura si es necesario
        template="plotly_white"  # Usar un tema claro para mejorar la legibilidad
    )
    
    fig.show()

def graficar_mapa_interactivo(territorios: List[Territorio]):
    """Genera un mapa interactivo de las Islas Canarias sin el territorio 'Canarias'."""

    # Coordenadas de las islas Canarias
    coordenadas = {
        'Tenerife - Sur': (28.0916, -16.6291),
        'Tenerife - Norte': (28.4753, -16.4167),
        'Tenerife - Área Metropolitana': (28.4633, -16.2519),
        'Tenerife': (28.2916, -16.6291),
        'Lanzarote': (29.0469, -13.6414),
        'La Palma': (28.6569, -17.8966),
        'La Gomera': (28.1088, -17.1023),
        'Gran Canaria - Sur': (27.8050, -15.5766),
        'Gran Canaria - Norte': (28.1463, -15.6586),
        'Gran Canaria - Área Metropolitana': (28.1038, -15.4131),
        'Gran Canaria': (27.95, -15.5),
        'Fuerteventura': (28.3587, -14.034),
        'El Hierro': (27.7414, -18.0310)
    }

    # Filtrar territorios para eliminar 'Canarias' y crear el DataFrame
    data = [
        {
            "Isla": t.nombre,
            "Lat": coordenadas[t.nombre][0],
            "Lon": coordenadas[t.nombre][1],
            **{
                FinalidadStruct.FINALIDADES[f]: f"{t.finalidades[f]['porcentaje']}%"
                for f in FinalidadStruct.FINALIDADES if f != FINALIDADES_EXCLUIR
            }
        }
        for t in territorios if t.nombre != 'Canarias'
    ]

    df = pd.DataFrame(data)

    # Comprobar si hay datos disponibles para evitar errores
    if df.empty:
        print("No hay datos para graficar el mapa.")
        return

    # Crear el mapa interactivo
    fig = px.scatter_mapbox(
        df,
        lat='Lat',
        lon='Lon',
        title="Mapa Interactivo de las Islas Canarias",
        size_max=15,
        zoom=6,
        mapbox_style='open-street-map'
    )

    # Configurar el hovertemplate
    fig.update_traces(
        marker=dict(size=14),
        hovertemplate='<b>%{hovertext}</b><br>%{customdata}<extra></extra>',
        hovertext=df['Isla'],
        customdata=df.drop(columns=['Isla', 'Lat', 'Lon']).apply(
            lambda row: '<br>'.join(
                [f"{FinalidadStruct.FINALIDADES[f]}={row[FinalidadStruct.FINALIDADES[f]]}" 
                 for f in FinalidadStruct.FINALIDADES if f != FINALIDADES_EXCLUIR]
            ),
            axis=1
        )
    )

    # Preparar y agregar la leyenda
    leyenda = _preparar_leyenda(incluir_finalidades=True)
    fig.add_annotation(
        text=leyenda.replace('\n', '<br>'),
        xref="paper", yref="paper",
        x=0.98, y=0.05,
        showarrow=False,
        font=dict(size=12),
        align="left",
        bordercolor="black",
        borderwidth=2,
        bgcolor="white",
        borderpad=4,
        opacity=0.8
    )

    # Mostrar el mapa
    fig.show()


# ==============================
# Ejecución Principal
# ==============================
territorios = leer_csv(path='territorios.csv', tipo='territorio')
edad_sexo = leer_csv(path='edad_sexo.csv', tipo='grupo_edad')

graficar_porcentajes_territorios(territorios)
graficar_porcentajes_territorios(territorios=territorios, escala=False)
graficar_media_porcentajes_territorios(territorios)
graficar_piechart_porcentajes(territorios=territorios)
graficar_heatmap_territorios(territorios=territorios)

graficar_interactivo_edad_sexo(grupos=edad_sexo)
graficar_interactivo_edad_sexo(grupos=edad_sexo, mostrar_total=True, mostrar_solo_edades=True)

graficar_mapa_interactivo(territorios=territorios)
