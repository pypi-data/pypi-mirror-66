class parse_save(cleaning_utility):
    """
        parse url and data files. 
        save parsed files individually
        assign ids to url
    """
    def __init__(self, 
                strict=True,  
                is_nltk=False,
                college_file='./learning_data/ContentAqusition__All.csv',  
                college_file_sep=',',
                college_id_col='college_id',
                 
                url_file_folder='C:/Stempro/Notebooks/data' ,
                url_file_pattern=r'.+url.csv$', 
                url_file_schema=['url', 'status_code'],
                url_file_sep='\t',  
                url_col='url',
                url_status='status_code',
                url_file_lemma_col='url_lemma',

                url_parsed_folder='C:/Stempro/Notebooks/data_parsed',
                url_parsed_ends='parsedurl.csv', 
                 
                 
                data_file_folder='C:/Stempro/Notebooks/data' ,
                data_file_pattern=r'.+\d+.csv$', 
                data_file_schema=['url', 'parent', 'ps', 'ns', 'text'], 
                data_file_sep='\t' ,  
                data_url_col='url',
                data_col='text',
                data_file_lemma_col='text_lemma',
                data_parsed_folder='C:/Stempro/Notebooks/data_parsed',
                data_parsed_ends='parseddata.csv', 
                 
                processed_pattern=r'.+parseddata.csv$',
                exception_log_file='parse_save_log.csv'
                ):
        """
            clean and lemmatize 
        """
        super().__init__(strict=strict, is_nltk=is_nltk)          
        if path.exists(url_parsed_folder)==False: 
            os.makedirs(url_parsed_folder)
        self.url_parsed_folder=url_parsed_folder
        
        self.college_id_col=college_id_col
        
        if path.exists(data_parsed_folder)==False: 
            os.makedirs(data_parsed_folder)
        self.data_parsed_folder=data_parsed_folder
                      
        self.url_file_folder=url_file_folder
        self.url_file_pattern=url_file_pattern
        self.url_file_schema=url_file_schema
        self.url_file_sep=url_file_sep  
        self.url_parsed_ends=url_parsed_ends 
        self.url_file_lemma_col=url_file_lemma_col
        self.url_col=url_col
        self.url_status=url_status
        
        self.data_file_folder=data_file_folder
        self.data_file_pattern=data_file_pattern
        self.data_file_schema=data_file_schema
        self.data_file_sep=data_file_sep  
        self.data_url_col=data_url_col
        self.data_parsed_ends=data_parsed_ends
        self.data_file_lemma_col=data_file_lemma_col
        self.data_col=data_col
        
        self.college_file=college_file
        self.college_file_sep=college_file_sep
        
        self.processed_pattern=processed_pattern
        self.exception_log_file=exception_log_file
        
    def get_college_masterdf(self):
        """
            load college file df
            add 1000000 to collegeid to make id consistent
        """
        df_coll= pd.read_csv(self.college_file, sep=self.college_file_sep) 
        df_coll['collegeId']=df_coll['collegeId']+100000 #why +100000? 
        df_coll.rename(columns={'collegeId': self.college_id_col}, inplace=True)
        
        return df_coll
    
    def process_files(self, n_files=10):
        """
            get a list of college ids to process
        """
        if n_files>0:
            colleges=list(self.get_college_masterdf()[self.college_id_col])[0:n_files]
        else:
            colleges=list(self.get_college_masterdf()[self.college_id_col])
        urls=[f for f in listdir(self.url_file_folder) if re.match(self.url_file_pattern, f)]
        data=[f for f in listdir(self.data_file_folder) if re.match(self.data_file_pattern, f)]
        
        processed=[int(''.join([c for c in re.split(r'[\\|/]', f)[-1] if c.isdigit()]))  for f in listdir(self.data_parsed_folder) if re.match(self.processed_pattern, f)]
        colleges=set(colleges)-set(processed)
        log=[]
        for c in colleges:
            url_files=[f for f in urls if str(c) in f] 
            data_file=None
            if len(url_files)>0:
                data_files=[f for f in data if str(c) in f] 
            else:
                log.append((c, '_no url file_', ' ', '1'))
                continue
            if len(data_files)>0:
                try:
                    self.process_individual_file(c,path.join(self.url_file_folder,url_files[0]), 
                                                 path.join(self.data_file_folder,data_files[0]))
                    log.append([c, url_files[0], data_files[0], '0'])
                except Exception as e:
                    log.append((c, url_files[0], data_files[0], re.sub(r'[\n|\t]', r' ', e)))
            else:
                log.append((c, ' ', '_no data file_', '1'))
                continue
        df_log=pd.DataFrame(log, columns=['college_id', 'url_file', 'data_file', 'result'])
        df_log.to_csv(self.exception_log_file, index=False, sep='\t')
                 

