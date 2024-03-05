from fastapi import FastAPI
import pandas as pd
from typing import Union

app = FastAPI()

@app.get('/Developer/{dev:str}')
def Developer(dev: Union[str,None] = None):
    if dev == None:
        return {'error':f'No se entregaron los parámetros necesarios para procesar su información, intentar de nuevo.'}
    priced = pd.read_parquet('DatasetFinal/games_priced.parquet')
    df_dev = priced[priced['developer'] == dev].value_counts(['price','año'])
    df_consulta = pd.DataFrame(df_dev)
    df_consulta.reset_index(inplace=True)
    df_consulta.sort_values('año', inplace=True)
    lista = []
    for df in df_consulta['año'].unique():
        aux = df_consulta[df_consulta['año'] == df]
        total = aux['count'].sum()
        free = aux[aux['price'] == 0.00]
        if free.empty:
            lista.append({'Año':df, 'Cantidad de items':total.item(), 'Contenido Free':f'{0}%'})
        else:
            lista.append({'Año':df, 'Cantidad de items':total.item(), 'Contenido Free':f'{round(free['count'].sum()*100/total,2).item()}%'})
    print(lista)
    return lista

@app.get('/User_Data/{user_id:str}')
def User_Data(user_id: Union[str,None] = None):
    if user_id == None:
        return {'error':f'No se entregaron los parámetros necesarios para procesar su información, intentar de nuevo.'}
    pass

@app.get('/UserForGenre/{genre:str}')
def UserForGenre(genre: Union[str,None] = None):
    '''
    A partir de un genero de juego que se pase por medio de una petición https, dentro de los generos presentes en los archivos usados me regresa el usuario que más horas tiene en dicho genero.

    En caso de no existir el genero dentro de nuestra información envía información nula.
    '''
    if genre == None:
        return {'error':f'No se entregaron los parámetros necesarios para procesar su información, intentar de nuevo'}
    pass

    users = pd.read_parquet('DatasetFinal/UserForGenre.parquet')

    if genre in users['genres'].unique():
        regreso = users[users['genres'] == genre]
        regreso = regreso[regreso['user_id'] == regreso.max()['user_id']]
        regreso['playtime_forever'] = regreso['playtime_forever'].apply(lambda x : round(x,0))
        regreso.set_index('año',inplace=True)
        regreso2 = regreso.to_dict()

        return {f'Usuario con más horas jugadas para el genero {genre}':regreso.max()['user_id'], 'Horas jugadas: (año:horas)':regreso2['playtime_forever']}
    else:
        return {"Error":"No ha sido posible encontrar la información"}

@app.get('/best_developer_year/{year:int}')
def best_developer_year(year: Union[int,None] = None):
    '''A partir del parámetro de año retorna el top 3 peores desarrolladores según las recomendaciones de los usuarios'''
    if year == None:
        return {'error':f'No se entregaron los parámetros necesarios para procesar su información, intentar de nuevo.'}
    
    developer = pd.read_parquet('DatasetFinal/games.parquet')
    recomendacion = pd.read_parquet('DatasetFinal/reviews.parquet')

    developer_year = developer[developer['año'] == str(year)]

    if developer_year.empty:
        return {'error':f'No existen juegos en el año seleccionado. Año:{year}'}

    recomendaciones = []
    for i in developer_year['id']:
        scores = recomendacion[recomendacion['item_id'] == i]
        value = scores['recommend'].value_counts()
        sentiment = scores['sentiment'].value_counts()
        if sentiment.empty:
            if value.empty:
                continue
            else:
                if value.__len__() == 1:
                    j = value.keys()
                    for k in j:
                        if (not k):
                            recomendaciones.append({"id":i,"value":value[False]})
                else:
                    recomendaciones.append({"id":i,"value":value[False]})
        else:
            if value.empty:
                continue
            else:
                if value.__len__() == 1:
                    j = value.keys()
                    s = sentiment.keys()
                    aux = 0
                    for s2 in s:
                        if s2 == 0:
                           aux = sentiment[0] 
                    for k in j:
                        if (not k):
                            recomendaciones.append({"id":i,"value":value[False] + aux})
                else:
                    s = sentiment.keys()
                    aux = 0
                    for s2 in s:
                        if s2 == 0:
                           aux = sentiment[0] 
                    recomendaciones.append({"id":i,"value":value[False] + aux})
    
    recomendaciones = sorted(recomendaciones, reverse=True, key= lambda x:x['value'])
    nombres = []
    for i in recomendaciones[0:3]:
        df = developer_year[developer_year['id'] == i['id']]
        nombres.append(df['developer'].values)
    return [{'Puesto 1': nombres[0][0]}, {'Puesto 2': nombres[1][0]}, {'Puesto 3': nombres[2][0]}]

@app.get('/developer_review_analysis/{dev:str}')
def developer_review_analysis(dev: Union[str,None] = None):
    '''Se necesita el nombre de la empresa desarrolladora para retornar un diccionario que contenga una lista de la categorización de los reviews que los usuarios le ha dado a la misma de manera tal que: [positivo=,neutro=,negativo=]'''
    if dev == None:
        return {'error':f'No se entregaron los parámetros necesarios para procesar su información, intentar de nuevo.'}
    
    developer = pd.read_parquet('DatasetFinal/games.parquet')
    recomendacion = pd.read_parquet('DatasetFinal/reviews.parquet')

    developer_year = developer[developer['developer'] == dev]

    if developer_year.empty:
        return {'error':f'No existen el desarrollador seleccionado. Año:{dev}'}
    
    developer_filtered = developer[developer['developer'] == dev]

    if developer_filtered.empty:
        return {'error': f'La empresa desarrolladora no existe en los datos actuales. Empresa {dev}'}
    
    sentiment_total = []
    for game in developer_filtered['id']:
        scores = recomendacion[recomendacion['item_id'] == game]
        sentiment = scores['sentiment'].value_counts()
        if sentiment.empty:
            continue
        else:
            print(sentiment)
            pos = 0
            neg = 0
            neu = 0
            if sentiment.__len__() == 3:
                sentiment_total.append({"neg":sentiment[0],"neu":sentiment[1],"pos":sentiment[2]})
            elif sentiment.__len__() < 3:
                for s in sentiment:
                    if s == 2:
                        pos = s
                    elif s == 1:
                        neu = s
                    elif s == 0:
                        neg = s
                sentiment_total.append({"neg":neg,"neu":neu,"pos":pos})

    positivo = 0
    negativo = 0

    for s in sentiment_total:
        positivo += s['pos']
        negativo += s['neg']

    return {f'{dev}': [f'Negativo = {negativo}', f'Positivo = {positivo}']}