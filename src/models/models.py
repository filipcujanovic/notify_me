from src.models import loader 
from orator.orm import belongs_to, has_many
from orator import Model


class Bus(Model):
    __table__ = 'busses'

    @has_many('bus_id')
    def bus_route(self):
        return BusRoute

    @has_many('bus_id', 'id')
    def users(self):
        return UserBusses

class BusRoute(Model):
    __table__ = 'current_busses_route_changes'

    @belongs_to('bus_id')
    def bus(self):
        return Bus

class User(Model):
    __table__ = 'auth_user'

    @has_many('user_id', 'id')
    def busses(self):
        return UserBusses


class UserBusses(Model):
    __table__ = 'busses_users'

    @belongs_to('user_id')
    def user(self):
        return User
        
    @belongs_to('bus_id')
    def bus(self):
        return Bus


class Municipality(Model):
    __table__ = 'municipalities'

    @has_many('municipalitiy_id', 'id')
    def users(self):
        return UserMunicipality


class UserMunicipality(Model):
    __table__ = 'municipalities_users'

    @belongs_to('user_id')
    def user(self):
        return User
        
    @belongs_to('municipalitiy_id')
    def bus(self):
        return Municipality