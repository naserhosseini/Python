import math, csv
import pandas as pd
import plotly.graph_objects as go
import plotly.express as px
import numpy as np
from plotly.subplots import make_subplots
import dash
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
    global P_Inj, dt_Shut, Prs_Shut, Cum

    Old_Click=0
    dt_Shut = []
    Prs_Shut = []
    P_Inj = Pressure[0]  # Pressure at first of Injection
    i = 0
    x = EndInj*Inj_Total*0
    Cum=[]
    EndInj=0
    while i < len(Time) - 1:  # Cumulative calculation
        i += 1
        x = Rate[i] * (Time[i] - Time[i - 1]) * 60 + x
        Cum.append(x)
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
        Cum.append(Inj_Total)

def G_Function(): ########################G Function Callulation
    global SlopeLine, P_res, Draft
    global G_Time
    global max_dpdg, T_max_dpdg, G_max_dpdg, P_max_dpdg
    global min_dpdg, T_min_dpdg, G_min_dpdg, P_min_dpdg
    global ISIP
    global dpdt_1_2, dpdt_1
    global dp_dg_1, gdp_dg_1, dpdg, gdpdg
    global dp, dtd,log_dt, t_1_2, t_1, dp_dt, tdp_dt, log_tdpdt
    global P_ISIP, Flow
    global x1,x2,x3
    global ShminT
    
    G_Time=[]
    dp=[]
    dtd=[]
    dp_dg_1 = [0]
    gdp_dg_1 = [0]
    log_dt=[0]
    t_1_2=[]
    t_1 =[]
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
    dpdg = Ave(dp_dg_1, Draft)
    gdpdg = Ave(gdp_dg_1, Draft)


    Draft = 3
    SlopeLine = (log_tdpdt[-Draft] - log_tdpdt[-Draft * 2]) / (log_dt[-Draft] - log_dt[-Draft * 2])
    dpdt_1_2 = (Prs_Shut[-Draft] - Prs_Shut[-1]) / (t_1_2[-Draft] - t_1_2[-1])
    dpdt_1 = (Prs_Shut[-Draft] - Prs_Shut[-1]) / (t_1[-Draft] - t_1[-1])
    if SlopeLine > -0.75:
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
    x3=i
    while dp_dg_1[-j] > dp_dg_1[-j - 1]:
        j += 1
    i = len(dt_Shut) - j - 1
    x1=i
    min_dpdg = dp_dg_1[i]
    P_min_dpdg = Prs_Shut[i]
    G_min_dpdg = G_Time[i]
    T_min_dpdg = dt_Shut[i]
    ShminC=P_min_dpdg-75
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
    global h_Shut,  Eff_Prs,h_fun, Stiff

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

