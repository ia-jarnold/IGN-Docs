=========
Webserver
=========

| Ignition makes heavy usage of a webserver.

 * It intersects with Clients(persective vision)
 * It intersects with GAN.
 * It provies http as well as websocket connections depending on what it is servicing.

   * Tag changes.
   * dynamic prop updates etc.
   * Will verify these.

HSTS
====

| Webserver security feature.

  * Very integrated with browser.
  * `HSTS Spec`_
  * `HSTS Why and How Guide`_ -- will outline more specifics of the protocol to cross reference with ignition configs.

| Still identifying ignition requirements relative to our initial hardening guide mention.

  * `IA Hardening Guide`_
