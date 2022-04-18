#!/usr/bin/env python
# coding: utf-8

# ## $\color{orange}{\textbf{Prevendo perdas russas na Guerra da Ucrânia com ML}}$

# # $\color{orange}{\textbf{Importando as bibliotecas}}$

# In[362]:


"""
1°) Importação do pandas como pd para trabalhar com dados.
"""
import pandas as pd
"""
2°) Importação do numpy como np para trabalhar com matrizes e tudo mais.
"""
import numpy as np
"""
3°) Importação do matplotlib.pyplot como plt para fazer gráficos.
"""
import matplotlib.pyplot as plt
"""
4°) De matplotlib.ticker vamos importar o AutoMinorLocator e o MaxNLocator para trabalhar com os "ticks"
    dos gráficos.
"""
import matplotlib.ticker as mticker
from matplotlib.ticker import AutoMinorLocator, MaxNLocator
"""
5°) De matplotlib.font_manager vamos importar FontProperties para criar fontes de texto.
"""
from matplotlib.font_manager import FontProperties
"""
6°) Importação do seaborn para fazer gráficos
"""
import seaborn as sbn
"""
7°) Importação de pycaret.time_series para trabalhar com séries temporais
"""
from pycaret.time_series import *
"""
8°) Ignorar alguns warnings que não afetam o código
"""
import warnings
warnings.filterwarnings("ignore")


# # $\color{orange}{\textbf{Importação dos dados}}$

# In[363]:


"""
1°) Importação do dataset que possui as perdas russas em termos de equipamento bélico
"""
losses_equipment = pd.read_csv("russia_losses_equipment_git.csv")
"""
2°) Importação do dataset que possui as perdas russas em termos de tropas
"""
losses_personnel = pd.read_csv("russia_losses_personnel_git.csv")


# # $\color{orange}{\textbf{Pré-processamento de dados}}$

# In[364]:


"""
Vamos começar concatenando os dois DFs anteriores
"""
"""
1°) Como já vai haver uma coluna de "data" e uma de "dias de guerra" no DF "losses_equipment", 
não faz sentido manter as mesmas no DF "losses_personnel". Além disso, vamos excluir algumas
colunas que não serão usadas no presente trabalho.
"""
losses_personnel.drop(["date", 
                       "day",
                       "personnel*",
                       "POW"], axis = 1, inplace = True)
losses_equipment.drop(["APC", 
                       "field artillery", 
                       "MRL",
                       "fuel tank",
                       "special equipment", 
                       "mobile SRBM system"], axis = 1, inplace = True)
"""
Concatenando os dois DFs anteriores
"""
Dados = pd.concat([losses_equipment, losses_personnel], axis = 1)
"""
Mostrar na tela a parte superior do DF "Dados" com suas 10 colunas
"""
pd.set_option("display.max_columns", 10)
Dados.head()


# In[365]:


"""
Tranformação da data de object para datetime64[ns]
"""
Dados["date"] = pd.to_datetime(Dados["date"])


# # $\color{orange}{\textbf{Dados faltantes}}$

# In[366]:


"""
Calcula as porcentagens de dados missing em cada coluna do DF
"""
Dados.isnull().sum()/len(Dados["date"])


# In[367]:


Dados.describe()


# # $\color{orange}{\textbf{Análise de dados}}$

# In[368]:


"""
Criação da primeira fonte de texto para colocar como fonte dos labels
"""
font1 = {"family": "Verdana", "weight": "bold", "color": "gray", "size": 13}
"""
Criação da segunda fonte de texto para colocar como fonte da legenda
"""
font2 = FontProperties(family = "Verdana", 
                      weight = "bold",
                      size = 13)
"""
Criando um "local" para alocar a nossa figura
"""
fig, axs = plt.subplots(figsize = (10, 7))
"""
Plot das curvas
"""
axs.plot(Dados["day"], Dados["military auto"], linewidth = 2, label = "Automóveis militares", color = "cyan")
axs.plot(Dados["day"], Dados["tank"], linewidth = 2, label = "Tanques", color = "yellow")
axs.plot(Dados["day"], Dados["helicopter"], linewidth = 2, label = "Helicópteros", color = "darkred")
axs.plot(Dados["day"], Dados["aircraft"], linewidth = 2, label = "Aeronaves", color = "blue")
axs.plot(Dados["day"], Dados["anti-aircraft warfare"], linewidth = 2, label = "Defesa antiaérea", color = "red")
axs.plot(Dados["day"], Dados["drone"], linewidth = 2, label = "Drones", color = "gray")
axs.plot(Dados["day"], Dados["naval ship"], linewidth = 2, label = "Navios", color = "orange")
"""
Grid = False
"""
axs.grid(False)
"""
Definindo a "grossura" e a cor do eixos
"""
for axis in ["left", "top", "right", "bottom"]:
    axs.spines[axis].set_linewidth(2)
    axs.spines[axis].set_color("gray")
