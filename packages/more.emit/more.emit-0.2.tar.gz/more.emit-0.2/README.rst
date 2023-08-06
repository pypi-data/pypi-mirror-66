more.emit: pymitter integration in Morepath
===============================================

This package provides Morepath integration for pymitter_.

*pymitter* is a Python port of the extended Node.js `EventEmitter 2`_
approach providing namespaces, wildcards and TTL.


Quick start
-----------

Install ``more.emit``:

.. code-block:: console

  $ pip install -U more.emit

Extend your App class from EmitApp:

.. code-block:: python

    from more.pony import EmitApp

    class App(EmitApp):
        pass

Now you can define signals:

.. code-block:: python

  from .app import App


  @App.signal.on('myevent')
  def handler1(arg, request):
      print(request)
      print('handler1 called with', arg)

  @App.signal.on('myevent')
  def handler2(arg, request):
      print('handler2 called with', arg)

You can emit the signals for example from the view:

.. code-block:: python

  @App.json(model=Root)
  def root_view(self, request):
      request.app.signal.emit('myevent', 'foo', request)
      return {
          'name': 'Root'
      }


Example
-------

An example for emitting signals on user creation
and user update for sending a confirmation email.
This example uses `more.pony`_.

signal.py

.. code-block:: python

  from .app import App


  @App.signal.on('user.email_updated')
  def send_confirmation_email(user, request):
      mailer = request.app.service(name='mailer')
      mailer.send_confirmation_email(user, request)

view.py

.. code-block:: python

  @App.json(model=UserCollection, request_method='POST')
  def user_collection_add(self, request):
      email = request.json['email']

      if not User.exists(email=email):
          user = self.add(email=email)

          @request.after
          def after(response):
              request.app.signal.emit('user.email_updated', user, request)
              response.status = 201

      else:
          @request.after
          def after(response):
              response.status = 409

          return {
              'validationError': 'Email already exists'
          }


  @App.json(model=User, request_method='PUT')
  def user_update(self, request):
      if 'email' in request.json and User.exists(email=request.json['email']):
          @request.after
          def after(response):
              response.status = 409

          return {
              'validationError': 'Email already exists'
          }

      else:
          self.update(request.json)
          if 'email' in request.json:
              self.email_confirmed = False

              @request.after
              def after(response):
                  request.app.signal.emit('user.email_updated', self, request)


.. _pymitter: https://github.com/riga/pymitter
.. _EventEmitter 2: https://github.com/asyncly/EventEmitter2
.. _more.pony: https://github.com/morepath/more.pony
