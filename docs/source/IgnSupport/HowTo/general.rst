=========================
Ignition General How To's
=========================

| I noticed that I get rusty when describing certain really normal actions in igntion on Responses so these should hold stock responses for those. I.E. Obtaining diagnotic reports....Status -> Overview. They also all contain slightly different assets and 8.3 will make them more accessable.
|
| Can use show source in sidebar to copy the text/md to zendesk. Use CTRL-SHIFT-V to paste MD. Notice I am not generating the md here but just writing it, it is since canned response anyway should not be very dynamic.
|
| Screenshots in docs have a tendancy to become stale and make things more confusing especially in complex apps. So I try to rely on more text base simple explanations. Standardize etc...

Pull Diagnostic Reports
=======================

| This should not talk about the context around why we grabbed them but simply how so that it gets communicated.

* :ign_zd_tickets:`148234`

1. Navigate to GW->Status->Overview
2. Download Diagnostic Report is in the bottom right of the page on 8.1.

Download Status Logs
====================

1. Navigate to GW->Status->Logs
2. There should be a Download Button below the paging arrows.

Take Gateway Backups
====================

| What Comes in the GW Backup

1. Project Configs
2. Wrapper Logs
3. SQLite IDB backup config not logs....
4. logback.xml configs
5. email-profiles
6. ignition.conf
7. Gateway.xml configs
8. Python deps.
9. Java third party db drivers
10. OPCUA configs.
11. Redundancy configs.
12. Tags....These can be extracted through kindling or by restoring the backup. I am still not sure if the 'internal impl details' are fully query-able in the idb file. It looked odd when I made a basic UDT etc on how things are combined but if have time will look again.

2. Thread Dumps
3. SQLite Logs for Status->Logs
4. Modules?...DATA Only...
 

| Response

1. Navigate to GW->Config->Backup.
2. Download backup.

Take Thread Dump 
================

1. Navigate to GW->Status->Threads
2. Near live values should be a button to download the thread dump. 

Share Resources
===============

| Attach it to the email reply. If to Large we can provide other file sharing solutions.

   1. Use dropbox build into zendesk if allowed.
   2. Add my <inductive email> us to a sharepoint so I can download the files there.
   3. Teams can facilitate file sharing through chat meetings. Members need to allow/accept permissions. Can't really say what teams will do unfortunatley so last resort.


