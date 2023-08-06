class CollegeCrawl():
    Gap_Insecond=1
    Max_Pages=15      
    """
        collegename: name
        rooturl: https://www.university.edu. Scheme and netloc need to be complete
        prioritykeywords: ['apply','adimission'...] etc. if None then everth page 
        respectrobottxt: True
    """
    def __init__(self,_collegename, _rooturl, 
                 _prioritykeywords=['apply', 'admission', 'application', 'deadline'], 
                 _url_file=None,                  
                 _save_to_folder=None,
                 _existingurlfile=None, #csv files that were visited in the past
                 _respectrobottxt=True, 
                _headers={'User-Agent':'Mozilla/5.0'} ):
        self.college=_collegename
         
        if urlparse(_rooturl).scheme=="":
            print('URL needs to have scheme. Please try again.')
            raise Exception('URL needs to have scheme')            
            return
        
        self.rootUrl=_rooturl
        self.base_domain=urlparse(self.rootUrl).netloc
        self.scheme=urlparse(self.rootUrl).scheme
        self.priorityKeywords=_prioritykeywords
        self.respectRobottext=_respectrobottxt
        if _save_to_folder==None or path.isdir(_save_to_folder)==False:
            self.save_to_folder=os.getcwd()
        else:
            self.save_to_folder=_save_to_folder
            
        #to make it less 
        if _existingurlfile==None or path.exists(_existingurlfile)==False:            
            self.existingurlfile=path.join(self.save_to_folder,re.sub("\s+", "_", self.college.strip()+'.csv'))
        else:
            self.existingurlfile=_existingurlfile
        self.allurls={}
        self.headers=_headers
        self.files=[]
            
    '''simple description'''        
    def __str__(self):
        return '{}. Starting URL: {}'.format(self.college, self.rootUrl)
    '''
        load _existingurlfile: two columns -- Url and status_code
        minimum assumptions: first two columns are url and status_code
    '''
    def Load_DiscoveredUrls(self, delimiter=',', hasHeader=False, header_names=['url', 'status_code']):   
        if self.existingurlfile==None:
            return {}
        else:
            if path.exists(self.existingurlfile) and re.sub('\s+', '_', self.college) in ntpath.basename(self.existingurlfile):
                df_urls=pd.read_csv(self.existingurlfile,  delimiter=delimiter).iloc[:, 0:2]   
                header_row=list(df_urls.columns) 
            
                if re.match('^http', header_row[0]):
                    df_urls.columns=header_names
                    df_urls=pd.concat([df_urls, pd.DataFrame([header_row], columns=header_names)])                
                else: #event it is not, still assign the header_name
                    df_urls.columns=header_names 
                
                return dict(zip(df_urls['url'], df_urls['status_code'])) #format: url:status_code. i.e., url is the key
                #another options is: df_urls.to_dict('list') #format of {url:[url1, url2...], status_code:[0, 200...]}
            else:
                return {}        
            
    """
        get all urls starting from rootUrl 
        headers={'User-Agent':'Mozilla/5.0'}
        #Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/79.0.3945.88 Safari/537.36
        #full list: https://www.whatismybrowser.com/guides/the-latest-user-agent/chrome
        response= requests.get(url, headers=headers)
        soup = BeautifulSoup(response.text)  
        
        it will first load which ever has alread visited 

    """    
    def GetAllUrls(self, headers=None, links_only=True): 
        #load existing urls if any
        urls=self.Load_DiscoveredUrls() 
        
        if len(urls)==0:
            urls={self.rootUrl:0}  
            unvisited=[self.rootUrl]
        else:
            unvisited=[url for url, status_code in urls.items() if status_code==0]
            if not unvisited:
                unvisited=[self.rootUrl]
            
        if headers==None: 
            if self.headers:
                headers=self.headers
            else: 
                 headers={'User-Agent':'Mozilla/5.0'}  
                    
        #get base_domain    
        if self.base_domain==None:
            self.base_domain=urlparse(unvisited[0]).netloc
        if self.scheme==None:
            self.scheme=urlparse(unvisited[0]).scheme
     
        pages_visited =0
        try:  
            while len(unvisited)>0:        
                pages_visited+=1
                url=unvisited.pop()  
                response=requests.get(url, headers=headers)     
                status_code=response.status_code
                urls[url]=status_code
                 
                if status_code==200:
                    soup=BeautifulSoup(response.text, 'html.parser') 
                    for link in soup.find_all('a'): 
                        if link.has_attr('href'):
                            url=link['href']       
                            url=re.sub(r'[\/_+!@#$?\\\s]+$', '', url)
                            parsed_uri = urlparse(url) 
                            absolute_url=''
           
                            if (parsed_uri.netloc=='') and (parsed_uri.scheme=='') and re.match(r'^\/.*\w$', parsed_uri.path) :
                                absolute_url=urljoin(self.scheme+'://'+self.base_domain,parsed_uri.path)
                            elif parsed_uri.netloc==self.base_domain and re.match('^http', parsed_uri.scheme):
                                absolute_url=url
                            elif parsed_uri.netloc==self.base_domain and parsed_uri.scheme=="" and re.match(r'^\/.*\w$', parsed_uri.path):
                                absolute_url=self.scheme+'://'+parsed_uri.netloc+parsed_uri.path
                            else:
                                continue    
                            if absolute_url!='' and absolute_url not in urls:   
                                 urls[absolute_url]=0
                  
                    self.SaveToCsv_FromResponse(url, response)  
              
                if pages_visited>=self.Max_Pages:
                    break 
                 
                unvisited=[name for name, code in urls.items() if code==0]    
                print('')
                break
                #sorting rule: has keywords, short url, else
                unvisited=sorted(unvisited, key=lambda item: (sum([w in item for w in self.priorityKeywords])*10+10)/len(item))
                time.sleep(self.Gap_Insecond) #wait for few seconds. 
          
        except: 
            print('url "{}" went wrong'.format(url))  
            urls[url]=999
                #not to consider failed pages. status_code 400s may need manual handling of they are high priority pages
        finally: 
            self.allurls=urls
            #csv_columns = ['url', 'status_code']  
            #try:
                #with open(self.existingurlfile, 'w', newline='', encoding='utf-8') as csvfile:
                    #writer = csv.DictWriter(csvfile, fieldnames=csv_columns)
                    #writer.writeheader()
                    #for data in urls:
                        #writer.writerow(data)
            #except IOError:
                #print("I/O error")
            self.Save_Summaries()
            
    """
        display summaries 
    """
    
    def Save_Summaries(self): 
        if self.allurls:
            df_urls=pd.DataFrame(list(c.allurls.items()), columns=['url', 'status_code'])
            print('Summary for college ', self.college)
            print('\n')
            print(df_urls.groupby('status_code').count().reset_index())
            #save file as well  
            try:
                with open(self.existingurlfile, 'w', newline='', encoding='utf-8') as csvfile:
                    writer = csv.writer(csvfile, delimiter=',', quoting=csv.QUOTE_MINIMAL)
                    writer.writerow(['url','status_code'])
                    for url, status_code in self.allurls.items():  
                        writer.writerow([url, status_code])  
            except IOError:
                print('IO Error in saving summaries')
                
        if self.files:
            print('\nThe following {} file(s) are generated. '.format(len(self.files)))
            pprint(self.files) 
    """
        read one page
    """
    def Read_Oneurl(self, url):  
        response=requests.get(url, self.headers)  
        if response.status_code==200: 
            return self.Get_Pagetext(response)
        else: 
            return [[None, None, None, None]]
    
    '''
        used for filter()
    '''
    def Tag_Visible(self, element):
        if element.parent.name in ['style', 'script', 'head', 'title', 'meta', '[document]']:
            return False
        if isinstance(element, Comment):
            return False
        return True 

    '''
        get all text from page body
    '''
    def Get_Pagetext(self, response):
        soup = BeautifulSoup(response.text, 'html.parser') #conent
        texts = soup.findAll(text=True) 
        visible_texts = filter(self.Tag_Visible, texts)       

        return [ [t.parent.name,   
                 t.parent.previousSibling.name if t.parent.previousSibling!=None else None, 
                 t.nextSibling.name if t.nextSibling!=None else None,
                 re.sub(r'[\s+\t]',' ',t) ]  for t in visible_texts if len(t.strip())>2] 

    """
        Save One Page
        filename, if not None, should not be full name. use import ntpath ntpath.basename("a\b\c")
    """
    def SaveToCsv_FromUrl(self,url): # tab delimiter only 
        url=url.strip() 
        content=self.Read_Oneurl(url) #in format of (a,a,a,a)   
        self.SaveToCsv(url, content)
        #return SaveToCsv_FromResponse()
    
    '''
        save from resonse. called in the initial loop
    '''
    def SaveToCsv_FromResponse(self, url, response):
        content= self.Get_Pagetext(response)
        self.SaveToCsv(url, content) 
        
    '''
        save to csv file and append it to self.files
    '''    
    def SaveToCsv(self, url, content):
        filename=url.replace('.', '_dot_').replace('/', '_').replace(':', '_')+'_'+datetime.now().strftime("%m_%d_%Y_%H_%M_%S")+'.csv'
        fullname=path.join(self.save_to_folder, filename)
        try:
            with open(fullname, 'w', newline='', encoding='utf-8') as csvfile:
                writer = csv.writer(csvfile, delimiter='\t', quoting=csv.QUOTE_MINIMAL)
                writer.writerow(['url', 'parent', 'ps', 'ns', 'text'])
                for lll in content: 
                    lll.insert(0, url)
                    writer.writerow(lll)  
            self.files.append(fullname) 
        except IOError:
            print('failed to save file.')
            
    '''
        move file from one folder to another 
        pattern: regular expression
    '''
    def MoveFiles(self, destination_folder, source_folder=None,  pattern=None): 
        if source_folder==None:
            source_folder=self.save_to_folder
        if source_folder==None:
            print('Please specify folder with the files. ')
            return
        if destination_folder==None or path.isdir(destination_folder)==False:
            print('Need a valid destination folder')
            
        if pattern==None or pattern=="":
            pattern="csv$" 
        files = [f for f in os.listdir(self.save_to_folder) if re.match(pattern, f) and path.isfile(path.join(src, f))]
        for f in files:
            shutil.move(path.join(src, f), destination_folder)  
            