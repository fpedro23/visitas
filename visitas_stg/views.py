from django.http import HttpResponse

# Create your views here.
from django.template import loader, RequestContext


def detail(request):
    template = loader.get_template('filtros.html')
    context = RequestContext(request, {
        'latest_question_list': "1,2",
    })
    return HttpResponse(template.render(context))