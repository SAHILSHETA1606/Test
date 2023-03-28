from import_export import resources
from .models import Symptoms
class SymptomsResource(resources.ModelResource):
    class meta:
        model=Symptoms