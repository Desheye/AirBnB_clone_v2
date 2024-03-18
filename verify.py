#!/usr/bin/python3
import os

# Set the environment variables
os.environ["HBNB_MYSQL_USER"] = "hbnb_dev"
os.environ["HBNB_MYSQL_PWD"] = "hbnb_dev_pwd"

# Print the values of the environment variables
print("HBNB_MYSQL_USER:", os.getenv("HBNB_MYSQL_USER"))
print("HBNB_MYSQL_PWD:", os.getenv("HBNB_MYSQL_PWD"))