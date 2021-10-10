from django.core.exceptions import ObjectDoesNotExist
from django.core.paginator import Paginator
from django.db.models import Max, Min

from .models import Product, Cart, Entry


class FilterParams:
    def __init__(self, filter_params: dict):
        self.search = filter_params.get("search")
        # self.category = filter_params.get("category")
        self.price_range = {
            "min": filter_params.get("price_min"),
            "max": filter_params.get("price_max"),
        }
        self.page = filter_params.get("page", 1)

    def is_price_range_empty(self):
        return self.price_range["min"] is None and self.price_range["max"] is None

    def is_empty(self):
        return (
            self.search is None
            # and self.category is None
            and self.is_price_range_empty()
        )


class GetProducts:
    PRICE_FIELD = "price"
    ITEMS_PER_PAGE = 1

    def __init__(self, filter_params: FilterParams):
        if filter_params.search:
            products = Product.objects.filter(name__contains=filter_params.search)
        else:
            products = Product.objects.all()

        price_range = {
            "min": products.aggregate(Min(self.PRICE_FIELD))[
                self.PRICE_FIELD + "__min"
            ],
            "max": products.aggregate(Max(self.PRICE_FIELD))[
                self.PRICE_FIELD + "__max"
            ],
        }
        if not filter_params.is_price_range_empty():
            products = products.filter(
                price__gte=filter_params.price_range["min"],
                price__lte=filter_params.price_range["max"],
            )

        self.products = products.order_by("-id")
        # self.categories = self.get_categories()
        self.price_range = price_range
        self.price_min = filter_params.price_range["min"]
        self.price_max = filter_params.price_range["max"]
        self.search = filter_params.search
        paginator = Paginator(self.products, self.ITEMS_PER_PAGE)
        self.products = paginator.page(filter_params.page)
        self.pagination = {
            "count": paginator.count,
            "current_page": int(filter_params.page),
            "start_page": 1,
            "last_page": paginator.num_pages,
            "page_range": list(paginator.page_range),
        }

    # @staticmethod
    # def get_categories() -> Dict[str, list]:
    #     return dict()

    def get_context(self):
        return {
            "products": self.products,
            # "categories": self.categories,
            "price_range": self.price_range,
            "pagination": self.pagination,
            "search": self.search,
            "price_min": self.price_min,
            "price_max": self.price_max,
        }


def get_product(identifier: int):
    try:
        product = Product.objects.get(id=identifier)
        return product
    except ObjectDoesNotExist:
        return None


def add_product_to_cart(user, identifier: int):
    product = get_product(identifier)
    user_cart, created = Cart.objects.get_or_create(user=user)
    user_entries = Entry.objects.filter(cart=user_cart, product=product)
    if user_entries:
        entry = user_entries.first()
        entry.quantity += 1
        entry.save()
    else:
        entry = Entry.objects.create(product=product, cart=user_cart, quantity=1)

    user_cart.refresh_from_db()
    return user_cart, entry


def remove_product_from_cart(user, identifier: int):
    product = get_product(identifier)
    user_cart = Cart.objects.get(user=user)
    entry = Entry.objects.filter(cart=user_cart, product=product).first()

    if entry.quantity >= 1:
        entry.quantity -= 1
    entry.save()
    user_cart.refresh_from_db()
    return user_cart, entry


def delete_product_from_cart(user, identifier: int):
    product = get_product(identifier)
    user_cart = Cart.objects.get(user=user)
    entry = Entry.objects.filter(cart=user_cart, product=product).first()
    entry.delete()
    user_cart.refresh_from_db()
    return user_cart


def get_cart_entries(user):
    user_cart, created = Cart.objects.get_or_create(user=user)
    return {"cart": user_cart, "entries": user_cart.entry_set.all()}
