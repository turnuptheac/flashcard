from django.conf import settings
from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.shortcuts import redirect
from django.urls import reverse_lazy
from django.views import View
from django.views.generic.base import TemplateView
from django.views.generic.edit import FormView

from rest_framework import generics, pagination

from cards.models import Card
from cards.forms import CardForm

# Create your views here.


class PlayView(LoginRequiredMixin, TemplateView):
    """
    Play game
    """
    template_name = 'cards/play.html'
    success_url = reverse_lazy('cards_play')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        user = self.request.user

        context.update({
            'card': Card.objects.next_card(user),
            'has_cards': Card.objects.has_cards(user),
            'temporarily_done': Card.objects.is_temporarily_done(user),
            'permanently_done': Card.objects.is_permanently_done(user),
        })
        return context


class CardsView(LoginRequiredMixin, TemplateView):
    """
    Show words history
    """
    template_name = 'cards/words.html'

    def get(self, request, *args, **kwargs):
        cards_list = request.user.cards.all().order_by('bucket', '-created_at')

        paginator = Paginator(cards_list, settings.CARDS_PAGE_SIZE)
        page = request.GET.get('page')
        try:
            cards = paginator.page(page)
        except PageNotAnInteger:
            # If page is not an integer, deliver first page.
            cards = paginator.page(1)
        except EmptyPage:
            # If page is out of range (e.g. 9999), deliver last page of results.
            cards = paginator.page(paginator.num_pages)

        self.cards = cards

        return super().get(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        page_numbers = pagination._get_displayed_page_numbers(
            self.cards.number, self.cards.paginator.num_pages)

        context.update({
            'cards': self.cards,
            'page_numbers': page_numbers
        })
        return context


class CardAddView(LoginRequiredMixin, FormView):
    """
    Add a card
    """
    template_name = 'cards/add.html'
    form_class = CardForm
    success_url = reverse_lazy('cards_display')

    def form_valid(self, form):
        # This method is called when valid form data has been POSTed.
        # It should return an HttpResponse.
        messages.success(self.request, 'You have successfully added a card.')
        form.instance.user = self.request.user
        form.save()
        return super().form_valid(form)


class CardSuccessView(LoginRequiredMixin, View):
    """
    Remembered a card
    """
    def post(self, request, *args, **kwargs):
        card = generics.get_object_or_404(
            self.request.user.cards.all(),
            id=self.kwargs['id'])
        card.success()
        messages.success(request, 'You remembered a word.')

        return redirect('home')


class CardFailureView(LoginRequiredMixin, View):
    """
    Forgotten a card
    """
    def post(self, request, *args, **kwargs):
        card = generics.get_object_or_404(
            self.request.user.cards.all(),
            id=self.kwargs['id'])
        card.failure()

        messages.error(request, 'You forgot a word.')
        return redirect('home')
