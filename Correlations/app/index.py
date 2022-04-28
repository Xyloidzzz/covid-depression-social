from dash import Dash, dcc, html, Input, Output
import plotly.graph_objects as go
import plotly.express as px
import pandas as pd
from scipy.stats import pearsonr

data = pd.read_csv(
    './data/cdcAnxietyUS_googleCovid_googleAnxiety_COMBINED.csv')
# data = pd.read_csv('./data/cdcAnxiety_googleCovid_COMBINED_withMissing.csv')

# turn data from string to float
data["cdcValue"] = data["cdcValue"].astype(float)
data["googleTrendsCovidValue"] = data["googleTrendsCovidValue"].astype(float)
data["googleTrendsAnxietyValue"] = data["googleTrendsAnxietyValue"].astype(
    float)

# normalize data
data["cdcValue"] = data["cdcValue"] / data["cdcValue"].max()
data["googleTrendsCovidValue"] = data["googleTrendsCovidValue"] / \
    data["googleTrendsCovidValue"].max()
data["googleTrendsAnxietyValue"] = data["googleTrendsAnxietyValue"] / \
    data["googleTrendsAnxietyValue"].max()

#############################################START OF DASH############################################
app = Dash(__name__)

app.layout = html.Div([
    html.H1('Covid Panic Analysis'),
    html.H2('Values of Interest / Time'),
    dcc.Graph(id="time-series-chart",
              style={'height': '650px', 'width': '100%'}),
    html.P("Select Graph:"),
    dcc.Dropdown(
        id="ticker",
        options=["CDC Anxiety Value", "Google Trends 'covid'",
                 "Google Trends 'anxiety'"],
        value="CDC Anxiety Value",
        clearable=False,
    ),
    html.H2('Correlation between Covid Panic and Google Trends'),
    html.P(id="correlation-info",
           style={'fontSize': '25px', 'font-weight': 'bold'}),
    dcc.Graph(id="correlation-chart",
              style={'height': '650px', 'width': '100%'}),
    html.P("Select Graph:"),
    dcc.Dropdown(
        id="correlation-ticker",
        options=["Google Trends Covid VS Google Trends Anxiety", "CDC VS Google Trends Covid",
                 "CDC VS Google Trends Anxiety"],
        value="Google Trends Covid VS Google Trends Anxiety",
        clearable=False,
    ),
])


@app.callback(
    Output("time-series-chart", "figure"),
    Input("ticker", "value"))
def display_time_series(ticker):

    # CDC Anxiety Value Time Series
    cdcAnxietyTime = go.Figure([go.Scatter(
        x=data['week'], y=data['cdcValue'], name='CDC Anxiety National Estimate')])
    # add line for 2 points in time delta: 2020-05-20 and omnicron: 2021-12-01
    # 2020-05-20 x-axis line
    cdcAnxietyTime.add_vline(
        x="2020-11-08", line_width=2, line_dash="solid", line_color="orange", name="Delta")
    cdcAnxietyTime.add_vline(
        x="2021-12-20", line_width=2, line_dash="solid", line_color="red", name="Omnicron")
    cdcAnxietyTime.update_layout(
        title_text='CDC Sentiment Analysis (Anxiety Over Time)')
    cdcAnxietyTime.update_xaxes(title_text='Time')
    cdcAnxietyTime.update_yaxes(title_text='CDC Value')

    # Google Trends 'covid' Time Series
    googleCovidTime = go.Figure(
        [go.Scatter(x=data['week'], y=data['googleTrendsCovidValue'])])
    googleCovidTime.add_vline(
        x="2020-11-08", line_width=2, line_dash="solid", line_color="orange", name="Delta")
    googleCovidTime.add_vline(
        x="2021-12-20", line_width=2, line_dash="solid", line_color="red", name="Omnicron")
    googleCovidTime.update_layout(
        title_text='Google Trends of Search "Covid" (Value Over Time)')
    googleCovidTime.update_xaxes(title_text='Time')
    googleCovidTime.update_yaxes(title_text='Google Trends')

    # Google Trends 'anxiety' Time Series
    googleAnxietyTime = go.Figure(
        [go.Scatter(x=data['week'], y=data['googleTrendsAnxietyValue'])])
    googleAnxietyTime.add_vline(
        x="2020-11-08", line_width=2, line_dash="solid", line_color="orange", name="Delta")
    googleAnxietyTime.add_vline(
        x="2021-12-20", line_width=2, line_dash="solid", line_color="red", name="Omnicron")
    googleAnxietyTime.update_layout(
        title_text='Google Trends of Search "Anxiety" (Value Over Time)')
    googleAnxietyTime.update_xaxes(title_text='Time')
    googleAnxietyTime.update_yaxes(title_text='Google Trends')

    # case switch for ticker values
    if ticker == "CDC Anxiety Value":
        return cdcAnxietyTime
    elif ticker == "Google Trends 'covid'":
        return googleCovidTime
    elif ticker == "Google Trends 'anxiety'":
        return googleAnxietyTime


