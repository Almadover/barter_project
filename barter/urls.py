from django.urls import path
from .views import (
    home, my_ads, ad_create, ad_edit, ad_delete, ad_detail,
    accept_exchange_proposal, decline_exchange_proposal, my_exchange_proposals, propose_exchange, 
    register, login_view, my_sent_proposals
)
from django.contrib.auth.views import LogoutView, LoginView

urlpatterns = [
    path('', home, name='home'),
    path('my_ads/', my_ads, name='my_ads'),
    path('logout/', LogoutView.as_view(next_page='home'), name='logout'),
    path('login/', login_view, name='login'),
    path('register/', register, name='register'),
    path('add/', ad_create, name='ad_create'),
    path('ads/<int:pk>/', ad_detail, name='ad_detail'),
    path('ads/<int:pk>/edit/', ad_edit, name='ad_edit'),
    path('ads/<int:pk>/delete/', ad_delete, name='ad_delete'),
    path('my_exchange_proposals/', my_exchange_proposals, name='my_exchange_proposals'),
    path('accept_proposal/<int:proposal_id>/', accept_exchange_proposal, name='accept_exchange_proposal'),
    path('decline_proposal/<int:proposal_id>/', decline_exchange_proposal, name='decline_exchange_proposal'),
    path('ads/<int:ad_receiver_id>/propose-exchange/', propose_exchange, name='propose_exchange'),
    path('my_sent_proposals/', my_sent_proposals, name='my_sent_proposals')
]
from django.http import HttpResponse
def stubprofile(request):
    return HttpResponse('Попытка попасть на /accounts/profile/!')

urlpatterns += [
    path('accounts/profile/', stubprofile)
]