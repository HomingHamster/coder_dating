from django.shortcuts import render
from django.views.generic import TemplateView


class HomePageView(TemplateView):
    template_name = "home.html"
    def get_context_data(self, **kwargs):
        output = """<html>
    <head>
        <title>Home</title>
    </head>
    <body>
        <h1>Home</h1>
    </body>
</html>"""
        return {"html": output}
