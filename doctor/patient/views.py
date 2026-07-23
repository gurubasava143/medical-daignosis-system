from django.shortcuts import render, redirect
from django.urls import reverse
from django.views.decorators.csrf import csrf_exempt

from patient.models import userregistration

from patient.models import symptomrecord

from patient.models import diagnosis

from patient.models import prescription

from patient.models import payment

from patient.models import patientprofile

from patient.models import notification

from patient.models import medicalhistory

from patient.models import labresult

from patient.models import labtest

from patient.models import feedback

from patient.models import doctorprofile

from patient.models import userlogin


# Create your views here.

@csrf_exempt
def logcheck(request):
    if request.method=="POST":
        username = request.POST.get('t1', '').strip()
        password = request.POST.get('t2', '').strip()
        count = userlogin.objects.filter(username=username).count()
        if count >= 1:
            udata = userlogin.objects.filter(username=username).first()
            request.session['username'] = username
            upass = udata.password.strip()
            utype = udata.type.strip().lower()
            
            if upass == password:
                request.session['utype'] = utype
                if utype == 'admin':
                    return redirect('admin_home')
                elif utype == 'doctor':
                    return redirect('doctor_home')
                elif utype == 'patient':
                    return redirect('patient_home')
                else:
                    return render(request, 'login.html', {'msg': f'Unauthorized role: {utype}'})
            else:
                return render(request, 'login.html', {'msg': 'Invalid password'})
        else:
            return render(request, 'login.html', {'msg': 'Invalid username (Email)'})

    return render(request,'login.html')

def admin_home(request):
    if request.session.get('utype') != 'admin':
        return redirect('logcheck')
    return render(request, 'admin_home.html')

def doctor_home(request):
    if request.session.get('utype') != 'doctor':
        return redirect('logcheck')
    profile_exists = doctorprofile.objects.filter(user=request.session.get('username')).exists()
    request.session['profile_exists'] = profile_exists
    return render(request, 'doctor_home.html')

def patient_home(request):
    if request.session.get('utype') != 'patient':
        return redirect('logcheck')
    profile_exists = patientprofile.objects.filter(user=request.session.get('username')).exists()
    request.session['profile_exists'] = profile_exists
    return render(request, 'patient_home.html')

def showindex(request):
    return render(request,'index.html',)

def logout(request):
    request.session.flush()
    return redirect('logcheck')

def insertuserreg(request):
    if request.method=="POST":
        import re
        s1 = request.POST.get("t1", "").strip() # name
        s2 = request.POST.get("t2", "").strip() # email
        s3 = request.POST.get("t3", "")          # password
        s4 = request.POST.get("t4", "").strip() # contact
        s5 = request.POST.get("t5", "").strip() # city
        s6 = request.POST.get("t6", "").strip() # address
        s7 = request.POST.get("t7", "").strip() # role

        errors = []
        if not re.match(r"^[a-zA-Z\s]{3,40}$", s1):
            errors.append("Full Name must contain only letters and spaces (min 3 chars).")
        if not re.match(r"^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$", s2):
            errors.append("A valid email address is required.")
        if not re.match(r"^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)(?=.*[@$!%*?&#])[A-Za-z\d@$!%*?&#]{8,}$", s3):
            errors.append("Password must be at least 8 characters and include uppercase, lowercase, a digit, and a special character.")
        if not re.match(r"^\d{10}$", s4):
            errors.append("Contact Number must be exactly 10 digits.")
        if not re.match(r"^[a-zA-Z\s]{2,30}$", s5):
            errors.append("City must contain only letters and spaces (min 2 chars).")
        if len(s6) < 10:
            errors.append("Address must be at least 10 characters long.")
        if s7 not in ['patient', 'doctor']:
            errors.append("Please select a valid role (patient or doctor).")

        if errors:
            return render(request, "register.html", {"msg": "Registration failed: " + " | ".join(errors)})

        # Check if email used 2 times
        email_count = userregistration.objects.filter(email=s2).count()
        if email_count >= 2:
            return render(request, "register.html", {"msg": "Registration failed! This Email already exists twice."})

        userregistration.objects.create(name=s1,email=s2,password=s3,contact=s4,city=s5,address=s6,role=s7)
        # Use email as username for login
        userlogin.objects.create(username=s2,password=s3,type=s7)
        return render(request,"register.html",{"msg":"Registration successful! You can now login."})
    return render(request,"register.html")

