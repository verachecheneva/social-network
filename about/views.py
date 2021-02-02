from django.views.generic.base import TemplateView


class AboutAuthorView(TemplateView):
    template_name = "AboutAuthor.html"


class AboutTechView(TemplateView):
    template_name = "AboutTech.html"
