from django.db import models
from accounts.models import User
from django.contrib.contenttypes.models import ContentType
from django.db.models.query import QuerySet
from thumbnail.fields import ImageWithThumbnailsField
from tagging.fields import TagField
import tagging
import os.path
import settings

ITEM_TEMPLATES = os.path.join(settings.ROOT, "templates/item_templates/")

class SubclassingQuerySet(QuerySet):
    """ Puts children in the queryset (their parents are useless) """
    def __getitem__(self, k):
        result = super(SubclassingQuerySet, self).__getitem__(k)
        if isinstance(result, models.Model):
            return result.as_leaf_class()
        else:
            return result
    def __iter__(self):
        for item in super(SubclassingQuerySet, self).__iter__():
            yield item.as_leaf_class()

class ItemManager(models.Manager):
    def available(self):
        return super(ItemManager,self).get_query_set().filter(status__exact='A')
    def visible(self):
        return super(ItemManager,self).get_query_set().filter(status__in=['A', 'E', 'C', 'L'])
    def deleted(self):
        return super(ItemManager,self).get_query_set().filter(status__exact='D')

class BaseItemManager(ItemManager):
    def get_query_set(self):
        return SubclassingQuerySet(self.model)
                
class Item(models.Model):
    # Give me my CHILD (object)
    objects = BaseItemManager()
    parents = models.Manager()
    content_type = models.ForeignKey(ContentType,editable=False,null=True)

    def as_leaf_class(self):
        content_type = self.content_type
        model = content_type.model_class()
        if (model == Item):
            return self
        return model.objects.get(id=self.id)

    def save(self, *args, **kwargs):
        if not self.content_type:
            self.content_type = ContentType.objects.get_for_model(self.__class__)
        super(Item, self).save(*args, **kwargs)

    MODE_CHOICES = (
        (u'sell', u'Sell'),
        (u'buy', u'Buy'),
    )
    STATUS_CHOICES = (
        (u'A', u'Available'),
        (u'E', u'Expired'),
        (u'D', u'Deleted'),
        (u'C', u'Complete'),
        (u'L', u'Locked'),
    )
    CONDITION_CHOICES = (
        ('0', 'New'),
        ('1', 'Slightly Used'),
        ('2', 'Used'),
        ('3', 'Well Used'),
        ('4', 'Broken'),
    )
    CATEGORY_CHOICES = (
        ('cloths', 'Cloths'),
        ('electronics', 'Electronics'),
        ('entertainment', 'Entertainment'),
        ('food', 'Food'),
        ('materials', 'Materials'),
        ('miscellaneous', 'Miscellaneous'),
        ('services', 'Services'),
        ('textbooks', 'Textbooks'),
        ('transportation', 'Transportation'),
    )

    mode = models.CharField(max_length=4, choices=MODE_CHOICES, default='S')
    status = models.CharField(max_length=1, choices=STATUS_CHOICES, default='A')
    # People
    owner = models.ForeignKey(User, related_name="my_items")
    customers = models.ManyToManyField(User, related_name="claimed_items")

    # Info
    name = models.CharField(max_length=100)
    description = models.TextField()
    photo = ImageWithThumbnailsField(
        upload_to = "images/items/",
        thumbnail = {
            'size': (200,200),
            'subdir': 'thumbs'
        },
        blank=True,
    )
    price = models.DecimalField(max_digits=6, decimal_places=2)
    condition = models.CharField(max_length=1, choices=CONDITION_CHOICES, default=3)
    location = models.CharField(max_length=200)
    date = models.DateTimeField(editable=False, auto_now_add = True)

    def __unicode__(self):
        return self.name

    def template(self):
        return ITEM_TEMPLATES + "generic.html"

    def claims(self):
        return self.customers.count()
try:
    tagging.register(Item)
except tagging.AlreadyRegistered:
    # Dev Note: Not sure the right way to register a model for tagging b/c it
    # raises this error if registered more than once. We end up registering
    # the first time during "manage.py syncdb" and then a second time when
    # actually attempting to run the site.
    pass

class ClothsItem(Item):
    objects = ItemManager()
    GENDER_CHOICES = (
        ('', 'Both'),
        ('F', 'Female'),
        ('M', 'Male'),
    )
    SIZE_CHOICES = (
        ('', 'N/A'),
        ('XXL', 'Extra-Extra Large'),
        ('XL', 'Extra Large'),
        ('L', 'Large'),
        ('ML', 'Medium Large'),
        ('M', 'Medium'),
        ('MS', 'Medium Small'),
        ('S', 'Small'),
        ('XS', 'Extra Small'),
        ('C', 'Child'),
        ('T', 'Toddler'),
        ('B', 'Baby'),
    )
    size = models.CharField(max_length=3,
                            choices=SIZE_CHOICES,
                            default='',
                            blank=True
                           )
    gender = models.CharField(max_length=1,
                              choices=GENDER_CHOICES,
                              default='',
                              blank=True
                             )
    def template(self):
        return ITEM_TEMPLATES + "cloths.html"

class ElectronicsItem(Item):
    objects = ItemManager()
    make = models.CharField(max_length=100, blank=True)
    def template(self):
        return ITEM_TEMPLATES + "electronics.html"

class EntertainmentItem(Item):
    objects = ItemManager()
    MEDIA_CHOICES = (
        # Other
        ('', 'Other'),
        # Music
        ('CD_M', 'Music - CD'),
        ('TAPM', 'Music - Tape'),
        ('DIGM', 'Music - Digital'),
        # Video
        ('DVDV', 'Video - DVD'),
        ('VHSV', 'Video - VHS'),
        ('DIGV', 'Video - Digital'),
        # Game
        ('VIDG', 'Game - Video'),
        ('BOAG', 'Game - Board'),
        ('CARG', 'Game - Card'),
        ('OTHG', 'Game - Other'),
        # Books
        ('PAPB', 'Book - Paperback'),
        ('HARB', 'Book - Hardcover'),
        ('ELEB', 'Book - Electronic'),
    )
      

    media = models.CharField(max_length=3, default='', blank=True)
    title = models.CharField(max_length=100, blank=True)
    author = models.CharField(max_length=100, blank=True)
    def template(self):
        return ITEM_TEMPLATES + "entertainment.html"

class FoodItem(Item):
    objects = ItemManager()
    def template(self):
        return ITEM_TEMPLATES + "generic.html"

class MaterialsItem(Item):
    objects = ItemManager()
    def template(self):
        return ITEM_TEMPLATES + "generic.html"

class MiscellaneousItem(Item):
    objects = ItemManager()
    def template(self):
        return ITEM_TEMPLATES + "generic.html"

class ServicesItem(Item):
    objects = ItemManager()
    def template(self):
        return ITEM_TEMPLATES + "generic.html"

class TextbooksItem(Item):
    objects = ItemManager()
    title = models.CharField(max_length=100, blank=True)
    author = models.CharField(max_length=100, blank=True)
    course = models.CharField(max_length=100, blank=True)
    def template(self):
        return ITEM_TEMPLATES + "textbooks.html"

class TransportationItem(Item):
    objects = ItemManager()
    make = models.CharField(max_length=100)
    def template(self):
        return ITEM_TEMPLATES + "transportation.html"
