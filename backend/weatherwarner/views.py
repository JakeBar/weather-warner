from django.shortcuts import render
from django.views.decorators.csrf import ensure_csrf_cookie


@ensure_csrf_cookie
def app(request, **kwargs):
    """
    View to render the react app.
    """
    return render(request, "app.html")
