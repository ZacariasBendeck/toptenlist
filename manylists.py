from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
 
from database_setup import Base, Owner, Lists, Items
 
engine = create_engine('sqlite:///finalProject.db')
# Bind the engine to the metadata of the Base class so that the
# declaratives can be accessed through a DBSession instance
Base.metadata.bind = engine
 
DBSession = sessionmaker(bind=engine)
# A DBSession() instance establishes all conversations with the database
# and represents a "staging zone" for all the objects loaded into the
# database session object. Any change made against the objects in the
# session won't be persisted into the database until you call
# session.commit(). If you're not happy about the changes, you can
# revert all of them back to the last commit by calling
# session.rollback()
session = DBSession()

owners =  [{'name': 'Zacarias Bendeck', 'id': '1'}, {'name':'Gabriela Tentori', 'id':'2'},{'name':'Mario Rojas', 'id':'3'}]
lists = [{'id','1','name','Joseph Ducreax Memes','description','This Guy knows where its at!','owner_id','1',},
	{'id','2','name','Best Programming Youtube Sites','description','','owner_id','1'},
	{'id','4','name','Cutest Cats','description','Sooooo Cute','owner_id','2'},
	{'id','5','name','Cutest Dogs','description','Looove them!','owner_id','2'},
	{'id','6','name','Love quotes','description','Make me wanna cry','owner_id','2'},
	{'id','7','name','Marvel Heroes','description','Cant wait for the next film','owner_id','3'},
	{'id','8','name','Models','description','Spank to these','owner_id','3'},
	{'id','9','name','Watch Mojo Videos','description','Pretty Cool','owner_id','3'}
]
items = [{'id','3','name','Kinsperson','description','Joseph Ducreax Memes','url','https://jukebox9.files.wordpress.com/2015/08/21.jpg','list_id','1'},
	{'id','4','name','They Observe Me Voyaging','description','Joseph Ducreax Memes','url','https://s-media-cache-ak0.pinimg.com/236x/50/5d/0e/505d0e7897b1bd94e26b85eb028c58e2.jpg','list_id','1'},
	{'id','5','name','You Doth Aspire','description','Joseph Ducreax Memes','url','https://jukebox9.files.wordpress.com/2015/08/31.jpg','list_id','1'},
	{'id','6','name','Quiet Down','description','Joseph Ducreax Memes','url','http://i2.kym-cdn.com/photos/images/original/000/464/285/17b.png','list_id','1'},
	{'id','7','name','BubbleGoth','description','Sooooo Cute','url','http://cdn.buzznet.com/assets/users16/kerli/default/cutest-cats--large-msg-134704087653.jpg','list_id','4'},
	{'id','8','name','Pinterest','description','Sooooo Cute','url','https://s-media-cache-ak0.pinimg.com/736x/8c/99/e3/8c99e3483387df6395da674a6b5dee4c.jpg','list_id','4'},
	{'id','9','name','Adorable','description','Sooooo Cute','url','http://amazinganimalphotos.com/wp-content/uploads/2013/04/cutest-cat-picture-ever.jpg','list_id','4'},
	{'id','10','name','Kerli','description','Sooooo Cute','url','http://cdn.buzznet.com/assets/users16/kerli/default/cutest-cats--large-msg-134704089222.jpg','list_id','4'},
	{'id','11','name','Cute','description','Sooooo Cute','url','http://cdn.buzznet.com/assets/users16/kerli/default/cutest-cats--large-msg-134704090282.jpg','list_id','4'},
	{'id','12','name','Blendspace','description','Sooooo Cute','url','http://cdn.cutestpaw.com/wp-content/uploads/2011/11/cute-cat-l.jpg','list_id','4'},
	{'id','14','name','Lifewithdogs','description','Little wolfie','url','http://www.lifewithdogs.tv/wp-content/uploads/2014/03/3.21.14-National-Puppy-Day25.jpg','list_id','5'},
	{'id','15','name','Cutie','description','Not me!','url','http://dailynewsdig.com/wp-content/uploads/2013/05/top-10-cutest-puppies-in-the-world-2.jpg','list_id','5'},
	{'id','16','name','Bluie','description','angry little one','url','http://thefabweb.com/wp-content/uploads/2013/02/Cutest-Puppies-Ever-181.jpg','list_id','5'},
	{'id','17','name','dogvacay','description','awwww','url','https://blog-photos.dogvacay.com/wp-content/uploads/2012/03/cute-dog-puppy-white-Favim.com-267645.jpg','list_id','5'},
	{'id','18','name','Love1','description','lovely','url','http://ideas.hallmark.com/wp-content/uploads/2015/05/love-quotes-06.png','list_id','6'},

	]

# Zacas Lists
owner1 = Owner(name = "Zacarias Bendeck", description = "Software Engineer", slogan = 'The man', pic_url = 'https://scontent-mia1-1.xx.fbcdn.net/hphotos-xfp1/v/t1.0-9/12065639_10153679634989772_1698217283237619988_n.jpg?oh=e14ecdc23a71554d17fcdc94b42660d6&oe=5699C5C3')
session.add(owner1)
session.commit()

