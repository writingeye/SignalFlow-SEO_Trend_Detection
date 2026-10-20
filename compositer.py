import pandas as pd 

def composite(df):

    df_y = (df
        .assign(y=df[KEYWORD] * df['source'].map(WEIGHTS))
        .groupby('date', as_index=False)['y']
        .sum()
        .rename(columns={"date": "ds"})
        )
    df_y["ds"] = pd.to_datetime(df_y["ds"]) 

    return df_y 
