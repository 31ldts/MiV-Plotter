
import matplotlib.pyplot as plt
from typing import List, Union
import seaborn as sns
import pandas as pd
import plotly.express as px
from constants import *
from models import *
from data_loader import *

def _generate_legend(
        names: List[str] = None, 
        abbreviations: List[str] = None, 
        include_purposes: bool = False
    ) -> str:

    """
    Create a legend.

    Args:
        names (List[str]): List with names.
        abbreviations (List[str]): List with names' abbreviations.
        include_purposes (bool): If True, include purposes names and abbreviations;
                                 if False, not.

    Returns:
        str: Structured legend.
    """

    sections = ["Leyenda:"]

    # Add territories names and labels if provided
    if names and abbreviations:
        sections.append("\n".join(f"· {x}: {n}" for x, n in zip(abbreviations, names)))

    # Add purposes if required
    if include_purposes:
        purposes = [
            f"· {value}: {key.replace('_', ' ').title()}"
            for key, value in PurposeStruct.PURPOSES.items()
            if key != EXCLUDED_CATEGORY
        ]
        sections.append("\n".join(purposes))

    return "\n".join(sections)

def _plot_bar_chart(
        title: str, 
        categories: List[str], 
        values: List[float], 
        legend: str, 
        legend_pos_x: float, 
        color: str, 
        y_limit: Union[float, None] = None
    ) -> None:

    """
    Create a bar chart.

    Args:
        title (str): Plot title
        categories (List[str]): Plot categories
        values (List[float]): Plot data
        legend (str): Plot legend
        legend_pos_x (float): Legend x-axis coordenade.
        y_limit (float, None): Y-axis value.
        color (str): color in hexadecimal format.

    Returns:
        None
    """
    
    plt.figure(figsize=FIG_SIZE)    # Create a figura with specific dimensions
    
    plt.bar(categories, values, color=color)    # Draw a bar chart with the provided categories and values
    
    plt.xticks(rotation=0)      # Roate the x-axis labels horizontally
    
    plt.title(title)    # Set the chart title
    
    plt.ylabel("Porcentaje (%)")
    
    # Set a y-axis limit if provided
    if y_limit:
        plt.ylim(0, y_limit)
    
    # Add a legend at the specified x position
    plt.gcf().text(legend_pos_x, 0.5, legend, fontsize=10, va='center', ha='left', bbox=BBOX_STYLE)
    
    # Adjust layout to prevent overlap
    plt.tight_layout(rect=[0, 0, legend_pos_x, 1])

    plt.show()

def plot_territory_percentages(
        territories: List[Territory], 
        scale_y: bool = True, 
        color: str = PRIMARY_COLOR
        ) -> None:
    
    """
    Plots the percentages per purpose for each territory.

    Args:
        territories (List[Territory]): List with Territory objects.
        scale_y (bool): If True, y-axis has the same value for all plots;
                        if False, y-axis varies depending on plot data.
        color (str): color in hexadecimal format.

    Returns:
        None
    """

    # Filter out excluded purposes
    purposes = [f for f in PurposeStruct.PURPOSES if f != EXCLUDED_CATEGORY]
    
    # Get the full and abbreviated names for the territories
    full_names = [t.name for t in territories]
    abbreviations = [''.join(filter(str.isupper, t.name)) for t in territories]
    
    # Create the chart legend
    legend = _generate_legend(names=full_names, abbreviations=abbreviations)

    for purpose in purposes:
        # Get percentage for the current purpose
        percentages = [t.purposes[purpose]['porcentaje'] for t in territories]
        
        # Determine y-axis upper limit
        max_limit = (Territory.highest_percentage if scale_y else max(percentages)) + 5

        _plot_bar_chart(
            f"Porcentaje de {purpose} por Territorio", 
            abbreviations, percentages, legend, 0.65, color, max_limit
        )

def plot_average_purpose_percentages(
        territories: List[Territory], 
        color: str = PRIMARY_COLOR
    ) -> None:
    
    """
    Plot the average percentage for each purpose across all territories.

    Args:
        territories (List[Territory]): List with Territory objects.
        color (str): color in hexadecimal format.

    Returns:
        None
    """
    # Filter out excluded purposes
    percentages = [f for f in PurposeStruct.PURPOSES if f != EXCLUDED_CATEGORY]
    
    # Calculate the average percentage for each purpose
    average_percentages = {
        PurposeStruct.PURPOSES[f]: sum(t.purposes[f]['porcentaje'] for t in territories) / len(territories)
        for f in percentages
    }

    legend = _generate_legend(include_purposes=True)
    _plot_bar_chart(
        "Media de Porcentajes por Finalidad (Territorios)", 
        list(average_percentages.keys()), 
        list(average_percentages.values()), 
        legend, 0.55, color, max(average_percentages.values()) + 5
    )

