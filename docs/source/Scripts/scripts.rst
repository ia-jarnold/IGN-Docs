#######
Scripts
#######

.. include:: ../Shared/actions.rst

Ignition Scripts
================

Vision Scripts
--------------

| Client Scope

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

Gateway Scripts
---------------

| Gateway Scope

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
      
      if previousValue.value < THRESHHOLD and currentValue.value >= THRESHHOLD: # Up
      	
      	threads_json = json.loads(system.util.threadDump().replace('\n',''))
      	
      	with open('C:\%s-%s.json' % (METRIC_NAME, ts_str), 'w') as fp:
      		json.dump(threads_json, fp, indent=4)
      		
      elif not previousValue.value >= THRESHHOLD and currentValue.value < THRESHHOLD: # Down
      	
      	threads_json = json.loads(system.util.threadDump().replace('\n',''))
      	
      	with open('C:\%s-%s.json' % (METRIC_NAME, ts_str), 'w') as fp:
      		json.dump(threads_json, fp, indent=4)
      		
      else: # steady state
      	pass

Selenium Scripts
================

* `Selenium Locating Elements`_
* `Selenium Login Example`_
* `Python Multiprocessing Library`_
* `Python Multithreading Examples`_

.. dropdown:: Selenium with Async 
   :color: info

   | The below script runs all sessions async on a single thread but the above threading libraries help can manange/scale this. cron/docker/scheduled tasks/background tasks also work.

   .. literalinclude:: selenium_async.py 
      :language: python 

