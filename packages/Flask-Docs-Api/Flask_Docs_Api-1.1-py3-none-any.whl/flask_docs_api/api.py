import flask
from flask import jsonify

class Api():
    '''Flask-Docs-Api object. Needs a provided <code>app</code> and a provided <code>docRoute</code> for the location of the docs
    '''
    template = '''<!Doctype HTML><html><head><title>{{ name }} API Docs</title><link href="https://fonts.googleapis.com/css2?family=Roboto&display=swap" rel="stylesheet"><meta name="viewport" content="width=device-width, initial-scale=1.0"><style>body{font-family:'Roboto',sans-serif}code{background-color:#00181f88;color:white;border-radius:10%}#POST{background-color:#00729188;color:white}#GET{background-color:#198c1988;color:white}#DELETE{background-color:#a7004c88}#PUT{background-color:#5a1d5788;color:white}.route{margin:10px;margin-left:20%;margin-right:20%;padding:0.7%;border-radius:5px;box-shadow:10px 10px 51px -24px rgba(0,0,0,0.75)}h1{margin-left:20%;margin-right:20%}a:link{color:white;text-decoration:none}a:visited{color:white;text-decoration:none}a:hover{color:white;text-decoration:none}a:active{color:white;text-decoration:none}</style></head><body><h1>{{ name }} API Docs</h1> {% for route in routes %} {% for method in route['methods'] %}<div class="route" id="{{method}}"><h3> <a href="{{route['url']}}">{{ route['url'] }}</a> <code id="{{method}}">{{method}}</code></h3><p> {{ route['doc']|e }}</p></div> {% endfor %} {% endfor %}</body></html>'''
    def __init__(self, app:flask.Flask, apiName="", template="", docRoute="" ):
        self.app = app
        #self.globalls = app.__globals__
        self.apiName = apiName
        if template != "":
            self.template == template
        if docRoute != "":
            self.app.add_url_rule(docRoute, '__createDocs', self.__createDocs, methods=['GET'], provide_automatic_options=True)

    def __createDocs(self):
        '''Gives the api a documentation interface
        '''
        globe = {}
        for (a, b) in self.app.view_functions.items():
            globe[a] = b.__doc__
        routes = []
        for rule in self.app.url_map.iter_rules():
            if rule.endpoint not in ['static', '__createDocs']:
                methods = []
                for method in rule.methods:
                    if not str(method) == 'HEAD' and not str(method) == 'OPTIONS':
                        methods.append(str(method))
                routes.append({'doc': globe[rule.endpoint], 'url': str(rule), 'methods':  methods})
        return flask.render_template_string(self.template, routes=routes, name=self.apiName)
    
    def route(self, url: str):
        self.app.add_url_rule(url, '__createDocs', self.__createDocs, methods=['GET'], provide_automatic_options=True)