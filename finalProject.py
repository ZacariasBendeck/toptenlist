from flask import Flask, render_template, url_for, request, redirect, flash, jsonify
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from database_setup import Base, Owner, Lists, Items

app = Flask(__name__)

engine = create_engine('sqlite:///finalProject.db')
Base.metadata.bind = engine

DBSession = sessionmaker(bind=engine)
session = DBSession()

#Fake Owners
owner = {'name': 'Zacarias Bendeck', 'id': '1'}
owners = [{'name': 'Zacarias Bendeck', 'id': '1'}, {'name':'Gabriela Tentori', 'id':'2'},{'name':'Mario Rojas', 'id':'3'}]


#Fake Restaurants
tlist = {'name': 'The CRUDdy Crab', 'id': '1'}

lists = [{'name': 'The CRUDdy Crab', 'id': '1'}, {'name':'Blue Burgers', 'id':'2'},{'name':'Taco Hut', 'id':'3'}]


#Fake Menu Items
items = [ {'name':'Cheese Pizza', 'description':'made with fresh cheese', 'price':'$5.99','course' :'Entree', 'id':'1'}, {'name':'Chocolate Cake','description':'made with Dutch Chocolate', 'price':'$3.99', 'course':'Dessert','id':'2'},{'name':'Caesar Salad', 'description':'with fresh organic vegetables','price':'$5.99', 'course':'Entree','id':'3'},{'name':'Iced Tea', 'description':'with lemon','price':'$.99', 'course':'Beverage','id':'4'},{'name':'Spinach Dip', 'description':'creamy dip with fresh spinach','price':'$1.99', 'course':'Appetizer','id':'5'} ]
item =  {'name':'Cheese Pizza','description':'made with fresh cheese','price':'$5.99','course' :'Entree'}


#Main Page, Owners List, template 1
@app.route('/')
@app.route('/topten/')
def mainPage():
	return render_template('mainPage.html', items = owners, error_message = '')

#This page will be for creating a NEW OWNER, template 2
@app.route('/topten/new/')
def createNewOwner():
	return render_template('createNewOwner.html')

#This page will be for editing owner #, template 3'
@app.route('/topten/<int:owner_id>/edit')
def editOwner(owner_id):
	for i in owners:
		if int(i['id']) == owner_id:
			owner_to_edit = i['name']
	return render_template('editOwner.html', owner_id = owner_to_edit)

#This page will be for deleting owner #, template 4'
@app.route('/topten/<int:owner_id>/delete')
def deleteOwner(owner_id):
	for i in owners:
		if int(i['id']) == owner_id:
			owner_to_delete = i['name']
			print i['name']
	return render_template('deleteOwner.html', owner_id = owner_to_delete)

#### End Owner Page dependencies ###
#### Start ownerLists Pages  ####

#This page will show the top ten lists for owner #', template 5

#'This page will show the top ten lists for owner #' + str(owner_id) template 5
@app.route('/topten/<int:owner_id>/')
def ownerLists(owner_id):
	owner_exists = False
	for i in owners:
		if int(i['id']) == owner_id:
			owner = i['name']
			owner_exists = True
#will render page, or render mainpage if no owner exists
	try:
		owner
	except NameError:
		error_message = 'There was no owner found for this ID'
		return render_template('mainPage.html', items = owners, error_message = error_message )
	else:
		return render_template('ownerLists.html', owner = owner, items = lists)

#create a new list, template 6
@app.route('/topten/<int:owner_id>/new')
def createNewList(owner_id):
	for i in owners:
		if int(i['id']) == owner_id:
			owner_of_list = i['name']
	return render_template('createNewList.html', owner = owner_of_list)

#This page will be for EDITING list #, by owner template 7
@app.route('/topten/<int:owner_id>/<int:tlist_id>/edit')
def editList(owner_id, tlist_id):
	for i in owners:
		if int(i['id']) == owner_id:
			owner_of_list = i['name']
	for i in lists:
		if int(i['id']) == tlist_id:
			list_to_edit = i['name']
	return render_template('editList.html', owner = owner_of_list, tlist = list_to_edit)

#'This page is for DELETING list # by Owner #, template 8
@app.route('/topten/<int:owner_id>/<int:tlist_id>/delete')
def deleteList(owner_id, tlist_id):
	for i in owners:
		if int(i['id']) == owner_id:
			owner_of_list = i['name']
	for i in lists:
		if int(i['id']) == tlist_id:
			print i['name']
			print i['id']
			list_to_delete = i['name']
	return  render_template('deleteList.html', owner = owner_of_list, tlist = list_to_delete)
### End Top Ten Lists Dependencies ###
###  Start Top Ten Item Pages ###


#'This page will show the top ten items for list # by owner #template 9
@app.route('/topten/<int:owner_id>/<int:tlist_id>/')
def topTenItems(owner_id, tlist_id):
	for i in owners:
		if int(i['id']) == owner_id:
			owner_of_list = i['name']
	for i in lists:
		if int(i['id']) == tlist_id:
			tlist = i['name']
#will render page, or render  if no owner exists
	try:
		tlist
	except NameError:
		error_message = 'There was no List found for this ID'
		return render_template('ownerLists.html', owner = owner_of_list, items = lists, error_message = error_message )
	else:
		return render_template('topTenItems.html', owner = owner_of_list, tlist = tlist, items = items)

#'This page is for CREATING a new item in list # by owner #, template 10
@app.route('/topten/<int:owner_id>/<int:tlist_id>/new')
def createNewItem(owner_id, tlist_id):
	for i in owners:
		if int(i['id']) == owner_id:
			owner_of_list = i['name']
	for i in lists:
		if int(i['id']) == tlist_id:
			list_item_belongsto = i['name']
	return  render_template('createNewItem.html', owner = owner_of_list, tlist = list_item_belongsto)


#'This page is for EDITING item # in list #  by owner # template 11
@app.route('/topten/<int:owner_id>/<int:tlist_id>/<int:item_id>/edit/')
def editItem(owner_id, tlist_id, item_id):
	for i in owners:
		if int(i['id']) == owner_id:
			owner_of_list = i['name']
	for i in lists:
		if int(i['id']) == tlist_id:
			list_item_belongsto = i['name']
	for i in items:
		if int(i['id']) == item_id:
			item_to_edit = i['name']
	return  render_template('editItem.html', owner = owner_of_list, tlist = list_item_belongsto, item = item_to_edit)

#'This page is for DELETING item #, in list#, from author#, template 12
@app.route('/topten/<int:owner_id>/<int:tlist_id>/<int:item_id>/delete/')
def deleteItem(owner_id, tlist_id, item_id):
	for i in owners:
		if int(i['id']) == owner_id:
			owner_of_list = i['name']
	for i in lists:
		if int(i['id']) == tlist_id:
			list_item_belongsto = i['name']
	for i in items:
		if int(i['id']) == item_id:
			item_to_delete = i['name']
	return  render_template('deleteItem.html', owner = owner_of_list, tlist = list_item_belongsto, item = item_to_delete)


if __name__ == '__main__':
	app.debug = True
	app.run(host = '0.0.0.0', port = 5000)




