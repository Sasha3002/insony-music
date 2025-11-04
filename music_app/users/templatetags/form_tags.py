from django import template

register = template.Library()

@register.filter(name="add_class")
def add_class(field, css):
    return field.as_widget(attrs={"class": css})

@register.inclusion_tag("partials/bs_field.html")
def bs_field(field, placeholder="", label=None):
    base_class = "form-control"
    attrs = {"class": base_class}

    if placeholder:
        attrs["placeholder"] = placeholder

    if field.errors:
        attrs["class"] = f"{attrs['class']} is-invalid"

    widget_html = field.as_widget(attrs=attrs)

    return {
        "field": field,
        "label": label or field.label,
        "widget": widget_html,  
    }
