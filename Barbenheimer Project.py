import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import plotly.express as px
sns.set_theme(style='darkgrid')

#importing google trends data on Barbie and Oppenheimer
df = pd.read_csv('/Users/erikrice/Downloads/Google Trends Barbenheimer Data - Sheet1 (2).csv')
print(df.head())
print(df.info())

#creating barbenheimer column
B_or_O = []
for x in df['Trend']:
    if x > 20: B_or_O.append('Oppenheimer')
    elif x == 20: B_or_O.append('Neutral')
    else: B_or_O.append('Barbie')
df['Barbie or Oppenheimer'] = B_or_O

#adding state codes for visualization
state_code_df = pd.read_csv('/Users/erikrice/Downloads/states.csv')
df = df.merge(state_code_df, on='State')
print(df.head())

#creating variable for visuals
Prefers_Barbie = df[df['Original Trend'] < 0]
Prefers_Barbie['Just Barbie'] = Prefers_Barbie['Original Trend'] + 20
Prefers_Oppenheimer = df[df['Original Trend'] > 0]
Prefers_Oppenheimer['Just Oppenheimer'] = Prefers_Oppenheimer['Original Trend']
bar_df = Prefers_Barbie.merge(Prefers_Oppenheimer, how='outer', on='State')

#cleaning tempoerary dataframe for visuals
bar_df[['Just Barbie', 'Just Oppenheimer']] = bar_df[['Just Barbie', 'Just Oppenheimer']].fillna(0)
bar_df.sort_values('State', inplace=True)
print(bar_df)

#creating some variables
font_color = '#525252'
hfont = {'fontname':'Calibri'}
facecolor = '#eaeaf2'
index = bar_df['State']
column0 = bar_df['Just Barbie']
column1 = bar_df['Just Oppenheimer']
title0 = 'Barbie Trending More'
title1 = 'Oppenheimer Trending More'

#visualizing the data
fig, axes = plt.subplots(figsize=(10,5), facecolor = facecolor, ncols=2, sharey=True)
fig.tight_layout()
axes[0].barh(index, column0, align='center', color='magenta', zorder=10)
axes[0].set_title(title0, fontsize=15, pad=15, color='magenta', **hfont) 
axes[1].barh(index, column1, align='center', color='dodgerblue', zorder=10)
axes[1].set_title(title1, fontsize=15, pad=15, color='dodgerblue', **hfont) 
axes[0].invert_xaxis()
plt.gca().invert_yaxis()
axes[0].set(yticks=index, yticklabels=index)
axes[0].yaxis.tick_left()
axes[0].tick_params(axis='y', colors='white')
axes[0].set_xticks([0, 5, 10, 15, 20])
axes[1].set_xticks([0, 5, 10, 15, 20])
for label in (axes[0].get_xticklabels() + axes[0].get_yticklabels()):
    label.set(fontsize=10, color=font_color, **hfont)
for label in (axes[1].get_xticklabels() + axes[1].get_yticklabels()):
    label.set(fontsize=10, color=font_color, **hfont)
plt.subplots_adjust(wspace=0, top=0.85, bottom=0.1, left=0.18, right=0.95)
plt.show()

#geomap of this central trend
fig = px.choropleth(df, locations='Abbreviation', locationmode="USA-states", scope="usa", color='Trend', color_continuous_scale="tealrose_r", range_color=(0, 40))
fig.update_layout(  title = 'What is Trending More: Barbie or Oppenheimer <br><sup>Source: Google Trends (7/15-7/22)</sup>', 
   title_x=0.5, 
   title_y=0.95, 
   title_font_size=28, 
   margin={"r":0,"t":0,"l":0,"b":0},coloraxis_colorbar=dict(
    ticks="outside",
    tickvals=[0,40],
    ticktext=["Barbie Trending More", "Oppenheimer Trending More"],
    dtick=2
))
fig.add_scattergeo(
    locations=df['Abbreviation'],
    locationmode="USA-states", 
    text=df['Abbreviation'],
    mode='text',
)
fig.show()

#importing 2020 state-by-state political spreadsheet
df_2020 = pd.read_csv('/Users/erikrice/Downloads/2020 Statewide Presidential Data - Sheet1 (1).csv')
print(df_2020.head())
print(df_2020.info())

#merging tables
df = df.merge(df_2020, on='State')
print(df.head())

