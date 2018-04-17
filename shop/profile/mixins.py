from django.contrib.auth.mixins import AccessMixin
from django.http import Http404
from django.shortcuts import redirect


class NotLoginRequiredMixin(AccessMixin):
    def dispatch(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            return redirect('product_list')
        return super(NotLoginRequiredMixin, self).dispatch(request, *args, **kwargs)


# class UserValidMixin(AccessMixin):
#     def dispatch(self, request, *args, **kwargs):
#         # import pdb; pdb.set_trace()
#         if request.user.id != int(self.kwargs['pk']):
#             raise Http404
#         return super(UserValidMixin, self).dispatch(request, *args, **kwargs)
