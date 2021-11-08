from django.core import paginator
from .models import Profiles, Skills
from django.db.models import Q 
from django.core.paginator import EmptyPage, PageNotAnInteger, Paginator

# pagination for profiles
def profilesPaginations(request, profiles, results):
    page = request.GET.get('page')
    paginator = Paginator(profiles, results)
    try:
        profiles = paginator.page(page)

    except PageNotAnInteger:
        page = 1
        profiles = paginator.page(page)
    
    except EmptyPage:
        page = paginator.num_pages
        profiles = paginator.page(page)
    
    leftIndex = (int(page) - 4)
    if leftIndex < 1 :
        leftIndex = 1
    
    rightIndex = (int(page) + 4)
    if rightIndex > paginator.num_pages:
        rightIndex = paginator.num_pages + 1
    
    custome_range= range(leftIndex, rightIndex)

    return custome_range, profiles





def searchProfiles(request):
    search_query = ''
    if request.GET.get('search_query'):
        # search_query = request.GET['search_query']
        search_query = request.GET.get('search_query')
    
    skill = Skills.objects.filter(name__iexact=search_query)
    profiles = Profiles.objects.distinct().filter(Q(name__icontains=search_query) | 
    Q(short_intro__icontains=search_query) | 
    Q(bio__icontains=search_query) | 
    Q(skills__in=skill))


    return profiles, search_query