def Results():
    global strain, sf_PKN, Perm_df
    global G_CL_PKN_C, G_lgt_PKN_C, G_K_PKN_C, Mass_PKN_C, Ms_PKN_C, G_CL_PKN_T, G_lgt_PKN_T, G_K_PKN_T, Mass_PKN_T, Ms_PKN_T
    global G_CL_RDL_C, sf_RDL_C, G_lgt_RDL_C, G_K_RDL_C, Mass_RDL_C, Ms_RDL_C, sf_RDL_T, G_CL_RDL_T, G_lgt_RDL_T, G_K_RDL_T, Mass_RDL_T, Ms_RDL_T
    global H_A_K
    global H_lgt_RDL_C, H_K_RDL_C,H_lgt_RDL_T, H_K_RDL_T
    global H_lgt_PKN_C, H_K_PKN_C, H_Ara_PKN_C, H_lgt_PKN_T, H_K_PKN_T, H_Ara_PKN_T
    global P_A_K
    global P_lgt_RDL_C, P_K_RDL_C, P_lgt_RDL_T, P_K_RDL_T
    global P_lgt_PKN_C, P_K_PKN_C, P_Ara_PKN_C, P_lgt_PKN_T, P_K_PKN_T, P_Ara_PKN_T
    global G_K_C, H_K_C, P_K_C
    global G_K_T, H_K_T, P_K_T

    l_min=1.0
    l_max=2000.0
    inc=0.01

    strain = Young / (1 - Poisson ** 2)

    # PKN Compliance
    sf_PKN = 2 * strain / (3.14159 * Frac_h)
    G_lgt_PKN_C =np.arange(l_min,l_max,inc) #452.122965031195 #
    G_CL_PKN_C = min_dpdg * (2 * WSC / 3.14159 * 5.615 + G_lgt_PKN_C * Frac_h ** 2 / strain) / ( G_lgt_PKN_C * Frac_h * (EndInj * 60) ** 0.5)
    G_K_PKN_C = 1E+15 * ((G_CL_PKN_C / 3.2808 / 60 ** 0.5) / (ISIP - P_res) * 145.04) ** 2 * 3.14159 * Fluid_Vis * 0.000000001 / (
                    Poro * (Fluid_Com + Comp) * 145.04)
    Mass_PKN_C = abs(Inj_Total * 5.615 - ((ISIP - ShminC) * WSC + 4 * G_CL_PKN_C * G_lgt_PKN_C * Frac_h * (
            EndInj * 60 / 2) ** 0.5 + G_lgt_PKN_C * Frac_h * (ISIP - ShminC) / sf_PKN))
    Ms_PKN_C = (Inj_Total * 5.615 - ((ISIP - ShminC) * WSC + 4 * G_CL_PKN_C * G_lgt_PKN_C * Frac_h * (EndInj * 60 / 2) ** 0.5 + G_lgt_PKN_C * Frac_h * (ISIP - ShminC) / sf_PKN))

    i=0
    while Mass_PKN_C[i]>Mass_PKN_C[i+1]: #abs(int(Mass_PKN[i]*Resol)/Resol-0.5)>0:
       i+=1
    G_lgt_PKN_C[0]=G_lgt_PKN_C[i]
    G_CL_PKN_C[0]= G_CL_PKN_C[i]
    G_K_PKN_C[0]=G_K_PKN_C[i]
    Mass_PKN_C[0]=Mass_PKN_C[i]


    # Radial Compliance
    G_lgt_RDL_C = np.arange(l_min, l_max, inc)  #61.0922808 #
    sf_RDL_C = 3 * 3.14159 * strain / 16 / G_lgt_RDL_C
    G_CL_RDL_C = min_dpdg * (WSC * 5.615 + G_lgt_RDL_C ** 3 * 16 / 3 / strain) / (
                2 * 3.14159 * G_lgt_RDL_C ** 2 * (EndInj * 60) ** 0.5)
    G_K_RDL_C = 1E+15 * ((G_CL_RDL_C / 3.2808 / 60 ** 0.5) / (
                ISIP - P_res) * 145.04) ** 2 * 3.14159 * Fluid_Vis * 0.000000001 / (Poro * (Comp + Fluid_Com) * 145.04)
    Mass_RDL_C = abs(Inj_Total * 5.615 - ((ISIP - ShminC) * WSC + 4 * G_CL_RDL_C * 3.14159 * G_lgt_RDL_C ** 2 * (
                EndInj * 60 / 2) ** 0.5 + G_lgt_RDL_C ** 2 * 3.14159 * (ISIP - ShminC) / sf_RDL_C))
    Ms_RDL_C = (Inj_Total * 5.615 - ((ISIP - ShminC) * WSC + 4 * G_CL_RDL_C * 3.14159 * G_lgt_RDL_C ** 2 * (
            EndInj * 60 / 2) ** 0.5 + G_lgt_RDL_C ** 2 * 3.14159 * (ISIP - ShminC) / sf_RDL_C))
    i = 0
    while (Mass_RDL_C[i] > Mass_RDL_C[i + 1]):
        i += 1
    sf_RDL_C[0] = sf_RDL_C[i]
    G_lgt_RDL_C[0] = G_lgt_RDL_C[i]
    G_CL_RDL_C[0] = G_CL_RDL_C[i]
    G_K_RDL_C[0] = G_K_RDL_C[i]
    Mass_RDL_C[0] = Mass_RDL_C[i]

    # PKN Tangent
    G_lgt_PKN_T =np.arange(l_min, l_max, inc)  #452.122965031195 #
    G_CL_PKN_T = min_dpdg * (2 * WSC / 3.14159 * 5.615 + G_lgt_PKN_T * Frac_h ** 2 / strain) / (
                G_lgt_PKN_T * Frac_h * (EndInj * 60) ** 0.5)
    G_K_PKN_T = 1E+15 * ((G_CL_PKN_T / 3.2808 / 60 ** 0.5) / (
                ISIP - P_res) * 145.04) ** 2 * 3.14159 * Fluid_Vis * 0.000000001 / (
                        Poro * (Fluid_Com + Comp) * 145.04)
    Mass_PKN_T =abs(Inj_Total*5.615-((ISIP-ShminT)*WSC+4*G_CL_PKN_T*G_lgt_PKN_T*Frac_h*(EndInj*60/2)**0.5+G_lgt_PKN_T*Frac_h*(ISIP-ShminT)/sf_PKN))
    Ms_PKN_T = (Inj_Total * 5.615 - ((ISIP - ShminT) * WSC + 4 * G_CL_PKN_T * G_lgt_PKN_T * Frac_h * (
            EndInj * 60 / 2) ** 0.5 + G_lgt_PKN_T * Frac_h * (ISIP - ShminT) / sf_PKN))
    i = 0
    while Mass_PKN_T[i] > Mass_PKN_T[i + 1]:  # abs(int(Mass_PKN[i]*Resol)/Resol-0.5)>0:
        i += 1
    G_lgt_PKN_T[0] = G_lgt_PKN_T[i]
    G_CL_PKN_T[0] = G_CL_PKN_T[i]
    G_K_PKN_T[0] = G_K_PKN_T[i]
    Mass_PKN_T[0] = Mass_PKN_T[i]

    # Radial Tangent
    G_lgt_RDL_T = np.arange(l_min, l_max, inc)  #61.0922808 #
    sf_RDL_T = 3 * 3.14159 * strain / 16 / G_lgt_RDL_T
    G_CL_RDL_T = min_dpdg * (WSC * 5.615 + G_lgt_RDL_T ** 3 * 16 / 3 / strain) / (
            2 * 3.14159 * G_lgt_RDL_T ** 2 * (EndInj * 60) ** 0.5)
    G_K_RDL_T = 1E+15 * ((G_CL_RDL_T / 3.2808 / 60 ** 0.5) / (
            ISIP - P_res) * 145.04) ** 2 * 3.14159 * Fluid_Vis * 0.000000001 / (Poro * (Comp + Fluid_Com) * 145.04)
    Mass_RDL_T = abs(Inj_Total * 5.615 - ((ISIP - ShminT) * WSC + 4 * G_CL_RDL_T * 3.14159 * G_lgt_RDL_T ** 2 * (
            EndInj * 60 / 2) ** 0.5 + G_lgt_RDL_T ** 2 * 3.14159 * (ISIP - ShminT) / sf_RDL_T))
    Ms_RDL_T = (Inj_Total * 5.615 - ((ISIP - ShminT) * WSC + 4 * G_CL_RDL_T * 3.14159 * G_lgt_RDL_T ** 2 * (
            EndInj * 60 / 2) ** 0.5 + G_lgt_RDL_T ** 2 * 3.14159 * (ISIP - ShminT) / sf_RDL_T))
    i = 0
    while (Mass_RDL_T[i] > Mass_RDL_T[i + 1]):
        i += 1
    sf_RDL_T[0] = sf_RDL_T[i]
    G_lgt_RDL_T[0] = G_lgt_RDL_T[i]
    G_CL_RDL_T[0] = G_CL_RDL_T[i]
    G_K_RDL_T[0] = G_K_RDL_T[i]
    Mass_RDL_T[0] = Mass_RDL_T[i]

    # h-function
    H_A_K = 3.2808 ** 3 * (0.9 * (Inj_Total / 6.29 - WSC / 6.29 * (P_max_dpdg - P_Inj))) / (
            4 * h_Peak / 145.04 * 60 * (
            Poro * (Comp + Fluid_Com) * 145.04 / (3.14159 * Fluid_Vis * 0.000000001)) ** 0.5)
    # Radial Compliance
    H_lgt_RDL_C = ((3 * 3.14159 * strain / 145.04 * (
            Inj_Total / 6.29 - WSC / 6.29 * 145.04 * (ISIP - P_Inj) / 145.04 - 4 * H_A_K / 3.2808 ** 3 * (
            ISIP - P_res) / 145.04 * (EndInj / 2 * 3600) ** 0.5 * (
                    Poro * (Comp + Fluid_Com) * 145.04 / (3.14159 * Fluid_Vis * 0.000000001)) ** 0.5)) / (
                           16 * 3.14159 * (ISIP - ShminC) / 145.04)) ** (1 / 3) * 3.2808
    H_K_RDL_C = (H_A_K / (3.14159 * H_lgt_RDL_C ** 2)) ** 2 / 3.2808 ** 2 * 1E+15

    # PKN Compliance
    H_Ara_PKN_C = 3.2808 ** 2 * (
                Inj_Total / 6.29 - (ISIP - P_Inj) * WSC / 6.29 - (H_A_K / 3.2808 ** 3) * 4 * h_Shut / 145.04 * 60 * (
                Poro * (Comp + Fluid_Com) * 145.04 / 3.14159 / (
                Fluid_Vis * 0.000000001)) ** 0.5) * sf_PKN / 145.04 * 3.2808 / ((ISIP - ShminC) / 145.04)
    H_lgt_PKN_C = H_Ara_PKN_C / Frac_h
    H_K_PKN_C = (H_A_K / 3.2808 ** 3 / (H_lgt_PKN_C / 3.2808 * Frac_h / 3.2808)) ** 2 * 1E+15

    # Radial Tangent
    H_lgt_RDL_T = ((3 * 3.14159 * strain / 145.04 * (
            Inj_Total / 6.29 - WSC / 6.29 * 145.04 * (ISIP - P_Inj) / 145.04 - 4 * H_A_K / 3.2808 ** 3 * (
            ISIP - P_res) / 145.04 * (EndInj / 2 * 3600) ** 0.5 * (
                    Poro * (Comp + Fluid_Com) * 145.04 / (3.14159 * Fluid_Vis * 0.000000001)) ** 0.5)) / (
                           16 * 3.14159 * (ISIP - ShminT) / 145.04)) ** (1 / 3) * 3.2808
    H_K_RDL_T = (H_A_K / (3.14159 * H_lgt_RDL_T ** 2)) ** 2 / 3.2808 ** 2 * 1E+15

    # PKN Tangent
    H_Ara_PKN_T = 3.2808 ** 2 * (
            Inj_Total / 6.29 - (ISIP - P_Inj) * WSC / 6.29 - (H_A_K / 3.2808 ** 3) * 4 * h_Shut / 145.04 * 60 * (
            Poro * (Comp + Fluid_Com) * 145.04 / 3.14159 / (
            Fluid_Vis * 0.000000001)) ** 0.5) * sf_PKN / 145.04 * 3.2808 / ((ISIP - ShminT) / 145.04)
    H_lgt_PKN_T = H_Ara_PKN_T / Frac_h
    H_K_PKN_T = (H_A_K / 3.2808 ** 3 / (H_lgt_PKN_T / 3.2808 * Frac_h / 3.2808)) ** 2 * 1E+15

    # Postclosure
    P_A_K = 3.2808 ** 3 * (dpdt_1_2 / 145.04 * 60) ** -1 * (
            Inj_Total / 6.29 - WSC / 6.29 * 145.04 * (P_res - P_Inj) / 145.04) / 2 * (
                    Fluid_Vis * 0.000000001 / (3.14159 * (Comp + Fluid_Com) * 145.04 * Poro)) ** 0.5
    # Radial Compliance
    P_lgt_RDL_C = ((3 * 3.14159 * strain / 145.04 * (
            Inj_Total / 6.29 - WSC / 6.29 * 145.04 * (ISIP - P_Inj) / 145.04 - 4 * P_A_K / 3.2808 ** 3 * (
            ISIP - P_res) / 145.04 * (EndInj / 2 * 3600) ** 0.5 * (
                    Poro * (Comp + Fluid_Com) * 145.04 / (3.14159 * Fluid_Vis * 0.000000001)) ** 0.5)) / (
                           16 * 3.14159 * (ISIP - ShminC) / 145.04)) ** (1 / 3) * 3.2808
    P_K_RDL_C = (P_A_K / (3.14159 * P_lgt_RDL_C ** 2)) ** 2 / 3.2808 ** 2 * 1E+15
    # PKN Compliance
    P_Ara_PKN_C = 3.2808 ** 2 * (
            Inj_Total / 6.29 - (ISIP - P_Inj) * WSC / 6.29 - (P_A_K / 3.2808 ** 3) * 4 * h_Shut / 145.04 * 60 * (
            Poro * (Comp + Fluid_Com) * 145.04 / 3.14159 / (
            Fluid_Vis * 0.000000001)) ** 0.5) * sf_PKN / 145.04 * 3.2808 / ((ISIP - ShminC) / 145.04)
    P_lgt_PKN_C = P_Ara_PKN_C / Frac_h
    P_K_PKN_C = (P_A_K / 3.2808 ** 3 / (P_lgt_PKN_C / 3.2808 * Frac_h / 3.2808)) ** 2 * 1E+15

    # Radial Tangent
    P_lgt_RDL_T = ((3 * 3.14159 * strain / 145.04 * (
            Inj_Total / 6.29 - WSC / 6.29 * 145.04 * (ISIP - P_Inj) / 145.04 - 4 * P_A_K / 3.2808 ** 3 * (
            ISIP - P_res) / 145.04 * (EndInj / 2 * 3600) ** 0.5 * (
                    Poro * (Comp + Fluid_Com) * 145.04 / (3.14159 * Fluid_Vis * 0.000000001)) ** 0.5)) / (
                           16 * 3.14159 * (ISIP - ShminT) / 145.04)) ** (1 / 3) * 3.2808
    P_K_RDL_T = (P_A_K / (3.14159 * P_lgt_RDL_T ** 2)) ** 2 / 3.2808 ** 2 * 1E+15
    # PKN Tangent
    P_Ara_PKN_T = 3.2808 ** 2 * (
            Inj_Total / 6.29 - (ISIP - P_Inj) * WSC / 6.29 - (P_A_K / 3.2808 ** 3) * 4 * h_Shut / 145.04 * 60 * (
            Poro * (Comp + Fluid_Com) * 145.04 / 3.14159 / (
            Fluid_Vis * 0.000000001)) ** 0.5) * sf_PKN / 145.04 * 3.2808 / ((ISIP - ShminT) / 145.04)
    P_lgt_PKN_T = P_Ara_PKN_T / Frac_h
    P_K_PKN_T = (P_A_K / 3.2808 ** 3 / (P_lgt_PKN_T / 3.2808 * Frac_h / 3.2808)) ** 2 * 1E+15


    #Final value of permeability
    if Frac_h>0:
        G_K_C=G_K_PKN_C[0]
        G_K_T=G_K_PKN_T[0]
        H_K_C = H_K_PKN_C
        H_K_T = H_K_PKN_T
        P_K_C = P_K_PKN_C
        P_K_T = P_K_PKN_T
    else:
        G_K_C = G_K_RDL_C[0]
        G_K_T = G_K_RDL_T[0]
        H_K_C = H_K_RDL_C
        H_K_T = H_K_RDL_T
        P_K_C = P_K_RDL_C
        P_K_T = P_K_RDL_T

    Perm_List = [['G_function', 'Compliance', G_K_C], ['G_function', 'Tangent', G_K_T],
                 ['h_function', 'Compliance', H_K_C], ['h_function', 'Tangent', H_K_T],
                 ['Postclosure','Compliance', P_K_C], ['Postclosure','Tangent', P_K_T]]

    Perm_df = pd.DataFrame(Perm_List, columns=['Method', 'Type', 'Permeability'])
    print(Perm_df)
    print('end of results')

