def savePostgres(df,tb,host,port,user,pwd,db):
    from sqlalchemy import create_engine
    import pandas as pd
    url=r'postgresql://'+user+':'+pwd+'@'+host+':'+str(port)+r'/'+db
    engine = create_engine(url)
    df.to_sql(tb, engine)