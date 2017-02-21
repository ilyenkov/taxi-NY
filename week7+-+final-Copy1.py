
# coding: utf-8

# In[1]:

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from ipywidgets import interact
from mpl_toolkits.basemap import Basemap,cm
import datetime
from dateutil.relativedelta import relativedelta
get_ipython().magic(u'matplotlib inline')
import seaborn


# In[2]:

result=pd.read_csv('table_for_w7.csv', index_col=0, parse_dates=True)


# In[3]:

result.head()


# ### Временной ряд фактического и прогнозируемого спроса на такси

# In[4]:

regions=np.unique(result.region.values).tolist()
dates=[datetime.date(2016, 6, x) for x in range(1,31)]


# In[5]:

def fig(shift=1, region=1075, date=datetime.date(2016, 6, 1)):
    date_new = datetime.datetime.strptime(date, '%Y-%m-%d').date()
    #print date_new, type(date_new)
    r=result[(result['shift']==int(shift))&(result['region']==int(region))].shift(int(shift))
    r=r[r.index.date==date_new]
    plt.plot(r.true.values, label='actual')
    plt.plot(r.y.values, label='forecast')
    plt.xlabel('hours')
    plt.ylabel('taxi rides')
    plt.legend(loc=0)
    plt.show()


# In[6]:

interact(fig, shift=(1,6,1), region=regions, date=dates)


# ### Карта с визуализацией реального и прогнозируемого спроса на такси в выбираемый момент времени

# In[7]:

map_types=['actual','forecast','delta(a-f)']
map_dict={'actual':'true','forecast':'y','delta(a-f)':'delta'}


# In[8]:

def map_fig(shift=1, map_type='forecast', hour=0):
    date = datetime.date(2016, 6, 1) + relativedelta(hour=int(hour)%24, days=int(hour)//24)
    print 'Date-time: ', date
    col_names=['region',map_dict[map_type]]
    r=result[result['shift']==int(shift)].shift(int(shift))
    r=r[r.index==date]
    zones=np.zeros((50,50))
    for i in r[col_names].as_matrix():
        zones[int(i[0])%50,int(i[0])//50]=i[1]
    fig = plt.figure(figsize=(8,8))
    ax = fig.add_subplot(111)
    m = Basemap(resolution=None,llcrnrlat=40.49612,urcrnrlat=40.91553,llcrnrlon=-74.25559,urcrnrlon=-73.70001)
    m.arcgisimage(xpixels = 400, dpi=96, verbose=False)
    ny = zones.shape[0]; nx = zones.shape[1]
    lons, lats = m.makegrid(nx, ny) 
    x, y = m(lons, lats)
    levels=5
    step=zones.max()//levels
    clevs = [1+n*step for n in range(levels)]
    cs = m.contourf(x,y,zones,clevs,alpha=0.8, cmap='plasma')
    cbar = m.colorbar(cs,location='bottom',pad="5%")
    plt.show()


# In[9]:

interact(map_fig, shift=(1,6,1), map_type=map_types, hour=(0,713,1))


# In[ ]:



