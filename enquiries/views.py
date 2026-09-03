from django.shortcuts import render, get_object_or_404, redirect
from django.contrib import messages
from django.contrib.admin.views.decorators import staff_member_required
from .models import Enquiry
from .forms import EnquiryStatusForm


@staff_member_required(login_url='dashboard_login')
def dashboard_enquiries_list(request):
    enquiries = Enquiry.objects.select_related('property').order_by('-created_at')
    
    # Filter by status if requested
    status_filter = request.GET.get('status', '').strip()
    if status_filter:
        enquiries = enquiries.filter(status=status_filter)

    return render(request, 'dashboard/enquiries_list.html', {
        'enquiries': enquiries,
        'selected_status': status_filter,
        'status_choices': Enquiry.STATUS_CHOICES,
    })


@staff_member_required(login_url='dashboard_login')
def dashboard_enquiry_update_status(request, pk):
    enquiry = get_object_or_404(Enquiry, pk=pk)
    if request.method == 'POST':
        new_status = request.POST.get('status')
        if new_status in dict(Enquiry.STATUS_CHOICES):
            enquiry.status = new_status
            enquiry.save()
            messages.success(request, f"Enquiry #{enquiry.id} status updated to '{new_status}'.")
        else:
            messages.error(request, "Invalid status choice.")
    return redirect('dashboard_enquiries')


@staff_member_required(login_url='dashboard_login')
def dashboard_enquiry_delete(request, pk):
    enquiry = get_object_or_404(Enquiry, pk=pk)
    if request.method == 'POST':
        enquiry_id = enquiry.id
        client_name = enquiry.name
        enquiry.delete()
        messages.success(request, f"Enquiry #{enquiry_id} from '{client_name}' has been deleted successfully.")
    return redirect('dashboard_enquiries')


from urllib.parse import quote

def quick_enquiry_submit(request):
    if request.method == 'POST':
        name = request.POST.get('name', '').strip()
        phone = request.POST.get('phone', '').strip()
        email = request.POST.get('email', '').strip()
        message = request.POST.get('message', 'Quick Enquiry from Website Popup').strip()

        if name and phone and email:
            Enquiry.objects.create(
                name=name,
                phone=phone,
                email=email,
                message=message
            )
            msg_text = f"Hello Perfect Homes, I submitted a quick enquiry.\nName: {name}\nPhone: {phone}\nEmail: {email}\nMessage: {message}"
            wa_url = f"https://wa.me/917083150302?text={quote(msg_text)}"
            request.session['whatsapp_url'] = wa_url

            messages.success(request, "Thank you! Your enquiry has been received. Redirecting to WhatsApp to send message...")
        else:
            messages.error(request, "Please fill in all required fields in the enquiry form.")

    next_url = request.META.get('HTTP_REFERER', '/')
    return redirect(next_url)

