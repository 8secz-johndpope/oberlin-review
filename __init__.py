from django.contrib.comments import CommentForm
from captcha.fields import CaptchaField

def add_captcha(f):
    ''' This adds a "captcha" field to Django's default comment form.
    '''
    def wrapped(self, *args, **kwargs):
        f(self, *args, **kwargs)
        self.fields['security_code'] = CaptchaField()
    return wrapped
CommentForm.__init__ = add_captcha(CommentForm.__init__)
