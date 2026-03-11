import pandas as pd
from django.core.management.base import BaseCommand
from registration.models import Hospital


class Command(BaseCommand):

    def handle(self, *args, **kwargs):

        df = pd.read_excel("hospitals.xlsx")

        for _, row in df.iterrows():

            Hospital.objects.update_or_create(

                email=row["email"],

                defaults={
                    "hospital_name": row["hospital_name"],
                    "hospital_id": row["hospital_id"],
                    "district": row["district"]
                }
            )

        print("Hospitals imported")