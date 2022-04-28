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
        id="correlation-ticker1",
        options=["CDC", "Google Trends Covid",
                 "Google Trends Anxiety"],
        value="CDC",
        clearable=False,
    ),
    html.P("VS"),
    dcc.Dropdown(
        id="correlation-ticker2",
        options=["CDC", "Google Trends Covid",
                 "Google Trends Anxiety"],
        value="Google Trends Covid",
        clearable=False,
    ),
])


@app.callback(
    Output("time-series-chart", "figure"),
    Input("ticker", "value"))
def display_time_series(ticker):

    # case switch for ticker values
    if ticker == "CDC Anxiety Value":
        axisData = data['cdcValue']
        title = 'CDC Sentiment Analysis (Anxiety Over Time)'
        axisTitle = 'CDC Value'
    elif ticker == "Google Trends 'covid'":
        axisData = data['googleTrendsCovidValue']
        title = 'Google Trends of Search "Covid" (Value Over Time)'
        axisTitle = 'Google Trends'
    elif ticker == "Google Trends 'anxiety'":
        axisData = data['googleTrendsAnxietyValue']
        title = 'Google Trends of Search "Anxiety" (Value Over Time)'
        axisTitle = 'Google Trends'

    # Time Series Chart
    fig = go.Figure([go.Scatter(
        x=data['week'], y=axisData, name='CDC Anxiety National Estimate')])
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

    return fig


@app.callback(
    Output("correlation-chart", "figure"),
    Input("correlation-ticker1", "value"),
    Input("correlation-ticker2", "value"))
def display_correlation_chart(correlation_ticker1, correlation_ticker2):

    # case switch for correlation-ticker values
    if correlation_ticker1 == "CDC":
        x = 'cdcValue'
        xTitle = 'CDC Value'
    elif correlation_ticker1 == "Google Trends Covid":
        x = 'googleTrendsCovidValue'
        xTitle = 'Google Trends Covid'
    elif correlation_ticker1 == "Google Trends Anxiety":
        x = 'googleTrendsAnxietyValue'
        xTitle = 'Google Trends Anxiety'

    # case switch for correlation-ticker2 values
    if correlation_ticker2 == "CDC":
        y = 'cdcValue'
        yTitle = 'CDC Value'
    elif correlation_ticker2 == "Google Trends Covid":
        y = 'googleTrendsCovidValue'
        yTitle = 'Google Trends Covid'
    elif correlation_ticker2 == "Google Trends Anxiety":
        y = 'googleTrendsAnxietyValue'
        yTitle = 'Google Trends Anxiety'

    # Google Trends Covid VS Google Trends Anxiety
    fig = px.scatter(
        data, x=x, y=y,
        trendline="ols",
        trendline_color_override="red",
        hover_name="week",
        hover_data=["googleTrendsCovidValue",
                    "googleTrendsAnxietyValue", "cdcValue"],
        size_max=20,
        labels={x: xTitle,
                y: yTitle},
        title=xTitle + " VS " + yTitle,)
    fig.update_layout(
        title_text=xTitle + " VS " + yTitle)
    fig.update_xaxes(title_text=xTitle)
    fig.update_yaxes(title_text=yTitle)

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

    return fig


@app.callback(
    Output("correlation-info", "children"),
    Input("correlation-ticker1", "value"),
    Input("correlation-ticker2", "value"))
def display_correlation_info(correlation_ticker1, correlation_ticker2):

    # case switch for correlation-ticker values
    if correlation_ticker1 == "CDC":
        x = 'cdcValue'
    elif correlation_ticker1 == "Google Trends Covid":
        x = 'googleTrendsCovidValue'
    elif correlation_ticker1 == "Google Trends Anxiety":
        x = 'googleTrendsAnxietyValue'

    # case switch for correlation-ticker2 values
    if correlation_ticker2 == "CDC":
        y = 'cdcValue'
    elif correlation_ticker2 == "Google Trends Covid":
        y = 'googleTrendsCovidValue'
    elif correlation_ticker2 == "Google Trends Anxiety":
        y = 'googleTrendsAnxietyValue'

    corr = pearsonr(data[x], data[y])

    return "Correlation: " + str(format(corr[0], '.6f')) + "... " + "P-value: " + str(format(corr[1], '.6f'))


app.run_server(debug=True)
