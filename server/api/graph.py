from api import base


class Graph(base.ApiResource):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def post(self):
        pass
        # here goes the method