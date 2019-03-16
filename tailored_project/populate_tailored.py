import os
os.environ.setdefault("DJANGO_SETTINGS_MODULE",
											"tailored_project.settings")

import django
django.setup()
from tailored.models import Category, Item, Section

def populate():

	# Instances of items
	T_Shirt_M = {"title": "Blue shirt", "price": 10, "description" : "Niko is the best ", 
					"sold" : False, "dailyVisits": 10, "size": "S"}

	T_Shirt_W = {"title": "Red shirt", "price": 20, "description" : "Niko is the best ",
								"sold" : False, "dailyVisits": 20, "size": "M"}

	T_Shirt_K = {"title": "Black shirt", "price": 30, "description" : "Niko is the best ",
								"sold" : False, "dailyVisits": 30, "size": "L"}

	Trousers_M = {"title": "Jeans Blue", "price": 10, "description" : "Niko is the best ",
									"sold" : False, "dailyVisits": 10, "size": "S"}

	Trousers_W = {"title": "Jeans Red", "price": 20, "description" : "Niko is the best ",
									"sold" : False, "dailyVisits": 20, "size": "M"}

	Trousers_K = {"title": "Jeans White", "price": 30, "description" : "Niko is the best ",
									"sold" : False, "dailyVisits": 30, "size": "XL"}

	Jacket_M = {"title": "Blue Coat", "price": 10, "description" : "Niko is the best ",
							"sold" : False, "dailyVisits": 10, "size": "S"}
		
	Jacket_W = {"title": "White Coat", "price": 20, "description" : "Niko is the best ",
							"sold" : False, "dailyVisits": 20, "size": "M"}
		
	Jacket_K = {"title": "Red Coat", "price": 30, "description" : "Niko is the best ",
							"sold" : False, "dailyVisits": 30, "size": "XXL"}

	# List of items
	items = [T_Shirt_M, T_Shirt_W, T_Shirt_K, Trousers_M, Trousers_W, Trousers_K, Jacket_M, Jacket_W, Jacket_K]
	
	# List of sections
	sections = [{"title": "Men"}, {"title": "Women"}, {"title": "Kids"}]

	# List of categories
	categories = [{"title": "T-Shirt"}, {"title": "Trousers"}, {"title": "Jackets"}]

	# List of instances of sections
	sections_instances = []
	for section in sections:
		sections_instances.append(add_section(section["title"]))

	# List of instances of categories
	categories_instances = []
	for category in categories:
		categories_instances.append(add_category(category["title"]))

	for item_data in items:
		add_item(item_data["title"], item_data["price"], item_data["description"],
				item_data["sold"], item_data["dailyVisits"], item_data["size"],
				categories_instances[int(items.index(item_data)/len(categories_instances) % len(categories_instances))],
				sections_instances[items.index(item_data) % len(sections_instances)])

						
def add_item(title, price, description, sold, dailyVisits, size, category, section):
	"""Adds a new item with the given title, price, description, sold, daily visits, size, category 
		and section to the database."""
	item = Item.objects.get_or_create(title = title, price = price, description = description,
									sold = sold, dailyVisits = dailyVisits, size = size, category = category, section = section)[0]
	return item

def add_category(title):
	"""Adds a new category with the given title to the database."""
	category = Category.objects.get_or_create(title = title)[0]
	category.save()
	return category

def add_section(title):
	"""Adds a new section with the given title to the database."""
	section = Section.objects.get_or_create(title = title)[0]
	section.save()
	return section

if __name__ == "__main__":
	print("Starting population script...")
	populate()