from typing import Any
from django.db.models import F
from django.db.models.query import QuerySet
from django.http import HttpResponseRedirect
from django.shortcuts import get_object_or_404, render, redirect
from django.urls import reverse
from django.views import generic
from .models import Item, Choice, Customer, Customer_Cart, Order
from django.utils import timezone
from django.core.mail import send_mail
from django.conf import settings
import stripe, uuid, smtplib
from email.mime.text import MIMEText
# STRIPE SETUP.
stripe.api_key = settings.STRIPE_API_KEY
stripe.verify_ssl_certs = settings.STRIPE_VERIFY_SSL

# UNSIGNED-IN VERSION
def women_bag(request):
    women_bag_list = Item.objects.filter(category = "women_bag")
    context = {
        "women_bag_list": women_bag_list,
        "customer_service_email": settings.CUSTOMER_SERVICE_EMAIL,
    }
    return render(request, "AsianFashion/women_bag.html", context)

def women_phonecase(request):
    women_phonecase_list = Item.objects.filter(category = "women_phonecase")
    context = {
        "women_phonecase_list": women_phonecase_list,
        "customer_service_email": settings.CUSTOMER_SERVICE_EMAIL,
    }
    return render(request, "AsianFashion/women_phonecase.html", context)

def women_leather(request):
    women_leather_list = Item.objects.filter(category = "women_leather")
    context = {
        "women_leather_list": women_leather_list,
        "customer_service_email": settings.CUSTOMER_SERVICE_EMAIL,
    }
    return render(request, "AsianFashion/women_leather.html", context)

def men_bag(request):
    men_bag_list = Item.objects.filter(category = "men_bag")
    context = {
        "men_bag_list": men_bag_list,
        "customer_service_email": settings.CUSTOMER_SERVICE_EMAIL,
    }
    return render(request, "AsianFashion/men_bag.html", context)

def item_detail(request, item_id, error_message = None):
    context = {
        "item":Item.objects.get(pk=item_id),
        "item_id":item_id,
        "customer_service_email":settings.CUSTOMER_SERVICE_EMAIL
        }
    if error_message != None:
        context["error_message"] = error_message
    return render(request,"AsianFashion/item_detail.html",context)

# SIGNED-IN VERSION
def women_bag_signed_in(request, customer_uuid):
    women_bag_list = Item.objects.filter(category = "women_bag")
    customer = get_object_or_404(Customer, uuid=customer_uuid)
    context = {
        "women_bag_list": women_bag_list,
        "customer": customer,
        "customer_uuid": customer_uuid,
        "customer_service_email": settings.CUSTOMER_SERVICE_EMAIL,
    }
    return render(request, "AsianFashion/women_bag.html", context)

def women_phonecase_signed_in(request, customer_uuid):
    women_phonecase_list = Item.objects.filter(category = "women_phonecase")
    customer = get_object_or_404(Customer, uuid=customer_uuid)
    context = {
        "women_phonecase_list": women_phonecase_list,
        "customer": customer,
        "customer_uuid": customer_uuid,
        "customer_service_email": settings.CUSTOMER_SERVICE_EMAIL,
    }
    return render(request, "AsianFashion/women_phonecase.html", context)

def women_leather_signed_in(request, customer_uuid):
    women_leather_list = Item.objects.filter(category = "women_leather")
    customer = get_object_or_404(Customer, uuid=customer_uuid)
    context = {
        "women_leather_list": women_leather_list,
        "customer": customer,
        "customer_uuid": customer_uuid,
        "customer_service_email": settings.CUSTOMER_SERVICE_EMAIL,
    }
    return render(request, "AsianFashion/women_leather.html", context)

