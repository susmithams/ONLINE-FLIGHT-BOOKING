from django.shortcuts import render,redirect,get_object_or_404
from django.http import HttpResponse
from .models import *
from django.conf import settings
from .forms import *
import stripe
from django.core.mail import send_mail
from datetime import datetime,timedelta
from django.template.loader import render_to_string
from django.utils.html import strip_tags
from django.contrib import messages
# from .pdf import htmltopdf


# Create your views here.
####--------authenticated user registration----------#####

def register_seller(request):
    if request.method=='POST':
        form=SellerRegistrationForm(request.POST)
        if form.is_valid():
            password=form.cleaned_data.get('password')
            cpassword=form.cleaned_data.get('cpassword')
            if password!=cpassword:
                messages.error(request,' IncorrectPassword ')
            else:
                user=form.save(commit=False)
                user.set_password(password)
                user.save()
                messages.success(request,'Registration successful.You can now login...')
                #return HttpResponse('Registration success')
                return redirect(login_view)
    else:
        form=SellerRegistrationForm()

    return render(request,'sellerregister.html',{'form':form})

####-----------------authenticated login-------------------------------------------------##########
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import authenticate,login



def login_view(request):
    if request.method=='POST':
        form=AuthenticationForm(request,data=request.POST)
        if form.is_valid():
            username=form.cleaned_data.get('username')
            password=form.cleaned_data.get('password')

            user=authenticate(username=username,password=password)
            if user is not None:
                login(request,user)
                request.session['sellerid']=user.id
                messages.success(request,f'You are now logged in as{username}')
                return redirect(profile_view)
                #return HttpResponse("login successful")
            else:
                messages.error(request,'Invalid Username and Password')
        else:
            messages.error(request,'Form is not Valid')
    else:
        form=AuthenticationForm()
    return render(request,'login.html',{'form':form})

 #####------------------------------------------------------------------------------
def profile_view(request):
    userid = request.session['sellerid']
    data = User.objects.get(id=userid)
    a= FlightAddModel.objects.all()
    return render(request,'sellerprofile.html',{'data':data,'a':a})


####---------------------------------------------------------------------------------
def add_flight(request):
    if (request.method=='POST'):
        city = request.POST.get('city')
        code = request.POST.get('code')
        country = request.POST.get('country')
        origin = request.POST.get('origin')
        destination = request.POST.get('destination')
        depttime = request.POST.get('dept-time')
        arrtime = request.POST.get('arr-time')
        seats = request.POST.get('seats')
        duration = request.POST.get('duration')
        airport = request.POST.get('airport')
        airline = request.POST.get('airline')
        ecofir = request.POST.get('eco-fir')
        busfir = request.POST.get('bus-fir')
        firsfir = request.POST.get('firs-fir')
        data=FlightAddModel(city=city,code=code,country=country,origin=origin,destination=destination,
                    depart_time=depttime,duration=duration,seats=seats,airport=airport,
                    arrival_time=arrtime,airline=airline,economy_fare=ecofir,business_fare=busfir,
                    first_fare=firsfir )
        data.save()
        return HttpResponse("upload successfully")
    return render(request, "addflightdetails.html")

def DeleteFlight(request,id):
    data=FlightAddModel.objects.get(id=id)
    data.delete()
    return redirect(profile_view)
def UpdateFlights(request,id):
    data = FlightAddModel.objects.get(id=id)
    if (request.method=="POST"):
        data.city = request.POST.get('city')
        data.code = request.POST.get('code')
        data.country = request.POST.get('country')
        data.origin = request.POST.get('origin')
        data.destination = request.POST.get('destination')
        data.depttime = request.POST.get('dept-time')
        data.arrtime = request.POST.get('arr-time')
        data.seats = request.POST.get('seats')
        data.duration = request.POST.get('duration')
        data.airport = request.POST.get('airport')
        data.airline = request.POST.get('airline')
        data.ecofir = request.POST.get('eco-fir')
        data.busfir = request.POST.get('bus-fir')
        data.firsfir = request.POST.get('firs-fir')
        data.save()
        return redirect(profile_view)
    return render(request, 'updateflights.html', {'data': data})
