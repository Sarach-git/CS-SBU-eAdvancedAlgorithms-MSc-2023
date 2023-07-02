from django.shortcuts import render

from diet.data.process import get_diet
from diet.forms import DietForm


def diet_form_view(request):
    diet = None

    if request.method == 'POST':
        form = DietForm(request.POST)
        if form.is_valid():
            diet = get_diet(
                form.cleaned_data.get("gender"),
                form.cleaned_data.get("weight"),
                form.cleaned_data.get("height"),
                form.cleaned_data.get("age"),
                form.cleaned_data.get("lifestyle"),
                form.cleaned_data.get("goal"),
                form.cleaned_data.get("pregnant"),
                form.cleaned_data.get("lactating"),
            )
    else:
        form = DietForm()

    return render(request, "diet_form.html", {
        "title": "Fitness Enthusiasts Diet",
        "form": form,
        "diet": diet,
    })
