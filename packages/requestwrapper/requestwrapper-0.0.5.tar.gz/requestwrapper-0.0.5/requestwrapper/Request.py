# -*- coding: utf-8 -*-
"""
Created on Tue Apr  9 16:49:50 2019

@author: jskro
TODO: prefix url with http://, https:// 
TODO: add get, put, post methods (like in requests)
"""

import requests, time as tm

# constants
DEFAULT_AUTH_METHOD='Bearer'
SEND_REQUEST_TIME_OUT=5
DEFAULT_VERIFY=True

# Request        
class Request():
    """ Request: sends API request using url, data, api_key. if status_code>299, raise API_ERROR"""
    REPEAT_REQUEST_SLEEP_TIME=2
    """initialization"""
    def __init__(self, PRINT_RESPONSE=True, verify=None, res_error_function=None, repeat_times=0,**kwargs):
        self.PRINT_RESPONSE=PRINT_RESPONSE
        self.verify=nvl(verify,DEFAULT_VERIFY)
        self.res_error_function=nvl(res_error_function,__res_error_function__)
        self.repeat_times=repeat_times
        self.mock_request=nvl(from_kwargs(kwargs,'mock_request')[0],False)
        
    """ class functions"""
    def send_request(self, url, data=None, method='post', api_key='undefined',repeat=False,
                     raise_error=True,as_json=True, default=None, print0=True, return_response=True, verify=None,
                     **kwargs):
        # set SSL verification
        verify=nvl(verify,self.verify)
        # send request to server
        repeat_times=kwargs.get('repeat_times',self.repeat_times)
        if repeat==False and repeat_times==0:
            # send single time
            print0=self.PRINT_RESPONSE and print0
            res=self.__send_request__(url, data, method, api_key, print0, verify, **kwargs)
            status_code=res.status_code
        else:
             # optional: repeat request
            status_code=999
            n_times=0
            # set repeat_times
            if repeat_times==0:
                # repeat within time window
                start=tm.time()
                while (status_code>299 and tm.time()<start+SEND_REQUEST_TIME_OUT) :
                    if print0 and n_times>0:
                        print('repeating request {0} {1}'.format(method,url))
                    tm.sleep(self.REPEAT_REQUEST_SLEEP_TIME)
                    res=self.__send_request__(url, data, method, api_key,print0=False, verify=verify)
                    status_code=res.status_code
                    n_times=n_times+1                    
            else:
                # repeat fixed number of times
                while (status_code>299 and n_times<=repeat_times) :
                    if print0 and n_times>0:
                        print('repeating request {0} {1}'.format(method,url))
                    tm.sleep(self.REPEAT_REQUEST_SLEEP_TIME)
                    res=self.__send_request__(url, data, method, api_key,print0=False, verify=verify) 
                    status_code=res.status_code
                    n_times=n_times+1
        # store last_response
        self.last_res=res
        # return or print response error 
        print_error=kwargs.get('print_error',True)
        res=self.res_error_function(res,raise_error=raise_error,print_error=print_error)
        # parse response or return response
        v=__return_response__(res,return_response)
        # return value
        return(v)

    def send_requests(self,url=None,body=None,method='post', api_key='undefined',reqs=None, return_response=True):
       """ send a list or dictionary of request inputs: url,body,method and return list or dictionary of responses """
       #body         
       if type(reqs)==list:
           resp=[]
           for req in reqs:
               if type(req)==dict:
                   url0,body0,method0=from_kwargs(req,'url','body','method') #deconstruct
                   resp.append(self.send_request(url=nvl(url0,url),data=nvl(body0,body),method=nvl(method0,method),repeat=False,repeat_times=0,raise_error=False, return_response=return_response))
               else:
                   raise TypeError('req is not dict but {0}'.format(type(req)))
       elif type(reqs)==dict:
           resp={}
           for ky in reqs:
               req=reqs[ky]
               if type(req)==dict:
                   url0,body0,method0=from_kwargs(req,'url','body','method') #deconstruct
                   resp[ky]=self.send_request(url=nvl(url0,url),data=nvl(body0,body),method=nvl(method0,method),repeat=False,repeat_times=0,raise_error=False, return_response=return_response)
               else:
                   raise TypeError('req is not dict but {0}'.format(type(req)))
       else:
           raise TypeError('reqs type is not dict or list but {0}'.format(type(reqs)))
       return(resp)
        
    #1 Send request to passed url with data using method and api_key
    def __send_request__(self, url, data=None, method='post', api_key='undefined', print0=True, verify=None,kwargs2={},**kwargs):
        """ base function, use kwargs2 to send key words args to requests.function """
        # mock_request: res as dummy class with status code and json function
        if self.mock_request:
            print('sending a mock request')
            res=MockResponse()
            return(res)
        # regular request
        method=method.lower()
        if data is None and 'body' in kwargs.keys():
            data=kwargs['body']
        if 'auth_method' in kwargs.keys():
            auth_method=kwargs['auth_method']
        else:
            auth_method=DEFAULT_AUTH_METHOD
        if print0==True and api_key != 'undefined':
            print('Send request using key {0}'.format(api_key))
        # Get or make headers
        if 'headers' in kwargs.keys():
            # get headers
            headers = kwargs['headers']
        else:
            # make headers
            headers = {
                #"Content-Type":  "application/json",
                "Accept":        "application/json",
                "Authorization": "{0} {1}".format(auth_method, api_key)
              }
            # Set header content type
            if "type" in kwargs:
                 # If we're querying VWE API (with XML) we need different headers
                if kwargs['type'] == "xml":
                    headers = {
                      "Content-Type": "application/xml",
                      "Accept": "*/*"
                    }
                # If we're querying /documents (pdf) we need accept header pdf
                elif kwargs['type'] == 'pdf':
                    headers["Accept"]="application/pdf"
                else:
                    headers["Accept"]=kwargs['type']
            elif "content_type" in kwargs:
                content_type = kwargs['content_type']
                headers["Content-Type"] = content_type
            else:
                # Default content-type is "application/json"
                content_type = "application/json"
                headers["Content-Type"] = content_type
        # Send request
        self.last_request={'url':url,'data':data,'headers':headers}
        if method == "post":
            res = requests.post(url, json=data, headers=headers, verify=verify)
        elif method == "put":
            res = requests.put(url, json=data, headers=headers, verify=verify)
        elif method == "patch":
            res = requests.patch(url, json=data, headers=headers, verify=verify)
        elif method == "get":
            #drop_keys(kwargs,['url','headers','verify']) # clear passed keys
            res = requests.get(url, headers=headers, verify=verify, **kwargs2)
        elif method == "delete":
            res = requests.delete(url, headers=headers, verify=verify)
        else:
            raise UNKNOWN_METHOD_ERROR(method)
        self.last_response=res
            
        if print0==True:
            print("{} ({}): {}".format(method.upper(), res.status_code, url))
        return res
    
    # save content
    def save_response(self,path,res=None,is_encoded=False):
       """ save last or passed response to path. path is the qualified file path dir/fname """ 
       is_encoded=False
       res=nvl(res,self.last_res)
       if res.status_code<=299:
          if is_encoded:
             s=str.encode(res.text)
          else:
             s=res.content
          f = open(path,"wb")
          f.write(s)
          f.close()
          print('response content saved as {0}'.format(path))
       else:
          raise RESPONSE_STATUS_CODE_ERROR(res.status_code)
       return(self)
              
