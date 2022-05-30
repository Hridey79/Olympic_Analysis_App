import pandas as pd

def preprocessing(df,regions):
    df=df.merge(regions,on="NOC",how='left')
    df.drop_duplicates(inplace=True);
    df=pd.concat([df,pd.get_dummies(df['Medal'])],axis=1)
    return df