def men_bag_signed_in(request, customer_uuid):
    men_bag_list = Item.objects.filter(category = "men_bag")
    customer = get_object_or_404(Customer, uuid=customer_uuid)
    context = {
        "men_bag_list": men_bag_list,
        "customer": customer,
        "customer_uuid": customer_uuid,
        "customer_service_email": settings.CUSTOMER_SERVICE_EMAIL,
    }
    return render(request, "AsianFashion/men_bag.html", context)

def item_detail_signed_in(request, customer_uuid, item_id, error_message=None):
    customer = get_object_or_404(Customer, uuid=customer_uuid)
    item = get_object_or_404(Item, pk=item_id)
    context = {
        "customer": customer,
        "item": item,
        "item_id": item_id,
        "customer_uuid": customer_uuid,
        "customer_service_email": settings.CUSTOMER_SERVICE_EMAIL,
    }
    if error_message != None:
        context["error_message"] = error_message
    return render(request, "AsianFashion/item_detail.html", context)

def cart_signed_in(request, customer_uuid):
    customer = get_object_or_404(Customer, uuid=customer_uuid)
    tax_rate = 0.0625
    shipping_cost = 10
    # Display cart main page.
    if request.method == "GET":
        cart_object_list = Customer_Cart.objects.filter(customer__uuid = customer_uuid)
        order_total_amount = sum([cart_object.item.price for cart_object in cart_object_list])
        order_total_amount_with_tax = round(order_total_amount * (1+tax_rate),2)
        if order_total_amount > 150:
            shipping_cost = 0
        ######## TEST #########
        if order_total_amount <= 1:
            shipping_cost = 0
        #######################   
        total_amount = order_total_amount_with_tax + shipping_cost
        return render(request, "AsianFashion/customer_cart.html", 
                    {
                        "customer": customer,
                        "cart_object_list":cart_object_list,
                        "customer_uuid":customer_uuid,
                        "order_total_amount":order_total_amount,
                        "order_total_amount_with_tax":order_total_amount_with_tax,
                        "shipping_cost": shipping_cost,
                        "total_amount": total_amount
                    }
                )
    
    # Delete an item from cart.
    elif request.method == "POST":
        object = Customer_Cart.objects.get(pk=request.POST['cart_object_id'])
        object.delete()
        cart_object_list = Customer_Cart.objects.filter(customer__uuid = customer_uuid)
        order_total_amount = sum([cart_object.item.price for cart_object in cart_object_list])
        order_total_amount_with_tax = round(order_total_amount * (1+tax_rate), 2)
        if order_total_amount > 150:
            shipping_cost = 0
        ######## TEST #########
        if order_total_amount <= 1:
            shipping_cost = 0
        #######################   
        total_amount = order_total_amount_with_tax + shipping_cost
        return render(request, "AsianFashion/customer_cart.html", 
                    {
                        "customer": customer,
                        "cart_object_list":cart_object_list,
                        "customer_uuid":customer_uuid,
                        "order_total_amount":order_total_amount,
                        "order_total_amount_with_tax":order_total_amount_with_tax,
                        "shipping_cost": shipping_cost,
                        "total_amount": total_amount,
                        "error_message": "Item deleted."
                    }
                )

# UTILITIES
def sign_in(request):
    # Display the sign-in page.
    if request.method == "GET":
        context = {}
        # Collect item id and choice id
        if "item_id" in request.GET:
            context["item_id"] = request.GET["item_id"]
            if 'choice_id' in request.GET:
                context['choice_id'] = request.GET['choice_id']
        return render(request, "AsianFashion/sign_in.html", context)

    # Customer signed in.
    elif request.method=="POST":
        # Check if a customer exists.
        try:
            customer = Customer.objects.get(email=request.POST['email'], password=request.POST['password'])
        # Customer not exist, give an error message.
        except (Customer.DoesNotExist):
            context ={"error_message": "The email or password you entered is wrong."}
            if "item_id" in request.POST:
                context["item_id"] = request.POST["item_id"]
                if 'choice_id' in request.POST:
                    context["choice_id"] = request.POST["choice_id"]
            # Redirect to sign in page.
            return render(request, "AsianFashion/sign_in.html", context)
        # Else customer exists, direct to item page.
        if "item_id" in request.POST:
            # redirect to item detail page
            return item_detail_signed_in(
                request, 
                customer_uuid = customer.uuid,
                item_id = request.POST["item_id"],
                error_message="Successfully signed in."
            )
        # Else just sign in.
        else:
            # Direct to the main signed in page – woman bag.
            return women_bag_signed_in(request, customer.uuid)
        
