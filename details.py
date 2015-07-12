import os
import logging

import json

from pyramid.config import Configurator
from pyramid.session import UnencryptedCookieSessionFactoryConfig

from wsgiref.simple_server import make_server

from pyramid.events import NewRequest
from pyramid.events import subscriber
from pyramid.events import ApplicationCreated
import sqlite3

from pyramid.exceptions import NotFound
from pyramid.httpexceptions import HTTPFound
from pyramid.view import view_config


logging.basicConfig()
log = logging.getLogger(__file__)

here = os.path.dirname(os.path.abspath(__file__))

@subscriber(ApplicationCreated)
def application_created_subscriber(event):
	log.warn('Initializing database...')
	with open(os.path.join(here, 'schema.sql')) as f:
		stmt = f.read()
		settings = event.app.registry.settings
		db = sqlite3.connect(settings['db'])
		db.executescript(stmt)

@subscriber(NewRequest)
def new_request_subscriber(event):
	request = event.request
	settings = request.registry.settings
	request.db = sqlite3.connect(settings['db'])
	request.add_finished_callback(close_db_connection)

def close_db_connection(request):
	request.db.close()

@view_config(route_name = 'new', renderer = 'new.mako')
def new_view(request):
	if request.method == 'POST':
		if  request.POST.get('mailid'):
			request.db.execute(
				"insert into details (mailid, name, phone) values(?,?,?)" ,
				[request.POST['mailid'], request.POST['name'], int(request.POST['phone']) ]
				)
			request.db.commit()
			request.session.flash('New Person was Successfully added')
			return HTTPFound(location = request.route_url('list'))
		else:
			request.session.flash('Please enter a mailid for the record')
	return {}


@view_config(route_name = 'list', renderer = 'list.mako')
def list_view(request):
	rs = request.db.execute("select * from details;")
	details = [dict(id = row[0], mailid = row[1], name = row[2], phone = row[3]) for row in rs.fetchall()]
	#return {'details': details}
	return {'details': json.dumps(details)}

@view_config(route_name = 'delete')
def delete_view(request):
	detail_id = int(request.matchdict['id'])
	request.db.execute(
		"delete from details where id = ?",
		(detail_id,)
		)
	request.db.commit()
	return HTTPFound(location= request.route_url('list'))

@view_config(context = 'pyramid.exceptions.NotFound', renderer = 'notfound.mako')
def notfound_view(request):
	request.response.status = '404 Not Found'


if __name__ == '__main__':
	settings = {}
	settings['reload_all'] = True
	settings['debug_all'] = True
	settings['db'] = os.path.join(here, 'details.db')
	settings['mako.directories'] = os.path.join(here, 'templates')
	session_factory = UnencryptedCookieSessionFactoryConfig('itsaseekreet')
	# configuration setup
	config = Configurator(settings=settings, session_factory=session_factory)
	config.scan()
	config.include('pyramid_mako')
	config.add_static_view('static', os.path.join(here, 'static'))
	#ROUTES setup
	config.add_route('new','/new')
	config.add_route('list', '/')
	config.add_route('delete', '/delete/{id}')
	# serve app
	app = config.make_wsgi_app()
	server = make_server('0.0.0.0', 8080, app)
	server.serve_forever()