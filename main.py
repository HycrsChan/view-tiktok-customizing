# import undetected_chromedriver as uc
import platform, os, time, requests
from colorama import Fore
import selenium
from selenium.webdriver.chrome.options import Options as options
from selenium.webdriver.common.by import By
from interface.interface import interface
import sys

banner = """
Customizing by:

██╗░░██╗██╗░░░██╗░█████╗░██████╗░░██████╗░█████╗░██╗░░██╗░█████╗░███╗░░██╗
██║░░██║╚██╗░██╔╝██╔══██╗██╔══██╗██╔════╝██╔══██╗██║░░██║██╔══██╗████╗░██║
███████║░╚████╔╝░██║░░╚═╝██████╔╝╚█████╗░██║░░╚═╝███████║███████║██╔██╗██║
██╔══██║░░╚██╔╝░░██║░░██╗██╔══██╗░╚═══██╗██║░░██╗██╔══██║██╔══██║██║╚████║
██║░░██║░░░██║░░░╚█████╔╝██║░░██║██████╔╝╚█████╔╝██║░░██║██║░░██║██║░╚███║
╚═╝░░╚═╝░░░╚═╝░░░░╚════╝░╚═╝░░╚═╝╚═════╝░░╚════╝░╚═╝░░╚═╝╚═╝░░╚═╝╚═╝░░╚══╝ """

