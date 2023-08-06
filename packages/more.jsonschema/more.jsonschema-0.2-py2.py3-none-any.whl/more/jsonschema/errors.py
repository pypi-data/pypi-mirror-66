class ValidationError(Exception):
    def __init__(self, errors):
        super().__init__("Jsonschema validation error")
        self.errors = errors