def sign_up(request, error_message = None):
    # Display the sign up page.
    if request.method=="GET":
        context = {}
        # Collect item id.
        if "item_id" in request.GET:
            context["item_id"] = request.GET["item_id"]
        return render(request, "AsianFashion/sign_up.html",context) 
    # Customer signed up.
    elif request.method=="POST":
        context = {}
        # Collect error message
        if 'error_message' in request.POST:
            context["error_message"]= error_message
        # Collect item.
        if "item_id" in request.POST:
            context["item_id"] = request.POST["item_id"]
        try:
            # Check if customer already exists.
            customer = Customer.objects.get(email=request.POST['email'])
            context["error_message"] = "Account already exists, please sign in."
            # Direct to sign-in page.
            return render(request, "AsianFashion/sign_in.html", context)
        # Customer not exist, create a new record into the customer database.
        except (Customer.DoesNotExist):
            # Send an email to prove customer email is valid 
            try:
                '''send_mail(
                    "You have successfully registered on Asian Fashion",
                    "You can now sign in.",
                    'katherine@asianfashion.org',
                    [request.POST['email']],
                    fail_silently=False,
                )'''
                # Email is verified, create new customer.
                customer = Customer(uuid = uuid.uuid4(), email=request.POST['email'], password=request.POST['password'])
                customer.save()
                context["error_message"] = "Sign up success, you can now sign in."
                return render(request, "AsianFashion/sign_in.html", context)
            # Send_mail fails, email is invalid.
            except:
                context["error_message"] = "The email you entered is invalid. Please try again."
                # Redirect to sign up page.
                return render(request, "AsianFashion/sign_up.html", context)

def reset_password(request):
    # Display the reset password page.
    if request.method == "GET":
        context = {}
        # Collect item
        if "item_id" in request.GET:
            context["item_id"]=request.GET["item_id"]
        return render(request, "AsianFashion/reset_password.html",context)
    # Customer reset the password.
    else:
        context = {}
        # Collect item.
        if "item_id" in request.POST:
            context["item_id"] = request.POST["item_id"]    
        # Reset password.
        try:
            customer = Customer.objects.get(email = request.POST['email'])
            customer.password = request.POST["new_password"]
            customer.save()
            context["error_message"] = "Password changed successfully."
            return render(request,"AsianFashion/sign_in.html", context)
        except (Customer.DoesNotExist):
            error_message = "Account does not exist, please sign up."
            context["error_message"] = error_message
            return render(request, "AsianFashion/sign_up.html", context)

def sign_out(request):
    return women_bag(request)

def check_out(request):
    # Customer check out.
    if request.method == "POST":
        cart_object_list = Customer_Cart.objects.filter(customer__uuid=request.POST["customer_uuid"])
        # Create an order summary.
        order_summary = ""
        for object in cart_object_list:
            order_summary += object.item.title
            if object.choice != None:
                order_summary+= " "+object.choice.choice_text
            order_summary += " (quantity: 1). "
        # Add information to context.
        context = {
            "customer_uuid": request.POST["customer_uuid"],
            "total_amount": request.POST["total_amount"],
            "cart_object_list": cart_object_list,
            "order_summary": order_summary
            }
        return render(request, "AsianFashion/check_out.html", context)