###---------------------------------------------------------------------------------------------------#####
####user side
def Index(request):

    if (request.method == "POST"):
        email = request.POST.get('email')
        password = request.POST.get('password')
        data = Passenger.objects.all()
        for i in data:
            if (i.email == email and i.password == password):
                request.session['userid'] = i.id
                return redirect(UserProfile)
                # return HttpResponse('login success')
        else:

            messages.error(request,'Invalid Username and Password')
            return redirect(Index)

    return render(request,"index.html")
def Registration(request):
    if(request.method=="POST"):
        fullname=request.POST.get('fullname')
        email=request.POST.get('email')
        phone=request.POST.get('phone')
        gender=request.POST.get("gender")
        password=request.POST.get('password')
        cpassword=request.POST.get('cpassword')
        if(password==cpassword):
            data=Passenger(fullname=fullname,email=email,phone=phone,gender=gender,password=password)
            data.save()
            return redirect(Index)
        else:
            return HttpResponse('registration failed')

    return render(request,'userreg.html')
def Updateprofile(request,id):
    data=Passenger.objects.get(id=id)
    if(request.method=="POST"):
        data.fullname=request.POST.get('fullname')
        data.email=request.POST.get('email')
        data.phone=request.POST.get('phone')
        data.gender=request.POST.get('gender')
        data.save()
        return redirect(FlightDetail)
    return render(request,'updateprofile.html',{'data':data})

def UserProfile(request):
    id = request.session['userid']
    user = Passenger.objects.get(id=id)

    if request.method == "POST":
        way = request.POST.get('way')
        origin = request.POST.get('origin')
        destination = request.POST.get('destination')
        departure_date = request.POST.get('ddate')
        return_date = request.POST.get('rdate')
        category = request.POST.get('category')
        request.session['way']=way
        request.session['departure_date'] = departure_date
        request.session['return_date'] = return_date
        request.session['category']=category


        if way == "1":
            if category == 'economy':
                flights = FlightAddModel.objects.filter(origin=origin, destination=destination).exclude(
                    economy_fare=0).order_by('economy_fare')
            elif category == 'business':
                flights = FlightAddModel.objects.filter(origin=origin, destination=destination).exclude(
                    business_fare=0).order_by('business_fare')
            else:
                flights = FlightAddModel.objects.filter(origin=origin, destination=destination).exclude(
                    first_fare=0).order_by('first_fare')

            context = {
                'way': way,
                'departure_date': departure_date,
                'return_date': return_date,
                'category': category,
                'flights': flights,
            }



            return render(request, 'userflights.html', context)

        elif way == "2":
            if category == 'economy':
                flights = FlightAddModel.objects.filter(origin=origin, destination=destination).exclude(
                    economy_fare=0).order_by('economy_fare')
                flights2 = FlightAddModel.objects.filter(origin=destination, destination=origin).exclude(
                    economy_fare=0).order_by('economy_fare')
            elif category == 'business':
                flights = FlightAddModel.objects.filter(origin=origin, destination=destination).exclude(
                    business_fare=0).order_by('business_fare')
                flights2 = FlightAddModel.objects.filter(origin=destination, destination=origin).exclude(
                    business_fare=0).order_by('business_fare')
            else:
                flights = FlightAddModel.objects.filter(origin=origin, destination=destination).exclude(
                    first_fare=0).order_by('first_fare')
                flights2 = FlightAddModel.objects.filter(origin=destination, destination=origin).exclude(
                    first_fare=0).order_by('first_fare')

            context = {
                'way': way,
                'departure_date': departure_date,
                'return_date': return_date,
                'category': category,
                'flights': flights,
                'flights2': flights2}


            return render(request, 'userflights.html', context)

    return render(request, 'userprofile.html', {'user': user})


