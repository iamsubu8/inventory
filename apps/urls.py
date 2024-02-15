from django.urls import path
from apps import views

urlpatterns = [
    path('',views.Login,name='login'),
    path('logout',views.logout),
    path('productList',views.Product,name='product'),
    path('addproduct',views.AddPRODUCT),
    path('edit',views.EditPRODUCT),
    path('remove',views.RemovePRODUCTS),
    path('pending',views.PendingProducts,name='pending'),
    path('ApprovePending/<int:recored_id>',views.AproveProduct, name='approval'),
    path('rejectPending/<int:recored_id>',views.RejectProduct, name='reject'),

]