def payment_success(request):
    #Initialize the context
    context = {}
    customer_service_email = settings.CUSTOMER_SERVICE_EMAIL
    context["customer_service_email"] = customer_service_email
    # Get order objects using session_id and set their status to paid.
    session_id = request.GET['session_id']
    order_list = Order.objects.filter(session_id = session_id)
    # Modify object status and add to description.
    for order_object in order_list:
        # Get order summary.
        order_summary = order_object.order_summary
        # Modify the status to paid.
        order_object.status = "paid"
        order_object.save()
        to_email = order_object.email
        # Customer signed in, collect customer id.
        if order_object.customer != None:
            context["customer_uuid"] = order_object.customer.uuid
    # Add order summary
    context["order_summary"] = order_summary
    # Email the customer about their order confirmation.
    try:
        send_mail(
            "Order Confirmation with Asian Fashion",
            "Your order #" + session_id + " has been confirmed. Here is the order detail: "+order_summary,
            customer_service_email,
            [to_email],
            fail_silently=False,
        )
    except:
        pass
    return render(request, "AsianFashion/payment_success.html", context)

def payment_cancel(request):
    context = {}
    # Get order list using session id.
    session_id = request.GET['session_id']
    order_list = Order.objects.filter(session_id = session_id)
    # Iterate through canceled objects.
    for order_object in order_list:
        # Get order summary.
        order_summary = order_object.order_summary
        # Re-add to cart if it was a cart object.
        if order_object.is_cart_object:
            cart_object = Customer_Cart(customer=order_object.customer, item=order_object.item)
            # add choice
            if order_object.choice != None:
                cart_object.choice = order_object.choice
            cart_object.save()
            context["customer_uuid"] = order_object.customer.uuid
        # Customer sign in but not checking out a cart object.
        elif order_object.customer != None:
            context["customer_uuid"] = order_object.customer.uuid
        # Delete object from Order DB.
        order_object.delete()
    context['order_summary'] = order_summary
    return render(request, "AsianFashion/payment_cancel.html", context)

