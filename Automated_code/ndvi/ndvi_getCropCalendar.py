
def get_crop_calendar(df_cord,df_ndvi,sm_frac):    
    import numpy as np
    import pandas as pd
    import geopandas as gpd
    import numpy as np
    import matplotlib.pyplot as plt
    import statsmodels.api as sm
    from scipy.signal import argrelextrema
    from datetime import datetime
    lowess = sm.nonparametric.lowess
    all_max=[]
    all_min=[]
    for col in df_ndvi:
        yran=df_ndvi[col].values.tolist()
        index=df_ndvi[col].index.tolist()
        Idx=len(df_ndvi[col].index.tolist())
        x=list(range(Idx))
        w=lowess(np.asarray(yran), np.asarray(x), frac=sm_frac, it=100, delta=0.2, is_sorted=False, missing='drop', return_sorted=True)
        sm_x=[]
        sm_y=[]
        for el in w:
            sm_x.append(el[0])
            sm_y.append(el[1])
        plt.plot(sm_x,sm_y) 
        plt.plot(x,yran,'bo')
        plt.savefig("D:\\plot_lowess.png")
        peaks=argrelextrema(np.asarray(sm_y), np.greater)[0]
        lows=argrelextrema(np.asarray(sm_y), np.less)[0]
        #print(col)
        i=0
        j=0        

        for peak in peaks:
            i+=1
            max_lis=[col,df_cord.loc[ col , 'LON'],df_cord.loc[ col , 'LAT']]
            max_date_new=datetime.strptime(index[peak],'%Y-%m-%d')
            max_date=max_date_new.strftime("%y%m%d")
            max_ndvi=sm_y[peak]
            max_lis.append(max_date)
            #max_lis.append(max_date)
            max_lis.append(max_ndvi)
            max_lis.append("--")
            max_lis.append("--")
            max_lis.append("season_max_"+str(i))
            all_max.append(max_lis)
            #df2 = pd.DataFrame(max_lis, columns=['Pixel Number','X','Y','Max_date','Max_NDVI'])
            #print(df2)
        for low in lows:
            j+=1
            min_lis=[col,df_cord.loc[ col , 'LON'],df_cord.loc[ col , 'LAT'],'--','--']
            min_date_new=datetime.strptime(index[low],'%Y-%m-%d')
            min_date=min_date_new.strftime("%y%m%d")
            min_ndvi=sm_y[low]
            min_lis.append(min_date)
            min_lis.append(min_ndvi)
            min_lis.append("season_min_"+str(j))
            all_min.append(min_lis)
    print(all_max+all_min)
    crop_cal = pd.DataFrame(all_max+all_min,columns=['Pixel Number','X','Y','Max_date','Max_NDVI','Min_date','Min_NDVI','Season'])
    return crop_cal
