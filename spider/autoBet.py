import time


from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.common.action_chains import ActionChains
from undetected_chromedriver.webelement import WebElement


def login(wait: WebDriverWait, email: str, password: str):
    apertar_botao(wait, ".hm-MainHeaderRHSLoggedOutWide_Login ")
    time.sleep(10)
    preencher_campo(wait, ".lms-StandardLogin_Username ", email)
    time.sleep(10)
    preencher_campo(wait, ".lms-StandardLogin_Password ", password)
    apertar_botao(wait, ".lms-LoginButton_Text ")


def apertar_botao(wait: WebDriverWait, selector: str):
    btn = wait.until(EC.element_to_be_clickable(
        (By.CSS_SELECTOR, selector)
    ))
    click(btn)


def esperar_sumir(wait: WebDriverWait, selector: str):
    wait.until(EC.invisibility_of_element(
        (By.CSS_SELECTOR, selector)))


def esperar_sumir_xpath(wait: WebDriverWait, selector: str):
    wait.until(EC.invisibility_of_element(
        (By.XPATH, selector)))


def preencher_campo(wait: WebDriverWait, selector: str, valor: str):
    wait.until(EC.presence_of_element_located(
        (By.CSS_SELECTOR, selector))
    ).clear()

    wait.until(EC.presence_of_element_located(
        (By.CSS_SELECTOR, selector))
    ).send_keys(valor)


def inList(A, B):
    ret = []
    for i in A:
        if A == "FC" or A == "United":
            continue
        if i in B:
            ret.append(i)
    if len(ret) > 0:
        return True
    return False


