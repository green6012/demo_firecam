from django.shortcuts import render
from  .models import postForm
# Create your views here.
def post(request):
    pF = postForm.objects.all()
    return render(request, 'post/post.html', {'pF':pF})

def postDetail(request, id):
    pD = postForm.objects.get(id = id)
    return render(request, 'post/postDetail.html', {'pD':pD})
