from flask import Flask, render_template, url_for, request, redirect, flash, jsonify
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from database_setup import Base, Owner, Lists, Items

#oauth imports
from flask import session as login_session
import random, string
from oauth2client.client import flow_from_clientsecrets
from oauth2client.client import FlowExchangeError
import httplib2
import json
from flask import make_response
import requests

CLIENT_ID = json.loads(
    open('client_secrets.json', 'r').read())['web']['client_id']
APPLICATION_NAME = "Restaurant Menu App"

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
	section2 = str(ownerListSection(1))
	return render_template('mainPage.html', items = owners, 
		login_session = login_session,section2=section2)

#This page will be for creating a NEW OWNER, template 2
@app.route('/topten/new/', methods=['GET', 'POST'])
def createNewOwner():
	if 'username' not in login_session:
		return redirect('/login')
   	if request.method == 'POST':
		newOwner = Owner(name = request.form['name'], slogan = request.form['slogan'], 
			pic_url = request.form['pic'], description = request.form['description'])
		session.add(newOwner)
		session.commit()
		flash('New Owner Created, ' + newOwner.name + ' will now be Blogging!!')
		return redirect(url_for('mainPage')) 
	else:	
		return render_template('createNewOwner.html')
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
		return render_template('ownerLists.html', owner = owner, 
			items = lists, owner_id = owner_id, login_session = login_session)

#Create a new list, template 6
@app.route('/topten/<int:owner_id>/new', methods=['GET', 'POST'])
def createNewList(owner_id):
	if 'username' not in login_session:
		return redirect('/login')
	owner = session.query(Owner).filter_by(id=owner_id).one()
	print owner.id + login_session['user_id']
	print (owner.id == login_session['user_id'])
	print owner.id, login_session['user_id']
	if owner.id != login_session['user_id']:
		flash('You are not authorized to Add Lists for %s' % owner.name)
		flash('Select the user you created to make a list')
		return redirect(url_for('mainPage'))
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
	if 'username' not in login_session:
		return redirect('/login')
	if list_to_edit.owner_id != login_session['user_id']:
		flash('You are not authorized to edit %s' % list_to_edit.name)
		flash('Only %s may edit this List ' % list_to_edit.owner.name)
		return redirect(url_for('mainPage'))
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
	list_to_delete = session.query(Lists).filter_by(id=tlist_id).one()	
	if 'username' not in login_session:
		return redirect('/login')
	if list_to_delete.owner_id != login_session['user_id']:
		flash('You are not authorized to Delete %s' % list_to_delete.name)
		flash('Only %s may Delete this List ' % list_to_delete.owner.name)
		return redirect(url_for('mainPage'))
	if owners == []:
		flash('There was no owner for this address!!')
		return redirect(url_for('mainPage'))
	if lists == []:
		flash('There was no list for this address!!')
		return redirect(url_for('ownerLists', owner_id = owner_id))
	if request.method == 'POST':
		list_to_delete = session.query(Lists).filter_by(id=tlist_id).one()
		items_to_delete = session.query(Items).filter_by(lists_id=tlist_id).all()
		session.delete(list_to_delete)
		session.delete(items_to_delete)
		session.commit()
		flash(list_to_delete.name + ' has been DELETED!!')
		return redirect(url_for('ownerLists', owner_id = owner_id))
	else:	
		owner = session.query(Owner).filter_by(id=owner_id).one()
		tlist = session.query(Lists).filter_by(id=tlist_id).one()
		items = session.query(Items).filter_by(lists_id = tlist_id).all()
		return render_template('deleteList.html', owner = owner, tlist = tlist, 
			owner_id = owner_id, tlist_id = tlist_id, items = items)

### End Top Ten Lists Dependencies ###
###  Start Top Ten Item Pages ###

#'This page will show the top ten items for list # by owner #template 9
@app.route('/topten/<int:owner_id>/<int:tlist_id>/')
def topTenItems(owner_id, tlist_id):
	owners = session.query(Owner).filter_by(id=owner_id).all()
	lists = session.query(Lists).filter_by(owner_id=owner_id).all()
	items = session.query(Items).filter_by(lists_id = tlist_id).order_by('rank').all()
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
		return render_template('topTenItems.html', owner = owner_of_list,
			tlist = tlist, items = items, owner_id = owner_id, tlist_id = tlist_id,
			login_session = login_session)

