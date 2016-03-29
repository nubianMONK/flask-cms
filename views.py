from models import Page, Author, app
from flask.views import MethodView
from flask import render_template

class ResourceView(MethodView):

    __model__ = None

    def get(self, id):
        resource = self.__model__.query.get(id)
        return render_template('show_resource.html', resource)

class PageView(ResourceView):
    __model__ = Page

class AuthorView(ResourceView):
    __model__ = Author

def register_api(view, endpoint, url, pk='id', pk_type='int'):
    view_func = view.as_view(endpoint)
    app.add_url_rule(url, defaults={pk: None},
                     view_func=view_func, methods=['GET',])
    app.add_url_rule(url, view_func=view_func, methods=['POST',])
    app.add_url_rule('%s<%s:%s>' % (url, pk_type, pk), view_func=view_func,
                     methods=['GET', 'PUT', 'DELETE'])

register_api(PageView, 'page_view', '/page/', pk='id')
register_api(AuthorView, 'author_view', '/author/', pk='id')
