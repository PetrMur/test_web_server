from aiohttp.web import Request
from app.validator import Validator
from app.models.models import AbstractModel


class IncomingRequest:
    def __init__(self, request: Request, model_scheme: AbstractModel, need_validation: bool = True):
        self.request = request
        fields = request.query
        self.model = model_scheme.create_object(fields)
        self.fields = self.model.fields()

        if need_validation:
            Validator(self.fields).validate()