def Export_CSV():
    #Export Estmations values

    with open(Results_Dir+'/Estimation.csv','w', newline="") as Estimation_csv:
        EST_CSV=csv.writer(Estimation_csv)
        EST_CSV.writerows([['Item', 'Values'],
                           ['Injection Duration (hr)', EndInj],
                           ['Pressure at start of Injection', P_Inj],
                           ['Minimum dP/dG (psi)', min_dpdg],
                           ['G-time at minimum dP/dG (unitless)', G_min_dpdg],
                           ['Pressure at minimum dP/dG (psi)', P_min_dpdg],
                           ['Effective ISIP (psi)', ISIP],
                           ['G-function value at peak dP/dG', G_max_dpdg],
                           ['Pressure at peak dP/dG', P_max_dpdg],
                           ['h-function at shut-in (psi-hrs^(1/2))', h_Shut],
                           ['h-function at peak dP/dG (psi-hrs^(1/2))', h_Peak],
                           ['Reservoir Pressure', P_res],
                           ['Minimum principal stress (psi) (Compliance)', ShminC],
                           ['Minimum principal stress (psi) (Tangent)   ', ShminT],
                           ['dP/d(t^(-1/2)) (if present) (psi/hours^(-1/2))', dpdt_1_2],
                           ['dP/d(t^-1) (if present)', dpdt_1],
                           ['Impulse', SlopeLine]
                           ])

    #Export PKN Geometry results from Compliance method
    with open(Results_Dir+'/PKN_Compliance.csv','w',newline="") as Results_CSV:
        Results=csv.writer(Results_CSV)
        Results.writerows([['Item', 'Values'],
                           ['Sf (psi/ft)',sf_PKN],
                           ['Length (ft)', G_lgt_PKN_C[0]],
                           ['CL (ft/min^.5)', "{:.2e}".format(G_CL_PKN_C[0])],
                           ['Permeability (md)', "{:.2e}".format(G_K_PKN_C[0])],
                           ['Mass balance residual', Mass_PKN_C[0]]
                           ])


    # Export RDL Geometry results from Compliance method
    with open(Results_Dir+'/RDL_Compliance.csv', 'w', newline="") as Results_CSV:
        Results = csv.writer(Results_CSV)
        Results.writerows([['Item', 'Values'],
                           ['Sf (psi/ft)', sf_RDL_C[0]],
                           ['Radius (ft)', G_lgt_RDL_C[0]],
                           ['CL (ft/min^.5)', "{:.2e}".format(G_CL_RDL_C[0])],
                           ['Permeability (md)', "{:.2e}".format(G_K_RDL_C[0])],
                           ['Mass balance residual', Mass_RDL_C[0]]
                           ])

    # Export PKN Geometry results from Tangent method
    with open(Results_Dir+'/PKN_Tangent.csv', 'w', newline="") as Results_CSV:
        Results = csv.writer(Results_CSV)
        Results.writerows([['Item', 'Values'],
                           ['Sf (psi/ft)', sf_PKN],
                           ['Length (ft)', G_lgt_PKN_T[0]],
                           ['CL (ft/min^.5)', "{:.2e}".format(G_CL_PKN_T[0])],
                           ['Permeability (md)', "{:.2e}".format(G_K_PKN_T[0])],
                           ['Mass balance residual', Mass_PKN_T[0]]
                           ])

    # Export RDL Geometry results from Tangent method
    with open(Results_Dir+'/RDL_Tangent.csv', 'w', newline="") as Results_CSV:
        Results = csv.writer(Results_CSV)
        Results.writerows([['Item', 'Values'],
                           ['Sf (psi/ft)', sf_RDL_T[0]],
                           ['Radius (ft)', G_lgt_RDL_T[0]],
                           ['CL (ft/min^.5)', "{:.2e}".format(G_CL_RDL_T[0])],
                           ['Permeability (md)', "{:.2e}".format(G_K_RDL_T[0])],
                           ['Mass balance residual', Mass_RDL_T[0]]
                           ])

    # Export RDL Geometry results from h-function method
    with open(Results_Dir+'/RDL_h_function.csv', 'w', newline="") as Results_CSV:
        Results = csv.writer(Results_CSV)
        Results.writerows([['Item', 'Values'],
                           ['Area*k^(1/2) (ft^3)', H_A_K],
                           ['Radius (ft)', H_lgt_RDL_C],
                           ['Permeability (md)', "{:.2e}".format(H_K_RDL_C)]
                           ])

    # Export PKN Geometry results from h-function method
    with open(Results_Dir+'/PKN_h_function.csv', 'w', newline="") as Results_CSV:
        Results = csv.writer(Results_CSV)
        Results.writerows([['Item', 'Values'],
                           ['Area*k^(1/2) (ft^3)',H_A_K],
                           ['Area estimate (ft^2)', H_Ara_PKN_C],
                           ['Length (ft)', H_lgt_PKN_C],
                           ['Permeability (md)', "{:.2e}".format(H_K_PKN_C)]
                           ])

    # Export RDL Geometry results from postclosure method
    with open(Results_Dir+'/RDL_Postclosure.csv', 'w', newline="") as Results_CSV:
        Results = csv.writer(Results_CSV)
        Results.writerows([['Item', 'Values'],
                           ['Area*k^(1/2) (ft^3)',P_A_K],
                           ['Radius (ft)',P_lgt_RDL_C],
                           ['Permeability (md)',"{:.2e}".format(P_K_RDL_C)]
                           ])

    # Export PKN Geometry results from from postclosure method
    with open(Results_Dir+'/PKN_Postclosure.csv', 'w', newline="") as Results_CSV:
        Results = csv.writer(Results_CSV)
        Results.writerows([['Item', 'Values'],
                           ['Area*k^(1/2) (ft^3)',P_A_K],
                           ['Area estimate (ft^2)',P_Ara_PKN_C],
                           ['Length (ft)',P_lgt_PKN_C],
                           ['Permeability (md)',"{:.2e}".format(P_K_PKN_C)]
                           ])

    # Export calculated permeability via all methods
    with open(Results_Dir+'/Permeability_Values.csv', 'w', newline="") as Results_CSV:
        Results = csv.writer(Results_CSV)
        Results.writerows([['Item', 'Values'],
                           ['G-function permeability (md) (Compliance)',"{:.2e}".format(G_K_C)],
                           ['G-function permeability (md) (Tangent)   ',"{:.2e}".format(G_K_T)],
                           ['h-function permeability (md) (Compliance)',"{:.2e}".format(H_K_C)],
                           ['h-function permeability (md) (Tangent)',"{:.2e}".format(H_K_T)],
                           ['Postclosure linear permeability (md) (Compliance)',"{:.2e}".format(P_K_C)],
                           ['Postclosure linear permeability (md) (Tangent)',"{:.2e}".format(P_K_T)]
                           ])

    # Export Vectors
    with open(Results_Dir+'/Vectors.csv', 'w', newline="") as Results_CSV:
        Results = csv.writer(Results_CSV)
        Results.writerow(['Time', 'Pressure', 'G_Time', 'dp/dG-1','G*dpdG-1','h-function (sqrt(psi*hr))',
                          'Relative Stiffness','P - ISIP (psi)','Afterflow rate (bpm)'])
        i=0
        while i<len(dp_dg_1):
            Exp_Lst = []
            Exp_Lst.append(dt_Shut[i])
            Exp_Lst.append(Prs_Shut[i])
            Exp_Lst.append(G_Time[i])
            Exp_Lst.append(dp_dg_1[i])
            Exp_Lst.append(gdp_dg_1[i])
            Exp_Lst.append(h_fun)
            Exp_Lst.append(Stiff)
            Exp_Lst.append(P_ISIP)
            Exp_Lst.append(Flow)
            i+=1
            Results.writerow(Exp_Lst)

