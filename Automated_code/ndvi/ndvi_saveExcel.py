def dfToCSV(dirs,filename,df):
    import pandas as pd
    df.to_csv(dirs+filename+'.csv', sep=',', encoding='utf-8')