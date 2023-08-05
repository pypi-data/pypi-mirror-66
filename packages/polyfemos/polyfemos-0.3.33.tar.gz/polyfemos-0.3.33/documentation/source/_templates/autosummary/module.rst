
{{ fullname }}
{{ underline }}

.. currentmodule:: {{ fullname }}

.. automodule:: {{ fullname }}

   .. comment to end block

{% block functions %}

{% set public_functions = [] %}
{% set private_functions = [] %}
{% for m in all_functions %}
    {% if m in functions %}
        {% set a = public_functions.append(m) %}
    {% else %}
        {% set a = private_functions.append(m) %}
    {% endif %}
{%- endfor %}

{% if public_functions %}

.. rubric:: Public Functions

{% for item in public_functions %}
.. autofunction:: {{ item }}
{%- endfor %}

{% endif %}

{% if private_functions %}

.. rubric:: Private Functions

{% for item in private_functions %}
.. autofunction:: {{ item }}
{%- endfor %}
{% endif %}

{% endblock %}


{% block classes %}
{% if classes %}

.. rubric:: Classes

.. autosummary::
    :toctree: .
    {% for item in classes %}
    {{ item }}
    {%- endfor %}

{% endif %}
{% endblock %}



{% block exceptions %}
{% if exceptions %}
.. rubric:: Exceptions

{% for item in exceptions %}
    {{ item }}
{%- endfor %}

{% endif %}
{% endblock %}






