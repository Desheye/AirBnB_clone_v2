#!/usr/bin/python3
""" Console Module """
import cmd
import sys
from models.base_model import BaseModel
from models.__init__ import storage
from models.amenity import Amenity
from models.state import State
from models.review import Review
from models.user import User
from models.city import City
from models.place import Place


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

    dot_cmds = ['all', 'count', 'destroy', 'show', 'update']

    types = {
        'latitude': float,
        'longitude': float,
        'max_guest': int,
        'number_bathrooms': int,
        'number_rooms': int,
        'price_by_night': int
    }

    def preloop(self):
        """Prints if isatty is false"""
        if not sys.__stdin__.isatty():
            print('(hbnb)')

    def precmd(self, line):
        """Reformat command line for enhanced command syntax.

        New syntax: <command> <class_name> [<id> [<*args> or <**kwargs>]]
        (Square brackets indicate optional fields.)
        """
        _args = _class = _cmd = _id = ''  # initialize line elements

        # Check for general formatting indicators: '.', '(', ')'
        if not ('.' in line and '(' in line and ')' in line):
            return line

        try:  # Parse line from left to right
            parsed_line = line[:]  # Parsed line

            # Isolate <command>
            _cmd = parsed_line[parsed_line.find('.') + 1:parsed_line.find('(')]
            if _cmd not in HBNBCommand.dot_cmds:
                raise Exception

            # Isolate and validate <class_name>
            _class = parsed_line[:parsed_line.find('.')]

            # Check for arguments within parentheses
            parsed_line = parsed_line[parsed_line.find(
                '(') + 1:parsed_line.find(')')]
            if parsed_line:
                # Partition arguments: (<id>, [<delim>], [<*args>])
                parsed_line = parsed_line.partition(', ')  # Converted to tuple

                # Isolate _id, removing quotes
                _id = parsed_line[0].replace('\"', '')

                # If arguments exist beyond _id
                parsed_line = parsed_line[2].strip()  # Converted to string
                if parsed_line:
                    # Check for *args or **kwargs
                    if parsed_line[0] == '{' and parsed_line[-1] == '}'\
                            and type(eval(parsed_line)) is dict:
                        _args = parsed_line
                    else:
                        _args = parsed_line.replace(',', '')
                        # _args = _args.replace('\"', '')
            line = ' '.join([_cmd, _class, _id, _args])

        except Exception:
            pass
        finally:
            return line

    def postcmd(self, stop, line):
        """Prints if isatty is false"""
        if not sys.__stdin__.isatty():
            print('(hbnb) ', end='')
            return stop

    def do_quit(self, command):
        """Exit the HBNB console."""

    def help_quit(self):
        """Display help documentation for the quit command."""
        print("Exits the program with formatting.\n")

    def do_EOF(self, arg):
        """Handle EOF to exit the program."""
        print()
        exit()

    def help_EOF(self):
        """Display help documentation for EOF."""
        print("Exits the program without formatting.\n")

    def do_create(self, arguments):
        """ Create an instance of any class"""
        try:
            if not arguments:
                raise SyntaxError()
            arg_list = arguments.split(" ")
            kw = {}
            for arg in arg_list[1:]:
                arg_split = arg.split("=")
                arg_split[1] = eval(arg_split[1])
                if type(arg_split[1]) is str:
                    arg_split[1] = arg_split[1].replace(
                        "_", " ").replace('"', '\\"')
                kw[arg_split[0]] = arg_split[1]
        except SyntaxError:
            print("** Missing Class Name **")
        except NameError:
            print("** Class Does Not Exist **")
        new_instance = HBNBCommand.classes[arg_list[0]](**kw)
        new_instance.save()
        print("Instance {} created.".format(new_instance.id))

    def emptyline(self):
        """Override the emptyline method of CMD."""
        pass

    def help_create(self):
        """Display help information for the create command."""
        print("Creates an instance of a specified class.")
        print("[Usage]: create <className>\n")

    def do_show(self, arguments):
        """Display information about an individual object."""
        new = arguments.partition(" ")
        class_name = new[0]
        class_id = new[2]

        # Prevent any additional arguments beyond the expected input
        if class_id and ' ' in class_id:
            class_id = class_id.partition(' ')[0]

        if not class_name:
            print("** class name missing **")
            return

        if class_name not in HBNBCommand.classes:
            print("** class doesn't exist **")
            return

        if not class_id:
            print("** instance id missing **")
            return

        key = class_name + "." + class_id
        try:
            print(storage._objects[key])
        except KeyError:
            print("** instance is not found **")


