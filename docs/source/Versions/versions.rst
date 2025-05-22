=================
Ignition Versions
=================

| More of and example of templating.

{% for item in ign_versions %}
* {{item}}
  {% for sitem in ign_versions[item] %}
 * {{ sitem }}
  {% endfor %}
{% endfor %}
