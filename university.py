
# coding: utf-8

# ## code for scrapying Indian Universities Ranking 

# In[30]:


#importing of all libraries
from bs4 import BeautifulSoup
import requests
import pandas as pd
from urllib.parse import urlparse

#directory
directory="india_university"

#function for scrapying data
def create_csv_file():
    #weblink
    value = 'http://www.webometrics.info/en/Asia/India'
    
    #flag set
    flag=True
    
    #dataframe for making table 
    india_university = pd.DataFrame()
    
    #print("indian_unversities :" ,india_university.head())
    
    while flag:
        #print(value)
        
        page_request=requests.get(value)
            
        search_page = BeautifulSoup(page_request.content,'html.parser')
        
        elements=search_page.find('table',class_='sticky-enabled')
       
        rows = elements.find_all('tr')
        
        data=[]
        
        #fetching of each row in column
        for row in rows:
            
            cols = row.find_all('td')
            
            v=[ele.text.strip() for ele in cols]
            
            cols =[ele.text.strip() for ele in cols]
            
            data.append([ele for ele in cols if ele])
            
            #print(cols)
            
            cols=pd.Series(cols)
            
            india_university=india_university.append(cols,ignore_index=True)
       
        nextpage_p=search_page.find('ul',class_='pager')
        
        if nextpage_p: 
            
            next_page = nextpage_p.find('li',class_= 'pager-next')
            #print("\n")
            if next_page:
                
                url="http://www.webometrics.info"
                
                value=url+next_page.a['href']
                
            else:
                
                break
                
                flag=False
    
    india_university.to_csv("output.csv", index=False,sep='\t')
    

#executing above functions
if __name__ == '__main__':
    
    print("process start...........")
    #function calling
    create_csv_file()
    
    #preprocessing
    india_universitys=pd.read_csv("output.csv",delimiter='\t')
    india_universitys.columns = ['ranking', 'world_rank','university','detail','presence_rank','impact_rank','openness_rank','excellence_rank']
    cols = india_universitys.columns[india_universitys.isna().any()]
    india_universitys.drop_duplicates(subset ="ranking",keep = False, inplace = True) 
    india_universitys=india_universitys.dropna(axis=1,how='all')
    #print(india_universitys)
    india_universitys=india_universitys.dropna(axis=0,how='all')
    india_universitys.to_csv("output.csv",index=False)
    #print(cols)
    
    print("successful.......")