class BetBot:
    def __init__(self):
        import undetected_chromedriver as uc
        # browser = uc.Chrome()

        options = uc.ChromeOptions()
        options.user_data_dir = "c:\\temp\\profile"
        options.add_argument('--user-data-dir=c:\\temp\\profile2')
        options.add_argument('--no-first-run --no-service-autorun --password-store=basic')
        browser = uc.Chrome(options=options)
        # from selenium import webdriver
        # browser = webdriver.Firefox()

        self.driver = browser
        self.wait = WebDriverWait(self.driver, 60)
        self.fast = WebDriverWait(self.driver, 5)
        self.normal = WebDriverWait(self.driver, 20)
        self.driver.delete_all_cookies()
        self.driver.maximize_window()

    def login(self):
        # self.driver.get("https://www.188-sb.com")
        self.driver.get("https://www.365-288.com")

        try:
            time.sleep(10)
            esperar_sumir(self.wait, ".bl-Preloader_MainHeader")
            login(self.wait, "zealot666", "qw8146657#")
            time.sleep(30)

            print("return main")
            from selenium.webdriver.common.action_chains import ActionChains
            ActionChains(self.driver).click().perform()
        except Exception as ex:
            print("return main")

        try:
            self.driver.get('http://www.baidu.com/')
            return True
        except:
            print("login error")
            return False

    def goBetList(self):
        try:
            # self.driver.get("https://www.188-sb.com")
            self.driver.get("https://www.365-288.com")
            try:
                flagList = True
                retryTime = 20
                time.sleep(10)
                while (retryTime > 0 and flagList):
                    try:
                        print(retryTime)
                        button = self.driver.find_element(by=By.CLASS_NAME,
                                                          value="hm-MainHeaderCentreWide :nth-child(2)")
                        click(button)
                        flagList = False
                    except Exception as ex:
                        print(ex)
                        retryTime -= 1
                        time.sleep(1)

                time.sleep(10)

                flagList = True
                retryTime = 20
                while (retryTime > 0 and flagList):
                    try:
                        button = self.driver.find_elements(by=By.CLASS_NAME,
                                                           value="ovm-ClassificationMarketSwitcherMenu_Item ")

                        ActionChains(self.driver).move_to_element(button[3]).click(button[3]).perform()
                        flagList = False
                    except:
                        retryTime -= 1
                        time.sleep(1)

                time.sleep(10)
            except Exception as ex:
                print("go main and click", ex)
            print("go end")
            try:
                self.driver.find_element(by=By.CLASS_NAME,
                                         value='hm-MainHeaderRHSLoggedOutWide_Login ')
                login(self.fast, "zealot666", "qw8146657#")
                time.sleep(15)
            except Exception as ex:
                print("login 2", ex)
            return True
        except Exception as ex:
            print("goBetList error", ex)
            return False

    def bet(self, zhuDui, keDui, num):
        ok = 0
        try:
            self.driver.find_element(by=By.CLASS_NAME,
                                     value='hm-MainHeaderRHSLoggedOutWide_Login ')
            login(self.fast, "zealot666", "qw8146657#")
            time.sleep(15)
        except Exception:
            print("login 2")

        try:
            try:
                self.driver.find_element(by=By.CLASS_NAME,
                                         value='lbs-DefaultContent ').click()
                time.sleep(1)
                removeAll = self.driver.find_element(by=By.CLASS_NAME,
                                                     value='lbl-ControlBar_RemoveAll ')
                removeAll.click()
            except:
                print("no dis play")

            try:
                self.driver.find_element(by=By.CLASS_NAME,
                                         value='bss-NormalBetItem_Remove').click()
            except:
                print("no dis play22")

            s = self.driver.find_elements(by=By.CLASS_NAME,
                                          value='ovm-Fixture_Container')

            for i in s:
                zhuDui2 = i.text.split('\n')[0].split(" ")
                keDui2 = i.text.split('\n')[1].split(" ")
                zhuDui3 = zhuDui.split(" ")
                keDui3 = keDui.split(" ")
                if inList(zhuDui2, zhuDui3) and inList(keDui2, keDui3):
                    try:
                        print("HorizontalMarket_Participants ")
                        time.sleep(4)
                        odds = i.find_element(by=By.CLASS_NAME,
                                              value='ovm-HorizontalMarket_Participants').find_elements(by=By.TAG_NAME,
                                                                                                       value='div')
                        odds[0].click()
                    except Exception as ex:
                        print("HorizontalMarket_Participants error", ex)

                    time.sleep(6)

                    try:
                        picture_url = self.driver.save_screenshot('.\\error ' + zhuDui + "1.png")
                        print("%s ：截图成功！！！" % picture_url)
                    except BaseException as msg:
                        print("%s ：截图失败！！！" % msg)

                    try:
                        print("lqb-BetPlacement ")
                        self.driver.find_element(by=By.CLASS_NAME,
                                                 value="lqb-StakeBox_StakeInput ").send_keys(num)
                        time.sleep(0.2)
                        button = self.driver.find_element(by=By.CLASS_NAME,
                                                          value="lqb-BetPlacement ")
                        from selenium.webdriver import ActionChains
                        ActionChains(self.driver).move_to_element(button).click(button).perform()
                        ok += 1
                    except Exception as ex:
                        print("lqb-BetPlacement error", ex)

                    try:
                        print("lqb-AcceptButton_PlaceBet ")
                        self.driver.find_element(by=By.CLASS_NAME,
                                                 value="lqb-StakeBox_StakeInput ").send_keys(num)
                        time.sleep(0.2)
                        button = self.driver.find_element(by=By.CLASS_NAME,
                                                          value="lqb-AcceptButton_PlaceBet ").click()
                        from selenium.webdriver import ActionChains
                        ActionChains(self.driver).move_to_element(button).click(button).perform()
                        ok += 1
                    except Exception as ex:
                        print("lqb-AcceptButton_PlaceBet error", ex)

                    try:
                        print("bsf-StakeBox_StakeInput ")
                        self.driver.find_element(by=By.CLASS_NAME,
                                                 value="bsf-StakeBox_StakeInput ").send_keys(num)
                        time.sleep(0.2)
                        button = self.driver.find_element(by=By.CLASS_NAME,
                                                          value="bsf-AcceptButton ").click()
                        from selenium.webdriver import ActionChains
                        ActionChains(self.driver).move_to_element(button).click(button).perform()
                        ok += 1
                    except Exception as ex:
                        print("bsf-StakeBox_StakeInput error", ex)

                    try:
                        print("bsf-StakeBox_StakeInput 2")
                        self.driver.find_element(by=By.CLASS_NAME,
                                                 value="bsf-StakeBox_StakeInput ").send_keys(num)
                        time.sleep(0.2)
                        button = self.driver.find_element(by=By.CLASS_NAME,
                                                          value="bsf-PlaceBetButton ").click()
                        from selenium.webdriver import ActionChains
                        ActionChains(self.driver).move_to_element(button).click(button).perform()
                        ok += 1
                    except Exception as ex:
                        print("bsf-StakeBox_StakeInput 2 error", ex)

                    try:
                        picture_url = self.driver.save_screenshot('.\\error ' + zhuDui + "2.png")
                        print("%s ：截图成功！！！" % picture_url)
                    except BaseException as msg:
                        print("%s ：截图失败！！！" % msg)

                    time.sleep(10)

                    try:
                        print("return")
                        from selenium.webdriver.common.action_chains import ActionChains
                        ActionChains(self.driver).click().perform()
                    except Exception as ex:
                        print("return error")

                    return ok
            return 1
        except Exception as ex:
            try:
                picture_url = self.driver.save_screenshot('.\\error ' + zhuDui + "3.png")
                print("%s ：截图成功！！！" % picture_url)
            except BaseException as msg:
                print("%s ：截图失败！！！" % msg)
            print("bet unknown error", ex)
            return 0

    def close(self):
        self.driver.quit()

    def quit(self):
        self.driver.get('http://www.baidu.com/')


def mouse_move(x, y):
    win32api.SetCursorPos([x, y])


def mouse_click(click_type="left"):
    if click_type == "left":
        win32api.mouse_event(win32con.MOUSEEVENTF_LEFTUP | win32con.MOUSEEVENTF_LEFTDOWN, 0, 0, 0, 0)
    else:
        win32api.mouse_event(win32con.MOUSEEVENTF_RIGHTUP | win32con.MOUSEEVENTF_RIGHTDOWN, 0, 0, 0, 0)
    time.sleep(0.01)


def click(e: WebElement):
    loca = e.location
    # mouse_move(loca.get("x"), loca.get("y") + 80)
    # mouse_click()

    # mouse_move(loca.get("x"), loca.get("y") + 50)
    # mouse_click()
    e.click()


if __name__ == '__main__':
    import ddddocr
    import time
    import zmq

    ocr = ddddocr.DdddOcr()
    context = zmq.Context()
    socket = context.socket(zmq.REP)
    socket.bind("tcp://*:12344")

    while True:
        message = socket.recv()
        print(message.decode('utf-8', 'ignore'))
        with open(message.decode('utf-8', 'ignore'), 'rb') as f:
            img_bytes = f.read()
        start = time.time()
        res = ocr.classification(img_bytes)
        end = time.time()
        print(res, end - start)
        socket.send(res.encode('utf-8'))
