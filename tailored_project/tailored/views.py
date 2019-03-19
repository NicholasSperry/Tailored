from django.http import HttpResponseRedirect
from django.shortcuts import render
from tailored.models import UserProfile, Category, Section, Item, Review
from tailored.forms import Search_bar, ItemForm, CategoryForm, SectionForm, UserProfileForm, ReviewForm
from django.db.models import Q
from django.core.urlresolvers import reverse
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib import auth
from django.contrib.auth.models import User


def index(request):
	return render(request, 'tailored/index.html')


def items(request):
	item_list = Item.objects.order_by('-dailyVisits')[:5]
	context_dict = {'items': item_list}

	return render(request, 'tailored/itemsList.html', context_dict)


@login_required
def add_category(request):
	form = CategoryForm()

	if request.method == 'POST':
		form = CategoryForm(request.POST)

		if form.is_valid():
			form.save(commit = True)
			return HttpResponseRedirect(reverse('tailored:index'))

		else:
			print(form.errors)

	return render(request, 'tailored/add_category.html', {'form': form})


def show_section(request, title):
	context_dict = {}

	try:
		title = title.lower().capitalize()
		
		section = Section.objects.get(title = title)
		items = Item.objects.filter(section = section)
		context_dict["items"] = items
		context_dict["section"] = section

	except Section.DoesNotExist:

		context_dict["section"] = None
		context_dict["items"] = None

	return render(request, "tailored/section.html", context_dict)


def show_category(request, title):
	context_dict = {}

	try:
		title = title.lower()
		
		category = Category.objects.get(slug = title)
		items = Item.objects.filter(category = category)
		context_dict["items"] = items
		context_dict["category"] = category

	except Category.DoesNotExist:

		context_dict["category"] = None
		context_dict["items"] = None

	return render(request, "tailored/category.html", context_dict)

@login_required
def add_item(request):
	queryset = Section.objects.all()
	form = ItemForm(section_set = queryset)

	if (request.method == "POST"):
		form = ItemForm(queryset, request.POST)
		if form.is_valid():
			item = form.save(commit = False)
			item.sellerID = UserProfile.objects.get(user = request.user)

			if 'picture' in request.FILES:
				item.picture = request.FILES['picture']
			
			item.save()

			return HttpResponseRedirect(reverse('tailored:show_section',
				kwargs = {'title': str(form.cleaned_data.get("section"))}))

		else:
			print(form.errors)
	return render(request, "tailored/add_item.html", {"form": form})


@login_required
def leave_review(request):
	"""queryset = Item.objects.filter(Q(sold_to = UserProfile.objects.get(user = request.user)) &
									~Q(item__in = Review.objects.filter(item__id = item.itemID)))"""

	items_reviewed = []

	for review in Review.objects.select_related():
		items_reviewed.append(review.item.itemID)
	
	queryset = Item.objects.filter(Q(sold_to = UserProfile.objects.get(user = request.user))
								).exclude(itemID__in = items_reviewed)

	print(not queryset) # Empty queryset

	form = ReviewForm(user_items = queryset)

	if(request.method == "POST"):
		form = ReviewForm(queryset, request.POST)
		if form.is_valid():
			review = form.save(commit = False)
			review.buyerID = UserProfile.objects.get(user = request.user)
			review.save()

			return HttpResponseRedirect(reverse('tailored:show_seller_profile',
					kwargs = {'username': request["seller"].username}))
		else:
			print(form.errors)

	return render(request, "tailored/leave_review.html", {"form": form})


def show_seller_profile(request, username):
	user = User.objects.filter(username = username)

	return render(request, 'tailored/seller_profile.html', {'user': user})



def search_bar(request, search = None, category = None):

	context_dict = {}
	categories = Category.objects.all()
	
	context_dict['categories'] = categories
	if(request.method == 'POST'):
		check = request.POST.get('search')
		if check != None:
			search = check
		check = request.POST.get('choose')
		if check != None: 
			category = check
		if search != None:
			search = search.split(" ")
			searchS = "_".join(search)
		items = []

		if category != None and search != None:
			for word in search:
				items += Item.objects.filter((Q(description__contains = word) | Q(title__contains = word) & (Q(category = category) | Q(category = category))))
			
			context_dict['category'] = category
			context_dict['search'] = searchS

		elif search != None:	
			for word in search:
				items += Item.objects.filter(Q(description__contains = word ) | Q(title__contains = word))
			
			context_dict['search'] = searchS

		elif category != None:
				
				items = Item.objects.filter(Q(category = category) | Q(category = category))
				context_dict['category'] = category

		else:
			return home_page(request)
		
		context_dict['items'] = items
	
		return render(request, 'tailored/search.html', context_dict)
	else :
		render(request, 'tailored/index.html')


def home_page(request):
	context_dict = {}
	categories = Category.objects.all()
	
	context_dict['categories'] = categories

	#placeholder for homepage, feel free to change it.

	return render(request, 'tailored/index.html', context_dict)