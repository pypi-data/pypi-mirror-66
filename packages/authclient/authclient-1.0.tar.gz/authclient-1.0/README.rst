Simple authentication client
============================

Simple authentication client

Usage
-----

.. code-block:: python

    from authclient import AuthClient

    async def main(username, password):
        cli = AuthClient("service", "127.0.0.1", 443)
        await cli.authenticate(username, password)
