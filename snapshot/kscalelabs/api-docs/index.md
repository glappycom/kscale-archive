# KOS API Documentation

Documentation for PyKOS, KOS-Sim, and KOS-SDK.

## PyKOS

{% for file in site.static_files %}
  {% if file.path contains '/pykos/' and file.extname == '.html' %}
* [{{ file.name | remove: '.html' | capitalize | replace: '_', ' ' }}]({{ file.path | relative_url }}) - {{ file.name | remove: '.html' }} service client
  {% endif %}
{% endfor %}

## KOS-Sim

{% for file in site.static_files %}
  {% if file.path contains '/kos_sim/' and file.extname == '.html' %}
* [{{ file.name | remove: '.html' | capitalize | replace: '_', ' ' }}]({{ file.path | relative_url }}) - {{ file.name | remove: '.html' | capitalize }} documentation
  {% endif %}
{% endfor %}

## KOS-SDK

{% for file in site.static_files %}
  {% if file.path contains '/kos-sdk/' and file.extname == '.html' %}
* [{{ file.name | remove: '.html' | capitalize | replace: '_', ' ' }}]({{ file.path | relative_url }}) - {{ file.name | remove: '.html' | capitalize }} documentation
  {% endif %}
{% endfor %}