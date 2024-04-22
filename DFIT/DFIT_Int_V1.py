import dash, math
import pandas as pd
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import dash_html_components as html
import dash_core_components as dcc
from dash.dependencies import Input,Output
from tkinter import *
from tkinter import filedialog
##########################################Functions

def Ave(Input_Array,n):###################Smoothing function
    y=[0]
    i=0
    while i<len(Input_Array)-1:
        x=0
        k=0
        j=-n+1
        while j<n:
            if i+j<=1:
                z=1
            else:
                if i+j >= len(Input_Array)-1:
                    z=-1
                else:
                    z=i+j
            x+=Input_Array[z]
            k+=1
            j+=1
        y.append(x/(2*n-1))
        i+=1
    return y

def Extract():   #########################Extraxt data
    global P_Inj
    global EndInj
    global Inj_Total
    global dt_Shut
    global Prs_Shut

    dt_Shut = []
    Prs_Shut = []
    P_Inj = Pressure[0]  # Pressure at first of Injection
    i = 0
    x = 0
    while i < len(Time) - 1:  # Cumulative calculation
        i += 1
        x = Rate[i] * (Time[i] - Time[i - 1]) * 60 + x
        if Rate[i] == 0:
            EndInj = Time[i - 1]  # Shut-in time
            Inj_Total = x
            break
    dt_Shut.append(Time[i] - EndInj)
    Prs_Shut.append(Pressure[i])
    Last_Prs = Prs_Shut[0]
    while i < len(Time) - 1:  # Shut-in data
        i += 1
        if Last_Prs - Pressure[i] > Res_Pres_Inc:
            dt_Shut.append(Time[i] - EndInj)
            Prs_Shut.append(Pressure[i])
            Last_Prs = Pressure[i]


def G_Function(): ########################G Function Callulation
    global Slope, P_res
    global G_Time
    global max_dpdg, T_max_dpdg, G_max_dpdg, P_max_dpdg
    global min_dpdg, T_min_dpdg, G_min_dpdg, P_min_dpdg
    global ISIP
    global dpdt_1_2, dpdt_1
    global dp_dg_1, gdp_dg_1, dpdg, gdpdg
    global dp, dtd,log_dt, t_1_2, t_1, dp_dt, tdp_dt, log_tdpdt
    global P_ISIP, Flow
    global x1,x2
    global ShminT
    
    G_Time=[]
    dp=[]
    dtd=[]
    dp_dg_1 = [0]
    gdp_dg_1 = [0]
    log_dt=[0]
    t_1_2=[0]
    t_1 =[0]
    dp_dt=[0]
    tdp_dt=[0]
    log_tdpdt=[0]
    P_ISIP=[0]
    Flow=[0]

    i = 0
    while i <= len(dt_Shut) - 1:
        dp.append(Prs_Shut[0] - Prs_Shut[i])
        dtd.append(dt_Shut[i] / EndInj)
        G_Time.append(4 / 3.14159 * 4 / 3 * ((1 + dtd[i]) ** 1.5 - dtd[i] ** 1.5 - 1))
        log_dt.append(math.log10(dt_Shut[i]))
        t_1_2.append(dt_Shut[i] ** (-1 / 2))
        t_1.append(dt_Shut[i] ** (-1))
        i += 1
    i = 1

    while i <= len(dt_Shut) - 2:
        dp_dg_1.append(-(Prs_Shut[i + 1] - Prs_Shut[i - 1]) / (G_Time[i + 1] - G_Time[i - 1]))
        gdp_dg_1.append(G_Time[i] * dp_dg_1[i])
        dp_dt.append(-(Prs_Shut[i + 1] - Prs_Shut[i - 1]) / (dt_Shut[i + 1] - dt_Shut[i - 1]))
        tdp_dt.append(dt_Shut[i] * dp_dt[i])
        log_tdpdt.append(math.log10(tdp_dt[i]))
        i += 1

    ######################################Smoothing Trend (Middle Moving Average)
    dpdg = Ave(dp_dg_1, 7)
    gdpdg = Ave(gdp_dg_1, 7)


    Draft = 5
    Slope = (log_tdpdt[-Draft] - log_tdpdt[-Draft * 2]) / (log_dt[-Draft] - log_dt[-Draft * 2])
    dpdt_1_2 = (Prs_Shut[-Draft] - Prs_Shut[-1]) / (t_1_2[-Draft] - t_1_2[-1])
    dpdt_1 = (Prs_Shut[-Draft] - Prs_Shut[-1]) / (t_1[-Draft] - t_1[-1])
    if Slope > -0.75:
        P_res = -dpdt_1_2 * t_1_2[-Draft] + Prs_Shut[-Draft]
    else:
        P_res = -dpdt_1 * t_1[-Draft] + Prs_Shut[-Draft]
    # ''''''''''''''''Finding ISP
    j = 1
    while dp_dg_1[-j] < dp_dg_1[-j - 1]:
        j += 1
    i = len(dt_Shut) - j - 1
    max_dpdg = dp_dg_1[i]
    P_max_dpdg = Prs_Shut[i]
    G_max_dpdg = G_Time[i]
    T_max_dpdg = dt_Shut[i]
    while dp_dg_1[-j] > dp_dg_1[-j - 1]:
        j += 1
    i = len(dt_Shut) - j - 1
    x1=i
    min_dpdg = dp_dg_1[i]
    P_min_dpdg = Prs_Shut[i]
    G_min_dpdg = G_Time[i]
    T_min_dpdg = dt_Shut[i]
    ISIP = P_min_dpdg + min_dpdg * G_min_dpdg
    i = 1
    P_ISIP.append([])
    Flow.append([])
    while i < len(dt_Shut) - 1:
        P_ISIP.append(Prs_Shut[i] - ISIP)
        Flow.append(WSC * dp_dt[i] / 60)
        i += 1


    i=1
    while gdp_dg_1[-i-1]>gdp_dg_1[-i]:
        i+=1
    Flag=True
    while Flag:
        if gdp_dg_1[-i]<G_Time[-i]*(gdp_dg_1[-i]-gdp_dg_1[-i-1])/(G_Time[-i]-G_Time[-i-1]):
            Flag=False
            i-=1
        i+=1
    ShminT=Prs_Shut [-i-1]
    x2=len(G_Time) -i-1

