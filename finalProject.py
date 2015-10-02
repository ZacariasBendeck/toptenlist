from flask import Flask, render_template, url_for, request, redirect, flash, jsonify
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from database_setup import Base, Owner, Lists, Items

#imports for atom feeds
from urlparse import urljoin
from werkzeug.contrib.atom import AtomFeed

#oauth imports
from flask import session as login_session
import random, string
from oauth2client.client import flow_from_clientsecrets
from oauth2client.client import FlowExchangeError
import httplib2
import json
from flask import make_response
import requests

app = Flask(__name__)

engine = create_engine('sqlite:///finalProject.db')
Base.metadata.bind = engine

DBSession = sessionmaker(bind=engine)
session = DBSession()

#Main Page, Owners List, template 1
@app.route('/')
@app.route('/topten/')
def mainPage():
	owners = session.query(Owner).all()
	return render_template('mainPage.html', items = owners, login_session = login_session)

@app.route('/topten/items/all')
def allItems():
	items = session.query(Items).all()
	owner = session.query(Owner).first()
	owner_id = owner.id
	tlist = session.query(Lists).first()
	tlist_id = tlist.id
	return render_template('allItems.html', items = items, owner = owner, owner_id = owner_id, tlist_id = tlist_id)

@app.route('/topten/lists/all')
def allLists():
	owner = session.query(Owner).first()
	owner_id = owner.id
	lists = session.query(Lists).all()
	return render_template('allLists.html', owner = owner, owner_id = owner_id, items = lists)


#This page will be for creating a NEW OWNER, template 2
@app.route('/topten/new/', methods=['GET', 'POST'])
def createNewOwner():
	if request.method == 'POST':
		newOwner = Owner(name = request.form['name'], slogan = request.form['slogan'], pic_url = request.form['pic'], description = request.form['description'])
		session.add(newOwner)
		session.commit()
		flash('New Owner Created, ' + newOwner.name + ' will now be Blogging!!')
		return redirect(url_for('mainPage')) 
	else:	
		return render_template('createNewOwner.html')

#This page will be for editing owner #, template 3'
@app.route('/topten/<int:owner_id>/edit', methods=['GET', 'POST'])
def editOwner(owner_id):
	owner_to_edit = session.query(Owner).filter_by(id=owner_id).one()
	if request.method == 'POST':
		if not (request.form['slogan'] == ''):
			owner_to_edit.slogan = request.form['slogan']
		if not (request.form['name'] == ''):
			owner_to_edit.name = request.form['name']
		if not (request.form['pic'] == ''):
			owner_to_edit.pic_url = request.form['pic']
		session.add(owner_to_edit)
		session.commit()
		flash('Author\'s '+ owner_to_edit + ' details have been edited')
		return redirect(url_for('mainPage'))
	else:
		return render_template('editOwner.html', owner = owner_to_edit)

#This page will be for deleting owner #, template 4'
@app.route('/topten/<int:owner_id>/delete', methods=['GET', 'POST'])
def deleteOwner(owner_id):
	owner_to_delete = session.query(Owner).filter_by(id=owner_id).one()
	if request.method == 'POST':
		session.delete(owner_to_delete)
		flash(owner_to_delete.name + ' has been DELETED')
		return redirect(url_for('mainPage'))
	else:
		return render_template('deleteOwner.html', owner_to_delete = owner_to_delete)

#### End Owner Page dependencies ###
#### Start ownerLists Pages  ####

#This page will show the top ten lists for owner #', template 5
@app.route('/topten/<int:owner_id>/')
def ownerLists(owner_id):
	lists = session.query(Lists).filter_by(owner_id=owner_id).all()
	owners = session.query(Owner).filter_by(id=owner_id).all()
	if owners == []:
		flash('No author found at this location')
		return redirect(url_for('mainPage'))
	else:
		owner = session.query(Owner).filter_by(id=owner_id).one()
		return render_template('ownerLists.html', owner = owner, items = lists, owner_id = owner_id)

