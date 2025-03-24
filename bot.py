import telebot
import time
import traceback

from webdriver_manager.chrome import ChromeDriverManager
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.webdriver.common.by import By
import undetected_chromedriver as uc

# Возможные значения текущего состояния бота (ввод ВИНа, номера узла и т.д.)
# STATE_START
# STATE_CHOOSE_SITE
# STATE_INPUT_VIN
# STATE_INPUT_CATEGORY
# STATE_INPUT_SUBCATEGORY
# STATE_INPUT_UZEL
state = "STATE_START"
site = -1
vin = ""
WAIT_S = 3  # Время ожидания в с. между переходами по страницам
categories_html = None
sub_categories_html = None
uzly_html = None

# токен бота
bot = telebot.TeleBot("7933183762:AAGTvsP7MRhClxpBJbcObfKhsgPzuiMAbjc")

d = {
    "FUEL & ENGINE CONTROL": "Управление топливной системой и двигателем",
    "POWER TRAIN SYSTEM": "Силовой агрегат",
    "BODY HANGON PARTS": "Части кузова",
    "INTERIOR & EXTERIOR": "Интерьер и экстерьер",
    "ELECTRICAL EQUIPMENTS": "Электрическое оборудование",
    "O.V.M TOOL & ACCESSORY": "Инструменты и аксессуары",
    "ACCELERATOR CONTROL": "Педаль газа",
    "ENGINE MOUNTING": "Крепление двигателя",
    "ENGINE": "Двигатель",
    "CHASSIS": "Шасси",
    "SIDE & REAR BODY": "Боковой и задний кузов",
    "BODY MOUNTING": "Крепление к кузову",
    "INSULATOR-BODY NO3 UPR": "Изолятор-корпус № 3 UPR",
    "WASHER & TUBE ASSY-BODY MTG NO3": "Шайба и трубка в сборе-корпус MTG № 3",
    "INSULATOR-BODY NO4 UPR": "Изолятор-корпус № 4 UPR",
    "WASHER & TUBE ASSY-BODY MTG NO4": "Шайба и трубка в сборе-корпус MTG № 4",
    "WASHER & TUBE ASSY-BODY NO5": "Шайба и трубка в сборе-корпус №5",
    "INSULATOR-BODY NO1 UPR": "Изолятор-корпус № 1 UPR",
    "INSULATOR-BODY LWR": "Корпус изолятора LWR",
    "INSULATOR-BODY NO2 UPR": "Изолятор-корпус № 2 UPR",
    "BODY-ELECTRIC THROTTLE": "Корпус-электрический дроссель",
    "BODY": "Кузов",
    "NUT": "Гайка",
    "SHORT BLOCK": "Короткий блок",
    "ENGINE UNIT": "Блок двигателя",
    "CYLINDER BLOCK": "Блок цилиндров",
    "CRANKSHAFT & FLYWHEEL": "Коленчатый вал и маховик",
    "CYLINDER HEAD & GASKET KIT": "Головка блока цилиндра и комплект прокладок",
    "CYLINDER HEAD COVER & CAMSHAFT": "Крышка головки блока цилиндров и распределительный вал",
    "CHAIN DRIVE(GSL)": "Цепной привод(GSL)",
    "CHAIN DRIVE": "Цепной привод",
    "TIMING CASE": "Корпус ГРМ",
    "BELT SYSTEM": "Ременная система",
    "ENGINE WIRING": "Электропроводка двигателя",
    "SENSORS": "Датчики",
    "ALTERNATOR": "Генератор переменного тока",
    "ALTERNATOR MOUNTING": "Монтаж генератора переменного тока",
    "STARTING MOTOR": "Пусковой двигатель",
    "EMISSION MODULE": "Модуль излучения",
    "COOLING SYSTEM(OM600,D20,D27)": "Сиситема охлаждения(OM600,D20,D27)",
    "COOLING SYSTEM(E23)": "Сиситема охлаждения(E23)",
    "OIL PAN & PUMP": "Масляный поддон и насос",
    "OIL FILTER": "Масляный фильтр",
    "VACUUM PUMP": "Вакуумный насос",
    "INTAKE MANIFOLD": "Впускной коллектор",
    "EXHAUST MANIFOLD": "Выпускной коллектор",
    "E.G.R VALVE(D20)": "Клапан E.G.R(D20)",
    "E.G.R VALVE(D27)": "Клапан E.G.R(D27)",
    "COMMON RAIL SYSTEM(D20)": "Аккумуляторная топливная система(D20)",
    "COMMON RAIL SYSTEM(D27)": "Аккумуляторная топливная система(D27)",
    "TURBOCHARGER": "Турбонагнетатель",
    "ROOF PANEL": "Панель крыши",
    "FRONT FLOOR PANEL": "Передняя панель пола",
    "REAR FLOOR PANEL": "Задняя панель пола",
    "FRONT END PANEL": "Передняя торцевая панель",
    "FENDER & APRON PANEL": "Панель крыла и фартука",
    "DASH PANEL & COWL": "Приборная панель и капот",
    "WASHER": "Мойка",
    "BOLT": "Болты",
    "PUMP ASSY-FUEL": "Насос в сборе-топливный",
    "BRKT-FUEL PUMP": "BRKT-топливный насос",
    "SPROCKET-HP PUMP": "Насос высокой мощности",
    "HOUSING ASSY-BEARING": "Корпус в сборе-подшибник",
    "NUT-GEAR MTG NO1": "Гайка-шестерня MTG NO1",
    "INJECTOR ASSY-FUEL": "Инжектор в сборе-топливный",
    "CLAMP": "Зажим",
    "VALVE ASSY-INLET METERING": "Клапан в сборе-дозатор на входе",
    "RUBBER-FUEL PIPE SUPT": "Резиновый топливопровод, поддерживающий",
    "PIPE ASSY-FUEL": "Труба в сборе-топливная",
    "CAPS KIT-PROTECTOR": "Комплект защитных колпачков",
    "TUBE ASSY-FUEL RETURN": "Трубка в сборе-возврат топлива",
    "RAIL ASSY-FUEL": "Рельс в сборое-топливный",
    "GASKET-FUEL PUMP": "Прокладка топливного насоса",
    "BRKT-FUEL PIPE UPR": "BRKT-топлипровод UPR",
    "BRKT ASSY-FUEL PIPE": "BRKT в сборе-топливопровод",
    "GROMMET": "Прокладка",
    "BUSH": "Втулка",
    "BRKT-ACOUSTIC COVER SIDE FRT": "BRKT-акустическая накладку сбоку FRT",
    "MANIFOLD ASSY-INTAKE": "Впускной коллектор в сборе",
    "BRKT-ACOUSTIC COVER SIDE RR": "BRKT-акустическая накладк сбоку RR",
    "COVER ASSY-ACOUSTIC": "Крышка в сборе-акустическая"

}
def translate(text):
    for en, ru in d.items():
        if en in text:
            return ru
    return "" # Если текст text есть в словаре d, возвращаем перевод, иначе пустая строка