def H_Function():  ######################H_Fuction calculation
    global h_Shut, h_Peak, Eff_Prs,h_fun, Stiff

    Eff_Prs=[]
    Matrix=[]
    Term1=[]
    h_fun=[]
    Stiff=[0]

    i=0
    while i<len(dt_Shut):
        if dt_Shut[i]<T_min_dpdg:
            Eff_Prs.append(P_min_dpdg + (G_min_dpdg - G_Time[i]) * min_dpdg)
        else:
            Eff_Prs.append(Prs_Shut[i])
        Sum=float(0)
        j=1
        while j < len(dt_Shut):
            if dt_Shut[j] < dt_Shut[i]:
                x=(Eff_Prs[j] - Eff_Prs[j - 1]) * (dt_Shut[i] - dt_Shut[j]) ** 0.5
                Sum += x
                j += 1
            else:
                break
        Matrix.append(Sum)
        i += 1
    i=0
    while i<len(dt_Shut):
        Term1.append((Eff_Prs[0] - P_res) * (EndInj * 0.5 + dt_Shut[i]) ** 0.5)
        h_fun.append(Term1[i] + Matrix[i])
        if dt_Shut[i]==T_max_dpdg:
            h_Peak=h_fun[i]
        i+=1
    h_Shut=h_fun[0]
    i=1
    Stiff.append([])
    while i<len(dt_Shut)-1:
        Stiff.append(-(Eff_Prs[i+1] - Eff_Prs[i-1]) / (h_fun[i+1] - h_fun[i-1]))
        i+=1


############################################################################################################################
############################################################################################################################
##########################################Main Body

root=Tk()
root.title('Open CSV files')

##########################################import raw data
root.filename=filedialog.askopenfilename(initialdir='CSV/',
                                         initialfile='Raw_Data.csv',
                                         title='Open raw data',
                                         filetype=(('CSV file','*.CSV' ),('Text File','*.txt'),('All files','*.*'))
                                         )
df=pd.read_csv(root.filename)
i=0
for column in df.columns:
    if i==0:
        Time=df[column].tolist()
    else:
        if i==1:
            Pressure=df[column].tolist()
        else:
            Rate=df[column].tolist()
    i+=1

##########################################import raw data
root.filename=filedialog.askopenfilename(initialfile='Parameters.csv',
                                         title='Import parameters',
                                         filetype=(('CSV file','*.CSV' ),('Text File','*.txt'),('All files','*.*'))
                                         )
df=pd.read_csv(root.filename)
Young =df['Value'][0]
Poisson=df['Value'][1]
Poro =df['Value'][2]
Comp=df['Value'][3]
Fluid_Com=df['Value'][4]
Fluid_Vis=df['Value'][5]
Res_Pres_Inc=df['Value'][6]
Frac_h=df['Value'][7]
WSC=df['Value'][8]
Inj_Total=df['Value'][9]


Extract()

G_Function()

