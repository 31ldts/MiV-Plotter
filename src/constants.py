from matplotlib.colors import LinearSegmentedColormap
from typing import Dict

# Encoding used for reading files
ENCODING = 'utf-8'

# Constant to exclude certain categories from processing
EXCLUDED_CATEGORY = '_T'

# Styling for bounding boxes used in graphs
BBOX_STYLE = dict(facecolor='white', alpha=0.6, boxstyle='round,pad=0.5')

# Default size for figures (width, height)
FIG_SIZE = (10, 6)

# Set of colors used across graphs
PRIMARY_COLOR = '#ee9b00'
PIE_COLORS = ["#005f73", "#0a9396", "#94d2bd", "#e9d8a6", "#ee9b00"]
GENERAL_COLORS = ["#0a9396", "#94d2bd", "#e9d8a6", "#ee9b00"]

# Custom colormap created for the heatmap
CMAP = LinearSegmentedColormap.from_list("mi_cmap", GENERAL_COLORS)

class PurposeStruct:
    """Stores purposes and their abbreviated codes."""
    PURPOSES: Dict[str, str] = {
        "CUALQUIER_FIN_SERVICIO_CANARIAS": "CFSC",
        "MEJORAR_CALIDAD_ENTORNOS_TURISTICOS": "MCET",
        "MEJORAR_CONDICIONES_VIDA_CANARIAS": "MCVC",
        "MEJORAR_DESARROLLO_ECONOMICO_CANARIAS": "MDEC",
        "MEJORAR_PROTEGER_MEDIO_AMBIENTE_CANARIAS": "MPMAC",
        "_T": "T"
    }

class GenderStruct:
    """Stores gender codes and their corresponding names."""
    GENDERS: Dict[str, str] = {
        "F": "Femenino",
        "M": "Masculino",
        "_T": "Total"
    }

class AgeStruct:
    """Strores age group codes and their corresponding ranges."""
    AGE_GROUPS: Dict[str, str] = {
        "Y_GE55": "> 55",
        "Y35T54": "35 - 54",
        "Y18T34": "18 - 34",
        "_T": "Total"
    }
