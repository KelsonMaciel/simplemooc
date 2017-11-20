import json
from django.shortcuts import render, redirect, get_object_or_404
from django.views.generic import (TemplateView, View, ListView, DetailView)
from django.contrib import messages
from django.http import HttpResponse

from .models import Thread,Reply
from .forms import ReplyForm

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

    def get_queryset(self):
            queryset = Thread.objects.all()
            order = self.request.GET.get('order', '')
            if order == 'view':
                queryset = queryset.order_by('-view')
            elif order == 'answers':
                queryset = queryset.order_by('-answers')

            tag = self.kwargs.get('tag', '')
            if tag:
                queryset = queryset.filter(tags__slug__icontains=tag)

            return queryset

    def get_context_data(self, **kwargs):
            context = super(ForumView, self).get_context_data(**kwargs)
            context['tags'] = Thread.tags.all()
            return context


class ThreadView(DetailView):

    model:Thread
    template_name = 'forum/thread.html'     

    def get_context_data(self, **kwargs):
        context = super(ThreadView, self).get_context_data(**kwargs)
        context['tags'] = Thread.tags.all()
        context['form'] = ReplyForm(self.request.POST or None)
        return context
    
    def post(self, request, *args, **kwargs):
        if not self.request.user_authenticated():
            messages.error(
                self.request, 'Para responder ao tópico é necessário esta logado'
            )
            return redirect(self.request.path)

        self.object = self.get_object()
        context = self.get_context_data(object=self.object)
        form = context['form'] 	
        if form.is_valid():
            reply = form.save(commit=False)
            reply.thread = self.object
            reply.author = self.request.user
            reply.save()
            messages.success(self.request, 'A sua mensagem foi enviada com sucesso')
            context['form'] = ReplyForm()
        return self.render_to_response(context)

class ReplyCorrectView(View):
    
    correct = True

    def get(self, request, pk):
            reply = get_object_or_404(Reply, pk=pk, thread__author=request.user)
            reply.correct = self.correct
            reply.save()
            message = 'Resposta atualizada com sucesso'
            if request.is_ajax():
                data = {'success': True, 'message': message}
                return HttpResponse(json.dumps(data), mimetype='application/json')
            else:
                messages.success(request, message)
                return redirect(reply.thread.get_absolute_url())

        
index  = ForumView.as_view()
thread = ThreadView.as_view()
replay_correct = ReplyCorrectView.as_view()
replay_incorrect = ReplyCorrectView.as_view(correct=False)  