def forgot_password(request):
    step = request.POST.get('step', 'email')
    
    if request.method == "POST":
        import random
        if step == 'email':
            email = request.POST.get('t1', '').strip()
            user = userlogin.objects.filter(username=email).first()
            if user:
                # Generate 6-digit OTP
                otp = str(random.randint(100000, 999999))
                request.session['forgot_otp'] = otp
                request.session['forgot_email'] = email
                return render(request, "forgotpassword.html", {
                    "step": "otp",
                    "email": email,
                    "otp_code": otp,  # Pass for offline simulation / visibility
                    "msg": f"A 6-digit OTP code has been simulated and sent to your email. (Demo OTP: {otp})"
                })
            else:
                return render(request, "forgotpassword.html", {
                    "step": "email",
                    "msg": "Email not found. Please enter your registered email address."
                })
                
        elif step == 'otp':
            email = request.session.get('forgot_email')
            entered_otp = request.POST.get('t2', '').strip()
            session_otp = request.session.get('forgot_otp')
            
            if entered_otp == session_otp:
                return render(request, "forgotpassword.html", {
                    "step": "reset",
                    "email": email,
                    "msg": "OTP Verified! You may now set your new password."
                })
            else:
                return render(request, "forgotpassword.html", {
                    "step": "otp",
                    "email": email,
                    "otp_code": session_otp,
                    "msg": "Incorrect OTP code. Please enter the correct code shown in the demo notification."
                })
                
        elif step == 'reset':
            email = request.session.get('forgot_email')
            pass1 = request.POST.get('t3')
            pass2 = request.POST.get('t4')
            
            if pass1 != pass2:
                return render(request, "forgotpassword.html", {
                    "step": "reset",
                    "email": email,
                    "msg": "Passwords do not match. Please enter identical passwords."
                })
            
            if len(pass1) < 8:
                return render(request, "forgotpassword.html", {
                    "step": "reset",
                    "email": email,
                    "msg": "Password must be at least 8 characters long."
                })
            
            # Update password in both tables
            userlogin.objects.filter(username=email).update(password=pass1)
            userregistration.objects.filter(email=email).update(password=pass1)
            
            # Cleanup sessions
            if 'forgot_otp' in request.session:
                del request.session['forgot_otp']
            if 'forgot_email' in request.session:
                del request.session['forgot_email']
                
            return render(request, "forgotpassword.html", {
                "step": "success",
                "msg": "Your password has been reset successfully!"
            })
            
    return render(request, "forgotpassword.html", {"step": "email"})

def showusereg(request):
    if request.session.get('utype') != 'admin':
        return redirect('logcheck')
    userdict=userregistration.objects.all()
    return render(request,"viewuseregistration.html",{'userdict':userdict})

def deluserreg(request,pk):
    if request.session.get('utype') != 'admin':
        return redirect('logcheck')
    id=userregistration.objects.get(id=pk)
    id.delete()
    userdict = userregistration.objects.all()
    return render(request, "viewuseregistration.html", {'userdict': userdict})



def insertsymptom(request):
    utype = request.session.get('utype')
    if utype != 'patient':
        return redirect('logcheck')
    if not patientprofile.objects.filter(user=request.session.get('username')).exists():
        return render(request, "patientprofileinfo.html", {"msg": "Please complete your patient profile before recording symptoms."})

    if request.method=="POST":
        s1 = request.session.get('username') # Auto-taken
        s2 = request.POST.get("t2", "").strip() # Symptom name
        s3 = request.POST.get("t3", "").strip() # Severity
        s4 = request.POST.get("t4", "").strip() # Duration
        s5 = request.POST.get("t5", "").strip() # Body part
        s6 = request.POST.get("t6", "").strip() # Recorded date
        s7 = request.POST.get("t7", "").strip() # Description

        errors = []
        if not s2 or len(s2) < 3:
            errors.append("Symptom name must be at least 3 characters.")
        if s3 not in ["Low", "Medium", "High", "Critical"]:
            errors.append("Please select a valid severity level.")
        if not s4 or len(s4) < 2:
            errors.append("Duration must be specified (min 2 characters).")
        if not s5 or len(s5) < 3:
            errors.append("Body part must be specified (min 3 characters).")
        if not s6:
            errors.append("Recorded date is required.")
        if not s7 or len(s7) < 5:
            errors.append("Description must be at least 5 characters.")

        if errors:
            return render(request, "symptomsinfo.html", {
                "msg": "Validation failed: " + " | ".join(errors)
            })

        symptomrecord.objects.create(
            patient=s1,
            symptom_name=s2,
            severity=s3,
            duration=s4,
            body_part=s5,
            recorded_date=s6,
            description=s7
        )
        return render(request, "symptomsinfo.html", {"msg": "Symptom info recorded successfully!"})
        
    return render(request, "symptomsinfo.html")


def showsymptom(request):
    utype = request.session.get('utype')
    if utype not in ['doctor', 'admin']:
        return redirect('logcheck')
    if utype == 'doctor' and not doctorprofile.objects.filter(user=request.session.get('username')).exists():
        return render(request, "docprofileinfo.html", {"msg": "Please complete your profile to access doctor modules."})
    userdict=symptomrecord.objects.all()
    return render(request,"viewsymptoms.html",{'userdict':userdict})

def delsymptom(request,pk):
    utype = request.session.get('utype')
    if utype not in ['doctor', 'admin']:
        return redirect('logcheck')
    if utype == 'doctor' and not doctorprofile.objects.filter(user=request.session.get('username')).exists():
        return render(request, "docprofileinfo.html", {"msg": "Please complete your profile to access doctor modules."})
    id=symptomrecord.objects.get(id=pk)
    id.delete()
    userdict = symptomrecord.objects.all()
    return render(request, "viewsymptoms.html", {'userdict': userdict})



