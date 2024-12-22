"""
WSGI config for askme_inyakin project.

It exposes the WSGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/5.1/howto/deployment/wsgi/
"""

import os

from django.core.wsgi import get_wsgi_application

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'askme_inyakin.settings')

application = get_wsgi_application()

def my_application(environ, start_response):
    method = environ['REQUEST_METHOD']
    path = environ['PATH_INFO']

    if method == "GET":
        print(f"GET request to {path}")
    elif method == "POST":
        print(f"POST request to {path}")
    return application(environ, start_response)

# def my_application(environ, start_response):
#     status = '200 OK'
#     output = b'<!DOCTYPE html><html><body><h1>Dynamic Test Page</h1></body></html>'
#     response_headers = [('Content-type', 'text/html'),
#                        ('Content-Length', str(len(output)))]
#     start_response(status, response_headers)
#     return [output]

