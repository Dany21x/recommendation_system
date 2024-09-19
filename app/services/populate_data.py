from app.database import engine, Base
import pandas as pd
import os

files_dict = {
    'categories': 'categories.csv',
    'products': 'products.csv',
    'users': 'users.csv',
    'user_preferences': 'user_preferences.csv',
    'purchases': 'purchases.csv'
}

column_name = 'purchase_date'

def import_data(file, table):

    current_dir = os.path.dirname(os.path.abspath(__file__))  # Esto da la ruta de `populate_data.py`
    file_path = os.path.join(current_dir, '..', 'resources', file)  # Navega hacia el directorio de resources
    df = pd.read_csv(file_path)

    if column_name in df.columns:
        df[column_name] = pd.to_datetime(df[column_name], format='%d/%m/%Y')
        df[column_name] = df[column_name].dt.strftime('%Y-%m-%d')

    df.to_sql(table, con=engine, schema='recommendation_system', if_exists='append', index=False)

    return {"message": f"Tabla {table} importada exitosamente"}

def populate_data():

    for key, value in files_dict.items():
        import_data(value, key)