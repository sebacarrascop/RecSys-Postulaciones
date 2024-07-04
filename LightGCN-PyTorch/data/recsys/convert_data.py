import pandas as pd

def convert_users(df: pd.DataFrame, user_col: str) -> pd.DataFrame:
    users = df[user_col].unique()
    user_map = {user: i for i, user in enumerate(users)}
    new_df = pd.DataFrame({'org_id': users, 'remap_id': user_map.values()})
    with open(f'user_list.txt', 'w') as f:
        f.write('org_id remap_id\n')
        for user, i in user_map.items():
            f.write(f'{user} {i}\n')
    return new_df

def convert_items(df: pd.DataFrame, item_col: str) -> pd.DataFrame:
    items = df[item_col].unique()
    item_map = {item: i for i, item in enumerate(items)}
    new_df = pd.DataFrame({'org_id': items, 'remap_id': item_map.values()})
    with open(f'item_list.txt', 'w') as f:
        f.write('org_id remap_id\n')
        for item, i in item_map.items():
            f.write(f'{item} {i}\n')
    return new_df

def convert_train(df_users: pd.DataFrame, df_items: pd.DataFrame, df: pd.DataFrame, user_col: str, item_col: str) -> pd.DataFrame:
    # Merge users and items into the main dataframe and keep the remapped IDs
    df = df.merge(df_users[['org_id', 'remap_id']], left_on=user_col, right_on='org_id', how='left')
    df = df.rename(columns={'remap_id': 'user_remap_id', 'org_id': 'user_org_id'})
    
    df = df.merge(df_items[['org_id', 'remap_id']], left_on=item_col, right_on='org_id', how='left')
    df = df.rename(columns={'remap_id': 'item_remap_id', 'org_id': 'item_org_id'})
    
    # Select only the relevant columns (remap_id from users and items)
    df = df[['user_remap_id', 'item_remap_id']]
    df.columns = ['user', 'item']
    
    # Open the train.txt file and write the user-item pairs
    with open('train.txt', 'w') as f:
        for user in df['user'].unique():
            items = df[df['user'] == user]['item'].tolist()
            items_str = ' '.join(map(str, items))
            f.write(f'{user} {items_str}\n')
    
    return df

def convert_test(df_users: pd.DataFrame, df_items: pd.DataFrame, df: pd.DataFrame, user_col: str, item_col: str) -> pd.DataFrame:
    # Merge users and items into the main dataframe and keep the remapped IDs
    df = df.merge(df_users[['org_id', 'remap_id']], left_on=user_col, right_on='org_id', how='left')
    df = df.rename(columns={'remap_id': 'user_remap_id', 'org_id': 'user_org_id'})
    
    df = df.merge(df_items[['org_id', 'remap_id']], left_on=item_col, right_on='org_id', how='left')
    df = df.rename(columns={'remap_id': 'item_remap_id', 'org_id': 'item_org_id'})
    
    # Select only the relevant columns (remap_id from users and items)
    df = df[['user_remap_id', 'item_remap_id']]
    df.columns = ['user', 'item']
    
    # Open the train.txt file and write the user-item pairs
    with open('test.txt', 'w') as f:
        for user in df['user'].unique():
            items = df[df['user'] == user]['item'].tolist()
            items_str = ' '.join(map(str, items))
            f.write(f'{user} {items_str}\n')
    
    return df

# Load users from file csv
users = pd.read_csv('postulantes_procesados.csv')
df_users = convert_users(users, 'MRUN')

# Load items from file csv
items = pd.read_csv('establecimientos_procesados.csv')
df_items = convert_items(items, 'RBD')

# Load train data from file csv
# train = pd.read_csv('postulaciones_training.csv')
# df_train = convert_train(df_users, df_items, train, 'MRUN', 'RBD')

# Load test data from file csv
test = pd.read_csv('postulaciones_testing.csv')
df_test = convert_test(df_users, df_items, test, 'MRUN', 'RBD')

