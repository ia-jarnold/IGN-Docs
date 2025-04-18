======================
Ignition Documentation
======================

* :ref:`IA 8.3 Rest Api`
* :ref:`IA Knowledge Base`
* :ref:`IA User Manual`
* :ref:`IA Java Docs`

IA 8.3 Rest Api
===============

| Deployed to the /openapi endpoint of an 8.3 GW I believe.

IA Knowledge Base
=================

| Has many useful articles. again many are more targeted but some should be highlighted here.

* `IA Knowledge Base`_
* `IA KBA Loggers`_
* `IA KBA Websockets`_
* `IA KBA IDB Reference (8.1)`_

IA User Manual
==============

| The user manual is very helpful but very verbose. I reccomend linking directly to it in more targeted areas. But there will be some more General pages here.

* `IA UM 8.1 Version Updates`_
* `IA UM 8.1 Appendix`_

IA Java Docs
============

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

