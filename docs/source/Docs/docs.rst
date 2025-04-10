=============
Documentation
=============

Java Docs
=========

{% for item in ign_versions %}
* {{ item }}
  {% for sitem in ign_versions[item] %}
    {% if item  == "8.1" %}
    * :ign_java_doc_8.1:`{{ sitem }}`
    {% else %}
    * `IA_JAVA_API_{{ sitem }}`_
    {% endif %}
  {% endfor %}
{% endfor %}
