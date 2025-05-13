from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait # may be better then timers in actual nav...
from selenium.webdriver.common.by import By

import asyncio
import time
import uuid

###############################################################################################
# 
# await asyncio.sleep(0) # * triggers next move in next session  so lots of sessions got
#                           through there routines quickly every move has some wait time 
#                           that must be considered a move is like a find click rerender.
#                           or maybe like a couple navs on a page per session...
#                         * selenium has built in 'WebDriverWait' that I believes does 
#                           them implicitly also
#                         * may execute session moves out of order have not seen yet
# await asyncio.sleep(4) # * I believe wait's 4 secs before next move in next session 
#                            each session goes thorugh this routine +sec I believe in order.
# time.sleep            # this will block event loop and all moves on seesion that use it
#                       # have to finish before next can go. could be useful
#
# As sessions increase one may be more realistic then the other at certain time.
#
# This is still a single python thread so won't see to much randomness since all doing 
# the thesame thing at same time.
# 
# However start to add maybe 'multithreading' lib on top or launch the python processes 
# across docker container could see more random behavior
# 'mutihreading' lib is usually based on available cores or was...
#
# Launch sessions when other have made it past certain areas 4 past login check launch 4 more.
# that will look more random too. at some point though the nav will be pretty syncronous.
#
# then have to maybe launch 500 sessions to get 300 active at same time....tradeoffs
##############################################################################################

NUM_SESSIONS = 20
ALL_HEADLESS = True # if False will run first as non-headless for testing etc...

async def run_session( headless=True ):

    username = "qa-test"
    password = "iggyLovesIgnition"
  
    # can pull these from the webdriver obj as well pretty sure.
    session_id = uuid.uuid4()
    print("Session ID: %s" % session_id)

    try:

        options = webdriver.ChromeOptions()
        if headless:
            options.headless = options.add_argument("--headless=new")
       
        # newer selenium tries to handle this but have not use it yet now the requirements
        # here just find the driver for you chrome. Check in Chrome->settings->about...135/136/137...etc
        cService = webdriver.ChromeService(executable_path=u"C:/Users/jarnold/chromedriver-win64/136/chromedriver-win64/chromedriver.exe")
        driver   = webdriver.Chrome(service = cService, options = options)

    except Exception as e:

        print('error creating driver')
        print(str(e))

    try:

        driver.set_window_size(340, 695) # set a mobile window size.
        driver.get("https://everywhere.inductiveautomation.com/")

    except: 
        print('Error creating opening app/sizing')

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
        login_box = driver.find_element(By.XPATH, '//*[@id="login-panel-content"]/div/div[2]/div[2]/div/input')
        login_box.send_keys(username)
        login_button = driver.find_element(By.XPATH,'//*[@id="login-panel-content"]/div/div[3]/span')
        login_button.click()
        await asyncio.sleep(0) # try to minimize
    except:
        print('could not find login')

    try:
        login_pass = driver.find_element(By.XPATH,'//*[@id="login-panel-content"]/div/div[2]/div[3]/div[2]/input')
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

        nearby_tab = driver.find_element(By.XPATH, '//*[@id="app-container"]/div/div[2]/div[2]/div[2]/div[1]/div/div[2]/div[2]')
        nearby_tab.click()
        await asyncio.sleep(4)
    except:
        print('could not navigate')

    # near by tabs back and fourth. can add more...
    # basically tmeplated
    #'//*[@id="app-container"]/div/div[2]/div[2]/div[2]/div[1]/div/div[1]/div[2]/div[1]/div/div[2]/div[2]/div[******]/div'
    try: # kristens testing
        nearby_row = driver.find_element(By.XPATH, '//*[@id="app-container"]/div/div[2]/div[2]/div[2]/div[1]/div/div[1]/div[2]/div[1]/div/div[2]/div[2]/div[1]/div')
        nearby_row.click()
        await asyncio.sleep(4)
    except:
        print('Could not find row')

    try:
        back = driver.find_element(By.CSS_SELECTOR, '[data-component-path="R[2].0:0:0:0:0"]')
        back.click() 
        await asyncio.sleep(4)
    except:
        print('could not find back arrow')

    try: # revloution byte
        nearby_row = driver.find_element(By.XPATH, '//*[@id="app-container"]/div/div[2]/div[2]/div[2]/div[1]/div/div[1]/div[2]/div[1]/div/div[2]/div[2]/div[3]/div')
        nearby_row.click()
        await asyncio.sleep(4)
    except:
        print('could not find row')

    try:
        back = driver.find_element(By.CSS_SELECTOR, '[data-component-path="R[2].0:0:0:0:0"]')
        back.click() 
        await asyncio.sleep(4)
    except:
        print('could not find back button')

    # navigate back to explore
    try:

        explore = driver.find_element(By.XPATH, '//*[@id="app-container"]/div/div[2]/div[2]/div[2]/div[1]/div/div[2]/div[3]')
        explore.click()
        await asyncio.sleep(10) # observe map goodness.

    except:
        print('could not navigate to explore')

    # navigate back to home
    try:
        #'//*[@id="app-container"]/div/div[2]/div[2]/div[2]/div[1]/div/div[1]/div[2]/div[2]/div/div[2]/div[2]/div[*******]' posts spec looks like we can use data components also they are in a lot of divs...
        hrm = driver.find_element(By.XPATH, '//*[@id="app-container"]/div/div[2]/div[2]/div[2]/div[1]/div/div[2]/div[1]')
        hrm.click()
        await asyncio.sleep(4) # observe map goodness.
        hrm_posts = driver.find_element(By.XPATH,'//*[@id="app-container"]/div/div[2]/div[2]/div[2]/div[1]/div/div[1]/div[2]/div[2]/div/div[2]/div[2]/div[1]')
        hrm_posts.click()
        await asyncio.sleep(4) # observe map goodness.
        back = driver.find_element(By.CSS_SELECTOR, '[data-component-path="R[0].0:0:0"]')
        back.click()
        await asyncio.sleep(4) # observe map goodness.
        hrm_posts = driver.find_element(By.XPATH,'//*[@id="app-container"]/div/div[2]/div[2]/div[2]/div[1]/div/div[1]/div[2]/div[2]/div/div[2]/div[2]/div[2]')
        hrm_posts.click()
        await asyncio.sleep(4) # observe map goodness.
        back = driver.find_element(By.CSS_SELECTOR, '[data-component-path="R[0].0:0:0"]')
        back.click()
        await asyncio.sleep(20) # observe map goodness.


    except:
        print('could not navigate to home or find homescreen elements')

    try:
        header_dropdown = driver.find_element(By.CSS_SELECTOR,'[data-component-path="C$0:0$0:0:1$0:0.0:4"]')
        header_dropdown.click()
        await asyncio.sleep(2) # try to lk
        logout_button = driver.find_element(By.XPATH,'//*[@id="popup-user-details"]/div/div/div/button')
        logout_button.click()
        await asyncio.sleep(10) # try to minimize
    except:
        print('could not find logout/header or find logout/header elements')

    await asyncio.sleep(1) # try to minimize

############################################## TEARDOWN ############################################

    try:
        driver.quit()
        print('Session id %s has logged out and driver exited successfully' % session_id)
    except:
        print('Driver failed to close or was closed prematurly')

async def main():

    tasks = []
    for i in range(0, NUM_SESSIONS):
        if i == 0:
            tasks.append( asyncio.create_task(run_session(headless=SINGLE_NON_HEADLESS)) )
        else:
            tasks.append( asyncio.create_task(run_session()) )

    await asyncio.gather(*tasks)


asyncio.run(main())