#'This page is for CREATING a new item in list # by owner #, template 10
@app.route('/topten/<int:owner_id>/<int:tlist_id>/new', methods=['GET', 'POST'])
def createNewItem(owner_id, tlist_id):
	if 'username' not in login_session:
		return redirect('/login')
	owner_of_list = session.query(Owner).filter_by(id=owner_id).one()
	list_to_add = session.query(Lists).filter_by(id=tlist_id).one()
	if owner_of_list == []:
		flash('There was no owner for this address!!')
		return redirect(url_for('ownerLists', owner_id = owner_id))
	if list_to_add == []:
		flash('There was no list for this address!!')
		return redirect(url_for('ownerLists', owner_id = owner_id))
	if 'username' not in login_session:
		return redirect('/login')
	if owner_of_list.id != login_session['user_id']:
		flash('You are not authorized to Edit %s' % list_to_add.name)
		flash('Only %s may Create Items in this List ' % owner_of_list.name)
		return redirect(url_for('mainPage'))
	if request.method == 'POST':
		newItem = Items(name = request.form['name'], description = request.form['description'], url = request.form['url'], lists_id = tlist_id)
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
	owners = session.query(Owner).filter_by(id=owner_id).all()
	lists = session.query(Lists).filter_by(id=tlist_id).all()
	item_to_edit = session.query(Items).filter_by(id=item_id).one()
	if 'username' not in login_session:
		return redirect('/login')
	if item_to_edit.lists.owner_id != login_session['user_id']:
		flash('You are not authorized to Edit %s' % item_to_edit.name)
		flash('Only %s may Delete this List ' % item_to_edit.lists.owner.name)
		return redirect(url_for('mainPage'))
	if request.method == 'POST':
		if not (request.form['name'] == ''):
			item_to_edit.name = request.form['name']
		if not (request.form['description'] == ''):
			item_to_edit.description = request.form['description']
		if not (request.form['url'] == ''):
			item_to_edit.pic_url = request.form['pic_url']
		if not (request.form['second_pic_url'] == ''):
			list_to_edit.pic_url = request.form['second_pic_url']
		if not (request.form['rank'] == ''):
			item_to_edit.rank = request.form['rank']
		session.add(item_to_edit)
		session.commit()
		flash(item_to_edit.name + ' has been edited')
		return redirect(url_for('topTenItems', owner_id = item.lists.owner_id, tlist_id = tlist_id))
	else:
		owner_of_list = session.query(Owner).filter_by(id=owner_id).one()
		list_item_belongsto = session.query(Lists).filter_by(id=tlist_id).one()
		return  render_template('editItem.html', tlist = list_item_belongsto, item = item_to_edit)

#'This page is for DELETING item #, in list#, from author#, template 12
@app.route('/topten/<int:owner_id>/<int:tlist_id>/<int:item_id>/delete/', methods=['GET', 'POST'])
def deleteItem(owner_id, tlist_id, item_id):
	item_to_delete = session.query(Items).filter_by(id=item_id).one()
	if 'username' not in login_session:
		return redirect('/login')
	if item_to_delete.lists.owner_id != login_session['user_id']:
		flash('You are not authorized to Delete %s' % item_to_delete.name)
		flash('Only %s may Delete this Item ' % item_to_delete.lists.owner.name)
		return redirect(url_for('mainPage'))
		return redirect(url_for('toptenItems', owner_id = owner_id))
	if request.method == 'POST':
		session.delete(item_to_delete)
		session.commit()
		flash(item_to_delete.name + ' has been DELETED!!')
		return redirect(url_for('topTenItems', owner_id = owner_id, tlist_id = tlist_id))
	else:	
		owner = session.query(Owner).filter_by(id=owner_id).one()
		tlist = session.query(Lists).filter_by(id=tlist_id).one()
		item_to_delete = session.query(Items).filter_by(id=item_id).one()
		return render_template('deleteItem.html', owner = owner, tlist = tlist, owner_id = owner_id, tlist_id = tlist_id, item_id = item_id, item = item_to_delete)

#Section Functions
def ownerListSection(owner_id):
	lists = session.query(Lists).filter_by(owner_id=owner_id).all()
	owner = session.query(Owner).filter_by(id=owner_id).one()
	return render_template('ownerListSection.html', owner = owner, 
		items = lists, owner_id = owner.id)

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

