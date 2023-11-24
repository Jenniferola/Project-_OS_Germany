# Import packages
from dash import Dash, html, dash_table, dcc
import pandas as pd
import plotly.express as px
import dash_bootstrap_components as dbc

punkt1 = "1. Tysklands bästa prestationer"
punkt2 = "2. Tyskland utifrån tidsperioder"
punkt3 = "3. 4 sporter vi tittat närmare: Athletics, Canoeing, Tug of war, Rythmetic (alla länder)"
punkt4 = "4. Framgångsfaktorer för OS vinnare (alla länder): "


#Function to do title question thingymojingy
def question_title(title):
    return dbc.Row([html.H2(f"{title}")], class_name="test-row-fill")

# Load the data
os_data = pd.read_csv('data/athlete_events.csv')

# Filter for German athletes
os_data_germany = os_data.query("NOC == 'GER' or NOC == 'FRG' or NOC == 'SAA' or NOC == 'GDR'")

# Filter out rows without medal information
data_medals_germany = os_data_germany.dropna(subset=['Medal'])

# For team events, count the event as a single medal instance
# Here, we drop duplicates considering 'Year', 'Event', and 'Medal' for unique medals per sport
unique_medals_per_sport = data_medals_germany.drop_duplicates(subset=['Year', 'Event', 'Medal'])

# For aggregating medals per year, do not include 'Name' in duplicates removal
unique_medals_per_year = data_medals_germany.drop_duplicates(subset=['Year', 'Event', 'Medal'])

# For counting individual athlete medals, include 'Name' in duplicates removal
unique_medals_per_athlete = data_medals_germany.drop_duplicates(subset=['Year', 'Event', 'Medal', 'Name'])

# Count medals in top 10 sports using the unique_medals_per_sport DataFrame
sport_data_medals = unique_medals_per_sport["Sport"].value_counts().head(10)
df_data_medals = pd.DataFrame(sport_data_medals).reset_index()
df_data_medals.columns = ['Sport', 'count']

# Medals per year data, considering unique medals only
medals_per_year = unique_medals_per_year.groupby("Year")['Medal'].count().reset_index(name="Medals")
medals_per_year_sorted = medals_per_year.sort_values("Medals", ascending=False)

# Average age data germany
# Filter out rows without age data
germany_age_data = os_data_germany.dropna(subset=['Age'])

# Calculate average age per year
avg_age_per_year = germany_age_data.groupby('Year')['Age'].mean().reset_index()

# Count medals for each athlete, considering unique medals only
medal_counts_athlete = unique_medals_per_athlete['Name'].value_counts().head(10)

# Filtering sport-specific datasets (with medals)
os_data_modified = os_data[os_data['Medal'].notna()]

os_data_athletics = os_data_modified.query("Sport == 'Athletics'")
os_data_canoeing = os_data_modified.query("Sport == 'Canoeing'")
os_data_tug_of_war = os_data_modified.query("Sport == 'Tug-Of-War'")
os_data_rhythmic_gymnastic = os_data_modified.query("Sport == 'Rhythmic Gymnastics'")

#Athletics
medal_count_athletics = os_data_athletics.groupby("NOC")["Medal"].count().reset_index()
top_10_athletics = medal_count_athletics.sort_values(by="Medal", ascending=False).head(10)
age_distribution_athletics = os_data[os_data['Sport'] == 'Athletics']

#Plot for canoeing
medal_count_canoeing = os_data_canoeing.groupby("NOC")["Medal"].count().reset_index()
top_10_canoeing = medal_count_canoeing.sort_values(by="Medal", ascending=False).head(10)
age_distribution_canoeing = os_data[os_data['Sport'] == 'Canoeing']

#Plot for tug of war
medal_count_tug_of_war = os_data_tug_of_war.groupby("NOC")["Medal"].count().reset_index()
top_10_tug_of_war = medal_count_tug_of_war.sort_values(by="Medal", ascending=False).head(10)
age_distribution_tug_of_war = os_data[os_data['Sport'] == 'Tug-Of-War']

#Plot for rythmic gymnastic
medal_count_rhythmic_gymnastic = os_data_rhythmic_gymnastic.groupby("NOC")["Medal"].count().reset_index()
top_10_rhythmic_gymnastic= medal_count_rhythmic_gymnastic.sort_values(by="Medal", ascending=False).head(10)
age_distribution_rhythmic_gymnastic = os_data[os_data['Sport'] == 'Rhythmic Gymnastics']

#Data for top 10 medals won of all time
medalists = os_data.dropna(subset=['Medal'])
top_10_medalists = medalists['Name'].value_counts().head(10)
#Data for avrage height weight and age for medal winners
avrage_age = medalists['Age'].mean()
avrage_weight = medalists['Weight'].mean()
avrage_height = medalists['Height'].mean()

