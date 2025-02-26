#######
Scripts
#######


.. button-link:: http://192.168.163.128:5000/source

   View Source

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


