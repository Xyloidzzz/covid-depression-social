import re
from dash import Dash, dcc, html, Input, Output
import plotly.graph_objects as go
import plotly.express as px
import pandas as pd
from scipy.stats import pearsonr

cdcAnxietyPath = "./Correlations/data/cdc/seperate-anxiety/time-series/"
cdcDepressionPath = "./Correlations/data/cdc/seperate-depression/time-series/"

googleTrendsData = pd.read_csv(
    "./Correlations/data/google/google_trends_CLEAN.csv")

names = ["National Estimate", "By Age", "By Sex",
         "By Race", "By Education", "By State"]

cdcAnxietyUS = pd.read_csv(cdcAnxietyPath + "CDCAnxiety_" +
                           re.sub(r"\s+", "", names[0])+"_TIMESERIES.csv")
cdcAnxietyAge = pd.read_csv(cdcAnxietyPath + "CDCAnxiety_" +
                            re.sub(r"\s+", "", names[1])+"_TIMESERIES.csv").drop(columns=["week"])
cdcAnxietySex = pd.read_csv(cdcAnxietyPath + "CDCAnxiety_" +
                            re.sub(r"\s+", "", names[2])+"_TIMESERIES.csv").drop(columns=["week"])
cdcAnxietyRace = pd.read_csv(cdcAnxietyPath + "CDCAnxiety_" +
                             re.sub(r"\s+", "", names[3])+"_TIMESERIES.csv").drop(columns=["week"])
cdcAnxietyEducation = pd.read_csv(cdcAnxietyPath + "CDCAnxiety_" +
                                  re.sub(r"\s+", "", names[4])+"_TIMESERIES.csv").drop(columns=["week"])
cdcAnxietyState = pd.read_csv(cdcAnxietyPath + "CDCAnxiety_" +
                              re.sub(r"\s+", "", names[5])+"_TIMESERIES.csv").drop(columns=["week"])

cdcDepressionUS = pd.read_csv(cdcDepressionPath + "CDCDepression_" +
                              re.sub(r"\s+", "", names[0])+"_TIMESERIES.csv")
cdcDepressionAge = pd.read_csv(cdcDepressionPath + "CDCDepression_" +
                               re.sub(r"\s+", "", names[1])+"_TIMESERIES.csv").drop(columns=["week"])
cdcDepressionSex = pd.read_csv(cdcDepressionPath + "CDCDepression_" +
                               re.sub(r"\s+", "", names[2])+"_TIMESERIES.csv").drop(columns=["week"])
cdcDepressionRace = pd.read_csv(cdcDepressionPath + "CDCDepression_" +
                                re.sub(r"\s+", "", names[3])+"_TIMESERIES.csv").drop(columns=["week"])
cdcDepressionEducation = pd.read_csv(cdcDepressionPath + "CDCDepression_" +
                                     re.sub(r"\s+", "", names[4])+"_TIMESERIES.csv").drop(columns=["week"])
cdcDepressionState = pd.read_csv(cdcDepressionPath + "CDCDepression_" +
                                 re.sub(r"\s+", "", names[5])+"_TIMESERIES.csv").drop(columns=["week"])

# match googleTrendsData['week'] to cdcAnxietyUS['week'] then delete the rows in googleTrendsData that don't match
googleTrendsData = googleTrendsData[googleTrendsData['week'].isin(
    cdcAnxietyUS['week'])]


def fixWeek(week):
    date = week.split("/")
    return date[2] + "-" + date[0] + "-" + date[1]  # format: YYYY-MM-DD


# fix the week column
googleTrendsData['week'] = googleTrendsData['week'].apply(fixWeek)


# turn data from string to float
for col in googleTrendsData.columns:
    if col != 'week':
        googleTrendsData[col] = googleTrendsData[col].astype(float)

cdcAnxietyUS['United States'] = cdcAnxietyUS['United States'].astype(float)
cdcAnxietyAge = cdcAnxietyAge.astype(float)
cdcAnxietySex = cdcAnxietySex.astype(float)
cdcAnxietyRace = cdcAnxietyRace.astype(float)
cdcAnxietyEducation = cdcAnxietyEducation.astype(float)
cdcAnxietyState = cdcAnxietyState.astype(float)

cdcDepressionUS['United States'] = cdcDepressionUS['United States'].astype(
    float)
cdcDepressionAge = cdcDepressionAge.astype(float)
cdcDepressionSex = cdcDepressionSex.astype(float)
cdcDepressionRace = cdcDepressionRace.astype(float)
cdcDepressionEducation = cdcDepressionEducation.astype(float)
cdcDepressionState = cdcDepressionState.astype(float)


# normalize data
for col in googleTrendsData.columns:
    if col != 'week':
        googleTrendsData[col] = googleTrendsData[col] / \
            googleTrendsData[col].max()

cdcAnxietyUS['United States'] = cdcAnxietyUS['United States'] / \
    cdcAnxietyUS['United States'].max()
cdcAnxietyAge = cdcAnxietyAge / cdcAnxietyAge.max()
cdcAnxietySex = cdcAnxietySex / cdcAnxietySex.max()
cdcAnxietyRace = cdcAnxietyRace / cdcAnxietyRace.max()
cdcAnxietyEducation = cdcAnxietyEducation / cdcAnxietyEducation.max()
cdcAnxietyState = cdcAnxietyState / cdcAnxietyState.max()

cdcDepressionUS['United States'] = cdcDepressionUS['United States'] / \
    cdcDepressionUS['United States'].max()
cdcDepressionAge = cdcDepressionAge / cdcDepressionAge.max()
cdcDepressionSex = cdcDepressionSex / cdcDepressionSex.max()
cdcDepressionRace = cdcDepressionRace / cdcDepressionRace.max()
cdcDepressionEducation = cdcDepressionEducation / cdcDepressionEducation.max()
cdcDepressionState = cdcDepressionState / cdcDepressionState.max()

googleTrendsData.reset_index(inplace=True)
googleTrendsData = googleTrendsData.drop(googleTrendsData.columns[0], axis=1)

#############################################START OF DASH############################################
app = Dash(__name__)
server = app.server
app.title = "Group 2: CDC Anxiety and Depression"

