from django.views.generic import CreateView
from django.urls import reverse_lazy

from .forms import CreationForms


class SignUpView(CreateView):
    form_class = CreationForms
    success_url = reverse_lazy("login")
    template_name = "signup.html"
