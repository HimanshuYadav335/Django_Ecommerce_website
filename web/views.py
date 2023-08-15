from django.shortcuts import render
# from .forms import StudentRegistration
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
# from django.contrib import auth
from .models import Visitor,ProductDetail,Cartdetail,Order
from django.shortcuts import redirect
from .utils import sent_mail_to_client
from django.http import HttpResponse,JsonResponse
from django.contrib.auth.hashers import check_password
from django.contrib.auth.hashers import make_password

import json
import razorpay
from Ecommerce.settings import RAZORPAY_API_KEY,RAZORPAY_API_SECRET_KEY
def import_product_data(request):
    with open('C:\\venv\Ecommerce\web\data\products.json', 'r') as file:
        products = json.load(file)

    for product in products:
        new_product = ProductDetail(
            pid=product['pid'],
            pimage=product['pimage'],
            pdetail=product['pdetail'],
            pprice=product['pprice'],
            ptitle=product['ptitle']
            
        )
        new_product.save()
      
        print("ok")
    return HttpResponse("whoel data enterd")
def show(request):
    search_value=request.GET.get('searchproduct')
    user_name=None
    try:
      user_pass=request.session.get('password')
      # user_name=user_name.split("@")[0]
      user_name=Visitor.objects.get(epass=user_pass)
      user_name=user_name.ename
      print(user_pass,user_name,"llllllllllllllllllllllllllllllllllll")

    except:
      pass
    if search_value:
      update_search_value=search_value.strip()
    # print(search_value,"search value")
    if search_value!=None:
      fm=ProductDetail.objects.filter(ptitle__icontains=update_search_value.lower())
      if fm:

        return render(request,'home.html',{"fm":fm,"user_name":user_name})
      return redirect("http://127.0.0.1:8000/home/")

    # if request.method=="POST":
    #     fm=StudentRegistration(request.POST)
    #     if fm.is_valid():
    #         try:
    #             fm.save()
    #         except Exception as e:
    #             print(e)
    #         retu
    # rn redirect("/")
    # else:
    #     fm=StudentRegistration()
    #     return render(request,'home..html') 

    fm=ProductDetail.objects.all()
    # print(User)
    print(request.session.get('email'),"session on home page")
    # if request.user.is_authenticated:
    #     current_user=request.User
    #     print(current_user.id,"ok")
    # print(fm,"fm")
    # print(request.session['email'],"home")
    return render(request,'home.html',{"fm":fm,"user_name":user_name})

def send_mail_on_signup(request):
  user_name=None
  if request.method=="POST":
    user_email=request.POST.get('email')
    user_pass=request.POST.get('pass2')
    user_pass2=request.POST.get('pass2')
    user_image=request.FILES.get('eimage')
    user_name=request.POST.get('ename')
    user_message=f"Hello {user_name} \n your account is created successfully ."
    # print(user_image)
    saved_pass=Visitor.objects.all()

    print(user_email,"ok")
    if user_email=="" or user_pass=="" or user_pass2=="" or user_name=="":
      return render(request,'signup.html',{'error':"Any field can't be empty"})
    elif user_pass!=user_pass2:
      return render(request,'signup.html',{'error':"Password not matched  "})
    else:
     try:
      for id in saved_pass:
        if id.epass==user_pass:
          print(id.epass)
          return render(request,'signup.html',{'error':"Password Already taken "})
      if (user_pass==user_pass2):
       print(user_image)
      #  user_pass=make_password(user_pass)
       userpresent=Visitor.objects.create(eemail=user_email,epass=user_pass,eimage=user_image,ename=user_name)
       userpresent.save()
       sent_mail_to_client(user_email,user_name,user_message)
      
       return redirect('http://127.0.0.1:8000/home/')
     except Exception as e:
        print(e)
        return HttpResponse("server error")
  else:
      
     try:
          user_pass=request.session.get('password')
          user_name=Visitor.objects.get(epass=user_pass)
          user_name=user_name.ename
     except:
       pass

     return render(request,'signup.html',{'user_name':user_name})
  
