

class ContextExtraViewMixin:
    context_extra = {}

    def get_context_data(self, **kwargs):
        context = {}
        if hasattr(super(),'get_context_data'):
            context = super().get_context_data(**kwargs)
        context.update(self.context_extra)
        return context


