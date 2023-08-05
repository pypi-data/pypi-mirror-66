Sanic-jwt Payload Encryption plugin
===================================

This project is a plugin for great [Sanic-jwt](https://github.com/ahopkins/sanic-jwt) project, allowing encrypt the content of the Payload and include all the User data inside them.

Install
-------

.. code-block:: console

    > pip install sanic-jwt-payload-encrypt

How to use
----------

Sometimes you may want to hide payload content. So it should be useful if you could encrypt payload content. sanic-jwt-payload-encrypt provides Fernet encryption for the Payload. You must provide the encryption key (and optionally a salt value).

.. code-block:: python

    from sanic import Sanic
    from sanic_jwt import Initialize
    from sanic_jwt_payload_encrypt import AuthenticationEncrypted

    app = Sanic()
    app.config.ENCRYPT_PASSWORD = "ASDFAsdfkjalsdfjlkasdfjlkasdjflksaKSKSKS" # USE STRONG PASSWORD!!
    app.config.ENCRYPT_SALT = "ASDFAsdfkjalsdfjlkasdfjlkasdjflksa"  # This is optional But recommendable

    async def authenticate(request):
        return {"user_id": "my name"}


    Initialize(app,
               authenticate=authenticate,
               authentication_class=AuthenticationEncrypted)

Include all User info into encrypted Payload
--------------------------------------------

Once the Payload is encrypted you may want to include all the User information into Payload. You can do that by setting app config *FULL_USER_INFO*:

.. code-block:: python

    import uuid

    from sanic import Sanic
    from sanic_jwt import Initialize
    from sanic_jwt_payload_encrypt import AuthenticationEncrypted

    app = Sanic()
    app.config.ENCRYPT_PASSWORD = "ASDFAsdfkjalsdfjlkasdfjlkasdjflksaKSKSKS"
    app.config.ENCRYPT_SALT = "ASDFAsdfkjalsdfjlkasdfjlkasdjflksa"  # This is optional
    app.config.FULL_USER_INFO = True

    class User:

        def __init__(self, user_id: str, name: str):
            self.user_id = user_id
            self.name = name

        def to_dict(self):
            return self.__dict__


    async def authenticate(request):
        return User(user_id=uuid.uuid4().hex, name="custom name")

    async def retrieve_user(request, payload, *args, **kwargs):
        return User(**payload)

    Initialize(app,
               authenticate=authenticate,
               retrieve_user=retrieve_user,
               authentication_class=AuthenticationEncrypted)

Usage demo
----------

Get a new access token:

.. code-block:: console

    > curl -X POST http://localhost:8000/auth
    {"access_token":"eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.Z0FBQUFBQmVtRGdDQXNvSDJHaXl0Y0lMajlRWkJwT1hQUmdZQ2VJdF93d0wwZ1lWX3BWbmN6eU9IQWUzTDBFT2RvQXhLQ08tSk93d2ZYX0xmUy04M0ZjV1BWWDMxS201U2V5T09wYWVwN0MwVGE4bkF6d0duNkZTVlBzWmFYUXlfeldQSXlMcWdWUXdlcmNsT01VOF9IYWZVTF9nWmFzR2J4MDRNVUxsMll3SURGbkI2ZzNmejZFNDZXNzVCMUNNME1kRnNHY19kbXBBZnpWR0ZHYVdPR0E4elprem5jbmNlN01NMVFqdDBjUDBjeENaUy01ZmJyVT0.HuDaQ7xwFe4YjfYY40cSHnMzwJduMY9x8Lcoq9Y0Om0"}%

If token is not encrypted by using base65 decoder we'll read their content, but by using following example we'll see that we'll get an unreadable data from the payload.

.. code-block:: console
    > ENCRYPTED_PAYLOAD=Z0FBQUFBQmVtRGdDQXNvSDJHaXl0Y0lMajlRWkJwT1hQUmdZQ2VJdF93d0wwZ1lWX3BWbmN6eU9IQWUzTDBFT2RvQXhLQ08tSk93d2ZYX0xmUy04M0ZjV1BWWDMxS201U2V5T09wYWVwN0MwVGE4bkF6d0duNkZTVlBzWmFYUXlfeldQSXlMcWdWUXdlcmNsT01VOF9IYWZVTF9nWmFzR2J4MDRNVUxsMll3SURGbkI2ZzNmejZFNDZXNzVCMUNNME1kRnNHY19kbXBBZnpWR0ZHYVdPR0E4elprem5jbmNlN01NMVFqdDBjUDBjeENaUy01ZmJyVT0
    > echo $ENCRYPTED_PAYLOAD | base64 -Dd
    gAAAAABemDgCAsoH2GiytcILj9QZBpOXPRgYCeIt_wwL0gYV_pVnczyOHAe3L0EOdoAxKCO-JOwwfX_LfS-83FcWPVX31Km5SeyOOpaep7C0Ta8nAzwGn6FSVPsZaXQy_zWPIyLqgVQwerclOMU8_HafUL_gZasGbx04MULl2YwIDFnB6g3fz6E46W75B1CM0MdFsGc_dmpAfzVGFGaWOGA8zZkzncnce7MM1Qjt0cP0cxCZS-5fbr

Now checks if the endpoints returns correct information for the */auth/me* end-point:

.. code-block:: console

    > curl -X POST http://localhost:8000/auth
    {"access_token":"eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.Z0FBQUFBQmVtRGdDQXNvSDJHaXl0Y0lMajlRWkJwT1hQUmdZQ2VJdF93d0wwZ1lWX3BWbmN6eU9IQWUzTDBFT2RvQXhLQ08tSk93d2ZYX0xmUy04M0ZjV1BWWDMxS201U2V5T09wYWVwN0MwVGE4bkF6d0duNkZTVlBzWmFYUXlfeldQSXlMcWdWUXdlcmNsT01VOF9IYWZVTF9nWmFzR2J4MDRNVUxsMll3SURGbkI2ZzNmejZFNDZXNzVCMUNNME1kRnNHY19kbXBBZnpWR0ZHYVdPR0E4elprem5jbmNlN01NMVFqdDBjUDBjeENaUy01ZmJyVT0.HuDaQ7xwFe4YjfYY40cSHnMzwJduMY9x8Lcoq9Y0Om0"}%
    > TOKEN=eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.Z0FBQUFBQmVtRGdDQXNvSDJHaXl0Y0lMajlRWkJwT1hQUmdZQ2VJdF93d0wwZ1lWX3BWbmN6eU9IQWUzTDBFT2RvQXhLQ08tSk93d2ZYX0xmUy04M0ZjV1BWWDMxS201U2V5T09wYWVwN0MwVGE4bkF6d0duNkZTVlBzWmFYUXlfeldQSXlMcWdWUXdlcmNsT01VOF9IYWZVTF9nWmFzR2J4MDRNVUxsMll3SURGbkI2ZzNmejZFNDZXNzVCMUNNME1kRnNHY19kbXBBZnpWR0ZHYVdPR0E4elprem5jbmNlN01NMVFqdDBjUDBjeENaUy01ZmJyVT0.HuDaQ7xwFe4YjfYY40cSHnMzwJduMY9x8Lcoq9Y0Om0
    > curl -X GET -H "Authorization: Bearer $TOKEN" http://localhost:8000/auth/me
    {"me":{"user_id":"85bbf574f9c1469da89de82a934fec96","exp":1587035913,"name":"custom name"}}

Config variables
----------------

- ENCRYPT_PASSWORD: Password to use for encrypt the payload
- ENCRYPT_SALT: Salt used for crypt algorithm
- FULL_USER_INFO: Indicates if all User information must be included in the encrypted Payload