def daignosis1(request):
    utype = request.session.get('utype')
    if utype != 'doctor':
        return redirect('logcheck')
    if not doctorprofile.objects.filter(user=request.session.get('username')).exists():
        return render(request, "docprofileinfo.html", {"msg": "Please complete your profile to access doctor modules."})

    import random
    if request.method=="POST":
        s1 = request.POST.get("t1", "").strip() # Patient Name
        s2 = request.session.get('username')   # Auto-taken Doctor Name
        s3 = request.POST.get("t3", "").strip() # Diagnosis Date
        s4 = request.POST.get("t4", "").strip() # Condition Name
        s5 = request.POST.get("t5", "").strip() # Diagnosis Type
        s6 = request.POST.get("t6", "").strip() # Description
        s7 = request.POST.get("t7", "").strip() # Severity Level
        s8 = request.POST.get("t8", "").strip() # Follow-up Date
        diag_id = request.POST.get("diagnosis_id", "").strip()

        errors = []
        if not diag_id:
            errors.append("Diagnosis ID is required.")
        if not s1 or len(s1) < 3:
            errors.append("Patient name must be at least 3 characters.")
        if not s3:
            errors.append("Diagnosis date is required.")
        if not s4 or len(s4) < 3:
            errors.append("Condition name must be at least 3 characters.")
        if not s5 or len(s5) < 3:
            errors.append("Diagnosis type must be at least 3 characters.")
        if not s6 or len(s6) < 5:
            errors.append("Description must be at least 5 characters.")
        if s7 not in ["Low", "Medium", "High", "Critical"]:
            errors.append("Please select a valid severity level.")
        if not s8:
            errors.append("Follow-up date is required.")
        
        if s3 and s8 and s8 < s3:
            errors.append("Follow-up date cannot be before the diagnosis date.")

        if errors:
            return render(request, "diagnosisinfo.html", {
                "msg": "Validation failed: " + " | ".join(errors),
                "diagnosis_id": diag_id or f"DIAG-{random.randint(10000, 99999)}"
            })

        diagnosis.objects.create(
            diagnosis_id=diag_id,
            patient=s1,
            doctor=s2,
            diagnosis_date=s3,
            condition_name=s4,
            diagnosis_type=s5,
            description=s6,
            severity_level=s7,
            follow_up_date=s8
        )
        next_id = f"DIAG-{random.randint(10000, 99999)}"
        return render(request, "diagnosisinfo.html", {
            "msg": "Diagnosis saved successfully!",
            "diagnosis_id": next_id
        })
        
    next_id = f"DIAG-{random.randint(10000, 99999)}"
    return render(request, "diagnosisinfo.html", {"diagnosis_id": next_id})


def showdiagnosis(request):
    utype = request.session.get('utype')
    if utype not in ['doctor', 'patient', 'admin']:
        return redirect('logcheck')
    if utype == 'doctor' and not doctorprofile.objects.filter(user=request.session.get('username')).exists():
        return render(request, "docprofileinfo.html", {"msg": "Please complete your profile to access doctor modules."})
    userdict=diagnosis.objects.all()
    return render(request,"viewdiagnosis.html",{'userdict':userdict})

def deldiagnosis(request,pk):
    utype = request.session.get('utype')
    if utype not in ['doctor', 'admin']:
        return redirect('logcheck')
    if utype == 'doctor' and not doctorprofile.objects.filter(user=request.session.get('username')).exists():
        return render(request, "docprofileinfo.html", {"msg": "Please complete your profile to access doctor modules."})
    id=diagnosis.objects.get(id=pk)
    id.delete()
    userdict = diagnosis.objects.all()
    return render(request, "viewdiagnosis.html", {'userdict': userdict})



def insertprescript(request):
    utype = request.session.get('utype')
    if utype != 'doctor':
        return redirect('logcheck')
    if not doctorprofile.objects.filter(user=request.session.get('username')).exists():
        return render(request, "docprofileinfo.html", {"msg": "Please complete your profile to access doctor modules."})

    patient_name = request.GET.get('patient', '')
    symptom = request.GET.get('symptom', '')
    
    suggested_medicine = ""
    suggested_dosage = ""
    suggested_instructions = ""
    
    if symptom:
        symptom_lower = symptom.lower()
        if "fever" in symptom_lower:
            suggested_medicine = "Paracetamol 500mg"
            suggested_dosage = "1 tablet"
            suggested_instructions = "After meals"
        elif "cold" in symptom_lower or "cough" in symptom_lower:
            suggested_medicine = "Cough Syrup / Cetirizine"
            suggested_dosage = "10ml / 1 tablet"
            suggested_instructions = "At bedtime"
        elif "headache" in symptom_lower:
            suggested_medicine = "Ibuprofen / Aspirin"
            suggested_dosage = "1 tablet"
            suggested_instructions = "When needed"
        else:
            suggested_medicine = "General Consultation Needed"

    if request.method=="POST":
        s1 = request.POST.get("t1", "").strip() # Diagnosis/Patient
        s7 = request.POST.get("t7", "").strip() # Prescribed Date

        medicines = request.POST.getlist("t2")
        dosages = request.POST.getlist("t3")
        frequencies = request.POST.getlist("t4")
        durations = request.POST.getlist("t5")
        instructions = request.POST.getlist("t6")

        errors = []
        if not s1 or len(s1) < 3:
            errors.append("Diagnosis/Patient reference is required.")
        if not s7:
            errors.append("Prescribed Date is required.")
        if not medicines or len(medicines) == 0:
            errors.append("At least one medicine is required.")

        valid_medicines_data = []
        for i in range(len(medicines)):
            m_name = medicines[i].strip() if i < len(medicines) else ""
            m_dosage = dosages[i].strip() if i < len(dosages) else ""
            m_freq = frequencies[i].strip() if i < len(frequencies) else ""
            m_dur = durations[i].strip() if i < len(durations) else ""
            m_inst = instructions[i].strip() if i < len(instructions) else ""

            if not m_name or len(m_name) < 3:
                errors.append(f"Medicine #{i+1} Name must be at least 3 characters.")
            if not m_dosage or len(m_dosage) < 2:
                errors.append(f"Medicine #{i+1} Dosage must be at least 2 characters.")
            if not m_freq or len(m_freq) < 3:
                errors.append(f"Medicine #{i+1} Frequency format (e.g. 1-0-1) must be valid.")
            if not m_dur or len(m_dur) < 2:
                errors.append(f"Medicine #{i+1} Duration must be at least 2 characters.")
            if not m_inst or len(m_inst) < 3:
                errors.append(f"Medicine #{i+1} Instructions must be at least 3 characters.")

            valid_medicines_data.append({
                'medicine_name': m_name,
                'dosage': m_dosage,
                'frequency': m_freq,
                'duration': m_dur,
                'instructions': m_inst
            })

        if errors:
            return render(request, "prescriptioninfo.html", {
                "msg": "Validation failed: " + " | ".join(errors),
                'patient_name': patient_name,
                'symptom': symptom,
                'suggested_medicine': suggested_medicine,
                'suggested_dosage': suggested_dosage,
                'suggested_instructions': suggested_instructions,
                'prefilled_medicines': valid_medicines_data
            })

        for med in valid_medicines_data:
            prescription.objects.create(
                diagnosis=s1,
                medicine_name=med['medicine_name'],
                dosage=med['dosage'],
                frequency=med['frequency'],
                duration=med['duration'],
                instructions=med['instructions'],
                prescribed_date=s7
            )
        return render(request, "prescriptioninfo.html", {"msg": "Prescriptions saved successfully!"})
    
    return render(request, "prescriptioninfo.html", {
        'patient_name': patient_name,
        'symptom': symptom,
        'suggested_medicine': suggested_medicine,
        'suggested_dosage': suggested_dosage,
        'suggested_instructions': suggested_instructions
    })


