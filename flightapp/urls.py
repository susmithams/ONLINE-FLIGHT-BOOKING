from django.urls import path
from .views import *
urlpatterns=[
    path('sellerreg/',register_seller),
    path('login/', login_view),
    path('profile/',profile_view),
    path('addflight/',add_flight),
    path('deleteflight/<int:id>',DeleteFlight),
    path('updateflight/<int:id>',UpdateFlights),

    path('index/',Index),
    path('userreg/',Registration),
    path('userprofile/',UserProfile),
    path('editprofile/<int:id>',Updateprofile),
    path('flightdetail/',FlightDetail),
    path('summary/',Summary),
    path('editpassenger/<int:id>', UpdatePassengerDetails),
    path('deletepassenger/<int:id>', DeletePassenger),
    path('payment/',PaymentSection, name='payment'),
    path('booking/',Mybooking),
    path('warning/<int:flight_id>',CancelWarning,name='CancelWarning'),
    path('cancel/<int:flight_id>',cancelflight, name='cancelflight'),
    path('logout/', logout),
    path('forgot/', forgotpass),
    path('renew/<int:id>', renewpassword),
    path('last/',LastSection),



]