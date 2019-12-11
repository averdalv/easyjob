from enum import Enum


class CustomerTypeEnum(Enum):
    INDIVIDUAL = "Individual"
    firm = "Firm"

CustomerCategoryChoices = [(category_type, category_type.value) for category_type in CustomerTypeEnum]