@app.callback(
    Output("correlation-chart", "figure"),
    Input("correlation-ticker", "value"))
def display_correlation_chart(correlation_ticker):

    # Google Trends Covid VS Google Trends Anxiety
    covidVSanxiety = px.scatter(
        data, x="googleTrendsAnxietyValue", y="googleTrendsCovidValue",
        trendline="ols",
        trendline_color_override="red",
        hover_name="week",
        hover_data=["googleTrendsCovidValue",
                    "googleTrendsAnxietyValue", "cdcValue"],
        size_max=20,
        labels={"googleTrendsCovidValue": "Google Trends Covid",
                "googleTrendsAnxietyValue": "Google Trends Anxiety"},
        title="Google Trends Covid VS Google Trends Anxiety",)
    covidVSanxiety.update_layout(
        title_text='Google Trends Covid VS Google Trends Anxiety')
    covidVSanxiety.update_xaxes(title_text='Google Trends Anxiety')
    covidVSanxiety.update_yaxes(title_text='Google Trends Covid')

    # CDC VS Google Trends Covid
    cdcVScovid = px.scatter(
        data, x="googleTrendsCovidValue", y="cdcValue",
        trendline="ols",
        trendline_color_override="red",
        hover_name="week",
        hover_data=["googleTrendsCovidValue",
                    "googleTrendsAnxietyValue", "cdcValue"],
        size_max=20,
        labels={"googleTrendsCovidValue": "Google Trends Covid",
                "cdcValue": "CDC"},
        title="CDC VS Google Trends Covid",)
    cdcVScovid.update_layout(
        title_text='CDC VS Google Trends Covid')
    cdcVScovid.update_xaxes(title_text='Google Trends Covid')
    cdcVScovid.update_yaxes(title_text='CDC')

    # CDC VS Google Trends Anxiety
    cdcVSanxiety = px.scatter(
        data, x="googleTrendsAnxietyValue", y="cdcValue",
        trendline="ols",
        trendline_color_override="red",
        hover_name="week",
        hover_data=["googleTrendsCovidValue",
                    "googleTrendsAnxietyValue", "cdcValue"],
        size_max=20,
        labels={"googleTrendsAnxietyValue": "Google Trends Anxiety",
                "cdcValue": "CDC"},
        title="CDC VS Google Trends Anxiety",)
    cdcVSanxiety.update_layout(
        title_text='CDC VS Google Trends Anxiety')
    cdcVSanxiety.update_xaxes(title_text='Google Trends Anxiety')
    cdcVSanxiety.update_yaxes(title_text='CDC')

    # case switch for correlation-ticker values
    if correlation_ticker == "Google Trends Covid VS Google Trends Anxiety":
        return covidVSanxiety
    elif correlation_ticker == "CDC VS Google Trends Covid":
        return cdcVScovid
    elif correlation_ticker == "CDC VS Google Trends Anxiety":
        return cdcVSanxiety


@app.callback(
    Output("correlation-info", "children"),
    Input("correlation-ticker", "value"))
def display_correlation_info(correlation_ticker):

    covidVSanxiety = pearsonr(
        data['googleTrendsAnxietyValue'], data['googleTrendsCovidValue'])
    cdcVScovid = pearsonr(data['cdcValue'], data['googleTrendsCovidValue'])
    cdcVSanxiety = pearsonr(data['cdcValue'], data['googleTrendsAnxietyValue'])

    # case switch for correlation-ticker values
    if correlation_ticker == "Google Trends Covid VS Google Trends Anxiety":
        return "Correlation: " + str(format(covidVSanxiety[0], '.6f')) + "... " + "P-value: " + str(format(covidVSanxiety[1], '.6f'))
    elif correlation_ticker == "CDC VS Google Trends Covid":
        return "Correlation: " + str(format(cdcVScovid[0], '.6f')) + "... " + "P-value: " + str(format(cdcVScovid[1], '.6f'))
    elif correlation_ticker == "CDC VS Google Trends Anxiety":
        return "Correlation: " + str(format(cdcVSanxiety[0], '.6f')) + "... " + "P-value: " + str(format(cdcVSanxiety[1], '.6f'))


app.run_server(debug=True)
