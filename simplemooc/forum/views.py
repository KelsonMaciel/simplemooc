from django.shortcuts import render
from django.views.generic import TemplateView, View, ListView

from .models import Thread

# Create your views here.

#Trabalhando com as views genericas
#class ForumView(TemplateView):
#
#    template_name = 'forum/index.html'
#
#index = ForumView.as_view()

#trabalhando direto com as views 
#class ForumView(view):
#    def get(self, request, *args, **kwargs):
#        return render(request, 'forum/index.html')

class ForumView(ListView):
    
    paginate_by = 1
    template_name = 'forum/index.html'

    def get_context_data(self, **kwargs):
        context = super(ForumView, self).get_context_data(**kwargs)
        context['tags'] = Thread.tags.all()
        return context

    def get_queryset(self):
        queryset = Thread.objects.all()
        order = self.request.GET.get('order','') 
        if order == 'view':
             queryset = queryset.order_by('-view')
        elif order == 'answers':
             queryset = queryset.order_by('-answers')    
        return queryset         
    

index = ForumView.as_view()