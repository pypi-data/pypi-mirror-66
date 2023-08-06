from dataclasses import asdict
from typing import Any, Dict, List, Optional, Union, cast

import httpx

from ..client import AuthenticatedClient, Client
from ..errors import ApiResponseError

{% for relative in collection.relative_imports %}
{{ relative }}
{% endfor %}
{% for endpoint in collection.endpoints %}


def {{ endpoint.name | snakecase }}(
    *,
    {# Proper client based on whether or not the endpoint requires authentication #}
    {% if endpoint.requires_security %}
    client: AuthenticatedClient,
    {% else %}
    client: Client,
    {% endif %}
    {# path parameters #}
    {% for parameter in endpoint.path_parameters %}
    {{ parameter.to_string() }},
    {% endfor %}
    {# Form data if any #}
    {% if endpoint.form_body_reference %}
    form_data: {{ endpoint.form_body_reference.class_name }},
    {% endif %}
    {# JSON body if any #}
    {% if endpoint.json_body %}
    json_body: {{ endpoint.json_body.get_type_string() }},
    {% endif %}
    {# query parameters #}
    {% for parameter in endpoint.query_parameters %}
    {{ parameter.to_string() }},
    {% endfor %}
) -> Union[
    {% for response in endpoint.responses %}
    {{ response.return_string() }},
    {% endfor %}
]:
    """ {{ endpoint.description }} """
    url = "{}{{ endpoint.path }}".format(
        client.base_url
        {%- for parameter in endpoint.path_parameters -%}
        ,{{parameter.name}}={{parameter.python_name}}
        {%- endfor -%}
    )

    {% if endpoint.query_parameters %}
    params = {
        {% for parameter in endpoint.query_parameters %}
        {% if parameter.required %}
            "{{ parameter.name }}": {{ parameter.transform() }},
        {% endif %}
        {% endfor %}
    }
    {% for parameter in endpoint.query_parameters %}
    {% if not parameter.required %}
    if {{ parameter.python_name }} is not None:
        params["{{ parameter.name }}"] = str({{ parameter.transform() }})
    {% endif %}
    {% endfor %}
    {% endif %}

    response = httpx.{{ endpoint.method }}(
        url=url,
        headers=client.get_headers(),
        {% if endpoint.form_body_reference %}
        data=asdict(form_data),
        {% endif %}
        {% if endpoint.json_body %}
        json={{ endpoint.json_body.transform() }},
        {% endif %}
        {% if endpoint.query_parameters %}
        params=params,
        {% endif %}
    )

    {% for response in endpoint.responses %}
    if response.status_code == {{ response.status_code }}:
        return {{ response.constructor() }}
    {% endfor %}
    else:
        raise ApiResponseError(response=response)
{% endfor %}