def FlightDetail(request):
    userid = request.session.get('userid')
    passenger = Passenger.objects.get(id=userid)
    category=request.session.get('category')

    flight_id = request.GET.get('selected_flight')
    if flight_id:
        selected_flight = get_object_or_404(FlightAddModel, id=flight_id)
        request.session['selected_flight'] = selected_flight.id

    flight_id_outbound = request.GET.get('selected_flight_outbound')
    if flight_id_outbound:
        selected_flight_outbound = get_object_or_404(FlightAddModel, id=flight_id_outbound)
        request.session['selected_flight_outbound'] = selected_flight_outbound.id

    flight_id_return = request.GET.get('selected_flight_return')
    if flight_id_return:
        selected_flight_return = get_object_or_404(FlightAddModel, id=flight_id_return)
        request.session['selected_flight_return'] = selected_flight_return.id

    departure_date = request.session.get('departure_date')
    return_date = request.session.get('return_date')
    way = request.session.get('way')

    pcount = NewPassenger.objects.count()

    if request.method == "POST":
        form = NewPassengerForm(request.POST)
        if form.is_valid():
            new_passenger = form.save(commit=False)
            if way == '1':  # One-way trip
                if selected_flight:
                    new_passenger.flight = selected_flight
                    new_passenger.save()
                    return redirect(Summary)
                # flight_id = request.POST.get('flight_id')
                # if flight_id:
                #     try:
                #         flight = FlightAddModel.objects.get(id=flight_id)
                #         new_passenger.flight = flight
                #         new_passenger.save()
                #         pcount = NewPassenger.objects.count()
                #         return redirect(Summary)  # Redirect to refresh the page and show updated count
                #     except FlightAddModel.DoesNotExist:
                #         return HttpResponse('Flight not found')
            elif way == '2':  # Round trip
                if selected_flight_outbound and selected_flight_return:
                    new_passenger.flight = selected_flight_outbound
                    new_passenger.save()
                    return redirect(Summary)

                # flight_id_outbound = request.POST.get('flight_id_outbound')
                # flight_id_return = request.POST.get('flight_id_return')
                # if flight_id_outbound and flight_id_return:
                #     try:
                #         flight_outbound = FlightAddModel.objects.get(id=flight_id_outbound)
                #         flight_return = FlightAddModel.objects.get(id=flight_id_return)
                #
                #         # Save outbound flight details
                #         new_passenger.flight = flight_outbound
                #         new_passenger.save()
                #         pcount = NewPassenger.objects.count()
                #         return redirect(Summary)
                #     except FlightAddModel.DoesNotExist:
                #         return HttpResponse('Flight not found')
    else:
        form = NewPassengerForm()

    context = {
        'form': form,
        'selected_flight': selected_flight if flight_id else None,
        'selected_flight_return': selected_flight_return if flight_id_return else None,
        'selected_flight_outbound': selected_flight_outbound if flight_id_outbound else None,
        'departure_date': departure_date,
        'return_date': return_date,
        'passenger': passenger,
        'way': way,
        'category':category,
    }

    return render(request, 'flightbooking.html', context)