############################################################################################################################
############################################################################################################################
##########################################Main Body

root=Tk()
root.title('Open CSV files')

##########################################import raw data
root.filename=filedialog.askopenfilename(initialdir='CSV/',
                                         initialfile='Raw_Data.csv',
                                         title='Open raw data',
                                         filetype=(('CSV file','*.CSV' ),('Text File','*.txt'),('All files','*.*'))                                        )
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
EndInj=df['Value'][10]

Results_Dir = filedialog.askdirectory(title='Select output results directory')

Extract()

G_Function()
limit=10000
if len(Time)>limit:
    shrTime=Time[:limit]
    shrPressure=Pressure[0:limit]
    shrRate=Rate[:limit]
    shrCum=Cum[:limit]
else:
    shrTime = Time
    shrPressure = Pressure
    shrRate = Rate
    shrCum = Cum

app=dash.Dash(__name__)


MainFig = make_subplots(rows=1, cols=2,
                        specs=[[{'secondary_y': True}, {'secondary_y': False}]]
                        )
MainFig.add_trace(
    go.Scatter(x=shrTime, y=shrPressure, name='Pressure', line=dict(color='blue')),
    secondary_y=False, row=1, col=1
)

MainFig.add_trace(
    go.Scatter(x=shrTime, y=shrRate, name='Rate', line=dict(color='red')),
    secondary_y=True, row=1, col=1
)

