from django import template
from bikes.cost_calculator import CostCalculator

register = template.Library()

# Filter for adding a css class to a Form field.
@register.filter(name="add_class")
def add_class(field, css):
    return field.as_widget(attrs={"class": css})


# Filter for adding an id to a Form field.
@register.filter(name="add_id")
def add_id(field, name):
    return field.as_widget(attrs={"id": name})

@register.filter(name="get_cost")
def get_cost(hire):
    return CostCalculator(hire).calculate_cost()[0]

@register.filter
def duration(td):
    total_seconds = int(td.total_seconds())
    hours = total_seconds // 3600
    minutes = (total_seconds % 3600) // 60

    if hours  == 0:
        return "{} mins".format(minutes)
    return '{} hours {} mins'.format(hours, minutes)