# add Zaca's Lists
List1 = Lists(name = 'Joseph Ducreax Memes', description = 'This Guy knows where its at!', owner = owner1)
session.add(List1)
session.commit()

List2 = Lists(name = 'Best Programming Youtube Sites', description = '', owner = owner1)
session.add(List2)
session.commit()

#Add Zaca's Items
Item1 = Items(name = 'Kinsperson', description = 'Joseph Ducreax Memes', url = 'https://jukebox9.files.wordpress.com/2015/08/21.jpg',  lists = List1)
session.add(Item1)
session.commit()

Item1 = Items(name = 'They Observe Me Voyaging', description = 'Joseph Ducreax Memes', url = 'https://s-media-cache-ak0.pinimg.com/236x/50/5d/0e/505d0e7897b1bd94e26b85eb028c58e2.jpg',  lists = List1)
session.add(Item1)
session.commit()

Item1 = Items(name = 'You Doth Aspire', description = 'Joseph Ducreax Memes', url = 'https://jukebox9.files.wordpress.com/2015/08/31.jpg',  lists = List1)
session.add(Item1)
session.commit()

Item1 = Items(name = 'Quiet Down', description = 'Joseph Ducreax Memes', url = 'http://i2.kym-cdn.com/photos/images/original/000/464/285/17b.png',  lists = List1)
session.add(Item1)
session.commit()

#Gaby's Lists Add Gaby
owner2 = Owner(name = "Gabriela Tentori", description = 'TV Star', pic_url = 'https://scontent-mia1-1.xx.fbcdn.net/hphotos-xpa1/v/t1.0-9/10452390_10152971538924788_66680664246420735_n.jpg?oh=cb8290ab9a80fb1909ca96f0b8c5f819&oe=5689FE4C')
session.add(owner2)
session.commit()

# add Gaby's Lists
List1 = Lists(name = 'Cutest Cats', description = 'Sooooo Cute', owner = owner2)
session.add(List1)
session.commit()

List2 = Lists(name = 'Cutest Dogs', description = 'Looove them!', owner = owner2)
session.add(List2)
session.commit()

List3 = Lists(name = 'Love quotes', description = 'Make me wanna cry', owner = owner2)
session.add(List2)
session.commit()

#Add Gaby's Items
Item1 = Items(name = 'BubbleGoth', description = 'Sooooo Cute', url = 'http://cdn.buzznet.com/assets/users16/kerli/default/cutest-cats--large-msg-134704087653.jpg',  lists = List1)
session.add(Item1)
session.commit()

Item1 = Items(name = 'Pinterest', description = 'Sooooo Cute', url = 'https://s-media-cache-ak0.pinimg.com/736x/8c/99/e3/8c99e3483387df6395da674a6b5dee4c.jpg',  lists = List1)
session.add(Item1)
session.commit()

Item1 = Items(name = 'Adorable', description = 'Sooooo Cute', url = 'http://amazinganimalphotos.com/wp-content/uploads/2013/04/cutest-cat-picture-ever.jpg',  lists = List1)
session.add(Item1)
session.commit()

Item1 = Items(name = 'Kerli', description = 'Sooooo Cute', url = 'http://cdn.buzznet.com/assets/users16/kerli/default/cutest-cats--large-msg-134704089222.jpg',  lists = List1)
session.add(Item1)
session.commit()

Item1 = Items(name = 'Cute', description = 'Sooooo Cute', url = 'http://cdn.buzznet.com/assets/users16/kerli/default/cutest-cats--large-msg-134704090282.jpg',  lists = List1)
session.add(Item1)
session.commit()

# Obama's Lists
owner1 = Owner(name = "Barack Obama", description = "President of the United States", pic_url = 'https://scontent-mia1-1.xx.fbcdn.net/hphotos-xpa1/v/t1.0-9/1376580_10151878817796749_162570700_n.png?oh=a1c4ec9ad5aed7f5f660c970743c166e&oe=569D44A0')
session.add(owner1)
session.commit()

# Mario's Lists
owner1 = Owner(name = "Mario Rojas", slogan = 'Born to be Wild', description = "Artist", pic_url = 'https://scontent-mia1-1.xx.fbcdn.net/hphotos-xlf1/v/t1.0-9/11990562_10153740461450984_7344915039710784206_n.jpg?oh=f3841f44ec3c6eb918ffc26781af7034&oe=568BCD43')
session.add(owner1)
session.commit()




'''
#item template
Item1 = Items(,  lists = List1)
session.add(Item1)
session.commit()

Item2 = Items(,  lists = List1)
session.add(Item2)
session.commit()

Item3 = Items(,  lists = List1)
session.add(Item3)
session.commit()

Item4 = Items(,  lists = List1)
session.add(Item4)
session.commit()
'''

print "Added Owner, Lists and Items"