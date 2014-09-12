import httplib2
from datetime import datetime
import simplejson


TESTDATA = {'bbox':
                {
                    'xmin': 1439918,
                    'ymin': 6866401,
                    'xmax': 1536152,
                    'ymax': 6929538,
                    'name': 'Berlin'
                }
            }
URL = 'http://localhost:8080/form'

jsondata = simplejson.dumps(TESTDATA)
h = httplib2.Http()
resp, content = h.request(URL,
                          'POST',
                          jsondata,
                          headers={'Content-Type': 'application/json'})
print resp
print content
