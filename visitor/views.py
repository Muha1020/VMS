from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from .models import Visitor, Blacklist
from django.utils import timezone
from datetime import timedelta

@login_required
def index(request):
    # Dashboard logic
    today = timezone.now().date()
    visitors_today = Visitor.objects.filter(check_in_time__date=today)
    
    active_count = Visitor.objects.filter(status='Checked In').count()
    today_count = visitors_today.count()
    
    recent_visitors = Visitor.objects.order_by('-check_in_time')[:5]
    
    context = {
        'active_count': active_count,
        'today_count': today_count,
        'recent_visitors': recent_visitors
    }
    return render(request, 'visitor/index.html', context)

@login_required
def register_visitor(request):
    # Security personnel check
    if hasattr(request.user, 'profile') and request.user.profile.dept == 'Security Unit':
        if request.method == 'POST':
            first_name = request.POST.get('first_name')
            last_name = request.POST.get('last_name')
            phone = request.POST.get('phone')
            email = request.POST.get('email')
            host_name = request.POST.get('host_name')
            purpose_of_visit = request.POST.get('purpose_of_visit')
            address = request.POST.get('address')
            
            if Blacklist.objects.filter(phone=phone).exists():
                entry = Blacklist.objects.get(phone=phone)
                messages.error(request, f'Entry denied: {first_name} {last_name} is blacklisted. Reason: {entry.reason}')
                return redirect('visitor')

            Visitor.objects.create(
                first_name=first_name,
                last_name=last_name,
                phone=phone,
                email=email,
                host_name=host_name,
                purpose_of_visit=purpose_of_visit,
                address=address,
                recorded_by=request.user
            )
            messages.success(request, f'Visitor {first_name} {last_name} successfully checked in.')
            return redirect('index')
            
        return render(request, 'visitor/visitor.html')
    else:
        messages.error(request, 'Only Security Unit personnel can register visitors.')
        return redirect('index')

@login_required
def report(request):
    visitors = Visitor.objects.order_by('-check_in_time')
    return render(request, 'visitor/report.html', {'visitors': visitors})

@login_required
def checkout_visitor(request, visitor_id):
    if hasattr(request.user, 'profile') and request.user.profile.dept == 'Security Unit':
        visitor = get_object_or_404(Visitor, id=visitor_id)
        if visitor.status == 'Checked In':
            visitor.status = 'Checked Out'
            visitor.check_out_time = timezone.now()
            visitor.save()
            messages.success(request, f'Visitor {visitor.first_name} {visitor.last_name} has been checked out.')
        return redirect(request.META.get('HTTP_REFERER', 'index'))
    else:
        messages.error(request, 'Only Security Unit personnel can check out visitors.')
        return redirect('index')


@login_required
def blacklist_visitor(request, visitor_id):
    if not (hasattr(request.user, 'profile') and request.user.profile.dept == 'Security Unit'):
        messages.error(request, 'Only Security Unit personnel can blacklist visitors.')
        return redirect('index')

    visitor = get_object_or_404(Visitor, id=visitor_id)

    if request.method == 'POST':
        reason = request.POST.get('reason', '').strip()
        if not reason:
            messages.error(request, 'A reason is required to blacklist a visitor.')
            return redirect(request.META.get('HTTP_REFERER', 'report'))

        Blacklist.objects.update_or_create(
            phone=visitor.phone,
            defaults={
                'first_name': visitor.first_name,
                'last_name': visitor.last_name,
                'reason': reason,
                'blacklisted_by': request.user,
            }
        )
        messages.success(request, f'{visitor.first_name} {visitor.last_name} has been blacklisted.')
        return redirect('blacklist_list')

    return render(request, 'visitor/blacklist_confirm.html', {'visitor': visitor})


@login_required
def blacklist_list(request):
    entries = Blacklist.objects.order_by('-blacklisted_at')
    return render(request, 'visitor/blacklist.html', {'entries': entries})


@login_required
def remove_blacklist(request, entry_id):
    if not (hasattr(request.user, 'profile') and request.user.profile.dept == 'Security Unit'):
        messages.error(request, 'Only Security Unit personnel can manage the blacklist.')
        return redirect('index')

    entry = get_object_or_404(Blacklist, id=entry_id)
    if request.method == 'POST':
        name = f'{entry.first_name} {entry.last_name}'
        entry.delete()
        messages.success(request, f'{name} has been removed from the blacklist.')
    return redirect('blacklist_list')