# Prep data
avrage_metrics = pd.DataFrame({
    'Metric': ['Average Age', 'Average Weight', 'Average Height'],
    'Value': [avrage_age, avrage_weight, avrage_height]
})

#Skapade figurer:
#Row 1
# Figure one - The sports where Germany performs the best
top_10_ger_sport_fig = px.bar(df_data_medals, x='Sport', y="count", 
             template='plotly_white',
             labels={"Sport": "Olympic Sport", "count": "Number of Medals"},
             color="count")
top_10_ger_sport_fig.update_layout(font_family="Rockwell", font_size=15)

#Figure two - top 10 athletes
top_10_athletes_all_time_fig = px.bar(top_10_medalists, x=top_10_medalists.index, y=top_10_medalists.values, 
             template="plotly_white",                         
             labels={'y': 'Number of Medals', 'index': 'Athlete'},
             color="count")
top_10_athletes_all_time_fig.update_layout(font_family="Rockwell",font_size=15)

#Row 2
#Figure three
medals_per_year_germany_fig = px.bar(medals_per_year_sorted, y="Medals", x="Year", 
             template='plotly_white',
             labels={"Sport": "Olympic Sport", "Medals": "Number of Medals"},
             color="Medals")
medals_per_year_germany_fig.update_layout(font_family="Rockwell", font_size=15)

#Figure three - Top 10 medal winners in all of german history
top_10_athletes_germany_fig = px.bar(medal_counts_athlete, x=medal_counts_athlete.values, y=medal_counts_athlete.index, 
             template='plotly_white',
             labels={'x': 'Number of Medals'},
             color="count")
top_10_athletes_germany_fig.update_layout(yaxis={'categoryorder':'total ascending'},font_family="Rockwell", font_size=15, bargap=0.4)

#Row 3
#Figure four - Avrage age per year for germany
avg_age_germany_fig = px.bar(avg_age_per_year, x='Year', y='Age',
                             template='plotly_white',
                             labels={'Age': 'Average Age', 'Year': 'Olympic Year'},color='Age')

avg_age_germany_fig.update_layout(font_family="Rockwell", font_size=15)

#Figure five
top_10_countries_athletics_fig = px.bar(top_10_athletics, x="NOC", y="Medal",
             template='plotly_white',
             labels={"NOC": "Countries", "Medal": "Number of Medals"},
             color="NOC")

top_10_countries_athletics_fig.update_layout(font_family="Rockwell", font_size=15)

#Row 4
#Figure six
age_distribution_athletics_fig = px.histogram(age_distribution_athletics, x='Age',
            template='plotly_white',
            labels={"Age": "Ages", "Count": "Medals"},
            color="Age")
age_distribution_athletics_fig.update_layout(font_family="Rockwell",font_size=15)

#Figure seven
top_10_canoeing_fig = px.bar(top_10_canoeing, x="NOC", y="Medal",
             template='plotly_white',
             labels={"NOC": "Countries", "Medal": "Number of Medals"},
             color="NOC")
top_10_canoeing_fig.update_layout(font_family="Rockwell", font_size=15)

#Figure eight
age_distribution_canoeing_fig = px.histogram(age_distribution_canoeing, x="Age",
            template="plotly_white",
            labels={"count": "Number of Medals", "Age": "Ages"},
            color="Age")
age_distribution_canoeing_fig.update_layout(font_family="Rockwell",font_size=15)
#Row5
#Figure nine
top_10_tug_of_war_fig = px.bar(top_10_tug_of_war, x="NOC", y="Medal",
             template='plotly_white',
             labels={"NOC": "Countries", "Medal": "Number of Medals"},
             color="NOC")
top_10_tug_of_war_fig.update_layout(font_family="Rockwell", font_size=15)
#Figure ten
age_distribution_tug_of_war_fig = px.histogram(age_distribution_tug_of_war, x="Age",
            nbins=30,  #Fixar så att barsen inte ligger på varandra
            template="plotly_white",
            color="Age")
age_distribution_tug_of_war_fig.update_layout(font_family="Rockwell",font_size=15)
#Row 6
#Figure eleven
top_10_rhythmic_gymnastic_fig= px.bar(top_10_rhythmic_gymnastic, x="NOC", y="Medal",
             template='plotly_white',
             labels={"NOC": "Countries", "Medal": "Number of Medals"},
             color="NOC")
top_10_rhythmic_gymnastic_fig.update_layout(font_family="Rockwell", font_size=15)