def pay(request):
    # Make a payment.
    if request.method == "POST":
        # Collect request information.
        context = {}
        if "cart_object_list" in request.POST:
            context["cart_object_list"] = request.POST["cart_object_list"]
        if "customer_uuid" in request.POST:
            context["customer_uuid"] = request.POST["customer_uuid"]
        if "item_id" in request.POST:
            context["item_id"] = request.POST["item_id"]
        if "choice_id" in request.POST:
            context["choice_id"] = request.POST["choice_id"]
        context["order_summary"] = request.POST["order_summary"]
        context["total_amount"] = request.POST["total_amount"]

        # Retrieve order information.
        order_summary = request.POST["order_summary"]
        total_amount = request.POST["total_amount"]
        invalid_mailing_info = False

        # Get mailing information.
        first_name = request.POST["first_name"]
        last_name = request.POST["last_name"]
        email = request.POST["email"]
        phone_number = request.POST["phone_number"]
        street_line_1 = request.POST["street_address_line_1"]
        street_line_2 = request.POST["street_address_line_2"]
        city = request.POST["city"]
        state = request.POST["state"]
        zip_code = request.POST["zip_code"]
        # Check first name.
        if first_name == "":
            error_message = "First name cannot be empty."
            invalid_mailing_info = True
        # Check last name.
        elif last_name == "":
            error_message = "Last name cannot be empty."
            invalid_mailing_info = True
        # Check email.
        elif email == "":
            error_message = "Email cannot be empty."
            invalid_mailing_info = True
        # Check phone number.
        elif phone_number == "":
            error_message = "Phone number cannot be empty."
            invalid_mailing_info = True
        # Check street address.
        elif street_line_1 =="":
            error_message="Street address line 1 cannot be empty."
            invalid_mailing_info = True
        # Check city.
        elif city == "":
            error_message = "City cannot be empty."
            invalid_mailing_info = True
        # Check state.
        elif state == "":
            error_message = "State cannot be empty."
            invalid_mailing_info = True
        # Check zip code.
        elif zip_code == "":
            error_message = "Zip code cannot be empty."
            invalid_mailing_info = True

        # Redirect back if mailing information is invalid.
        if invalid_mailing_info:
            context["error_message"]=error_message
            return render(request,"AsianFashion/check_out.html", context)

        # Create a payment.
        session = stripe.checkout.Session.create(
            line_items=[{
                            'price_data': 
                            {
                                'currency': 'usd',
                                'product_data': 
                                {
                                    'name': 'Order (including sales tax and shipping fee)',
                                },
                                'unit_amount': int(float(request.POST["total_amount"])*100),
                            },
                            'quantity': 1,
                        }],
            mode='payment',
            # Pass the session id to urls.
            success_url="http://127.0.0.1:8000/AsianFashion/payment_success?session_id={CHECKOUT_SESSION_ID}",
            cancel_url="http://127.0.0.1:8000/AsianFashion/payment_cancel?session_id={CHECKOUT_SESSION_ID}"
        )
        # Retrieve session id.
        session_id = session.id
        # Customer check out their cart.
        if "customer_uuid" in request.POST and "item_id" not in request.POST:
            cart_object_list = Customer_Cart.objects.filter(customer__uuid=request.POST["customer_uuid"])
            for object in cart_object_list:
                order_object = Order(
                    order_summary=order_summary,
                    session_id = session_id,
                    item = object.item,
                    amount = object.item.price * 100,
                    customer = object.customer,
                    first_name = first_name,
                    last_name = last_name,
                    email = email,
                    phone_number = phone_number,
                    street_address_line_1 = street_line_1,
                    street_address_line_2 = street_line_2,
                    city = city,
                    state = state,
                    zip_code = zip_code,
                    order_date = timezone.now(),
                    is_cart_object = True,
                )
                # Collect choice.
                if object.choice != None:
                    order_object.choice = object.choice
                order_object.save()
                # Delete the object from customer's cart.
                object.delete()
        # Customer sign in and directly purchase an item from item page.
        elif "customer_uuid" in request.POST:
            item = Item.objects.get(pk=request.POST["item_id"])  
            order_object = Order(
                order_summary=order_summary,
                session_id = session_id,
                item = item,
                amount = int(float(total_amount) * 100),
                customer = Customer.objects.get(uuid=request.POST["customer_uuid"]),
                first_name = first_name,
                last_name = last_name,
                email = email,
                phone_number = phone_number,
                street_address_line_1 = street_line_1,
                street_address_line_2 = street_line_2,
                city = city,
                state = state,
                zip_code = zip_code,
                order_date = timezone.now(),
                is_cart_object = False,
            )
            # Collect choice.
            if 'choice_id' in request.POST:
                order_object.choice = item.choice_set.get(pk=request.POST['choice_id'])
            order_object.save()
        # Customer not sign in and directly purchase an item.
        else:
            order_object = Order(
                order_summary=order_summary,
                session_id = session_id,
                item = Item.objects.get(pk=request.POST["item_id"]),
                amount = int(float(total_amount) * 100),
                customer = None,
                first_name = first_name,
                last_name = last_name,
                email = email,
                phone_number = phone_number,
                street_address_line_1 = street_line_1,
                street_address_line_2 = street_line_2,
                city = city,
                state = state,
                zip_code = zip_code,
                order_date = timezone.now(),
                is_cart_object = False,
            )
            # Collect choice.
            if 'choice_id' in request.POST:
                order_object.choice = Item.objects.get(pk=request.POST["item_id"]).choice_set.get(pk=request.POST['choice_id'])
            order_object.save()
        return redirect(session.url, code=303)  

