"""All Ticket methods are housed here"""
from tuneuptechnology.client import Client

class Ticket(Client):
    """Ticket methods"""
    @classmethod
    def create(cls, data):
        """Create a ticket based on the data passed"""
        endpoint = f'{Client.API_BASE_URL}tickets/create'
        response = Client.response(data, endpoint)
        return response.json()

    @classmethod
    def all(cls, data):
        """Retrieve all tickets"""
        endpoint = f'{Client.API_BASE_URL}tickets'
        response = Client.response(data, endpoint)
        return response.json()

    @classmethod
    def retrieve(cls, data):
        """Retrieve a single ticket"""
        endpoint = f'{Client.API_BASE_URL}tickets/{data["id"]}'
        response = Client.response(data, endpoint)
        return response.json()

    @classmethod
    def update(cls, data):
        """Update a ticket with the passed params"""
        endpoint = f'{Client.API_BASE_URL}tickets/{data["id"]}/update'
        response = Client.response(data, endpoint)
        return response.json()

    @classmethod
    def delete(cls, data):
        """Delete a ticket with the ID passed"""
        endpoint = f'{Client.API_BASE_URL}tickets/{data["id"]}/delete'
        response = Client.response(data, endpoint)
        return response.json()