def showprescription(request):
    utype = request.session.get('utype')
    if utype not in ['doctor', 'patient', 'admin']:
        return redirect('logcheck')

    # doctor must complete profile
    if utype == 'doctor' and not doctorprofile.objects.filter(user=request.session.get('username')).exists():
        return render(request, "docprofileinfo.html", {"msg": "Please complete your profile to access doctor modules."})

    username = request.session.get('username')

    if utype == 'patient':
        # prescription.diagnosis is a CharField, and in practice it may store either:
        # 1) diagnosis.diagnosis_id (DIAG-xxxxx), OR
        # 2) the diagnosis.patient (patient username/email), depending on how t1 was filled.
        patient_diagnosis_ids = diagnosis.objects.filter(patient=username) \
            .values_list('diagnosis_id', flat=True)

        # include also the diagnosis.patient strings as a fallback match
        userdict = prescription.objects.filter(
            diagnosis__in=list(patient_diagnosis_ids)
        )

        # If nothing matched by diagnosis_id, try matching by the patient string stored in diagnosis.patient.
        if not userdict.exists():
            userdict = prescription.objects.filter(diagnosis=username)

    elif utype == 'doctor':
        userdict = prescription.objects.all()
    else:
        userdict = prescription.objects.all()

    return render(request, "viewprescription.html", {'userdict': userdict})


def delprescription(request,pk):
    utype = request.session.get('utype')
    if utype not in ['doctor', 'admin']:
        return redirect('logcheck')

    if utype == 'doctor' and not doctorprofile.objects.filter(user=request.session.get('username')).exists():
        return render(request, "docprofileinfo.html", {"msg": "Please complete your profile to access doctor modules."})

    id = prescription.objects.get(id=pk)

    # If a doctor deletes, keep existing behavior; if an admin deletes, also keep.
    # (Do not allow patient to delete.)
    id.delete()

    # After deletion, respect doctor/patient visibility rules.
    return showprescription(request)


def viewprescriptiondetail(request, pk):
    utype = request.session.get('utype')
    if utype not in ['doctor', 'patient', 'admin']:
        return redirect('logcheck')

    # Restrict access similar to showprescription
    if utype == 'doctor' and not doctorprofile.objects.filter(user=request.session.get('username')).exists():
        return render(request, "docprofileinfo.html", {"msg": "Please complete your profile to access doctor modules."})

    pres = prescription.objects.get(id=pk)

    if utype == 'patient':
        username = request.session.get('username')
        patient_diagnosis_ids = diagnosis.objects.filter(patient=username).values_list('diagnosis_id', flat=True)
        allowed = pres.diagnosis in list(patient_diagnosis_ids) or pres.diagnosis == username
        if not allowed:
            return redirect('showprescription')

    return render(request, "viewprescriptiondetail.html", {'pres': pres})








