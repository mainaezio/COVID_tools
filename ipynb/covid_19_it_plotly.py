import pandas as pd

import plotly.graph_objects as go


def plot_COVID(region: str, *args):
    """
    args is a tuple of column names to be plotted
    e.g
    plot_COVID("Piemonte",'totale_casi','deceduti')
    will plot the overall daily results for 'totale_casi','deceduti' in Piemonte
    
    Additional columns 'nuovi_casi', 'decessi_giorno', 'ricoveri_ICU_giorno' have been introduced.
    Daily data use dashed lines. Cumulative data use continuous lines.
    'Alto Adige' combines P.A. Bolzano and P.A. Trento.
    """

# The keys of the dictionary 'col' are the vailable columns (strings). The values are the colors for plotting 
    col={'ricoverati_con_sintomi':'C8',
         'nuovi_ricoverati_con_sintomi':'C8',
         'terapia_intensiva':'red',
         'nuovi_terapia_intensiva':'red',
         'totale_ospedalizzati':'C2',
         'isolamento_domiciliare':'C1',
         'totale_attualmente_positivi':'C4',
         'nuovi_attualmente_positivi':'C5',
         'dimessi_guariti':'green',
         'nuovi_dimessi_guariti':'green',
         'deceduti':'C0',
         'nuovi_deceduti':'C0',
         'tamponi':'C6',
         'nuovi_tamponi':'C6',
         'totale_casi':'0',
         'nuovi_casi':'0'}
    
# Load the data from the official repository. Notice that you need to download the file in 'raw' format non in html.
# The output is a pandas Dataframe.
    if region=='Italia':
        TotalByDate=pd.read_csv("https://raw.githubusercontent.com/pcm-dpc/COVID-19/master/dati-andamento-nazionale/dpc-covid19-ita-andamento-nazionale.csv")
    else:
        TotalByDate=pd.read_csv("https://raw.githubusercontent.com/pcm-dpc/COVID-19/master/dati-regioni/dpc-covid19-ita-regioni.csv")
        if region=='Alto Adige':
# Dataframe for 'Alto Adige' is the sum of 'P.A. Bolzano' and 'P.A. Trento'
            TotalByDate1=TotalByDate.loc[lambda df: df['denominazione_regione']=='P.A. Bolzano',:]
            TotalByDate2=TotalByDate.loc[lambda df: df['denominazione_regione']=='P.A. Trento',:]
            TotalByDate=TotalByDate1.add(TotalByDate1)
            TotalByDate['denominazione_regione']=['Alto Adige' for i in range(len(TotalByDate))]
            TotalByDate['data']=TotalByDate1['data']
        else:
            TotalByDate=TotalByDate.loc[lambda df: df['denominazione_regione']==region,:]
# fix indices to be [0,1,.........,len(TotalByDate)-1]
        TotalByDate['entry']=list(range(len(TotalByDate)))
        TotalByDate.set_index('entry',inplace=True)


# Drop some unused columns
#    print(TotalByDate.columns)
    TotalByDate=TotalByDate.drop(columns=['stato','note_it','note_en'])
#    print(TotalByDate)

# Add columns 'nuovi_casi', 'nuovi_decessi_giorno', 'nuovi_terapia_intensiva',
#             'nuovi_dimessi_guariti'
    daily=['nuovi_casi','nuovi_deceduti','nuovi_terapia_intensiva','nuovi_dimessi_guariti',
          'nuovi_tamponi','nuovi_ricoverati_con_sintomi']
    TotalByDate['nuovi_casi']=[0]+[TotalByDate['totale_casi'][i]-TotalByDate['totale_casi'][i-1] for i in range(1,len(TotalByDate))]
    TotalByDate['nuovi_deceduti']=[0]+[TotalByDate['deceduti'][i]-TotalByDate['deceduti'][i-1] for i in range(1,len(TotalByDate))]
    TotalByDate['nuovi_terapia_intensiva']=[0]+[TotalByDate['terapia_intensiva'][i]-TotalByDate['terapia_intensiva'][i-1] for i in range(1,len(TotalByDate))]
    TotalByDate['nuovi_dimessi_guariti']=[0]+[TotalByDate['dimessi_guariti'][i]-TotalByDate['dimessi_guariti'][i-1] for i in range(1,len(TotalByDate))]
    TotalByDate['nuovi_tamponi']=[0]+[TotalByDate['tamponi'][i]-TotalByDate['tamponi'][i-1] for i in range(1,len(TotalByDate))]
    TotalByDate['nuovi_ricoverati_con_sintomi']=[0]+[TotalByDate['ricoverati_con_sintomi'][i]-TotalByDate['ricoverati_con_sintomi'][i-1] for i in range(1,len(TotalByDate))]
                                                     

# Format dates
    xx=list(TotalByDate['data'])
    xx=[d[5:10].replace('02-','Feb ').replace('03-','Mar ')  for d in xx]
    TotalByDate['data']=xx

# Set and Format title
    my_title=region+" "+xx[0]+"-"+xx[-1]

# Create the figure object
    fig = go.Figure()



    for name in args:
        yy=list(TotalByDate[name])
        fig.add_scatter(x=xx,y=yy, mode="lines+markers", name=name)


    fig.update_xaxes( # the x-axis labels are rotated
        tickangle=50
    )

    fig.update_yaxes(type='log')

    fig.update_layout( # customize font and legend orientation & position
        font_family="Rockwell",
        width=700,height=800,
        title=dict(text=my_title, x=0.5, xanchor="center", font_size=30),
        xaxis_title="",
        yaxis_title="numero di casi",
#        font=dict(
#            family="Courier New, monospace",
#            size=18,
#            color="#7f7f7f"
#        ),
    )

    if region in ['Italia','Lombardia']:
        fig.update_layout(
            legend=dict(
                   title=None, orientation="h", y=0.03, yanchor="bottom", x=0.63, xanchor="center",
                       ),
            )
    else:
        fig.update_layout(
            legend=dict(
                   title=None, orientation="v", y=0.99, yanchor="top", x=0.01, xanchor="left",
                       ),
            )


#    fig.show()

    counts=my_title.count(' ')
    my_title=my_title.replace(' ','_',counts)

#    fig.write_html("html/"+my_title+".html",config=dict(include_plotlyjs="directory",file="html/plotly.min.js",full_html=True))
    fig.write_html("html/"+my_title+".html")
    fig.write_image("images/"+my_title+".jpg")

    return


def plot_COVID_all(*args):
    regions=['Italia','Abruzzo','Alto Adige','Basilicata','Calabria','Campania','Emilia Romagna','Friuli Venezia Giulia',
            'Lazio','Liguria','Lombardia','Marche','Molise','Piemonte','Puglia','Sardegna','Sicilia',
            'Toscana','Umbria','Valle d\'Aosta','Veneto']
    
    for region in regions:
        print('region:',region)
        plot_COVID(region,*args)
    
    return


#plot_COVID('Veneto','totale_casi','nuovi_casi','terapia_intensiva','nuovi_terapia_intensiva',
#               'deceduti','nuovi_deceduti','tamponi')

#plot_COVID('Italia','totale_casi')

plot_COVID_all('totale_casi','nuovi_casi','terapia_intensiva','nuovi_terapia_intensiva',
               'deceduti','nuovi_deceduti','tamponi')







