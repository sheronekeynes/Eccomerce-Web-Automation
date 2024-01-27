
from Ecommerce_main import Swag
from colorama import Style,Fore

with Swag() as bot:

    bot.land_first_page()
    bot.user_name_fill()
    bot.password_fill()
    bot.login_button()
    bot.drop_down()
    bot.fetch_details_from_container()
    bot.multiple_add_to_cart(product_name="Sauce Labs Fleece Jacket")
    bot.check_cart(cart_check_in=True)
    bot.check_out()
    bot.check_out_info(user_first_name="sherone",user_last_name="keynes",user_postal_code="642-154")
    bot.check_out_continue_button(click=True)
    bot.check_out_description()
    bot.cancel_or_finish(choice = input(f"{Fore.LIGHTMAGENTA_EX}Enter your choice (y or n) for the item to be checked out or to be cancelled: {Style.RESET_ALL}"))

