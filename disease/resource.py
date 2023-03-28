from import_export import resources
from .models import Disease
class DiseaseResource(resources.ModelResource):
    class meta:
        model=Disease