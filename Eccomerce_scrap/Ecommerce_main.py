from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import Select
from prettytable import PrettyTable
import Ecommerce_constants as const
import time
from colorama import Style,Fore


class  Swag(webdriver.Chrome):

    def __init__(self):

        self.options=webdriver.ChromeOptions()
        self.options.add_experimental_option("detach",True)
        self.driver=webdriver.Chrome(options=self.options)
        self.driver.maximize_window()

    def land_first_page(self):
        self.driver.get(const.base_url)





    def user_name_fill(self):
        self.wait=WebDriverWait(self.driver,10)
        username_element=self.wait.until(EC.presence_of_element_located((By.CLASS_NAME,"form_group")))
        username_line=username_element.find_element(By.ID,"user-name")
        username_line.send_keys("standard_user")

    def password_fill(self):
        password_line=self.wait.until(EC.presence_of_element_located((By.ID,"password")))
        password_line.send_keys("secret_sauce")

    def login_button(self):
        login_element=self.driver.find_element(By.ID,"login-button")
        login_element.click()


    def drop_down(self):
        dropdown_container=self.driver.find_element(By.CLASS_NAME,"product_sort_container")

        select=Select(dropdown_container)
        select.select_by_value('lohi')


    def __exit__(self, exc_type, exc_value, traceback):
        try:
            super().__exit__(exc_type, exc_value, traceback)
        except AttributeError:
            pass  # Ignore AttributeError during exit


    def fetch_details_from_container(self):
        containers=self.driver.find_elements(By.CLASS_NAME,"inventory_item")
        product_table=PrettyTable(['Product Name','Product Details','Price'])

        for container in containers:
            heading=container.find_element(By.CLASS_NAME,"inventory_item_name ").text
            paragraph=container.find_element(By.CLASS_NAME,"inventory_item_desc").text.strip()
            price=container.find_element(By.CLASS_NAME,"inventory_item_price").text.strip()

            product_table.add_row([heading,paragraph,price])




        print(product_table)
        print('\n')



    def add_to_cart(self,product_name):

        try:
            product_locator= (By.XPATH, f"//div[@class='inventory_item']/div[@class='inventory_item_description']//div[@class='inventory_item_name ' and text()='{product_name}']/ancestor::div[@class='inventory_item']//button[@id='add-to-cart-sauce-labs-onesie']")

            add_to_cart_button=WebDriverWait(self.driver, 10).until(
                EC.presence_of_element_located(product_locator))

            self.driver.execute_script("arguments[0].scrollIntoView();", add_to_cart_button)

            add_to_cart_button.click()
            print(f"Successfully added '{product_name}' to the cart.")

        except Exception as e:
            print(f"Failed to add '{product_name}' to the cart. Error: {str(e)}")

    def multiple_add_to_cart(self, product_name):
        try:

            inventory_container = WebDriverWait(self.driver, 10).until(
                EC.presence_of_element_located(
                    (By.XPATH, "//div[@id='inventory_container' and @class='inventory_container']"))
            )
            print("Name of the products:\n")

            # Find inventory items within the container
            inventory_contents = inventory_container.find_elements(By.XPATH, ".//div[@class='inventory_item']")

            for content in inventory_contents:

                inventory_item_description=content.find_element(By.CLASS_NAME,"inventory_item_description" )
                inventory_item_anchor_name=content.find_element(By.XPATH,"//a[@href='#']")
                inventory_item_name=inventory_item_description.find_element(By.CLASS_NAME,"inventory_item_name").text
                print('*',inventory_item_name)

                if(inventory_item_name==product_name):
                    add_to_cart_container=content.find_element(By.CLASS_NAME,"pricebar")
                    add_to_cart_button=add_to_cart_container.find_element(By.TAG_NAME,"button")
                    add_to_cart_button.click()

        except Exception as e:
            print(f"Failed to add '{product_name}' to the cart. Error: {str(e)}")




    def check_cart(self,cart_check_in):
        header_label=self.driver.find_element(By.ID,"shopping_cart_container")
        time.sleep(2)
        if(cart_check_in==True):
            header_label.click()


    def check_out(self):
        check_out_button=self.driver.find_element(By.ID,"checkout")

        wait = WebDriverWait(self.driver, 10)
        check_out_element = wait.until(EC.element_to_be_clickable((By.ID, "checkout")))

        check_out_element.click()

    def check_out_info(self,user_first_name,user_last_name,user_postal_code):

        check_out_info_box=self.driver.find_element(By.CLASS_NAME,"checkout_info")
        first_name=check_out_info_box.find_element(By.ID,"first-name")
        first_name.send_keys(user_first_name)
        last_name=check_out_info_box.find_element(By.ID,"last-name")
        last_name.send_keys(user_last_name)
        postal_code=check_out_info_box.find_element(By.ID,"postal-code")
        postal_code.send_keys(user_postal_code)

    def check_out_continue_button(self,click):

        if click:
            continue_button=self.driver.find_element(By.ID,"continue")
            wait=WebDriverWait(self.driver,5)
            continue_element=wait.until(EC.element_to_be_clickable((By.ID,"continue")))

            continue_element.click()


    def check_out_description(self):

        description_table=PrettyTable(['Payment Information','Shipping Information','item total','tax','Total'])
        description_container=self.driver.find_element(By.CLASS_NAME,"summary_info")
        payment_info=description_container.find_element(By.CLASS_NAME,"summary_value_label").text.strip()

        shipping_info=description_container.find_element(By.XPATH,"//div[text()='Free Pony Express Delivery!']").text.strip()

        item_total=description_container.find_element(By.CLASS_NAME,"summary_subtotal_label").text.strip()

        Tax=description_container.find_element(By.CLASS_NAME,"summary_tax_label").text.strip()

        Total=description_container.find_element(By.XPATH,"//div[@class='summary_info_label summary_total_label']").text.strip()

        description_table.add_row([payment_info,shipping_info,item_total,Tax,Total])
        print("\n")
        print("Product Details:\n")
        print(description_table)


    def cancel_or_finish(self,choice):

        cart_footer=self.driver.find_element(By.CLASS_NAME,"cart_footer")
        cancel_button=cart_footer.find_element(By.ID,"cancel")
        finish_button=cart_footer.find_element(By.ID,"finish")

        if choice.lower()=='n':
            cancel_button.click()
            print(f"\n{Fore.RED}item cancelled!{Style.RESET_ALL}")

        elif choice.lower()=='y':
            finish_button.click()
            print(f"\n{Fore.GREEN}item checked out!{Style.RESET_ALL}")







