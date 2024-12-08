from django.db.models import Exists, OuterRef  #Onko kirja lainassa testiin
from django.shortcuts import get_object_or_404, redirect, render
from django.views import generic, View
from django.urls import reverse_lazy
from django.utils import timezone
from django.db.models import Q
from django.http import HttpResponseServerError
from .models import Laina, Kirja


class LainaListView(generic.ListView):
    """
    Näkymä aktiivisten lainojen listaamiseen. Näyttää vain kirjautuneen käyttäjän aktiiviset lainat.

    Attributes:
        model (django.db.models.Model): Malli, joka kuvaa lainaa.
        template_name (str): Polku HTML-pohjaan, jota käytetään näkymän renderöintiin.
        context_object_name (str): Kontekstimuuttujan nimi, jolla lainat välitetään templateen.
    """

    model = Laina
    template_name = 'kirjasto/lainat.html'
    context_object_name = 'lainat'

    def get_queryset(self):
        """
        Palauttaa käyttäjän aktiiviset lainat. Vain kirjautuneille käyttäjille.
        """
        try:
            if not self.request.user.is_authenticated:
                return Laina.objects.none()
            return Laina.objects.filter(asiakas=self.request.user,
                                        palautettu__isnull=True)
        except Exception as e:
            # Log error here if necessary
            return Laina.objects.none()  # Return an empty queryset on error

    def get_context_data(self, **kwargs):
        """
        Luo kontekstitietojen sanakirjan näkymälle. Lisää 'lainat' ja 'loan_history' konteksteihin.
        """
        context = super().get_context_data(**kwargs)
        user = self.request.user
        if user.is_authenticated:
            context['lainat'] = self.get_queryset()
            context['loan_history'] = LoanHistoryView.get_queryset(self).order_by('-palautettu')
        else:
            context['lainat'] = []
            context['loan_history'] = []
        return context


class ReturnBookView(generic.UpdateView):
    """
    Näkymä kirjan palauttamiseen. Päivittää kirjan 'palautettu'-kentän nykyisellä aikaleimalla, kun
    lomake lähetetään onnistuneesti.

    Attributes:
        model (django.db.models.Model): Malli, joka kuvaa lainattua kirjaa.
        fields (list): Lista kentistä, joita päivitetään. Tässä tapauksessa vain 'palautettu'-kenttä.
        template_name (str): Polku HTML-pohjaan, jota käytetään näkymän renderöintiin.
        success_url (django.urls.reverse_lazy): URL, johon ohjataan käyttäjä onnistuneen päivityksen jälkeen.
    """
    model = Laina
    fields = ['palautettu']
    template_name = 'kirjasto/return_book.html'
    success_url = reverse_lazy('kirjasto:lainat')

    def form_valid(self, form):
        """
        Kutsutaan, kun lomake on validi. Asettaa 'palautettu'-kentän arvoksi nykyisen aikaleiman
        ennen kuin ylivuorotetaan perusluokan form_valid-metodi.
        
        Args:
            form (django.forms.ModelForm): Lomake, joka sisältää päivitettävät tiedot.

        Returns:
            HttpResponseRedirect: Uudelleenohjaus 'success_url':iin.
        """
        try:
            form.instance.palautettu = timezone.now()
            return super().form_valid(form)
        except Exception as e:
            # Log error here if necessary
            return HttpResponseServerError("Error updating book return")


class LainaView(View):

    def post(self, request, *args, **kwargs):
        try:
            kirja_id = request.POST.get('kirja_id')
            kirja = get_object_or_404(Kirja, pk=kirja_id)
            lainaus = Laina.objects.create(asiakas=request.user,
                                           kirja=kirja,
                                           lainauspaiva=timezone.now(),
                                           palautuspaiva=timezone.now() +
                                           timezone.timedelta(days=14))
            return redirect('kirjasto:lainat')
        except Exception as e:
            # Log error here if necessary
            return HttpResponseServerError("Error processing loan")


class LoanHistoryView(generic.ListView):
    """
    Näkymä, joka esittää käyttäjän lainahistorian, eli palautetut lainat.

    Attributes:
        model (django.db.models.Model): Malli, joka kuvaa lainaa.
        template_name (str): Polku HTML-pohjaan, jota käytetään näkymän renderöintiin.
        context_object_name (str): Kontekstimuuttujan nimi, jolla lainat välitetään templateen.
    """

    model = Laina
    template_name = 'kirjasto/history.html'
    context_object_name = 'loan_history'

    def get_queryset(self):
        """
        Määrittää QuerySetin, jota käytetään lainahistorian hankkimiseen. 
        Palauttaa vain kirjautuneen käyttäjän palautetut lainat.

        Returns:
            django.db.models.query.QuerySet: QuerySet, joka sisältää käyttäjän palautetut lainat.
        """
        try:
            return Laina.objects.filter(asiakas=self.request.user,
                                        palautettu__isnull=False)
        except Exception as e:
            # Log error here if necessary
            return Laina.objects.none()  # Return an empty queryset on error


class KirjaView(generic.DetailView):
    login_required = True
    model = Kirja
    template_name = 'kirjasto/kirja.html'
    context_object_name = 'kirja'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        kirja = self.get_object()
        laina = Laina.objects.filter(kirja=kirja,
                                     palautettu__isnull=True).first()
        context['laina'] = laina
        return context


#kirjasto.html kirjojen selaamiseen.
class KirjastoView(generic.ListView):
    model = Kirja
    template_name = 'kirjasto/kirjasto.html'
    context_object_name = 'kirjat'

    #filtteröintiä ja järjestelyä
    def get_queryset(self):
        try:
            queryset = Kirja.objects.all()
            # Kirjoista haku nimen perusteella
            search_query = self.request.GET.get('search', '')
            if search_query:
                queryset = queryset.filter(nimi__icontains=search_query)

            # Kirjoista haku kirjailijan nimen perusteella
            search_query_kirjailija = self.request.GET.get(
                'search_kirjailija', '')
            if search_query_kirjailija:
                queryset = queryset.filter(
                    Q(kirjailija__sukunimi__icontains=search_query_kirjailija)
                    | Q(kirjailija__etunimi__icontains=search_query_kirjailija)
                )

            # Kirjojen järjestely
            order_by = self.request.GET.get('order_by', 'julkaisuvuosi')
            queryset = queryset.order_by(order_by)

            #Onko kirja lainassa?
            loans_subquery = Laina.objects.filter(
                kirja=OuterRef('pk'),
                palautettu__isnull=True  # jos null, kirja on lainassa
            )
            queryset = queryset.annotate(on_loan=Exists(loans_subquery))
            return queryset
        except Exception as e:
            # Log error here if necessary
            return Kirja.objects.none()  # Return an empty queryset on error


def custom_404(request):
    response = render(request, '404.html', {})
    response.status_code = 404
    return response


def custom_500(request):
    response = render(request, '500.html', {})
    response.status_code = 500
    return response
