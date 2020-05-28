import os

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'DjangoApp1.settings')
import django

django.setup()

import random
from first_app.models import Register
from faker import Faker

fakegen = Faker()


def populate(n=10):
    for i in range(n):
        fake_fname = fakegen.first_name()
        fake_lname = fakegen.last_name()
        fake_email = fakegen.ascii_safe_email()
        fake_pass = fakegen.lexify(text='??????????')
        user = Register.objects.get_or_create(first_name=fake_fname, last_name=fake_lname, email=fake_email,
                                              password=fake_pass)[0]


if __name__ == '__main__':
    print("Populating Data")
    populate(10)
    print("Populating complete")
