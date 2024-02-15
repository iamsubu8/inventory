from django.shortcuts import render
from .models import *
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from django.contrib.auth import authenticate, login, logout
from rest_framework_simplejwt.tokens import RefreshToken
from django.db.models import Q
from .serializer import *
from rest_framework.permissions import AllowAny, IsAuthenticated
import json
from apps.models import *

class LoginView(APIView):
    def post(self, request):
        username = request.data.get('username')
        password = request.data.get('password')

        if not username or not password:
            return Response({'status': False, 'msg': 'Username and password are required.'}, status=status.HTTP_400_BAD_REQUEST)

        user = authenticate(request, username=username, password=password)

        if user is not None:
            refresh = RefreshToken.for_user(user)
            access_token = str(refresh.access_token)
            return Response({'status': True, 'msg': 'Logged in successfully', 'token': access_token}, status=status.HTTP_200_OK)
        else:
            return Response({'status': False, 'msg': 'Invalid credentials'}, status=status.HTTP_400_BAD_REQUEST)

class Logoutviews(APIView):       
    def post(self,request):
        try:
            logout(request)
            return Response({'status':True,"msg":'loged Out succefully'},status=status.HTTP_200_OK)    
        except Exception as e:
            print(e)
            return Response({"status":False,"msg":"server error!"},status=status.HTTP_500_INTERNAL_SERVER_ERROR)

class ProductViews(APIView):
    permission_classes=(IsAuthenticated,)
    def get(self,request):
        try:
            if request.user.userprofile.roles.filter(Q(name='store') | Q(name='dprt')).exists():
                product=Inventory.objects.filter(status='approved').order_by('-id')
                serializer=ProductSerializer(product,many=True)
                return Response({"status":True,'data':serializer.data})
            else:
                return Response({'status':False,"msg":"unauthorized access!"},status=status.HTTP_401_UNAUTHORIZED)
        except Exception as e:
            print(e)
            return Response({'status': False, 'msg': 'server error'}, status=status.HTTP_400_BAD_REQUEST)

    def post(self,request):
        try:
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
                return Response({"ststus":True,"msg":'Product added succesfully!'})
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
                return Response({"ststus":True,"msg":'Product sent for Approval!'})
            else:
                return Response({'status':False,"msg":"unauthorized access!"},status=status.HTTP_401_UNAUTHORIZED)
        except Exception as e:
            print(e)
            return Response({'status': False, 'msg': 'server error'}, status=status.HTTP_400_BAD_REQUEST)

    def put(request):
        try:
            if request.user.userprofile.roles.filter(name='store').exists():
                product = Inventory.objects.get(product_Id=request.POST.get('product_id'))
                product.product_Name=request.POST.get('product_name')
                product.vendor=request.POST.get('vendor')
                product.mrp=request.POST.get('mrp')
                product.batch_num=request.POST.get('batch_number')
                product.batch_date=request.POST.get('batch_date')
                product.quantity=request.POST.get('quantity')
                product.save()
                return Response({"status":True,'msg':'Product Updated Successfully'})
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
                return Response({"status":True,'msg':'Product sent for Approval!'})
            else:
                return Response({'status':False,"msg":"unauthorized access!"},status=status.HTTP_401_UNAUTHORIZED)

        except Exception as e:
            print(e)
            return Response({'status': False, 'msg': 'server error'}, status=status.HTTP_400_BAD_REQUEST)

    def delete(request):
        try:
            if request.user.userprofile.roles.filter(name='store').exists():
                product = Inventory.objects.get(product_Id=request.POST.get('product_id'))
                product.delete()
                return Response({"ststus":True,'msg':'Product removed sucessfully!'})
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
                return Response({"ststus":True,'msg':'Product sent for Approval!'})
            else:
                return Response({'status':False,"msg":"unauthorized access!"},status=status.HTTP_401_UNAUTHORIZED)

        except Exception as e:
            print(e)
            return Response({'status': False, 'msg': 'server error'}, status=status.HTTP_400_BAD_REQUEST)

def JsonifyPayload(dict):
    dict['payload'] = json.loads(dict['payload'])
    return dict

class PendingProductsViewS(APIView):
    permission_classes=(IsAuthenticated,)
    def get(self,request):
        try:
            if request.user.userprofile.roles.filter(Q(name='store') | Q(name='dprt')).exists():
                requestedData=RequestRecord.objects.all().order_by('-id')
                payloadData = [{'id':data.id,'product': json.loads(data.payload), 'action': data.action, 'status': data.request_status} for data in requestedData]
                # context={
                #     'product': payloadData
                # }
                return Response({"status":True,'data':payloadData})
            else:
                return Response({'status':False,"msg":"unauthorized access!"},status=status.HTTP_401_UNAUTHORIZED)
        except Exception as e:
            print(e)
            return Response({'status': False, 'msg': 'server error'}, status=status.HTTP_400_BAD_REQUEST)

class AproveProductViews(APIView):
    permission_classes=(IsAuthenticated,)
    def post(request, recored_id):
        try:
            if request.user.userprofile.roles.filter(name='store').exists():
                request_ = RequestRecord.objects.get(id=recored_id)
                request_.request_status='approved'
                request_.save()
                return Response({"ststus":True,'msg':"Product approved!"})
            else:
                return Response({'status':False,"msg":"unauthorized access!"},status=status.HTTP_401_UNAUTHORIZED)

        except Exception as e:
            print(e)
            return Response({'status': False, 'msg': 'server error'}, status=status.HTTP_400_BAD_REQUEST)

class RejectProjectViews(APIView):
    permission_classes=(IsAuthenticated,)
    def post(request, recored_id):
        try:
            if request.user.userprofile.roles.filter(name='store').exists():
                request_ = RequestRecord.objects.get(id=recored_id)
                request_.request_status='rejected'
                request_.save()
                return Response({"ststus":True,'msg':"Product Rejected!"})
            else:
                return Response({'status':False,"msg":"unauthorized access!"},status=status.HTTP_401_UNAUTHORIZED)
        except Exception as e:
            print(e)
            return Response({'status': False, 'msg': 'server error'}, status=status.HTTP_400_BAD_REQUEST)