app.layout = html.Div([
    html.H1('Covid Anxiety & Depression Analysis'),
    html.H2('Values of Interest / Time'),
    dcc.Graph(id="time-series-chart",
              style={'height': '650px', 'width': '100%'}),
    html.P("Select Graph:"),
    dcc.Dropdown(
        id="ticker",
        options=["CDC Anxiety US",
                 "CDC Anxiety Age",
                 "CDC Anxiety Sex",
                 "CDC Anxiety Race",
                 "CDC Anxiety Education",
                 "CDC Anxiety States",
                 "CDC Depression US",
                 "CDC Depression Age",
                 "CDC Depression Sex",
                 "CDC Depression Race",
                 "CDC Depression Education",
                 "CDC Depression States",
                 "Google Trends 'covid'",
                 "Google Trends 'anxiety'",
                 "Google Trends 'depression'", ],
        value="CDC Anxiety US",
        clearable=False,
    ),
    html.H2(
        'Pearson Correlation, P-Value, and Trend Scatter Plot Between Custom Variables'),
    html.P(id="correlation-info",
           style={'fontSize': '25px', 'font-weight': 'bold'}),
    dcc.Graph(id="correlation-chart",
              style={'height': '650px', 'width': '100%'}),
    html.P("Select Graph:"),
    html.Div([
        dcc.Dropdown(
            id="correlation-ticker1",
            options=["CDC Anxiety US",
                     "CDC Anxiety Age (18 - 29 years)",
                     "CDC Anxiety Age (30 - 39 years",
                     "CDC Anxiety Age (40 - 49 years)",
                     "CDC Anxiety Age (50 - 59 years)",
                     "CDC Anxiety Age (60 - 69 years)",
                     "CDC Anxiety Age (70 - 79 years)",
                     "CDC Anxiety Age (80+ years)",
                     "CDC Anxiety Sex (Male)",
                     "CDC Anxiety Sex (Female)",
                     "CDC Anxiety Race (Hispanic or Latino)",
                     "CDC Anxiety Race (Non-Hispanic White, single race)",
                     "CDC Anxiety Race (Non-Hispanic Black, single race)",
                     "CDC Anxiety Race (Non-Hispanic Asian, single race)",
                     "CDC Anxiety Race (Non-Hispanic, other races and multiple races)",
                     "CDC Anxiety Education (Less than a high school diploma)",
                     "CDC Anxiety Education (High school diploma or GED)",
                     "CDC Anxiety Education (Some college/Associate's degree)",
                     "CDC Anxiety Education (Bachelor's degree or higher)",
                     "CDC Depression US",
                     "CDC Depression Age (18 - 29 years)",
                     "CDC Depression Age (30 - 39 years",
                     "CDC Depression Age (40 - 49 years)",
                     "CDC Depression Age (50 - 59 years)",
                     "CDC Depression Age (60 - 69 years)",
                     "CDC Depression Age (70 - 79 years)",
                     "CDC Depression Age (80+ years)",
                     "CDC Depression Sex (Male)",
                     "CDC Depression Sex (Female)",
                     "CDC Depression Race (Hispanic or Latino)",
                     "CDC Depression Race (Non-Hispanic White, single race)",
                     "CDC Depression Race (Non-Hispanic Black, single race)",
                     "CDC Depression Race (Non-Hispanic Asian, single race)",
                     "CDC Depression Race (Non-Hispanic, other races and multiple races)",
                     "CDC Depression Education (Less than a high school diploma)",
                     "CDC Depression Education (High school diploma or GED)",
                     "CDC Depression Education (Some college/Associate's degree)",
                     "CDC Depression Education (Bachelor's degree or higher)",
                     "Google Trends 'covid'",
                     "Google Trends 'body aches'",
                     "Google Trends 'sore throat'",
                     "Google Trends 'cough'",
                     "Google Trends 'anxiety'",
                     "Google Trends 'panic attacks'",
                     "Google Trends 'hyperventilation'",
                     "Google Trends 'loss of focus'",
                     "Google Trends 'depression'",
                     "Google Trends 'sadness'",
                     "Google Trends 'fatigue'",
                     "Google Trends 'suicidal thoughts'", ],
            value="CDC Anxiety US",
            clearable=False,
            style={'width': '100%', 'padding-right': '10px'}
        ),
        html.P("VS"),
        dcc.Dropdown(
            id="correlation-ticker2",
            options=["CDC Anxiety US",
                     "CDC Anxiety Age (18 - 29 years)",
                     "CDC Anxiety Age (30 - 39 years",
                     "CDC Anxiety Age (40 - 49 years)",
                     "CDC Anxiety Age (50 - 59 years)",
                     "CDC Anxiety Age (60 - 69 years)",
                     "CDC Anxiety Age (70 - 79 years)",
                     "CDC Anxiety Age (80+ years)",
                     "CDC Anxiety Sex (Male)",
                     "CDC Anxiety Sex (Female)",
                     "CDC Anxiety Race (Hispanic or Latino)",
                     "CDC Anxiety Race (Non-Hispanic White, single race)",
                     "CDC Anxiety Race (Non-Hispanic Black, single race)",
                     "CDC Anxiety Race (Non-Hispanic Asian, single race)",
                     "CDC Anxiety Race (Non-Hispanic, other races and multiple races)",
                     "CDC Anxiety Education (Less than a high school diploma)",
                     "CDC Anxiety Education (High school diploma or GED)",
                     "CDC Anxiety Education (Some college/Associate's degree)",
                     "CDC Anxiety Education (Bachelor's degree or higher)",
                     "CDC Depression US",
                     "CDC Depression Age (18 - 29 years)",
                     "CDC Depression Age (30 - 39 years",
                     "CDC Depression Age (40 - 49 years)",
                     "CDC Depression Age (50 - 59 years)",
                     "CDC Depression Age (60 - 69 years)",
                     "CDC Depression Age (70 - 79 years)",
                     "CDC Depression Age (80+ years)",
                     "CDC Depression Sex (Male)",
                     "CDC Depression Sex (Female)",
                     "CDC Depression Race (Hispanic or Latino)",
                     "CDC Depression Race (Non-Hispanic White, single race)",
                     "CDC Depression Race (Non-Hispanic Black, single race)",
                     "CDC Depression Race (Non-Hispanic Asian, single race)",
                     "CDC Depression Race (Non-Hispanic, other races and multiple races)",
                     "CDC Depression Education (Less than a high school diploma)",
                     "CDC Depression Education (High school diploma or GED)",
                     "CDC Depression Education (Some college/Associate's degree)",
                     "CDC Depression Education (Bachelor's degree or higher)",
                     "Google Trends 'covid'",
                     "Google Trends 'body aches'",
                     "Google Trends 'sore throat'",
                     "Google Trends 'cough'",
                     "Google Trends 'anxiety'",
                     "Google Trends 'panic attacks'",
                     "Google Trends 'hyperventilation'",
                     "Google Trends 'loss of focus'",
                     "Google Trends 'depression'",
                     "Google Trends 'sadness'",
                     "Google Trends 'fatigue'",
                     "Google Trends 'suicidal thoughts'", ],
            value="Google Trends 'covid'",
            clearable=False,
            style={'width': '100%', 'padding-left': '10px'}
        ),
    ], style={'display': 'flex', 'flex-direction': 'row', 'width': 'full', 'justify-content': 'center'}),
    html.H2('Spider Charts of Groups and Subgroups Average CDC Values'),
    dcc.Graph(id="spider-chart",
              style={'height': '650px', 'width': '100%'}),
    html.P("Select Graph:"),
    dcc.Dropdown(
        id="spiderTicker",
        options=["Anxiety & Depression",
                 "Age (Subgroups)", "Sex (Subgroups)", "Race (Subgroups)", "Education (Subgroups)"],
        value="Anxiety & Depression",
        clearable=False,
    ),
    dcc.Graph(id="sex-pyramid-graph",
              style={'height': '650px', 'width': '50%'}),
    html.P("Select Graph:"),
    dcc.Dropdown(
        id="sexBarTicker",
        options=["Anxiety", "Depression"],
        value="Anxiety",
        clearable=False,
    ),
    dcc.Graph(id="sex-bar-graph",
              style={'height': '650px', 'width': '50%'}),
    dcc.Graph(id="education-bar-graph",
              style={'height': '650px', 'width': '50%'}),
    dcc.Dropdown(
        id="educationBarTicker",
        options=["Anxiety", "Depression"],
        value="Anxiety",
        clearable=False,
    ),
    dcc.Graph(id="age-bar-graph",
              style={'height': '650px', 'width': '50%'}),
    dcc.Dropdown(
        id="ageBarTicker",
        options=["Anxiety", "Depression"],
        value="Anxiety",
        clearable=False,
    ),
    dcc.Graph(id="big-bar-graph",
              style={'height': '650px', 'width': '100%'}),
    dcc.Graph(id="state-map",
              style={'height': '650px', 'width': '100%'}),
    dcc.Dropdown(
        id="stateMapTicker",
        options=["Anxiety", "Depression"],
        value="Anxiety",
        clearable=False,
    ),
])


@app.callback(
    Output("state-map", "figure"),
    Input("stateMapTicker", "value"))
def display_sex_bar(stateMapTicker):

    if stateMapTicker == 'Anxiety':
        color = 'ylorrd'
        raw = cdcAnxietyState
    elif stateMapTicker == 'Depression':
        color = 'greys'
        raw = cdcDepressionState

    state_abbrev = [
        'AL', 'AK', 'AZ', 'AR', 'CA', 'CO', 'CT', 'DE', 'DC', 'FL', 'GA',
        'HI', 'ID', 'IL', 'IN', 'IA', 'KS', 'KY', 'LA', 'ME', 'MD', 'MA',
        'MI', 'MN', 'MS', 'MO', 'MT', 'NE', 'NV', 'NH', 'NJ', 'NM', 'NY',
        'NC', 'ND', 'OH', 'OK', 'OR', 'PA', 'RI', 'SC', 'SD', 'TN', 'TX',
        'UT', 'VT', 'VA', 'WA', 'WV', 'WI', 'WY'
    ]
    # convert raw.columns from state names to state abbreviations
    raw.columns = state_abbrev

    week = []
    state = []
    value = []
    # iterate over week
    for i in range(len(googleTrendsData['week'])):
        for j in range(len(raw.columns)):
            week.append(googleTrendsData['week'][i])
            state.append(raw.columns[j])
            value.append(raw[raw.columns[j]][i])

    data = pd.DataFrame({'week': week, 'state': state, 'value': value})

    fig = px.choropleth(data, locations="state", locationmode="USA-states", animation_frame="week",
                        color="value", color_continuous_scale=color, scope="usa")

    return fig


