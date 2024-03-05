# Proyecto individual

![1709664288680](image/README/1709664288680.png)

## Índice

1. Presentación
2. Requerimientos
3. Uso
4. Adicional
5. Información de contacto

## Presentación

Se encuentran los archivos competentes sobre un sistema de recomendaciones para juegos de la plataforma STEAM, dentro de una parte de su catálogo junto con reviews de usuarios como también usuarios con su lista de juegos que les pertenecen

## Requerimientos

Al momento de querer implementar directamente con los recursos presentes, necesita:

1. pandas
2. numpy
3. ntlk
4. scikit-learn
5. matplotlib
6. pyarrow
7. seaborn

```bash
pip install pandas numpy nltk matplotlib pyarrow scikit-learn seaborn
```

Entender que estas dependencias funcionan con todos los archivos presentes.

## Uso

* Copiar el repositorio en su máquina local.

  ```
  git clone https://github.com/jaraycode/steam_games_mlops2.git
  ```
* Activar un entorno virtual (virtualenv).

  ```
  python -m virtualenv venv
  ```
* Activar el entorno virtual.

  ```
  source venv/bin/activate
  ```
* Descargar los requerimientos existentes en el archivo requirement.txt.

  ```
  pip install -r requirement.txt
  ```
* Usar el siguiente comando para iniciar la API.

  ```
  uvicorn app:app --host 127.0.0.1 --port 8000
  ```
* Ingresar a "http://127.0.0.1:8000/docs" para poder visualizar todas las consultas disponibles.

## Adicional

Una vez realizado los pasos en el apartado anterior se podrán encontrar las siguientes consultas

* `/developer`: a partir del nombre de una desarrolladora retorna el año de lanzamiento y la cantidad de juegos registrados por esos años, así como el porcentaje de los que son gratis.
* `/userForGenre`: a partir de un genero retorna el usuario que más tiempo de juego tiene, listado por el tiempo que jugo por año.
* `/userData`: a partir del id de un usuario retorna el dinero que ha gastado así como también la cantidad de juegos que tiene y el % de recomendaciones que ha hecho en la plataforma.
* `/best_developer_year`: a partir de una año retorna los desarrolladoresde videojuegos que tuvieron las mejores recomendaciones.
* `/developer_reviews_analysis`: buscas a tu empresa desarrolladora favorita y te genera cuantos comentarios negativos y positivos ha tenido según los datos disponibles.
