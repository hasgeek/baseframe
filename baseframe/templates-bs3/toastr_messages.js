{%- with messages = get_flashed_messages(with_categories=true) %}
  {%- if messages -%}
    {%- for category, message in messages %}
      {%- if category in ['error', 'info', 'success', 'warning'] %}
        toastr.{{ category }}({{ message|tojson|safe }});
      {%- else %}
        toastr.info({{ message|tojson|safe }});
      {%- endif %}
    {%- endfor %}
  {%- endif %}
{%- endwith %}
