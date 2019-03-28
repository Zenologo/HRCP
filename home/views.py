from django.http import HttpResponseRedirect
from django.shortcuts import get_list_or_404, render
from .forms import SearchForm
#from product.models import Product
from merchant.models import PriceMonitor, MerchantProduct
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger

def home_page(request):

    if request.method == 'POST':
        # create a form instance and populate it with data from the request:
        form = SearchForm(request.POST)
        print("home page begin")
        # check whether it's valid:
        if form.is_valid(): 

            var_tmp = form.cleaned_data['main_search']
            #lst_product = get_list_or_404(Product, name__contains=var_tmp)
            # lst_product = Product.objects.filter(name__contains = var_tmp)

            lst_product = PriceMonitor.objects.filter(merchant_product__product__name__contains = var_tmp)
            paginator = Paginator(lst_product, 20)
            products = paginator.page(1)
            print(products)

            total = len(lst_product)
            print("Total: " + str(total))
            
            # Reorganise product's info.
            lst_items = get_page_products(lst_product, products.start_index() - 1, products.end_index())
            return render(request, 'home/resultat.html', {'lst_product': lst_items, 
                                                            'total_results': total,                         
                                                            'serach_form' :form,
                                                            'pages': products
                                                            })
        else:
            return render(request, 'home/thanks.html')
    # if a GET (or any other method) we'll create a blank form
    elif request.method == 'GET':
        page_current = request.GET.get('page')
        if page_current == None:
            form = SearchForm()

            return render(request, 'home/home.html', {'serach_form': form})            
        else:
            
            
            page_current = request.GET.get('page', 1)
            lst_product = PriceMonitor.objects.filter(merchant_product__product__name__contains = var_tmp)
            paginator = Paginator(lst_product, 20)

            try:
                products = paginator.page(page_current)
            except PageNotAnInteger:
                products = paginator.page(1)
            except EmptyPage:
                products = paginator.page(paginator.num_pages)
            

def get_page_products(lst_product, start_index, end_index):
    set_name = set()
    lst_items = []
    for item in lst_product:
        if item.merchant_product not in set_name:
            """ Create a new item in result list"""
            set_name.add(item.merchant_product)
            item_prod = ItemSearch()
            item_prod.name = item.merchant_product.product.name
            item_prod.brand = item.merchant_product.brand
            item_prod.description = item.description

            item_prod.price_max = item.price
            item_prod.price_min = item.price

            item_prod.url = "http://127.0.0.1"
            lst_items.append(item_prod)
        else:
            for price_item in lst_items:
                """ Update price range """
                if price_item.name == item.merchant_product:
                    if price_item.price_max < item.price:
                        price_item.price_max = item.price
                    elif price_item.price > item.price:
                        price_item.price = item.price
                    break
    return lst_items[start_index:end_index]


def thanks_page(request):
    return render(request, 'home/thanks.html')

def resultat_page(request):
    return render(request, 'resulat.html')


class ItemSearch:
    """
        All results of search page.
    """
    def __init__(self):
        self.price_min = 0
        self.price_max = 0
        self.name = "product name"
        self.description = "product description"
        self.brand = "product's brand"
        self.url = "http://127.0.0.1"