#cleaning data
df['Democratic Popular Vote'] = df['Democratic Popular Vote'].str.replace(',', '')
df['Republican Popular Vote'] = df['Republican Popular Vote'].str.replace(',', '')
df.drop(['Democratic %', 'Republican %'], axis=1, inplace=True)
df['Democratic Electoral Vote'] = df['Democratic Electoral Vote'].str.replace('–', '0')
df['Republican Electoral Vote'] = df['Republican Electoral Vote'].str.replace('–', '0')
df[['Trend', 'Democratic Popular Vote', 'Democratic Electoral Vote', 'Republican Popular Vote', 'Republican Electoral Vote']] = df[['Trend', 'Democratic Popular Vote', 'Democratic Electoral Vote', 'Republican Popular Vote', 'Republican Electoral Vote']].astype(float)
print(df.head())

#creating red/blue state column
df['Net Political Bent'] = df['Democratic Electoral Vote'] - df['Republican Electoral Vote']
Red_or_Blue = []
for x in df['Net Political Bent']:
    if x > 0: Red_or_Blue.append('Blue State')
    elif x < 0: Red_or_Blue.append('Red State')
    else: Red_or_Blue.append('Tie')
df['Red or Blue'] = Red_or_Blue
print(df['Red or Blue'])

#converting new categorical columns to binary for analysis/charting
barbenheimer_binary1 = df['Barbie or Oppenheimer'].astype(str)
barbenheimer_binary1 = df['Barbie or Oppenheimer'].str.replace('Oppenheimer', '1')
barbenheimer_binary2 = barbenheimer_binary1.str.replace('Barbie', '0')
barbenheimer_binary3 = barbenheimer_binary2.str.replace('Neutral', '.5')
df['Barbie or Oppenheimer Numeric'] = barbenheimer_binary3.astype(float)
Red_or_Blue_Binary1 = df['Red or Blue'].astype(str)
Red_or_Blue_Binary1 = df['Red or Blue'].str.replace('Blue State', '1')
Red_or_Blue_Binary2 = Red_or_Blue_Binary1.str.replace('Red State', '0')
df['Red or Blue Numeric'] = Red_or_Blue_Binary2.astype(float)

#creating numeric dataframe
political_numeric = df[['Trend', 'Democratic Electoral Vote', 'Democratic Popular Vote', 'Republican Electoral Vote', 'Republican Popular Vote', 'Barbie or Oppenheimer Numeric', 'Red or Blue Numeric']]

#heatmap for correlation analysis. 
sns.heatmap(political_numeric.corr(), annot=True)
plt.show()

#visualizing this
sns.relplot(data=df, x='Abbreviation', y='Trend', hue='Red or Blue', palette='Set1')
plt.show()
#moderate correlation between Oppenheimer-preference and blue states.

#importing education data
education_df = pd.read_csv('/Users/erikrice/Downloads/State Education Data - Sheet1 (1).csv')
print(education_df.head())
print(education_df.info())

#merging into main dataframe
df = df.merge(education_df, on='State')
print(df.head())

#trend for the education indicators?
df['Education Rank'] = df['RANK']
df.drop(['RANK', 'Student Success', 'Student Safety', 'School Quality'], axis=1, inplace=True)
education_corr = df[['Trend', 'Education Rank']].corr()
print(education_corr)
#a low-to-moderate relationship between a preference for Oppenheimer and education rank

#what about crime rates?
crime_df = pd.read_csv('/Users/erikrice/Downloads/State Crime Data - Sheet1 (1).csv')
print(crime_df.head())
print(crime_df.info())

#cleaning crime data
crime_df['Crime Index ▲'] = crime_df['Crime Index ▲'].str.replace(',', '')
crime_df['Population'] = crime_df['Population'].str.replace(',', '')
crime_df['Crime Index ▲'] = crime_df['Crime Index ▲'].astype(float)
crime_df['Population'] = crime_df['Population'].astype(float)
crime_df['Safety Rank'] = crime_df['Rank']
crime_df['Crime Index'] = crime_df['Crime Index ▲']
crime_df['State Population'] = crime_df['Population']
crime_df = crime_df[['Safety Rank', 'Crime Index', 'State', 'State Population', 'Size Rank']]

#merging into main dataframe
df = df.merge(crime_df, on='State')
print(df.head())

#trend for the crime data?
crime_corr = df[['Trend', 'Safety Rank', 'Crime Index']].corr()
print(crime_corr)
#minor correlation, but Oppenheimer states have less crime. 

#what about state size?
population_corr = df[['Trend', 'State Population', 'Size Rank']].corr()
print(population_corr)
#no relationship at all.

#what about GDP by state?
gdp_df = pd.read_csv('/Users/erikrice/Downloads/State GDP Data 2023 - Sheet1 (2).csv')
print(gdp_df.head())
print(gdp_df.info())

