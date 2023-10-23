from webdriver_manager.chrome import ChromeDriverManager


chrome_driver_path = ChromeDriverManager().install()

with open('./chrome_driver_path.txt', 'w') as file:
    file.write(chrome_driver_path)
