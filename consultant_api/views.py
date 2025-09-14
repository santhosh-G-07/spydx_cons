# consultant_api/views.py

from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from .models import Consultant


def index(request):
    return render(request, 'frontend/index.html')

def about(request):
    return render(request, 'frontend/about.html')

def services(request):
    return render(request, 'frontend/services.html')

def projects(request):
    return render(request, 'frontend/projects.html')

def contact(request):
    return render(request, 'frontend/contact.html')


def consultant_signup(request):
    if request.method == 'POST':
        name = request.POST.get('name')
        email = request.POST.get('email')
        password = request.POST.get('password')
        phone = request.POST.get('phone')
        specialization = request.POST.get('specialization')  # job role
        location = request.POST.get('location')
        linkedin_id = request.POST.get('linkedin_id')

        # Create the User
        user = User.objects.create_user(
            username=email,
            email=email,
            password=password,
            first_name=name
        )

        # Create Consultant with new fields
        Consultant.objects.create(
            user=user,
            phone=phone,
            specialization=specialization,
            location=location,
            linkedin_id=linkedin_id
        )

        return redirect('consultant_login')

    return render(request, 'frontend/consultant/signup.html')



# ----------------- Consultant Login -----------------
def consultant_login(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        password = request.POST.get('password')

        user = authenticate(request, username=email, password=password)
        if user is not None:
            login(request, user)
            return redirect('consultant_dashboard')
        else:
            return render(request, 'frontend/consultant/login.html', {
                'error': 'Invalid email or password'
            })

    return render(request, 'frontend/consultant/login.html')


# ----------------- Consultant Logout -----------------
def consultant_logout(request):
    logout(request)
    return redirect('consultant_login')


# ----------------- Consultant Dashboard -----------------

@login_required(login_url='consultant_login')
def consultant_dashboard_view(request):
    consultant = request.user.consultant
    total_projects = Project.objects.filter(consultant=consultant).count()
    
    return render(request, 'frontend/consultant/dashboard.html', {
        'consultant': consultant,
        'total_projects': total_projects
    })


# ----------------- Admin placeholders -----------------
def admin_login(request):
    return render(request, 'frontend/admin/login.html')

def admin_signup(request):
    return render(request, 'frontend/admin/signup.html')

def admin_dashboard_view(request):
    return render(request, 'frontend/admin/dashboard.html')
from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.shortcuts import render

@login_required
def consultant_profile(request):
    return render(request, 'frontend/consultant/profile.html')

@login_required
def consultant_projects(request):
    return render(request, 'frontend/consultant/projects.html')

@login_required
def consultant_resume(request):
    return render(request, 'frontend/consultant/resume.html')

@login_required
def consultant_notifications(request):
    return render(request, 'frontend/consultant/notifications.html')

@login_required
def consultant_tracker(request):
    return render(request, 'frontend/consultant/tracker.html')

@login_required
def consultant_reports(request):
    return render(request, 'frontend/consultant/reports.html')

@login_required
def consultant_settings(request):
    return render(request, 'frontend/consultant/settings.html')


import os
from django.conf import settings
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from .forms import ResumeUploadForm
from .models import ResumeUpload, Project
from .utils import extract_text_from_resume, parse_projects_nlp

@login_required(login_url='consultant_login')
def resume_upload_view(request):
    if request.method == 'POST':
        form = ResumeUploadForm(request.POST, request.FILES)
        if form.is_valid():
            resume_instance = form.save(commit=False)
            resume_instance.user = request.user
            resume_instance.save()

            file_path = os.path.join(settings.MEDIA_ROOT, resume_instance.file.name)
            extracted_text = extract_text_from_resume(file_path)

            parsed_projects = parse_projects_nlp(extracted_text)

            max_length = Project._meta.get_field('name').max_length
            consultant = request.user.consultant

            for proj in parsed_projects:
                name = proj['name'][:max_length]  # safely truncate long names
                description = proj['description']

                Project.objects.update_or_create(
                    consultant=consultant,
                    name=name,
                    defaults={'description': description}
                )

            return redirect('consultant_resume')  # or your chosen URL
    else:
        form = ResumeUploadForm()

    user_resumes = ResumeUpload.objects.filter(user=request.user).order_by('-uploaded_at')
    return render(request, 'frontend/consultant/resume_upload.html', {'form': form, 'user_resumes': user_resumes})


from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from .models import Project
from .forms import ProjectForm

@login_required(login_url='consultant_login')
def project_list_view(request):
    consultant = request.user.consultant
    projects = Project.objects.filter(consultant=consultant).order_by('-start_date')
    return render(request, 'frontend/consultant/projects.html', {'projects': projects})

@login_required(login_url='consultant_login')
def project_add_view(request):
    if request.method == 'POST':
        form = ProjectForm(request.POST)
        if form.is_valid():
            project = form.save(commit=False)
            project.consultant = request.user.consultant
            project.save()
            return redirect('consultant_projects')  # URL name for project list
    else:
        form = ProjectForm()
    return render(request, 'frontend/consultant/project_add.html', {'form': form})
import textract
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django import forms
from .models import UserATSResult, Consultant

import os
import tempfile
import textract
from django import forms
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from .models import UserATSResult, Consultant


# ------------ Form for resume upload ------------
class ResumeUploadForm(forms.Form):
    resume_file = forms.FileField()


# ------------ Utility Function: Extract text from uploaded file (Windows Safe) ------------
def extract_text_from_uploaded_file(uploaded_file):
    """
    Saves the uploaded file to a temp path, extracts text using textract,
    deletes the file, and returns the extracted text as a UTF-8 string.
    Works on Windows without permission errors.
    """
    fd, temp_path = tempfile.mkstemp()        # create temp file path
    os.close(fd)                              # close handle (important for Windows)

    try:
        # Write uploaded content to the temp file
        with open(temp_path, 'wb') as tmp_file:
            for chunk in uploaded_file.chunks():
                tmp_file.write(chunk)

        # Extract text
        text_bytes = textract.process(temp_path)
        text = text_bytes.decode('utf-8', errors='ignore')  # ignore decode errors
    finally:
        # Always clean up the temp file
        if os.path.exists(temp_path):
            os.remove(temp_path)

    return text


# ------------ Step 1: Upload Resume & Show Score (Anonymous allowed) ------------
def ats_upload_view(request):
    score = None
    if request.method == "POST":
        form = ResumeUploadForm(request.POST, request.FILES)
        if form.is_valid():
            file = request.FILES["resume_file"]

            # Extract text safely
            try:
                text = extract_text_from_uploaded_file(file)
            except Exception as e:
                return render(request, "frontend/ats/ats_upload.html", {
                    "form": form,
                    "error": f"Could not read file: {e}"
                })

            # Dummy ATS score for now (replace with your ML model later)
            score = 72.5

            # Store text & score in session for after-login use
            request.session["resume_text"] = text
            request.session["ats_score"] = score

            return render(request, "frontend/ats/ats_score.html", {"score": score})
    else:
        form = ResumeUploadForm()

    return render(request, "frontend/ats/ats_upload.html", {"form": form})


# ------------ Step 2: View Mistakes (Requires Login) ------------
@login_required
def ats_view_mistakes(request):
    resume_text = request.session.get("resume_text")
    ats_score = request.session.get("ats_score")

    if not resume_text or ats_score is None:
        return redirect("consultant_ats_upload")

    # Link result to the logged-in consultant
    try:
        consultant = Consultant.objects.get(user=request.user)
    except Consultant.DoesNotExist:
        return redirect("dashboard_home")

    # Example rules for mistakes — replace with your ATS logic
    mistakes = []
    if "Python" not in resume_text:
        mistakes.append("Missing skill: Python")
    if len(resume_text) < 500:
        mistakes.append("Resume is too short")
    if "@" not in resume_text:
        mistakes.append("No email address found")

    # Save the ATS result to DB
    UserATSResult.objects.create(
        consultant=consultant,
        resume_text=resume_text,
        ats_score=ats_score,
        mistakes=mistakes
    )

    # Clear from session
    request.session.pop("resume_text", None)
    request.session.pop("ats_score", None)

    return render(request, "frontend/ats/ats_mistakes.html", {
        "score": ats_score,
        "mistakes": mistakes
    })
