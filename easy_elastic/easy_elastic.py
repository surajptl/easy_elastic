from elasticsearch import Elasticsearch

# SETTINGS =   {
#     "settings": {
#                 "analysis": {
#                 "analyzer": {
#                     "autocomplete": {
#                     "tokenizer": "autocomplete",
#                     "filter": [
#                         "lowercase"
#                     ]
#                     },
#                     "autocomplete_search": {
#                     "tokenizer": "lowercase"
#                     }
#                 },
#                 "tokenizer": {
#                     "autocomplete": {
#                     "type": "edge_ngram",
#                     "min_gram": 1,
#                     "max_gram": 10,
#                     "token_chars": [
#                         "letter"
#                     ]
#                     }
#                 }
#                 }
#             },
    # "mappings": {

    #         "properties": {
    #             "id": {
    #                 "type": "integer"
    #                 },
    #             "name": {
    #                 "type": "text",
    #                 "analyzer": "autocomplete",
    #                 "search_analyzer": "autocomplete_search"
    #                 },
    #             "collection_name": {
    #                 "type": "text"
    #                 }
    #         }
            
    #     }
        # }

DATA_TYPE = ['integer', 'text', 'keyword', 'date',  'long', 'double', 'boolean'] 
COMPLEX_TYPE = ['ip', 'object', 'nested', 'geo_point', 'geo_shape', 'completion']

#BASIC CONFIGURATION AND SOME FUNCTIONALITY OF FULL TEXT SEARCH
class ElasticSearchBasic:
    """
    This is basic configuration for the every new elasticsearch cluster
    """
    def __init__(self, user_name, password, cloud_id=None, url=None):
        #url = 'https://2a56b26765ef47a49cab169c5fc46bf9.asia-south1.gcp.elastic-cloud.com:9243/'
        self.cloud_id = cloud_id
        self.user_name = user_name
        self.password = password
        self.url = url
    
    def regex_connection(self, val, url=None, cloud=None):
        if url:
            if not isinstance(val, str):
                return False
            if val.find("com:9243/") < 0:
                return False
            return True
        if cloud:
            if not isinstance(val, str):
                return False
            if val.find(":") < 0:
                return False
            return True
        return False
        
    
    def connection(self):
        if self.url and self.regex_connection(self.url, url=True):
            _es = Elasticsearch([url], http_auth=(self.user_name, self.password))
        elif self.cloud_id and self.regex_connection(self.cloud_id, cloud=True):
            _es = Elasticsearch(cloud_id = self.cloud_id, http_auth=(self.user_name, self.password))
        else:
            return "Something went wrong into your configuration, Please check once."
        if not _es.ping():
            # print("need to log that connection feild!")
            return None
        return _es
    
    def create_index(self, index_name, settings = None):
        if settings:
            SETTINGS = settings
        es = self.connection()
        if es:
            try:
                es.indices.create(index=index_name, body= SETTINGS)
                return 'index created sucessfully'
            except Exception as e:
                print('need to log this exception: {0}'.format(e))
                return "need to raise exception {0}".format(e)
        else:
            return 'connectino refused'
    
    def insert_records(self, index_name, record):
        es = self.connection()
        if es:
            if not es.indices.exists(index_name):
                return "Need to create index first"
            try:
                es.index(index = index_name, body = record, doc_type="_doc")
                return "Inserted Successfully"
            except Exception as e:
                print('need to log this exception')
                return "Failed due to {0} exception".format(e)
        else:
            return 'connectino refused'

    def match(self, index_name, doc_name, search):
        es = self.connection()
        if es:
            result = es.search(index=index_name, body={"from":0,"size":100,"query":{"match":{doc_name: search}}})
            if result.get("hits").get("hits"):
                return [i.get("_source") for i in result.get("hits").get("hits") ]
            else:
                return "Match Not Found"
        else:
            return 'connectino refused'

    def match_phrase(self, index_name, doc_name, search):
        es = self.connection()
        if es:
            result = es.search(index=index_name, body={"from":0,"size":100,"query":{"match_phrase":{doc_name:search}}}) 
            if result.get("hits").get("hits"):
                return [i.get("_source") for i in result.get("hits").get("hits") ]
            else:
                return "Match Not Found"
        else:
            return 'connectino refused'

    def term_case_sensitive(self, index_name, doc_name, search):
        es = self.connection()
        if es:
            result = es.search(index=index_name, body={"from":0,"size":100,"query":{"term":{doc_name: search}}})   
            if result.get("hits").get("hits"):
                return [i.get("_source") for i in result.get("hits").get("hits") ]
            else:
                return "Match Not Found"
        else:
            return 'connectino refused'

    def regex(self, index_name, doc_name, search_with_regexp):
        es = self.connection()
        if es:
            result = es.search(index=index_name, body={"from":0,"size":100,"query":{"regexp":{doc_name: search_with_regexp}}})   
            if result.get("hits").get("hits"):
                return [i.get("_source") for i in result.get("hits").get("hits") ]
            else:
                return "Match Not Found"
        else:
            return 'connectino refused'
    
    def create_mapping(self,*args, min_gram=1, max_gram=10, **kwargs):
        #args will be use to insert analyZer and search search_analyzer
        if min_gram in (False, None, 0):
            min_gram = 1
        if max_gram in(False, None, 0):
            max_gram = 10
        _SETTINGS =   {
                    "settings": {
                                "analysis": {
                                "analyzer": {
                                    "autocomplete": {
                                    "tokenizer": "autocomplete",
                                    "filter": [
                                        "lowercase"
                                    ]
                                    },
                                    "autocomplete_search": {
                                    "tokenizer": "lowercase"
                                    }
                                },
                                "tokenizer": {
                                    "autocomplete": {
                                    "type": "edge_ngram",
                                    "min_gram": min_gram,
                                    "max_gram": max_gram,
                                    "token_chars": [
                                        "letter"
                                    ]
                                    }
                                }
                                }
                            }
                        }
        if kwargs:
            map = {}
            for key, value in kwargs.items():
                temp_map = {}
                if value in DATA_TYPE:
                    temp_map[key] = {"type": value}
                else:
                    temp_map[key] = {"type": 'text'}
                if key in args:
                        temp_map.get(key).update({"analyzer": "autocomplete", "search_analyzer":"autocomplete_search"})
                map.update(temp_map)
            _MAPPING = {'mappings':
                        {
                            "properties": map
                            }
                    }
            return {**_SETTINGS, **_MAPPING}
        else:
            return None

