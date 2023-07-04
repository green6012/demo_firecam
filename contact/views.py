from django.http import HttpResponse
from django.shortcuts import render
from django.views import View
from  .forms import contact_form
from .models import contactform
# Create your views here.
class contact(View):
    def get(self ,request):
        #cach 2
        # context = {'cf':contact_form}
        cf = contact_form
       #return render(request, 'contact/contact.html',context)
        return render(request, 'contact/contact.html',{'cf':cf})

    def post(self, request):
        if request.method == "POST":
            cf= contact_form(request.POST)
            if cf.is_valid():
                saveCF = contactform(username = cf.cleaned_data['username'],
                                     email = cf.cleaned_data['email'],
                                     body = cf.cleaned_data['body'])
                saveCF.save()
                return HttpResponse('save success')
        else:
            return HttpResponse("not post")




#cach 1
# def getContact(request):
#     if request.method == "POST":
#         cf = contact_form(request.POST)
#         if cf.is_valid():
#             cf.save()
#             return contact(request)
#         else:
#             return  HttpResponse("not POST")