def insertpayment(request):
    utype = request.session.get('utype')
    if utype != 'patient':
        return redirect('logcheck')
    if not patientprofile.objects.filter(user=request.session.get('username')).exists():
        return render(request, "patientprofileinfo.html", {"msg": "Please complete your patient profile before proceeding with payment."})

    if request.method=="POST":
        s1 = request.POST.get("t1", "").strip() # patient name
        s2 = request.POST.get("t2", "").strip() # diagnosis id
        s3 = request.POST.get("t3", "").strip() # lab test id
        s4 = request.POST.get("t4", "").strip() # amount
        s5 = request.POST.get("t5", "").strip() # date
        s6 = request.POST.get("t6", "").strip() # method
        s7 = request.POST.get("t7", "").strip() # transaction id
        s8 = request.POST.get("t8", "").strip() # status

        errors = []
        if not s1:
            errors.append("Patient name is required.")
        if not s2:
            errors.append("Diagnosis reference is required.")
        if not s3:
            errors.append("Lab Test reference is required.")
        try:
            amt = float(s4)
            if amt <= 0:
                errors.append("Amount must be greater than zero.")
        except ValueError:
            errors.append("Amount must be a valid numeric value.")
        
        if not s5:
            errors.append("Payment date is required.")
        if s6 not in ["Credit Card", "UPI", "PayPal", "Net Banking"]:
            errors.append("Please select a valid payment method.")
        if not s7:
            errors.append("Transaction ID is missing or invalid.")
        if s8 not in ["Completed", "Pending"]:
            errors.append("Invalid payment status.")

        if errors:
            return render(request, "paymentinfo.html", {"msg": "Payment failed: " + " | ".join(errors)})

        payment.objects.create(patient=s1,diagnosis=s2,lab_test=s3,amount=s4,payment_date=s5,payment_method=s6,transaction_id=s7,status=s8)
        return render(request,"paymentinfo.html", {"msg": f"Payment of ${s4} processed successfully! Transaction ID: {s7}"})
        
    return render(request,"paymentinfo.html")

def showmpayment(request):
    userdict=payment.objects.all()
    return render(request,"viewpayment.html",{'userdict':userdict})

def delpayment(request,pk):
    id=payment.objects.get(id=pk)
    id.delete()
    userdict = payment.objects.all()
    return render(request, "viewpayment.html", {'userdict': userdict})



def insertpatient(request):
    if request.session.get('utype') != 'patient':
        return redirect('logcheck')
        
    username = request.session.get('username')
    profile = patientprofile.objects.filter(user=username).first()

    if request.method=="POST":
        s2 = request.POST.get("t2", "").strip() # Age
        s3 = request.POST.get("t3", "").strip() # Gender
        s4 = request.POST.get("t4", "").strip() # Blood Group
        s5 = request.POST.get("t5", "").strip() # Weight
        s6 = request.POST.get("t6", "").strip() # Height
        s7 = request.POST.get("t7", "").strip() # Existing Conditions
        s8 = request.POST.get("t8", "").strip() # Allergies

        errors = []
        if not s2.isdigit() or int(s2) < 0 or int(s2) > 120:
            errors.append("Age must be a valid number between 0 and 120.")
        if s3 not in ["Male", "Female", "Other"]:
            errors.append("Please select a valid gender.")
        if s4 not in ["A+", "A-", "B+", "B-", "AB+", "AB-", "O+", "O-"]:
            errors.append("Please select a valid blood group.")
        
        try:
            w = float(s5)
            if w <= 0 or w > 300:
                errors.append("Weight must be a valid number between 1 and 300 kg.")
        except ValueError:
            errors.append("Weight must be a valid number.")

        try:
            h = float(s6)
            if h <= 0 or h > 250:
                errors.append("Height must be a valid number between 30 and 250 cm.")
        except ValueError:
            errors.append("Height must be a valid number.")

        if not s7 or len(s7) < 3:
            errors.append("Existing Conditions must be at least 3 characters.")
        if not s8 or len(s8) < 3:
            errors.append("Allergies must be at least 3 characters.")

        if errors:
            return render(request, "patientprofileinfo.html", {
                "msg": "Validation failed: " + " | ".join(errors),
                "profile": profile
            })

        if profile:
            # Update existing profile
            profile.age = s2
            profile.gender = s3
            profile.blood_group = s4
            profile.weight = s5
            profile.height = s6
            profile.existing_conditions = s7
            profile.allergies = s8
            profile.save()
            msg = "Profile updated successfully!"
        else:
            # Create new profile
            profile = patientprofile.objects.create(
                user=username,
                age=s2,
                gender=s3,
                blood_group=s4,
                weight=s5,
                height=s6,
                existing_conditions=s7,
                allergies=s8
            )
            msg = "Profile created successfully!"

        request.session['profile_exists'] = True
        return render(request, "patientprofileinfo.html", {"msg": msg, "profile": profile})

    return render(request, "patientprofileinfo.html", {"profile": profile})


def showmpatient(request):
    utype = request.session.get('utype')
    if utype not in ['doctor', 'admin']:
        return redirect('logcheck')
    if utype == 'doctor' and not doctorprofile.objects.filter(user=request.session.get('username')).exists():
        return render(request, "docprofileinfo.html", {"msg": "Please complete your profile to access doctor modules."})
    userdict=patientprofile.objects.all()
    for patient in userdict:
        symptoms = symptomrecord.objects.filter(patient=patient.user)
        patient.symptoms = ", ".join([s.symptom_name for s in symptoms]) if symptoms.exists() else "No symptoms recorded"
    return render(request,"viewpatientprofie.html",{'userdict':userdict})

def delpatient(request,pk):
    utype = request.session.get('utype')
    if utype not in ['doctor', 'admin']:
        return redirect('logcheck')
    if utype == 'doctor' and not doctorprofile.objects.filter(user=request.session.get('username')).exists():
        return render(request, "docprofileinfo.html", {"msg": "Please complete your profile to access doctor modules."})
    id=patientprofile.objects.get(id=pk)
    id.delete()
    userdict = patientprofile.objects.all()
    for patient in userdict:
        symptoms = symptomrecord.objects.filter(patient=patient.user)
        patient.symptoms = ", ".join([s.symptom_name for s in symptoms]) if symptoms.exists() else "No symptoms recorded"
    return render(request, "viewpatientprofie.html", {'userdict': userdict})