def send_mail_on_login(request):
    if request.method == 'POST':
        user_email = request.POST.get('eemail')
        user_pass = request.POST.get('epass')
        # cutomer=Visitor.objects.get(epass=user_pass)
        user_name=None
        print(user_pass,user_email)

        users = Visitor.objects.filter(eemail=user_email)
        print(users)
        if users:
            print(users,"ok")
            # Iterate over the queryset and check each user's password
            try:
              for user in users:
                print(users,"inside for loop")
                print(user.epass,type(user.epass),type(user_pass))
                if user.epass == int(user_pass):
                    print("gggggggggggggggggggggggggggggggggggggggggggggggggggggggggg",user.epass)
                    # Password matches for at least one user
                    # Proceed with further actions
                    user_message=f"Hello {user.ename} \n your have successfully login ."

                    request.session['email']=user_email
                    request.session['password']=user_pass
                    request.session.set_expiry(0)
                    print(request.session['email'],"i am session")
                    # request.session.set_expiry(10)  # Set session timeout to 5 seconds
                    try:sent_mail_to_client(user_email,user_name,user_message)
                    except:return redirect('http://127.0.0.1:8000/home/')

              return redirect('http://127.0.0.1:8000/home/')
            except:
            # Password does not match for any user
             error_message = 'Invalid email or password'
             return render(request, 'login.html',{'error_message':error_message})

        else:
            # No user found with the provided email
            error_message = 'Invalid email or password'
            # return render(request, 'login.html', {'error_message': error_message})
            print("no match")
            return render(request, 'login.html',{'error_message':error_message})

    else:
        # Render the login form
        return render(request, 'login.html')

def logout(request):
 if 'email' in request.session:
  # session_value = request.session.get('email')
    del request.session['email']
 if 'password' in request.session:
    del request.session['password']
    request.session.save()
    print("logout")
    return redirect('http://127.0.0.1:8000/home/')
 else:
    return redirect('http://127.0.0.1:8000/home/')



def product_detail(request,id):
 if 'email' in request.session:
   print(request.session['email'],"i am session")
   password = request.session.get('password')
   product=ProductDetail.objects.get(pid=id)
   fix_price=ProductDetail.objects.all()
   user_name=Visitor.objects.get(epass=password)
   cart_detail=None
   get_all_product=Cartdetail.objects.filter(userid=password)
   
   try:
       cart_detail=Cartdetail.objects.get(pid=id,userid=password)
       return JsonResponse({"response":"success"},status=200)

   except:
       cart_detail=Cartdetail.objects.create(pid=id,pimage=product.pimage,pdetail=product.pdetail,pprice=product.pprice, ptitle=product.ptitle,pnumber=1,userid=password )
       cart_detail.save()
       return JsonResponse({"response":"success"},status=200)

    
  #  if cart_detail:
  #        return render(request,'cart.html',{"product":get_all_product,"fix_price":fix_price,"user_name":user_name.ename})
  #  else:
  #    cart_detail=Cartdetail.objects.create(pid=id,pimage=product.pimage,pdetail=product.pdetail,pprice=product.pprice, ptitle=product.ptitle,pnumber=1,userid=password )
  #   #  return render(request,'cart.html',{"product":get_all_product,"fix_price":fix_price,"user_name":user_name.ename})
  #   #  return redirect("http://127.0.0.1:8000/cart")
  #    return JsonResponse({"response":"success"},status=200)

 else:
      return render(request,'login.html')

 

def inc_dec(request,id):
  if request.method=="POST":
    pquantity = request.POST.get('pquantitiy')
    pprice=request.POST.get('pprice')
    password=request.session.get('password')
    print(pquantity,pprice,"okkkkkkkkkk")

    # if pquantity.is_valid():
    if pquantity:
      print(pquantity,"okkkkkkkkkkkk")
      obj=Cartdetail.objects.get(pid=id,userid=password)
      obj.pnumber=pquantity
      obj.pprice=pprice
      obj.save()
      return JsonResponse({"response":"success"},status=200)
  return JsonResponse({"response": "error"}, status=400)
def delete_cart(request,id):
   password=request.session.get('password')
   product=Cartdetail.objects.get(pid=id,userid=password)
   product.delete()
   return redirect('http://127.0.0.1:8000/cart')


client=razorpay.Client(auth=(RAZORPAY_API_KEY,RAZORPAY_API_SECRET_KEY))
def cart_detail(request):
  if 'email' in request.session:
   password=request.session.get('password')
  #  user_name=request.session.get('user_name')
   product=Cartdetail.objects.filter(userid=password)
  #  productdetail=ProductDetail.objects.all()
   product_ids = product.values_list('pid', flat=True)  # Get the product IDs from the Cartdetail queryset
   productdetail = ProductDetail.objects.filter(pid__in=product_ids)  # Filter ProductDetail objects based on matching IDs
   user_name=Visitor.objects.get(epass=password)
   print(productdetail)
   for i in productdetail:
    print(i.pprice)
   return render(request,'cart.html',{'product':product,"fix_price":productdetail,"user_name":user_name.ename})
  else:
    return render(request,'login.html')