app=dash.Dash(__name__)
app.layout=html.Div([
    html.H1(children='Series Data'),

    html.Div(children='dp/dg slider'),
    dcc.Slider(
        id='dp_dg',
        min=1,
        max=len(G_Time),
        value=x1
    ),
    html.Div(children='Please select desired curve:'),
    dcc.Dropdown(
        id='DD_Curve',
        options=[
            {'label':'Original curve','value':'Original'},
            {'label':'Smoothed curve','value':'Smoothed'}
        ],
        value='Original',
        style={'width':'40%'}
    ),
    html.Div(children='  '),

    html.Div(children='Charts'),
    dcc.Graph(
        id="Graph",
        figure={}
    ),


    html.Div(children='G*dp/dg Tangent Line'),
    dcc.Slider(
        id='Tangent',
        min=1,
        max=len(G_Time),
        value=x2+1
    ),

    html.Div(children=['Vertical Line']),
    dcc.Slider(
        id='vertical',
        min=1,
        max=len(G_Time),
        value=x2
    ),

    html.Div(id='ShC',children=[]),
    html.Div(id='ShT',children=[]),
    html.Div(id='ISIP',children=[])
])

@app.callback(
    [Output(component_id='Graph',component_property='figure'),
     Output(component_id='ShC',component_property='children'),
     Output(component_id='ShT',component_property='children'),
     Output(component_id='ISIP',component_property='children')],
    [Input(component_id='dp_dg',component_property='value'),
     Input(component_id='Tangent',component_property='value'),
     Input(component_id='vertical',component_property='value'),
     Input(component_id='DD_Curve',component_property='value')]
)
def Update_Graph(G, Slope, Ver, Fit):
    global pg,gpg

    max_G=G_max_dpdg*1.5
    max_gdpdg=max(gdp_dg_1)*1.1
    max_dp=max_dpdg*1.5

    fig1=make_subplots(rows=1,cols=2,
                       specs= [[{'secondary_y':True},{'secondary_y':True}]]
                       )
    fig1.add_trace(
        go.Scatter(x=G_Time,y=Prs_Shut,name='Pressure',line=dict(color='blue')),
        secondary_y=False,row=1,col=1
    )
    fig1.add_trace(
        go.Scatter(x=G_Time[:-1],y=dp_dg_1,name='dp/dg',line=dict(color='red')),
        secondary_y=True,row=1,col=1
    )
    fig1.add_trace(
        go.Scatter(x=G_Time[:-1], y=dpdg, name='dp/dg smoothed', line=dict(color='red',dash='dot')),
        secondary_y=True, row=1, col=1
    )
    fig1.add_trace(
        go.Scatter(x=[G_Time[G],G_Time[G]],y=[0,100],name='Min',line=dict(color='black',dash='dash')),
        secondary_y=True,row=1,col=1
    )
    fig1.add_trace(
        go.Scatter(x=G_Time,y=Prs_Shut,name='Pressure',line=dict(color='blue')),
        secondary_y=False,row=1,col=2
    )
    fig1.add_trace(
        go.Scatter(x=G_Time[:-1],y=gdp_dg_1,name='G*dp/dg',line=dict(color='green')),
        secondary_y=True,row=1,col=2
    )
    fig1.add_trace(
        go.Scatter(x=G_Time[:-1], y=gdpdg, name='G*dp/dg smoothed', line=dict(color='green',dash='dot')),
        secondary_y=True, row=1, col=2
    )
    fig1.add_trace(
        go.Scatter(x=[0,G_Time[Slope]],y=[0,max_gdpdg],name='Tangent',line=dict(color='black',dash='dot')),
        secondary_y=True,row=1,col=2
    )
    fig1.add_trace(
        go.Scatter(x=[G_Time[Ver], G_Time[Ver]], y=[0, max_gdpdg], name='Vertical',line=dict(color='grey', dash='dash')),
        secondary_y=True, row=1, col=2
    )
    fig1.update_xaxes(title_text='G-Function', row=1, col=1,range=[0,max_G])
    fig1.update_yaxes(title_text="Pressure", secondary_y=False, row=1,col=1)
    fig1.update_yaxes(title_text="dp/dg", secondary_y=True,row=1,col=1,range=[0,max_dp])
    fig1.update_xaxes(title_text='G-Function',row=1,col=2,range=[0,max_G])
    fig1.update_yaxes(title_text='Pressure',secondary_y=False,row=1,col=2)
    fig1.update_yaxes(title_text='G*dp/dg',secondary_y=True,row=1,col=2)

    ShC='Minimum Principle Stress (Compliance) is: ',Prs_Shut[G]-75.0
    ShT='Minimum Principle Stress (Tangent) is: ',Prs_Shut[Ver]
    if Fit=='Original':
        pg=dp_dg_1
        gpg=gdp_dg_1
    else:
        pg=dpdg
        gpg=gdpdg
    ISIP = 'The effective ISIP is: ', Prs_Shut[G] + pg[G] * G_Time[G]
    min_dpdg = pg[G]
    P_min_dpdg = Prs_Shut[G]
    G_min_dpdg = G_Time[G]
    T_min_dpdg = dt_Shut[G]

    H_Function()

    return fig1,ShC, ShT, ISIP


app.run_server()