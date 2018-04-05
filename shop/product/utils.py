from django.contrib.sessions.models import Session

def get_session_instance(request):
    session_key = request.session.session_key
    return Session.objects.get(session_key=session_key)