from django import forms
from django.utils.translation import gettext_lazy as _

from diet import widgets
from diet import consts


class DietForm(forms.Form):
    gender = forms.ChoiceField(
        label=_("Gender"),
        choices=consts.GENDER_CHOICES,
        widget=forms.Select(
            attrs={
                "class": "form-select",
            },
        ),
    )

    pregnant = forms.BooleanField(
        required=False,
        label=_("Pregnant"),
    )

    lactating = forms.BooleanField(
        required=False,
        label=_("Lactating"),
    )

    weight = forms.IntegerField(
        label=_("Weight"),
        min_value=1,
        widget=widgets.NumberInputWithUnit(
            unit="kg",
            attrs={
                "class": "form-control",
            },
        ),
    )

    height = forms.IntegerField(
        label=_("Height"),
        min_value=1,
        widget=widgets.NumberInputWithUnit(
            unit="cm",
            attrs={
                "class": "form-control",
            },
        ),
    )

    age = forms.IntegerField(
        label=_("Age"),
        min_value=1,
        widget=widgets.NumberInputWithUnit(
            unit="years",
            attrs={
                "class": "form-control",
            },
        ),
    )

    lifestyle = forms.ChoiceField(
        label=_("Lifestyle"),
        choices=consts.LIFESTYLE_CHOICES,
        widget=forms.Select(
            attrs={
                "class": "form-select",
            },
        ),
    )

    goal = forms.ChoiceField(
        label=_("Goal"),
        choices=consts.GOAL_CHOICES,
        widget=forms.Select(
            attrs={
                "class": "form-select",
            },
        ),
    )

    def clean(self):
        cd = self.cleaned_data
        if cd.get('gender') == consts.GENDER_MALE:
            if cd.get('pregnant'):
                self.add_error('pregnant', _("A male cannot be pregnant."))
            if cd.get('lactating'):
                self.add_error('lactating', _("A male cannot be lactating."))
        return cd
