import json

class MessageContext:
    """Keeps track of all the message types.

    To add a class to this context, use ``add(cls)``.

    To parse a message, use ``parse_json(data)``.
    """
    def __init__(self):
        # Dictionary mapping type name -> message class
        self.message_types = {}

    def add(self, cls):
        """Register a message class with this context, so it will be
        recognized by the parser.

        This is supposed to be used as a class decorator. Example::

            context = MessageContext()

            @context.add
            class Status(Message):
                # ... code ...
        """

        # Add the class to the message dictionary
        if cls.__name__ in self.message_types:
            raise ValueError('name %s already exists' % cls.__name__)
        else:
            self.message_types[cls.__name__] = cls

        # Return the class, so we can use this method as a decorator
        return cls

    def parse_dict(self, data):
        """Load a message from a dictionary of attributes."""
        name = data.pop('__name__')
        cls = self.message_types[name]
        return cls._from_dict(data)

    def parse_json(self, s):
        """Load a message from a JSON string."""
        return self.parse_dict(json.loads(s))

    def unparse_dict(self, msg):
        """Convert a message to a dictionary of attributes."""
        return msg._to_dict()

    def unparse_json(self, msg):
        """Convert a message to a JSON string."""
        return json.dumps(self.unparse_dict(msg))