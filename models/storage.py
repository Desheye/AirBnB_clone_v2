from models import storage

# Assuming 'State' is a model representing states in your application
from models.state import State

# Initialize the storage mechanism
storage.reload()

# Now you can use 'storage' to access data, such as getting all State objects
states = storage.all(State)

# Get the number of State objects
num_states = len(states)
print(num_states)