@app.callback(
    Output("big-bar-graph", "figure"),
    Input("stateMapTicker", "value"))
def display_big_bar(x):

    tempAnxCol = []
    for i in range(len(cdcAnxietyAge.columns.tolist())):
        tempAnxCol.append(cdcAnxietyAge.columns.tolist()[i])
    for i in range(len(cdcAnxietySex.columns.tolist())):
        tempAnxCol.append(cdcAnxietySex.columns.tolist()[i])
    for i in range(len(cdcAnxietyRace.columns.tolist())):
        tempAnxCol.append(cdcAnxietyRace.columns.tolist()[i])
    for i in range(len(cdcAnxietyEducation.columns.tolist())):
        tempAnxCol.append(cdcAnxietyEducation.columns.tolist()[i])

    tempDepCol = []
    for i in range(len(cdcDepressionAge.columns.tolist())):
        tempDepCol.append(cdcDepressionAge.columns.tolist()[i])
    for i in range(len(cdcDepressionSex.columns.tolist())):
        tempDepCol.append(cdcDepressionSex.columns.tolist()[i])
    for i in range(len(cdcDepressionRace.columns.tolist())):
        tempDepCol.append(cdcDepressionRace.columns.tolist()[i])
    for i in range(len(cdcDepressionEducation.columns.tolist())):
        tempDepCol.append(cdcDepressionEducation.columns.tolist()[i])

    tempAnxMean = []
    for i in range(len(cdcAnxietyAge.mean().tolist())):
        tempAnxMean.append(cdcAnxietyAge.mean().tolist()[i])
    for i in range(len(cdcAnxietySex.mean().tolist())):
        tempAnxMean.append(cdcAnxietySex.mean().tolist()[i])
    for i in range(len(cdcAnxietyRace.mean().tolist())):
        tempAnxMean.append(cdcAnxietyRace.mean().tolist()[i])
    for i in range(len(cdcAnxietyEducation.mean().tolist())):
        tempAnxMean.append(cdcAnxietyEducation.mean().tolist()[i])

    tempDepMean = []
    for i in range(len(cdcDepressionAge.mean().tolist())):
        tempDepMean.append(cdcDepressionAge.mean().tolist()[i])
    for i in range(len(cdcDepressionSex.mean().tolist())):
        tempDepMean.append(cdcDepressionSex.mean().tolist()[i])
    for i in range(len(cdcDepressionRace.mean().tolist())):
        tempDepMean.append(cdcDepressionRace.mean().tolist()[i])
    for i in range(len(cdcDepressionEducation.mean().tolist())):
        tempDepMean.append(cdcDepressionEducation.mean().tolist()[i])

    dataAnx = pd.DataFrame(
        {'col': tempAnxCol, 'mean': tempAnxMean})
    dataDep = pd.DataFrame(
        {'col': tempDepCol, 'mean': tempDepMean})

    fig = go.Figure()

    fig.add_trace(go.Bar(x=dataAnx['col'], y=dataAnx['mean'],
                         name='Anxiety',
                         marker=dict(color=dataAnx["mean"], colorscale='ylorrd')))

    fig.add_trace(go.Bar(x=dataDep['col'], y=dataDep['mean'],
                         name='Depression',
                         marker=dict(color=dataDep["mean"], colorscale='greys')))

    fig.update_layout(title='CDC Anxiety & Depression Average (All Subgroups)',
                      title_font_size=22, xaxis_title='All Subgroups', yaxis_title='Average CDC Value', barmode='group')

    return fig


@ app.callback(
    Output("age-bar-graph", "figure"),
    Input("ageBarTicker", "value"))
def display_sex_bar(ageBarTicker):

    if ageBarTicker == 'Anxiety':
        name = 'Anxiety'
        color = 'ylorrd'
        data = pd.DataFrame(
            {'col': cdcAnxietyAge.columns.tolist(), 'mean': cdcAnxietyAge.mean()})
    elif ageBarTicker == 'Depression':
        name = 'Depression'
        color = 'greys'
        data = pd.DataFrame(
            {'col': cdcDepressionAge.columns.tolist(), 'mean': cdcDepressionAge.mean()})

    fig = px.bar(data, x='col', y='mean',
                 color='mean', color_continuous_scale=color)

    fig.update_layout(title='CDC ' + name + ' Average (By Age)',
                      title_font_size=22, xaxis_title='Age Level', yaxis_title='Average CDC Value',)

    return fig


@ app.callback(
    Output("education-bar-graph", "figure"),
    Input("educationBarTicker", "value"))
def display_sex_bar(educationBarTicker):

    if educationBarTicker == 'Anxiety':
        name = 'Anxiety'
        color = 'ylorrd'
        data = pd.DataFrame(
            {'col': cdcAnxietyEducation.columns.tolist(), 'mean': cdcAnxietyEducation.mean()})
    elif educationBarTicker == 'Depression':
        name = 'Depression'
        color = 'greys'
        data = pd.DataFrame(
            {'col': cdcDepressionEducation.columns.tolist(), 'mean': cdcDepressionEducation.mean()})

    fig = px.bar(data, x='col', y='mean',
                 color='mean', color_continuous_scale=color)

    fig.update_layout(title='CDC ' + name + ' Average (By Education)',
                      title_font_size=22, xaxis_title='Education Level', yaxis_title='Average CDC Value',)

    return fig


@ app.callback(
    Output("sex-bar-graph", "figure"),
    Input("sexBarTicker", "value"))
def display_sex_bar(sexBarTicker):
    fig = go.Figure()

    fig.add_trace(go.Bar(x=["Male", "Female"], y=[cdcAnxietySex["Male"].mean(), cdcAnxietySex["Female"].mean()],
                         name="Anxiety", marker=dict(color='red', line=dict(color='#99ccff'))))
    fig.add_trace(go.Bar(x=["Male", "Female"], y=[cdcDepressionSex["Male"].mean(), cdcDepressionSex["Female"].mean()],
                         name="Depression", marker=dict(color='black', line=dict(color='pink'))))

    fig.update_layout(title='CDC Anxiety & Depression Average (By Sex)',
                      title_font_size=22, barmode='group',)

    return fig


@ app.callback(
    Output("sex-pyramid-graph", "figure"),
    Input("sexBarTicker", "value"))
def display_sex_pyramid(sexBarTicker):
    if sexBarTicker == "Anxiety":
        x = googleTrendsData["week"]
        yMale = cdcAnxietySex["Male"] * -1
        yFemale = cdcAnxietySex["Female"]
    elif sexBarTicker == "Depression":
        x = googleTrendsData["week"]
        yMale = cdcDepressionSex["Male"] * -1
        yFemale = cdcDepressionSex["Female"]

    fig = go.Figure()

    fig.add_trace(go.Bar(x=yMale, y=x, orientation='h',
                         name="Male", marker=dict(color='#99ccff')))
    fig.add_trace(go.Bar(x=yFemale, y=x, orientation='h',
                         name="Female", marker=dict(color='pink')))

    fig.update_layout(title='CDC By Sex Value ('+sexBarTicker+")",
                      title_font_size=22, barmode='relative',
                      bargap=0.0, bargroupgap=0,
                      xaxis=dict(tickvals=[-1, -0.8, -0.6, -0.4, -0.2, 0, 0.2, 0.4, 0.6, 0.8, 1],
                                 title='CDC Value',
                                 title_font_size=14)
                      )

    return fig


@ app.callback(
    Output("spider-chart", "figure"),
    Input("spiderTicker", "value"))
