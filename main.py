import json
import plotly.express as px
import streamlit as st
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import folium
from folium import plugins
from wordcloud import WordCloud

st.set_page_config(layout="wide")

st.title('Analyse des Crimes en France')

st.header('À propos de ce projet')

st.write("""
Ce projet vise à analyser les données sur les crimes enregistrés en France. 
Il s'appuie sur un ensemble de données provenant de data.gouv.fr, 
et offre une vue d'ensemble des tendances et des schémas dans les données criminelles.
""")

st.subheader('Méthodologie')
st.write("""
Les données sont filtrées et traitées pour fournir des visualisations interactives 
et offrir des information sur les crimes dans différentes régions, 
leurs évolutions au fil du temps.

""")

st.subheader('Problématique')
st.write("""
En france, la criminalité un grand sujet de discussion. C'est pour ce la que nous allons chercher les deparetment les plus dangerueux mais aussi ceux les plus safe. Nous allons essayer de voir aussi si les differentes actualités en France ont eux des impacts sur la criminalité.

""")

st.write("""

""")
st.write("""

""")
st.write("""

""")
st.write("""

""")
st.write("""

""")
st.write("""

""")
st.write("""

""")
st.write("""

""")
st.write("""

""")

with st.sidebar:
    st.image("https://www.efrei.fr/wp-content/uploads/2022/01/LOGO_EFREI-PRINT_EFREI-WEB.png", width=100)
    st.subheader('Mes informations :')
    st.write('🔗 [LinkedIn](https://www.linkedin.com/in/sam-pondevie-b1219423b/)')
    st.write('📧 Email: sam.pondevie@efrei.net')
    st.write('📞 Numéro: 06 51 08 42 14')
    st.write(
        '📄 [Lien vers les données](https://www.data.gouv.fr/fr/datasets/bases-statistiques-communale-et-departementale-de-la-delinquance-enregistree-par-la-police-et-la-gendarmerie-nationales/)')

    data = pd.read_csv('donnee-dep-data.gouv-2022-geographie2023-produit-le2023-07-17.csv', delimiter=";")
    crime = st.selectbox('Select Crime:', data['classe'].unique())
    year = st.slider('Select Year:', min_value=data['annee'].min(), max_value=data['annee'].max(),
                     value=data['annee'].max())
    department = st.selectbox('Select Department:', data['Code.département'].unique())
    pass

filtered_data = data[(data['classe'] == crime) & (data['annee'] == year) & (data['Code.département'] == department)]
st.write(filtered_data)


def plot_time_series(data):
        st.subheader('Évolution des délits au fil du temps')
        time_series_data = data.groupby(['annee', 'classe'])['faits'].sum().unstack().fillna(0)
        fig = time_series_data.plot(kind='line', figsize=(10, 6))
        st.pyplot(fig.figure)


def plot_crime_per_selected_department(data, department):
        st.subheader(f'Nombre de crimes pour le département {department}')
        selected_department_data = data[data['Code.département'] == department]
        crime_data = selected_department_data.groupby('annee')['faits'].sum()
        fig = crime_data.plot(kind='bar', figsize=(10, 6))
        plt.xlabel('Année')
        plt.ylabel('Nombre de crimes')
        plt.title(f'Nombre de crimes par année pour le département {department}')
        st.pyplot(fig.figure)


plot_crime_per_selected_department(data, department)


def plot_crime_per_selected_department_crime(data, department, crime):
        st.subheader(f'Nombre de {crime} pour le département {department}')

        selected_data = data[(data['Code.département'] == department) & (data['classe'] == crime)]

        crime_data = selected_data.groupby('annee')['faits'].sum()

        fig, ax = plt.subplots(figsize=(10, 6))
        crime_data.plot(kind='bar', ax=ax)

        plt.xlabel('Année')
        plt.ylabel('Nombre de crimes')
        plt.title(f'Nombre de {crime} par année pour le département {department}')

        st.pyplot(fig.figure)


plot_crime_per_selected_department_crime(data, department, crime)


def plot_top_10_departments_by_crime(data, year):
        st.subheader(f'Les 10 départements avec le plus grand nombre de faits pour l\'année {year}')
        year_data = data[data['annee'] == year]
        top_10 = year_data.groupby('Code.département')['faits'].sum().nlargest(10).reset_index()

        fig = sns.barplot(x='Code.département', y='faits', data=top_10)

        x_labels = top_10['Code.département']
        fig.set_xticks(range(len(x_labels)))
        fig.set_xticklabels(x_labels, rotation=90)

        fig.set_xlabel('Département')
        fig.set_ylabel('Nombre de faits')
        st.pyplot(fig.figure)


plot_top_10_departments_by_crime(data, year)


def plot_top_10_crime_rates(data, year):
        st.subheader(f'Les 10 départements avec les taux de crimes les plus élevés pour l\'année {year}')
        year_data = data[data['annee'] == year]
        year_data['tauxpourmille'] = year_data['tauxpourmille'].str.replace(',', '.').apply(
            lambda x: round(float(x), 2))
        top_10 = year_data.groupby('Code.département')['tauxpourmille'].sum().nlargest(10).reset_index()
        st.write(top_10)