.. dropdown:: Selenium with Proxy 
   :color: info
 
   | sort of experiment ....

   .. code-block:: python
      
      from selenium import webdriver
      from selenium.webdriver.support.ui import WebDriverWait
      from selenium.webdriver.common.by import By
      import asyncio
      import time
      import uuid
      
      
      
      NUM_SESSIONS = 1
      USE_PROXY = True 
      
      cService = webdriver.ChromeService(executable_path=u"C:/Users/jarnold/chromedriver-win64/136/chromedriver-win64/chromedriver.exe")
      driver = webdriver.Chrome(service = cService)
      def get_free_proxies(driver):
      
          driver.get('https://sslproxies.org')
      
          table = driver.find_element(By.TAG_NAME, 'table')
          thead = table.find_element(By.TAG_NAME, 'thead').find_elements(By.TAG_NAME, 'th')
          tbody = table.find_element(By.TAG_NAME, 'tbody').find_elements(By.TAG_NAME, 'tr')
      
          headers = []
          for th in thead:
              headers.append(th.text.strip())
      
          proxies = []
          for tr in tbody:
              proxy_data = {}
              tds = tr.find_elements(By.TAG_NAME, 'td')
              for i in range(len(headers)):
                  proxy_data[headers[i]] = tds[i].text.strip()
              proxies.append(proxy_data)
          return proxies
      
      
      free_proxies = get_free_proxies(driver)
      
      #print(free_proxies)
      
      proxy_list = []
      for proxy in free_proxies:
          proxy_list.append("%s:%s" % (proxy['IP Address'], proxy['Port']))
        
      print(proxy_list)
      
      async def run_session(use_proxy=False, proxy_list=None):
      
          username = "***"
          password = "****"
         
          session_id = uuid.uuid4()
      
          print("Session ID: %s" % session_id) 
      
          if use_proxy and proxy_list is not None:
      
              for proxy in proxy_list:
      
                  try:
      
                      cService = webdriver.ChromeService(executable_path=u"C:/Users/jarnold/chromedriver-win64/136/chromedriver-win64/chromedriver.exe")
                      options = webdriver.ChromeOptions() 
                      options.add_argument('--proxy-server=%s' % proxy)
                      driver = webdriver.Chrome(service = cService, options = options )
                      driver.set_window_size(340, 695) # set a mobile window size.
      
                  except Exception as e:
                      print('Error creating driver proxy %s' % proxy)
                      print(str(e))
      
      
                  try:
                      driver.get("url to root page of app")
                      print('%s using %s proxy' % (session_id, proxy))
                      break
                  except Exception as e:
                      print('Error creating opening app %s' % proxy)
                      print(str(e))
      
          else:
      
              try:
                  cService = webdriver.ChromeService(executable_path=u"C:/Users/jarnold/chromedriver-win64/136/chromedriver-win64/chromedriver.exe")
                  driver = webdriver.Chrome(service = cService)
                  driver.set_window_size(340, 695) # set a mobile window size.
              except:
                  print('error creating driver')
      
              try:
                  driver.get("************url to root page*************")
              except:
                     print('Error creating opening app %s' % proxy)
      
          await asyncio.sleep(0) # try to minimize
      
           # ############################## LOGIN ####################
          # continue screen
          try:
            continue_screen = driver.find_element(By.CLASS_NAME, "button-message")
            continue_screen.click()
            await asyncio.sleep(0) # try to minimize
          except:
              print('Could not find continue button splash')
       
       
          # Log in screen
          try:
              login_box = driver.find_element(By.XPATH, '//\*[@id="login-panel-content"]/div/div[2]/div[2]/div/input')
              login_box.send_keys(username)
              login_button = driver.find_element(By.XPATH,'//\*[@id="login-panel-content"]/div/div[3]/span')
              login_button.click()
              await asyncio.sleep(0) # try to minimize
          except:
              print('could not find login')
      
          try:
              login_pass = driver.find_element(By.XPATH,'//\*[@id="login-panel-content"]/div/div[2]/div[3]/div[2]/input')
              login_pass.send_keys(password)
              login_button.click()
              await asyncio.sleep(10) # try to minimize
          except:
              print('could not find pass')
      
           # ##############################  APP NAVIGATION ####################
          # HOME Loads Possibly wait for seesion initilization.
          await asyncio.sleep(0)
      
          # navigate to nearby me
          try:
      
              nearby_tab = driver.find_element(By.XPATH, '//\*[@id="app-container"]/div/div[2]/div[2]/div[2]/div[1]/div/div[2]/div[2]')
              nearby_tab.click()
              await asyncio.sleep(4)
          except:
              print('could not navigate')
      
          # near by tabs back and fourth. can add more...
          # basically tmeplated
          #'//\*[@id="app-container"]/div/div[2]/div[2]/div[2]/div[1]/div/div[1]/div[2]/div[1]/div/div[2]/div[2]/div[INDEX]/div'
          try: # kristens testing
              nearby_row = driver.find_element(By.XPATH, '//\*[@id="app-container"]/div/div[2]/div[2]/div[2]/div[1]/div/div[1]/div[2]/div[1]/div/div[2]/div[2]/div[1]/div')
              await asyncio.sleep(4)
              nearby_row.click()
              await asyncio.sleep(4)
              back = driver.find_element(By.CSS_SELECTOR, '[data-component-path="R[1].0:0:0:0:0"]')
              back.click() 
              await asyncio.sleep(4)
          except:
              print('could not find near by row')
      
          try: # revloution byte
              nearby_row = driver.find_element(By.XPATH, '//\*[@id="app-container"]/div/div[2]/div[2]/div[2]/div[1]/div/div[1]/div[2]/div[1]/div/div[2]/div[2]/div[3]/div')
              await asyncio.sleep(4)
              nearby_row.click()
              await asyncio.sleep(4)
              back = driver.find_element(By.CSS_SELECTOR, '[data-component-path="R[1].0:0:0:0:0"]')
              back.click() 
              await asyncio.sleep(4)
          except:
              print('could not find near by row')
      
          # navigate back to explore
          try:
      
              explore = driver.find_element(By.XPATH, '//\*[@id="app-container"]/div/div[2]/div[2]/div[2]/div[1]/div/div[2]/div[3]')
              explore.click()
              await asyncio.sleep(10) # observe map goodness.
      
          except:
              print('could not navigate to explore')
      
          # navigate back to home
          try:
              #'//\*[@id="app-container"]/div/div[2]/div[2]/div[2]/div[1]/div/div[1]/div[2]/div[2]/div/div[2]/div[2]/div[*******]' posts spec looks like we can use data components also they are in a lot of divs...
              hrm = driver.find_element(By.XPATH, '//\*[@id="app-container"]/div/div[2]/div[2]/div[2]/div[1]/div/div[2]/div[1]')
              hrm.click()
              await asyncio.sleep(4) # observe map goodness.
              hrm_posts = driver.find_element(By.XPATH,'//\*[@id="app-container"]/div/div[2]/div[2]/div[2]/div[1]/div/div[1]/div[2]/div[2]/div/div[2]/div[2]/div[1]')
              hrm_posts.click()
              await asyncio.sleep(4) # observe map goodness.
              back = driver.find_element(By.CSS_SELECTOR, '[data-component-path="R[0].0:0:0"]')
              back.click()
              await asyncio.sleep(4) # observe map goodness.
              hrm_posts = driver.find_element(By.XPATH,'//\*[@id="app-container"]/div/div[2]/div[2]/div[2]/div[1]/div/div[1]/div[2]/div[2]/div/div[2]/div[2]/div[2]')
              hrm_posts.click()
              await asyncio.sleep(4) # observe map goodness.
              back = driver.find_element(By.CSS_SELECTOR, '[data-component-path="R[0].0:0:0"]')
              back.click()
              await asyncio.sleep(20) # observe map goodness.
      
      
          except:
              print('could not navigate to home')
      
      
          try:
              header_dropdown = driver.find_element(By.CSS_SELECTOR,'[data-component-path="C$0:0$0:0:1$0:0.0:4"]')
              header_dropdown.click()
              await asyncio.sleep(2) # try to lk
              logout_button = driver.find_element(By.XPATH,'//\*[@id="popup-user-details"]/div/div/div/button')
              logout_button.click()
              await asyncio.sleep(10) # try to minimize
          except:
              print('could not find logout/header')
      
          await asyncio.sleep(1) # try to minimize
      
      
      ############################################## TEARDOWN ############################################
      
          try:
            driver.quit()
          except:
              print('driver failed to close or was closed prematurly')
      
      async def main():
      
          tasks = []
          for i in range(0, NUM_SESSIONS):
              tasks.append( asyncio.create_task(run_session(USE_PROXY, proxy_list)) )
      
          await asyncio.gather(\*tasks)
      
      
      asyncio.run(main()) 

      


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

