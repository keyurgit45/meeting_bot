from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time 
import webbrowser
import pyautogui

my_mail_id = None
my_password = None
chrome_driver_path = None
path_to_chrome_profile = None
profile = None
email_end_with = 'viit.ac.in'


def take_credentials(email, password):
    global my_mail_id, my_password, email_end_with
    my_mail_id = email
    my_password = password

def change_driver_path(path):
    global chrome_driver_path
    chrome_driver_path = path

def change_profile_path(path):
    global path_to_chrome_profile, profile
    # 'C:\\Users\\keyur\\AppData\\Local\\Google\\Chrome\\User Data\\Profile 1'
    data = path.split('\\')
    path_to_chrome_profile = '\\'.join(data[:-1])
    profile = data[-1]


def google_meet_with_gmail_login(meet_url):
    global my_mail_id, my_password, chrome_driver_path

    mail_address = my_mail_id
    password = my_password
    
    opt = webdriver.ChromeOptions() 
    opt.add_argument('--disable-blink-features=AutomationControlled') 
    opt.add_argument('--start-maximized') 
    opt.add_experimental_option("prefs", { 
	"profile.default_content_setting_values.media_stream_mic": 1, 
	"profile.default_content_setting_values.media_stream_camera": 1, 
	"profile.default_content_setting_values.geolocation": 0, 
	"profile.default_content_setting_values.notifications": 1
    })

    driver = webdriver.Chrome(executable_path=f"{chrome_driver_path}", options=opt)  
    driver.maximize_window()

    # going to Gmail Login Page
    driver.get('https://accounts.google.com/ServiceLogin?hl=en&passive=true&continue=https://www.google.com/&ec=GAZAAQ')

    # input Gmail 
    driver.find_element_by_id("identifierId").send_keys(mail_address) 
    driver.find_element_by_id("identifierNext").click() 
    driver.implicitly_wait(20) 
    
    # input Password 
    driver.find_element_by_xpath('//*[@id="password"]/div[1]/div/div[1]/input').send_keys(password) 
    driver.implicitly_wait(20) 
    driver.find_element_by_id("passwordNext").click() 
    driver.implicitly_wait(20)
    time.sleep(2)

    # going to google meet link
    driver.get(meet_url) 
    wait = WebDriverWait(driver, 20)    
    
    # turn off mic
    wait.until(EC.visibility_of_element_located((By.CLASS_NAME ,'sUZ4id' ))).click()
    driver.implicitly_wait(20)
    
    # turn off camera 
    driver.find_elements_by_class_name('sUZ4id')[1].click()
    driver.implicitly_wait(20) 
    

    #click on join button
    driver.find_element_by_css_selector('div.uArJ5e.UQuaGc.Y5sE8d.uyXBBb.xKiqt').click()
    input("press enter key to close the browser window")
    driver.quit()

def google_meet_with_profile(meet_url):

    global path_to_chrome_profile, chrome_driver_path, email_end_with
    
    options = webdriver.ChromeOptions() 
    options.add_argument(f"--user-data-dir={path_to_chrome_profile}") #Path to your chrome profile
    options.add_argument(f'--profile-directory={profile}') #give your profile
    driver = webdriver.Chrome(executable_path=f"{chrome_driver_path}", options=options)
    driver.maximize_window()
    time.sleep(3)
    

    # going to google meet link
    driver.get(meet_url) 
    wait = WebDriverWait(driver, 20)    
    
    # turn off mic
    wait.until(EC.visibility_of_element_located((By.CLASS_NAME ,'sUZ4id' ))).click()
    driver.implicitly_wait(10)
    
    # turn off camera 
    driver.find_elements_by_class_name('sUZ4id')[1].click()
    driver.implicitly_wait(10) 
    time.sleep(2)

    #click on join button
    emailid = driver.find_element_by_css_selector('div.ASy21.Duq0Bf')
    print(emailid.text)
    if not (emailid.text.endswith(email_end_with)):
        driver.quit()
        raise Exception("Wrong Email Exception")
    else:
        time.sleep(1)

        #click on join button
        driver.find_element_by_css_selector('div.uArJ5e.UQuaGc.Y5sE8d.uyXBBb.xKiqt').click()

        input("press enter key to close the browser window") 
        driver.quit()   


   
def google_meet(meeting_url):
    try:
        google_meet_with_profile(meeting_url)
    except Exception as e:
        print("Error Occured :",e)
        google_meet_with_gmail_login(meeting_url)
          

def google_meet_by_id(meeting_id):
    url = f"http://meet.google.com/{meeting_id}"
    google_meet(url)


def zoom(zoom_url):
   webbrowser.open(zoom_url)


def zoom_by_id(meeting_id, meeting_password):
    url = f"https://zoom.us/j/{meeting_id}"
    webbrowser.open(url)
    time.sleep(5)
    pyautogui.write(meeting_password)
