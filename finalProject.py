from flask import Flask

app = Flask(__name__)


#Main Page, Owners List, template 1
@app.route('/')
@app.route('/topten/')
def mainPage():
	return 'This is the main page, with the owners list'

#This page will be for creating a NEW OWNER, template 2
@app.route('/topten/new/')
def createNewOwner():
	return 'This page will be for creating a NEW OWNER'

#This page will be for editing owner #, template 3'
@app.route('/topten/<int:owner_id>/edit')
def editOwner(owner_id):
	return 'This page will be for editing owner #' + str(owner_id)

#This page will be for deleting owner #, template 4'
@app.route('/topten/<int:owner_id>/delete')
def deleteOwner(owner_id):
	return 'This page will be for deleting owner #' + str(owner_id)

#### End Owner Page dependencies ###
#### Start TopTenLists Pages  ####

#This page will show the top ten lists for owner #', template 5

#template 5
@app.route('/topten/<int:owner_id>/')
def toptenlists(owner_id):
	return 'This page will show the top ten lists for owner #' + str(owner_id)

#template 6
@app.route('/topten/<int:owner_id>/new')
def createNewList(owner_id):
	return 'This page will be for CREATING a new list for owner # ' + str(owner_id)

#template 7
@app.route('/topten/<int:owner_id>/<int:list_id>/edit')
def editList(owner_id, list_id):
	return 'This page will be for EDITING list #' + str(list_id) + ' by owner #' + str(owner_id)

#template 8
@app.route('/topten/<int:owner_id>/<int:list_id>/delete')
def deleteList(owner_id, list_id):
	return 'This page is for DELETING list #' + str(list_id) + ' by owner #' + str(owner_id)

### End Top Ten Lists Dependencies ###
###  Start Top Ten Item Pages ###


#template 9
@app.route('/topten/<int:owner_id>/<int:list_id>/')
def topTenItems(owner_id, list_id):
	return 'This page will show the top ten items for list #' + str(list_id) + ' by owner ' + str(owner_id)

#template 10
@app.route('/topten/<int:owner_id>/<int:list_id>/new')
def createNewItem(owner_id, list_id):
	return 'This page is for CREATING a new item in list # ' + str(list_id) + ' by owner #' + str(owner_id)

#template 11
@app.route('/topten/<int:owner_id>/<int:list_id>/<int:item_id>/edit/')
def editItem(owner_id, list_id, item_id):
	return 'This page is for EDITING item #'+str(item_id)+' in list # '+str(list_id)+' by owner #' + str(owner_id)

#template 11
@app.route('/topten/<int:owner_id>/<int:list_id>/<int:item_id>/delete/')
def deleteItem(owner_id, list_id, item_id):
	return 'This page is for DELETING item #'+str(item_id)+' in list # '+str(list_id)+' by owner #' + str(owner_id)


if __name__ == '__main__':
	app.debug = True
	app.run(host = '0.0.0.0', port = 5000)



