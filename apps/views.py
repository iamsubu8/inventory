from django.shortcuts import render, HttpResponse ,redirect
from .models import *
import json
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from .decorator import *
from django.db.models import Q
from django.contrib import messages

def Login(request):
    if request.method == "POST":
        username = request.POST.get("username")
        password = request.POST.get("password")
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            messages.success(request, 'Loged In Succefully!')
            return redirect("product")
        else:
            return render(request, 'login.html', {'error_message': 'Invalid credentials'})
    return render(request, 'login.html')

def logout(request):
    try:
        logout(request)
        return redirect("login")    
    except Exception as e:
        print(e)
        return HttpResponse("Somthing went wrong")

# @unauthenticated_user
def Product(request):
    try:
        # print(request.user)
        if request.user.userprofile.roles.filter(Q(name='store') | Q(name='dprt')).exists():
            product=Inventory.objects.filter(status='approved').order_by('-id')

        context={
            'product':product
        }
        return render(request,'product.html',context=context)
    except Exception as e:
        print(e)
        messages.error(request, "Error in Item adding!")
        return redirect('product')

def AddPRODUCT(request):
    try:
        if request.method == "POST":
            if request.user.userprofile.roles.filter(name='store').exists():
                product=Inventory(
                    product_Id=request.POST.get('product_id'),
                    product_Name=request.POST.get('product_name'),
                    vendor=request.POST.get('vendor'),
                    mrp=request.POST.get('mrp'),
                    batch_num=request.POST.get('batch_number'),
                    batch_date=request.POST.get('batch_date'),
                    quantity=request.POST.get('quantity'),
                    status='approved'
                )
                product.save()
                messages.success(request, 'Product added succesfully!')
                return redirect('product')
            elif request.user.userprofile.roles.filter(name='dprt').exists():
                requestedData = {
                    'product_id': request.POST.get('product_id'),
                    'product_name': request.POST.get('product_name'),
                    'vendor': request.POST.get('vendor'),
                    'mrp': request.POST.get('mrp'),
                    'batch_number': request.POST.get('batch_number'),
                    'batch_date': request.POST.get('batch_date'),
                    'quantity': request.POST.get('quantity'),
                }
                RequestRecord.objects.create(
                    requested_user=request.user,
                    payload=json.dumps(requestedData),
                    request_status='pending',
                    action='Adding'
                )
                messages.success(request, 'Product sent for Approval!')
                return redirect('product')
            else:
                messages.warning(request, "You don't have permission!")
                return redirect('product')
    except Exception as e:
        print(e)
        messages.error(request, "Server Error!")
        return redirect('product')

def EditPRODUCT(request):
    try:
        if request.method == 'POST':
            if request.user.userprofile.roles.filter(name='store').exists():
                product = Inventory.objects.get(product_Id=request.POST.get('product_id'))
                product.product_Name=request.POST.get('product_name')
                product.vendor=request.POST.get('vendor')
                product.mrp=request.POST.get('mrp')
                product.batch_num=request.POST.get('batch_number')
                product.batch_date=request.POST.get('batch_date')
                product.quantity=request.POST.get('quantity')
                product.save()
                messages.success(request, 'Product Updated Successfully')
                return redirect('product')
            elif request.user.userprofile.roles.filter(name='dprt').exists():
                product = Inventory.objects.get(product_Id=request.POST.get('product_id'))
                requestedData = {
                    'product_id': request.POST.get('product_id'),
                    'product_name': request.POST.get('product_name'),
                    'vendor': request.POST.get('vendor'),
                    'mrp': request.POST.get('mrp'),
                    'batch_number': request.POST.get('batch_number'),
                    'batch_date': request.POST.get('batch_date'),
                    'quantity': request.POST.get('quantity'),
                }
                RequestRecord.objects.create(
                    requested_user=request.user,
                    payload=json.dumps(requestedData),
                    request_status='pending',
                    action='edit'
                )
                messages.success(request, 'Product sent for Approval!')
                return redirect('product')
            else:
                messages.warning(request, "You don't have permission!")
                return redirect('product')
        else:
            messages.error(request, 'Failed to update!')
            return redirect('product')
        
    except Exception as e:
        print(e)
        messages.error(request, "Server error!")
        return redirect("product")

def RemovePRODUCTS(request):
    try:
        if request.method == "POST":
            if request.user.userprofile.roles.filter(name='store').exists():
                product = Inventory.objects.get(product_Id=request.POST.get('product_id'))
                product.delete()
                messages.success(request, 'Product removed!')
                return redirect('product')
            elif request.user.userprofile.roles.filter(name='dprt').exists():
                product = Inventory.objects.get(product_Id=request.POST.get('product_id'))
                requestedData = {
                    'product_id': product.product_Id,
                    'product_name': product.product_Name,
                    'vendor':product.vendor,
                    'mrp': product.mrp,
                    'batch_number': product.batch_num,
                    'batch_date': str(product.batch_date),
                    'quantity':product.quantity,
                }
                print("reere", type(requestedData))
                RequestRecord.objects.create(
                    requested_user=request.user,
                    payload=json.dumps(requestedData),
                    request_status='pending',
                    action='delete'
                )
                messages.success(request, 'Product sent for Approval!')
                return redirect('product')

            else:
                messages.warning(request, 'You do not have permission to perform this action!')
                return redirect('product')
        else:
            messages.warning(request, 'Failed to remove!')
            return redirect('product')
    except Exception as e:
        print(e)
        return HttpResponse("server error!")

def JsonifyPayload(dict):
    dict['payload'] = json.loads(dict['payload'])
    return dict

def PendingProducts(request):
    try:
        if request.user.userprofile.roles.filter(Q(name='store') | Q(name='dprt')).exists():
            requestedData=RequestRecord.objects.all().order_by('-id')
            payloadData = [{'id':data.id,'product': json.loads(data.payload), 'action': data.action, 'status': data.request_status} for data in requestedData]
            context={
                'product': payloadData
            }
            return render(request,'pending.html',context=context)
        else:
            return HttpResponse("You don't have permission to perform this action.")
    except Exception as e:
        print(e)
        messages.error(request, "Server Error!")
        return redirect("pending")

def AproveProduct(request, recored_id):
    try:
        if request.user.userprofile.roles.filter(name='store').exists():
            request_ = RequestRecord.objects.get(id=recored_id)
            request_.request_status='approved'
            request_.save()
            messages.success(request, 'Product approved!')
            return redirect('pending')
        else:
            messages.warning(request, 'You do not have permisions!')
            return redirect("pending")
    except Exception as e:
        print(e)
        messages.error(request, "Server Error!")
        return redirect("pending")
    
def RejectProduct(request, recored_id):
    try:
        if request.user.userprofile.roles.filter(name='store').exists():
            request_ = RequestRecord.objects.get(id=recored_id)
            request_.request_status='rejected'
            request_.save()
            messages.success(request, 'Product Rejected!')
            return redirect('pending')
        else:
            messages.warning(request, 'You do not have permisions!')
            return redirect("pending")
    except Exception as e:
        print(e)
        messages.error(request, "Server Error!")
        return redirect("pending")
    
