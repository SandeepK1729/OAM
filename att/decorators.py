from functools import wraps
from django.shortcuts import redirect

# faculty login required 
def faculty_login_required(func, REDIRECT_URL = 'home'):
    @wraps(func)
    def wrap(request, *args, **kwargs):
        if request.user.user_type in ['faculty', 'admin']:
            return func(request, *args, **kwargs)
        return redirect(REDIRECT_URL)
    return wrap
    

