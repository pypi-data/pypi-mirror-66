
{{ fullname }}
{{ underline }}

.. currentmodule:: {{ module }}

.. autoclass:: {{ objname }}
    :show-inheritance:

    {% block methods %}

    {% set public_methods = [] %}
    {% set private_methods = [] %}
    {% set special_methods = [] %}
    {% for m in all_methods if not m in inherited_members %}
    {% if m in methods or m == "__init__" %}
    {% set a = public_methods.append(m) %}
    {% elif m.startswith('__') %}
    {% set a = special_methods.append(m) %}
    {% else %}
    {% set a = private_methods.append(m) %}
    {% endif %}
    {%- endfor %}

    {% if (public_methods|count) > 0 %}
    .. rubric:: Public Methods

    {% for m in public_methods %}
    .. automethod:: {{ m }}
    {%- endfor %}
    {% endif %}


    {% if (private_methods|count) > 0 %}
    .. rubric:: Private Methods

    {% for m in private_methods %}
    .. automethod:: {{ m }}
    {%- endfor %}
    {% endif %}

    {% if (special_methods|count) > 0 %}
    .. rubric:: Special Methods

    {% for m in special_methods %}
    .. automethod:: {{ m }}
    {%- endfor %}
    {% endif %}

    {% endblock %}


|