def plot_piechart_percentages(
        territories: List[Territory], 
        pie_colors: List[str] = PIE_COLORS
    ) -> None:
    """
    Generate a pie chart showing the distribution of average percentages by purpose.
    
    Args:
        territories (List[Territory]): List with Territory objects.

    Returns:
        None
    """

    # Initialize dictionaries to store the sum of percentages and the count per purpose
    average_percentages = {name: 0.0 for name in PurposeStruct.PURPOSES if name != EXCLUDED_CATEGORY}
    divisor = {name: 0 for name in PurposeStruct.PURPOSES if name != EXCLUDED_CATEGORY}

    # Iterate through all territories to accumulate percentages and count occurrences per purpose
    for territory in territories:
        for purpose in PurposeStruct.PURPOSES:
            if purpose != EXCLUDED_CATEGORY:
                percentage = territory.purposes[purpose]['porcentaje']
                average_percentages[purpose] += percentage
                divisor[purpose] += 1

    # Calculate the average percentages for each purpose
    for purpose in average_percentages.keys():
        if divisor[purpose] > 0:  # Avoid division by zero
            average_percentages[purpose] /= divisor[purpose]

    # Create the figure and axes for the pie chart
    fig, ax = plt.subplots(figsize=FIG_SIZE)

    # Plot the pie chart
    wedges, texts, autotexts = ax.pie(
        average_percentages.values(), 
        autopct='%1.1f%%',      # Plot the pie chart
        startangle=90,  # Start the chart from a 90-degree angle
        colors=pie_colors[:len(average_percentages)]  # Use only the required colors
    )

    ax.axis('equal')    # Equalize axes to ensure the pie chart is circular

    plt.title("Distribución de Medias de Porcentajes por Finalidad")

    legend = [
        f"{purpose.replace('_', ' ').title()}"  # Replace underscores and capitalize words
        for purpose in average_percentages
    ]

    ax.legend(
        legend,
        title="Leyenda:", 
        alignment="left", 
        loc="center left",  # Position at the center-left of the chart
        bbox_to_anchor=(1, 0.5),  # Anchor the legend to the right of the chart
        ncol=1  # Display in one column
    )
    
    plt.tight_layout()      # Adjust layout to prevent overlap

    plt.show()

def plot_heatmap_territories(territories: List[Territory]) -> None:
    """
    Generate a heatmap that visualizes percentages by territory and purpose.
    
    Args:
        territories (List[Territory]): List with Territory objects.

    Returns:
        None
    """

    # Build a data dictionary: keys are territory abbreviations, values are lists of percentages by purpose
    data = {
        ''.join(filter(str.isupper, t.name)):  # Extract uppercase letters from the territory name
        [t.purposes[f]['porcentaje'] for f in PurposeStruct.PURPOSES if f != EXCLUDED_CATEGORY]
        for t in territories  # Iterate through all territories and store percentages
    }

    # Create a pandas DataFrame to structure the data (rows = purposes, columns = territories).
    df = pd.DataFrame(
        data,
        index=[PurposeStruct.PURPOSES[f] for f in PurposeStruct.PURPOSES if f != EXCLUDED_CATEGORY]
    )

    # Prepare full and abbreviated territory names.
    names = [t.name for t in territories]
    abbreviations = [''.join(filter(str.isupper, t.name)) for t in territories]

    plt.figure(figsize=(10, 8))

    sns.heatmap(df, annot=True, cmap=CMAP, fmt=".1f")   # Generate the heatmap using seaborn

    # Add title and axis labels
    plt.title("Heatmap de Porcentajes por Territorio y Finalidad")
    plt.xlabel("Territorios")
    plt.ylabel("Finalidades")

    legend = _generate_legend(names=names, abbreviations=abbreviations, include_purposes=True)

    # Add the legend to the figure in the specified position.
    plt.gcf().text(0.7, 0.5, legend, fontsize=10, va='center', ha='left', bbox=BBOX_STYLE)

    # Adjust layout to prevent overlap.
    plt.tight_layout(rect=[0, 0, 0.7, 1])

    plt.show()