def display_spider_chart(spiderTicker):
    if spiderTicker == "Anxiety & Depression":
        theta = names
        r1 = [cdcAnxietyUS["United States"].mean(), cdcAnxietyAge.mean()[1].mean(),
              cdcAnxietySex.mean()[1].mean(), cdcAnxietyRace.mean()[1].mean(), cdcAnxietyEducation.mean()[1].mean()]
        r2 = [cdcDepressionUS["United States"].mean(), cdcDepressionAge.mean()[1].mean(), cdcDepressionSex.mean()[
            1].mean(), cdcDepressionRace.mean()[1].mean(), cdcDepressionEducation.mean()[1].mean()]
        name1 = "Anxiety"
        name2 = "Depression"
        color1 = 'red'
        color2 = 'black'
        title = "Anxiety & Depression (Average of All Subgroups)"
    elif spiderTicker == "Age (Subgroups)":
        theta = cdcAnxietyAge.columns.tolist()
        r1 = cdcAnxietyAge.mean()
        r2 = cdcDepressionAge.mean()
        name1 = "Anxiety"
        name2 = "Depression"
        color1 = 'red'
        color2 = 'black'
        title = "Anxiety & Depression (Age Subgroups)"
    elif spiderTicker == "Sex (Subgroups)":
        theta = cdcAnxietySex.columns.tolist()
        r1 = cdcAnxietySex.mean()
        r2 = cdcDepressionSex.mean()
        name1 = "Anxiety"
        name2 = "Depression"
        color1 = 'red'
        color2 = 'black'
        title = "Anxiety & Depression (Sex Subgroups)"
    elif spiderTicker == "Race (Subgroups)":
        theta = cdcAnxietyRace.columns.tolist()
        r1 = cdcAnxietyRace.mean()
        r2 = cdcDepressionRace.mean()
        name1 = "Anxiety"
        name2 = "Depression"
        color1 = 'red'
        color2 = 'black'
        title = "Anxiety & Depression (Race Subgroups)"
    elif spiderTicker == "Education (Subgroups)":
        theta = cdcAnxietyEducation.columns.tolist()
        r1 = cdcAnxietyEducation.mean()
        r2 = cdcDepressionEducation.mean()
        name1 = "Anxiety"
        name2 = "Depression"
        color1 = 'red'
        color2 = 'black'
        title = "Anxiety & Depression (Education Subgroups)"

    fig = go.Figure()

    fig.add_trace(go.Scatterpolar(
        r=r1,
        theta=theta,
        fill='toself',
        name=name1,
        line=dict(color=color1),
    ))
    fig.add_trace(go.Scatterpolar(
        r=r2,
        theta=theta,
        fill='toself',
        name=name2,
        line=dict(color=color2),
    ))
    fig.update_layout(
        title=title,
        polar=dict(
            radialaxis=dict(
                visible=True,
                range=[0, 1]
            )),
        showlegend=True
    )

    return fig


@ app.callback(
    Output("time-series-chart", "figure"),
    Input("ticker", "value"))
def display_time_series(ticker):

    # case switch for ticker values
    if ticker == "CDC Anxiety US":
        isSolo = True
        axisData = cdcAnxietyUS['United States']
        title = 'CDC Anxiety Trend (National Estimate)'
        axisTitle = 'CDC Value'
    elif ticker == "CDC Anxiety Age":
        isSolo = False
        axisData = cdcAnxietyAge
        title = 'CDC Anxiety Trends (By Age)'
        axisTitle = 'CDC Value'
    elif ticker == "CDC Anxiety Sex":
        isSolo = False
        axisData = cdcAnxietySex
        title = 'CDC Anxiety Trends (By Sex)'
        axisTitle = 'CDC Value'
    elif ticker == "CDC Anxiety Race":
        isSolo = False
        axisData = cdcAnxietyRace
        title = 'CDC Anxiety Trends (By Race)'
        axisTitle = 'CDC Value'
    elif ticker == "CDC Anxiety Education":
        isSolo = False
        axisData = cdcAnxietyEducation
        title = 'CDC Anxiety Trends (By Education)'
        axisTitle = 'CDC Value'
    elif ticker == "CDC Anxiety States":
        isSolo = False
        axisData = cdcAnxietyState
        title = 'CDC Anxiety Trends (By State)'
        axisTitle = 'CDC Value'
    elif ticker == "CDC Depression US":
        isSolo = True
        axisData = cdcDepressionUS['United States']
        title = 'CDC Depression Trend (National Estimate)'
        axisTitle = 'CDC Value'
    elif ticker == "CDC Depression Age":
        isSolo = False
        axisData = cdcDepressionAge
        title = 'CDC Depression Trends (By Age)'
        axisTitle = 'CDC Value'
    elif ticker == "CDC Depression Sex":
        isSolo = False
        axisData = cdcDepressionSex
        title = 'CDC Depression Trends (By Sex)'
        axisTitle = 'CDC Value'
    elif ticker == "CDC Depression Race":
        isSolo = False
        axisData = cdcDepressionRace
        title = 'CDC Depression Trends (By Race)'
        axisTitle = 'CDC Value'
    elif ticker == "CDC Depression Education":
        isSolo = False
        axisData = cdcDepressionEducation
        title = 'CDC Depression Trends (By Education)'
        axisTitle = 'CDC Value'
    elif ticker == "CDC Depression States":
        isSolo = False
        axisData = cdcDepressionState
        title = 'CDC Depression Trends (By State)'
        axisTitle = 'CDC Value'
    elif ticker == "Google Trends 'covid'":
        isSolo = False
        axisData = pd.DataFrame(googleTrendsData['covid'])
        axisData['Body Aches'] = googleTrendsData['bodyAches']
        axisData['Sore Throat'] = googleTrendsData['soreThroat']
        axisData['Cough'] = googleTrendsData['cough']
        title = 'Google Search Trends (Covid-19 & Symptoms)'
        axisTitle = 'Google Trends Value'
    elif ticker == "Google Trends 'anxiety'":
        isSolo = False
        axisData = pd.DataFrame(googleTrendsData['anxiety'])
        axisData['Panic Attacks'] = googleTrendsData['panicAttacks']
        axisData['Hyperventilation'] = googleTrendsData['hyperventilation']
        axisData['Loss of Focus'] = googleTrendsData['lossOfFocus']
        title = 'Google Search Trends (Anxiety & Symptoms)'
        axisTitle = 'Google Trends Value'
    elif ticker == "Google Trends 'depression'":
        isSolo = False
        axisData = pd.DataFrame(googleTrendsData['depression'])
        axisData['Sadness'] = googleTrendsData['sadness']
        axisData['Fatigue'] = googleTrendsData['fatigue']
        axisData['Suicidal Thoughts'] = googleTrendsData['suicidalThoughts']
        title = 'Google Search Trends (Depression & Symptoms)'
        axisTitle = 'Google Trends Value'

    if isSolo:
        # Time Series Chart
        fig = go.Figure([go.Scatter(
            x=googleTrendsData['week'], y=axisData)])
        fig.add_hline(y=axisData.mean(), line_dash="dot",
                      annotation_text="Average",
                      annotation_position="bottom right")
        # add line for 2 points in time delta: 2020-05-20 and omnicron: 2021-12-01
        # 2020-05-20 x-axis line
        fig.add_vline(
            x="2020-11-08", line_width=2, line_dash="solid", line_color="orange", name="Delta")
        fig.add_vline(
            x="2021-12-20", line_width=2, line_dash="solid", line_color="red", name="Omnicron")
        fig.update_layout(
            title_text=title)
        fig.update_xaxes(title_text='Time')
        fig.update_yaxes(title_text=axisTitle)
    else:
        fig = go.Figure()
        # iterate through all columns in dataframe axisData
        for col in axisData.columns:
            fig.add_trace(go.Scatter(x=googleTrendsData['week'], y=axisData[col],
                                     mode='lines',
                                     name=col))
        # fig.add_hline(y=axisData.mean(), line_dash="dot",
        #               annotation_text="Average",
        #               annotation_position="bottom right")
        fig.add_vline(
            x="2020-11-08", line_width=2, line_dash="solid", line_color="orange", name="Delta")
        fig.add_vline(
            x="2021-12-20", line_width=2, line_dash="solid", line_color="red", name="Omnicron")
        fig.update_layout(
            title_text=title)
        fig.update_xaxes(title_text='Time')
        fig.update_yaxes(title_text=axisTitle)

    return fig


@ app.callback(
    Output("correlation-chart", "figure"),
    Input("correlation-ticker1", "value"),
    Input("correlation-ticker2", "value"))
