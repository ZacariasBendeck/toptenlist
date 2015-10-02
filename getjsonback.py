##import json files

import json



data = json.loads(open('data/owner.json').read())

print data['Owner']

print 'data[Owner][1]'
print data['Owner'][1]

for i in data['Owner']:
	print i['name']
	print i['description']
#print json.dumps(data, indent = 1)

#for i in data:
#	print i['owner']