#Figure twelve
age_distribution_rhythmic_gymnastic_fig = px.histogram(age_distribution_rhythmic_gymnastic, x="Age",
            template="plotly_white",
            labels={"count": "Number of Medals", "Age": "Ages"},
            color="Age")
age_distribution_rhythmic_gymnastic_fig.update_layout(xaxis_title="Age", yaxis_title="Number of Medals",font_family="Rockwell",font_size=15)

#Row 7
#Figure fourteen
avrage_medal_winner = px.bar(avrage_metrics, x='Metric', y='Value',
             labels={'Value': 'Average (Age in years, Weight in kg, Height in cm)'},
             color="Value")
avrage_medal_winner.update_layout(font_family="Rockwell",font_size=15)

# Initialize the app
app = Dash(__name__)

# App layout
app.layout = html.Div([
    #Header
    html.Header([html.H1("OS dataanalys - grupp Tyskland")], id="header"),
    #Uppgift 1'plots
    html.Main([
        dbc.Row([
            html.H3("Våra frågeställningar:"),
            html.Ul(children=[html.Li(punkt1),html.Li(punkt2),html.Li(punkt3),html.Li(punkt4)])
            ], id="info-box"),
        question_title("Tysklands bästa prestationer"),
        dbc.Row([
            dbc.Col([
                html.H2("Topp 10 sporter"),
                dcc.Graph(figure=top_10_ger_sport_fig)], class_name="graph-box"),
                #Second box first row
            dbc.Col([
                html.H2("Topp 10 atleter "),
                dcc.Graph(figure=top_10_athletes_germany_fig)], class_name="graph-box"),        
        ], class_name="rower"),

        question_title("Tyskland utifrån tidsperioder"),
        dbc.Row([
            dbc.Col([
                html.H2("Medaljer per år"),
                dcc.Graph(figure=medals_per_year_germany_fig)], class_name="graph-box"),
            dbc.Col([
                html.H2("Medelåldern för atleter genom åren"),
                dcc.Graph(figure=avg_age_germany_fig)], class_name="graph-box")
        ], class_name="rower"),

        question_title("Fyra sporter vi tittat närmare: Athletics, Canoeing, Tug of war, Rythmetic (alla länder)"), 
        dbc.Row([question_title("Friidrott")], class_name="rower"),
        dbc.Row([
            dbc.Col([
                html.H2("Topp 10 länder i friidrott"),
                dcc.Graph(figure=top_10_countries_athletics_fig)], class_name="graph-box"), 
            dbc.Col([
                html.H2("Åldersfördelning friidrott"),
                dcc.Graph(figure=age_distribution_athletics_fig)], class_name="graph-box")
        ], class_name="rower"),

        question_title("Kanot"),
        dbc.Row([
            dbc.Col([
                html.H2("Topp 10 länder i Kanot"),
                dcc.Graph(figure=top_10_canoeing_fig)], class_name="graph-box"),
            dbc.Col([
                html.H2("Åldersfördelning kanot"),
                dcc.Graph(figure=age_distribution_canoeing_fig)], class_name="graph-box")
        ], class_name="rower"),

        question_title("Dragkamp"),
        dbc.Row([
            dbc.Col([
                html.H2("Topp 10 länder dragkamp"),
                dcc.Graph(figure=top_10_tug_of_war_fig)], class_name="graph-box"),
            dbc.Col([
                html.H2("Åldersfördelning dragkamp av alla länder"),
                dcc.Graph(figure=age_distribution_tug_of_war_fig)], class_name="graph-box")
        ], class_name="rower"),

        question_title("Rytmisk gymnastik"),
        dbc.Row([
            dbc.Col([
                html.H2("Topp 10 länder rythmisk gymnastik"),
                dcc.Graph(figure=top_10_rhythmic_gymnastic_fig)], class_name="graph-box"),
            dbc.Col([
                html.H2("Åldersfördelning rythmisk gymnastik av alla länder"),
                dcc.Graph(figure=age_distribution_rhythmic_gymnastic_fig)], class_name="graph-box")
        ], class_name="rower"),

        question_title("Framgångsfaktorer för OS vinnare (alla länder)"),
        dbc.Row([
            dbc.Col([
                html.H2("Världens bästa 10 atleter"),
                dcc.Graph(figure=top_10_athletes_all_time_fig)], class_name="graph-box"),
            dbc.Col([
                html.H2("Medelålder, -vikt och -längd för medaljvinnare"),
                dcc.Graph(figure=avrage_medal_winner)], class_name="graph-box")
        ], class_name="rower"),

    ])

])

# Run the app
if __name__ == '__main__':
    app.run(debug=True)