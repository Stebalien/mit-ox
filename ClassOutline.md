### class Item ###
  * name
  * category
  * ID
  * poster (buyer/seller) --Person
  * description
  * image
  * sale type
  * customers --list of Persons
  * tag list
  * location
  * post status (valid, expired, deleted, sold)

### class Category ###
|class|ClassMaterials|extends|Category|
|:----|:-------------|:------|:-------|
|class|Transportation|extends|Category|
|class|Entertainment|extends|Category|
|class|Textbooks|extends|Category|
|class|Food|extends|Category|
|class|Services|extends|Category|
|class|Clothes|extends|Category|
|class|Miscellaneous|extends|Category|
|class|Electronics|extends|Category|

### class Person ###
  * name
  * location
  * role (student/faculty)
  * Items Posted(list of Items owned by this person)
  * Items Claimed (list of Items claimed by this person)
  * Prof pic!
  * Contact (separate class?)

### class Contact ###
  * mit email
  * alt email
  * cell number
  * cell provider
  * use mit email (bool)
  * use alt email (bool)
  * use cell (bool)