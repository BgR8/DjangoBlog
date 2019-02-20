from django.shortcuts import render, HttpResponse

# Create your views here.

def home_view(request):
    #if request.user.is_authenticated():
    #    context = {
    #        'isim': 'Buğra',
    #    }
    #else:
    #    context = {
    #        'isim': 'Misafir Kullanıcı',
    #    }
    context ={
        'isim': 'Buğra',
    }
    return render(request, 'home.html', context)