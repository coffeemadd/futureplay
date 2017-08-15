
# coding: utf-8

# In[ ]:


'''
Investor Network Analysis
'''


# In[11]:


import pandas as pd
import re
import gensim
import pickle
from datetime import datetime
from matplotlib import pyplot as plt
import networkx as nx
import numpy as np
import operator
get_ipython().magic(u'matplotlib inline')


# In[12]:


# load data
data_folder = '../data/csv_export/'
util_folder = '../util/'
df_funding_rounds = pd.read_csv(data_folder + 'funding_rounds.csv')
df_funds = pd.read_csv(data_folder + 'funds.csv')
df_investors = pd.read_csv(data_folder + 'investors.csv')
df_investments = pd.read_csv(data_folder + 'investments.csv')


# In[13]:


df_funding_rounds = df_funding_rounds[['company_uuid', 'funding_round_uuid']]
df_funding_rounds.head()


# In[14]:


df_investments = df_investments[['funding_round_uuid', 'investor_uuid']]
df_investments.head()


# In[15]:


df = df_funding_rounds.merge(df_investments, on = 'funding_round_uuid')


# In[16]:


groups = df.groupby('funding_round_uuid')['investor_uuid'].apply(list)


# In[17]:


g = nx.Graph()
# groups = df_investments.groupby('funding_round_uuid')['investor_uuid'].apply(list)


# In[20]:


# 같은 회사에 투자를 한 경우, 두 투자 회사 사이에 링크를 준다
g = nx.Graph()
for index, investors in enumerate(groups.values):
    for investor1 in investors:
        for investor2 in investors:
            if type(investor1) != str or type(investor2) != str:
                continue
            if investor1 != investor2:
                weight = 1
                if investor1 in g:
                    if investor2 in g[investor1]:
                        weight = g[investor1][investor2]['weight'] + 1
                g.add_edge(investor1, investor2, weight = weight)
with open(util_folder + 'investor_weight_network.pickle', 'w') as f:
    pickle.dump(g, f)


# In[ ]:


g = pickle.load(open(util_folder + 'investor_weight_network.pickle'))
# for n1,n2,attr in g.edges(data=True):
#     print n1,n2,attr

# reverse weights
for edge in g.edges():
    n0 = edge[0]
    n1 = edge[1]
    weight = 1 / float(g[n0][n1]['weight'])
    g.add_edge(n0, n1, weight = weight)

print 'calculating centrality'
central = nx.betweenness_centrality(g, weight = 'weight')
central = sorted(central.items(), key=operator.itemgetter(1))
central.reverse()
f = open(util_folder + 'investor_centrality_between_one_over_k.pickle', 'w')
pickle.dump(central, f)
f.close()


# In[ ]:


central = pickle.load(open(util_folder + 'investor_centrality_between_one_over_k.pickle'))
top20 = [uuid for uuid, value in central[:10]]
for i, uuid in enumerate(top20):
    print df_investors[df_investors['uuid'] == (uuid)]['investor_name'], central[i][1]


# In[ ]:


g = pickle.load(open(util_folder + 'investor_weight_network.pickle'))
# for n1,n2,attr in g.edges(data=True):
#     print n1,n2,attr

# reverse weights
for edge in g.edges():
    n0 = edge[0]
    n1 = edge[1]
    weight = 1 / np.sqrt(float(g[n0][n1]['weight']))
    g.add_edge(n0, n1, weight = weight)

print 'calculating centrality'
central = nx.betweenness_centrality(g, weight = 'weight')
central = sorted(central.items(), key=operator.itemgetter(1))
central.reverse()
f = open(util_folder + 'investor_centrality_between_one_over_sqrt_k.pickle', 'w')
pickle.dump(central, f)
f.close()


# In[ ]:


central = pickle.load(open(util_folder + 'investor_centrality_between_one_over_sqrt_k.pickle'))
top20 = [uuid for uuid, value in central[:10]]
for i, uuid in enumerate(top20):
    print df_investors[df_investors['uuid'] == (uuid)]['investor_name'], central[i][1]


# In[ ]:





# In[18]:


central = pickle.load(open(util_folder + 'investor_centrality_degree.pickle'))
top20 = [uuid for uuid, value in central[:10]]


# In[19]:


central = pickle.load(open(util_folder + 'investor_centrality_degree.pickle'))
top20 = [uuid for uuid, value in central[:10]]for i, uuid in enumerate(top20):
    print df_investors[df_investors['uuid'] == (uuid)]['investor_name'], central[i][1]


# In[ ]:




