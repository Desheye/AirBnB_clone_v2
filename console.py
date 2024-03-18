#!/usr/bin/python3

""" Console Module """
import cmd
import sys
from models.base_model import BaseModel
from models.__init__ import storage
from models.user import User
from models.place import Place
from models.state import State
from models.city import City
from models.amenity import Amenity
from models.review import Review


class HBNBCommand(cmd.Cmd):
    """ All the required functionality for the HBNB console"""

    """ Here is a prompt for both non-interactive/interactive modes """
    prompt = '(hbnb) ' if sys.__stdin__.isatty() else ''

    classes = {
        'Amenity': Amenity,
        'BaseModel': BaseModel,
        'City': City,
        'Place': Place,
        'Review': Review,
        'State': State,
        'User': User
    }
    dot_commands = ['all', 'count', 'show', 'destroy', 'update']
    types = {
        'number_rooms': int, 'number_bathrooms': int,
        'max_guest': int, 'price_by_night': int,
        'latitude': float, 'longitude': float
    }

    def preloop(self):
        """Prints if isatty is false"""
        if not sys.__stdin__.isatty():
            print('(hbnb)')

   def precmd(self, line):
        """Prepares the command line for advanced command syntax.

        Syntax: <class_name>.<command>([<id> [<*args> or <**kwargs>]])
        (Square brackets indicate optional fields in the syntax example.)
        """
    class_name = command = identifier = args = ''

    # Scan for general formatting - i.e., '.', '(', ')'
    if not ('.' in line and '(' in line and ')' in line):
        return line

    try:  # Parse line left to right
        parsed_line = line[:]  # Parsed line

        # Isolate <class_name>
        class_name = parsed_line[:parsed_line.find('.')]

        # Isolate and validate <command>
        command = parsed_line[parsed_line.find('.') + 1:parsed_line.find('(')]
        if command not in HBNBCommand.dot_commands:
            raise Exception

        # If parentheses contain arguments, parse them
        parsed_line = parsed_line[parsed_line.find('(') + 1:parsed_line.find(')')]
        if parsed_line:
            # Partition arguments: (<id>, [<delimiter>], [<*args>])
            # Parsed line converted to a tuple
            parsed_line = parsed_line.partition(', ')

            # Isolate identifier, stripping quotes
            identifier = parsed_line[0].replace('\"', '')
            # Possible bug here:
            # Empty quotes register as an empty identifier when
            # replaced

            # If arguments exist beyond the identifier
            # Parsed line is now a string
            parsed_line = parsed_line[2].strip()
            if parsed_line:
                # Check for *args or **kwargs
                if (parsed_line[0] == '{' and parsed_line[-1] == '}' and
                        isinstance(eval(parsed_line), dict)):

                    args = parsed_line
                else:
                    args = parsed_line.replace(',', '')
                    # args = args.replace('\"', '')
        line = ' '.join([command, class_name, identifier, args])

    except Exception as message:
        pass
    finally:
        return line



    def postcmd(self, stop, line):
        """Prints if isatty is false"""
        if not sys.__stdin__.isatty():
            print('(hbnb) ', end='')
        return stop

    def do_quit(self, command):
        """ Method to exit the HBNB console"""
        exit()

    def help_quit(self):
        """ Prints the help documentation for quit  """
        print("Exits the program with formatting\n")

    def do_EOF(self, arg):
        """ Handles EOF to exit program """
        print()
        exit()

    def emptyline(self):
        """ Overrides the emptyline method of CMD """
        pass

    def do_create(self, args):
        """Create an instance of any class."""
        try:
            if not args:
                raise SyntaxError()
            arg_list = args.split(" ")
            kwargs = {}
            for arg in arg_list[1:]:
                arg_split = arg.split("=")
                arg_split[1] = eval(arg_split[1])
                if isinstance(arg_split[1], str):
                    arg_split[1] = arg_split[1].replace(
                        "_", " ").replace('"', '\\"')
                kwargs[arg_split[0]] = arg_split[1]
        except SyntaxError:
            print("** class name missing **")
        except NameError:
            print("** class doesn't exist **")
        new_instance = HBNBCommand.classes[arg_list[0]](**kwargs)
        new_instance.save()
        print(new_instance.id)

    def help_create(self):
        """ Help information for the create method """
        print("Creates a class of any type")
        print("[Usage]: create <className>\n")

    def do_show(self, args):
        """Display information about a specific object."""
        try:
            class_name, _, obj_id = args.partition(" ")
            # Guard against trailing args
            if obj_id and ' ' in obj_id:
                obj_id = obj_id.partition(' ')[0]

            if not class_name:
                print("** class name missing **")
                return

            if class_name not in HBNBCommand.classes:
                print("** class doesn't exist **")
                return

            if not obj_id:
                print("** instance id missing **")
                return

            key = f"{class_name}.{obj_id}"
            try:
                print(storage._FileStorage__objects[key])
            except KeyError:
                print("** no instance found **")

        except Exception as e:
            print(f"An error occurred: {e}")

    def help_show(self):
        """ Help information for the show command """
        print("Shows an individual instance of a class")
        print("[Usage]: show <className> <objectId>\n")

    def do_destroy(self, args):
        """Delete a specified object."""
        try:
            class_name, _, obj_id = args.partition(" ")
            # Guard against trailing args
            if obj_id and ' ' in obj_id:
                obj_id = obj_id.partition(' ')[0]

            if not class_name:
                print("** class name missing **")
                return

            if class_name not in HBNBCommand.classes:
                print("** class doesn't exist **")
                return

            if not obj_id:
                print("** instance id missing **")
                return

            key = f"{class_name}.{obj_id}"

            try:
                del storage.all()[key]
                storage.save()
            except KeyError:
                print("** no instance found **")

        except Exception as e:
            print(f"An error occurred: {e}")

    def help_destroy(self):
        """ Help information for the destroy command """
        print("Destroys an individual instance of a class")
        print("[Usage]: destroy <className> <objectId>\n")

    def do_all(self, args):
        """Show all objects, or all objects of a specified class."""
        print_list = []

        if args:
            # Remove possible trailing args
            class_name = args.split(' ')[0]
            if class_name not in HBNBCommand.classes:
                print("** class doesn't exist **")
                return
            class_objects = storage.all(HBNBCommand.classes[class_name])
        for key, value in class_objects.items():

            print_list.append(str(value))
        else:
            for key, value in storage.all().items():
                print_list.append(str(value))
                print(print_list)

    def help_all(self):
        """ Help information for the all command """
        print("Shows all objects, or all of a class")
        print("[Usage]: all <className>\n")

    def do_count(self, args):
        """Count current number of class instances"""
        count = 0
        for k, v in storage._FileStorage__objects.items():
            if args == k.split('.')[0]:
                count += 1
        print(count)

    def help_count(self):
        """ """
        print("Usage: count <class_name>")

    def do_update(self, args):
        """Update attributes of a specific object."""
        class_name = obj_id = attr_name = attr_value = kwargs = ''

        # Isolate class name from id/args, e.g., (<class>, delimiter, <id/args>)
        args = args.partition(" ")
        if args[0]:
            class_name = args[0]
        else:  # Class name not provided
            print("** class name missing **")
            return
        if class_name not in HBNBCommand.classes:  # Class name invalid
            print("** class doesn't exist **")
            return

        # Isolate id from args
        args = args[2].partition(" ")
        if args[0]:
            obj_id = args[0]
        else:  # Id not provided
            print("** instance id missing **")
            return

        # Generate key from class and id
        key = class_name + "." + obj_id

        # Determine if key is present
        if key not in storage.all():
            print("** no instance found **")
            return

        # First determine if kwargs or args
        if '{' in args[2] and '}' in args[2] and isinstance(eval(args[2]), dict):
            kwargs = eval(args[2])
            args = []  # Reformat kwargs into list, e.g., [<name>, <value>, ...]
            for k, v in kwargs.items():
                args.append(k)
                args.append(v)
        else:  # Isolate args
            args = args[2]
            if args and args[0] == '\"':  # Check for quoted arg
                second_quote = args.find('\"', 1)
                attr_name = args[1:second_quote]
                args = args[second_quote + 1:]

            args = args.partition(' ')

            # If attr_name was not quoted arg
            if not attr_name and args[0] != ' ':
                attr_name = args[0]
            # Check for quoted val arg
            if args[2] and args[2][0] == '\"':
                attr_value = args[2][1:args[2].find('\"', 1)]

            # If attr_value was not quoted arg
            if not attr_value and args[2]:
                attr_value = args[2].partition(' ')[0]

            args = [attr_name, attr_value]

        # Retrieve dictionary of current objects
        new_dict = storage.all()[key]

        # Iterate through attr names and values
        for i, attr_name in enumerate(args):
            # Block only runs on even iterations
            if i % 2 == 0:
                attr_value = args[i + 1]  # Following item is value
                if not attr_name:  # Check for attr_name
                    print("** attribute name missing **")
                    return
                if not attr_value:  # Check for attr_value
                    print("** value missing **")
                    return
                # Type cast as necessary
                if attr_name in HBNBCommand.types:
                    attr_value = HBNBCommand.types[attr_name](attr_value)

                # Update dictionary with name, value pair
                new_dict.__dict__.update({attr_name: attr_value})

        new_dict.save()  # Save updates to file

    def help_update(self):
        """ Help information for the update class """
        print("Updates an object with new information")
        print("Usage: update <className> <id> <attName> <attVal>\n")


if __name__ == "__main__":
    HBNBCommand().cmdloop()
