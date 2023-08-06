class parse_merge_utility(cleaning_utility):
    """
        parse url and data files. 
        save parsed files individually
        assign ids to url
        merge files
    """
    def __init__(self, 
               is_nltk=False,
               url_file_folder='./learning_data',
               url_file_pattern=r'.+url.csv$', 
               url_file_schema=['url', 'status_code'],
               url_file_sep='\t', 
               url_merged_csv='url_sum.csv',
               url_parsed_folder='./parsed',
               url_parsed_ends='parsed.csv', 
               data_file_folder='./learning_data',
               data_file_pattern=r'.+\d+.csv$', 
               data_file_schema=['url', 'parent', 'ps', 'ns', 'text'], 
               data_file_sep='\t' , 
               data_merged_csv='data_sum.csv', 
               data_parsed_folder='./parsed',
               data_parsed_ends='parsed.csv',
              ): 
        self.is_nltk=is_nltk
        super().__init__(is_nltk=is_nltk)
        if path.exists(url_parsed_folder)==False: 
            os.makedirs(url_parsed_folder)
        self.url_parsed_folder=url_parsed_folder
        
        if path.exists(data_parsed_folder)==False: 
            os.makedirs(data_parsed_folder)
        self.data_parsed_folder=data_parsed_folder
                      
        self.url_file_folder=url_file_folder
        self.url_file_pattern=url_file_pattern
        self.url_file_schema=url_file_schema
        self.url_file_sep=url_file_sep  
        self.url_parsed_ends=url_parsed_ends
        self.url_merged_csv=url_merged_csv
        self.data_file_folder=data_file_folder
        self.data_file_pattern=data_file_pattern
        self.data_file_schema=data_file_schema
        self.data_file_sep=data_file_sep 
        self.data_merged_csv=data_merged_csv 
        self.data_parsed_ends=data_parsed_ends
        
    def merge_url(self, is_test=True, nrows=100, url_files=0):
        """
            all other parameters is from constructor
            two options: test or prod
            merge url files
        """
        files=[f for f in listdir(self.url_file_folder) if re.match(self.url_file_pattern, f)]
        if url_files==0:
            n=len(files)
        else:
            n=len(files) if url_files>len(files) else url_files
            
        if is_test==True: 
            return pd.concat([pd.read_csv(path.join(self.url_file_folder, f), nrows=nrows, names=self.url_file_schema, sep=self.url_file_sep) for 
                 f in files[0:n]], axis=0) #{0/'index', 1/'columns'}, default 0
        return pd.concat([pd.read_csv(path.join(self.url_file_folder, f), names=self.url_file_schema, sep=self.url_file_sep) for 
                 f in files[0:n]], axis=0)
    
    def merge_data(self, is_test=True, nrows=100, data_files=10):
        """
            all other parameters is from constructor
            two options: test or prod
            merge data files
        """
        files=[f for f in listdir(self.data_file_folder) if re.match(self.data_file_pattern, f)]
        if data_files==0:
            n=len(files)
        else:
            n=len(files) if data_files>len(files) else data_files
            
        if is_test==True: 
            return pd.concat([pd.read_csv(path.join(self.data_file_folder, f), nrows=nrows, names=self.data_file_schema, sep=self.data_file_sep) for 
                 f in files[0:n]], axis=0) #{0/'index', 1/'columns'}, default 0
        return pd.concat([pd.read_csv(path.join(self.data_file_folder, f), names=self.data_file_schema, sep=self.data_file_sep) for 
                 f in files[0:n]], axis=0)
    
    def data_file_to_csv(self):
        """
            generate data df and save it to a single file
        """
        df=self.merge_data(is_test=False, data_files=0)
        df.to_csv(self.data_merged_csv, index=False, sep=self.data_file_sep)
        return df
    
    def url_file_to_csv(self):
        """
            generate url df and save it to a single file
        """
        df=self.merge_url(is_test=False, url_files=0)
        df.to_csv(self.url_merged_csv, index=False, sep=self.url_file_sep)
        return df
    
    def college_parse_and_save(self, file, *others):
        """
            parse and save url and data file college by college. 
            url
        """