def help_show(self):
    """ Show command Help Info """
    print("Shows an individual instance of a class")
    print("[Usage]: show <className> <objectId>\n")

    def help_show(self):
        """ Show command Help Info """
        print("Shows an individual instance of a class")
        print("[Usage]: show <className> <objectId>\n")

    def do_destroy(self, arguments):
        """Destroy a specified object."""
        new = arguments.partition(" ")
        class_name = new[0]
        class_id = new[2]
        if class_id and ' ' in class_id:
            class_id = class_id.partition(' ')[0]

        if not class_name:
            print("** Missing class name **")
            return

        if class_name not in HBNBCommand.classes:
            print("** Class doesn't exist **")
            return

        if not class_id:
            print("** Missing instance id **")
            return

        key = class_name + "." + class_id
        try:
            del (storage.all()[key])
            storage.save()
        except KeyError:
            print("** Instance Not Found **")

    def help_destroy(self):
        """ (Help info) For The Destroy Command """
        print("Destroys an instance of a class")
        print("[Usage]: destroy <className> <objectId>\n")

    def do_all(self, arguments):
        """ Display all objects, or all objects of a specified class."""
        print_list = []

        if arguments:
            # Remove possible trailing args
            class_name = arguments.split(' ')[0]
            if class_name not in self.classes:
                print("** class doesn't exist **")
                return
            # Access classes member using self
            instances = storage.all(self.classes[class_name])
            for instance in instances.values():
                print_list.append(str(instance))
        else:
            instances = storage.all()
            for instance in instances.values():
                print_list.append(str(instance))
            print(print_list)

    def help_all(self):
        """ Help information for the all command """
        print("Shows all objects, or all of a class")
        print("[Usage]: all <className>\n")

    def do_count(self, arguments):
        """Display the current number of instances for a specified class."""
        instance_count = 0
        for key, value in storage._objects.items():
            if arguments == key.split('.')[0]:
                instance_count += 1
        print(instance_count)

    def help_count(self):
        """ """
        print("Usage: count <class_name>")

    def do_update(self, arguments):
        """Update attributes of a specified object."""
        class_name = object_id = attribute_name = attribute_value = kwargs = ''

        # Extract class name and object id/arguments
        args = arguments.partition(" ")
        if args[0]:
            class_name = args[0]
        else:
            print("** Missing class name **")
            return
        if class_name not in HBNBCommand.classes:
            print("** Class doesn't exist **")
            return

        args = args[2].partition(" ")
        if args[0]:
            object_id = args[0]
        else:
            print("** Missing instance id **")
            return

        key = class_name + "." + object_id

        if key not in storage.all():
            print("** No instance found **")
            return

        # Determine if keyword arguments or positional arguments
        if '{' in args[2] and '}' in args[2] and type(eval(args[2])) is dict:
            kwargs = eval(args[2])
            args = []
            for k, v in kwargs.items():
                args.append(k)
                args.append(v)
        else:
            args = args[2]
            if args and args[0] == '\"':
                second_quote = args.find('\"', 1)
                attribute_name = args[1:second_quote]
                args = args[second_quote + 1:]

            args = args.partition(' ')

            if not attribute_name and args[0] != ' ':
                attribute_name = args[0]

            if args[2] and args[2][0] == '\"':
                attribute_value = args[2][1:args[2].find('\"', 1)]

            if not attribute_value and args[2]:
                attribute_value = args[2].partition(' ')[0]

            args = [attribute_name, attribute_value]

        new_dict = storage.all()[key]

        # Iterate through attribute names and values
        for i, attribute_name in enumerate(args):
            if (i % 2 == 0):
                attribute_value = args[i + 1]
                if not attribute_name:
                    print("** Attribute name missing **")
                    return
                if not attribute_value:
                    print("** Value missing **")
                    return

                if attribute_name in HBNBCommand.types:
                    attribute_value = HBNBCommand.types[attribute_name](
                        attribute_value)

                new_dict.__dict__.update({attribute_name: attribute_value})

        new_dict.save()

    def help_update(self):
        """ Help information for the update class """
        print("Updates object with new info")
        print("Usage: update <className> <id> <attName> <attVal>\n")


if __name__ == "__main__":
    HBNBCommand().cmdloop()
