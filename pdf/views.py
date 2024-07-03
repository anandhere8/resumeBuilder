from django.shortcuts import render
from .models import Profile
from django.template import loader
from django.http import HttpResponse
import pdfkit
import io
# Create your views here.
def accept(request) :
  if request.method == "POST" :
    name = request.POST['name']
    email = request.POST['email']
    phone = request.POST['phone']
    summary = request.POST['summary']
    work = request.POST['work']
    skill = request.POST['skill']
    school = request.POST['school']
    university = request.POST['university']
    degree = request.POST['degree']

    profile = Profile(name=name,
                      email=email,
                      phone=phone,
                      summary=summary,
                      previous_work=work,
                      skills=skill,
                      school=school,
                      university=university,
                      degree=degree)
    profile.save()
    
  return render(request=request, template_name="pdf/accept.html")


def resume(request, id) :
  user_profile = Profile.objects.get(pk=id)
  context = {
    'user_profile' : user_profile
  }

  template = loader.get_template('pdf/resume.html')
  html = template.render(context=context)
  # html = render(request=request, template_name='pdf/resume.html', context=context)
  # print(type(html))
  options = {
    'page-size':'Letter',
    'encoding': 'UTF-8',
  }

  pdf = pdfkit.from_string(html, False, options=options)

  response = HttpResponse(pdf, content_type='application/pdf')
  response['Content-Disposition'] = 'attachment'
  filename= 'resume.pdf'

  return response


def list(request) :
  profiles = Profile.objects.all()

  return render(request=request, template_name='pdf/list.html', context= {
    'profiles' : profiles
  })