def __return_response__(res, return_response=False):
    try:
        #body
        if return_response==True:
            return(res)
        else:
            if res.status_code<=299:
                try:
                    v=res.json()
                except Exception as e:
                    v=res.text
                return(v)
            else:
                return(res.text)
    except Exception as e:
        print('error in __return_response__')
        raise e

def __res_error_function__(res, raise_error,print_error=True):
    """ default response error function """
    #body
    if res.status_code<=299:
        pass
    else:
        if raise_error:
            raise API_ERROR('request returns status code {0}'.format(res.status_code))
        elif print_error:
            print('request returns status code {0}'.format(res.status_code))
    #return value
    return(res)


""" classes """
class MockResponse():
    def __init__(self):
        self.status_code=404
        self.json=lambda x=1: {'mock':True}

""" errors """
class RESPONSE_STATUS_CODE_ERROR(Exception):
    def __init__(self, message=None, errors=None):
        super().__init__(message)
        self.errors = errors
        
class API_ERROR(Exception):
    """Exception raised for custom error.
    Attributes:
        expression -- expression which caused error
        message -- explanation of the error
    """
    def __init__(self, message=None, errors=None):

        # Call the base class constructor with the parameters it needs
        super().__init__(message)

        # Now for your custom code...
        self.errors = errors

class UNKNOWN_METHOD_ERROR(Exception):
    def __init__(self, message=None, errors=None):
        super().__init__(message)
        self.errors = errors

""" helpers: nvl, from_kwargs, tryjson """
#nvl: checks input is None or has zero length, returns default
def nvl(input, default=''): 
    #body 
    if  input is None:
        return(default)
    else:
        return(input)

def from_kwargs(kwargs,*args):
    # unpack key-values from kwargs into args variables 
    try:
        #body
        kw=tuple([kwargs.get(arg) for arg in args])
    except Exception as e:
        print('error in from_kwargs')
        raise e
    #return value
    return(kw)      

def tryjson(res):
    try:
        v=res.json()
        return(v)
    except Exception as e:
        return(False)