@app.route('/topten/Lists/JSON/')
def ListsJSON():
	items = session.query(Lists).all()
	return jsonify(Items = [i.serialize for i in items])

@app.route('/topten/Items/JSON/')
def itemsJSON():
	items = session.query(Items).all()
	return jsonify(Items = [i.serialize for i in items])
   
@app.route('/topten/<int:owner_id>/Lists/JSON/')
def ownerListsJSON(owner_id):
	lists = session.query(Lists).filter_by(owner_id = owner_id).all()
	return jsonify(Lists = [i.serialize for i in lists])
@app.route('/topten/<int:lists_id>/Items/JSON/')
def listJSON(lists_id):
	items = session.query(Items).filter_by(lists_id = lists_id).all()
	return jsonify(Items = [i.serialize for i in items])
@app.route('/topten/<int:item_id>/Lists/Items/JSON/')
def itemJSON(item_id):
	items = session.query(Items).filter_by(id = item_id).all()
	return jsonify(Items = [i.serialize for i in items])
## End JSON API endpoints

CLIENT_ID = json.loads(
    open('client_secrets.json', 'r').read())['web']['client_id']
APPLICATION_NAME = "My Top Ten Lists"

# Create anti-forgery state token
@app.route('/login')
def showLogin():
    state = ''.join(random.choice(string.ascii_uppercase + string.digits)
                    for x in xrange(32))
    login_session['state'] = state
    # return "The current session state is %s" % login_session['state']
    return render_template('login.html', STATE=state)


@app.route('/fbconnect', methods=['POST'])
def fbconnect():
    if request.args.get('state') != login_session['state']:
        response = make_response(json.dumps('Invalid state parameter.'), 401)
        response.headers['Content-Type'] = 'application/json'
        return response
    access_token = request.data
    print "access token received %s " % access_token

    app_id = json.loads(open('fb_client_secrets.json', 'r').read())[
        'web']['app_id']
    app_secret = json.loads(
        open('fb_client_secrets.json', 'r').read())['web']['app_secret']
    url = 'https://graph.facebook.com/oauth/access_token?grant_type=fb_exchange_token&client_id=%s&client_secret=%s&fb_exchange_token=%s' % (
        app_id, app_secret, access_token)
    h = httplib2.Http()
    result = h.request(url, 'GET')[1]

    # Use token to get user info from API
    userinfo_url = "https://graph.facebook.com/v2.4/me"
    # strip expire tag from access token
    token = result.split("&")[0]


    url = 'https://graph.facebook.com/v2.4/me?%s&fields=name,id,email' % token
    h = httplib2.Http()
    result = h.request(url, 'GET')[1]
    # print "url sent for API access:%s"% url
    # print "API JSON result: %s" % result
    data = json.loads(result)
    login_session['provider'] = 'facebook'
    login_session['username'] = data["name"]
    login_session['email'] = data["email"]
    login_session['facebook_id'] = data["id"]

    # The token must be stored in the login_session in order to properly logout, let's strip out the information before the equals sign in our token
    stored_token = token.split("=")[1]
    login_session['access_token'] = stored_token

    # Get user picture
    url = 'https://graph.facebook.com/v2.4/me/picture?%s&redirect=0&height=200&width=200' % token
    h = httplib2.Http()
    result = h.request(url, 'GET')[1]
    data = json.loads(result)

    login_session['picture'] = data["data"]["url"]

    # see if user exists
    user_id = getUserID(login_session['email'])
    if not user_id:
        user_id = createUser(login_session)
    login_session['user_id'] = user_id

    output = ''
    output += '<h1>Welcome, '
    output += login_session['username']

    output += '!</h1>'
    output += '<img src="'
    output += login_session['picture']
    output += ' " style = "width: 300px; height: 300px;border-radius: 150px;-webkit-border-radius: 150px;-moz-border-radius: 150px;"> '

    flash("Now logged in as %s" % login_session['username'])
    return output


@app.route('/fbdisconnect')
def fbdisconnect():
    facebook_id = login_session['facebook_id']
    # The access token must me included to successfully logout
    access_token = login_session['access_token']
    url = 'https://graph.facebook.com/%s/permissions?access_token=%s' % (facebook_id,access_token)
    h = httplib2.Http()
    result = h.request(url, 'DELETE')[1]
    return "you have been logged out"


