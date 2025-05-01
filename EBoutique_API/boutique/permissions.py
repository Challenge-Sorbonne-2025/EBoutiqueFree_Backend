from django.contrib.auth.mixins import UserPassesTestMixin

class GestionnaireBoutiqueMixin(UserPassesTestMixin):
    def test_func(self):
        return (
            self.request.user.is_authenticated and 
            hasattr(self.request.user, 'boutique_geree')
        )
    
    def get_queryset(self):
        qs = super().get_queryset()
        if hasattr(self.request.user, 'boutique_geree'):
            return qs.filter(boutique=self.request.user.boutique_geree)
        return qs.none()