"""
Trabalha com os ticks do gráfico
"""        
axs.xaxis.set_minor_locator(AutoMinorLocator())
axs.yaxis.set_minor_locator(AutoMinorLocator())
axs.tick_params(axis = "both", direction = "in", labelcolor = "gray", labelsize = 13, top = True, right = True, left = True, bottom = True)
axs.tick_params(which='minor', direction = "in", length=2, color='gray', width = 2, top = True, right = True, left = True, bottom = True)
axs.tick_params(which='major', direction = "in", color='gray', length=3.4, width = 2, top = True, right = True, left = True, bottom = True)
"""
Definindo um intervalo para o eixo x do gráfico
"""
plt.xlim(2, 53)
"""
Legenda da figura
"""
plt.legend(frameon = False, prop = font2, labelcolor = "gray")
"""
Tudo em negrito
"""
plt.rcParams["font.weight"] = "bold"
plt.rcParams["axes.labelweight"] = "bold"
"""
Labels
"""
axs.set_xlabel("Dias de guerra", fontdict = font1)
axs.set_ylabel("Total de perdas", fontdict = font1)
"""
Fundo branco
"""
fig.patch.set_facecolor("white")
"""
Título da figura
"""
axs.set_title("Perdas bélicas da Rússia na guerra contra a Ucrânia", fontdict = font1)
plt.show()


# In[369]:


Lista_de_perdas_para_cada_equipamento = []
Lista_de_equipamentos = ["Aeronaves", "Helicópteros", "Tanques", "Automóveis militares", "Drones", "Navios", "Defesa antiaérea"]
for c in ["aircraft", "helicopter", "tank", "military auto", "drone", "naval ship", "anti-aircraft warfare"]:
    S = 0 # Variável soma  
    for i in Dados[c]:
        S = S + i
    Lista_de_perdas_para_cada_equipamento.append(S)


# In[370]:


fig, axs = plt.subplots(figsize = (10, 9))
"""
Plot de um gráfico do tipo pizza
"""
axs.pie(x = Lista_de_perdas_para_cada_equipamento, 
        labels = Lista_de_equipamentos, 
        shadow = True, 
        explode = [0, 0, 0.1, 0, 0, 0, 0], # Lista de seprações entre os "pedaços da pizza"
        textprops={"family": "verbose", 
                   "weight": "bold", 
                   "color" :"gray", 
                   'fontsize': 13}, 
        colors = ["blue", "darkred", "yellow", "cyan", "pink", "orange", "red"],
        labeldistance = 1.06) # Distância dos labels ao centro da pizza
fig.patch.set_facecolor("white")
plt.show() 


# $\color{orange}{\textbf{Em termos bélicos, o que a Russia mais perde são automóveis militares e tanques de guerra.}}$

# In[371]:


fig, axs = plt.subplots(figsize = (10, 7))
axs.plot(Dados["day"], Dados["personnel"], linewidth = 2, color = "cyan")
axs.grid(False)
for axis in ["left", "top", "right", "bottom"]:
    axs.spines[axis].set_linewidth(2)
    axs.spines[axis].set_color("gray")
axs.xaxis.set_minor_locator(AutoMinorLocator())
axs.yaxis.set_minor_locator(AutoMinorLocator())
axs.tick_params(axis = "both", direction = "in", labelcolor = "gray", labelsize = 13, top = True, right = True, left = True, bottom = True)
axs.tick_params(which='minor', direction = "in", length=2, color='gray', width = 2, top = True, right = True, left = True, bottom = True)
axs.tick_params(which='major', direction = "in", color='gray', length=3.4, width = 2, top = True, right = True, left = True, bottom = True)
plt.rcParams["font.weight"] = "bold"
plt.rcParams["axes.labelweight"] = "bold"
plt.xlim(2, 53)
axs.set_xlabel("Dias de guerra", fontdict = font1)
axs.set_ylabel("Total de mortes russas", fontdict = font1)
fig.patch.set_facecolor("white")
plt.show()                      


# $\color{orange}{\textbf{Muitos russos foram mortos e, pelo andar crescente do gráfico, vem mais por aí...}}$

# # $\color{orange}{\textbf{Previsão das séries temporais}}$