def Summary(request):
    selected_flight_id = request.session.get('selected_flight')
    selected_flight_outbound_id = request.session.get('selected_flight_outbound')
    selected_flight_return_id = request.session.get('selected_flight_return')
    way = request.session.get('way')
    category = request.session.get('category')  # Assuming category is stored in session


    selected_flight = None
    selected_flight_outbound = None
    selected_flight_return = None

    if selected_flight_id:
        selected_flight = FlightAddModel.objects.get(id=selected_flight_id)
    if selected_flight_outbound_id:
        selected_flight_outbound = FlightAddModel.objects.get(id=selected_flight_outbound_id)
    if selected_flight_return_id:
        selected_flight_return = FlightAddModel.objects.get(id=selected_flight_return_id)

    if way == '1':
        filtered_passengers = NewPassenger.objects.filter(flight=selected_flight)

    elif way == '2':
        filtered_passengers = NewPassenger.objects.filter(
            flight=selected_flight_outbound)

    else:
        filtered_passengers = []
    passenger_count = filtered_passengers.count()
    total_fare=0
    # Calculate total fare

    if category == 'economy' :
        price=selected_flight.economy_fare
    elif category == 'business':
        price=selected_flight.business_fare
    else:
        price=selected_flight.first_fare



    if way == '1' and selected_flight:
        total_fare = passenger_count * price
    elif way == '2' and selected_flight_outbound and selected_flight_return:
        total_fare = 0
        # Calculate total fare

        if category == 'economy':
            price = selected_flight_outbound.economy_fare+selected_flight_return.economy_fare
        elif category == 'business':
            price = selected_flight_outbound.business_fare+selected_flight_return.business_fare
        else:
            price = selected_flight_outbound.first_fare+selected_flight_return.first_fare
        total_fare = passenger_count* price


    subtotal=0
    key = settings.STRIPE_PUBLISHABLE_KEY
    striptotal = 0


    subtotal=total_fare+100
    request.session['subtotal']=subtotal

    striptotal=subtotal*100
    bookingdate = datetime.now()

    context = {
        'filtered_passengers': filtered_passengers,
        'selected_flight': selected_flight,
        'selected_flight_outbound': selected_flight_outbound,
        'selected_flight_return': selected_flight_return,
        'passenger_count': passenger_count,
        'total_fare': total_fare,
        'category': category,
        'subtotal':subtotal,
        'striptotal':striptotal,
        'key':key,
        'bookingdate':bookingdate,

    }

    return render(request, 'summery.html', context)

def UpdatePassengerDetails(request,id):
    data=NewPassenger.objects.get(id=id)
    if(request.method=="POST"):
        data.fname=request.POST.get('fname')
        data.lname=request.POST.get('lname')
        data.age=request.POST.get('age')
        data.gender=request.POST.get('gender')
        data.save()
        return redirect(Summary)
    return render(request,'updatepassengerprofile.html',{'data':data})

def DeletePassenger(reqest,id):
    db = NewPassenger.objects.get(id=id)
    db.delete()
    return redirect(Summary)

def PaymentSection(request):
    if request.method == "POST":
        mail_flights = []
        userid = request.session['userid']
        user = Passenger.objects.get(id=userid)
        subtotal = request.session.get('subtotal')
        category = request.session.get('category')
        departure_date = request.session.get('departure_date')
        return_date = request.session.get('return_date')
        way=request.session.get('way')
        selected_flight_id = request.session.get('selected_flight')
        selected_flight_outbound_id = request.session.get('selected_flight_outbound')
        selected_flight_return_id = request.session.get('selected_flight_return')

        flights = []

        if way == '1' and selected_flight_id:
            # selected_flight = FlightAddModel.objects.get(id=selected_flight_id)
            flight = get_object_or_404(FlightAddModel, id=selected_flight_id)
            flights.append(flight)
        if way=='2' and selected_flight_outbound_id and selected_flight_return_id:
            # selected_flight_outbound = FlightAddModel.objects.get(id=selected_flight_outbound_id)
            flight = get_object_or_404(FlightAddModel, id=selected_flight_outbound_id)

            flights.append(flight)
            # selected_flight_return = FlightAddModel.objects.get(id=selected_flight_return_id)
            flight = get_object_or_404(FlightAddModel, id=selected_flight_return_id)

            flights.append(flight)

        # Create the order
        order = Order.objects.create(passenger=user)

        # Add the selected flights to the order
        for flight in flights:
            order.flights.add(flight)

        flight_ids = [flight.id for flight in flights]
        cart = NewPassenger.objects.filter(flight_id__in=flight_ids)


        # Create order tickets
        for i in cart:
            orderticket.objects.create(order=order, fname=i.fname, lname=i.lname, age=i.age, gender=i.gender)

        # Prepare email context
        mail_flights = [{'order': order, 'fname': i.fname, 'lname': i.lname, 'age': i.age, 'gender': i.gender} for i in
                        cart]

        booking_date = datetime.now()

        subject = 'Order confirmation'

        context = {
            'mail_flights': mail_flights,
            'subtotal': subtotal,
            'booking_date': booking_date.strftime('%Y-%m-%d'),
            'order': order,
            'user': user,
            'flights': flights,
            'category': category,
            'departure_date': departure_date,
            'return_date': return_date
        }

        html_message=render_to_string('order_confirmaion_email.html',context)

        plain_message=strip_tags(html_message)

        from_email='mssusmitha.007@gmail.com'
        to_email=[user.email]
        send_mail(subject,plain_message,from_email,to_email,html_message=html_message)
        cart.delete()
        return render(request, 'ticket.html', context)  # Render the ticket.html template with context

    return render(request,'payment.html')


