from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.http import JsonResponse
from django.views.decorators.http import require_POST

from .models import Product, Category, Order, OrderItem
from .cart import Cart
from .forms import CheckoutForm, RegisterForm


def product_list(request):
    categories = Category.objects.all()
    products = Product.objects.filter(available=True)

    category_slug = request.GET.get('category')
    search_query = request.GET.get('q', '').strip()
    sort = request.GET.get('sort', 'newest')

    selected_category = None
    if category_slug:
        selected_category = get_object_or_404(Category, slug=category_slug)
        products = products.filter(category=selected_category)

    if search_query:
        products = products.filter(name__icontains=search_query)

    if sort == 'price_asc':
        products = products.order_by('price')
    elif sort == 'price_desc':
        products = products.order_by('-price')
    elif sort == 'name':
        products = products.order_by('name')
    else:
        products = products.order_by('-created_at')

    context = {
        'products': products,
        'categories': categories,
        'selected_category': selected_category,
        'search_query': search_query,
        'sort': sort,
    }
    return render(request, 'store/product_list.html', context)


def product_detail(request, slug):
    product = get_object_or_404(Product, slug=slug, available=True)
    # show a few related products from the same category
    related = Product.objects.filter(category=product.category, available=True).exclude(id=product.id)[:4]
    return render(request, 'store/product_detail.html', {
        'product': product,
        'related': related,
    })


def category_detail(request, slug):
    category = get_object_or_404(Category, slug=slug)
    products = Product.objects.filter(category=category, available=True)
    return render(request, 'store/product_list.html', {
        'products': products,
        'categories': Category.objects.all(),
        'selected_category': category,
        'search_query': '',
        'sort': 'newest',
    })


def cart_detail(request):
    cart = Cart(request)
    return render(request, 'store/cart.html', {'cart': cart})


@require_POST
def cart_add(request, product_id):
    cart = Cart(request)
    product = get_object_or_404(Product, id=product_id, available=True)
    quantity = int(request.POST.get('quantity', 1))
    cart.add(product, quantity=quantity)

    # return json for ajax requests (product listing page)
    if request.headers.get('x-requested-with') == 'XMLHttpRequest':
        return JsonResponse({'cart_count': len(cart), 'total': str(cart.get_total_price())})

    messages.success(request, f'"{product.name}" added to cart.')
    return redirect('cart_detail')


@require_POST
def cart_update(request, product_id):
    cart = Cart(request)
    product = get_object_or_404(Product, id=product_id)
    quantity = int(request.POST.get('quantity', 1))
    cart.add(product, quantity=quantity, override_quantity=True)
    return redirect('cart_detail')


@require_POST
def cart_remove(request, product_id):
    cart = Cart(request)
    product = get_object_or_404(Product, id=product_id)
    cart.remove(product)
    return redirect('cart_detail')


def checkout(request):
    cart = Cart(request)

    if cart.is_empty():
        messages.warning(request, 'Your cart is empty.')
        return redirect('product_list')

    # pre-fill form if user is logged in
    initial = {}
    if request.user.is_authenticated:
        initial = {
            'first_name': request.user.first_name,
            'last_name': request.user.last_name,
            'email': request.user.email,
        }

    form = CheckoutForm(request.POST or None, initial=initial)

    if request.method == 'POST' and form.is_valid():
        order = Order.objects.create(
            user=request.user if request.user.is_authenticated else None,
            first_name=form.cleaned_data['first_name'],
            last_name=form.cleaned_data['last_name'],
            email=form.cleaned_data['email'],
            phone=form.cleaned_data['phone'],
            address=form.cleaned_data['address'],
            city=form.cleaned_data['city'],
            postal_code=form.cleaned_data['postal_code'],
        )

        for item in cart:
            OrderItem.objects.create(
                order=order,
                product=item['product'],
                quantity=item['quantity'],
                price=item['price'],
            )
            # reduce stock
            item['product'].stock -= item['quantity']
            item['product'].save()

        order.calculate_total()
        cart.clear()
        return redirect('order_confirm', order_id=order.id)

    return render(request, 'store/checkout.html', {'cart': cart, 'form': form})


def order_confirm(request, order_id):
    order = get_object_or_404(Order, id=order_id)
    return render(request, 'store/order_confirm.html', {'order': order})


@login_required
def order_list(request):
    orders = Order.objects.filter(user=request.user).prefetch_related('items__product')
    return render(request, 'store/order_list.html', {'orders': orders})


def login_view(request):
    if request.user.is_authenticated:
        return redirect('product_list')

    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        if user:
            login(request, user)
            next_url = request.GET.get('next', 'product_list')
            return redirect(next_url)
        messages.error(request, 'Invalid username or password.')

    return render(request, 'store/login.html')


def logout_view(request):
    logout(request)
    return redirect('product_list')


def register_view(request):
    if request.user.is_authenticated:
        return redirect('product_list')

    form = RegisterForm(request.POST or None)
    if request.method == 'POST' and form.is_valid():
        user = form.save()
        login(request, user)
        messages.success(request, 'Account created! Welcome.')
        return redirect('product_list')

    return render(request, 'store/register.html', {'form': form})
