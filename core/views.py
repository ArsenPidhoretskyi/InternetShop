from django.views import View


class WithContextView(View):
    def __init__(self, **kwargs):
        super(WithContextView, self).__init__(**kwargs)
        self.context = dict()
