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

| The user manual is very helpful but very verbose. I recommend linking directly to it in more targeted areas. But there will be some more General pages here.

* `IA UM 8.1 Version Updates`_
* `IA UM 8.1 Appendix`_

IA Site 
=======

| The IA site provides articles for various scaling, hardening, deployment  best practices and procedures. They should be understood in context that Ignition can come in a lot of variations that may not make them acurate but foundational(directional)(bounds that we can ~verify/expect to work and build from).

* `IA Downloads`_ -- Ignition Downloads. Has archived versions and third-party modules.
* `IA 8.1 Deployment Best Practices`_
* `IA Hardening Guide`_
* `IA Server Sizing and Arch Guide`_


IA Java Docs
============

| I have not found the base url for 7.9/8.3 yet.

{% for item in ign_versions %}
  {% if item == "8.1" %}
    {% for sitem in ign_versions[item] %}
      {% if item  == "8.1" %}
* :ign_java_doc_8.1:`{{ sitem }}`
      {% endif %}
    {% endfor %}
  {% endif %}
{% endfor %}

