from datetime import datetime

from django.db.models import Q
from django.shortcuts import get_object_or_404, render

from room_booking_app.controllers import check_user_role
from room_booking_app.models import*


def usagereport(request):
    if request.user.is_authenticated:
        role = check_user_role(request.user)
    else:
        role = None

    bookings = Booking.objects.all()
    users = User.objects.all()
    all_peripherals = Facility.objects.all()
    refreshments = Refreshments.objects.all()
    rooms = Rooms.objects.all()

    if request.method == 'POST':
        selected_user_id = request.POST.get('user')
        facility_id = request.POST.get('facility')
        peripheral_id = request.POST.get('peripheral')
        refreshment_id = request.POST.get('refreshment')
        datefrom = request.POST.get('datefrom')
        dateto = request.POST.get('dateto')

        if all([selected_user_id, facility_id, peripheral_id, refreshment_id, datefrom, dateto]):
            selected_user = int(selected_user_id)
            selected_facility = int(facility_id)
            selected_peripheral = int(peripheral_id)
            selected_refreshment = int(refreshment_id)
            selected_from_date = datefrom
            selected_date_to = dateto
            user = get_object_or_404(User, id=selected_user_id)
            bookings = Booking.objects.filter(
                user_id=selected_user_id,
                room=facility_id,
                date_from__gte=datetime.strptime(datefrom, '%Y-%m-%d').date(),
                date_to__lte=datetime.strptime(dateto, '%Y-%m-%d').date()
            ).filter(
                Q(extra_peripherals__startswith=peripheral_id + ',') |
                Q(extra_peripherals__endswith=',' + peripheral_id) |
                Q(extra_peripherals__contains=',' + peripheral_id + ',') |
                Q(extra_peripherals=peripheral_id)
            ).filter(
                Q(refreshments__startswith=refreshment_id + ',') |
                Q(refreshments__endswith=',' + refreshment_id) |
                Q(refreshments__contains=',' + refreshment_id + ',') |
                Q(refreshments=refreshment_id)
            )

            users = User.objects.all()
            all_peripherals = Facility.objects.all()
            refreshments = Refreshments.objects.all()
            rooms = Rooms.objects.all()

            peripheral_names = None
            for booking in bookings:
                if booking.extra_peripherals:
                    peripheral_ids = set(booking.extra_peripherals.split(','))
                    peripherals = Facility.objects.filter(id__in=peripheral_ids)
                    if peripherals.exists():
                        peripheral_names = ", ".join([peripheral.title for peripheral in peripherals])
                        booking.peripheral_names = peripheral_names
                    else:
                        booking.peripheral_names = ""
                else:
                    booking.peripheral_names = ""

            refreshment_names = None
            for booking in bookings:
                if booking.refreshments:
                    refreshment_ids = set(booking.refreshments.split(','))
                    refreshments = Refreshments.objects.filter(id__in=refreshment_ids)
                    if refreshments.exists():
                        refreshment_names = ", ".join([refreshment.title for refreshment in refreshments])
                        booking.refreshment_names = refreshment_names
                    else:
                        booking.refreshment_names = ""
                else:
                    booking.refreshment_names = ""

            context = {
                'users': users,
                'all_peripherals': all_peripherals,
                'refreshments': refreshments,
                'rooms': rooms,
                'user': user,
                'bookings': bookings,
                'peripheral_names': peripheral_names,
                'refreshment_names': refreshment_names,
                'role': role,
                'selected_user': selected_user,
                'selected_facility': selected_facility,
                'selected_peripheral': selected_peripheral,
                'selected_refreshment': selected_refreshment,
                'selected_from_date': selected_from_date,
                'selected_date_to': selected_date_to
            }
            return render(request, 'accounts/usage_report.html', context)
        elif all([selected_user_id, facility_id, peripheral_id, refreshment_id, datefrom]):
            selected_user = int(selected_user_id)
            selected_facility = int(facility_id)
            selected_refreshment = int(refreshment_id)
            selected_peripheral = int(peripheral_id)
            selected_from_date = datefrom
            user = get_object_or_404(User, id=selected_user_id)
            bookings = Booking.objects.filter(
                user_id=selected_user_id,
                room_id=facility_id,
                date_start__gte=datetime.strptime(datefrom, '%Y-%m-%d').date(),
            ).filter(
                Q(extra_peripherals__startswith=peripheral_id + ',') |
                Q(extra_peripherals__endswith=',' + peripheral_id) |
                Q(extra_peripherals__contains=',' + peripheral_id + ',') |
                Q(extra_peripherals=peripheral_id)
            ).filter(
                Q(refreshments__startswith=refreshment_id + ',') |
                Q(refreshments__endswith=',' + refreshment_id) |
                Q(refreshments__contains=',' + refreshment_id + ',') |
                Q(refreshments=refreshment_id)
            )
            users = User.objects.all()
            all_peripherals = Facility.objects.all()
            refreshments = Refreshments.objects.all()
            rooms = Rooms.objects.all()

            peripheral_names = None
            for booking in bookings:
                if booking.extra_peripherals:
                    peripheral_ids = set(booking.extra_peripherals.split(','))
                    peripherals = Facility.objects.filter(id__in=peripheral_ids)
                    if peripherals.exists():
                        peripheral_names = ", ".join([peripheral.title for peripheral in peripherals])
                        booking.peripheral_names = peripheral_names
                    else:
                        booking.peripheral_names = ""
                else:
                    booking.peripheral_names = ""

            refreshment_names = None
            for booking in bookings:
                if booking.refreshments:
                    refreshment_ids = set(booking.refreshments.split(','))
                    refreshments = Refreshments.objects.filter(id__in=refreshment_ids)
                    if refreshments.exists():
                        refreshment_names = ", ".join([refreshment.title for refreshment in refreshments])
                        booking.refreshment_names = refreshment_names
                    else:
                        booking.refreshment_names = ""
                else:
                    booking.refreshment_names = ""

            context = {
                'users': users,
                'all_peripherals': all_peripherals,
                'refreshments': refreshments,
                'rooms': rooms,
                'user': user,
                'bookings': bookings,
                'peripheral_names': peripheral_names,
                'refreshment_names': refreshment_names,
                'role': role,
                'selected_user': selected_user,
                'selected_facility': selected_facility,
                'selected_peripheral_id': selected_peripheral,
                'selected_refreshment': selected_refreshment,
                'selected_from_date': selected_from_date,
            }
            return render(request, 'accounts/usage_report.html', context)

        elif all([selected_user_id, facility_id, peripheral_id, refreshment_id]):
            user = get_object_or_404(User, id=selected_user_id)
            selected_user = int(selected_user_id)
            selected_facility = int(facility_id)
            selected_refreshment = int(refreshment_id)
            selected_peripheral = int(peripheral_id)
            bookings = Booking.objects.filter(
                user_id=selected_user_id,
                room_id=facility_id,

            ).filter(
                Q(extra_peripherals__startswith=peripheral_id + ',') |
                Q(extra_peripherals__endswith=',' + peripheral_id) |
                Q(extra_peripherals__contains=',' + peripheral_id + ',') |
                Q(extra_peripherals=peripheral_id)
            ).filter(
                Q(refreshments__startswith=refreshment_id + ',') |
                Q(refreshments__endswith=',' + refreshment_id) |
                Q(refreshments__contains=',' + refreshment_id + ',') |
                Q(refreshments=refreshment_id)
            )
            users = User.objects.all()
            all_peripherals = Facility.objects.all()
            refreshments = Refreshments.objects.all()
            rooms = Rooms.objects.all()

            peripheral_names = None
            for booking in bookings:
                if booking.extra_peripherals:
                    peripheral_ids = set(booking.extra_peripherals.split(','))
                    peripherals = Facility.objects.filter(id__in=peripheral_ids)
                    if peripherals.exists():
                        peripheral_names = ", ".join([peripheral.title for peripheral in peripherals])
                        booking.peripheral_names = peripheral_names
                    else:
                        booking.peripheral_names = ""
                else:
                    booking.peripheral_names = ""

            refreshment_names = None
            for booking in bookings:
                if booking.refreshments:
                    refreshment_ids = set(booking.refreshments.split(','))
                    refreshments = Refreshments.objects.filter(id__in=refreshment_ids)
                    if refreshments.exists():
                        refreshment_names = ", ".join([refreshment.title for refreshment in refreshments])
                        booking.refreshment_names = refreshment_names
                    else:
                        booking.refreshment_names = ""
                else:
                    booking.refreshment_names = ""

            context = {
                'users': users,
                'all_peripherals': all_peripherals,
                'refreshments': refreshments,
                'rooms': rooms,
                'user': user,
                'bookings': bookings,
                'peripheral_names': peripheral_names,
                'refreshment_names': refreshment_names,
                'role': role,
                'selected_user': selected_user,
                'selected_facility': selected_facility,
                'selected_peripheral': selected_peripheral,
                'selected_refreshment': selected_refreshment

            }
            return render(request, 'accounts/usage_report.html', context)
        elif all([selected_user_id, facility_id, peripheral_id]):
            selected_user = int(selected_user_id)
            selected_facility = int(facility_id)
            selected_peripheral = int(peripheral_id)
            user = get_object_or_404(User, id=selected_user_id)

            bookings = Booking.objects.filter(
                user_id=selected_user_id,
                room_id=facility_id,
            ).filter(
                Q(extra_peripherals__startswith=peripheral_id + ',') |
                Q(extra_peripherals__endswith=',' + peripheral_id) |
                Q(extra_peripherals__contains=',' + peripheral_id + ',') |
                Q(extra_peripherals=peripheral_id)
            )
            users = User.objects.all()
            all_peripherals = Facility.objects.all()
            refreshments = Refreshments.objects.all()
            rooms = Rooms.objects.all()

            peripheral_names = None
            for booking in bookings:
                if booking.extra_peripherals:
                    peripheral_ids = set(booking.extra_peripherals.split(','))
                    peripherals = Facility.objects.filter(id__in=peripheral_ids)
                    if peripherals.exists():
                        peripheral_names = ", ".join([peripheral.title for peripheral in peripherals])
                        booking.peripheral_names = peripheral_names
                    else:
                        booking.peripheral_names = ""
                else:
                    booking.peripheral_names = ""

            refreshment_names = None
            for booking in bookings:
                if booking.refreshments:
                    refreshment_ids = set(booking.refreshments.split(','))
                    refreshments = Refreshments.objects.filter(id__in=refreshment_ids)
                    if refreshments.exists():
                        refreshment_names = ", ".join([refreshment.title for refreshment in refreshments])
                        booking.refreshment_names = refreshment_names
                    else:
                        booking.refreshment_names = ""
                else:
                    booking.refreshment_names = ""

            context = {
                'users': users,
                'all_peripherals': all_peripherals,
                'refreshments': refreshments,
                'rooms': rooms,
                'user': user,
                'bookings': bookings,
                'peripheral_names': peripheral_names,
                'refreshment_names': refreshment_names,
                'role': role,
                'selected_user': selected_user,
                'selected_facility': selected_facility,
                'selected_peripheral': selected_peripheral,
            }
            return render(request, 'accounts/usage_report.html', context)
        # -----------------------user and facility------------------------>
        elif selected_user_id and facility_id:
            selected_user = int(selected_user_id)
            selected_facility = int(facility_id)
            user = get_object_or_404(User, id=selected_user_id)
            facility = get_object_or_404(Rooms, id=facility_id)
            bookings = Booking.objects.filter(Q(user_id=user) & Q(room_id=facility))

            peripheral_names = None
            for booking in bookings:
                if booking.extra_peripherals:
                    peripheral_ids = set(booking.extra_peripherals.split(','))
                    peripherals = Facility.objects.filter(id__in=peripheral_ids)
                    if peripherals.exists():
                        peripheral_names = ", ".join([peripheral.title for peripheral in peripherals])
                        booking.peripheral_names = peripheral_names
                    else:
                        booking.peripheral_names = ""
                else:
                    booking.peripheral_names = ""

            refreshment_names = None
            for booking in bookings:
                if booking.refreshments:
                    refreshment_ids = set(booking.refreshments.split(','))
                    refreshments = Refreshments.objects.filter(id__in=refreshment_ids)
                    if refreshments.exists():
                        refreshment_names = ", ".join([refreshment.title for refreshment in refreshments])
                        booking.refreshment_names = refreshment_names
                    else:
                        booking.refreshment_names = ""
                else:
                    booking.refreshment_names = ""

            context = {
                'users': users,
                'all_peripherals': all_peripherals,
                'refreshments': refreshments,
                'rooms': rooms,
                'bookings': bookings,
                'peripheral_names': peripheral_names,
                'refreshment_names': refreshment_names,
                'role': role,
                'selected_user': selected_user,
                'selected_facility': selected_facility,
                'peripheral_id': peripheral_id,
                'refreshment_id': refreshment_id

            }

            return render(request, 'accounts/usage_report.html', context)
        elif selected_user_id and peripheral_id:
            selected_user = int(selected_user_id)
            selected_peripheral = int(peripheral_id)
            bookings = Booking.objects.filter(
                user_id=selected_user_id
            ).filter(
                Q(extra_peripherals__startswith=peripheral_id + ',') |
                Q(extra_peripherals__endswith=',' + peripheral_id) |
                Q(extra_peripherals__contains=',' + peripheral_id + ',') |
                Q(extra_peripherals=peripheral_id)
            )

            peripheral_names = None
            for booking in bookings:
                if booking.extra_peripherals:
                    peripheral_ids = set(booking.extra_peripherals.split(','))
                    peripherals = Facility.objects.filter(id__in=peripheral_ids)
                    if peripherals.exists():
                        peripheral_names = ", ".join([peripheral.title for peripheral in peripherals])
                        booking.peripheral_names = peripheral_names
                    else:
                        booking.peripheral_names = ""
                else:
                    booking.peripheral_names = ""

            refreshment_names = None
            for booking in bookings:
                if booking.refreshments:
                    refreshment_ids = set(booking.refreshments.split(','))
                    refreshments = Refreshments.objects.filter(id__in=refreshment_ids)
                    if refreshments.exists():
                        refreshment_names = ", ".join([refreshment.title for refreshment in refreshments])
                        booking.refreshment_names = refreshment_names
                    else:
                        booking.refreshment_names = ""
                else:
                    booking.refreshment_names = ""

            context = {
                'users': users,
                'all_peripherals': all_peripherals,
                'refreshments': refreshments,
                'rooms': rooms,
                'bookings': bookings,
                'peripheral_names': peripheral_names,
                'refreshment_names': refreshment_names,
                'role': role,
                'selected_user': selected_user,
                'selected_peripheral': selected_peripheral,
            }

            return render(request, 'accounts/usage_report.html', context)
        elif selected_user_id and refreshment_id:
            selected_user = int(selected_user_id)
            selected_refreshment = int(refreshment_id)
            bookings = Booking.objects.filter(
                user_id=selected_user_id
            ).filter(
                Q(refreshments__startswith=refreshment_id + ',') |
                Q(refreshments__endswith=',' + refreshment_id) |
                Q(refreshments__contains=',' + refreshment_id + ',') |
                Q(refreshments=refreshment_id)
            )

            peripheral_names = None
            for booking in bookings:
                if booking.extra_peripherals:
                    peripheral_ids = set(booking.extra_peripherals.split(','))
                    peripherals = Facility.objects.filter(id__in=peripheral_ids)
                    if peripherals.exists():
                        peripheral_names = ", ".join([peripheral.title for peripheral in peripherals])
                        booking.peripheral_names = peripheral_names
                    else:
                        booking.peripheral_names = ""
                else:
                    booking.peripheral_names = ""

            refreshment_names = None
            for booking in bookings:
                if booking.refreshments:
                    refreshment_ids = set(booking.refreshments.split(','))
                    refreshments = Refreshments.objects.filter(id__in=refreshment_ids)
                    if refreshments.exists():
                        refreshment_names = ", ".join([refreshment.title for refreshment in refreshments])
                        booking.refreshment_names = refreshment_names
                    else:
                        booking.refreshment_names = ""
                else:
                    booking.refreshment_names = ""

            context = {
                'users': users,
                'all_peripherals': all_peripherals,
                'refreshments': refreshments,
                'rooms': rooms,
                'bookings': bookings,
                'peripheral_names': peripheral_names,
                'refreshment_names': refreshment_names,
                'role': role,
                'selected_user': selected_user,
                'selected_refreshment': selected_refreshment,
            }

            return render(request, 'accounts/usage_report.html', context)
        elif selected_user_id and datefrom:
            selected_user = int(selected_user_id)
            selected_from_date = datefrom
            bookings = Booking.objects.filter(
                user_id=selected_user_id,
                date_start__gte=datetime.strptime(datefrom, '%Y-%m-%d').date(),
            )
            peripheral_names = None
            for booking in bookings:
                if booking.extra_peripherals:
                    peripheral_ids = set(booking.extra_peripherals.split(','))
                    peripherals = Facility.objects.filter(id__in=peripheral_ids)
                    if peripherals.exists():
                        peripheral_names = ", ".join([peripheral.title for peripheral in peripherals])
                        booking.peripheral_names = peripheral_names
                    else:
                        booking.peripheral_names = ""
                else:
                    booking.peripheral_names = ""

            refreshment_names = None
            for booking in bookings:
                if booking.refreshments:
                    refreshment_ids = set(booking.refreshments.split(','))
                    refreshments = Refreshments.objects.filter(id__in=refreshment_ids)
                    if refreshments.exists():
                        refreshment_names = ", ".join([refreshment.title for refreshment in refreshments])
                        booking.refreshment_names = refreshment_names
                    else:
                        booking.refreshment_names = ""
                else:
                    booking.refreshment_names = ""

            context = {
                'users': users,
                'all_peripherals': all_peripherals,
                'refreshments': refreshments,
                'rooms': rooms,
                'bookings': bookings,
                'peripheral_names': peripheral_names,
                'refreshment_names': refreshment_names,
                'role': role,
                'selected_user': selected_user,
                'selected_from_date': selected_from_date
            }
            return render(request, 'accounts/usage_report.html', context)
        elif selected_user_id and dateto:
            selected_user = int(selected_user_id)
            selected_to_date = dateto
            bookings = Booking.objects.filter(
                user_id=selected_user_id,
                date_start__lte=datetime.strptime(dateto, '%Y-%m-%d').date(),
            )
            peripheral_names = None
            for booking in bookings:
                if booking.extra_peripherals:
                    peripheral_ids = set(booking.extra_peripherals.split(','))
                    peripherals = Facility.objects.filter(id__in=peripheral_ids)
                    if peripherals.exists():
                        peripheral_names = ", ".join([peripheral.title for peripheral in peripherals])
                        booking.peripheral_names = peripheral_names
                    else:
                        booking.peripheral_names = ""
                else:
                    booking.peripheral_names = ""

            refreshment_names = None
            for booking in bookings:
                if booking.refreshments:
                    refreshment_ids = set(booking.refreshments.split(','))
                    refreshments = Refreshments.objects.filter(id__in=refreshment_ids)
                    if refreshments.exists():
                        refreshment_names = ", ".join([refreshment.title for refreshment in refreshments])
                        booking.refreshment_names = refreshment_names
                    else:
                        booking.refreshment_names = ""
                else:
                    booking.refreshment_names = ""

            context = {
                'users': users,
                'all_peripherals': all_peripherals,
                'refreshments': refreshments,
                'rooms': rooms,
                'bookings': bookings,
                'peripheral_names': peripheral_names,
                'refreshment_names': refreshment_names,
                'role': role,
                'selected_user': selected_user,
                'selected_to_date': selected_to_date
            }
            return render(request, 'accounts/usage_report.html', context)
        elif datefrom:
            selected_from_date = datefrom
            bookings = Booking.objects.filter(
                date_start__gte=datetime.strptime(datefrom, '%Y-%m-%d').date(),
            )
            peripheral_names = None
            for booking in bookings:
                if booking.extra_peripherals:
                    peripheral_ids = set(booking.extra_peripherals.split(','))
                    peripherals = Facility.objects.filter(id__in=peripheral_ids)
                    if peripherals.exists():
                        peripheral_names = ", ".join([peripheral.title for peripheral in peripherals])
                        booking.peripheral_names = peripheral_names
                    else:
                        booking.peripheral_names = ""
                else:
                    booking.peripheral_names = ""

            refreshment_names = None
            for booking in bookings:
                if booking.refreshments:
                    refreshment_ids = set(booking.refreshments.split(','))
                    refreshments = Refreshments.objects.filter(id__in=refreshment_ids)
                    if refreshments.exists():
                        refreshment_names = ", ".join([refreshment.title for refreshment in refreshments])
                        booking.refreshment_names = refreshment_names
                    else:
                        booking.refreshment_names = ""
                else:
                    booking.refreshment_names = ""

            context = {
                'users': users,
                'all_peripherals': all_peripherals,
                'refreshments': refreshments,
                'rooms': rooms,
                'bookings': bookings,
                'peripheral_names': peripheral_names,
                'refreshment_names': refreshment_names,
                'role': role,
                'selected_from_date': selected_from_date
            }
            return render(request, 'accounts/usage_report.html', context)
        elif dateto:
            selected_to_date = dateto
            bookings = Booking.objects.filter(
                date_start__lte=datetime.strptime(dateto, '%Y-%m-%d').date(),
            )
            peripheral_names = None
            for booking in bookings:
                if booking.extra_peripherals:
                    peripheral_ids = set(booking.extra_peripherals.split(','))
                    peripherals = Facility.objects.filter(id__in=peripheral_ids)
                    if peripherals.exists():
                        peripheral_names = ", ".join([peripheral.title for peripheral in peripherals])
                        booking.peripheral_names = peripheral_names
                    else:
                        booking.peripheral_names = ""
                else:
                    booking.peripheral_names = ""

            refreshment_names = None
            for booking in bookings:
                if booking.refreshments:
                    refreshment_ids = set(booking.refreshments.split(','))
                    refreshments = Refreshments.objects.filter(id__in=refreshment_ids)
                    if refreshments.exists():
                        refreshment_names = ", ".join([refreshment.title for refreshment in refreshments])
                        booking.refreshment_names = refreshment_names
                    else:
                        booking.refreshment_names = ""
                else:
                    booking.refreshment_names = ""

            context = {
                'users': users,
                'all_peripherals': all_peripherals,
                'refreshments': refreshments,
                'rooms': rooms,
                'bookings': bookings,
                'peripheral_names': peripheral_names,
                'refreshment_names': refreshment_names,
                'role': role,
                'selected_to_date': selected_to_date
            }
            return render(request, 'accounts/usage_report.html', context)
        elif selected_user_id:
            selected_user = int(selected_user_id)
            bookings = Booking.objects.filter(user_id=selected_user_id)
            peripheral_names = None
            for booking in bookings:
                if booking.extra_peripherals:
                    peripheral_ids = set(booking.extra_peripherals.split(','))
                    peripherals = Facility.objects.filter(id__in=peripheral_ids)
                    if peripherals.exists():
                        peripheral_names = ", ".join([peripheral.title for peripheral in peripherals])
                        booking.peripheral_names = peripheral_names
                    else:
                        booking.peripheral_names = ""
                else:
                    booking.peripheral_names = ""

            refreshment_names = None
            for booking in bookings:
                if booking.refreshments:
                    refreshment_ids = set(booking.refreshments.split(','))
                    refreshments = Refreshments.objects.filter(id__in=refreshment_ids)
                    if refreshments.exists():
                        refreshment_names = ", ".join([refreshment.title for refreshment in refreshments])
                        booking.refreshment_names = refreshment_names
                    else:
                        booking.refreshment_names = ""
                else:
                    booking.refreshment_names = ""

            context = {
                'users': users,
                'all_peripherals': all_peripherals,
                'refreshments': refreshments,
                'rooms': rooms,
                'bookings': bookings,
                'peripheral_names': peripheral_names,
                'refreshment_names': refreshment_names,
                'role': role,
                'selected_user': selected_user,
            }

            return render(request, 'accounts/usage_report.html', context)
        elif all([facility_id]):
            facility = get_object_or_404(Rooms, id=facility_id)
            selected_user = int(selected_user_id)
            selected_facility = int(facility_id)
            bookings = Booking.objects.filter(room_id=facility)

            peripheral_names = None
            for booking in bookings:
                if booking.extra_peripherals:
                    peripheral_ids = set(booking.extra_peripherals.split(','))
                    peripherals = Facility.objects.filter(id__in=peripheral_ids)
                    if peripherals.exists():
                        peripheral_names = ", ".join([peripheral.title for peripheral in peripherals])
                        booking.peripheral_names = peripheral_names
                    else:
                        booking.peripheral_names = ""
                else:
                    booking.peripheral_names = ""

            refreshment_names = None
            for booking in bookings:
                if booking.refreshments:
                    refreshment_ids = set(booking.refreshments.split(','))
                    refreshments = Refreshments.objects.filter(id__in=refreshment_ids)
                    if refreshments.exists():
                        refreshment_names = ", ".join([refreshment.title for refreshment in refreshments])
                        booking.refreshment_names = refreshment_names
                    else:
                        booking.refreshment_names = ""
                else:
                    booking.refreshment_names = ""

            context = {
                'users': users,
                'all_peripherals': all_peripherals,
                'refreshments': refreshments,
                'rooms': rooms,
                'bookings': bookings,
                'peripheral_names': peripheral_names,
                'refreshment_names': refreshment_names,
                'role': role,
                'selected_user': selected_user,
                'selected_facility': selected_facility,
                'peripheral_id': peripheral_id,
                'refreshment_id': refreshment_id
            }

            return render(request, 'accounts/usage_report.html', context)
        elif peripheral_id:
            selected_peripheral = int(peripheral_id)
            bookings = Booking.objects.filter(
                Q(extra_peripherals__startswith=peripheral_id + ',') |
                Q(extra_peripherals__endswith=',' + peripheral_id) |
                Q(extra_peripherals__contains=',' + peripheral_id + ',') |
                Q(extra_peripherals=peripheral_id)
            )

            peripheral_names = None
            for booking in bookings:
                if booking.extra_peripherals:
                    peripheral_ids = set(booking.extra_peripherals.split(','))
                    peripherals = Facility.objects.filter(id__in=peripheral_ids)
                    if peripherals.exists():
                        peripheral_names = ", ".join([peripheral.title for peripheral in peripherals])
                        booking.peripheral_names = peripheral_names
                    else:
                        booking.peripheral_names = ""
                else:
                    booking.peripheral_names = ""

            refreshment_names = None
            for booking in bookings:
                if booking.refreshments:
                    refreshment_ids = set(booking.refreshments.split(','))
                    refreshments = Refreshments.objects.filter(id__in=refreshment_ids)
                    if refreshments.exists():
                        refreshment_names = ", ".join([refreshment.title for refreshment in refreshments])
                        booking.refreshment_names = refreshment_names
                    else:
                        booking.refreshment_names = ""
                else:
                    booking.refreshment_names = ""

            context = {
                'users': users,
                'all_peripherals': all_peripherals,
                'refreshments': refreshments,
                'rooms': rooms,
                'bookings': bookings,
                'peripheral_names': peripheral_names,
                'refreshment_names': refreshment_names,
                'role': role,
                'selected_peripheral': selected_peripheral,
                'refreshment_id': refreshment_id
            }

            return render(request, 'accounts/usage_report.html', context)
        elif refreshment_id:
            selected_refreshment = int(refreshment_id)
            bookings = Booking.objects.filter(
                Q(refreshments__startswith=refreshment_id + ',') |
                Q(refreshments__endswith=',' + refreshment_id) |
                Q(refreshments__contains=',' + refreshment_id + ',') |
                Q(refreshments=refreshment_id)
            )

            peripheral_names = None
            for booking in bookings:
                if booking.extra_peripherals:
                    peripheral_ids = set(booking.extra_peripherals.split(','))
                    peripherals = Facility.objects.filter(id__in=peripheral_ids)
                    if peripherals.exists():
                        peripheral_names = ", ".join([peripheral.title for peripheral in peripherals])
                        booking.peripheral_names = peripheral_names
                    else:
                        booking.peripheral_names = ""
                else:
                    booking.peripheral_names = ""

            refreshment_names = None
            for booking in bookings:
                if booking.refreshments:
                    refreshment_ids = set(booking.refreshments.split(','))
                    refreshments = Refreshments.objects.filter(id__in=refreshment_ids)
                    if refreshments.exists():
                        refreshment_names = ", ".join([refreshment.title for refreshment in refreshments])
                        booking.refreshment_names = refreshment_names
                    else:
                        booking.refreshment_names = ""
                else:
                    booking.refreshment_names = ""

            context = {
                'users': users,
                'all_peripherals': all_peripherals,
                'refreshments': refreshments,
                'rooms': rooms,
                'bookings': bookings,
                'peripheral_names': peripheral_names,
                'refreshment_names': refreshment_names,
                'role': role,
                'peripheral_id': peripheral_id,
                'selected_refreshment': selected_refreshment

            }

            return render(request, 'accounts/usage_report.html', context)
    peripheral_names = None
    for booking in bookings:
        if booking.extra_peripherals:
            peripheral_ids = set(booking.extra_peripherals.split(','))
            peripherals = Facility.objects.filter(id__in=peripheral_ids)
            if peripherals.exists():
                peripheral_names = ", ".join([peripheral.title for peripheral in peripherals])
                booking.peripheral_names = peripheral_names
            else:
                booking.peripheral_names = ""
        else:
            booking.peripheral_names = ""

    refreshment_names = None
    for booking in bookings:
        if booking.refreshments:
            refreshment_ids = set(booking.refreshments.split(','))
            refreshments = Refreshments.objects.filter(id__in=refreshment_ids)
            if refreshments.exists():
                refreshment_names = ", ".join([refreshment.title for refreshment in refreshments])
                booking.refreshment_names = refreshment_names
            else:
                booking.refreshment_names = ""
        else:
            booking.refreshment_names = ""

    context = {
        'users': users,
        'all_peripherals': all_peripherals,
        'refreshments': refreshments,
        'rooms': rooms,
        'bookings': bookings,
        'peripheral_names': peripheral_names,
        'refreshment_names': refreshment_names,
        'role': role
    }

    return render(request, 'accounts/usage_report.html', context)