@app.route('/gconnect', methods=['POST'])
def gconnect():
    # Validate state token
    if request.args.get('state') != login_session['state']:
        response = make_response(json.dumps('Invalid state parameter.'), 401)
        response.headers['Content-Type'] = 'application/json'
        print 'part 1 ok'
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
        print 'part 2 failed'
        return response

    # Check that the access token is valid.
    access_token = credentials.access_token
    print access_token, 'access_token'
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
    print 'Verify that the access token is valid for this app.'

    stored_credentials = login_session.get('credentials')
    stored_gplus_id = login_session.get('gplus_id')
    if stored_credentials is not None and gplus_id == stored_gplus_id:
        response = make_response(json.dumps('Current user is already connected.'),
                                 200)
        response.headers['Content-Type'] = 'application/json'
        return response

    # Store the access token in the session for later use.
    login_session['credentials'] = credentials.access_token
    login_session['gplus_id'] = gplus_id
    print 'Store the access token in the session for later use.'

    # Get user info
    userinfo_url = "https://www.googleapis.com/oauth2/v1/userinfo"
    params = {'access_token': credentials.access_token, 'alt': 'json'}
    print 'params !!!!!!******'
    answer = requests.get(userinfo_url, params=params)

    data = answer.json()
    print ' NOT SERIALIZABLE!'

    login_session['username'] = data['name']
    login_session['picture'] = data['picture']
    login_session['email'] = data['email']
    # ADD PROVIDER TO LOGIN SESSION
    login_session['provider'] = 'google'

    # see if user exists, if it doesn't make a new one
    user_id = getUserID(data["email"])
    if not user_id:
        user_id = createUser(login_session)
    login_session['user_id'] = user_id

    output = ''
    output += '<h1>Welcome, '
    output += login_session['username']
    output += '!</h1>'
    output += '<img src="'
    output += login_session['picture']
    output += ' " style = "width: 300px; height: 300px;border-radius: 150px;-webkit-border-radius: 150px;-moz-border-radius: 150px;"> '
    flash("you are now logged in as %s" % login_session['username'])
    print "done!"
    return output

# User Helper Functions


def createUser(login_session):
    newUser = Owner(name=login_session['username'], email=login_session[
                   'email'], pic_url=login_session['picture'])
    session.add(newUser)
    session.commit()
    user = session.query(Owner).filter_by(email=login_session['email']).one()
    return user.id


def getUserInfo(user_id):
    user = session.query(Owner).filter_by(id=user_id).one()
    return user


def getUserID(email):
    try:
        user = session.query(Owner).filter_by(email=email).one()
        return user.id
    except:
        return None

# DISCONNECT - Revoke a current user's token and reset their login_session


@app.route('/gdisconnect')
def gdisconnect():
    # Only disconnect a connected user.
    credentials = login_session.get('credentials')
    if credentials is None:
        response = make_response(
            json.dumps('Current user not connected.'), 401)
        response.headers['Content-Type'] = 'application/json'
        return response
    access_token = credentials
    url = 'https://accounts.google.com/o/oauth2/revoke?token=%s' % access_token
    h = httplib2.Http()
    result = h.request(url, 'GET')[0]
    if result['status'] != '200':
        # For whatever reason, the given token was invalid.
        response = make_response(
            json.dumps('Failed to revoke token for given user.', 400))
        response.headers['Content-Type'] = 'application/json'
        return response

# Disconnect based on provider
@app.route('/disconnect')
def disconnect():
    if 'provider' in login_session:
        if login_session['provider'] == 'google':
            gdisconnect()
            del login_session['gplus_id']
            del login_session['credentials']
        if login_session['provider'] == 'facebook':
            fbdisconnect()
            del login_session['facebook_id']
        del login_session['username']
        del login_session['email']
        del login_session['picture']
        del login_session['user_id']
        del login_session['provider']
        flash("You have successfully been logged out.")
        return redirect(url_for('mainPage'))
    else:
        flash("You were not logged in")
        return redirect(url_for('mainPage'))

	

if __name__ == '__main__':
	app.secret_key = 'super_secret_key'
	app.debug = True
	app.run(host = '0.0.0.0', port = 5000)