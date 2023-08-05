"""All Inventory methods are housed here"""
from tuneuptechnology.client import Client

class Inventory(Client):
    """Inventory methods"""
    @classmethod
    def create(cls, data):
        """Create an inventory item based on the data passed"""
        endpoint = f'{Client.API_BASE_URL}inventory/create'
        response = Client.response(data, endpoint)
        return response.json()

    @classmethod
    def all(cls, data):
        """Retrieve all inventory"""
        endpoint = f'{Client.API_BASE_URL}inventorys'
        response = Client.response(data, endpoint)
        return response.json()

    @classmethod
    def retrieve(cls, data):
        """Retrieve a single inventory item"""
        endpoint = f'{Client.API_BASE_URL}inventory/{data["id"]}'
        response = Client.response(data, endpoint)
        return response.json()

    @classmethod
    def update(cls, data):
        """Update an inventory item with the passed params"""
        endpoint = f'{Client.API_BASE_URL}inventory/{data["id"]}/update'
        response = Client.response(data, endpoint)
        return response.json()

    @classmethod
    def delete(cls, data):
        """Delete an inventory item with the ID passed"""
        endpoint = f'{Client.API_BASE_URL}inventory/{data["id"]}/delete'
        response = Client.response(data, endpoint)
        return response.json()
