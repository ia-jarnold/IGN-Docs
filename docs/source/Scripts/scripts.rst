#######
Scripts
#######

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
  
   .. code-block:: Bash
      
      # print .pem
      openssl x509 -in ~/share/jarnold_host/Downloads/.pem -text
      
      ## convert from pem to crt
      openssl x509 -outform der -in ~/share/jarnold_host/Downloads/.pem -out ./def_pem.crt

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

.. dropdown:: MSSQL TCP Port
   :color: info

   | This can also be found in comp management under like properties of sql server. Tcp needs to be enabled after install.

   .. code-block:: MSSQL

      USE master
      GO
      xp_readerrorlog 0, 1, N'Server is listening on'
      GO
