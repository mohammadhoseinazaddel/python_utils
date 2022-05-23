from dotmap import DotMap
# https://stackoverflow.com/questions/2352181/how-to-use-a-dot-to-access-members-of-dictionary
m = DotMap()
m.hello = 'hhhh'
print(m.hello)
m.hello+= "!"
print(m.hello)
m.val = 5
m.val2 = 'Sam'
print (m)
print (m["hello"])

import json
jsonDict = json.loads(text)
data = DotMap(jsonDict)
print data.location.city