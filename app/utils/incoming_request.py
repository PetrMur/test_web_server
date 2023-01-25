from datetime import datetime
from app.validator import Validator


class IncomingRequest:
    def __init__(self, body, model_scheme, need_validation: bool = True):
        self.body = body
        self.model = model_scheme.create_object(body)
        self.fields = self.model.get_fields

        if need_validation:
            Validator(self.fields, self.model.get_required).validate()