def insertnotification(request):
    utype = request.session.get('utype')
    if utype not in ['admin', 'doctor']:
        return redirect('logcheck')

    if request.method=="POST":
        s1 = request.POST.get("t1", "").strip() # Target User
        s2 = request.POST.get("t2", "").strip() # Message Content
        s3 = request.POST.get("t3", "").strip() # Notification Type
        s4 = request.POST.get("t4", "").strip() # Status (Read/Unread)
        s5 = request.POST.get("t5", "").strip() # Created Date

        errors = []
        if not s1 or len(s1) < 3:
            errors.append("Target User is required (min 3 characters).")
        if not s2 or len(s2) < 5:
            errors.append("Message Content must be at least 5 characters.")
        if s3 not in ["Alert", "Reminder", "Recommendation", "System"]:
            errors.append("Please select a valid notification type.")
        if s4 not in ["0", "1"]:
            errors.append("Please select a valid status.")
        if not s5:
            errors.append("Created Date is required.")

        if errors:
            return render(request, "notificationinfo.html", {
                "msg": "Validation failed: " + " | ".join(errors)
            })

        notification.objects.create(
            user=s1,
            message=s2,
            notification_type=s3,
            is_read=s4,
            created_date=s5
        )
        return render(request, "notificationinfo.html", {"msg": "Notification sent successfully!"})
        
    return render(request, "notificationinfo.html")


def showmnotification(request):
    utype = request.session.get('utype')
    if utype == 'admin':
        # Admin sees all notifications (sent to any user)
        notifications = notification.objects.all()
    elif utype == 'patient':
        # Patient sees only notifications addressed to them
        username = request.session.get('username')
        notifications = notification.objects.filter(user=username)
    else:
        # For other roles (e.g., doctor) restrict to none or redirect
        notifications = notification.objects.none()
    return render(request, "viewnotification.html", {'userdict': notifications})

def delnotification(request,pk):
    id=notification.objects.get(id=pk)
    id.delete()
    userdict = notification.objects.all()
    return render(request, "viewnotification.html", {'userdict': userdict})

def viewnotificationdetail(request, pk):
    try:
        notif = notification.objects.get(id=pk)
    except notification.DoesNotExist:
        return redirect('showmnotification')
    return render(request, "notification_detail.html", {'notif': notif})

def insertmedihistory(request):
    utype = request.session.get('utype')
    if utype != 'doctor':
        return redirect('logcheck')
    if not doctorprofile.objects.filter(user=request.session.get('username')).exists():
        return render(request, "docprofileinfo.html", {"msg": "Please complete your profile to access doctor modules."})

    if request.method=="POST":
        s1 = request.POST.get("t1", "").strip() # Patient Name
        s2 = request.POST.get("t2", "").strip() # Existing Conditions (Diagnosis)
        s3 = request.POST.get("t3", "").strip() # Past Surgeries (Treatment Summary)
        s4 = request.POST.get("t4", "").strip() # Allergies (Outcome)
        s5 = request.POST.get("t5", "").strip() # Current Medications (Date Recorded)
        s6 = request.POST.get("t6", "").strip() # Family Medical History (Notes)

        errors = []
        if not s1 or len(s1) < 3:
            errors.append("Patient Name is required (min 3 characters).")
        if not s2 or len(s2) < 3:
            errors.append("Existing Conditions are required (min 3 characters).")
        if not s3 or len(s3) < 3:
            errors.append("Past Surgeries are required (min 3 characters).")
        if not s4 or len(s4) < 3:
            errors.append("Allergies are required (min 3 characters).")
        if not s5 or len(s5) < 3:
            errors.append("Current Medications are required (min 3 characters).")
        if not s6 or len(s6) < 3:
            errors.append("Family Medical History is required (min 3 characters).")

        if errors:
            return render(request, "medicallhistoryinfo.html", {
                "msg": "Validation failed: " + " | ".join(errors)
            })

        medicalhistory.objects.create(
            patient=s1,
            diagnosis=s2,
            treatment_summary=s3,
            outcome=s4,
            date_recorded=s5,
            notes=s6
        )
        return render(request, "medicallhistoryinfo.html", {"msg": "Medical History recorded successfully!"})
        
    return render(request, "medicallhistoryinfo.html")


def showmedicalhistory(request):
    utype = request.session.get('utype')
    if utype not in ['doctor', 'patient', 'admin']:
        return redirect('logcheck')
    if utype == 'doctor' and not doctorprofile.objects.filter(user=request.session.get('username')).exists():
        return render(request, "docprofileinfo.html", {"msg": "Please complete your profile to access doctor modules."})
    userdict=medicalhistory.objects.all()
    return render(request,"viewmedicalhistory.html",{'userdict':userdict})

def delmedicalhistory(request,pk):
    utype = request.session.get('utype')
    if utype not in ['doctor', 'admin']:
        return redirect('logcheck')
    if utype == 'doctor' and not doctorprofile.objects.filter(user=request.session.get('username')).exists():
        return render(request, "docprofileinfo.html", {"msg": "Please complete your profile to access doctor modules."})
    id=medicalhistory.objects.get(id=pk)
    id.delete()
    userdict = medicalhistory.objects.all()
    return render(request, "viewmedicalhistory.html", {'userdict': userdict})

