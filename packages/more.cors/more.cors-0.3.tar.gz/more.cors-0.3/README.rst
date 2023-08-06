more.cors: CORS support for Morepath
====================================

This package adds CORS support to Morepath.


Quick start
-----------

Install ``more.cors``:

.. code-block:: console

    $ pip install -U more.cors

Extend your App class from CORSApp:

.. code-block:: python

    from more.cors import CORSApp


    class App(CORSApp):
        pass

This will add basic CORS support to your Morepath app.


Settings
--------

more.cors provides settings in the 'cors' section. Here are the defaults:

.. code-block:: python

    @App.setting_section(section='cors')
    def cors_settings():
        return {
            'allowed_verbs': ['GET', 'PUT', 'POST', 'PATCH', 'DELETE', 'OPTIONS'],
            'allowed_origin': '*',
            'expose_headers': ['Content-Type', 'Authorization'],
            'allowed_headers': ['Content-Type', 'Authorization'],
            'max_age': 60,
            'allow_credentials': False
        }

The following settings are available:

allowed_verbs
  A list of allowed HTTP request methods.

allowed_origin
  A URI that may access the resource.
  For requests **without credentials**, "*" can be used as a wildcard,
  allowing any origin to access the resource.

expose_headers
  A list of HTTP headers which can be exposed as part of the response.

allowed_headers
  A list of HTTP headers which can be used during the actual request.

max_age
  Maximum number of seconds the results of a preflight request can be cached.

allow_credentials
  Boolean which indicates whether or not the actual request can be made using
  credentials.
  Credentials are cookies, authorization headers or TLS client certificates.


Specify CORS settings for a single view
---------------------------------------

more.cors exposes the ``App.cors()`` class method.
This can be used to specify settings for a single view:

.. code-block:: python

    App.cors(
        model=Root,
        view_name='view2',
        allowed_headers=['Cache-Control'],
        expose_headers=['Cookie'],
        allowed_origin='http://foo.com',
        allow_credentials=True,
        max_age=10
    )

model
  Specifies the corresponding view model.

view_name
  Is needed when you use a named view.

allowed_headers, expose_headers, allowed_origin, allow_credentials, max_age
  The settings which can be specified. For details see Settings_.
