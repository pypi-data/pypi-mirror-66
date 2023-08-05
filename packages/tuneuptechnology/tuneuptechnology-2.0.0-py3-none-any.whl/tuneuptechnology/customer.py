"""All Customer methods are housed here"""
from tuneuptechnology.client import Client

class Customer(Client):
    """Customer methods"""
    @classmethod
    def create(cls, data):
        """Create a customer based on the data passed"""
        endpoint = f'{Client.API_BASE_URL}customers/create'
        response = Client.response(data, endpoint)
        return response.json()

    @classmethod
    def all(cls, data):
        """Retrieve all customers"""
        endpoint = f'{Client.API_BASE_URL}customers'
        response = Client.response(data, endpoint)
        return response.json()

    @classmethod
    def retrieve(cls, data):
        """Retrieve a single customer"""
        endpoint = f'{Client.API_BASE_URL}customers/{data["id"]}'
        response = Client.response(data, endpoint)
        return response.json()

    @classmethod
    def update(cls, data):
        """Update a customer with the passed params"""
        endpoint = f'{Client.API_BASE_URL}customers/{data["id"]}/update'
        response = Client.response(data, endpoint)
        return response.json()

    @classmethod
    def delete(cls, data):
        """Delete a customer with the ID passed"""
        endpoint = f'{Client.API_BASE_URL}customers/{data["id"]}/delete'
        response = Client.response(data, endpoint)
        return response.json()
