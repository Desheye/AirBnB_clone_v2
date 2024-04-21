from sqlalchemy import Column, String
from sqlalchemy.orm import relationship
from models.base_model import BaseModel, Base
import shlex


class State(BaseModel, Base):
    """Represents a state in the database."""

    __tablename__ = "states"
    name = Column(String(128), nullable=False)
    cities = relationship(
        "City", cascade="all, delete, delete-orphan", backref="state")

    @property
    def get_cities(self):
        """Gets the list of cities associated with this state."""
        import models  # Import placed here
        var = models.storage.all()
        lista = []
        result = []
        for key in var:
            city = key.replace(".", " ")
            city = shlex.split(city)
            if city[0] == "City":
                lista.append(var[key])
        for elem in lista:
            if elem.state_id == self.id:
                result.append(elem)
        return result

    # Public getter method for cities, if storage engine is not DBStorage
    if __name__ != 'DBStorage':
        @property
        def cities(self):
            """Gets the list of cities associated with this state."""
            import models  # Import placed here
            return [city for city in models.storage.all('City').values() if city.state_id == self.id]
