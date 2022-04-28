import plotly.graph_objects as go
import pandas as pd

df = pd.read_csv('./data/cdcAnxiety_googleCovid_COMBINED.csv')
# df = pd.read_csv('./data/cdcAnxiety_googleCovid_COMBINED_withMissing.csv')


fig = go.Figure([go.Scatter(x=df['week'], y=df['cdcValue'])])

# fig.update_layout(
#     title_text='Google Trends of Search "Covid" (Value Over Time)')
# fig.update_xaxes(title_text='Time')
# fig.update_yaxes(title_text='Google Trends')

# fig.show()

fig.update_layout(
    title_text='CDC Sentiment Analysis (Anxiety Over Time)')
fig.update_xaxes(title_text='Time')
fig.update_yaxes(title_text='CDC Value')

fig.show()
