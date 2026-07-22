import os
import sys
import django
from django.conf import settings

# Add 'doctor' to sys.path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'doctor')))

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'doctor.settings')
django.setup()

from django.template.loader import get_template

templates_to_test = [
    'base.html',
    'docprofileinfo.html',
    'patientprofileinfo.html',
    'symptomsinfo.html',
    'diagnosisinfo.html',
    'prescriptioninfo.html',
    'paymentinfo.html',
    'feedbackinfo.html',
    'notificationinfo.html',
    'medicallhistoryinfo.html',
    'labtest.html',
    'labresultinfo.html',
    'login.html',
    'register.html'
]

for t_name in templates_to_test:
    try:
        print(f"Trying to load {t_name}...")
        t = get_template(t_name)
        print(f"  {t_name} loaded successfully!")
    except Exception as e:
        print(f"  Error loading {t_name}:")
        import traceback
        traceback.print_exc()