#Create a new list, template 6
@app.route('/topten/<int:owner_id>/new', methods=['GET', 'POST'])
def createNewList(owner_id):
	if request.method == 'POST':
		newList = Lists(name = request.form['name'], description = request.form['description'], pic_url = request.form['pic'], owner_id = owner_id)
		session.add(newList)
		session.commit()
		flash('New List Created, ' + newList.name + 'Now add items to your List!!')
		return redirect(url_for('ownerLists', owner_id = owner_id))
	else:	
		return render_template('createNewList.html', owner_id = owner_id)

#This page will be for EDITING list #, by owner template 7
@app.route('/topten/<int:owner_id>/<int:tlist_id>/edit', methods=['GET', 'POST'])
def editList(owner_id, tlist_id):
	owners = session.query(Owner).filter_by(id=owner_id).all()
	lists = session.query(Lists).filter_by(id=tlist_id).all()
	list_to_edit = session.query(Lists).filter_by(id=tlist_id).one()
	if request.method == 'POST':
		if not (request.form['name'] == ''):
			list_to_edit.name = request.form['name']
		if not (request.form['description'] == ''):
			list_to_edit.description = request.form['description']
		if not (request.form['pic_url'] == ''):
			list_to_edit.pic_url = request.form['pic_url']
		session.add(list_to_edit)
		session.commit()
		flash(list_to_edit.name + ' has been edited')
		return redirect(url_for('ownerLists', owner_id = owner_id))
	else:
		owner_of_list = session.query(Owner).filter_by(id=owner_id).one()
		list_to_edit = session.query(Lists).filter_by(id=tlist_id).one()
		return  render_template('editList.html', owner = owner_of_list, tlist = list_to_edit)

#'This page is for DELETING list # by Owner #, template 8
@app.route('/topten/<int:owner_id>/<int:tlist_id>/delete', methods=['GET', 'POST'])
def deleteList(owner_id, tlist_id):
	owners = session.query(Owner).filter_by(id=owner_id).all()
	lists = session.query(Lists).filter_by(id=tlist_id).all()
	if owners == []:
		flash('There was no owner for this address!!')
		return redirect(url_for('mainPage'))
	if lists == []:
		flash('There was no list for this address!!')
		return redirect(url_for('ownerLists', owner_id = owner_id))
	if request.method == 'POST':
		list_to_delete = session.query(Lists).filter_by(id=tlist_id).one()
		session.delete(list_to_delete)
		session.commit()
		flash(list_to_delete.name + ' has been DELETED!!')
		return redirect(url_for('ownerLists', owner_id = owner_id))
	else:	
		owner = session.query(Owner).filter_by(id=owner_id).one()
		tlist = session.query(Lists).filter_by(id=tlist_id).one()
		return render_template('deleteList.html', owner = owner, tlist = tlist, owner_id = owner_id, tlist_id = tlist_id)

### End Top Ten Lists Dependencies ###
###  Start Top Ten Item Pages ###

#'This page will show the top ten items for list # by owner #template 9
@app.route('/topten/<int:owner_id>/<int:tlist_id>/', methods=['GET', 'POST'])
def topTenItems(owner_id, tlist_id):
	## to do, add a nother segment showing honorable mentions, all those ranked above 10
	# right now we show only unranked and ranked in top ten
	owners = session.query(Owner).filter_by(id=owner_id).all()
	lists = session.query(Lists).filter_by(owner_id=owner_id).all()
	owner = session.query(Owner).filter_by(id=owner_id).one()
	tlist = session.query(Lists).filter_by(id=tlist_id).one()
	items = session.query(Items).filter(Items.lists_id == tlist_id, Items.rank > 0, Items.rank <= 10).order_by('rank')
	unranked_items = session.query(Items).filter(Items.lists_id == tlist_id, Items.rank == None).all()
	if request.method == 'POST':
		if (request.form['new_rank'] == ''):
			flash('No rerank was done!!')
			return redirect(url_for('topTenItems', owner_id = owner_id, tlist_id = tlist_id))
		else:
			print 'old rank, hidden' + str(request.form['old_rank_id']) + ', new rank =' + str(request.form['new_rank'])
			old_rank_id =request.form['old_rank_id']
			item_to_edit = session.query(Items).filter_by(id=old_rank_id).one()
			item_to_edit.rank = request.form['new_rank']
			session.add(item_to_edit)
			session.commit()
			return redirect(url_for('topTenItems', owner_id = owner_id, tlist_id = tlist_id, loggin_session = login_session))
	else:			
		if lists == []:
			flash('There were no lists for this address!!')
			return redirect(url_for('ownerLists', owner_id = owner_id))
		elif owners == []:
			flash('There were no lists for this address!!')
			return redirect(url_for('ownerLists', owner_id = owner_id))
		else:
			for i in items:
				print i.url
			owner_of_list = session.query(Owner).filter_by(id=owner_id).one()
			tlist = session.query(Lists).filter_by(id=tlist_id).one()
			return render_template('topTenItems.html', owner = owner, tlist = tlist, items = items, unranked_items = unranked_items, login_session = login_session)

