## **README.md**

# **Análisis de la Opinión sobre la Tasa Turística en Canarias**  
Este proyecto tiene como objetivo analizar la opinión de los residentes canarios mayores de 18 años sobre la implementación de una tasa turística. El estudio utiliza datos públicos para entender cómo la percepción sobre este impuesto varía según edad, sexo, territorios y finalidades específicas para las que debería destinarse la recaudación.

---

## **Estructura del Proyecto**

### **Archivos principales**
- **`src/`**: Contiene los módulos con el código fuente del proyecto.  
    - `main.py`: Punto de entrada del programa.  
    - `data_loader.py`: Funciones para la carga de datos desde archivos CSV.  
    - `models.py`: Contiene las clases `Entity`, `Territory` y `AgeGender` para estructurar los datos.  
    - `visualizations.py`: Incluye funciones para generar gráficos (barras, pie charts, heatmaps, gráficos interactivos).  
    - `constants.py`: Define las estructuras de datos, constantes, y parámetros estilísticos para las gráficas.  

- **`data/`**: Carpeta que contiene los archivos CSV.  
    - `territorios.csv`: Opinión por territorios.  
    - `edad_sexo.csv`: Opinión por grupos de edad y sexo.  

- **`figures/`**: Carpeta donde se guardan algunos ejemplo de gráficos.  

- **`requirements.txt`**: Lista de dependencias necesarias para ejecutar el proyecto.  

---

## **Instalación**

### **Requisitos**
- Python 3.8 o superior  
- pip (gestor de paquetes de Python)  

### **Instalar dependencias**
Ejecuta el siguiente comando para instalar las librerías necesarias:  

```bash
pip install -r requirements.txt
```

---

## **Descripción de los Datos**
El proyecto utiliza dos archivos CSV con la misma estructura básica:  

- **`territorios.csv`**: Muestra las opiniones según los territorios.  
- **`edad_sexo.csv`**: Detalla las opiniones según grupos de edad y sexo.  

Ambos ficheros contienen información sobre las finalidades para las que debería destinarse la recaudación, el porcentaje de apoyo, y el número de personas a favor.

---

## **Uso**

### **Ejecutar el Proyecto**
Puedes ejecutar el proyecto con el siguiente comando:  

```bash
python src/main.py
```

### **Funciones Principales**
1. **`read_csv()`**:  
   Carga y procesa los datos de un archivo CSV en listas de objetos `Territory` o `AgeGroup` según el parámetro indicado.
   
2. **Visualizaciones**:  
   El proyecto genera diferentes tipos de gráficos para interpretar los datos:
   - **Gráficos de barras**: Comparaciones entre territorios y finalidades.  
   - **Gráficos de pie**: Distribución de finalidades.  
   - **Heatmaps**: Visualización de porcentajes en distintas categorías.  
   - **Gráficos interactivos**: Explorar relaciones entre edad, sexo y territorio.  

---

## **Ejemplo de Código**  

```python
from data_loader import read_csv
from visualizations import plot_piechart_percentages

# Cargar datos desde el archivo de territorios
territories = read_csv('data/territorios.csv', tipo='territorio')

# Generar un gráfico de pie con los porcentajes medios por finalidad
plot_piechart_percentages(territories)
```

---

## **Librerías Utilizadas**
- **`csv`**: Lectura y escritura de archivos CSV.  
- **`matplotlib`**: Creación de gráficos como barras y pie charts.  
- **`seaborn`**: Generación de heatmaps y gráficos avanzados.  
- **`pandas`**: Manipulación y análisis de datos.  
- **`plotly`**: Creación de gráficos interactivos.  
- **`typing`**: Definición de tipos para una mejor organización del código.  

---

## **Estructura de Clases**

- **`Entity`**: Clase base compartida por `Territory` y `AgeGender`.  
- **`Territory`**: Representa los datos agrupados por regiones y su finalidad asociada.  
- **`AgeGender`**: Modela la información según los grupos de edad y sexo.  
- **Estructuras**:  
  - `PurposeStruct`: Contiene las finalidades de la tasa turística.  
  - `GenderStruct`: Define los códigos y nombres de sexos.  
  - `AgeStruct`: Almacena los grupos de edad con sus códigos.  

---

## **Modificaciones y Personalización**

### **Modificar el Tamaño de los Gráficos**  
El tamaño de los gráficos se puede ajustar cambiando el parámetro `FIG_SIZE` en el archivo **`constants.py`**.

```python
FIG_SIZE = (12, 8)  # Ancho y alto en pulgadas
```

Para gráficos de pie, el tamaño del círculo puede ajustarse directamente en el método `ax.pie()`:

```python
fig, ax = plt.subplots(figsize=(8, 8))  # Modificar el tamaño aquí
```