from django.urls import path
from .import HODViews
from .import views
from django.contrib.auth import views as auth_views


urlpatterns=[
    path('',HODViews.adminDashboard,name='admin_dashboard'),
    path("pos/", views.pos, name="pos"),
    path("pos/checkout", views.checkout_modal, name="checkout-modal"),
    path('pos/save-pos', views.save_pos, name="save-pos"),
    path('receipt', views.receipt, name="receipt-modal"),
    path('login/',views.loginPage,name='login'),
    path('logout/',views.logoutUser,name='logout'),
 
    path('admin_user/add_stock/',HODViews.addStock,name='add_stock'),
    path('admin_user/add_category/',HODViews.addCategory,name='add_category'),
    path('admin_user/manage_stock/',HODViews.manageStock,name='manage_stock'),
    path('admin_user/stock-graph', HODViews.stock_graph, name="stock_graph"),

    path('admin_user/hod_profile/',HODViews.hodProfile,name='hod_profile'),
    path('admin_user/hod_profile/editAdmin_profile/',HODViews.editAdmin,name='edit-admin'),
    path('admin_user/delete_drug/<str:pk>/',HODViews.deleteDrug,name='delete_drug'),

    path('admin_user/edit_drug/<pk>/', HODViews.editStock, name="edit_drug"),
    path('admin_user/receive_drug/<pk>/', HODViews.receiveDrug, name="receive_drug"),
    path('admin_user/reorder_level/<str:pk>/', HODViews.reorder_level, name="reorder_level"),
    path('admin_user/drug_details/<str:pk>/', HODViews.drugDetails, name="drug_detail"),

    # reports
    path('reports/sales/', views.SalesReportView.as_view(), name="sales_report"),
    path('reports/products-sold/', views.DrugsReportView.as_view(), name="drugs_sold"),
  
    path('reset_password/',auth_views.PasswordResetView.as_view(template_name="password_reset.html"),name="reset_password"),
    path('reset_password_sent/',auth_views.PasswordResetDoneView.as_view(template_name="password_reset_sent.html"),name="password_reset_done"),
    path('reset/<uidb64>/<token>/',auth_views.PasswordResetConfirmView.as_view(template_name="password_reset_form.html"),name="password_reset_confirm"),
    path('reset_password_complete/',auth_views.PasswordResetCompleteView.as_view(template_name="password_reset_done.html"),name="password_reset_complete"),
]
