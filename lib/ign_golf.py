import requests

BASE_URL_TEMPLATE = 'https://api.golfcourseapi.com/%s/%s' #/version/resource
VERSION = 'v1'
API_KEY = 'BSWZ6IRYVMZ4S56IAWFWAZQFWY' 

def _build_query_string(url, query):
    
    pass # flask prob has some lib that has all these for api work

def _get(url, headers):

    resp = requests.get(url, headers = headers, verify=False )

    if resp.status_code in (200,'200'): #type ;)
        return resp.json()

def _post():
    pass

def _delete():
    pass

def search_course(name):

    headers = {
        "Content-Type":"Application/json",
        "Authorization": "Key %s" % API_KEY
    }

    url = BASE_URL_TEMPLATE % (VERSION, 'search')
    url += '?search_query=%s' % name
    return _get(url, headers)

def get_course(id):

    return _get()

def register_course():

    return _post()

def activate_course():

    return _post() # meh put...post

def healthcheck():

    return _get()