def plot_top_10_crime_rates_reverse(data, year):
        st.subheader(f'Les 10 départements avec les taux de crimes les plus faible pour l\'année {year}')
        year_data = data[data['annee'] == year]
        year_data['tauxpourmille'] = year_data['tauxpourmille'].str.replace(',', '.').apply(
            lambda x: round(float(x), 2))
        top_10_reverse = year_data.groupby('Code.département')['tauxpourmille'].sum().nsmallest(10).reset_index()
        st.write(top_10_reverse)


option = st.radio('Choisissez le type de données', ('les plus dangereux', 'les moins dangereux'))
plot_container = st.empty()
if option == 'les plus dangereux':
    plot_top_10_crime_rates(data, year)
elif option == 'les moins dangereux':
    plot_container.empty()
    plot_top_10_crime_rates_reverse(data, year)


def plot_total_crime_per_class_department(data, year, department):
    st.subheader(f'Comparaison du nombre total de crimes par classe pour {department} en {year}')

    filtered_data = data[(data['Code.département'] == department) & (data['annee'] == year)]

    grouped_data = filtered_data.groupby('classe')['faits'].sum()

    fig, ax = plt.subplots(figsize=(10, 6))
    grouped_data.plot(kind='pie', ax=ax, autopct='%1.1f%%', startangle=140, cmap='viridis')
    plt.ylabel('')  # Enlever le label y
    plt.title(f'Nombre total de crimes par classe pour {department} en {year}')
    st.pyplot(fig)


def plot_total_crime_by_class(data):
    st.subheader('Comparaison du nombre total de crimes par classe de crime')
    grouped_data = data.groupby('classe')['faits'].sum()
    fig, ax = plt.subplots(figsize=(10, 6))
    grouped_data.plot(kind='pie', ax=ax, autopct='%1.1f%%', startangle=140, cmap='viridis')
    plt.ylabel('')  # Enlever le label y
    plt.title('Nombre total de crimes par classe de crime')
    st.pyplot(fig)

plot_total_crime_per_class_department(data, year, department)
plot_total_crime_by_class(data)

top_crimes = data.groupby('classe')['faits'].sum().reset_index()
top_crimes.columns = ['Crime', 'Nombre']

wordcloud = WordCloud(width=800, height=400, background_color='white', colormap='viridis',
                          min_font_size=10, max_words=100).generate_from_frequencies(
        top_crimes.set_index('Crime')['Nombre'])

st.subheader('Nuage de mots des crimes les plus fréquents')
fig, ax = plt.subplots(figsize=(10, 6))
ax.imshow(wordcloud, interpolation='bilinear')
ax.axis("off")
st.pyplot(fig)


def departement_max_incidents(data, year):
        year_data = data[data['annee'] == year]

        grouped_data = year_data.groupby(['annee', 'classe', 'Code.département'])['faits'].sum().reset_index()

        max_incidents_regions = grouped_data.groupby(['classe'])['faits'].idxmax()

        max_incidents_data = grouped_data.loc[max_incidents_regions]

        return max_incidents_data


st.title('Le département avec le plus d\'incidents pour chaque type de crime')

max_incidents_data = departement_max_incidents(data, year)

st.dataframe(max_incidents_data)


def departement_min_incidents(data, year):
        year_data = data[data['annee'] == year]

        grouped_data = year_data.groupby(['annee', 'classe', 'Code.département'])['faits'].sum().reset_index()

        min_incidents_departements = grouped_data.groupby(['classe'])['faits'].idxmin()

        min_incidents_data = grouped_data.loc[min_incidents_departements]

        return min_incidents_data


st.title('Le département avec le moins d\'incidents pour chaque type de crime')

min_incidents_data = departement_min_incidents(data, year)

st.dataframe(min_incidents_data)

st.write("## Nous allons maintenant nous intéresser à la répartition des faits de délinquance par département")
with open('departements.geojson', 'r') as geojson_file:
        geojson_data = json.load(geojson_file)



filtered_df = data[data['annee'] == year]

total_by_dept = filtered_df.groupby('Code.département')['faits'].sum().reset_index()
total_by_dept.rename(columns={'faits': 'TotalFaits'}, inplace=True)


fig2 = px.choropleth_mapbox(total_by_dept,
                                geojson=geojson_data,
                                locations="Code.département",
                                featureidkey="properties.code",
                                color="TotalFaits",
                                title=f"Répartition des Crimes et Délits en France en {year}",
                                mapbox_style="open-street-map",
                                center={"lat": 46.6061, "lon": 1.875277},
                                zoom=5.0,
                                color_continuous_scale=["blue", "red"])

fig2.update_geos(projection_type="mercator", visible=False)
fig2.update_layout(margin={"r": 0, "t": 0, "l": 0, "b": 0})
st.plotly_chart(fig2)
pass
