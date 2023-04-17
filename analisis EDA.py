import pandas as pd
import numpy as np
import pingouin as pg
import matplotlib.pyplot as plt
import seaborn as sb

#BASES DE DATOS
df_UF = pd.read_csv('01. URBANA_FONDO.csv', sep = ',', encoding = 'latin-1', header= 0)

df_SU = pd.read_csv('02. SUBURBANA_FONDO.csv', sep = ';', encoding = 'latin-1',header= 0)

df_UT = pd.read_csv('03. URBANA_TRAFICO.csv', sep = ';', encoding = 'latin-1', header= 0)

df_I = pd.read_csv('04. INDUSTRIAL.csv', sep = ';', encoding = 'latin-1',header= 0)

df_TM = pd.read_csv('05. TENDENCIA MESO ESCALA.csv', sep = ';', encoding = 'latin-1', header= 0)


#este codigo tiene amarrado todo con estas variables, por ejemplo si cambias de dataframe tambien debes por ner las
#respectivas estacionees a analizar PARA ESO PUEDES USAR   print(df_SU.columns)

ESTACIONES = ['MED-UNNV', 'EST-HOSP', 'MED-VILL','MED-BEME']

#aqui solo cambiar el nombre del dataframe a analizar
C = df_UF[['aÃ±o', 'MESL', 'MED-UNNV', 'EST-HOSP', 'MED-VILL','MED-BEME']]
c = C #esta elimina las filas donde se encuentra un valor no existente

##############################################################################################
#agrupacion de los datos por mes y filtrado por año

A_2017 = c[c['aÃ±o']==2017].groupby('MESL', sort = False)[ESTACIONES].mean()
A_2018 = c[c['aÃ±o']==2018].groupby('MESL', sort= False)[ESTACIONES].mean()
A_2019 = c[c['aÃ±o']==2019].groupby('MESL', sort= False)[ESTACIONES].mean()
A_2020 = c[c['aÃ±o']==2020].groupby('MESL', sort= False)[ESTACIONES].mean()
A_2021 = c[c['aÃ±o']==2021].groupby('MESL', sort= False)[ESTACIONES].mean()

#grafica de las concentraciones

'''
fig, axes = plt.subplots(2, 2, figsize=(20, 10))
A_2017.plot(ax=axes[0,0], xlabel = "", ylabel = "PM 2.5", linestyle = 'solid', marker = 'o')
axes[0,0].set_title('2017')
A_2018.plot(ax=axes[0,1], xlabel = "", ylabel = "PM 2.5",linestyle = 'solid', marker = 'o')
axes[0,1].set_title('2018')
A_2019.plot(ax=axes[1,0],xlabel = "", ylabel = "PM 2.5", linestyle = 'solid', marker = 'o')
axes[1,0].set_title('2019')
A_2020.plot(ax=axes[1,1], xlabel = "", ylabel = "PM 2.5", linestyle = 'solid',  marker = 'o')
axes[1,1].set_title('2020')
plt.show()
'''







################################################################################################
#analisis de diagrama de cajas
c = C.dropna()

#agrupamiento sin tomar en cuenta un promedio mensual
UF = (c.melt().iloc[1592:] ).rename({'variable': 'ESTACIONES', 'value': 'PM2.5'}, axis = 1)
UF['PM2.5'] = UF['PM2.5'].astype('float64')

#agrupamiento tomando en cuenta el agrupamiento por promedio mensual generando un total de 12 muestras semi-homogeneas para el analisis
UF_2 = (c.groupby('MESL')[ESTACIONES].mean() ).melt().rename({'variable': 'ESTACIONES', 'value': 'PM2.5'}, axis = 1)

#visualizacion de los datos
''
fig, ax = plt.subplots(1, 1, figsize=(8, 4))
sb.boxplot(x= 'ESTACIONES' , y = 'PM2.5', data = UF_2 , ax= ax )
sb.swarmplot(x= 'ESTACIONES' , y = 'PM2.5', data = UF_2 , color='black',  alpha = 0.5, ax= ax)
plt.title('DIAGRAMA DE CAJAS DE LAS ESTACIONES URBANAS DE FONDO')
''

##############################################################################################
#analisis ANOVA usando la libreria pingouin

'''
fig, axs = plt.subplots(2, 2, figsize=(8, 7))
pg.qqplot(UF_2.loc[UF_2.ESTACIONES=='MED-UNNV', 'PM2.5'], dist='norm', ax=axs[0,0])
axs[0,0].set_title('MED-UNNV')
pg.qqplot(UF_2.loc[UF_2.ESTACIONES=='EST-HOSP', 'PM2.5'], dist='norm', ax=axs[0,1])
axs[0,1].set_title('EST-HOSP')
pg.qqplot(UF_2.loc[UF_2.ESTACIONES=='MED-VILL', 'PM2.5'], dist='norm', ax=axs[1,0])
axs[1,0].set_title('MED-VILL')
pg.qqplot(UF_2.loc[UF_2.ESTACIONES=='MED-BEME', 'PM2.5'], dist='norm', ax=axs[1,1])
axs[1,1].set_title('MED-BEME')
plt.tight_layout()
'''





#PRUEVA DE NORMALIZACION
P_normalizacion = pg.normality(data=UF_2, dv='PM2.5', group='ESTACIONES')


anova = pg.anova(data = UF_2, dv = 'PM2.5', between = 'ESTACIONES', detailed=True )


################################################################################################
#analisis TUKEY

TUKEY = pg.pairwise_tukey(data=UF_2, dv='PM2.5', between='ESTACIONES').round(3)