class InventoryLocators:

    TITLE = "[data-test='title']"
    INVENTORY_CONTAINER = "[data-test='inventory-container']"

    INVENTORY_ITEM = "[data-test='inventory-item']"
    ITEM_NAME = "[data-test='inventory-item-name']"
    ITEM_PRICE = "[data-test='inventory-item-price']"
    ITEM_DESC = "[data-test='inventory-item-desc']"

    SORT_DROPDOWN = "[data-test='product-sort-container']"

    CART_LINK = "[data-test='shopping-cart-link']"
    CART_BADGE = "[data-test='shopping-cart-badge']"

    # Buttons use kebab-cased product name suffix
    @staticmethod
    def add_to_cart(item_slug: str) -> str:
        return f"[data-test='add-to-cart-{item_slug}']"

    @staticmethod
    def remove(item_slug: str) -> str:
        return f"[data-test='remove-{item_slug}']"

    BURGER_MENU_BUTTON = "#react-burger-menu-btn"
    RESET_APP_STATE_LINK = "text=Reset App State"
    LOGOUT_LINK = "#logout_sidebar_link"