def display_correlation_chart(correlation_ticker1, correlation_ticker2):

    # case switch for correlation-ticker1 values
    if correlation_ticker1 == "CDC Anxiety US":
        x = cdcAnxietyUS['United States']
        xTitle = 'CDC Value'
        # scale = 'oranges'
    elif correlation_ticker1 == "CDC Anxiety Age (18 - 29 years)":
        x = cdcAnxietyAge['18 - 29 years']
        xTitle = 'CDC Value'
    elif correlation_ticker1 == "CDC Anxiety Age (30 - 39 years":
        x = cdcAnxietyAge['30 - 39 years']
        xTitle = 'CDC Value'
    elif correlation_ticker1 == "CDC Anxiety Age (40 - 49 years)":
        x = cdcAnxietyAge['40 - 49 years']
        xTitle = 'CDC Value'
    elif correlation_ticker1 == "CDC Anxiety Age (50 - 59 years)":
        x = cdcAnxietyAge['50 - 59 years']
        xTitle = 'CDC Value'
    elif correlation_ticker1 == "CDC Anxiety Age (60 - 69 years)":
        x = cdcAnxietyAge['60 - 69 years']
        xTitle = 'CDC Value'
    elif correlation_ticker1 == "CDC Anxiety Age (70 - 79 years)":
        x = cdcAnxietyAge['70 - 79 years']
        xTitle = 'CDC Value'
    elif correlation_ticker1 == "CDC Anxiety Age (80+ years)":
        x = cdcAnxietyAge['80 years and above']
        xTitle = 'CDC Value'
    elif correlation_ticker1 == "CDC Anxiety Sex (Male)":
        x = cdcAnxietySex['Male']
        xTitle = 'CDC Value'
    elif correlation_ticker1 == "CDC Anxiety Sex (Female)":
        x = cdcAnxietySex['Female']
        xTitle = 'CDC Value'
    elif correlation_ticker1 == "CDC Anxiety Race (Hispanic or Latino)":
        x = cdcAnxietyRace['Hispanic or Latino']
        xTitle = 'CDC Value'
    elif correlation_ticker1 == "CDC Anxiety Race (Non-Hispanic White, single race)":
        x = cdcAnxietyRace['Non-Hispanic White, single race']
        xTitle = 'CDC Value'
    elif correlation_ticker1 == "CDC Anxiety Race (Non-Hispanic Black, single race)":
        x = cdcAnxietyRace['Non-Hispanic Black, single race']
        xTitle = 'CDC Value'
    elif correlation_ticker1 == "CDC Anxiety Race (Non-Hispanic Asian, single race)":
        x = cdcAnxietyRace['Non-Hispanic Asian, single race']
        xTitle = 'CDC Value'
    elif correlation_ticker1 == "CDC Anxiety Race (Non-Hispanic, other races and multiple races)":
        x = cdcAnxietyRace['Non-Hispanic, other races and multiple races']
        xTitle = 'CDC Value'
    elif correlation_ticker1 == "CDC Anxiety Education (Less than a high school diploma)":
        x = cdcAnxietyEducation['Less than a high school diploma']
        xTitle = 'CDC Value'
    elif correlation_ticker1 == "CDC Anxiety Education (High school diploma or GED)":
        x = cdcAnxietyEducation['High school diploma or GED']
        xTitle = 'CDC Value'
    elif correlation_ticker1 == "CDC Anxiety Education (Some college/Associate's degree)":
        x = cdcAnxietyEducation["Some college/Associate's degree"]
        xTitle = 'CDC Value'
    elif correlation_ticker1 == "CDC Anxiety Education (Bachelor's degree or higher)":
        x = cdcAnxietyEducation["Bachelor's degree or higher"]
        xTitle = 'CDC Value'
    elif correlation_ticker1 == "CDC Depression US":
        x = cdcDepressionUS['United States']
        xTitle = 'CDC Value'
    elif correlation_ticker1 == "CDC Depression Age (18 - 29 years)":
        x = cdcDepressionAge['18 - 29 years']
        xTitle = 'CDC Value'
    elif correlation_ticker1 == "CDC Depression Age (30 - 39 years":
        x = cdcDepressionAge['30 - 39 years']
        xTitle = 'CDC Value'
    elif correlation_ticker1 == "CDC Depression Age (40 - 49 years)":
        x = cdcDepressionAge['40 - 49 years']
        xTitle = 'CDC Value'
    elif correlation_ticker1 == "CDC Depression Age (50 - 59 years)":
        x = cdcDepressionAge['50 - 59 years']
        xTitle = 'CDC Value'
    elif correlation_ticker1 == "CDC Depression Age (60 - 69 years)":
        x = cdcDepressionAge['60 - 69 years']
        xTitle = 'CDC Value'
    elif correlation_ticker1 == "CDC Depression Age (70 - 79 years)":
        x = cdcDepressionAge['70 - 79 years']
        xTitle = 'CDC Value'
    elif correlation_ticker1 == "CDC Depression Age (80+ years)":
        x = cdcDepressionAge['80 years and above']
        xTitle = 'CDC Value'
    elif correlation_ticker1 == "CDC Depression Sex (Male)":
        x = cdcDepressionSex['Male']
        xTitle = 'CDC Value'
    elif correlation_ticker1 == "CDC Depression Sex (Female)":
        x = cdcDepressionSex['Female']
        xTitle = 'CDC Value'
    elif correlation_ticker1 == "CDC Depression Race (Hispanic or Latino)":
        x = cdcDepressionRace['Hispanic or Latino']
        xTitle = 'CDC Value'
    elif correlation_ticker1 == "CDC Depression Race (Non-Hispanic White, single race)":
        x = cdcDepressionRace['Non-Hispanic White, single race']
        xTitle = 'CDC Value'
    elif correlation_ticker1 == "CDC Depression Race (Non-Hispanic Black, single race)":
        x = cdcDepressionRace['Non-Hispanic Black, single race']
        xTitle = 'CDC Value'
    elif correlation_ticker1 == "CDC Depression Race (Non-Hispanic Asian, single race)":
        x = cdcDepressionRace['Non-Hispanic Asian, single race']
        xTitle = 'CDC Value'
    elif correlation_ticker1 == "CDC Depression Race (Non-Hispanic, other races and multiple races)":
        x = cdcDepressionRace['Non-Hispanic, other races and multiple races']
        xTitle = 'CDC Value'
    elif correlation_ticker1 == "CDC Depression Education (Less than a high school diploma)":
        x = cdcDepressionEducation['Less than a high school diploma']
        xTitle = 'CDC Value'
    elif correlation_ticker1 == "CDC Depression Education (High school diploma or GED)":
        x = cdcDepressionEducation['High school diploma or GED']
        xTitle = 'CDC Value'
    elif correlation_ticker1 == "CDC Depression Education (Some college/Associate's degree)":
        x = cdcDepressionEducation["Some college/Associate's degree"]
        xTitle = 'CDC Value'
    elif correlation_ticker1 == "CDC Depression Education (Bachelor's degree or higher)":
        x = cdcDepressionEducation["Bachelor's degree or higher"]
        xTitle = 'CDC Value'
    elif correlation_ticker1 == "Google Trends 'covid'":
        x = googleTrendsData['covid']
        xTitle = 'Google Trends Value'
    elif correlation_ticker1 == "Google Trends 'body aches'":
        x = googleTrendsData['bodyAches']
        xTitle = 'Google Trends Value'
    elif correlation_ticker1 == "Google Trends 'sore throat'":
        x = googleTrendsData['soreThroat']
        xTitle = 'Google Trends Value'
    elif correlation_ticker1 == "Google Trends 'cough'":
        x = googleTrendsData['cough']
        xTitle = 'Google Trends Value'
    elif correlation_ticker1 == "Google Trends 'anxiety'":
        x = googleTrendsData['anxiety']
        xTitle = 'Google Trends Value'
    elif correlation_ticker1 == "Google Trends 'panic attacks'":
        x = googleTrendsData['panicAttacks']
        xTitle = 'Google Trends Value'
    elif correlation_ticker1 == "Google Trends 'hyperventilation'":
        x = googleTrendsData['hyperventilation']
        xTitle = 'Google Trends Value'
    elif correlation_ticker1 == "Google Trends 'loss of focus'":
        x = googleTrendsData['lossOfFocus']
        xTitle = 'Google Trends Value'
    elif correlation_ticker1 == "Google Trends 'depression'":
        x = googleTrendsData['depression']
        xTitle = 'Google Trends Value'
    elif correlation_ticker1 == "Google Trends 'sadness'":
        x = googleTrendsData['sadness']
        xTitle = 'Google Trends Value'
    elif correlation_ticker1 == "Google Trends 'fatigue'":
        x = googleTrendsData['fatigue']
        xTitle = 'Google Trends Value'
    elif correlation_ticker1 == "Google Trends 'suicidal thoughts'":
        x = googleTrendsData['suicidalThoughts']
        xTitle = 'Google Trends Value'

    # case switch for correlation-ticker2 values
    if correlation_ticker2 == "CDC Anxiety US":
        y = cdcAnxietyUS['United States']
        yTitle = 'CDC Value'
    elif correlation_ticker2 == "CDC Anxiety Age (18 - 29 years)":
        y = cdcAnxietyAge['18 - 29 years']
        yTitle = 'CDC Value'
    elif correlation_ticker2 == "CDC Anxiety Age (30 - 39 years":
        y = cdcAnxietyAge['30 - 39 years']
        yTitle = 'CDC Value'
    elif correlation_ticker2 == "CDC Anxiety Age (40 - 49 years)":
        y = cdcAnxietyAge['40 - 49 years']
        yTitle = 'CDC Value'
    elif correlation_ticker2 == "CDC Anxiety Age (50 - 59 years)":
        y = cdcAnxietyAge['50 - 59 years']
        yTitle = 'CDC Value'
    elif correlation_ticker2 == "CDC Anxiety Age (60 - 69 years)":
        y = cdcAnxietyAge['60 - 69 years']
        yTitle = 'CDC Value'
    elif correlation_ticker2 == "CDC Anxiety Age (70 - 79 years)":
        y = cdcAnxietyAge['70 - 79 years']
        yTitle = 'CDC Value'
    elif correlation_ticker2 == "CDC Anxiety Age (80+ years)":
        y = cdcAnxietyAge['80 years and above']
        yTitle = 'CDC Value'
    elif correlation_ticker2 == "CDC Anxiety Sex (Male)":
        y = cdcAnxietySex['Male']
        yTitle = 'CDC Value'
    elif correlation_ticker2 == "CDC Anxiety Sex (Female)":
        y = cdcAnxietySex['Female']
        yTitle = 'CDC Value'
    elif correlation_ticker2 == "CDC Anxiety Race (Hispanic or Latino)":
        y = cdcAnxietyRace['Hispanic or Latino']
        yTitle = 'CDC Value'
    elif correlation_ticker2 == "CDC Anxiety Race (Non-Hispanic White, single race)":
        y = cdcAnxietyRace['Non-Hispanic White, single race']
        yTitle = 'CDC Value'
    elif correlation_ticker2 == "CDC Anxiety Race (Non-Hispanic Black, single race)":
        y = cdcAnxietyRace['Non-Hispanic Black, single race']
        yTitle = 'CDC Value'
    elif correlation_ticker2 == "CDC Anxiety Race (Non-Hispanic Asian, single race)":
        y = cdcAnxietyRace['Non-Hispanic Asian, single race']
        yTitle = 'CDC Value'
    elif correlation_ticker2 == "CDC Anxiety Race (Non-Hispanic, other races and multiple races)":
        y = cdcAnxietyRace['Non-Hispanic, other races and multiple races']
        yTitle = 'CDC Value'
    elif correlation_ticker2 == "CDC Anxiety Education (Less than a high school diploma)":
        y = cdcAnxietyEducation['Less than a high school diploma']
        yTitle = 'CDC Value'
    elif correlation_ticker2 == "CDC Anxiety Education (High school diploma or GED)":
        y = cdcAnxietyEducation['High school diploma or GED']
        yTitle = 'CDC Value'
    elif correlation_ticker2 == "CDC Anxiety Education (Some college/Associate's degree)":
        y = cdcAnxietyEducation["Some college/Associate's degree"]
        yTitle = 'CDC Value'
    elif correlation_ticker2 == "CDC Anxiety Education (Bachelor's degree or higher)":
        y = cdcAnxietyEducation["Bachelor's degree or higher"]
        yTitle = 'CDC Value'
    elif correlation_ticker2 == "CDC Depression US":
        y = cdcDepressionUS['United States']
        yTitle = 'CDC Value'
    elif correlation_ticker2 == "CDC Depression Age (18 - 29 years)":
        y = cdcDepressionAge['18 - 29 years']
        yTitle = 'CDC Value'
    elif correlation_ticker2 == "CDC Depression Age (30 - 39 years":
        y = cdcDepressionAge['30 - 39 years']
        yTitle = 'CDC Value'
    elif correlation_ticker2 == "CDC Depression Age (40 - 49 years)":
        y = cdcDepressionAge['40 - 49 years']
        yTitle = 'CDC Value'
    elif correlation_ticker2 == "CDC Depression Age (50 - 59 years)":
        y = cdcDepressionAge['50 - 59 years']
        yTitle = 'CDC Value'
    elif correlation_ticker2 == "CDC Depression Age (60 - 69 years)":
        y = cdcDepressionAge['60 - 69 years']
        yTitle = 'CDC Value'
    elif correlation_ticker2 == "CDC Depression Age (70 - 79 years)":
        y = cdcDepressionAge['70 - 79 years']
        yTitle = 'CDC Value'
    elif correlation_ticker2 == "CDC Depression Age (80+ years)":
        y = cdcDepressionAge['80 years and above']
        yTitle = 'CDC Value'
    elif correlation_ticker2 == "CDC Depression Sex (Male)":
        y = cdcDepressionSex['Male']
        yTitle = 'CDC Value'
    elif correlation_ticker2 == "CDC Depression Sex (Female)":
        y = cdcDepressionSex['Female']
        yTitle = 'CDC Value'
    elif correlation_ticker2 == "CDC Depression Race (Hispanic or Latino)":
        y = cdcDepressionRace['Hispanic or Latino']
        yTitle = 'CDC Value'
    elif correlation_ticker2 == "CDC Depression Race (Non-Hispanic White, single race)":
        y = cdcDepressionRace['Non-Hispanic White, single race']
        yTitle = 'CDC Value'
    elif correlation_ticker2 == "CDC Depression Race (Non-Hispanic Black, single race)":
        y = cdcDepressionRace['Non-Hispanic Black, single race']
        yTitle = 'CDC Value'
    elif correlation_ticker2 == "CDC Depression Race (Non-Hispanic Asian, single race)":
        y = cdcDepressionRace['Non-Hispanic Asian, single race']
        yTitle = 'CDC Value'
    elif correlation_ticker2 == "CDC Depression Race (Non-Hispanic, other races and multiple races)":
        y = cdcDepressionRace['Non-Hispanic, other races and multiple races']
        yTitle = 'CDC Value'
    elif correlation_ticker2 == "CDC Depression Education (Less than a high school diploma)":
        y = cdcDepressionEducation['Less than a high school diploma']
        yTitle = 'CDC Value'
    elif correlation_ticker2 == "CDC Depression Education (High school diploma or GED)":
        y = cdcDepressionEducation['High school diploma or GED']
        yTitle = 'CDC Value'
    elif correlation_ticker2 == "CDC Depression Education (Some college/Associate's degree)":
        y = cdcDepressionEducation["Some college/Associate's degree"]
        yTitle = 'CDC Value'
    elif correlation_ticker2 == "CDC Depression Education (Bachelor's degree or higher)":
        y = cdcDepressionEducation["Bachelor's degree or higher"]
        yTitle = 'CDC Value'
    elif correlation_ticker2 == "Google Trends 'covid'":
        y = googleTrendsData['covid']
        yTitle = 'Google Trends Value'
    elif correlation_ticker2 == "Google Trends 'body aches'":
        y = googleTrendsData['bodyAches']
        yTitle = 'Google Trends Value'
    elif correlation_ticker2 == "Google Trends 'sore throat'":
        y = googleTrendsData['soreThroat']
        yTitle = 'Google Trends Value'
    elif correlation_ticker2 == "Google Trends 'cough'":
        y = googleTrendsData['cough']
        yTitle = 'Google Trends Value'
    elif correlation_ticker2 == "Google Trends 'anxiety'":
        y = googleTrendsData['anxiety']
        yTitle = 'Google Trends Value'
    elif correlation_ticker2 == "Google Trends 'panic attacks'":
        y = googleTrendsData['panicAttacks']
        yTitle = 'Google Trends Value'
    elif correlation_ticker2 == "Google Trends 'hyperventilation'":
        y = googleTrendsData['hyperventilation']
        yTitle = 'Google Trends Value'
    elif correlation_ticker2 == "Google Trends 'loss of focus'":
        y = googleTrendsData['lossOfFocus']
        yTitle = 'Google Trends Value'
    elif correlation_ticker2 == "Google Trends 'depression'":
        y = googleTrendsData['depression']
        yTitle = 'Google Trends Value'
    elif correlation_ticker2 == "Google Trends 'sadness'":
        y = googleTrendsData['sadness']
        yTitle = 'Google Trends Value'
    elif correlation_ticker2 == "Google Trends 'fatigue'":
        y = googleTrendsData['fatigue']
        yTitle = 'Google Trends Value'
    elif correlation_ticker2 == "Google Trends 'suicidal thoughts'":
        y = googleTrendsData['suicidalThoughts']
        yTitle = 'Google Trends Value'

    # # iterate over x and y and make a new dataframe with each correlation
    # corr = pd.DataFrame(googleTrendsData['week'])
    # corr.reset_index(inplace=True)
    # corr = corr.drop(corr.columns[0], axis=1)
    # temp = []
    # for i in range(len(x)):
    #     temp.append(pearsonr(x[i], y[i])[0])
    # corr['corr'] = temp
    # corr.reset_index(inplace=True)
    # corr = corr.drop(corr.columns[0], axis=1)

    # Google Trends Covid VS Google Trends Anxiety
    fig = px.scatter(x=x, y=y,
                     trendline="ols",
                     trendline_color_override="red",
                     size_max=20,
                     #  color=corr,
                     #  color_continuous_scale=scale,
                     #  hover_name=corr['week'],
                     hover_name=googleTrendsData['week'],
                     labels={x.name: xTitle, y.name: yTitle},
                     title=correlation_ticker1 + " VS " + correlation_ticker2,)
    fig.update_xaxes(title_text=correlation_ticker1)
    fig.update_yaxes(title_text=correlation_ticker2)

    return fig


