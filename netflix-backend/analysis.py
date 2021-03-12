import pandas as pd
import pymysql

from datetime import datetime
from my_settings import db_connection
from sqlalchemy import create_engine


def top_ten_video():
    today = datetime.today()
    date = today - timedelta(days=7)
    
    query = '''
    SELECT watched_movies.movie_id, watched_movies.series_id
    CASE WHEN movie_id IS NULL THEN 's'+series_id
    ELSE 'm'+movie_id
    END AS video
    FROM watched_movies
    WHERE registered_at >= date
    '''
    df = pd.read_sql(query, con=db_connection)
    top_ten = df['video'].value_counts().head(10)
    dic = dict(top_ten)
    
    ls = []
    for k,v in dic.items():
        ls.append(k)

    return ls