def plot_interactive_age_gender(
        groups: List[AgeGender], 
        show_total: bool = False, 
        show_only_ages: bool = False
    ) -> None:
    """
    Generate an interactive bar chart of percentages by age and gender.

    Args:
        groups (List[AgeGroup]): List of age and gender groups.
        show_total (bool): If True, shows only the total; 
                           if False, shows Male and Female.
        show_only_ages (bool): If True, shows only age groups without the total;
                               if False, includes the total.
                            
    Returns:
        None
    """
    data = []

    # Gather the data for each age and gender group
    for group in groups:
        for purpose in PurposeStruct.PURPOSES:
            # Exclude purposes according to the EXCLUDED_CATEGORY constant
            if purpose == EXCLUDED_CATEGORY:
                continue
            
            percentage = group.purposes[purpose]['porcentaje']
            data.append({
                "Edad": group.age,
                "Sexo": group.gender,
                "Finalidad": PurposeStruct.PURPOSES[purpose], 
                "Porcentaje": percentage
            })

    df = pd.DataFrame(data)

    # Check if there is data to avoid errors
    if df.empty:
        print("No hay datos para graficar.")
        return

    # Define the desired order for age groups
    age_order = ["18 - 34", "35 - 54", "> 55", "Total"]
    
    # Convert the 'Age' column to categorical with a specific order
    df['Edad'] = pd.Categorical(df['Edad'], categories=age_order, ordered=True)

    # Define the specific order for purposes
    purpose_order = [
        "MEJORAR_CALIDAD_ENTORNOS_TURISTICOS",
        "MEJORAR_CONDICIONES_VIDA_CANARIAS",
        "MEJORAR_DESARROLLO_ECONOMICO_CANARIAS",
        "MEJORAR_PROTEGER_MEDIO_AMBIENTE_CANARIAS",
        "CUALQUIER_FIN_SERVICIO_CANARIAS"
    ]
    
    # Convert the 'Purpose' column to categorical with a specific order
    df['Finalidad'] = pd.Categorical(df['Finalidad'], categories=[PurposeStruct.PURPOSES[p] for p in purpose_order], ordered=True)

    # Filter the data according to the show_total parameter
    if show_total:
        df = df[df['Sexo'] == 'Total']
    else:
        df = df[df['Sexo'].isin(['Masculino', 'Femenino'])]

    # Filter the data according to the show_only_ages parameter
    if show_only_ages:
        df = df[df['Edad'] != "Total"]

    # Ensure that the data order is applied to the DataFrame
    df = df.sort_values(by=['Edad', 'Finalidad'])

    # Create the interactive bar chart
    fig = px.bar(
        df, 
        x='Edad', 
        y='Porcentaje', 
        color='Finalidad', 
        barmode='group', 
        facet_col='Sexo' if not show_total else None,  # Remove facet_col if show_total is True
        title="Porcentajes por Edad, Sexo y Finalidad",
        labels={"Porcentaje": "Porcentaje (%)", "Edad": "Grupos de Edad"},
        pattern_shape='Finalidad',  # Add patterns based on the purpose
        pattern_shape_sequence=["/", "+", "\\", "x", "."]  # Different patterns/textures
    )
    
    # Adjust layout to prevent overlap.
    fig.update_layout(
        xaxis_title="Grupos de Edad",
        yaxis_title="Porcentaje (%)",
        legend_title="Finalidad",
        height=600, 
        template="plotly_white"
    )
    
    fig.show()

def plot_interactive_map(territories: List[Territory]) -> None:
    """
    Generate an interactive map of the Canary Islands excluding the 'Canarias' territory.
    
    Args:
        territories (List[Territory]): List with Territory objects.

    Returns:
        None
    """

    # Coordinates of the Canary Islands
    coordinates = {
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

    # Prepare the data to be displayed
    data = [
        {
            "Isla": t.name,
            "Lat": coordinates[t.name][0],
            "Lon": coordinates[t.name][1],
            **{
                PurposeStruct.PURPOSES[p]: f"{t.purposes[p]['porcentaje']}%"
                for p in PurposeStruct.PURPOSES if p != EXCLUDED_CATEGORY
            }
        }
        for t in territories if t.name != 'Canarias'
    ]

    df = pd.DataFrame(data)

    if df.empty:
        print("No hay datos para graficar el mapa.")
        return

    # Create the interactive map
    fig = px.scatter_mapbox(
        df,
        lat='Lat',
        lon='Lon',
        title="Mapa Interactivo de las Islas Canarias",
        size_max=15,
        zoom=6,
        mapbox_style='open-street-map'
    )

    # Set hovertemplate
    fig.update_traces(
        marker=dict(size=14),
        hovertemplate='<b>%{hovertext}</b><br>%{customdata}<extra></extra>',
        hovertext=df['Isla'],
        customdata=df.drop(columns=['Isla', 'Lat', 'Lon']).apply(
            lambda row: '<br>'.join(
                [f"{PurposeStruct.PURPOSES[p]}={row[PurposeStruct.PURPOSES[p]]}" 
                 for p in PurposeStruct.PURPOSES if p != EXCLUDED_CATEGORY]
            ),
            axis=1
        )
    )

    legend = _generate_legend(include_purposes=True)
    fig.add_annotation(
        text=legend.replace('\n', '<br>'),
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

    fig.show()
