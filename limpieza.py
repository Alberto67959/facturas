import pandas as pd

df1=pd.read_csv("clientes.csv")
df2=pd.read_csv("facturas.csv")

def clasificar(dias):
    if dias>60:
        return "urgente"
    elif dias>30:
        return "recordatorio"
    elif dias>15:
        return "amistoso"

    return "ninguno"


df2["cliente"]=df2["cliente"].str.strip()

suma_importes=df2.groupby("cliente")["importe"].sum().reset_index()

suma_importes=suma_importes.rename(columns={"importe":"deuda_total"})

num_facturas=df2.groupby("cliente")["importe"].count().reset_index()

num_facturas=num_facturas.rename(columns={"importe":"numero_facturas"})



df2["avisos"]=df2["dias_retraso"].apply(clasificar)

diccionario={"ninguno": 0,"amistoso":1,"recordatorio":2,"urgente":3}

df2["nivel"]=df2["avisos"].map(diccionario)

peores_avisos=df2.groupby("cliente")["nivel"].max()

diccionario_invertido={0:"ninguno",1:"amistoso",2:"recordatorio",3:"urgente"}


peores_avisos=peores_avisos.map(diccionario_invertido)
peores_avisos=peores_avisos.reset_index()

informe=suma_importes.merge(df1,on="cliente",how="left").merge(num_facturas,on="cliente").merge(peores_avisos,on="cliente")

informe=informe.rename(columns={"nivel":"peor_aviso"})
print(informe)


informe.to_csv("informe_final.csv",index=False)