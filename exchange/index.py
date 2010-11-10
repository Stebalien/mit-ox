from djapian import space, Indexer, CompositeIndexer
from exchange.models import *

class ItemIndexer(Indexer):
    fields = ['description', 'title', 'get_condition_display']
    tags = [
        ('name', 'name'),
        ('price', 'price'),
        ('location', 'location'),
        ('date', 'date'),
        ('condition', 'condition'),
        ('claims', 'claims'),
    ]

class ClothsIndexer(ItemIndexer):
    tags = ItemIndexer.tags + [
        ('gender', 'get_gender_display'),
        ('size', 'size'),
    ]

space.add_index(ClothsItem, ClothsIndexer, attach_as='indexer')

class ElectronicsIndexer(ItemIndexer):
    tags = ItemIndexer.tags + [
        ('make', 'make'),
    ]

space.add_index(ElectronicsItem, ElectronicsIndexer, attach_as='indexer')

class EntertainmentIndexer(ItemIndexer):
    tags = ItemIndexer.tags + [
        ('media', 'get_media_display'),
        ('title', 'title'),
        ('author', 'author'),
    ]

space.add_index(EntertainmentItem, EntertainmentIndexer, attach_as='indexer')

class FoodIndexer(ItemIndexer):
    pass
space.add_index(FoodItem, FoodIndexer, attach_as='indexer')

class MaterialsIndexer(ItemIndexer):
    pass
space.add_index(MaterialsItem, MaterialsIndexer, attach_as='indexer')

class MiscellaneousIndexer(ItemIndexer):
    pass
space.add_index(MiscellaneousItem, MiscellaneousIndexer, attach_as='indexer')

class ServicesIndexer(ItemIndexer):
    pass
space.add_index(ServicesItem, ServicesIndexer, attach_as='indexer')

class TextbooksIndexer(ItemIndexer):
    tags = ItemIndexer.tags + [
        ('title', 'title'),
        ('author', 'author'),
        ('course', 'course'),
    ]

space.add_index(TextbooksItem, TextbooksIndexer, attach_as='indexer')

class TransportationIndexer(ItemIndexer):
    tags = ItemIndexer.tags + [
        ('make', 'make'),
    ]

space.add_index(TransportationItem, TransportationIndexer, attach_as='indexer')

complete_indexer = CompositeIndexer(ClothsItem.indexer, ElectronicsItem.indexer, EntertainmentItem.indexer, FoodItem.indexer, MaterialsItem.indexer, MiscellaneousItem.indexer, ServicesItem.indexer, TextbooksItem.indexer, TransportationItem.indexer)