def proceed_order(request,id):
   password=request.session.get('password')
   product_in_order=None
   try:
    product_in_order=Order.objects.get(pid=id,userid=password)
    print(product_in_order)
   except:
    pass
   if product_in_order:
    return redirect('http://127.0.0.1:8000/cart')
   product1=Cartdetail.objects.get(pid=id,userid=password)
   product=Cartdetail.objects.filter(userid=password)
  #  product=Cartdetail.objects.filter(userid=password)
   print(product)
   user=Visitor.objects.get(epass=password)
   cart_detail=Order.objects.create(pid=product1.pid,ptitle=product1.ptitle,pprice=product1.pprice,pnumber=product1.pnumber,ename=user.ename,eemail=user.eemail,userid=product1.userid)
   user_message = f'Hello {user.ename},\n\nYou have confirmed  your order for: \n\n{product1.ptitle} (Price: {product1.pprice} $, Quantity: {product1.pnumber}). We will deliver your order shortly'
   user_email=user.eemail
   user_name=user.ename
   cart_detail.save()
  #  product_ids = product.values_list('pid', flat=True)  # Get the product IDs from the Cartdetail queryset
   product_ids = Cartdetail.objects.filter(userid=password).values_list('pid', flat=True)

   productdetail = ProductDetail.objects.filter(pid__in=product_ids)  # Filter ProductDetail objects based on matching IDs


   try:
    sent_mail_to_client(user_email,user_name,user_message)
   except Exception as e:
     return HttpResponse("server problam")
  
   return  render(request,'cart.html',{'product':product,"fix_price":productdetail,"user_name":user_name})


def order_status(request):
  password=request.session.get('password')
  order=Order.objects.filter(userid=password)
  product=Cartdetail.objects.filter(userid=password)
  j=0
  for i in product:
    print(i.pimage)
    print(j)
    j+=1
  return render(request,'status.html',{"order":order,"product":product})



def contact(request):
  if request.method=="POST":
    user_email=request.POST.get('owner_email')
    user_email2=request.POST.get('email')
    user_name=request.POST.get('name')
    user_message=request.POST.get('message')
    user_message=user_message+f'\t{user_email2}'
    try:
      sent_mail_to_client(user_email,user_name,user_message)
      return redirect("http://127.0.0.1:8000/home/")
    except:
      return HttpResponse("server Error")

  else:
    return render(request,'contact.html')



def generate_razorpay_order(request, productID):
    if 'email' in request.session:
        password = request.session.get('password')
        # product = Cartdetail.objects.filter(userid=password, pid=product_id).first()
        product = Cartdetail.objects.get(pid=productID,userid=password )
        print("hhhhhhhhhhhhhhhhhhhhhhh")
        print(product)
        if not product:
            return JsonResponse({"error": "Product not found in cart"}, status=400)
        
        client = razorpay.Client(auth=(RAZORPAY_API_KEY, RAZORPAY_API_SECRET_KEY))
        amount_in_paise = int(product.pprice * 100)  # Amount in paise (multiply by 100)
        order_currency = "INR"  # You can modify this based on your currency requirement
        
        order_data = {
            "amount": amount_in_paise,
            "currency": order_currency,
            "receipt": f"order_{productID}",  # You can generate a receipt based on your requirement
            # Add any additional data you need in the notes field
            # "notes": {
            #     "product_name": product.pname,
            #     "product_id": product_id,
            # }
        }

        order = client.order.create(data=order_data)
        return JsonResponse({"order_id": order['id'], "amount": amount_in_paise})
    else:
        return JsonResponse({"error": "User not logged in"}, status=403)

# def cart(request,id):
#    password=request.session.get('password')
#    product_detail=ProductDetail.objects.filter(userid=password)
#    cart_detail=O
  

# def  send_mail_on_login(request):
#     if request.method=="POST":
#       user_email=request.POST.get('email')
#       user_password=request.POST.get('pass')
#       try: 
#         users = User.objects.filter(email=user_email)
#       except User.DoesNotExist:
#         return HttpResponse("user not exits")

# def inc_dec(request,id):
#     if request.method=="POST":
     
#        product_quantity=request.POST.get('quantity')
#        print(id,product_quantity)
       
#        try:
#         product=Cartdetail.objects.get(pid=id)
#         print(product,"ok")
#         product.pnumber=product_quantity
        
#         product.save()
#         return redirect("http://127.0.0.1:8000/cart")
#        except Exception as e:
#         return HttpResponse("error occur")
#     return HttpResponse("invalid request")