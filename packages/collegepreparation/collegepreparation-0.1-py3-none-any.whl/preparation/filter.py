class concat_filter_and_search(Cleaning_Utility):
    """
        concat, filter and search url as well as web content 
    """
    def __init__(self,  
                 college_file='./learning_data/ContentAqusition__All.csv',  
                 college_file_sep=',',
                  
                 url_lemma_file='url_sum_with_lemma.csv',
                 url_lemma_file_lemma_col='url_lemma', 
                 url_lemma_file_names=['url', 'status_code', 'url_lemma'],
                 url_sum_file_sep='\t', 
                 url_lemma_file_url='url',
                 url_lemma_file_dtype={'url':str, 'status_code':int,  'url_lemma':str},  
 
                 data_lemma_file='data_sum_with_lemma.csv', 
                 data_lemma_file_lemma_col='text_lemma',  
                 data_lemma_file_sep='\t', 
                 data_lemma_file_names=['url', 'parent', 'ps', 'ns', 'text', 'text_lemma'],
                 data_lemma_file_text='text',
                 data_lemma_file_dtype={'url':str, 'parent':str, 'ps':str, 'ns':str, 'text':str, 'text_lemma':str}, 
                 
                 default_url_cates=['admi', 'application', 'apply']  
                ):
        """
            lemmatize and search
        """    
        super().__init__()
        self.college_file=college_file
        self.college_file_sep=college_file_sep
         

        self.url_lemma_file=url_lemma_file
        self.url_lemma_file_lemma_col=url_lemma_file_lemma_col
        self.url_lemma_file_names=url_lemma_file_names
        self.url_sum_file_sep=url_sum_file_sep
        self.url_lemma_file_url=url_lemma_file_url
        self.url_lemma_file_dtype=url_lemma_file_dtype

        self.data_lemma_file=data_lemma_file
        self.data_lemma_file_lemma_col=data_lemma_file_lemma_col
        self.data_lemma_file_sep=data_lemma_file_sep
        self.data_lemma_file_names=data_lemma_file_names
        self.data_lemma_file_text=data_lemma_file_text
        self.data_lemma_file_dtype=data_lemma_file_dtype
     
    def get_college_masterdf(self):
        """
            load college file df
        """
        df_coll= pd.read_csv(self.college_file, sep=self.college_file_sep) 
        df_coll['collegeId']=df_coll['collegeId']+100000
        df_coll.rename(columns={'collegeId': 'id_college'}, inplace=True)
        return df_coll
    
    def college_filtering(self, x, colleges): #name and url . any in colleges
        """
            x: url and name. this method is used for a dataframe
            colleges: e.g., mit, massachusetts, washington
        """ 
        splits=self.parse_url(x['url'])
        splits.extend(re.split(r'[\.|/|\-|:| ]', x['name']))
        return any(w in splits for w in colleges) 
    
    def url_in_any_or_all(self, x, url_cates, any_or_all):
        """
            x: after url is parsed and splitted, match with words.  
            url_cates: e.g., admission. it uses contains. so, adm will match admission, admit etc.
        """
        if any_or_all=='any':
            return any(cate in x for cate in url_cates) 
        return all(cate in x for cate in url_cates)
    
    def text_in_any_or_all(self, x, criteria, any_or_all):
        """
            x: after url is parsed and splitted, match with words.  
            url_cates: e.g., admission. it uses contains. so, adm will match admission, admit etc.
        """
        if any_or_all=='any':
            return any(word in x for word in criteria) 
        return all(word in x for word in criteria)

    
    def filter_and_search_college(self, 
            colleges=['atsu', 'princeton', 'mit'], 
            url_cates=['admission', 'financial'],  
            any_or_all_cates='any', #all or any
            filter_by='college' ): #url, both 
        """
            filter by: college - list urls for all these colleges
            filter by: url - list all the urls that meet the criteria
            filter by url and college -- both
        """           
        df_coll=self.get_college_masterdf() 
         
        df_coll=df_coll[df_coll.apply(lambda x: self.college_filtering(x, colleges), axis=1)]
 
        #df_url=pd.read_csv(self.url_lemma_file,  sep=self.url_sum_sep)     
        #if filter_by!="college":
        #df_url=df_url.loc[df_url[self.url_sum_lemma_col].apply(lambda x: self.text_in_any_or_all(x, url_cates, any_or_all_cates))]
          
        return df_coll
    
    def filter_and_search_url(self, 
            colleges=['atsu', 'princeton', 'mit'], 
            url_cates=['admission', 'financial'],  
            any_or_all_cates='any', #all or any
            filter_by='college'):  #url, both  
        """
            filter by: college - list urls for all these colleges
            filter by: url - list all the urls that meet the criteria
            filter by url and college -- both
        """     
        df_url=pd.read_csv(self.url_lemma_file,  sep=self.url_sum_file_sep)     
        if filter_by!="college":
            df_url=df_url.loc[df_url[self.url_sum_lemma_col].apply(lambda x: self.url_in_any_or_all(x, url_cates, any_or_all_cates))]
        return df_url
    
    def filter_and_search_data(self, 
            criteria=['apply', 'delay'],
            any_or_all='any' ): #all or any   
        """
            filter by: college - list urls for all these colleges
            filter by: url - list all the urls that meet the criteria
            filter by url and college -- both
        """          
        ############## Step 1: filtering colleges ############################
   
        df_data=pd.read_csv(self.data_lemma_file,  sep=self.data_lemma_file_sep, dtype=self.data_lemma_file_dtype)  
       
        df_data=df_data.loc[df_data[self.data_lemma_file_lemma_col].apply(lambda x: self.text_in_any_or_all(x, criteria, any_or_all))]
   
        df_data[self.data_lemma_file_lemma_col]=df_data[self.data_lemma_file_lemma_col].astype(str)
        df_data= df_data.groupby('url')[self.data_lemma_file_lemma_col].agg(' '.join).reset_index() 
           
        return df_data
    