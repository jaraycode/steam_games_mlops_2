from fastapi import FastAPI
import pandas as pd
from typing import Union

app = FastAPI()

@app.get('/Developer/{dev:str}')
def Developer(dev: Union[str,None] = None):
    if dev == None:
        return {'error':f'No se entregaron los parámetros necesarios para procesar su información, intentar de nuevo.'}
    pass

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
        regreso = users[users['genres'] == genre].max()
        return {f'Usuario con más horas jugadas para el genero {genre}':regreso['user_id'], 'Horas jugadas: (año:horas)':regreso['playtime_forever']}
    else:
        return {"Error":"No ha sido posible encontrar la información"}

@app.get('/best_developer_year/{year:int}')
def best_developer_year(year: Union[int,None] = None):
    if year == None:
        return {'error':f'No se entregaron los parámetros necesarios para procesar su información, intentar de nuevo.'}
    pass

@app.get('/developer_review_analysis/{dev:str}')
def developer_review_analysis(dev: Union[str,None] = None):
    if dev == None:
        return {'error':f'No se entregaron los parámetros necesarios para procesar su información, intentar de nuevo.'}
    pass