MainFig.add_trace(
    go.Scatter(x=shrTime, y=shrCum, name='Cumulative', line=dict(color='green')),
    secondary_y=True, row=1, col=1
)

MainFig.add_trace(
    go.Scatter(x=dt_Shut, y=dp, name='Pressure', line=dict(color='blue')),
     row=1, col=2
)
MainFig.add_trace(
    go.Scatter(x=dt_Shut[1:-1], y=tdp_dt, name='Deravetive', line=dict(color='red')),
     row=1, col=2
)
MainFig.add_trace(
    go.Scatter(x=[dt_Shut[-Draft],dt_Shut[-Draft*2]],y=[tdp_dt[-Draft],tdp_dt[-Draft*2]],name='Impule',line=dict(color="black")),
    row=1,col=2
)
MainFig.update_xaxes(title_text='Time (hr)', row=1, col=1,)
MainFig.update_yaxes(title_text="Pressure (psi)", secondary_y=False, row=1, col=1)
MainFig.update_yaxes(title_text="Rate (bpm)", secondary_y=True, row=1, col=1)
MainFig.update_xaxes(title_text='Elapse Time (hr)', row=1, col=2, type='log',range=[math.log10(0.001),math.log10(max(dt_Shut))])
MainFig.update_yaxes(title_text='dp t*dp/dt (psi)', type='log', row=1, col=2)

