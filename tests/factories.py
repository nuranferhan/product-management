import factory
from factory.fuzzy import FuzzyChoice, FuzzyDecimal
from service.models import Product


class ProductFactory(factory.Factory):
    """Creates fake products for testing"""

    class Meta:
        model = Product

    id = factory.Sequence(lambda n: n)
    name = factory.Faker("word")
    description = factory.Faker("text", max_nb_chars=100)
    price = FuzzyDecimal(0.5, 999.99, 2)
    available = FuzzyChoice(choices=[True, False])
    category = FuzzyChoice(choices=["Clothing", "Electronics", "Food", "Automotive", "Tools"])