from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from .models import Visitor
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