# $\color{orange}{\textbf{Realizaremos previsões para 5 variáveis; Aeronaves, helicópteros, tanques de guerra, automóveis}}$
# 
# $\color{orange}{\textbf{e mortes russas.}}$

# In[372]:


"""
Definindo vários DFs apenas com a data e uma variável. 
"""
aeronaves = Dados[["date", "aircraft"]]              
helicopteros = Dados[["date", "helicopter"]]              
tanques = Dados[["date", "tank"]]                    
automoveis_militares = Dados[["date", "military auto"]]             
pessoas = Dados[["date", "personnel"]]               


# In[373]:


"""
Transformando a data em índices
"""
aeronaves.set_index("date", drop = True, inplace = True)           
helicopteros.set_index("date", drop = True, inplace = True)             
tanques.set_index("date", drop = True, inplace = True)                   
automoveis_militares.set_index("date", drop = True, inplace = True)          
pessoas.set_index("date", drop = True, inplace = True)


# In[374]:


"""
Criando um setup com a variável
"""
setup(aeronaves, fh = 5, fold = 6, seasonal_period="D", n_jobs = -1, use_gpu = True)


# In[375]:


"""
Comparando modelos de ajuste
"""
best_model = compare_models()


# In[376]:


"""
Definindo o modelo que ganhou na comparação
"""
auto_arima = create_model("auto_arima")


# In[377]:


"""
Finalização do modelo
"""
final_aeronaves = finalize_model(auto_arima)


# In[378]:


"""
Realizando 5 dias de previsão
"""
pred_aeronaves = predict_model(final_aeronaves, fh = 5)
pred_aeronaves = pd.DataFrame(pred_aeronaves, columns = ["date", "aircraft"])
pred_aeronaves["date"] = pred_aeronaves.index.to_timestamp()
pred_aeronaves = pred_aeronaves.loc[pred_aeronaves["aircraft"] > 0]
pred_aeronaves


# In[379]:


setup(helicopteros, fh = 5, fold = 6, seasonal_period = "D", n_jobs = -1, use_gpu = True)


# In[380]:


best_model = compare_models()


# In[381]:


theta = create_model("theta")


# In[382]:


final_helicopter = finalize_model(theta)


# In[383]:


pred_helicopter = predict_model(final_helicopter, fh = 5)
pred_helicopter = pd.DataFrame(pred_helicopter, columns = ["date", "helicopter"])
pred_helicopter["date"] = pred_helicopter.index.to_timestamp()
pred_helicopter = pred_helicopter.loc[pred_helicopter["helicopter"] > 0]
pred_helicopter


# In[384]:


setup(tanques, fh = 5, fold = 6, seasonal_period = "D", n_jobs = -1, use_gpu = True)


# In[385]:


best_model = compare_models()


# In[386]:


auto_arima = create_model("auto_arima")


# In[387]:


final_tanques = finalize_model(auto_arima)


# In[388]:


pred_tanques = predict_model(final_tanques, fh = 5)
pred_tanques = pd.DataFrame(pred_tanques, columns = ["date", "tank"])
pred_tanques["date"] = pred_tanques.index.to_timestamp()
pred_tanques = pred_tanques.loc[pred_tanques["tank"] > 0]
pred_tanques


# In[389]:


setup(automoveis_militares, fh= 5, fold = 6, seasonal_period = "D", n_jobs = -1, use_gpu=True)


# In[390]:


best_model = compare_models()


# In[391]:


huber_cds_dt = create_model("huber_cds_dt")                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                     


# In[392]:


final_automoveis = finalize_model("huber_cds_dt")


# In[393]:


pred_automoveis = predict_model(final_automoveis, fh = 5)
pred_automoveis = pd.DataFrame(pred_automoveis, columns = ["date", "military auto"])
pred_automoveis["date"] = pred_automoveis.index.to_timestamp()
pred_automoveis = pred_automoveis.loc[pred_automoveis["military auto"] > 0]
pred_automoveis


# In[394]:


setup(pessoas, fh = 5, fold = 6, seasonal_period="D", n_jobs=-1, use_gpu=True)


# In[395]:


best_model = compare_models()


# In[396]:


theta = create_model("theta")


# In[397]:


final_pessoas = finalize_model(theta)


# In[398]:


pred_pessoas = predict_model(final_pessoas, fh = 5)
pred_pessoas = pd.DataFrame(pred_pessoas, columns = ["date", "personnel"])
pred_pessoas["date"] = pred_pessoas.index.to_timestamp()
pred_pessoas = pred_pessoas.loc[pred_pessoas["personnel"] > 0]
pred_pessoas


