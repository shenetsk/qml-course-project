from BaseModel import BaseModel
from peewee import IntegerField, CharField

class Favorites(BaseModel):
	user_id = IntegerField()
	path = CharField()