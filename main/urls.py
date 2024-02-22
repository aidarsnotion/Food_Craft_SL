from django.urls import path
from . import views, AdminViews, StaffViews, ClientViews
from django.contrib.auth import views as auth_views


urlpatterns = [
    #URL's для клиента
    path('', ClientViews.client_home, name="client_home"),
    path('about', ClientViews.about, name='about-us'),
    path('contact', ClientViews.contact, name='contact'),
    path('send_message/', ClientViews.send_message),
    path('cart', ClientViews.cart, name='cart'),
    path('calculation/', StaffViews.meels, name='meels'),
    path('list', ClientViews.list, name='list-of-products'),
    path('details/<int:id>', ClientViews.product_details, name='details'),
    path('recips-details/<int:id>', StaffViews.recips_detail, name='recips_detail'),
    path('not/', views.error_400, name='not'),
    path('recips_list', StaffViews.recips_list, name='recips_list'),
    path('download_pdf', ClientViews.download_pdf, name='download_pdf'),

    #Ajax-regions choice
    path('load-regions/', StaffViews.load_courses, name='ajax_load_region'),
    path('load-calculations/', StaffViews.load_calculation, name='ajax_load_calculation'),
    path('load-calculations/save', StaffViews.save_view, name="save_results"),

    path("admin_home/convert-pdf-to-excel",AdminViews.Conver_PDF_to_Excel,name="convert"),
    path('admin_home/Import_Excel_pandas/', AdminViews.Import_Excel_pandas,name="Import_Excel_pandas"),

    path('login/', views.loginPage, name='login'),
    path('doLogin/', views.doLogin, name="doLogin"),
    path('logout_user/', views.logout_page, name="logout_user"),

    #URL's для администратора
    path('admin_home/', AdminViews.admin_home, name="admin_home"),
    path('admin-panel/add_staff/', AdminViews.add_staff, name="add_staff"),
    path('admin-panel/add_staff_save/', AdminViews.add_staff_save, name="add_staff_save"),
    path('admin-panel/manage_staff/', AdminViews.manage_staff, name="manage_staff"),
    path('admin-panel/edit_staff/<int:staff_id>/', AdminViews.edit_staff, name="edit_staff"),
    path('admin-panel/edit_staff_save/', AdminViews.edit_staff_save, name="edit_staff_save"),
    path('admin-panel/delete_staff/<int:staff_id>/', AdminViews.delete_staff, name="delete_staff"),
    path('admin-panel/check_email_exist/', AdminViews.check_email_exist, name="check_email_exist"),
    path('admin-panel/check_username_exist/', AdminViews.check_username_exist, name="check_username_exist"),

    path(r'admin-panel/profile/update/^', AdminViews.ProfileUpdateView.as_view(), name = 'update_profile'),
    path(r'admin-panel/profile/update/^/change_password/', AdminViews.ChangePasswordView.as_view(), name = 'change_password'),
    
    # Reset password
    path("accounts/password_reset/", AdminViews.password_reset_request, name="password_reset"),
    path('accounts/password_reset/done/', auth_views.PasswordResetDoneView.as_view(template_name="admin_templates/pages/user/password_reset_done.html"), name='password_reset_done'),
    path('accounts/reset/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(template_name="admin_templates/pages/user/password_reset_confirm.html"), name='password_reset_confirm'),
    path('accounts/reset/done/', auth_views.PasswordResetCompleteView.as_view(template_name="admin_templates/pages/user/password_reset_complete.html"), name='password_reset_complete'),


    # path('admin-panel/accounts/login/', StaffViews.login_page, name='login_page'),
    path('admin-panel/accounts/login/success/', AdminViews.authorization, name='authorizate'),
    path('admin-panel/accounts/logout/', AdminViews.logout_page, name = 'logout_page'),
    path('admin-panel/main/', AdminViews.AdminMain.as_view(), name='admin_panel'),

    # Regions View
    path('admin-panel/regions/all/', AdminViews.RegionsListView.as_view(), name='regions_all'),
    path('admin-panel/regions/create/', AdminViews.RegionsCreateView.as_view(), name='regions_create'),
    path('admin-panel/regions/update/<int:pk>/', AdminViews.RegionsUpdateView.as_view(), name='regions_update'),
    path('admin-panel/regions/delete/<int:id>/', AdminViews.regions_delete, name='regions_delete'),
    path('admin-panel/regions/clear_all/', AdminViews.regions_clear_clear, name='regions_clear_all'),
    path('admin-panel/regions/delete/', AdminViews.RegionsDeleteView.as_view(), name='regions_delete'),

    # Categories View
    path('admin-panel/categories/all/', AdminViews.CategoriesListView.as_view(), name='categories_all'),
    path('admin-panel/categories/create/', AdminViews.CategoriesCreateView.as_view(), name='categories_create'),
    path('admin-panel/categories/update/<int:pk>/', AdminViews.CategoriesUpdateView.as_view(), name='categories_update'),
    path('admin-panel/categories/delete/<int:id>/', AdminViews.categories_delete, name='categories_delete'),
    path('admin-panel/categories/clear_all/', AdminViews.categories_clear_clear, name='categories_clear_all'),
    path('admin-panel/categories/delete/', AdminViews.CategoriesDeleteView.as_view(), name='categories_delete'),

    # Types View
 

    # Products View
    path('admin-panel/products/all/', AdminViews.ProductsListView.as_view(), name='products_all'),
    path('admin-panel/products/create/', AdminViews.ProductsCreateView.as_view(), name='products_create'),
    path('admin-panel/products/update/<int:pk>/', AdminViews.ProductsUpdateView.as_view(), name='products_update'),
    path('admin-panel/products/delete/<int:id>/', AdminViews.products_delete, name='products_delete'),
    path('admin-panel/products/clear_all/', AdminViews.products_clear_clear, name='products_clear_all'),
    path('admin-panel/products/delete/', AdminViews.ProductsDeleteView.as_view(), name='products_delete'),

    # FatAcids View
    path('admin-panel/fatacids/all/', AdminViews.FatAcidsListView.as_view(), name='fatacids_all'),
    path('admin-panel/fatacids/create/', AdminViews.FatAcidsCreateView.as_view(), name='fatacids_create'),
    path('admin-panel/fatacids/update/<int:pk>/', AdminViews.FatAcidsUpdateView.as_view(), name='fatacids_update'),
    path('admin-panel/fatacids/delete/<int:id>/', AdminViews.fatacids_delete, name='fatacids_delete'),
    path('admin-panel/fatacids/clear_all/', AdminViews.fatacids_clear_clear, name='fats_clear_all'),
    path('admin-panel/fatacids/delete/', AdminViews.FatAcidsDeleteView.as_view(), name='fatacids_delete'),

    # FatAcidsTypes View
    path('admin-panel/fatacidstype/all/', AdminViews.FatAcidTypesListView.as_view(), name='fatacidstype_all'),
    path('admin-panel/fatacidstype/create/', AdminViews.FatAcidTypesCreateView.as_view(), name='fatacidstype_create'),
    path('admin-panel/fatacidstype/update/<int:pk>/', AdminViews.FatAcidTypesUpdateView.as_view(), name='fatacidstype_update'),
    path('admin-panel/fatacidstype/delete/<int:id>/', AdminViews.fatacidstype_delete, name='fatacidstype_delete'),
    path('admin-panel/fatacidstype/clear_all/', AdminViews.fatacidstypes_clear_clear, name='fatacidstype_clear_all'),
    path('admin-panel/fatacidstype/delete/', AdminViews.FatAcidTypesDeleteView.as_view(), name='fatacidstype_delete'),

    # FatAcidComposition View
    path('admin-panel/fatacidcomposition/all/', AdminViews.FatAcidCompositionListView.as_view(), name='fatacidcomposition_all'),
    path('admin-panel/fatacidcomposition/create/', AdminViews.FatAcidCompositionCreateView.as_view(), name='fatacidcomposition_create'),
    path('admin-panel/fatacidcomposition/update/<int:pk>/', AdminViews.FatAcidCompositionUpdateView.as_view(), name='fatacidcomposition_update'),
    path('admin-panel/fatacidcomposition/delete/<int:id>/', AdminViews.fatacidcomposition_delete, name='fatacidcomposition_delete'),
    path('admin-panel/fatacidcomposition/clear_all/', AdminViews.fatacidcomposition_clear_clear, name='fatacidcomposition_clear_all'),
    path('admin-panel/fatacidcomposition/delete/', AdminViews.FatAcidCompositionDeleteView.as_view(), name='fatacidcomposition_delete'),

    # Minerals View
    path('admin-panel/minerals/all/', AdminViews.MineralsListView.as_view(), name='minerals_all'),
    path('admin-panel/minerals/create/', AdminViews.MineralsCreateView.as_view(), name='minerals_create'),
    path('admin-panel/minerals/update/<int:pk>/', AdminViews.MineralsUpdateView.as_view(), name='minerals_update'),
    path('admin-panel/minerals/delete/<int:id>/', AdminViews.minerals_delete, name='minerals_delete'),
    path('admin-panel/minerals/clear_all/', AdminViews.minerals_clear_clear, name='minerals_clear_all'),
    path('admin-panel/minerals/delete/', AdminViews.MineralsDeleteView.as_view(), name='minerals_delete'),

    # AminoAcids View
    path('admin-panel/aminoacids/all/', AdminViews.AminoAcidsListView.as_view(), name='aminoacids_all'),
    path('admin-panel/aminoacids/create/', AdminViews.AminoAcidsCreateView.as_view(), name='aminoacids_create'),
    path('admin-panel/aminoacids/update/<int:pk>/', AdminViews.AminoAcidsUpdateView.as_view(), name='aminoacids_update'),
    path('admin-panel/aminoacids/delete/<int:id>/', AdminViews.aminoacids_delete, name='aminoacids_delete'),
    path('admin-panel/aminoacids/clear_all/', AdminViews.aminos_clear_clear, name='aminos_clear_all'),
    path('admin-panel/aminoacids/delete/', AdminViews.AminoacidsDeleteView.as_view(), name='aminoacids_delete'),

    # Chemicals View
    path('admin-panel/chemicals/all/', AdminViews.ChemicalsListView.as_view(), name='chemicals_all'),
    path('admin-panel/chemicals/create/', AdminViews.ChemicalsCreateView.as_view(), name='chemicals_create'),
    path('admin-panel/chemicals/update/<int:pk>/', AdminViews.ChemicalsUpdateView.as_view(), name='chemicals_update'),
    path('admin-panel/chemicals/delete/<int:id>/', AdminViews.chemicals_delete, name='chemicals_delete'),
    path('admin-panel/chemicals/clear_all/', AdminViews.chemicals_clear_clear, name='chemicals_clear_all'),
    path('admin-panel/chemicals/delete/', AdminViews.ChemicalsDeleteView.as_view(), name='chemicals_delete'),

    #URL's для сотрудника
    path('staff_home/', StaffViews.staff_home, name="staff_home"),
    path('about', StaffViews.about, name='about-us'),
    path('contact', StaffViews.contact, name='contact'),
    path('send_message/', StaffViews.send_message),
    path('calculation/all', StaffViews.meels, name='meels'),
    path('list', StaffViews.list, name='list-of-products'),
    path('details/<int:id>', StaffViews.product_details, name='details'),
]