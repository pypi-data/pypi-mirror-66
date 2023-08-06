class Params(object):
    """ Params object """

    def __init__(self):
        self._params = set()
        self._undefined_params = set()

    @property
    def params(self) -> set:
        return self._params

    @property
    def defined_params(self) -> set:
        return self._params ^ self._undefined_params

    @property
    def undefined_params(self) -> set:
        return self._undefined_params

    def add_param(self, name: str):
        self._params.add(name)

    def add_undefined_param(self, name: str):
        self._undefined_params.add(name)

    def to_dict(self):
        """ Returns a dict of params """

        resp = {}
        for param in self._params:
            resp[param] = getattr(self, param)

        return resp
