# Prevendo perdas russas na Guerra da Ucrânia com ML

# 1. Introdução

Após cerca de 2 anos de pandemia de covid-19, fomos surpreendidos pela <b>invasão da Rússia à Ucrânia</b>. Independente dos motivos de tal guerra, esse trabalho possui cunho imparcial e <b>pretende fazer previsões de séries temporais nesse contexto</b>.

<p align="center">

<img src = "https://media0.giphy.com/media/hFKpvVLENPAMmoy5nf/giphy.gif" height = 400, widht = 900>

<p>

Uma guerra é prejudicial para todo mundo. No entanto, ela ainda mais destrutiva para os que nela estão envolvidos diretamente. A Rússia, por exemplo, apresenta os perfis a seguir de perdas bélicas e humanas;
    
<p align="center">
    
<img src = "https://user-images.githubusercontent.com/93550626/163851149-5081e289-fea2-43c6-af87-5e4adaeeb6de.png" width = 500 height = 400>
<img src = "https://user-images.githubusercontent.com/93550626/163851713-ee8a939a-a67a-40ae-8630-210a7cba0c45.png" width = 500 height = 400>    
    
<p>    

Muitos russos foram mortos e muitos equipamentos foram perdidos. Nesse sentido, o presente trabalho <b>pretende prever perdas russas, tanto bélicas quanto humanas</b>.

# 2. Objetivos

* Realizar previsões para 5 variáveis; Aeronaves, helicópteros, tanques de guerra, automóveis militares e pessoas.

# 3. Procedimentos
## 3.1. Conjunto de dados original

O conjunto de dados que foi utilizado aqui está disponível no site do <b>Kaggle</b>: https://www.kaggle.com/datasets/piterfm/2022-ukraine-russian-war?select=russia_losses_personnel.csv

Tal dataset é divido em duas partes; "Perdas de equipamentos russos" e "Perdas de pessoal russo".

As colunas aproveitadas do 1º conjunto do dados são descritas abaixo:

* `date` : Data de observação
* `day` :  Dias de guerra
* `aircraft` : Aeronaves
* `helicopter` : Helicópteros
* `tank` : Tanques
* `military auto` : Automóveis militares 
* `drone` : Drones
* `naval ship` : Navio
* `anti-aircraft warfare` : Defesa antiaérea

As colunas aproveitadas do 2º conjunto de dados são descritas abaixo:

* `date` : Data de observação
* `day` : Dias de Guerra
* `personnel` : Pessoas mortas

## 3.2. Importação das bibliotecas

``` bash
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
```

## 3.3. Importação e pré-processamento de dados

```bash
"""
1°) Importação do dataset que possui as perdas russas em termos de equipamento bélico
"""
losses_equipment = pd.read_csv("russia_losses_equipment_git.csv")
"""
2°) Importação do dataset que possui as perdas russas em termos de tropas
"""
losses_personnel = pd.read_csv("russia_losses_personnel_git.csv")
"""
Vamos começar concatenando os dois DFs anteriores

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
Tranformação da data de object para datetime64[ns]
"""
Dados["date"] = pd.to_datetime(Dados["date"])
```

### 3.3.1. Dados faltantes

```bash
"""
Calcula as porcentagens de dados missing em cada coluna do DF
"""
Dados.isnull().sum()/len(Dados["date"])
```
Felizmente, não há dados faltantes nesse conjunto de dados.

### 3.3.2. Análise dos dados

Começamos plotando as séries temporais para as perdas bélicas da Rússia;
    
<p alighn="center">

<img src = "https://user-images.githubusercontent.com/93550626/163851149-5081e289-fea2-43c6-af87-5e4adaeeb6de.png" width = 500 height = 400>
<img src = "https://user-images.githubusercontent.com/93550626/163858392-f3d0175d-7c05-4dfb-b15f-503d8a2f91f5.png" width = 500 height = 400>    
    
<p>    

Agora, as perdas humanas;
    
<p align="center">
    
<img src = "https://user-images.githubusercontent.com/93550626/163858498-85597a3d-ed2e-4b5b-9782-11a5e5ce391f.png" width = 500 height = 400>
    
<p>    

Muitos russos foram mortos e, pelo andar crescente do gráfico, vem mais por aí...

## 3.4. Preparação dos dados para a aplicação do PyCaret

```bash
"""
Definindo vários DFs apenas com a data e uma variável. 
"""
aeronaves = Dados[["date", "aircraft"]]              
helicopteros = Dados[["date", "helicopter"]]              
tanques = Dados[["date", "tank"]]                    
automoveis_militares = Dados[["date", "military auto"]]             
pessoas = Dados[["date", "personnel"]]       
"""
Transformando a data em índices
"""
aeronaves.set_index("date", drop = True, inplace = True)           
helicopteros.set_index("date", drop = True, inplace = True)             
tanques.set_index("date", drop = True, inplace = True)                   
automoveis_militares.set_index("date", drop = True, inplace = True)          
pessoas.set_index("date", drop = True, inplace = True)
```

## 3.5. Como o PyCaret é aplicado?
### Exemplo para o caso das aeronaves russas
```bash
"""
Criando um setup com a variável
"""
setup(aeronaves, fh = 5, fold = 6, seasonal_period="D", n_jobs = -1, use_gpu = True)
"""
Comparando modelos de ajuste
"""
best_model = compare_models()
"""
Definindo o modelo que ganhou na comparação
"""
auto_arima = create_model("auto_arima")
"""
Finalização do modelo
"""
final_aeronaves = finalize_model(auto_arima)
"""
Realizando 5 dias de previsão
"""
pred_aeronaves = predict_model(final_aeronaves, fh = 5)
pred_aeronaves = pd.DataFrame(pred_aeronaves, columns = ["date", "aircraft"])
pred_aeronaves["date"] = pred_aeronaves.index.to_timestamp()
pred_aeronaves = pred_aeronaves.loc[pred_aeronaves["aircraft"] > 0]
pred_aeronaves
```

# 4. Resultados 

A previsão foi feita de de 2022-04-19 até 2022-04-23; Começamos primeiro com as perdas bélicas;
    
<p align="center">
    
<img src = "https://user-images.githubusercontent.com/93550626/163860396-7337248b-d393-45a2-8e5b-7d36e1a6d7fe.png" width = 500 height = 400>
    
<p>      

Agora com as perdas humanas;
    
<p align="center">
    
<img src = "https://user-images.githubusercontent.com/93550626/163862019-20f60fbd-ec80-4108-9843-4182adb71233.png" width = 500 height = 400>
    
<p>      

# 5. Conclusão

As perdas bélicas continuam sendo altas, mas a taxa de variação das perdas humanas visivelmente diminuiu!