class holo:
    def __init__(self):
        self.show_process = False
        chrome_options = options()
        chrome_options.add_argument('--log-level=1')
        chrome_options.add_argument('--incognito')
        if '--show' in sys.argv:
            pass
        else:
            chrome_options.add_argument('--headless')
        
        self.driver = selenium.webdriver.Chrome(options=chrome_options)
        
        self.interface = interface()
        self.captcha_box = '/html/body/div[5]/div[2]/form/div/div'
        self.clear       = "clear"
        
        if platform.system() == "Windows":
            self.clear = "cls"
            
        self.color  = Fore.BLUE
        self.sent   = 0
        self.xpaths = {
            "followers"     : "/html/body/div[6]/div/div[2]/div/div/div[2]/div/button",
            "hearts"        : "/html/body/div[6]/div/div[2]/div/div/div[3]/div/button",
            "comment_hearts": "/html/body/div[6]/div/div[2]/div/div/div[4]/div/button",
            "views"         : "/html/body/div[6]/div/div[2]/div/div/div[6]/div/button",
            "shares"        : "/html/body/div[6]/div/div[2]/div/div/div[7]/div/button",
            "favorites"     : "/html/body/div[6]/div/div[2]/div/div/div[8]/div/button",
        }
        self.choice = 0
        self.input  = ""
        self.input_comment = ""
        self.limit  = 0
        
            
    def main(self):
        try: 
            os.system(self.clear)
            self.interface.change_title("TikTok Booster")
            
            print(self.color + banner)
            print("\n" + self.interface._print("Ko bật VPN"))
            
            self.driver.get("https://zefoy.com")
            self.wait_for_xpath(self.captcha_box)
            
            print(self.interface._print("Giari Captcha"))
            
            self.solve_captcha()
            
            # self.wait_for_xpath(self.xpaths["followers"])
            os.system(self.clear)
            status = self.check_status()
            
            print(self.color + banner)
            print()
            print(self.interface._print(f"nhập lựa chọn mà bạn muốn." + "\n"))
            
            counter = 1
            for thing in status:
                print(self.interface._print(f"{thing} {status[thing]}", counter))
                counter += 1
            
            print(f" {Fore.WHITE}[{self.color}7{Fore.WHITE}] Set Limit")
            
            option = int(input("\n" + self.interface._print(f"")))
            
            self.user_choice(option)
            
        except Exception as e:
            self.driver.quit()
            time.sleep(3)
            os._exit(1)

    def send_bot(self, search_button, main_xpath, vid_info, div):
        try:            
            element = self.driver.find_element('xpath', main_xpath)
            element.clear()
            element.send_keys(vid_info)
            time.sleep(6)

            find_start = f"/html/body/div[{div}]/div/div/*"
            if not self.driver.find_elements("xpath", find_start):
                self.driver.find_element("xpath", search_button).click()
                time.sleep(5)

            ratelimit_seconds, full = self.check_submit(div)
            if "(s)" in str(full):
                self.main_sleep(ratelimit_seconds)
                self.driver.find_element('xpath', search_button).click()
                time.sleep(5)

            send_button = f'/html/body/div[{div}]/div/div/div[1]/div/form/button'
            button = self.driver.find_element('xpath', send_button)
            count_text = button.text
            button.click()
            self.sent += 1
            print(self.interface._print(f"[ {self.sent} ] | Số lượt xem : {count_text}"))

            time.sleep(3)
            count_textv = count_text.replace(',', '')
            self.check_limit(int(count_textv))
            self.send_bot(search_button, main_xpath, vid_info, div)

        except Exception:
            self.driver.refresh()
            self.wait_for_user(self.xpaths["followers"])
            time.sleep(5)
            self.user_choice(self.choice)
            
    def send_comment(self, search_button, main_xpath, vid_info, cmt_info, div):
        try:            
            element = self.driver.find_element('xpath', main_xpath)
            element.clear()
            element.send_keys(vid_info)
            time.sleep(6)

            find_start = f"/html/body/div[{div}]/div/div/*"
            if not self.driver.find_elements("xpath", find_start):
                self.driver.find_element("xpath", search_button).click()
                time.sleep(5)

            ratelimit_seconds, full = self.check_submit(div)
            if "(s)" in str(full):
                self.main_sleep(ratelimit_seconds)
                self.driver.find_element('xpath', search_button).click()
                time.sleep(5)
                
            send_button = f'/html/body/div[{div}]/div/div/div[1]/div/form/button'
            buttonSearch = self.driver.find_element('xpath', send_button)
            buttonSearch.click()
            
            time.sleep(5)
            
            input_value = cmt_info
            self.driver.execute_script(f"document.querySelector('#c2VuZC9mb2xsb3dlcnNfdGlrdG9r > form > ul > li > div > input[type=hidden]:nth-child(5)').value = '{input_value}';")
            
            button = self.driver.find_element(By.XPATH, '//*[@id="c2VuZC9mb2xsb3dlcnNfdGlrdG9r"]/form/ul/li/div/button')
            # button = self.driver.find_element(By.CSS_SELECTOR, "#c2VuZC9mb2xsb3dlcnNfdGlrdG9r > form:nth-child(2) > ul > li > div > button")
            count_text = button.text
            button.click()
            self.sent += 1
            print(self.interface._print(f"[ {self.sent} ] | Số lượt xem: {count_text}"))

            time.sleep(3)
            count_textv = count_text.replace(',', '')
            self.check_limit(int(count_textv))
            self.send_comment(search_button, main_xpath, vid_info, div)

        except Exception:
            self.driver.refresh()
            self.wait_for_user(self.xpaths["followers"])
            time.sleep(5)
            self.user_choice(self.choice)

    def main_sleep(self, delay):
        while delay != 0:
            time.sleep(1)
            delay -= 1
            self.interface.change_title(f"TikTok Zefoy Automator | Cooldown: {delay}s | Github: @hycrschan")

    def convert(self, min, sec):
        seconds = 0
        
        if min != 0:
            answer = int(min) * 60
            seconds += answer
        
        seconds += int(sec) + 5
        return seconds

    def check_submit(self, div):
        remaining = f"/html/body/div[{div}]/div/div/span[1]"
        
        try:
            element = self.driver.find_element("xpath", remaining)
        except:
            return None, None
        
        if "READY" in element.text:
            return True, True
        
        if "seconds for your next submit" in element.text:
            output          = element.text.split("Please wait ")[1].split(" for")[0]
            minutes         = element.text.split("Please wait ")[1].split(" ")[0]
            seconds         = element.text.split("(s) ")[1].split(" ")[0]
            sleep_duration  = self.convert(minutes, seconds)
            
            return sleep_duration, output
        
        return element.text, None
        
    def check_status(self):
        statuses = {}
        
        for thing, value in self.xpaths.items():
            value = self.xpaths[thing]
            element = self.driver.find_element('xpath', value)
            
            if not element.is_enabled():
                statuses[thing] = f"{Fore.RED}[OFFLINE]"
            
            else:
                statuses[thing] = f"{Fore.GREEN}[WORKS]"
        
        return statuses

    

    def wait_for_xpath(self, xpath):
        while True:
            try:
                f = self.driver.find_element('xpath', xpath)
                return True
            except selenium.common.exceptions.NoSuchElementException:
                pass
            
    def wait_for_user(self, xpath):
        print(self.interface._print("Đang tiến hành giải captcha"))
        while True:
            try:
                time.sleep(3)
                f = self.driver.find_element('xpath', xpath)
                return True
            except selenium.common.exceptions.NoSuchElementException:
                self.solve_captcha()
            
    def user_choice(self, option):
        if option == 1:
            div = "7"
            self.choice = 1
            self.driver.find_element("xpath", self.xpaths["followers"]).click()
        
        elif option == 2:
            div = "8"
            self.choice = 2
            self.driver.find_element("xpath", self.xpaths["hearts"]).click()
            
        elif option == 3:
            div = "9"
            self.choice = 3
            self.driver.find_element("xpath", self.xpaths["comment_hearts"]).click()
            
        elif option == 4: 
            div = "10"
            self.choice = 4
            self.driver.find_element("xpath", self.xpaths["views"]).click()
            
        elif option == 5:
            div = "11"
            self.choice = 5
            self.driver.find_element("xpath", self.xpaths["shares"]).click()
            
        elif option == 6:
            div = "12"
            self.choice = 6
            self.driver.find_element("xpath", self.xpaths["favorites"]).click()
            
        elif option == 7:
            self.limit = input("\n" + self.interface._print("Enter limit: "))
            os.system(self.clear)
            status = self.check_status()
            
            print(self.color + banner)
            print()
            print(self.interface._print(f"Nhập lựa chọn mà bạn muốn" + "\n"))
            print('Limit: ' + self.limit)
            
            counter = 1
            for thing in status:
                print(self.interface._print(f"{thing} {status[thing]}", counter))
                counter += 1
            
            option = int(input("\n" + self.interface._print(f"")))
            
            self.user_choice(option)
        
        else:
            self.driver.quit()
            os._exit(1)
            
        video_url_box = f'/html/body/div[{div}]/div/form/div/input'
        search_box    = f'/html/body/div[{div}]/div/form/div/div/button'
        vid_info = self.input if self.input else input("\n" + self.interface._print("Username/VideoURL: "))
        self.input = vid_info
        
        if self.choice == 3:
            cmt_info = self.input_comment if self.input_comment else input("\n" + self.interface._print("Comment-id: "))
            self.input_comment = cmt_info
            self.send_comment(search_box, video_url_box, vid_info, cmt_info, div)
        else:
            self.send_bot(search_box, video_url_box, vid_info, div)
        
    def check_limit(self, limit):
        if int(self.limit) > 0 and limit >= int(self.limit):
            print(f"Limit is reached. Limit: {self.limit}")
            self.driver.quit()
            os._exit(1)
            
    def get_captcha(self):
        try:
            time.sleep(5)
            image_element = self.driver.find_element(By.CSS_SELECTOR, "body > div.noscriptcheck > div.ua-check > form > div > div > img")
            image_element.screenshot("image.png")
            ocr_result = self.ocr_from_image("./image.png")
            self.interface._print("Captcha: " + ocr_result["ParsedResults"][0]["ParsedText"])
            time.sleep(3)
            return ocr_result["ParsedResults"][0]["ParsedText"]
        
        except Exception as e:
            print(e)
            
    def ocr_from_image(self, image_path):
        try:
            url = "https://api.ocr.space/parse/image"
            payload = {
            "language": "eng",
            "isOverlayRequired": False,
            "scale": True,
            "isTable": False,
            "filetype": "png"
            }
            headers = {
                "apikey": "K87899142388957", #this api key is not mine lol
            }

            with open(image_path, "rb") as image_file:
                files = {
                    "file": image_file
                }
                response = requests.post(url, data=payload, headers=headers, files=files)

            if response.status_code == 200:
                return response.json()
            else:
                return None

        except Exception as e:
            print(e)
            
    def solve_captcha(self):
        try:
            print(self.interface._print("Solving CAPTCHA..."))
            
            captcha = self.get_captcha()
            
            captcha_input = self.driver.find_element(By.CSS_SELECTOR, "body > div.noscriptcheck > div.ua-check > form > div > div > div > input")

            captcha_input.send_keys(captcha)
        
        except Exception as e:
            print(e)

if __name__ == "__main__":
    try:
        obj = holo()
        if '--url' in sys.argv:
            url_index = sys.argv.index('--url')
            obj.input = sys.argv[url_index + 1]
        
        if '--comment' in sys.argv:
            comment_index = sys.argv.index('--comment')
            obj.input_comment = sys.argv[comment_index + 1]
            
        if '--limit' in sys.argv:
            limit_index = sys.argv.index('--limit')
            obj.limit = sys.argv[limit_index + 1]
        
        obj.main()
    except Exception as e:
        print("\n" + str(e))
        input("\nclick enter để thoát")
        os._exit(1)