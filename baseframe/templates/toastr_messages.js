{%- with messages = get_flashed_messages(with_categories=true) %}
  {%- if messages -%}
    {%- for category, message in messages %}
      {%- if category in ['error', 'info', 'success', 'warning'] %}
        toastr.{{ category }}("{{ message }}");
      {%- else %}
        toastr.info("{{ message }}");
      {%- endif %}
    {%- endfor %}
  {%- endif %}
{%- endwith %}
