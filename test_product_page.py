from .pages.product_page import ProductPage

link = "http://selenium1py.pythonanywhere.com/catalogue/the-shellcoders-handbook_209/?promo=newYear"

def test_guest_can_add_product_to_basket(browser):
    page = ProductPage(browser, link)
    page.open()

    page.set_product_name()
    page.set_product_price()

    page.should_be_add_to_basket_button()
    page.click_add_to_basket()
    page.guest_can_add_product_to_basket()
