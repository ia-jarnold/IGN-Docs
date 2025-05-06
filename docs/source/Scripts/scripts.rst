#######
Scripts
#######

.. include:: ../Shared/actions.rst

Ignition
========

.. dropdown:: Auto Thread Dumps Vison based on connectivity 
   :color: info

   | I run this in a client timer script on an interval.

   .. code-block:: python

      # should verify the timer 1 sec may be to much but inline with Tag Group changes etc. Soft marker.
      import time
      import json
      
      # Type will depend on metric.
      CONNECT_TIMEOUT = 10000 # Calibrate me if necessary
      SOCKET_TIMEOUT = 10000 # Calibrate me if necessary
      METRIC_NAME = 'VisionClientConnectivityStatus' # depends on metric
      
      ts = system.date.now()
      ts_str = system.date.format(ts,"yy-MM-dd-HH-mm-ss")
      
      # you may have to test which root dir vision client can write too I beleive C:\ is fine since jre is installed under Program Files.
      try:
      	#https://www.docs.inductiveautomation.com/docs/8.1/appendix/scripting-functions/system-util/system-util-getGatewayStatus#code-examples
      	#gw_status = system.util.getGatewayStatus('http://ip:port', CONNECT_TIMEOUT, SOCKET_TIMEOUT)
      	gw_status = system.util.getGatewayStatus('http://IP:PORT/main') # CONFIGURE ME!!!!!!!!!!!!!!!!!!!!!!!!!!!!
      except:
      	METRIC_NAME = 'VisionFailedToConnect' #update Metric never made it.
      	threads_json = json.loads(system.util.threadDump().replace('\n',''))
       	with open('C:\%s-%s.json' % (METRIC_NAME, ts_str), 'w') as fp:
      		json.dump(threads_json, fp)
      	return # critial
      	
      if gw_status != 'RUNNING' # made it but bad...not as critical...
      
        threads_json = json.loads(system.util.threadDump().replace('\n',''))
      
        with open('C:\%s-%s.json' % (METRIC_NAME, ts_str), 'w') as fp:
                json.dump(threads_json, fp)
      
      else: # steady state can add other steady state collections here similarly.
        pass

      
.. dropdown:: Auto Thread Dumps based on Metrics
   :color: info

   | These Are put in tag change scripts and dpepenting on state will take thread dump. on/off or off/on etc...

   .. code-block:: python
      
      import time
      import json
      
      THRESHHOLD = 10 # Depends on metric.
      METRIC_NAME = 'QueriesPerSecond' # depends on metric
      
      ts = system.date.now()
      ts_str = system.date.format(ts,"yy-MM-dd-HH-mm-ss")
      
      if previousValue.value < THRESHHOLD and not currentValue.value >= THRESHHOLD: # Up
      	
      	threads_json = json.loads(system.util.threadDump().replace('\n',''))
      	
      	with open('C:\%s-%s.json' % (METRIC_NAME, ts_str), 'w') as fp:
      		json.dump(threads_json, fp, indent=4)
      		
      elif not previousValue.value >= THRESHHOLD and currentValue.value < THRESHHOLD: # Down
      	
      	threads_json = json.loads(system.util.threadDump().replace('\n',''))
      	
      	with open('C:\%s-%s.json' % (METRIC_NAME, ts_str), 'w') as fp:
      		json.dump(threads_json, fp, indent=4)
      		
      else: # steady state
      	pass


Shell
=====

.. dropdown:: Expose Ubuntu VM shares
   :color: info
  
   .. code-block:: Bash 

      # puts them under home share
      sudo vmhgfs-fuse ~/share/ -o allow_other -o uid=1000

      # I beleive this one places them in the host specified dir
      # like mnt...
      sudo vmhgfs-fuse .host:/ -o allow_other -o uid=1000

.. dropdown:: ldapsearch examples 
   :color: info
  
   .. code-block:: Bash

      ldapsearch -W -H ldap://10.10.65.22:389 -D 'cn=Jared Arnold,cn=Users,dc=testsupport,dc=local' -b 'dc=testsupport,dc=local'
      ldapsearch -W -H ldap://10.10.65.22:389 -D 'jarnold@testsupport.local' -b 'dc=testsupport,dc=local'

.. dropdown:: openssl examples 
   :color: info
 
   * `IA Lets Encrypt`_

   .. code-block:: Bash
      
      # print .pem
      openssl x509 -in ~/share/jarnold_host/Downloads/.pem -text
      
      ## convert from pem to crt
      openssl x509 -outform der -in ~/share/jarnold_host/Downloads/.pem -out ./def_pem.crt

      # convert a PFX(personal exchange format) used to exchange pub/priv objects to it's
      # private key and cert(public)
      openssl pkcs12 -in filename.pfx -nocerts -out key.pem # private...
      openssl pkcs12 -in filename.pfx -clcerts -nokeys -out cert.pem

.. dropdown:: tar examples
   :color: info

   .. code-block:: Bash

      # create tarball
      tar -czvf project.tar.gz project
      tar -cvf project.tar.gz project


      # extract tarball
      tar -xzvf project.tar.gz
      tar -xvf project.tar


      # list tarball (z arg) optional here I believe
      tar -tzvf project.tar.gz
      tar -tvf project.tar

.. dropdown:: Launch Kate
   :color: info

   Accidently installed this with flatpak pkmgr I guess....prob not necessary...but nice gui ide for working in rst files. Can have spellcheck and stuff.

   .. code-block:: Bash

      flatpak run org.kde.kate

SQL
===

.. dropdown:: MSSQL Express TCP Port
   :color: info

   | This can also be found in comp management under like properties of sql server. Tcp needs to be enabled after install.

   .. code-block:: SQL
     
      -- MSSQL
      USE master
      GO
      xp_readerrorlog 0, 1, N'Server is listening on'
      GO


Powershell
==========

.. dropdown:: Keytool 
   :color: info

   | Check client certs, sometimes customers use a reuse able CN making it hard to identify which cert goes where.

   .. code-block:: Powershell 
      
      $files = Get-ChildItem "C:\Users\jarnold\.ignition\clientlauncher-data\certificates\" -Filter \*.pem

      Set-location "C:\Program Files\Inductive Automation\Vision Client Launcher\jre\bin\"
      for ($i=0; $i -lt $files.Count; $i++) {
          $outfile = $files[$i].FullName
          echo ""
          echo "START"
          echo $outFile
          .\keytool.exe -printcert -file $outFile 
          echo "END"
          echo ""
      }


.. dropdown:: MSSQL Generate Scripts 
   :color: info

   * `SMO Scripting Options`_

   .. literalinclude:: mssql_generate_scripts.ps1
      :language: powershell

.. dropdown:: curl/Invoke-WebRequest 
   :color: info


   .. code-block:: Powershell 

      curl -Method PUT "http://localhost:9088/data/api/v1/projects/API Lesson" -Headers @{"Content-type"="application/json"} -Body '{"description":"hey"}' # body could be that IDictionary type maybe...@....

.. dropdown:: Tail Logs 
   :color: info


   .. code-block:: Powershell 

       Get-Content -Path "C:\Program Files\Inductive Automation\Ignition2\logs\wrapper.log" -Wait -Tail 100

