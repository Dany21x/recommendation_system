import pandas as pd
from sklearn.metrics.pairwise import cosine_similarity
from sklearn.feature_extraction.text import TfidfVectorizer
from sqlalchemy.orm import Session
from app.models.user_preference import UserPreference
from app.models.purchase import Purchase
from app.database import get_db
from fastapi import Depends

def transform_to_df(query_data):
    # Transform query data in dataframe to analyze
    data = []
    for purchase, product in query_data:
        data.append({
            'id_user': purchase.id_user,
            'id_product': purchase.id_product,
            'purchase_date': purchase.purchase_date,
            'price': purchase.price,
            'description': product.description
        })

    return pd.DataFrame(data)
def segment_customer(df):

    df['purchase_date'] = pd.to_datetime(df['purchase_date'], format='%d/%m/%Y')#format='%Y-%m-%d'
    df['id_product'] = df['id_product'].astype(str)

    NOW = df['purchase_date'].max()
    rfmTable = df.groupby('id_user').agg({'purchase_date': lambda x: (NOW - x.max()).days, 'id_product': lambda x: len(x), 'price': lambda x: x.sum()})
    rfmTable['purchase_date'] = rfmTable['purchase_date'].astype(int)
    rfmTable.rename(columns={'purchase_date': 'recency',
                             'id_product': 'frequency',
                             'price': 'monetary_value'}, inplace=True)

    rfmTable['r_quartile'] = pd.qcut(rfmTable['recency'], q=4, labels=range(1, 5), duplicates='raise')
    rfmTable['f_quartile'] = pd.qcut(rfmTable['frequency'], q=4, labels=range(1, 5), duplicates='drop')
    rfmTable['m_quartile'] = pd.qcut(rfmTable['monetary_value'], q=4, labels=range(1, 5), duplicates='drop')

    rfmTable['r_quartile'] = rfmTable['r_quartile'].astype(str)
    rfmTable['f_quartile'] = rfmTable['f_quartile'].astype(str)
    rfmTable['m_quartile'] = rfmTable['m_quartile'].astype(str)

    rfmTable['RFM_score'] = rfmTable['r_quartile'] + rfmTable['f_quartile'] + rfmTable['m_quartile']

    rfmTable['customer_segment'] = 'Other'
    rfmTable.loc[rfmTable['RFM_score'].isin(['334', '443', '444', '344', '434', '433', '343', '333']), 'customer_segment'] = 'Premium Customer' #nothing <= 2
    rfmTable.loc[rfmTable['RFM_score'].isin(['244', '234', '232', '332', '143', '233', '243']), 'customer_segment'] = 'Repeat Customer' # f >= 3 & r or m >=3
    rfmTable.loc[rfmTable['RFM_score'].isin(['424', '414', '144', '314', '324', '124', '224', '423', '413', '133', '323', '313', '134']), 'customer_segment'] = 'Top Spender' # m >= 3 & f or m >=3
    rfmTable.loc[rfmTable['RFM_score'].isin(['422', '223', '212', '122', '222', '132', '322', '312', '412', '123', '214']), 'customer_segment'] = 'At Risk Customer' # two or more  <=2
    rfmTable.loc[rfmTable['RFM_score'].isin(['411', '111', '113', '114', '112', '211', '311']), 'customer_segment'] = 'Inactive Customer' # two or more  =1

    return rfmTable.reset_index()

def generate_recommendations(target_customer, cohort, num_recommendations=5):
    user_item_matrix = cohort.groupby('id_user')['id_product'].apply(lambda x: ', '.join(x)).reset_index()
    user_item_matrix['description'] = cohort.groupby('id_user')['description'].apply(lambda x: ', '.join(x)).reset_index()['description']
    tfidf = TfidfVectorizer()
    tfidf_matrix = tfidf.fit_transform(user_item_matrix['description'])
    similarity_matrix = cosine_similarity(tfidf_matrix)
    target_customer_index = user_item_matrix[user_item_matrix['id_user'] == target_customer].index[0]
    similar_customers = similarity_matrix[target_customer_index].argsort()[::-1][1:num_recommendations+1]
    target_customer_purchases = set(user_item_matrix[user_item_matrix['id_user'] == target_customer]['id_product'].iloc[0].split(', '))
    recommendations = []
    for customer_index in similar_customers:
        customer_purchases = set(user_item_matrix.iloc[customer_index]['id_product'].split(', '))
        new_items = customer_purchases.difference(target_customer_purchases)
        recommendations.extend(new_items)

    return list(set(recommendations))[:num_recommendations]