def insertlabtest(request):
    utype = request.session.get('utype')
    if utype not in ['admin', 'doctor']:
        return redirect('logcheck')

    if request.method=="POST":
        s1 = request.POST.get("t1", "").strip() # Patient Name
        s2 = request.POST.get("t2", "").strip() # Diagnosis / Reason
        s3 = request.POST.get("t3", "").strip() # Test Name
        s4 = request.POST.get("t4", "").strip() # Test Type
        s5 = request.session.get('username') if utype == 'doctor' else request.POST.get("t5", "").strip() # Prescribed By
        s6 = request.POST.get("t6", "").strip() # Test Date
        s7 = request.POST.get("t7", "").strip() # Status
        s8 = request.POST.get("t8", "").strip() # Cost

        errors = []
        if not s1 or len(s1) < 3:
            errors.append("Patient Name must be at least 3 characters.")
        if not s2 or len(s2) < 3:
            errors.append("Diagnosis / Reason must be at least 3 characters.")
        if not s3 or len(s3) < 3:
            errors.append("Test Name must be at least 3 characters.")
        if not s4 or len(s4) < 3:
            errors.append("Test Type must be at least 3 characters.")
        if not s5 or len(s5) < 3:
            errors.append("Prescribed By Doctor Name must be at least 3 characters.")
        if not s6:
            errors.append("Test Date is required.")
        if s7 not in ["Pending", "Completed", "Cancelled"]:
            errors.append("Please select a valid status.")
        
        try:
            c = float(s8)
            if c < 0:
                errors.append("Cost must be a positive number.")
        except ValueError:
            errors.append("Cost must be a valid numeric value.")

        if errors:
            return render(request, "labtest.html", {
                "msg": "Validation failed: " + " | ".join(errors)
            })

        labtest.objects.create(
            patient=s1,
            diagnosis=s2,
            test_name=s3,
            test_type=s4,
            prescribed_by=s5,
            test_date=s6,
            status=s7,
            cost=s8
        )
        return render(request, "labtest.html", {"msg": "Lab Test scheduled successfully!"})
        
    return render(request, "labtest.html")


def showlabtest(request):
    userdict=labtest.objects.all()
    return render(request,"viewlabtest.html",{'userdict':userdict})

def dellabtest(request,pk):
    id=labtest.objects.get(id=pk)
    id.delete()
    userdict = labtest.objects.all()
    return render(request, "viewlabtest.html", {'userdict': userdict})

def insertlabresult(request):
    utype = request.session.get('utype')
    if utype not in ['admin', 'doctor']:
        return redirect('logcheck')

    if request.method=="POST":
        s1 = request.POST.get("t1", "").strip() # Lab Test
        s2 = request.POST.get("t2", "").strip() # Result Value
        s3 = request.POST.get("t3", "").strip() # Normal Range
        s4 = request.POST.get("t4", "").strip() # Result Status
        s5 = request.POST.get("t5", "").strip() # Report Date
        s6 = request.POST.get("t6", "").strip() # Technician Name
        report_file = request.FILES.get("t7")    # Report File Upload

        errors = []
        if not s1 or len(s1) < 3:
            errors.append("Lab Test reference is required (min 3 characters).")
        if not s2:
            errors.append("Result Value is required.")
        if not s3:
            errors.append("Normal Range is required.")
        if s4 not in ["Normal", "Abnormal", "Critical"]:
            errors.append("Please select a valid result status.")
        if not s5:
            errors.append("Report Date is required.")
        if not s6 or len(s6) < 3:
            errors.append("Technician Name is required.")

        # File validation
        ALLOWED_EXTENSIONS = ['.pdf', '.jpg', '.jpeg', '.png', '.doc', '.docx']
        MAX_FILE_SIZE = 5 * 1024 * 1024 # 5MB
        
        if report_file:
            import os
            file_ext = os.path.splitext(report_file.name)[1].lower()
            if file_ext not in ALLOWED_EXTENSIONS:
                errors.append("Report File must be a valid document (.pdf, .jpg, .jpeg, .png, .doc, .docx).")
            if report_file.size > MAX_FILE_SIZE:
                errors.append("Report file size must be less than 5MB.")

        if errors:
            return render(request, "labresultinfo.html", {
                "msg": "Validation failed: " + " | ".join(errors)
            })

        labresult.objects.create(
            lab_test=s1,
            result_value=s2,
            normal_range=s3,
            result_status=s4,
            report_date=s5,
            technician_name=s6,
            report_file=report_file
        )
        return render(request, "labresultinfo.html", {"msg": "Lab Result saved successfully!"})
        
    return render(request, "labresultinfo.html")


def showlabresult(request):
    userdict=labresult.objects.all()
    return render(request,"viewlabresultinfo.html",{'userdict':userdict})

def dellabresult(request,pk):
    id=labresult.objects.get(id=pk)
    id.delete()
    userdict = labresult.objects.all()
    return render(request, "viewlabresultinfo.html", {'userdict': userdict})

