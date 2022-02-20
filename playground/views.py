from django.shortcuts import render
from django.http import HttpResponse
# exception import when using Objects.get()
from django.core.exceptions import ObjectDoesNotExist
# using Q onjects to filter querysets with or
from django.db.models import Q, F
from store.models import Product

# Create your views here.


def say_hello(request):
  # every model has an attribute called .objects, this returns a manager object
  # it is an interface to the DB
  # .objects also has methods for querying and manipulating data
  # all -> all the objects in product table, get -> single object, filter e.t.c
    # this methods return a queryset
    # the do not do anything immediately until other actions are called on them
    """ query_set = Product.objects.all()
    for product in query_set:
        print(product) """

    # using the get method, with exception handler.
    """ try:
      product = Product.objects.get(pk=1)
    except ObjectDoesNotExist:
      pass """

    # a better way of getting without try and catch
    #product = Product.objects.filter(pk=0).first()
    # check if it exists at all
    #exists = Product.objects.filter(pk=0).exists()
    #query_set = Product.objects.filter(unit_price=20)
    # for greater than or less than we use __gt and __lt, gte, lte
    # queryset api docs, more examples below
    #query_set = Product.objects.filter(unit_price__range=(20, 30))
    #query_set = Product.objects.filter(collection__id__range=(1, 2, 3))
    # query_set = Product.objects.filter(title__contains='coffee') #case insenstive
    # query_set = Product.objects.filter(
    # title__icontains='coffee')  # case senstive
    # query_set = Product.objects.filter(last_update__year=2021)

    ####### Q OBJECTS #####
    # Products: inventory < 10 AND price < 20
    # one way of solving this
    #query_set = Product.objects.filter(inventory__lt=10, unit_price__lt=20)
    # another
    """ query_set = Product.objects.filter(
        inventory__lt=10).filter(unit_price__lt=20) """

    # Products: inventory < 10 OR price < 20
    # | => || , & => &&, ~ => !=
    """ query_set = Product.objects.filter(
        Q(inventory__lt=10) | Q(unit_price__lt=20)) """

    ###### REFRENCING FIELDS USING F-Objects ######
    # we want ro compare two fields
    # query_set = Product.objects.filter(inventory=F('unit_price'))

    #### SORTING DATA #####
    # sort all products by ascending order (Default)
    # to change default you negate the keyword eg '-title'
    # can concat operations as well
    #query_set = Product.objects.filter(collection__id=1).order_by('unit_price')
    #query_set = Product.objects.order_by('unit_price','title')
    # used in returning lists
    # return render(request, 'hello.html', {'name': 'Obi', 'products': list(query_set)})

    # get just first product
    #product = Product.objects.order_by('unit_price')[0]
    # using earliest, latest they return objects
    #product = Product.objects.earliest('unit_price')
   # return render(request, 'hello.html', {'name': 'Obi', 'product': product})

   ####### LIMITING RESULTS #########
   # returns first five objects
    #query_set = Product.objects.all()[:5]
    # return render(request, 'hello.html', {'name': 'Obi', 'products': list(query_set)})

  ######### Selecting Fields to Table #############
  # this return a dictionary of objects, we can get related fields as well
  # related fields like collection__title
  # object.values_list() returns a tuple
  # .distinct() eliminates duplicates
    query_set = Product.objects.values(
        'id', 'title', 'collection__title').distinct()
    return render(request, 'hello.html', {'name': 'Obi', 'products': list(query_set)})