def buy_or_add_item_to_cart(request, item_id):
    # Tax rate and shipping costs
    tax_rate = 0.0625
    shipping_cost = 10
    # Signed-in version.
    if 'customer_uuid' in request.POST:
        # Buy.
        if 'buy' in request.POST:
            item = get_object_or_404(Item, pk=item_id)
            order_amount = item.price
            order_amount_with_tax = round(order_amount*(1+tax_rate),2)
            ######## TEST #########
            if order_amount == 1:
                shipping_cost = 0
            #######################    
            if order_amount > 150:
                shipping_cost = 0
            total_amount = order_amount_with_tax + shipping_cost
            customer_uuid =request.POST["customer_uuid"]
            context = {
                "total_amount": total_amount,
                "customer_uuid": customer_uuid,
                "item_id": item_id,
            }
            order_summary = item.title + " quantity: 1"
            # Collect choice
            if "have_choice" in request.POST:
                if 'choice' in request.POST:
                    context['choice_id'] = request.POST["choice"]
                    context['choice_text'] = item.choice_set.get(pk=request.POST["choice"]).choice_text
                    order_summary += "("+context['choice_text']+")"
                # Choice is not selected, redirect back.
                else:
                    error_message = "Please select a choice."
                    return item_detail_signed_in(
                                request,
                                customer_uuid = customer_uuid, 
                                item_id = item_id,
                                error_message = error_message
                            )
            # Add order summary.
            context["order_summary"] = order_summary
            # Direct to checkout page.
            return render(request, "AsianFashion/check_out.html", context)
        
        # Add item to cart.
        elif 'add-to-cart' in request.POST:
            customer = get_object_or_404(Customer, uuid=request.POST['customer_uuid'])
            item = get_object_or_404(Item, pk=item_id)
            # Check if item has a choice.
            if "have_choice" in request.POST:
                if 'choice' in request.POST:
                    new_cart_item = Customer_Cart(customer=customer, item=item)
                    new_cart_item.choice = item.choice_set.get(pk = request.POST["choice"])
                    new_cart_item.save()
                else:
                    error_message = "Please select a choice."
                    return item_detail_signed_in(
                                request, 
                                customer_uuid = customer.uuid, 
                                item_id = str(item.id),
                                error_message = error_message
                            )      
            # Customer signed in, add item to cart.
            else:
                new_cart_item = Customer_Cart(customer=customer, item=item)
                new_cart_item.save()
            # Redirect to item detail page.
            return item_detail_signed_in(
                        request, 
                        customer_uuid = customer.uuid,
                        item_id = str(item.id),
                        error_message = "Succefully added to cart."
                    )
    # Customer not sign in.
    else:
        # Buy the item.
        if 'buy' in request.POST:
            item = get_object_or_404(Item, pk=item_id)
            order_amount = item.price
            order_amount_with_tax = round(order_amount*(1+tax_rate),2)
            if order_amount > 150:
                shipping_cost = 0
            ######## TEST #########
            if order_amount == 1:
                shipping_cost = 0
            #######################   
            total_amount = order_amount_with_tax+shipping_cost
            order_summary = item.title + " quantity: 1"
            context = {
                        'total_amount':total_amount,
                        "item_id":item_id
                    }
            # Collect choice
            if 'have_choice' in request.POST:
                if 'choice' in request.POST:
                    context['choice_id'] = request.POST["choice"]
                    context['choice_text'] = item.choice_set.get(pk=request.POST["choice"]).choice_text
                    order_summary+="("+context['choice_text']+")"
                # Direct to item detail page if choice is not selected.
                else:
                    error_message = "Please select a choice."
                    return item_detail(
                        request,
                        item_id = item_id,
                        error_message = error_message
                    )
            # Add order summary
            context['order_summary'] = order_summary
            # Go to checkout page.
            return render(request, "AsianFashion/check_out.html", context)
        # Add item to cart.
        elif 'add-to-cart' in request.POST:
            context = {
                        "item_id": item_id
                    }   
            # Direct to sign in page.
            return render(request, "AsianFashion/sign_in.html", context)