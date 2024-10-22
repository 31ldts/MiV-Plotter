from visualizations import *
from data_loader import *

territorios = read_csv(path='data/territorios.csv', entity_class=Territory)
edad_sexo = read_csv(path='data/edad_sexo.csv', entity_class=AgeGender)

plot_territory_percentages(territorios)
plot_territory_percentages(territories=territorios, scale_y=False)
plot_average_purpose_percentages(territorios)
plot_piechart_percentages(territories=territorios)
plot_heatmap_territories(territories=territorios)

plot_interactive_age_gender(groups=edad_sexo)
plot_interactive_age_gender(groups=edad_sexo, show_total=True, show_only_ages=True)

plot_interactive_map(territories=territorios)