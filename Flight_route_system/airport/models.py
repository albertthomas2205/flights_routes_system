from django.db import models

# Create your models here.
from django.db import models

class Airport(models.Model):
    code = models.CharField(max_length=10, unique=True)
    left = models.ForeignKey('self', on_delete=models.SET_NULL, null=True, blank=True, related_name='left_airport')
    right = models.ForeignKey('self', on_delete=models.SET_NULL, null=True, blank=True, related_name='right_airport')
    left_distance = models.FloatField(null=True, blank=True)
    right_distance = models.FloatField(null=True, blank=True)
    
    def __str__(self):
        return self.code


def add_next_airport(parent_code, direction, child_code, distance):
    """
    Adds a left or right child to a parent airport.
    direction -> 'left' or 'right'
    """
    try:
        parent = Airport.objects.get(code=parent_code)
    except Airport.DoesNotExist:
        raise ValueError(f"Parent airport '{parent_code}' not found")

    child, _ = Airport.objects.get_or_create(code=child_code)

    if direction == 'left':
        parent.left = child
        parent.left_distance = distance
    elif direction == 'right':
        parent.right = child
        parent.right_distance = distance
    else:
        raise ValueError("Direction must be 'left' or 'right'")

    parent.save()
    print(f"Added {direction} node '{child_code}' to '{parent_code}'")
    return child
