import requests

BASE_URL_TEMPLATE = 'https://api.golfcourseapi.com/%s/%s' #/version/resource
VERSION = 'v1'
API_KEY = 'BSWZ6IRYVMZ4S56IAWFWAZQFWY' 

def _build_query_string(url, query_params):
    
    pass # flask/requests prob has some lib that has all these for api work so keeping stubbed for now.

def _get(url, headers):

    resp = requests.get(url, headers = headers, verify=False )

    if resp.status_code == 200:
        return {"results": resp.json()}

    return {"results":  "No Error reporting implemented server side yet for rest code: %d" % resp.status_code, }

def _post():
    pass

def _delete():
    pass

def search_course(name):

    headers = {
        "Content-Type": "Application/json",
        "Authorization": "Key %s" % API_KEY
    }

    url = BASE_URL_TEMPLATE % (VERSION, 'search')
    url += '?search_query=%s' % name # query param

    return _get(url, headers)

def get_course(id):

    headers = {
        "Content-Type": "Application/json",
        "Authorization": "Key %s" % API_KEY
    }

    url = BASE_URL_TEMPLATE % (VERSION, 'courses')
    url += '/%d' % id # path param

    return _get(url, headers)

# really just grabbing course info atm
#def register_user():
#
#    return _post()
#
#def activate_user():
#
#    return _post() # meh put...post

def healthcheck():

    headers = {
        "Content-Type": "Application/json",
        "Authorization": "Key %s" % API_KEY
    }

    url = BASE_URL_TEMPLATE % (VERSION, 'healthcheck')

    return _get(url, headers)