def insertfeedback(request):
    utype = request.session.get('utype')
    if utype != 'patient':
        return redirect('logcheck')
    if not patientprofile.objects.filter(user=request.session.get('username')).exists():
        return render(request, "patientprofileinfo.html", {"msg": "Please complete your patient profile before submitting feedback."})

    if request.method=="POST":
        s1 = request.session.get('username') # Auto-taken Patient
        s2 = request.POST.get("t2", "").strip() # Doctor Name
        s3 = request.POST.get("t3", "").strip() # Rating
        s4 = request.POST.get("t4", "").strip() # Comments
        s5 = request.POST.get("t5", "").strip() # Date

        errors = []
        if not s2 or len(s2) < 3:
            errors.append("Doctor Name must be at least 3 characters.")
        
        try:
            r = int(s3)
            if r < 1 or r > 5:
                errors.append("Rating must be an integer between 1 and 5.")
        except ValueError:
            errors.append("Rating must be a valid number.")

        if not s4 or len(s4) < 5:
            errors.append("Comments must be at least 5 characters.")
        if not s5:
            errors.append("Feedback Date is required.")

        if errors:
            return render(request, "feedbackinfo.html", {
                "msg": "Validation failed: " + " | ".join(errors)
            })

        feedback.objects.create(
            patient=s1,
            doctor=s2,
            rating=s3,
            comments=s4,
            feedback_date=s5
        )
        return render(request, "feedbackinfo.html", {"msg": "Feedback submitted successfully!"})
        
    return render(request, "feedbackinfo.html")


def showfeedback(request):
    userdict=feedback.objects.all()
    return render(request,"viewfeedback.html",{'userdict':userdict})

def delfeedback(request,pk):
    id=feedback.objects.get(id=pk)
    id.delete()
    userdict = feedback.objects.all()
    return render(request, "viewfeedback.html", {'userdict': userdict})

def insertdoctor(request):
    if request.session.get('utype') != 'doctor':
        return redirect('logcheck')
    
    username = request.session.get('username')
    profile = doctorprofile.objects.filter(user=username).first()

    if request.method == "POST":
        import re
        s2 = request.POST.get("t2", "").strip() # specialization
        s3 = request.POST.get("t3", "").strip() # qualification
        s4 = request.POST.get("t4", "").strip() # experience_years
        s5 = request.POST.get("t5", "").strip() # hospital_name
        s6 = request.POST.get("t6", "").strip() # consultation_fee
        s7 = request.POST.get("t7", "").strip() # available_time
        photo_file = request.FILES.get("t8")     # photo file upload

        errors = []
        if not s2 or len(s2) < 3:
            errors.append("Specialization must be at least 3 characters.")
        if not s3 or len(s3) < 2:
            errors.append("Qualification must be at least 2 characters.")
        if not s4.isdigit() or int(s4) < 0 or int(s4) > 60:
            errors.append("Experience must be a valid number of years between 0 and 60.")
        if not s5 or len(s5) < 3:
            errors.append("Hospital Name must be at least 3 characters.")
        
        try:
            fee = float(s6)
            if fee < 0:
                errors.append("Consultation Fee must be a positive number.")
        except ValueError:
            errors.append("Consultation Fee must be a valid number.")

        if not s7 or len(s7) < 3:
            errors.append("Available Time must be provided.")
        
        # Photo file validation
        ALLOWED_EXTENSIONS = ['.jpg', '.jpeg', '.png', '.gif', '.bmp', '.webp']
        MAX_FILE_SIZE = 5 * 1024 * 1024  # 5MB

        if photo_file:
            import os
            file_ext = os.path.splitext(photo_file.name)[1].lower()
            if file_ext not in ALLOWED_EXTENSIONS:
                errors.append("Photo must be a valid image file (.jpg, .jpeg, .png, .gif, .bmp, .webp).")
            if photo_file.size > MAX_FILE_SIZE:
                errors.append("Photo file size must be less than 5MB.")
        elif not profile or not profile.photo:
            errors.append("Please upload a profile photo.")

        if errors:
            return render(request, "docprofileinfo.html", {
                "msg": "Validation failed: " + " | ".join(errors),
                "profile": profile
            })

        if profile:
            # Update profile
            profile.specialization = s2
            profile.qualification = s3
            profile.experience_years = s4
            profile.hospital_name = s5
            profile.consultation_fee = s6
            profile.available_time = s7
            if photo_file:
                profile.photo = photo_file
            profile.save()
            msg = "Profile updated successfully!"
        else:
            # Create new profile
            profile = doctorprofile.objects.create(
                user=username,
                specialization=s2,
                qualification=s3,
                experience_years=s4,
                hospital_name=s5,
                consultation_fee=s6,
                available_time=s7,
                photo=photo_file
            )
            msg = "Profile created successfully!"

        request.session['profile_exists'] = True
        return render(request, "docprofileinfo.html", {"msg": msg, "profile": profile})
    
    return render(request, "docprofileinfo.html", {"profile": profile})


def showdoctor(request):
    userdict=doctorprofile.objects.all()
    return render(request,"viewdoctorprofileinfo.html",{'userdict':userdict})

def deldoctor(request,pk):
    id=doctorprofile.objects.get(id=pk)
    id.delete()
    userdict = doctorprofile.objects.all()
    return render(request, "viewdoctorprofileinfo.html", {'userdict': userdict})



def insertlogin(request):

    if request.method=="POST":
        s1=request.POST.get("t1")
        s2 = request.POST.get("t2")
        s3 = request.POST.get("t3")


        userlogin.objects.create(username=s1,password=s2,type=s3)
        return render(request,"login.html")
    return render(request,"login.html")

def showlogin(request):
    userdict=userlogin.objects.all()
    return render(request,"viewlogin.html",{'userdict':userdict})

def dellogin(request,pk):
    id=userlogin.objects.get(id=pk)
    id.delete()
    userdict = userlogin.objects.all()
    return render(request, "viewlogin.html", {'userdict': userdict})

def showindex(request):
    return render(request,"index.html")