def Mybooking(request):
    userid = request.session['userid']
    orders = orderticket.objects.filter(order__passenger__id=userid).order_by('-order__booking_date')

    order_details = []
    for order in orders:
        flights = order.order.flights.all()
        order_details.append({
            'order': order,
            'flights': flights
        })

    return render(request, 'myorder.html', {'order_details': order_details})

def CancelWarning(request,flight_id):
    flight=get_object_or_404(FlightAddModel,id=flight_id)
    context={'flight':flight}
    return render(request,'warning.html',context)

def cancelflight(request,flight_id):
    userid = request.session['userid']
    user = Passenger.objects.get(id=userid)
    departure_date = request.session['departure_date']

    if request.method == 'POST':
        flight = get_object_or_404(FlightAddModel, id=flight_id)
        order_tickets = orderticket.objects.filter(order__passenger=user, order__flights=flight)
        for order_ticket in order_tickets:
            order_ticket.order_status = False
            order_ticket.save()
            
    subject = 'Order cancelation'
    context = {'user':user,
            'flight': flight,
    'departure_date':departure_date,}
    html_message = render_to_string('order_cancellation_email.html', context)

    plain_message = strip_tags(html_message)

    from_email = 'mssusmitha.007@gmail.com'
    to_email = [user.email]
    send_mail(subject, plain_message, from_email, to_email, html_message=html_message)

    return HttpResponse('Flight cancelled')




def logout(request):
    request.session.flush()
    return redirect(Index)


def forgotpass(request):
    data=Passenger.objects.all()
    if request.method=='POST':
        email=request.POST.get('email')
        for i in data:
            if i.email==email:
                subject = 'change password'

                html_message = render_to_string('passwordmail.html',{'email':i.email,'id':i.id})

                plain_message = strip_tags(html_message)

                from_email = 'mssusmitha.007@gmail.com'
                to_email = [i.email]
                send_mail(subject, plain_message, from_email, to_email, html_message=html_message)


                return redirect(renewpassword)
            else:
                messages.error(request, 'please enter correct Email')
    return render(request,'forgotpassword.html')


def renewpassword(request,id):

    if request.method=="POST":
        data=Passenger.objects.get(id=id)
        password=request.POST.get('pass')
        cpassword=request.POST.get('repass')
        if password==cpassword:
            data.password=password
            data.save()
            return redirect(Index)
        else:
            messages.error(request, 'please enter correct password')



    return render(request,'correctpassword.html')

def LastSection(request):
    return render(request,'lastpage.html')


# def GenerateTicket(request):
#     userid = request.session['userid']
#     user = Passenger.objects.get(id=userid)
#
#     orders = orderticket.objects.filter(order__passenger__id=userid).order_by('-order__booking_date')
#
#     context = {
#         'mail_flights': mail_flights,
#         'subtotal': subtotal,
#         'booking_date': booking_date.strftime('%Y-%m-%d'),
#         'order': order,
#         'user': user,
#         'flights': flights,
#         'category': category,
#         'departure_date': departure_date,
#         'return_date': return_date
#     }








