import json, requests

url = 'https://maps.googleapis.com/maps/api/place/textsearch/json?'
url = 'https://maps.googleapis.com/maps/api/place/autocomplete/json'
url = 'http://maps.google.com/maps/api/geocode/json?address=Felton%20Road+australia&sensor=true'

params = dict(
#    key = "AIzaSyBSi_cIXVfK0VRvGpV6Loufr5EtxhaFxKM",
#    input = "school",
    sensor ='true',
    address = "Summer Hill Public School"
#    location = "37.76999,-122.44696",
#    radius=500
)

#url += "?"

#for k in params:
#    url += k + "=" + params[k] + '&'

resp = requests.get(url=url, params=params)
#resp = requests.get(url)
#print resp.url
#print resp.status_code
#print resp.headers
#print resp.text

data = json.loads(resp.text)
res = data['results']

for r in res:
    print "%s (%s, %s)" % (r['formatted_address'], r['geometry']['location']['lat'], r['geometry']['location']['lng'])

