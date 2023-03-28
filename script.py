import csv
import os
PROJECT_NAME='clinicsoftware'
def backup():
    from django.apps import apps
    model_list = apps.get_models()
    model_name_list = [model.__name__ for model in model_list]

    for model in model_list:
        all_fields=model._meta.get_fields()
        columns=[x.name for x in all_fields]

        if not os.path.exists('csvs'):
            os.makedirs('csvs')

        with open(f'csvs/{model.__name__}.csv','w') as csv_file:
            writer=csv.writer(csv_file,delimiter=',',quotechar='"',quoting=csv.QUOTE_MINIMAL)
            writer.writerow(columns)
            objects=model.objects.all()

            for obj in objects:
                row=[str(getattr(obj,column,"NA")) for column in columns]
                writer.writerow(row)

if __name__=='__main__':
    os.environ.setdefault('DJANGO_SETTINGS_MODULE',PROJECT_NAME+'.settings')
    import django
    django.setup()
    backup()