PST=make_subplots(rows=1,cols=2)
PST.add_trace(
    go.Scatter(x=t_1_2,y=Prs_Shut,name='pressure', line=dict(color='green')),
    row=1,col=1
)
PST.add_trace(
    go.Scatter(x=t_1, y=Prs_Shut, name='pressure', line=dict(color='green')),
    row=1, col=2
)
PST.update_xaxes(title_text='Inverse Time Squared Root (hr ^ (-1/2))', range=[0, 1], row=1, col=1)
PST.update_xaxes(title_text='Inverse Time (hr ^ (-1))', range=[0, 1], row=1, col=2)
PST.update_yaxes(title_text='Pressure (psi)', row=1, col=1)
PST.update_yaxes(title_text='Pressure (psi)', row=1, col=2)


app.layout=html.Div([
    html.H1(children='DFIT data calculation'),

    html.H2(children='Main Charts'),
    dcc.Graph(
        id="basic",
        figure=MainFig
    ),

    html.H2(children='Post Closure Charts'),
    dcc.Graph(
        id='PST_CLS',
        figure=PST
    ),

    html.Br(),
    html.Br(),

    html.Div(children='Please select desired curve:'),
    dcc.Dropdown(
        id='DD_Curve',
        options=[
            {'label':'Original curve','value':'Original'},
            {'label':'Smoothed curve','value':'Smoothed'}
        ],
        value='Original'
    ),

    html.Br(),
    html.Br(),

    html.Div(children='dp/dg slider'),
    dcc.Slider(
        id='dp_dg',
        min=1,
        max=len(G_Time),
        value=x1
    ),

    html.Div(children='Max dp/dg'),
    dcc.Slider(
        id='Max_G',
        min=1,
        max=len(G_Time),
        value=x3
    ),

    html.H2(children='G-Function Charts'),
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

    html.H2(children='Results'),
    dcc.Graph(
        id='Perm',
        figure={}
    ),

    html.Div(children='Minimum Principle Slider'),
    dcc.Slider(
        id='Shmin',
        min=min(Prs_Shut),
        max=max(Prs_Shut),
        value=P_min_dpdg - 75
    ),

    html.Div(id='ShC', children='Minimum Principle Stress (Compliance) is:'),
    html.Div(id='ShT', children='Minimum Principle Stress (Tangent) is:'),
    html.Div(id='ISIP', children='The effective ISIP is: '),

    html.Br(),
    html.Br(),

    dcc.Graph(
        id='Results',
        figure={}
    ),

    html.Br(),
    html.Br(),

    html.Button(
        id='Export',children='Export',n_clicks=0
    )
])

