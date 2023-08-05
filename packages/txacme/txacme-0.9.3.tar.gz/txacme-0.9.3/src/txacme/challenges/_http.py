"""
``http-01`` challenge implementation.
"""
from twisted.web.resource import Resource
from twisted.web.static import Data

from zope.interface import implementer

from txacme.interfaces import IResponder


@implementer(IResponder)
class HTTP01Responder(object):
    """
    An ``http-01`` challenge responder for txsni.
    """
    challenge_type = u'http-01'

    def __init__(self):
        self.resource = Resource()

    def start_responding(self, server_name, challenge, response):
        """
        Add the child resource.
        """
        self.resource.putChild(
            challenge.encode('token').encode('utf-8'),
            Data(response.key_authorization.encode('utf-8'), 'text/plain'))

    def stop_responding(self, server_name, challenge, response):
        """
        Remove the child resource.
        """
        encoded_token = challenge.encode('token').encode('utf-8')
        if self.resource.getStaticEntity(encoded_token) is not None:
            self.resource.delEntity(encoded_token)


__all__ = ['HTTP01Responder']
