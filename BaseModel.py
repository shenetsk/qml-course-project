import Base
from peewee import Model

class BaseModel(Model):
	class Meta:
		database = Base.db