@app.callback(
    [Output(component_id='Graph',component_property='figure'),
     Output(component_id='ShC',component_property='children'),
     Output(component_id='ShT',component_property='children'),
     Output(component_id='ISIP',component_property='children'),
     Output(component_id='Results',component_property='figure'),
     Output(component_id='Perm',component_property='figure')],
    [Input(component_id='dp_dg',component_property='value'),
     Input(component_id='Max_G',component_property='value'),
     Input(component_id='Tangent',component_property='value'),
     Input(component_id='vertical',component_property='value'),
     Input(component_id='DD_Curve',component_property='value'),
     Input(component_id='Export',component_property='n_clicks'),
     Input(component_id='Shmin',component_property='value')]
)
def Update_Graph(G, Peak, Slope, Ver, Fit, Click,ClsPrs):
    global pg,gpg, Old_Click, ShminC, ShminT,h_Peak

    max_G=G_max_dpdg*1.5
    max_gdpdg=max(gdp_dg_1)*1.1
    max_dp=max_dpdg*1.5

    if Click==0:
        Old_Click=0

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
        go.Scatter(x=[G_Time[Peak], G_Time[Peak]], y=[0, max(dpdg)], name='Peak', line=dict(color='grey', dash='dot')),
        secondary_y=True, row=1, col=1
    )
    fig1.add_trace(
        go.Scatter(x=[G_Time[G],G_Time[G]],y=[0,max(dpdg)],name='Min',line=dict(color='black',dash='dash')),
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
    fig1.update_xaxes(title_text='G-Function', row=1, col=1,range=[0,max(G_Time)])
    fig1.update_yaxes(title_text="Pressure (psi)", secondary_y=False, row=1,col=1)
    fig1.update_yaxes(title_text="dp/dg (psi)", secondary_y=True,row=1,col=1,range=[0,max_dp])
    fig1.update_xaxes(title_text='G-Function',row=1,col=2,range=[0,max(G_Time)])
    fig1.update_yaxes(title_text='Pressure (psi)',secondary_y=False,row=1,col=2)
    fig1.update_yaxes(title_text='G*dp/dg (psi)',secondary_y=True,row=1,col=2)


    ShminC=Prs_Shut[G]-75
    ShminC=ClsPrs
    SminC='Minimum Principle Stress (Compliance) is: '+ str(round(ShminC,2))+' psi'

    ShminT=Prs_Shut[Ver]
    SminT='Minimum Principle Stress (Tangent) is: '+str(round(ShminT,2))+' psi'
    if Fit=='Original':
        pg=dp_dg_1
        gpg=gdp_dg_1
    else:
        pg=dpdg
        gpg=gdpdg
    ISIP = 'The effective ISIP is: '+ str(round(Prs_Shut[G] + pg[G] * G_Time[G],2))+' (psi) and reservoir pressure is: '+ str(round(P_res,2))+' (psi) and impuls slope of: ',str(round(SlopeLine,3))
    min_dpdg = pg[G]
    P_min_dpdg = Prs_Shut[G]
    G_min_dpdg = G_Time[G]
    T_min_dpdg = dt_Shut[G]

    H_Function()
    h_Peak=h_fun[Peak]
    Results()

    fig2=make_subplots(rows=1,cols=2,
        subplot_titles=('PKN Sytem','Radial System','PST_Closure Linear','PST_Closure Radial'))
    fig2.add_trace(
        go.Scatter(x=G_lgt_PKN_C[1:],y=Ms_PKN_C[1:],name='Compliance',line=dict(color='blue')),
        row=1,col=1
    )
    fig2.add_trace(
        go.Scatter(x=G_lgt_PKN_T[1:],y=Ms_PKN_T[1:],name='Tangent',line=dict(color='red')),
        row=1,col=1
    )
    fig2.add_trace(
        go.Scatter(x=G_lgt_RDL_C[1:],y=Ms_RDL_C[1:],name='Compliance',line=dict(color='blue')),
        row=1,col=2
    )
    fig2.add_trace(
        go.Scatter(x=G_lgt_RDL_T[1:],y=Ms_RDL_T[1:],name='Tangent',line=dict(color='red')),
        row=1,col=2
    )

    if G_lgt_PKN_T[0]>G_lgt_PKN_C[0]:
        max_l=G_lgt_PKN_T[0]
    else:
        max_l=G_lgt_PKN_C[0]
    if G_lgt_RDL_T[0]>G_lgt_RDL_C[0]:
        max_r=G_lgt_RDL_T[0]
    else:
        max_r=G_lgt_RDL_C[0]
    fig2.update_xaxes(title_text='length (ft)',row=1,col=1,range=[0,max_l*1.5])
    fig2.update_yaxes(title_text='Mass balance residual (bbl)',row=1,col=1,range=[-100,100])
    fig2.update_yaxes(title_text='Mass balance residual (bbl)',row=1,col=2,range=[-100,100])
    fig2.update_xaxes(title_text='radius (ft)',row=1,col=2,range=[0,max_r*1.5])




    PermBar=make_subplots(1,2)
    for Type, group in Perm_df.groupby('Type'):
        PermBar.add_trace(go.Bar(x=group['Method'], y=group['Permeability'], name=Type),
                          row=1,col=2)
    PermBar.add_trace(
        go.Scatter(x=Eff_Prs, y=Stiff, name='Relative System Stiffness', line=dict(color='blue')), row=1, col=1
    )

    PermBar.add_trace(
        go.Scatter(x=[ShminC, ShminC], y=[0, 3], name='Impule', line=dict(color="black")),
        row=1, col=1
    )
    PermBar.update_xaxes(title_text='Pressure (psi)', row=1, col=1)
    PermBar.update_yaxes(title_text='Relative System Stiffness', type='log', row=1, col=1)
    PermBar.update_yaxes(title_text='Permeability (md)', row=1, col=2)

    '''PermBar= px.bar(Perm_df,
                    x='Method',
                    y='Permeability',
                    color='Type',
                    barmode='group')'''


    if Click>Old_Click:
        Export_CSV()


    Old_Click=Click
    return fig1, SminC, SminT, ISIP, fig2, PermBar


app.run_server()