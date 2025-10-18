from django import forms
from .models import Airport, add_next_airport

class AirportForm(forms.ModelForm):
    class Meta:
        model = Airport
        fields = ['code', 'left', 'right', 'left_distance', 'right_distance']

class AddNextAirportForm(forms.Form):
    parent_code = forms.CharField(max_length=10)
    direction = forms.ChoiceField(choices=[('left', 'Left'), ('right', 'Right')])
    child_code = forms.CharField(max_length=10)
    distance = forms.FloatField()

    def save(self):
        data = self.cleaned_data
        return add_next_airport(
            parent_code=data['parent_code'],
            direction=data['direction'],
            child_code=data['child_code'],
            distance=data['distance']
        )

class ShortestPathForm(forms.Form):
    start = forms.CharField(max_length=10)
    # end = forms.CharField(max_length=10)