#cleaning GDP data
gdp_df['Nominal GDP'] = gdp_df['Nominal GDP'].str.replace(',', '')
gdp_df['GDP Per Capita'] = gdp_df['GDP Per Capita'].str.replace(',', '')
gdp_df['GDP Per Capita'] = gdp_df['GDP Per Capita'].str.replace('$', '')
gdp_df['State'] = gdp_df['State or Territory']
gdp_df['State'] = gdp_df['State'].str.replace(' *', '')
gdp_df['Nominal GDP'] = gdp_df['Nominal GDP'].astype(float)
gdp_df['GDP Per Capita'] = gdp_df['GDP Per Capita'].astype(float)
gdp_df = gdp_df[['State', 'Nominal GDP', 'GDP Per Capita', 'GDP Per Capita Rank', 'Inverted GDP Rank']]
print(gdp_df.head())

#merging into main dataframe
df = df.merge(gdp_df, on='State')
print(df.head())

#trend with the GDP data?
gdp_corr = df[['Trend', 'Nominal GDP', 'GDP Per Capita', 'GDP Per Capita Rank']].corr()
print(gdp_corr)
#moderate correlation between Oppenheimer preference and higher GDP per capita

#final indicator: happiness by state
happiness_df = pd.read_csv('/Users/erikrice/Downloads/happiest-states-2023 - happiest-states-2023.csv (1).csv')
print(happiness_df.head())
print(happiness_df.info())

#quick clean
happiness_df['State'] = happiness_df['state']
happiness_df['Happiness Score'] = happiness_df['totalScore']
happiness_df = happiness_df[['State', 'Happiness Score', 'Happiness Rank', 'Inverted Happiness Rank']]

#merging into main dataframe one last time
df = df.merge(happiness_df, on='State')
print(df.head())

#any relationship?
happiness_corr = df[['Trend', 'Happiness Score', 'Happiness Rank']].corr()
print(happiness_corr)

#calculations for visual of these major indicators compared to central categorical variable
Prefers_Barbie2 = df[df['Barbie or Oppenheimer'] == 'Barbie']
Prefers_Oppenheimer2 = df[df['Barbie or Oppenheimer'] == 'Oppenheimer']
Barbie_Mean = Prefers_Barbie2[['Education Rank', 'Safety Rank', 'Size Rank', 'GDP Per Capita Rank', 'Happiness Rank']].mean()
print(Barbie_Mean)
Oppenheimer_Mean = Prefers_Oppenheimer2[['Education Rank', 'Safety Rank', 'Size Rank', 'GDP Per Capita Rank', 'Happiness Rank']].mean()
print(Oppenheimer_Mean)

#visual of all these indicators together compared to main categorical variable
x1 = ['Barbie', 'Oppenheimer']
y1 = [34.65, 19.36]
y2 = [32.9, 19.82]
y3 = [22.45, 26.59]
y4 = [35.45, 18.82]
y5 = [31.5, 18.73]
chart3 = pd.DataFrame(np.c_[y1, y2, y3, y4, y5], index=x1)
chart3.plot.bar(color=['tab:brown', 'tab:pink', 'tab:gray', 'tab:olive', 'tab:cyan'])
plt.legend(['Education Rank', 'Safety Rank', 'Population Rank', 'GDP Rank', 'Happiness Rank'])
plt.ylabel("Mean State Rank")
plt.xticks(rotation=45)
plt.title('Barbenheimer Trends Compared to State Indicators')
plt.show()

#setting Barbenheimer aside for a moment, let's see a bubbleplot with several core state indicators
#I made inverted columns in Excel for *each* of these rankings so the chart (directionally and proportionally) would be intuitive
df['GDP Bubble'] = df['Inverted GDP Rank'] * 75
x = df['Inverted Education Rank']
y = df['Inverted Happiness Rank']
c = df['Safety Rank']
s = df['GDP Bubble']
fig, ax = plt.subplots()
scatter = ax.scatter(x, y, c=c, s=s)
legend1 = ax.legend(*scatter.legend_elements(),
                    loc="lower left", title="Crime")
ax.add_artist(legend1)
handles, labels = scatter.legend_elements(prop="sizes", alpha=0.6)
legend2 = ax.legend(handles, labels, loc="upper right", title="GDP Per Capita", labelspacing=2, bbox_to_anchor=(1.125, 1))
plt.xlabel('Education')
plt.ylabel('Happiness')
plt.title('Interstate Correlation Analysis: Education/Crime/GDP/Happiness Indicators')
plt.show()

#lets have a look at all these indicators together
print(df.columns)
final_df = df[['Trend', 'Democratic Electoral Vote', 'Republican Electoral Vote', 'Democratic Popular Vote', 'Republican Popular Vote', 'Barbie or Oppenheimer Numeric', 'Red or Blue Numeric', 'Education Rank', 'Safety Rank', 'Size Rank', 'GDP Per Capita Rank', 'Happiness Rank']]
sns.heatmap(final_df.corr(), annot=True, cmap="YlGnBu")
plt.show()