#'This page is for CREATING a new item in list # by owner #, template 10
@app.route('/topten/<int:owner_id>/<int:tlist_id>/new', methods=['GET', 'POST'])
def createNewItem(owner_id, tlist_id):
	if 'username' not in login_session:
		flash('Sorry you must be logged in to create items!!')
		print ' login session variable is working!!'
		return redirect('/login')
	owners = session.query(Owner).filter_by(id=owner_id).all()
	lists = session.query(Lists).filter_by(id=tlist_id).all()
	if owners == []:
		flash('There was no owner for this address!!')
		return redirect(url_for('ownerLists', owner_id = owner_id))
	if lists == []:
		flash('There was no list for this address!!')
		return redirect(url_for('ownerLists', owner_id = owner_id))
	if request.method == 'POST':
		newItem = Items(name = request.form['name'], description = request.form['description'], url = request.form['url'], 
			second_pic_url = request.form['second_pic_url'], lists_id = tlist_id)
		session.add(newItem)
		session.commit()
		flash('New Item Created, ' + newItem.name + ' has been added!!')
		return redirect(url_for('topTenItems', owner_id = owner_id, tlist_id = tlist_id))
	else:	
		owner = session.query(Owner).filter_by(id=owner_id).one()
		tlist = session.query(Lists).filter_by(id=tlist_id).one()
		return render_template('createNewItem.html', owner = owner, tlist = tlist, owner_id = owner_id, tlist_id = tlist_id)


#'This page is for EDITING item # in list #  by owner # template 11
@app.route('/topten/<int:owner_id>/<int:tlist_id>/<int:item_id>/edit/', methods=['GET', 'POST'])
def editItem(owner_id, tlist_id, item_id):
	if 'username' not in login_session:
		return redirect('/login')
	owners = session.query(Owner).filter_by(id=owner_id).all()
	lists = session.query(Lists).filter_by(id=tlist_id).all()
	item_to_edit = session.query(Items).filter_by(id=item_id).one()
	if request.method == 'POST':
		if not (request.form['name'] == ''):
			item_to_edit.name = request.form['name']
		if not (request.form['description'] == ''):
			item_to_edit.description = request.form['description']
		if not (request.form['url'] == ''):
			item_to_edit.url = request.form['url']
		if not (request.form['second_pic_url'] == ''):
			item_to_edit.url = request.form['second_pic_url']
		if not (request.form['rank'] == ''):
			item_to_edit.rank = request.form['rank']
		session.add(item_to_edit)
		session.commit()
		flash(item_to_edit.name + ' has been edited')
		return redirect(url_for('topTenItems', owner_id = owner_id, tlist_id = tlist_id))
	else:
		owner_of_list = session.query(Owner).filter_by(id=owner_id).one()
		list_item_belongsto = session.query(Lists).filter_by(id=tlist_id).one()
		return  render_template('editItem.html', owner = owner_of_list, tlist = list_item_belongsto, item = item_to_edit)