@bot.message_handler(content_types=['text'])
def main(message):
    global driver
    global state
    global vin
    global site
    global categories_html
    global sub_categories_html
    global uzly_html

    try:
        if message.text in ["/start", "Найти автозапчасть"]:
            site = -1
            state = "STATE_START"
            vin = ""
        elif message.text in [str(x) for x in list(range(1, 51))]:
            pass
        elif message.text == "/help":
            site = -1
            state = "STATE_START"
            vin = ""
            bot.send_message(message.from_user.id, "Напиши /start")
            return

        # - selenium в python - браузер, который запускается по командам из питона, и мы можем получить информацию о результатах работы
        # - выборка элементов через XPATH
        # - для одного из сайтов нужна авторизация, тоже с использованием селениума

        if state == "STATE_START":
            bot.send_message(message.from_user.id, "Введите цифру для получения информации с одного из сайтов (1 - auto3n.ru, 2 - autodoc.ru): ")
            state = "STATE_CHOOSE_SITE"
            return

        if state == "STATE_CHOOSE_SITE":
            site = int(message.text)
            if site in (1, 2):
                bot.send_message(message.from_user.id, "Введите vin (например, Z8NTANZ51DS021829): ")
                state = "STATE_INPUT_VIN"
                return
            else:
                bot.send_message(message.from_user.id, "Укажите номер из списка")
                return

        print(state)
        if site == 1:
            if state == "STATE_INPUT_VIN":
                vin = message.text

                url = f"https://auto3n.ru"
                print(f"Сайт: {url}")

                driver.get(
                    f"https://auto3n.ru/?ident_string={vin}&option=com_guayaquil&task=vehicles.view&ft=findVehicle&c=")
                time.sleep(WAIT_S * 2)  # Время на ввод капчи + загрузку

                # Нажимаем на "Схемы узлов", если эта кнопка есть
                try:
                    show_uzly_html = driver.find_element(by=By.XPATH, value="//a[contains(text(), 'Схемы узлов')]")
                    show_uzly_html.click()
                    time.sleep(WAIT_S)
                except NoSuchElementException:
                    pass # Если не найден, ничего не делаем

                categories_html = driver.find_elements(by=By.XPATH, value="//ul[@class='groups-tree']//li")
                categories = []
                for category in categories_html:
                    # print(category)
                    categories.append(dict(
                        name=category.text
                    ))

                if len(categories) == 0:
                    bot.send_message(message.from_user.id, "Нет доступных категорий")
                    return

                s = ["Выберите категорию:"]
                for i, category in enumerate(categories, start=1):
                    s.append(f"{i}. {category['name']}") # ({translate(category['name'])})")
                bot.send_message(message.from_user.id, "\n".join(s))

                state = "STATE_INPUT_CATEGORY"
                print(f"NEW STATE = {state}, USER_INPUT = {message.text}")

            elif state == "STATE_INPUT_CATEGORY":
                q = int(message.text) - 1
                if not(0 <= q < len(categories_html)):
                    bot.send_message(message.from_user.id, "Укажите номер из списка")
                    return

                categories_html[q].click()
                time.sleep(WAIT_S)

                # Выбор подкатегории
                sub_categories_html = driver.find_elements(by=By.XPATH, value="//ul[contains(@class, 'schemes-list')]//li")
                sub_categories = []
                for sub_category in sub_categories_html:
                    # print(sub_category)
                    sub_categories.append(dict(
                        name=sub_category.text
                    ))

                if len(sub_categories) == 0:
                    bot.send_message(message.from_user.id, "Нет доступных подкатегорий")
                    return

                s = ["Выберите подкатегорию:"]
                for i, sub_category in enumerate(sub_categories, start=1):
                    s.append(f"{i}. {sub_category['name']}") # ({translate(sub_category['name'])})")
                bot.send_message(message.from_user.id, "\n".join(s))

                state = "STATE_INPUT_SUBCATEGORY"
                print(f"NEW STATE = {state}, USER_INPUT = {message.text}")

            elif state == "STATE_INPUT_SUBCATEGORY":
                q = int(message.text) - 1
                if not(0 <= q < len(sub_categories_html)):
                    bot.send_message(message.from_user.id, "Укажите номер из списка")
                    return

                sub_categories_html[q].click()
                time.sleep(WAIT_S)

                # Выбор узла
                uzly_html = driver.find_elements(by=By.XPATH,
                                                 value="//div[contains(@class, 'guayaquil-unit-detail') and contains(@class, 'flex-column')]")
                uzly = []
                for uzel in uzly_html:
                    uzly.append(dict(
                        name=uzel.text
                    ))

                if len(uzly) == 0:
                    bot.send_message(message.from_user.id, "Нет доступных узлов")
                    return

                s = ["Выберите узел:"]
                for i, uzel in enumerate(uzly, start=1):
                    s.append(f"{i}. {uzel['name']}") #  ({translate(uzel['name'])})")
                bot.send_message(message.from_user.id, "\n".join(s))

                state = "STATE_INPUT_UZEL"
                print(f"NEW STATE = {state}, USER_INPUT = {message.text}")

            elif state == "STATE_INPUT_UZEL":
                q = int(message.text) - 1
                if not(0 <= q < len(uzly_html)):
                    bot.send_message(message.from_user.id, "Укажите номер из списка")
                    return

                element = driver.find_elements(by=By.XPATH,
                                               value="//div[contains(@class, 'guayaquil-unit-detail') and contains(@class, 'flex-column')]//a")[
                    q]
                element.click()
                time.sleep(WAIT_S * 2)
                if len(driver.window_handles) > 1:
                    driver.switch_to.window(driver.window_handles[1])  # Предложения открываются в новой вкладке

                    # Выводим детали
                    if "временно нет в наличии" in driver.page_source:
                        bot.send_message(message.from_user.id, "Выбранный узел недоступен к продаже (отсутствует)")
                    else:
                        offers = []
                        elements = driver.find_elements(by=By.XPATH,
                                                        value="//div[contains(@class, 'group-wrapper')]//div[contains(@class, 'flex') and contains(@class, 'flex-column')]")
                        i = 0
                        for i in range(len(elements)):
                            text = elements[i].text.strip()
                            if "шт." in text:
                                offers.append(dict(count=int(text.replace("шт.", ""))))
                            if "₽" in text:
                                offers[-1]["price"] = float(text.split()[0].replace("₽.", ""))

                        if len(offers) > 0:
                            s = ["Доступны следующие предложения:"]
                            for i, offer in enumerate(sorted(offers, key=lambda x: x['price']), start=1):
                                s.append(f"{i}. {offer['count']} шт. по {offer['price']} ₽.")
                            bot.send_message(message.from_user.id, "\n".join(s))
                        else:
                            bot.send_message(message.from_user.id, "Выбранный узел недоступен к продаже (отсутствует)")
                else:
                    bot.send_message(message.from_user.id, "Ошибка при получении информации об узле")

                state = "STATE_START"
                print(f"NEW STATE = {state}, USER_INPUT = {message.text}")
            else:
                print("UNKNOWN STATE")

        elif site == 2:
            if state == "STATE_INPUT_VIN":
                vin = message.text

                url = f"https://www.autodoc.ru"
                print(f"Сайт: {url}")

                # Авторизация
                driver.get(f"https://www.autodoc.ru/")
                time.sleep(WAIT_S)  # Время на ввод капчи + загрузку

                # На следующем этапе может потребоваться ввода логина и пароля
                try:
                    button = driver.find_element(by=By.XPATH, value='//*[@id="loginInfo"]/div/a')
                    button.click()
                    time.sleep(WAIT_S)  # Время на открытие окна для ввода логина и пароля
                    edtLogin = driver.find_element(by=By.XPATH, value='//*[@id="Login"]')
                    edtLogin.send_keys('KUN-34755')
                    edtPassword = driver.find_element(by=By.XPATH, value='//*[@id="Password"]')
                    edtPassword.send_keys('58B3B965')
                    button = driver.find_element(by=By.XPATH, value='//*[@id="submit_logon_page"]')
                    button.click()
                    time.sleep(WAIT_S)  # Время на ввод капчи + загрузку
                except NoSuchElementException:
                    pass # Если не найден, ничего не делаем

                driver.get(f"https://www.autodoc.ru/catalogs/original/list-nodes/nodes?vin={vin}")
                time.sleep(WAIT_S * 2)  # Время на ввод капчи + загрузку

                # Нажимаем на "Категории", если эта кнопка есть
                try:
                    show_uzly_html = driver.find_element(by=By.XPATH, value="//a[text()='Категории']")
                    show_uzly_html.click()
                    time.sleep(WAIT_S)
                except NoSuchElementException:
                    pass # Если не найден, ничего не делаем

                categories_html = driver.find_elements(by=By.XPATH, value="//a[contains(@class, 'tree-link')]")
                categories = []
                for category in categories_html:
                    # print(category)
                    categories.append(dict(
                        name=category.text
                    ))

                if len(categories) == 0:
                    bot.send_message(message.from_user.id, "Нет доступных категорий")
                    return

                s = ["Выберите категорию:"]
                for i, category in enumerate(categories, start=1):
                    s.append(f"{i}. {category['name']}") #  ({translate(category['name'])})")
                bot.send_message(message.from_user.id, "\n".join(s))

                state = "STATE_INPUT_CATEGORY"
                print(f"NEW STATE = {state}, USER_INPUT = {message.text}")

            elif state == "STATE_INPUT_CATEGORY":
                q = int(message.text) - 1
                if not(0 <= q < len(categories_html)):
                    bot.send_message(message.from_user.id, "Укажите номер из списка")
                    return

                categories_html[q].click()
                time.sleep(WAIT_S)

                # Выбор подкатегории
                sub_categories_html = driver.find_elements(by=By.XPATH, value="//a[contains(@class, 'uzel')]")
                sub_categories = []
                for sub_category in sub_categories_html:
                    # print(sub_category)
                    sub_categories.append(dict(
                        name=sub_category.text
                    ))

                if len(sub_categories) == 0:
                    bot.send_message(message.from_user.id, "Нет доступных подкатегорий")
                    return

                s = ["Выберите подкатегорию:"]
                for i, sub_category in enumerate(sub_categories, start=1):
                    s.append(f"{i}. {sub_category['name']}") #  ({translate(sub_category['name'])})")
                bot.send_message(message.from_user.id, "\n".join(s))

                state = "STATE_INPUT_SUBCATEGORY"
                print(f"NEW STATE = {state}, USER_INPUT = {message.text}")

            elif state == "STATE_INPUT_SUBCATEGORY":
                q = int(message.text) - 1

                sub_categories_html[q].click()
                time.sleep(WAIT_S)

                # Выбор узла
                uzly_html = driver.find_elements(by=By.XPATH, value="//td[@class='table-name']")
                uzly = []
                for uzel in uzly_html:
                    uzly.append(dict(
                        name=uzel.text
                    ))

                if len(uzly) == 0:
                    bot.send_message(message.from_user.id, "Нет доступных узлов")
                    return

                s = ["Выберите узел:"]
                for i, uzel in enumerate(uzly, start=1):
                    s.append(f"{i}. {uzel['name']}") #  ({translate(uzel['name'])})")
                bot.send_message(message.from_user.id, "\n".join(s))

                state = "STATE_INPUT_UZEL"
                print(f"NEW STATE = {state}, USER_INPUT = {message.text}")

            elif state == "STATE_INPUT_UZEL":
                q = int(message.text) - 1

                element = driver.find_elements(by=By.XPATH, value="//a[contains(@class,'catalogs-buy-link')]")[q]
                element.click()
                time.sleep(WAIT_S * 2)
                if len(driver.window_handles) > 1:
                    driver.switch_to.window(driver.window_handles[1])  # Предложения открываются в новой вкладке

                    # Выводим детали
                    if "Нет предложений" in driver.page_source:
                        bot.send_message(message.from_user.id, "Выбранный узел недоступен к продаже (отсутствует)")
                    else:
                        offers = []
                        prices_html = driver.find_elements(by=By.XPATH, value="//td[@class='price']")
                        counts_html = driver.find_elements(by=By.XPATH, value="//td[@class='presence']")
                        i = 0

                        for i in range(len(prices_html)):
                            try:
                                offers.append(dict(count=int(counts_html[i].text), price=float(prices_html[i].text)))
                            except ValueError:
                                print("error")
                                print(counts_html[i].text)
                                print(prices_html[i].text)

                        if len(offers) > 0:
                            s = ["Доступны следующие предложения:"]
                            # print(offers)
                            for i, offer in enumerate(sorted(offers, key=lambda x: x['price']), start=1):
                                s.append(f"{i}. {offer['count']} шт. по {offer['price']} ₽.")
                            bot.send_message(message.from_user.id, "\n".join(s))
                        else:
                            bot.send_message(message.from_user.id, "Выбранный узел недоступен к продаже (отсутствует)")
                else:
                    bot.send_message(message.from_user.id, "Ошибка при получении информации об узле")

                state = "STATE_START"
                print(f"NEW STATE = {state}, USER_INPUT = {message.text}")
            else:
                print("UNKNOWN STATE")

    except Exception as e:
        print(str(e) + "\n" + traceback.format_exc())
        bot.send_message(message.from_user.id, "Я сломался, попробуйте еще раз")


if __name__ == '__main__':
    service = ChromeService(executable_path=ChromeDriverManager().install())
    options = Options()
    options.page_load_strategy = 'none'

    driver = uc.Chrome(
        options=options,
        use_subprocess=False,
        headless=True,
    )

    print("Bot started...")

    bot.polling(none_stop=True, interval=0)
