from django import forms


class NumberInputWithUnit(forms.NumberInput):
    def __init__(self, unit=None, *args, **kwargs):
        self.unit = unit
        super().__init__(*args, **kwargs)

    def get_context(self, name, value, attrs):
        context = super().get_context(name, value, attrs)
        context['widget']['unit'] = self.unit
        return context

    template_name = "number_with_unit.html"