#'This page is for DELETING item #, in list#, from author#, template 12
@app.route('/topten/<int:owner_id>/<int:tlist_id>/<int:item_id>/delete/', methods=['GET', 'POST'])
def deleteItem(owner_id, tlist_id, item_id):
	owners = session.query(Owner).filter_by(id=owner_id).all()
	lists = session.query(Lists).filter_by(id=tlist_id).all()
	items = session.query(Items).filter_by(id = item_id).all()
	if owners == []:
		flash('There was no owner for this address!!')
		return redirect(url_for('mainPage'))
	if lists == []:
		flash('There was no list for this address!!')
		return redirect(url_for('ownerLists', owner_id = owner_id))
	if items == []:
		flash('There was no item at this address!!')
		return redirect(url_for('toptenItems', owner_id = owner_id))
	if request.method == 'POST':
		item_to_delete = session.query(Items).filter_by(id=item_id).one()
		session.delete(item_to_delete)
		session.commit()
		flash(item_to_delete.name + ' has been DELETED!!')
		return redirect(url_for('topTenItems', owner_id = owner_id, tlist_id = tlist_id))
	else:	
		owner = session.query(Owner).filter_by(id=owner_id).one()
		tlist = session.query(Lists).filter_by(id=tlist_id).one()
		item_to_delete = session.query(Items).filter_by(id=item_id).one()
		return render_template('deleteItem.html', owner = owner, tlist = tlist, owner_id = owner_id, tlist_id = tlist_id, item_id = item_id, item = item_to_delete, user_pic = login_session['picture'])

#Helper Functions
def ownerExists(owner_id):
	owners = session.query(Owner).filter_by(id=owner_id).all()
	if owners == []:
		return False
	else:
		return True

##  JSON API endpoints  start
@app.route('/topten/owners/JSON/')
def topTenOwnersJSON():
	owners = session.query(Owner).all()
	return jsonify(Owner = [i.serialize for i in owners])

@app.route('/topten/lists/JSON/')
def listsJSON():
	items = session.query(Lists).all()
	return jsonify(Lists = [i.serialize for i in items])

@app.route('/topten/items/JSON/')
def itemsJSON():
	items = session.query(Items).all()
	return jsonify(Items = [i.serialize for i in items])

@app.route('/topten/<int:owner_id>/Lists/JSON/')
def ownerListsJSON(owner_id):
	lists = session.query(Lists).filter_by(owner_id = owner_id).all()
	return jsonify(Lists = [i.serialize for i in lists])

@app.route('/topten/<int:lists_id>/Items/JSON/')
def listItemsJSON(lists_id):
	items = session.query(Items).filter_by(lists_id = lists_id).all()
	return jsonify(Items = [i.serialize for i in items])

@app.route('/topten/<int:item_id>/JSON/')
def itemJSON(item_id):
	items = session.query(Items).filter_by(id = item_id).all()
	return jsonify(Items = [i.serialize for i in items])


## End JSON API endpoints

## Start Atomic Feed ###
def make_external(url):
	return urljoin(request.url_root, url)
'''
@app.route('/recent.atom')
def recent_feed():
	feed = AtomFeed('Recent Items',
					feed_url=request.url, url=request.url_root)
	items = session.query(Items).limit(15).all()
	for item in items:
		feed.add(item.name, item.description, content_type = 'html', author = item.lists_id, url = make_external(item.url), updated = item.name, published = item.name)
	return feed.get_response()
'''

CLIENT_ID = json.loads(
	open('client_secrets.json', 'r').read())['web']['client_id']
APPLICATION_NAME = "Top Ten Webpage"


# Create anti-forgery state token
@app.route('/login')
def showLogin():	
	print CLIENT_ID
	state = ''.join(random.choice(string.ascii_uppercase + string.digits)
					for x in xrange(32))
	login_session['state'] = state
	# return "The current session state is %s" % login_session['state']
	return render_template('login.html', STATE=state)


