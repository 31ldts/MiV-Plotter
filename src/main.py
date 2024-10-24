from visualizations import *
from data_loader import *

territories = read_csv(path='data/territorios.csv', entity_class=Territory)
age_gender = read_csv(path='data/edad_sexo.csv', entity_class=AgeGender)

plot_territory_percentages(territories)
plot_territory_percentages(territories=territories, scale_y=False)
plot_average_purpose_percentages(territories)
plot_piechart_percentages(territories=territories)
plot_heatmap_territories(territories=territories)

plot_interactive_age_gender(groups=age_gender)
plot_interactive_age_gender(groups=age_gender, show_total=True, show_only_ages=True)

plot_interactive_map(territories=territories)