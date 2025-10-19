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



# class AirportSearchForm(forms.Form):
#     CHOICES = [
#         ('nth_node', 'Find Nth Left/Right Node'),
#         ('longest_route', 'Find Longest Route'),
#         ('duration_between', 'Find Duration Between Two Airports'),
#     ]

#     search_type = forms.ChoiceField(choices=CHOICES, label="Select Search Type")

#     # Fields for different types of searches
#     start = forms.CharField(required=False, label="Start Airport Code")
#     direction = forms.ChoiceField(choices=[('left', 'Left'), ('right', 'Right')], required=False)
#     n = forms.IntegerField(required=False, min_value=1, label="N (Step Count)")

#     from_airport = forms.CharField(required=False, label="From Airport Code")
#     to_airport = forms.CharField(required=False, label="To Airport Code")


from django import forms

class NthNodeForm(forms.Form):
    start = forms.CharField(label="Start Airport Code")
    direction = forms.ChoiceField(choices=[('left', 'Left'), ('right', 'Right')], label="Direction")
    n = forms.IntegerField(min_value=1, label="N (Step Count)")

class DurationForm(forms.Form):
    from_airport = forms.CharField(label="From Airport Code")
    to_airport = forms.CharField(label="To Airport Code")
