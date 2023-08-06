Kigo asynchronous event framework
=================================

.. image:: https://travis-ci.org/AsyncMicroStack/kigo.svg?branch=master
   :target: http://travis-ci.org/AsyncMicroStack/kigo

.. pull-quote ::
   Asynchronous and high performance event microservices framework for Python that lets service developers concentrate on application and testability.

.. code-block:: python

    # helloworld.py

    from kigo.rpc import Consumer, rpc

    @Consumer()
    class EchoService:

        @rpc
        def echo(self, say):
            return "Hello, {}!".format(say)

    if __name__ == '__main__':
        service = EchoService()
        service.run()


Documentation
-------------

Documentation and links to additional resources are available at
https://www.asyncstack.org/kigo


License
-------

Apache 2.0. See LICENSE for details.