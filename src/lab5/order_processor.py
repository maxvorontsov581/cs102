import re
from collections import OrderedDict
from enum import Enum
from typing import List, Optional


class DeliveryPriority(Enum):
    MAX = "MAX"
    MIDDLE = "MIDDLE"
    LOW = "LOW"


class ValidationErrorType(Enum):
    ADDRESS_ERROR = "ADDRESS_ERROR"
    PHONE_ERROR = "PHONE_ERROR"


class ValidationError:
    def __init__(self, error_type: ValidationErrorType, error_value: str):
        self.error_type = error_type
        self.error_value = error_value


class PersonName:
    def __init__(self, full_name: str):
        self.full_name = full_name.strip()

    def __str__(self):
        return self.full_name


class Address:
    def __init__(self, country: str, region: str, city: str, street: str):
        self.country = country
        self.region = region
        self.city = city
        self.street = street

    @classmethod
    def from_string(cls, s: str) -> Optional["Address"]:
        if not s or not s.strip():
            return None
        parts = [p.strip() for p in s.split(".")]
        if len(parts) != 4:
            return None
        if any(p == "" for p in parts):
            return None
        return cls(parts[0], parts[1], parts[2], parts[3])

    def format_for_output(self) -> str:
        return f"{self.region}. {self.city}. {self.street}"


class PhoneNumber:
    def __init__(self, raw: str):
        self.raw = raw.strip()

    @classmethod
    def from_string(cls, s: str) -> Optional["PhoneNumber"]:
        if not s or not s.strip():
            return None
        if re.match(r'^\+\d-\d{3}-\d{3}-\d{2}-\d{2}$', s.strip()):
            return cls(s.strip())
        return None

    def __str__(self):
        return self.raw


class ProductList:
    def __init__(self, raw: str):
        self.products = [p.strip() for p in raw.split(",")]

    def format_for_output(self) -> str:
        seen = OrderedDict()
        for p in self.products:
            seen[p] = seen.get(p, 0) + 1
        parts = []
        for name, count in seen.items():
            if count > 1:
                parts.append(f"{name} x{count}")
            else:
                parts.append(name)
        return ", ".join(parts)


class Order:
    def __init__(self, order_number, products, customer_name, address_raw, phone_raw, priority_raw):
        self.order_number = order_number
        self.products = products
        self.customer_name = customer_name
        self._address_raw = address_raw
        self._phone_raw = phone_raw
        self.address = Address.from_string(address_raw)
        self.phone = PhoneNumber.from_string(phone_raw)
        try:
            self.priority = DeliveryPriority(priority_raw.strip())
        except ValueError:
            self.priority = None

    @classmethod
    def from_line(cls, line: str) -> "Order":
        parts = line.strip().split(";")
        while len(parts) < 6:
            parts.append("")
        return cls(parts[0].strip(), ProductList(parts[1]), PersonName(parts[2]), parts[3].strip(), parts[4].strip(), parts[5].strip())

    def validate(self) -> List[ValidationError]:
        errors = []
        if self.address is None:
            value = self._address_raw if self._address_raw else "no data"
            errors.append(ValidationError(ValidationErrorType.ADDRESS_ERROR, value))
        if self.phone is None:
            value = self._phone_raw if self._phone_raw else "no data"
            errors.append(ValidationError(ValidationErrorType.PHONE_ERROR, value))
        return errors


class OrderProcessor:
    PRIORITY_ORDER = {DeliveryPriority.MAX: 0, DeliveryPriority.MIDDLE: 1, DeliveryPriority.LOW: 2}

    def __init__(self, filename: str):
        self.orders: List[Order] = []
        self.valid_orders: List[Order] = []
        self.invalid_orders: List[Order] = []
        self._load(filename)

    def _load(self, filename: str):
        with open(filename, "r", encoding="utf-8") as f:
            lines = f.readlines()
        for line in lines:
            line = line.strip()
            if not line:
                continue
            order = Order.from_line(line)
            self.orders.append(order)
            if order.validate():
                self.invalid_orders.append(order)
            else:
                self.valid_orders.append(order)

    def save_invalid_orders(self, filename: str):
        with open(filename, "w", encoding="utf-8") as f:
            for order in self.invalid_orders:
                for err in order.validate():
                    code = 1 if err.error_type == ValidationErrorType.ADDRESS_ERROR else 2
                    f.write(f"{order.order_number};{code};{err.error_value}\n")

    def save_valid_orders_sorted(self, filename: str):
        def sort_key(o):
            country = o.address.country if o.address else ""
            return (0 if country == "Россия" else 1, country, self.PRIORITY_ORDER.get(o.priority, 99))
        with open(filename, "w", encoding="utf-8") as f:
            for order in sorted(self.valid_orders, key=sort_key):
                f.write(f"{order.order_number};{order.products.format_for_output()};{order.customer_name};{order.address.country}. {order.address.format_for_output()};{order.phone};{order.priority.value}\n")
