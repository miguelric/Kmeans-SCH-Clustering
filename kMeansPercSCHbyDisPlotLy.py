import pandas as pd                                             # inport libraries
from sklearn.cluster import KMeans
from kneed import KneeLocator
import plotly.express as px
import plotly.graph_objects as go
import plotly.figure_factory as ff

data = pd.read_csv(r"schPercByDis.csv")                         # input csv


print("\n\nClustering\n-------------------")                    # prompt for specific discipline
initial = input("\nDo you want a specific discipline?\n")
if initial.upper() == "YES":
    disciplineAns = input("\nWhich discipline?\n")
    data = data.loc[data["Discipline"] == disciplineAns]


utsaDF = data.loc[data["FICE"] == 10115]                        # make two separate df (one for utsa, one for without)
data = data.loc[data["FICE"] != 10115]


maxClusters = 7                                                 # perform WCSS to find elbow
wcss=[]
x = data.iloc[:,4:5]                                            # separate numeric cols we want to cluster for algorithm
for i in range(1,maxClusters):
    kmeans = KMeans(i)
    kmeans.fit(x)
    wcss_iter = kmeans.inertia_
    wcss.append(wcss_iter)
number_clusters = range(1,maxClusters)
kneedle = KneeLocator(number_clusters, wcss, curve="convex", direction="decreasing")

def plotElbow():
    fig = px.line(x=number_clusters, y=wcss)
    fig.show()
# plotElbow()


                                    
kmeans = KMeans(kneedle.knee)                                   # perform kmeans on data
kmeans.fit(x)
data_with_clusters = data.copy()
data_with_clusters['Clusters'] = kmeans.fit_predict(x) 


def plotScatter():
    fig = px.scatter(data_with_clusters, x="Percentage of SCH", y="Total SCH" , color = "Clusters" , hover_name = "Institution", hover_data=["Discipline"]  ,  symbol_sequence = ['circle'] )
    fig.update_traces(marker=dict(size=12, line=dict(width=2, color='DarkSlateGrey'),  opacity=0.7), selector=dict(mode='markers'))

    utsaFig = px.scatter(utsaDF, x="Percentage of SCH", y="Total SCH" , color_discrete_sequence=['red'], hover_name = "Institution", hover_data=["Discipline"], symbol_sequence = ['circle'] )
    utsaFig.update_traces(marker=dict(size=12, line=dict(width=2, color='DarkSlateGrey')), selector=dict(mode='markers'))


    finalScatter = go.Figure(data=fig.data + utsaFig.data)          # combine figs


    finalScatter.update(layout_coloraxis_showscale=False)           # remove bar on right
    finalScatter.update_layout(xaxis_tickformat = '.2%')            # adjust x axis tick labels to include % and 2 decimals
    finalScatter.update_xaxes(title="Percentage of SCH" )           # adjust x axis titles
    finalScatter.update_yaxes(title="Total SCH")                    # adjust y axis titles

    # adjust title
    if initial.upper() == "YES":                                    # change title to discipline
        finalScatter.update_layout( title=disciplineAns)
        finalScatter.update_layout(title={  'y':0.95,
                                    'x':0.5,
                                    'xanchor': 'center',
                                    'yanchor': 'top'    },
                                    font=dict(
                                    family="Times New Roman",
                                    size=22,
                                    color="Black" ) )
    else:                                                           # change title to default
        finalScatter.update_layout(title="All Disciplines")
        finalScatter.update_layout(
        title={ 'y':0.95,
                'x':0.5,
                'xanchor': 'center',
                'yanchor': 'top'    },
                font=dict(
                family="Times New Roman",
                size=22,
                color="Black" ) )
            


    finalScatter.show()

plotScatter()

def plotTable(data_with_clusters):
    # rename and reorder columns 
    data_with_clusters['Percent of SCH'] = data_with_clusters['Percentage of SCH']                              
    data_with_clusters['Clusters '] = data_with_clusters['Clusters']
    data_with_clusters = data_with_clusters.drop(columns=['FICE', 'Total SCH', 'Percentage of SCH', 'Clusters'])

    # if there is a specific discipline chosen then drop the discipline col since itll be the title
    if initial.upper() == "YES":
        data_with_clusters = data_with_clusters.drop(columns=['Discipline'])


    # sort by Clusters col
    data_with_clusters = data_with_clusters.sort_values(by=['Clusters '])
    # data_with_clusters['Percent of SCH'] = data_with_clusters['Percent of SCH']*100                                     # format
    data_with_clusters['Percent of SCH'] = (data_with_clusters['Percent of SCH']*100).map('{:,.2f}%'.format)                  # format %



    tableFig =  ff.create_table(data_with_clusters)

    # adjust title
    if initial.upper() == "YES":                # change title to discipline
        tableFig.update_layout(title_text = disciplineAns)
        tableFig.update_layout({'margin':{'t':50}})
    else:                                       # change title to default
        tableFig.update_layout(title_text = "All Disciplines")
        tableFig.update_layout({'margin':{'t':50}})

    # change font and size
    tableFig.update_layout(font=dict(family="Calibri",
                                    size=18,
                                    color="Black"))


    tableFig.show()

plotTable(data_with_clusters)


# if discpline is selected then
# for table
# show only cluster wehre utsa lies 



print("Script Complete")