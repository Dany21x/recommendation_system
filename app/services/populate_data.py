from app.database import engine, Base
import pandas as pd

files_dict = {
    'categories': 'categories.csv',
    'products': 'products.csv',
    'users': 'users.csv',
    'user_preferences': 'user_preferences.csv',
    'purchases': 'purchases.csv'
}

column_name = 'purchase_date'

def import_data(file, table):

    df = pd.read_csv(f'resources/{file}')

    if column_name in df.columns:
        df[column_name] = pd.to_datetime(df[column_name], format='%d/%m/%Y')
        df[column_name] = df[column_name].dt.strftime('%Y-%m-%d')

    df.to_sql(table, con=engine, schema='recommendation_system', if_exists='append', index=False)

    return {"message": f"Tabla {table} importada exitosamente"}

def populate_data():

    for key, value in files_dict.items():
        import_data(value, key)