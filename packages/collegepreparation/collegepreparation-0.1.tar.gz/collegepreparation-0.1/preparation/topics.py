class college_topics(Cleaning_Utility):
    """
    Task A: Practice part -- goal is to identify admission focus for each university. 
        step 1). starts simple - two labels. This can be achieved from [parsing URL and looking for key words in web content]. We will need high precision on Admission label. 
            label all web pages to three categories only: Admission / Other 
        step 2). Topics for admission for each university. 
            we use LDA and NMF for topics among 2000 colleges for few rounds: keep removing non-esscential frequent words
            for our final topic model, review and define final number of topics from both metrics and relevancy 
        step 3). look for some students' essays for topic inference.         
    """
    def __init__(self, 
        strict=True,  
                 college_file='C:\\Stempro\\Notebooks\\final_data\\ContentAqusition__All.csv',
                 college_sep=',',
                 processed_url_sum_file='C:\\Stempro\\Notebooks\\final_data\\url_sum_with_lemma.csv', 
                 reprocess_url_sum_file=False, 
                 url_sum_file='C:\\Stempro\\Notebooks\\final_data\\url_sum.csv', 
                 url_sum_lemma_col='url_lemma', 
                 url_sum_names=['entries', 'id_college', 'id_url', 'textlen', 'url'],
                 url_sum_sep='\t', 
                 url_sum_url='url',
                 url_sum_dtype={'entries':int, 'id_college':int, 'id_url':int, 'textlen':int, 'url':str}, 
                 raw_data_folder='C:\\Stempro\\Notebooks\\data', 
                 raw_data_sep='\t', 
                 raw_data_pattern=r'^A.+\d+.csv', 
                 lemma_data_lemma_col='text_lemma', 
                 lemma_data_save_file_mark='lemma', 
                 lemma_data_patter=r'^A.+lemma.csv',         
                 model_folder='C:\\Stempro\\Notebooks\\models\\',
                 default_full_corpus_file='C:\\Stempro\\Notebooks\\models\\adm_college_corpus.pkl', 
                 default_dic_file= 'C:\\Stempro\\Notebooks\\models\\adm_college_dictionary.gensim', 
                 default_model='C:\\Stempro\\Notebooks\\models\\adm_lda.model', 
                 default_url_cates=['admi', 'application', 'apply'], 
                 min_count=5, 
                 threshold=100
                ):
        """
            when self.is_default_corpus_dic_ready==False: need to explicitly run:
                prepare_dictionary(self, df=None, dic_prefix=None, url_cates=default_url_cates)
        """
        super().__init__(strict=strict)          
        self.college_file=college_file
        self.college_sep=college_sep
        
        self.default_corpus=default_full_corpus_file 
        self.default_dic=default_dic_file  
        self.default_model=default_model
        
        self.default_url_cates=default_url_cates
        
        self.default_full_corpus_file=default_full_corpus_file
        self.default_dic_file=default_dic_file
        
        self.min_count=min_count
        self.threshold=threshold
        
        self.bigram_mod=None
        self.trigram_mod=None
        
        if (path.isfile(self.default_full_corpus_file)==False) or  (path.isfile(self.default_dic_file)==False):
            self.is_default_corpus_dic_ready=False
        else:
            self.is_default_corpus_dic_ready=True                  
        
        self.model=None 
        self.docs=None
        
        self.processed_url_sum_file=processed_url_sum_file
        self.url_sum_lemma_col=url_sum_lemma_col
        self.url_sum_file=url_sum_file
        self.url_sum_sep=url_sum_sep
        self.url_sum_dtype=url_sum_dtype
        self.url_sum_names=url_sum_names
        self.url_sum_url=url_sum_url
        
        self.raw_data_folder=raw_data_folder
        self.raw_data_sep=raw_data_sep
        self.raw_data_pattern=raw_data_pattern
        
        self.lemma_data_lemma_col=lemma_data_lemma_col
        self.lemma_data_save_file_mark=lemma_data_save_file_mark
        
        """
            if strict: only take isalnum. 
            corpus, dictionary, model and docs: used for Topic
        """ 
        if (path.isfile(processed_url_sum_file)==False) or reprocess_url_sum_file: 
            self.processed_url_sum_file=self.process_sum_url_file()
       
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
    
    def get_college_masterdf(self):
        """
            load college file df
        """
        df_coll= pd.read_csv(self.college_file, sep=self.college_sep) 
        df_coll['collegeId']=df_coll['collegeId']+100000
        df_coll.rename(columns={'collegeId': 'id_college'}, inplace=True)
        return df_coll
      
    def process_sum_url_file(self):
        """
            since url_sum files will be frequently searched, process a lemmatized copy.            
        """  
        df=pd.read_csv(self.url_sum_file,sep=self.url_sum_sep,dtype= self.url_sum_dtype)
        df[self.url_sum_lemma_col]=df[self.url_sum_url].apply(lambda x:self.parse_url(x, return_type='list')) 
        df.to_csv(self.processed_url_sum_file, index=False, sep='\t')

    def process_data_file_lemmatize_all(self, return_type='sentence', text_col='text', 
                                         re_process=False, sep='\t'):
        """
            save all lemmatized files. expensive operation
        """
        files=[path.join(self.raw_data_folder, f) for f in listdir(self.raw_data_folder) if re.match(self.raw_data_pattern, f) ]
        for f in files:             
            lemmafile=path.join(path.dirname(f),path.basename(f).replace('.csv', self.lemma_data_save_file_mark+'.csv'))
            df=pd.read_csv(f, sep=sep)
            df[text_col]=df[text_col].astype(str)
            df[self.lemma_data_lemma_col]=pd.Series(df.loc[:,text_col].apply(lambda x:self.clean_sentence(x, return_type=return_type)))
            df.to_csv(lemmafile, index=False, sep=sep)
                 
    def prepare_texts_by_college_url(self, 
            colleges=['atsu', 'princeton', 'mit'], 
            url_cates=['admission', 'sat'],  
            any_or_all_cates='any', #all or any
            filter_by='college',  #url, both 
            is_test=True ):  
        """
            filter by: college - list urls for all these colleges
            filter by: url - list all the urls that meet the criteria
            filter by url and college -- both
        """  
        
        ############## Step 1: filtering colleges ############################
        df_coll=self.get_college_masterdf() 
        if (len(colleges)>0) and (filter_by !='url'):
            #df_coll=df_coll[df_coll['name'].str.contains('|'.join(colleges),regex=True,flags=re.IGNORECASE )] 
            df_coll=df_coll[df_coll.apply(lambda x: self.college_filtering(x, colleges), axis=1)]
        
        ############## Step 2: url file ############################ 
        if is_test==True:
            df_url=pd.read_csv(self.processed_url_sum_file,nrows=10, sep=self.url_sum_sep)  
        else:
            df_url=pd.read_csv(self.processed_url_sum_file,  sep=self.url_sum_sep)     
        if filter_by!="college":
            df_url=df_url.loc[df_url[self.url_sum_lemma_col].apply(lambda x: self.url_in_any_or_all(x, url_cates, any_or_all_cates))]
 
        ############### Step 3: college and url ###############
        if filter_by!="both": 
            colleges_files=[ path.join(self.raw_data_folder, 'A_'+str(i)+self.lemma_data_save_file_mark+'.csv') for i in df_coll['id_college'].unique()]
        elif filter_by=="url":
            colleges_files=[ path.join(self.raw_data_folder, 'A_'+str(i)+self.lemma_data_save_file_mark+'.csv') for i in df_url['id_college'].unique()]
        else: #both
            df_merge=df_coll.merge(df_url, left_on='id_college', right_on='id_college', how='inner').reset_index()
            colleges_files=[ path.join(self.raw_data_folder, 'A_'+str(i)+self.lemma_data_save_file_mark+'.csv') for i in df_merge['id_college'].unique()]
            del(df_merge)  
        
        ##################### now colleges_files and df_url are used for loop #####################
        df_text_full=pd.DataFrame()
        for lemmafile in colleges_files:
            if path.isfile(lemmafile)==True:
                id_college=int(re.sub("[^0-9]", "", path.basename(lemmafile))) 
                df_filtered=pd.read_csv(lemmafile, sep=self.raw_data_sep)
                df_filtered=df_filtered.merge(df_url[df_url.id_college==id_college], left_on='url', right_on='url', how='inner')
                df_text_full=pd.concat([df_text_full,df_filtered ], axis=0)
         
        #dffff[['url_lemma', 'id_college', 'url', 'text_lemma']] 
        df_text_full[self.lemma_data_lemma_col]=df_text_full[self.lemma_data_lemma_col].astype(str)
        df_text_full=df_text_full.groupby(['id_college', 'url', 'url_lemma'])[self.lemma_data_lemma_col].agg(' '.join).reset_index() 
           
        return df_text_full
    
    def multigram(self,word_pool):
        """
            creating a bigram/trigram generator
        """
        bigram = gensim.models.Phrases(word_pool, min_count=self.min_count, threshold=self.threshold)  
        trigram = gensim.models.Phrases(bigram[word_pool], threshold=self.threshold)
        self.bigram_mod = gensim.models.phrases.Phraser(bigram)
        self.trigram_mod = gensim.models.phrases.Phraser(trigram) 
    
    def make_bigrams(self,texts):
        """
            generate bigrams
        """
        return [self.bigram_mod[doc] for doc in texts]
    
    def make_trigrams(self,texts):
        return [self.trigram_mod[bigram_mod[doc]] for doc in texts]

    def prepare_texts_by_url(self,  
            url_cates=['admission', 'sat'],  
            any_or_all_cates='any', #all or any
            filter_by='url',  #url, both 
            is_test=False ):  
        return self.prepare_texts_by_college_url(
            colleges=[],url_cates=url_cates,any_or_all_cates='any',filter_by=filter_by,is_test=is_test )
 
    def prepare_dictionary(self,   url_cates=None, corpus_file=None, dic_file=None, is_test=False): 
        """
            generate corpus and dictionary file
            input: dataframe with lemmatized content
            if is_test: take small number of lemmatized df
            
            Note: bigrams/trigrams are not included in this excercise
        """        
        try:
            if  url_cates==None: #default
                df=self.prepare_texts_by_url(url_cates=self.default_url_cates)
                corpus_file=self.default_full_corpus_file
                dic_file=self.default_dic_file
                self.is_default_corpus_dic_ready=True
            else: 
                if (corpus_file==None) or  (dic_file==None):
                    print('please supply corpus file / dictionary file')
                    return 
                if url_cates==None:
                    url_cates=['admi']
                df=self.prepare_texts_by_url(url_cates=url_cates)
             
            text_data_raw=list(df[self.lemma_data_lemma_col])
             
            #bigrams only
            text_data =self.make_bigrams(text_data_raw)
            
            #dictionary= corpora.Dictionary(text_data)  
            dictionary= corpora.Dictionary([i.split() for i in text_data])  

            corpus = [dictionary.doc2bow(text.split(' ')) for text in text_data] 
            joblib.dump(corpus, open(corpus_file, 'wb'))
            dictionary.save(dic_file)
            return 0
        except Exception as e:
            print(e)  
            return 1
         
    def train_lda_model(self, full_corpus_file=None,dic_file=None, 
                        NUM_TOPICS=15, passes=15, chunksize=5000, save_model=None, num_words=15, is_eval=False):
        """
            when full_corpus_file or dic_file is None, re-generate
        """  
        if (full_corpus_file==None) or (path.isfile(full_corpus_file)==False) or (dic_file==None) or (path.isfile(dic_file)==False):
            if self.is_default_corpus_dic_ready==False:            
                self.prepare_dictionary()
                self.is_default_corpus_dic_ready=True
            corpus=joblib.load(self.default_full_corpus_file)                      
            dictionary=joblib.load(self.default_dic_file)
        else:
            try:
                corpus=joblib.load(full_corpus_file)                      
                dictionary=joblib.load(dic_file)
            except Exception as e:
                print(e)
                dictionary, corpus=None, None
                return
            
        if dictionary==None or corpus==None:
            print('corpus or dictionary not ready. please build them before procedding')
            return
        
        if save_model==None or path.isfile(save_model)==False:
            save_model=self.default_model
        ldamodel = gensim.models.ldamodel.LdaModel(corpus, num_topics = NUM_TOPICS, id2word=dictionary, passes=passes)
        if is_eval==False:
            ldamodel.save(save_model) 
            self.model=ldamodel
        topics = ldamodel.print_topics(num_words=num_words)
          
        return topics, ldamodel
    
    def model_evalu(self): 
        model=joblib.load('C:\\Stempro\\Notebooks\\models\\adm_lda.model')
        corpus=joblib.load('C:\\Stempro\\Notebooks\\models\\adm_college_corpus.pkl')
        dic=joblib.load('C:\\Stempro\\Notebooks\\models\\adm_college_dictionary.gensim')
        cm = CoherenceModel(model=self.model, corpus=corpus, coherence='u_mass')
        coherence_lda = cm.get_coherence()
        return coherence_lda
    
    def compute_coherence_values(self, dictionary, corpus, texts, limit, start=2, step=2): 
        coherence_values = []
        model_list = []
        for num_topics in range(start, limit, step):
            
            _, model=self.train_lda_model(full_corpus_file=None,dic_file=None, 
                        NUM_TOPICS=num_topics, passes=15, chunksize=5000, save_model=None, num_words=15, is_eval=True)   
            model_list.append(model)
            coherencemodel = CoherenceModel(model=model, texts=texts, dictionary=dictionary, coherence='c_v')
            coherence_values.append(coherencemodel.get_coherence()) 
            print(num_topics, coherencemodel.get_coherence(), end('-------------\n'))
        return model_list, coherence_values

    def plot_coherence(self, start=3, limit=40, step=3):
        model_list, coherence_values = self.compute_coherence_values(dictionary=self.dictionary, 
            corpus=self.corpus, texts=self.docs, start=start, limit=limit, step=step)  
        x = range(start, limit, step)
        plt.plot(x, coherence_values)
        plt.xlabel("Num Topics")
        plt.ylabel("Coherence score")
        plt.legend(("coherence_values"), loc='best')
        plt.show()

    def summarize_new_college(self, text='Practical Bayesian Optimization of Machine Learning Algorithms'):
        tokens = self.make_tokens(text)  
        doc_bow = self.dictionary.doc2bow(tokens)  
        print(self.model.get_document_topics(doc_bow))
        
    def visualize(self, dictionary_file=None, corpus_file=None, model_file=None):        
        if corpus_file==None:
            corpus=self.corpus
        else:
            if path.isfile(corpus_file):
                corpus=joblib.load(corpus_file)
            else:
                corpus=None
                
        if dictionary_file==None:
            dictionary=self.dictionary
        else:
            if path.isfile(dictionary_file):
                dictionary=joblib.load(dictionary_file)
            else:
                dictionary=None
                
        if model_file==None:
            model=self.model
        else:
            if path.isfile(model_file):
                model=joblib.load(model_file)
            else:
                model=None
                
        if dictionary==None or corpus==None or model==None:
            print('corpus, dictionary or model not ready. please build them before procedding')
            return
     
        #dictionary = gensim.corpora.Dictionary.load(dictionary_file)
        #corpus = joblib.load(open(corpus_file, 'rb'))
        
        #lda = gensim.models.ldamodel.LdaModel.load(model_file)
        lda_display = pyLDAvis.gensim.prepare(model, corpus, dictionary, sort_topics=False)
        return lda_display 