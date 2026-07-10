class CartLocators:

    TITLE = "[data-test='title']"

    CART_ITEM = "[data-test='inventory-item']"
    ITEM_NAME = "[data-test='inventory-item-name']"
    ITEM_PRICE = "[data-test='inventory-item-price']"
    ITEM_QUANTITY = "[data-test='item-quantity']"

    CONTINUE_SHOPPING_BUTTON = "[data-test='continue-shopping']"
    CHECKOUT_BUTTON = "[data-test='checkout']"

    @staticmethod
    def remove(item_slug: str) -> str:
        return f"[data-test='remove-{item_slug}']"