# # $\color{orange}{\textbf{Plotando as previsões}}$

# In[399]:


"""
Criando um "local" para alocar a nossa figura
"""
fig, axs = plt.subplots(figsize = (10, 7))
"""
Plot das curvas
"""
axs.plot(Dados["date"], Dados["military auto"], linewidth = 2, label = "Automóveis militares (De 2022-02-25 até 2022-04-18)", color = "cyan")
axs.plot(pred_automoveis["date"], pred_automoveis["military auto"], "--g", linewidth = 2, label = "Previsão (De 2022-04-19 até 2022-04-23)", color = "cyan")
axs.plot(Dados["date"], Dados["tank"], linewidth = 2, label = "Tanques", color = "yellow")
axs.plot(pred_tanques["date"], pred_tanques["tank"], "--g", linewidth = 2, label = "Previsão", color = "yellow")
axs.plot(Dados["date"], Dados["helicopter"], linewidth = 2, label = "Helicópteros", color = "darkred")
axs.plot(pred_helicopter["date"], pred_helicopter["helicopter"], "--g", linewidth = 2, label = "Previsão", color = "darkred")
axs.plot(Dados["date"], Dados["aircraft"], linewidth = 2, label = "Aeronaves", color = "blue")
axs.plot(pred_aeronaves["date"], pred_aeronaves["aircraft"], "--g", label = "Previsão", color = "blue")
"""
Grid = False
"""
axs.grid(False)
"""
Definindo a "grossura" e a cor do eixos
"""
for axis in ["left", "top", "right", "bottom"]:
    axs.spines[axis].set_linewidth(2)
    axs.spines[axis].set_color("gray")
"""
Trabalha com os ticks do gráfico
"""        
axs.xaxis.set_minor_locator(AutoMinorLocator())
axs.yaxis.set_minor_locator(AutoMinorLocator())
axs.tick_params(axis = "both", direction = "in", labelcolor = "gray", labelsize = 13, top = True, right = True, left = True, bottom = True)
axs.tick_params(which='minor', direction = "in", length=2, color='gray', width = 2, top = True, right = True, left = True, bottom = True)
axs.tick_params(which='major', direction = "in", color='gray', length=3.4, width = 2, top = True, right = True, left = True, bottom = True)
"""
Rotacionando o label do eixo x 
"""
plt.xticks(rotation=45)
"""
Definindo um intervalo para o eixo x do gráfico
"""
"""
Legenda da figura
"""
plt.legend(frameon = False, prop = font2, labelcolor = "gray")
"""
Tudo em negrito
"""
plt.rcParams["font.weight"] = "bold"
plt.rcParams["axes.labelweight"] = "bold"
"""
Labels
"""
axs.set_xlabel("Data", fontdict = font1)
axs.set_ylabel("Total de perdas", fontdict = font1)
"""
Fundo branco
"""
fig.patch.set_facecolor("white")
"""
Título da figura
"""
axs.set_title("Perdas bélicas da Rússia na Guerra contra a Ucrânia", fontdict = font1)
plt.show()


# In[400]:


fig, axs = plt.subplots(figsize = (10, 7))
axs.plot(Dados["date"], Dados["personnel"], linewidth = 2, color = "cyan", label = "Dados originais (De 2022-02-25 até 2022-04-18)")
axs.plot(pred_pessoas["date"], pred_pessoas["personnel"], "--g", linewidth = 2, color = "cyan", label = "Previsão (De 2022-04-19 até 2022-04-23)")
axs.grid(False)
for axis in ["left", "top", "right", "bottom"]:
    axs.spines[axis].set_linewidth(2)
    axs.spines[axis].set_color("gray")
axs.xaxis.set_minor_locator(AutoMinorLocator())
axs.yaxis.set_minor_locator(AutoMinorLocator())
axs.tick_params(axis = "both", direction = "in", labelcolor = "gray", labelsize = 13, top = True, right = True, left = True, bottom = True)
axs.tick_params(which='minor', direction = "in", length=2, color='gray', width = 2, top = True, right = True, left = True, bottom = True)
axs.tick_params(which='major', direction = "in", color='gray', length=3.4, width = 2, top = True, right = True, left = True, bottom = True)
plt.xticks(rotation = 45)
plt.rcParams["font.weight"] = "bold"
plt.rcParams["axes.labelweight"] = "bold"
axs.set_xlabel("Data", fontdict = font1)
axs.set_ylabel("Total de mortes russas", fontdict = font1)
plt.legend(frameon = False, prop = font2, labelcolor = "gray")
fig.patch.set_facecolor("white")
plt.show()          

