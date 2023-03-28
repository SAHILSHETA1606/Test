from .models import RefDoc
from import_export import resources
class refdocres(resources.ModelResource):
    class meta:
        model=RefDoc
