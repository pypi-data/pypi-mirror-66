more.jsonschema: JSON Schema support for Morepath
=================================================

This package provides Morepath integration for `JSON Schema`_,
implemented with jsonschema_:

.. _JSON Schema: http://json-schema.org
.. _jsonschema: https://python-jsonschema.readthedocs.io/en/latest

JSON Schema can automate user input validation in a HTTP API.


Schema
------

The JSON schema need to be load into a Python dict
(you can use ``json.load()``):

.. code-block:: python

  user_schema = {
      'type': 'object',
      'properties': {
          'name': {
              'type': 'string',
              'minLength': 3
          },
          'age': {
              'type': 'integer',
              'minimum': 10
          }
      },
      'required': ['name', 'age']
  }

If you want to define JSON schemas in Python, you can use jsl_ for instance.

.. _jsl: http://jsl.readthedocs.io/en/latest


Validate
--------

The ``more.jsonschema`` integration helps
with validation of the request body as it is POSTed to a view.
First we must create a loader for our schema:

.. code-block:: python

  from more.jsonschema import loader

  user_schema_load = loader(user_schema)

We can use this loader to handle a POST request for instance:

.. code-block:: python

  @App.json(model=User, request_method='POST', load=user_schema_load)
  def user_post(self, request, json):
      # json is now a validated and normalized dict of whatever got
      # POST onto this view that you can use to update
      # self


Customize the Validator
-----------------------

By default ``more.jsonschema`` uses the ``Draft7Validator``.
But you can also use ``Draft3Validator``, ``Draft4Validator`` or ``Draft6Validator``.
You can even create your own Validator or extend an existent one.
Just pass the Validator to the ``loader``:

.. code-block:: python

  from jsonschema import Draft4Validator
  from more.jsonschema import loader

    user_schema_load = loader(user_schema, validator=Draft4Validator)

More information about creating or extending Validator classes
you can find in the `jsonschema documentation`_.

.. _jsonschema documentation:
  https://python-jsonschema.readthedocs.io/en/latest/creating


Error handling
--------------

If validation fails due to a validation error (a required field is
missing, or a field is of the wrong datatype, for instance), you want
to show some kind of error message. The ``load`` function created by
``more.jsonschema`` raise the ``more.jsonschema.ValidationError`` exception
in case of errors.

This exception object has an ``errors`` attribute with the validation errors.
You must define an exception view for it, otherwise validation errors are
returned as "500 internal server error" to API users.

This package provides a default exception view implementation. If you subclass
your application from ``more.jsonschema.JsonSchemaApp`` then you get a default
error view for ``ValidationError`` that has a 422 status code with an error
message:

.. code-block:: python

  from more.jsonschema import JsonSchemaApp

  class App(JsonSchemaApp):
      pass

Now your app has reasonable error handling built-in.