@app.route('/gconnect', methods=['POST'])
def gconnect():
	# Validate state token
	if request.args.get('state') != login_session['state']:
		response = make_response(json.dumps('Invalid state parameter.'), 401)
		response.headers['Content-Type'] = 'application/json'
		return response
	# Obtain authorization code
	code = request.data

	try:
		# Upgrade the authorization code into a credentials object
		oauth_flow = flow_from_clientsecrets('client_secrets.json', scope='')
		oauth_flow.redirect_uri = 'postmessage'
		credentials = oauth_flow.step2_exchange(code)
	except FlowExchangeError:
		response = make_response(
			json.dumps('Failed to upgrade the authorization code.'), 401)
		response.headers['Content-Type'] = 'application/json'
		return response

	# Check that the access token is valid.
	access_token = credentials.access_token
	url = ('https://www.googleapis.com/oauth2/v1/tokeninfo?access_token=%s'
		   % access_token)
	h = httplib2.Http()
	result = json.loads(h.request(url, 'GET')[1])
	# If there was an error in the access token info, abort.
	if result.get('error') is not None:
		response = make_response(json.dumps(result.get('error')), 500)
		response.headers['Content-Type'] = 'application/json'

	# Verify that the access token is used for the intended user.
	gplus_id = credentials.id_token['sub']
	if result['user_id'] != gplus_id:
		response = make_response(
			json.dumps("Token's user ID doesn't match given user ID."), 401)
		response.headers['Content-Type'] = 'application/json'
		return response

	# Verify that the access token is valid for this app.
	if result['issued_to'] != CLIENT_ID:
		response = make_response(
			json.dumps("Token's client ID does not match app's."), 401)
		print "Token's client ID does not match app's."
		response.headers['Content-Type'] = 'application/json'
		return response

	stored_credentials = login_session.get('access_token')
	stored_gplus_id = login_session.get('gplus_id')
	if stored_credentials is not None and gplus_id == stored_gplus_id:
		response = make_response(json.dumps('Current user is already connected.'),
								 200)
		response.headers['Content-Type'] = 'application/json'
		return response

	# Store the access token in the session for later use.
	login_session['credentials'] = credentials.access_token
	login_session['gplus_id'] = gplus_id

	# Get user info
	userinfo_url = "https://www.googleapis.com/oauth2/v1/userinfo"
	params = {'access_token': credentials.access_token, 'alt': 'json'}
	answer = requests.get(userinfo_url, params=params)

	data = answer.json()

	login_session['username'] = data['name']
	login_session['picture'] = data['picture']
	login_session['email'] = data['email']

	output = ''
	output += '<h1>Welcome, '
	output += login_session['username']
	output += '!</h1>'
	output += '<img src="'
	output += login_session['picture']
	output += ' " style = "width: 300px; height: 300px;border-radius: 150px;-webkit-border-radius: 150px;-moz-border-radius: 150px;"> '
	flash("you are now logged in as %s" % login_session['username'])
	print login_session['username'] + 'has logged in with google+...  done!'
	return output

@app.route('/gdisconnect')
def gdisconnect():
		# Only disconnect a connected user.
	credentials = login_session.get('credentials')
	if credentials is None:
		response = make_response(
			json.dumps('Current user not connected.'), 401)
		response.headers['Content-Type'] = 'application/json'
		return response
	print ' login_session credentiasls' + str(login_session.get('credentials'))
	access_token = credentials
	url = 'https://accounts.google.com/o/oauth2/revoke?token=%s' % access_token
	h = httplib2.Http()
	result = h.request(url, 'GET')[0]

	if result['status'] == '200':
		# Reset the user's sesson.
		del login_session['credentials']
		del login_session['gplus_id']
		del login_session['username']
		del login_session['email']
		del login_session['picture']

		response = make_response(json.dumps('Successfully disconnected.'), 200)
		response.headers['Content-Type'] = 'application/json'
		return response
	else:
		# For whatever reason, the given token was invalid.
		response = make_response(
			json.dumps('Failed to revoke token for given user.', 400))
		response.headers['Content-Type'] = 'application/json'
		return response
	

if __name__ == '__main__':
	app.secret_key = 'super_secret_key'
	app.debug = True
	app.run(host = '0.0.0.0', port = 5000)