@ app.callback(
    Output("correlation-info", "children"),
    Input("correlation-ticker1", "value"),
    Input("correlation-ticker2", "value"))
def display_correlation_info(correlation_ticker1, correlation_ticker2):

    # case switch for correlation-ticker1 values
    if correlation_ticker1 == "CDC Anxiety US":
        x = cdcAnxietyUS['United States']
    elif correlation_ticker1 == "CDC Anxiety Age (18 - 29 years)":
        x = cdcAnxietyAge['18 - 29 years']
    elif correlation_ticker1 == "CDC Anxiety Age (30 - 39 years":
        x = cdcAnxietyAge['30 - 39 years']
    elif correlation_ticker1 == "CDC Anxiety Age (40 - 49 years)":
        x = cdcAnxietyAge['40 - 49 years']
    elif correlation_ticker1 == "CDC Anxiety Age (50 - 59 years)":
        x = cdcAnxietyAge['50 - 59 years']
    elif correlation_ticker1 == "CDC Anxiety Age (60 - 69 years)":
        x = cdcAnxietyAge['60 - 69 years']
    elif correlation_ticker1 == "CDC Anxiety Age (70 - 79 years)":
        x = cdcAnxietyAge['70 - 79 years']
    elif correlation_ticker1 == "CDC Anxiety Age (80+ years)":
        x = cdcAnxietyAge['80 years and above']
    elif correlation_ticker1 == "CDC Anxiety Sex (Male)":
        x = cdcAnxietySex['Male']
    elif correlation_ticker1 == "CDC Anxiety Sex (Female)":
        x = cdcAnxietySex['Female']
    elif correlation_ticker1 == "CDC Anxiety Race (Hispanic or Latino)":
        x = cdcAnxietyRace['Hispanic or Latino']
    elif correlation_ticker1 == "CDC Anxiety Race (Non-Hispanic White, single race)":
        x = cdcAnxietyRace['Non-Hispanic White, single race']
    elif correlation_ticker1 == "CDC Anxiety Race (Non-Hispanic Black, single race)":
        x = cdcAnxietyRace['Non-Hispanic Black, single race']
    elif correlation_ticker1 == "CDC Anxiety Race (Non-Hispanic Asian, single race)":
        x = cdcAnxietyRace['Non-Hispanic Asian, single race']
    elif correlation_ticker1 == "CDC Anxiety Race (Non-Hispanic, other races and multiple races)":
        x = cdcAnxietyRace['Non-Hispanic, other races and multiple races']
    elif correlation_ticker1 == "CDC Anxiety Education (Less than a high school diploma)":
        x = cdcAnxietyEducation['Less than a high school diploma']
    elif correlation_ticker1 == "CDC Anxiety Education (High school diploma or GED)":
        x = cdcAnxietyEducation['High school diploma or GED']
    elif correlation_ticker1 == "CDC Anxiety Education (Some college/Associate's degree)":
        x = cdcAnxietyEducation["Some college/Associate's degree"]
    elif correlation_ticker1 == "CDC Anxiety Education (Bachelor's degree or higher)":
        x = cdcAnxietyEducation["Bachelor's degree or higher"]
    elif correlation_ticker1 == "CDC Depression US":
        x = cdcDepressionUS['United States']
    elif correlation_ticker1 == "CDC Depression Age (18 - 29 years)":
        x = cdcDepressionAge['18 - 29 years']
    elif correlation_ticker1 == "CDC Depression Age (30 - 39 years":
        x = cdcDepressionAge['30 - 39 years']
    elif correlation_ticker1 == "CDC Depression Age (40 - 49 years)":
        x = cdcDepressionAge['40 - 49 years']
    elif correlation_ticker1 == "CDC Depression Age (50 - 59 years)":
        x = cdcDepressionAge['50 - 59 years']
    elif correlation_ticker1 == "CDC Depression Age (60 - 69 years)":
        x = cdcDepressionAge['60 - 69 years']
    elif correlation_ticker1 == "CDC Depression Age (70 - 79 years)":
        x = cdcDepressionAge['70 - 79 years']
    elif correlation_ticker1 == "CDC Depression Age (80+ years)":
        x = cdcDepressionAge['80 years and above']
    elif correlation_ticker1 == "CDC Depression Sex (Male)":
        x = cdcDepressionSex['Male']
    elif correlation_ticker1 == "CDC Depression Sex (Female)":
        x = cdcDepressionSex['Female']
    elif correlation_ticker1 == "CDC Depression Race (Hispanic or Latino)":
        x = cdcDepressionRace['Hispanic or Latino']
    elif correlation_ticker1 == "CDC Depression Race (Non-Hispanic White, single race)":
        x = cdcDepressionRace['Non-Hispanic White, single race']
    elif correlation_ticker1 == "CDC Depression Race (Non-Hispanic Black, single race)":
        x = cdcDepressionRace['Non-Hispanic Black, single race']
    elif correlation_ticker1 == "CDC Depression Race (Non-Hispanic Asian, single race)":
        x = cdcDepressionRace['Non-Hispanic Asian, single race']
    elif correlation_ticker1 == "CDC Depression Race (Non-Hispanic, other races and multiple races)":
        x = cdcDepressionRace['Non-Hispanic, other races and multiple races']
    elif correlation_ticker1 == "CDC Depression Education (Less than a high school diploma)":
        x = cdcDepressionEducation['Less than a high school diploma']
    elif correlation_ticker1 == "CDC Depression Education (High school diploma or GED)":
        x = cdcDepressionEducation['High school diploma or GED']
    elif correlation_ticker1 == "CDC Depression Education (Some college/Associate's degree)":
        x = cdcDepressionEducation["Some college/Associate's degree"]
    elif correlation_ticker1 == "CDC Depression Education (Bachelor's degree or higher)":
        x = cdcDepressionEducation["Bachelor's degree or higher"]
    elif correlation_ticker1 == "Google Trends 'covid'":
        x = googleTrendsData['covid']
    elif correlation_ticker1 == "Google Trends 'body aches'":
        x = googleTrendsData['bodyAches']
    elif correlation_ticker1 == "Google Trends 'sore throat'":
        x = googleTrendsData['soreThroat']
    elif correlation_ticker1 == "Google Trends 'cough'":
        x = googleTrendsData['cough']
    elif correlation_ticker1 == "Google Trends 'anxiety'":
        x = googleTrendsData['anxiety']
    elif correlation_ticker1 == "Google Trends 'panic attacks'":
        x = googleTrendsData['panicAttacks']
    elif correlation_ticker1 == "Google Trends 'hyperventilation'":
        x = googleTrendsData['hyperventilation']
    elif correlation_ticker1 == "Google Trends 'loss of focus'":
        x = googleTrendsData['lossOfFocus']
    elif correlation_ticker1 == "Google Trends 'depression'":
        x = googleTrendsData['depression']
    elif correlation_ticker1 == "Google Trends 'sadness'":
        x = googleTrendsData['sadness']
    elif correlation_ticker1 == "Google Trends 'fatigue'":
        x = googleTrendsData['fatigue']
    elif correlation_ticker1 == "Google Trends 'suicidal thoughts'":
        x = googleTrendsData['suicidalThoughts']

    # case switch for correlation-ticker2 values
    if correlation_ticker2 == "CDC Anxiety US":
        y = cdcAnxietyUS['United States']
    elif correlation_ticker2 == "CDC Anxiety Age (18 - 29 years)":
        y = cdcAnxietyAge['18 - 29 years']
    elif correlation_ticker2 == "CDC Anxiety Age (30 - 39 years":
        y = cdcAnxietyAge['30 - 39 years']
    elif correlation_ticker2 == "CDC Anxiety Age (40 - 49 years)":
        y = cdcAnxietyAge['40 - 49 years']
    elif correlation_ticker2 == "CDC Anxiety Age (50 - 59 years)":
        y = cdcAnxietyAge['50 - 59 years']
    elif correlation_ticker2 == "CDC Anxiety Age (60 - 69 years)":
        y = cdcAnxietyAge['60 - 69 years']
    elif correlation_ticker2 == "CDC Anxiety Age (70 - 79 years)":
        y = cdcAnxietyAge['70 - 79 years']
    elif correlation_ticker2 == "CDC Anxiety Age (80+ years)":
        y = cdcAnxietyAge['80 years and above']
    elif correlation_ticker2 == "CDC Anxiety Sex (Male)":
        y = cdcAnxietySex['Male']
    elif correlation_ticker2 == "CDC Anxiety Sex (Female)":
        y = cdcAnxietySex['Female']
    elif correlation_ticker2 == "CDC Anxiety Race (Hispanic or Latino)":
        y = cdcAnxietyRace['Hispanic or Latino']
    elif correlation_ticker2 == "CDC Anxiety Race (Non-Hispanic White, single race)":
        y = cdcAnxietyRace['Non-Hispanic White, single race']
    elif correlation_ticker2 == "CDC Anxiety Race (Non-Hispanic Black, single race)":
        y = cdcAnxietyRace['Non-Hispanic Black, single race']
    elif correlation_ticker2 == "CDC Anxiety Race (Non-Hispanic Asian, single race)":
        y = cdcAnxietyRace['Non-Hispanic Asian, single race']
    elif correlation_ticker2 == "CDC Anxiety Race (Non-Hispanic, other races and multiple races)":
        y = cdcAnxietyRace['Non-Hispanic, other races and multiple races']
    elif correlation_ticker2 == "CDC Anxiety Education (Less than a high school diploma)":
        y = cdcAnxietyEducation['Less than a high school diploma']
    elif correlation_ticker2 == "CDC Anxiety Education (High school diploma or GED)":
        y = cdcAnxietyEducation['High school diploma or GED']
    elif correlation_ticker2 == "CDC Anxiety Education (Some college/Associate's degree)":
        y = cdcAnxietyEducation["Some college/Associate's degree"]
    elif correlation_ticker2 == "CDC Anxiety Education (Bachelor's degree or higher)":
        y = cdcAnxietyEducation["Bachelor's degree or higher"]
    elif correlation_ticker2 == "CDC Depression US":
        y = cdcDepressionUS['United States']
    elif correlation_ticker2 == "CDC Depression Age (18 - 29 years)":
        y = cdcDepressionAge['18 - 29 years']
    elif correlation_ticker2 == "CDC Depression Age (30 - 39 years":
        y = cdcDepressionAge['30 - 39 years']
    elif correlation_ticker2 == "CDC Depression Age (40 - 49 years)":
        y = cdcDepressionAge['40 - 49 years']
    elif correlation_ticker2 == "CDC Depression Age (50 - 59 years)":
        y = cdcDepressionAge['50 - 59 years']
    elif correlation_ticker2 == "CDC Depression Age (60 - 69 years)":
        y = cdcDepressionAge['60 - 69 years']
    elif correlation_ticker2 == "CDC Depression Age (70 - 79 years)":
        y = cdcDepressionAge['70 - 79 years']
    elif correlation_ticker2 == "CDC Depression Age (80+ years)":
        y = cdcDepressionAge['80 years and above']
    elif correlation_ticker2 == "CDC Depression Sex (Male)":
        y = cdcDepressionSex['Male']
    elif correlation_ticker2 == "CDC Depression Sex (Female)":
        y = cdcDepressionSex['Female']
    elif correlation_ticker2 == "CDC Depression Race (Hispanic or Latino)":
        y = cdcDepressionRace['Hispanic or Latino']
    elif correlation_ticker2 == "CDC Depression Race (Non-Hispanic White, single race)":
        y = cdcDepressionRace['Non-Hispanic White, single race']
    elif correlation_ticker2 == "CDC Depression Race (Non-Hispanic Black, single race)":
        y = cdcDepressionRace['Non-Hispanic Black, single race']
    elif correlation_ticker2 == "CDC Depression Race (Non-Hispanic Asian, single race)":
        y = cdcDepressionRace['Non-Hispanic Asian, single race']
    elif correlation_ticker2 == "CDC Depression Race (Non-Hispanic, other races and multiple races)":
        y = cdcDepressionRace['Non-Hispanic, other races and multiple races']
    elif correlation_ticker2 == "CDC Depression Education (Less than a high school diploma)":
        y = cdcDepressionEducation['Less than a high school diploma']
    elif correlation_ticker2 == "CDC Depression Education (High school diploma or GED)":
        y = cdcDepressionEducation['High school diploma or GED']
    elif correlation_ticker2 == "CDC Depression Education (Some college/Associate's degree)":
        y = cdcDepressionEducation["Some college/Associate's degree"]
    elif correlation_ticker2 == "CDC Depression Education (Bachelor's degree or higher)":
        y = cdcDepressionEducation["Bachelor's degree or higher"]
    elif correlation_ticker2 == "Google Trends 'covid'":
        y = googleTrendsData['covid']
    elif correlation_ticker2 == "Google Trends 'body aches'":
        y = googleTrendsData['bodyAches']
    elif correlation_ticker2 == "Google Trends 'sore throat'":
        y = googleTrendsData['soreThroat']
    elif correlation_ticker2 == "Google Trends 'cough'":
        y = googleTrendsData['cough']
    elif correlation_ticker2 == "Google Trends 'anxiety'":
        y = googleTrendsData['anxiety']
    elif correlation_ticker2 == "Google Trends 'panic attacks'":
        y = googleTrendsData['panicAttacks']
    elif correlation_ticker2 == "Google Trends 'hyperventilation'":
        y = googleTrendsData['hyperventilation']
    elif correlation_ticker2 == "Google Trends 'loss of focus'":
        y = googleTrendsData['lossOfFocus']
    elif correlation_ticker2 == "Google Trends 'depression'":
        y = googleTrendsData['depression']
    elif correlation_ticker2 == "Google Trends 'sadness'":
        y = googleTrendsData['sadness']
    elif correlation_ticker2 == "Google Trends 'fatigue'":
        y = googleTrendsData['fatigue']
    elif correlation_ticker2 == "Google Trends 'suicidal thoughts'":
        y = googleTrendsData['suicidalThoughts']

    corr = pearsonr(x, y)

    return "Correlation: " + str(format(corr[0], '.6f')) + "... " + "P-value: " + str(format(corr[1], '.6f'))


if __name__ == '__main__':
    app.run_server()  # debug=True
