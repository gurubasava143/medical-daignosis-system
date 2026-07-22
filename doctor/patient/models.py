
from django.db import models

class userregistration(models.Model):
    name = models.CharField(max_length=40)
    email = models.CharField(max_length=40)
    password = models.CharField(max_length=40)
    contact = models.CharField(max_length=20)
    city = models.CharField(max_length=30)
    address = models.CharField(max_length=100)
    role = models.CharField(max_length=20)

# 1. User Login
class userlogin(models.Model):
    username = models.CharField(max_length=40)
    password = models.CharField(max_length=20)
    type = models.CharField(max_length=20)

# 2. Doctor Profile
class doctorprofile(models.Model):
    user = models.CharField(max_length=40)
    specialization = models.CharField(max_length=100)
    qualification = models.CharField(max_length=100)
    experience_years = models.CharField(max_length=10)
    hospital_name = models.CharField(max_length=100)
    consultation_fee = models.CharField(max_length=20)
    available_time = models.CharField(max_length=50)
    photo = models.FileField(upload_to='documents/', null=True, blank=True)

# 3. Patient Profile
class patientprofile(models.Model):
    user =models.CharField(max_length=40)
    age = models.CharField(max_length=5)
    gender = models.CharField(max_length=10)
    blood_group = models.CharField(max_length=10)
    weight = models.CharField(max_length=10)
    height = models.CharField(max_length=10)
    existing_conditions = models.CharField(max_length=200)
    allergies = models.CharField(max_length=200)

# 4. Symptom Record
class symptomrecord(models.Model):
    patient =models.CharField(max_length=40)
    symptom_name = models.CharField(max_length=100)
    severity = models.CharField(max_length=20)
    duration = models.CharField(max_length=30)
    body_part = models.CharField(max_length=50)
    recorded_date = models.CharField(max_length=25)
    description = models.CharField(max_length=200)

# 5. Diagnosis
class diagnosis(models.Model):
    diagnosis_id = models.CharField(max_length=50, blank=True, null=True)
    patient = models.CharField(max_length=40)
    doctor = models.CharField(max_length=40)
    diagnosis_date = models.CharField(max_length=25)
    condition_name = models.CharField(max_length=100)
    diagnosis_type = models.CharField(max_length=30)
    description = models.CharField(max_length=200)
    severity_level = models.CharField(max_length=20)
    follow_up_date = models.CharField(max_length=25)

# 6. Lab Test
class labtest(models.Model):
    patient = models.CharField(max_length=40)
    diagnosis =models.CharField(max_length=40)
    test_name = models.CharField(max_length=100)
    test_type = models.CharField(max_length=50)
    prescribed_by = models.CharField(max_length=40)
    test_date = models.CharField(max_length=25)
    status = models.CharField(max_length=20)
    cost = models.CharField(max_length=20)

# 7. Lab Result
class labresult(models.Model):
    lab_test = models.CharField(max_length=40)
    result_value = models.CharField(max_length=100)
    normal_range = models.CharField(max_length=50)
    result_status = models.CharField(max_length=20)
    report_date = models.CharField(max_length=25)
    technician_name = models.CharField(max_length=50)
    report_file = models.FileField(upload_to='documents/', null=True, blank=True)

# 8. Prescription
class prescription(models.Model):
    diagnosis = models.CharField(max_length=40)
    medicine_name = models.CharField(max_length=100)
    dosage = models.CharField(max_length=50)
    frequency = models.CharField(max_length=30)
    duration = models.CharField(max_length=30)
    instructions = models.CharField(max_length=200)
    prescribed_date = models.CharField(max_length=25)

# 9. Medical History
class medicalhistory(models.Model):
    patient = models.CharField(max_length=40)
    diagnosis = models.CharField(max_length=40)
    treatment_summary = models.CharField(max_length=200)
    outcome = models.CharField(max_length=50)
    date_recorded = models.CharField(max_length=25)
    notes = models.CharField(max_length=200)

# 10. Payment
class payment(models.Model):
    patient = models.CharField(max_length=40)
    diagnosis = models.CharField(max_length=40)
    lab_test =models.CharField(max_length=40)
    amount = models.CharField(max_length=20)
    payment_date = models.CharField(max_length=25)
    payment_method = models.CharField(max_length=20)
    transaction_id = models.CharField(max_length=100)
    status = models.CharField(max_length=20)

# 11. Feedback
class feedback(models.Model):
    patient = models.CharField(max_length=40)
    doctor = models.CharField(max_length=40)
    rating = models.CharField(max_length=10)
    comments = models.CharField(max_length=200)
    feedback_date = models.CharField(max_length=25)

# 12. Notification
class notification(models.Model):
    user =models.CharField(max_length=40)
    message = models.CharField(max_length=200)
    notification_type = models.CharField(max_length=50)
    is_read = models.CharField(max_length=10)
    created_date = models.CharField(max_length=25)


    