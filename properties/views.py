from django.shortcuts import render, get_object_or_404, redirect
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.admin.views.decorators import staff_member_required
from django.db.models import Q, Count
from .models import Property, PropertyImage, PropertyVideo, Amenity, SiteSettings
from .forms import PropertyForm, PropertyImageForm, PropertyVideoForm, SiteSettingsForm
from enquiries.models import Enquiry
from enquiries.forms import EnquiryForm


def home_view(request):
    featured_properties = Property.objects.filter(status='Available', featured=True)[:4]
    recent_properties = Property.objects.filter(status='Available').order_by('-created_at')[:6]
    locations = Property.objects.values_list('location', flat=True).distinct()
    featured_video = PropertyVideo.objects.select_related('property').order_by('-created_at').first()
    
    context = {
        'featured_properties': featured_properties,
        'recent_properties': recent_properties,
        'locations': [loc for loc in locations if loc],
        'featured_video': featured_video,
    }
    return render(request, 'home/index.html', context)


def property_list_view(request):
    queryset = Property.objects.all()

    # Search query
    query = request.GET.get('q', '').strip()
    if query:
        queryset = queryset.filter(
            Q(title__icontains=query) |
            Q(location__icontains=query) |
            Q(description__icontains=query) |
            Q(address__icontains=query)
        )

    # Filters
    location = request.GET.get('location', '').strip()
    if location:
        queryset = queryset.filter(Q(location__icontains=location) | Q(address__icontains=location))

    property_type = request.GET.get('property_type', '').strip()
    if property_type:
        queryset = queryset.filter(property_type__iexact=property_type)

    purpose = request.GET.get('purpose', '').strip()
    if purpose:
        queryset = queryset.filter(purpose__iexact=purpose)

    min_price = request.GET.get('min_price', '').strip()
    if min_price and min_price.isdigit():
        queryset = queryset.filter(price__gte=float(min_price))

    max_price = request.GET.get('max_price', '').strip()
    if max_price and max_price.isdigit():
        queryset = queryset.filter(price__lte=float(max_price))

    bedrooms = request.GET.get('bedrooms', '').strip()
    if bedrooms and bedrooms.isdigit():
        queryset = queryset.filter(bedrooms__gte=int(bedrooms))

    locations = Property.objects.values_list('location', flat=True).distinct()

    context = {
        'properties': queryset,
        'locations': [loc for loc in locations if loc],
        'selected_location': location,
        'selected_type': property_type,
        'selected_purpose': purpose,
        'min_price': min_price,
        'max_price': max_price,
        'bedrooms': bedrooms,
        'query': query,
        'total_count': queryset.count(),
    }
    return render(request, 'properties/property_list.html', context)


from urllib.parse import quote

def property_detail_view(request, slug):
    property_obj = get_object_or_404(Property, slug=slug)
    images = property_obj.images.all()
    videos = property_obj.videos.all()
    amenities = property_obj.amenities.all()
    similar_properties = Property.objects.filter(
        property_type=property_obj.property_type
    ).exclude(id=property_obj.id)[:3]

    whatsapp_url = request.session.pop('whatsapp_url', None)

    if request.method == 'POST':
        enquiry_form = EnquiryForm(request.POST)
        if enquiry_form.is_valid():
            enquiry = enquiry_form.save(commit=False)
            enquiry.property = property_obj
            enquiry.save()

            # Construct WhatsApp pre-filled message & redirect URL
            msg_text = f"Hello Perfect Homes, I submitted an enquiry for '{property_obj.title}'.\nName: {enquiry.name}\nPhone: {enquiry.phone}\nMessage: {enquiry.message}"
            wa_url = f"https://wa.me/917083150302?text={quote(msg_text)}"
            request.session['whatsapp_url'] = wa_url

            messages.success(request, "Your enquiry has been submitted successfully! Redirecting to WhatsApp to send message...")
            return redirect('property_detail', slug=property_obj.slug)
        else:
            messages.error(request, "There was an error submitting your enquiry. Please check your inputs.")
    else:
        enquiry_form = EnquiryForm(initial={'property': property_obj.id})

    context = {
        'property': property_obj,
        'images': images,
        'videos': videos,
        'amenities': amenities,
        'similar_properties': similar_properties,
        'enquiry_form': enquiry_form,
        'whatsapp_url': whatsapp_url,
    }
    return render(request, 'properties/property_detail.html', context)


def about_view(request):
    return render(request, 'about/about.html')


def contact_view(request):
    whatsapp_url = request.session.pop('whatsapp_url', None)
    if request.method == 'POST':
        enquiry_form = EnquiryForm(request.POST)
        if enquiry_form.is_valid():
            enquiry = enquiry_form.save()
            msg_text = f"Hello Perfect Homes, I submitted a contact enquiry.\nName: {enquiry.name}\nPhone: {enquiry.phone}\nMessage: {enquiry.message}"
            wa_url = f"https://wa.me/917083150302?text={quote(msg_text)}"
            request.session['whatsapp_url'] = wa_url

            messages.success(request, "Thank you for reaching out! Redirecting to WhatsApp to send your message...")
            return redirect('contact')
        else:
            messages.error(request, "Please correct the errors in the form below.")
    else:
        enquiry_form = EnquiryForm()

    return render(request, 'contact/contact.html', {'enquiry_form': enquiry_form, 'whatsapp_url': whatsapp_url})


# DASHBOARD AUTHENTICATION VIEWS

def dashboard_login_view(request):
    if request.user.is_authenticated and request.user.is_staff:
        return redirect('dashboard')

    next_url = request.GET.get('next', request.POST.get('next', 'dashboard'))

    if request.method == 'POST':
        username_val = request.POST.get('username', '').strip()
        password_val = request.POST.get('password', '')

        user = authenticate(request, username=username_val, password=password_val)

        if user is not None:
            if user.is_staff:
                login(request, user)
                messages.success(request, f"Welcome back, {user.first_name or user.username}!")
                return redirect(next_url or 'dashboard')
            else:
                messages.error(request, "Access denied. Only authorized staff members can access the dashboard.")
        else:
            messages.error(request, "Invalid username or password. Please try again.")

    return render(request, 'dashboard/login.html', {'next_url': next_url})


def dashboard_logout_view(request):
    logout(request)
    messages.info(request, "You have been logged out of the dashboard.")
    return redirect('dashboard_login')


# CUSTOM ADMIN DASHBOARD VIEWS (Protected by staff_member_required)

@staff_member_required(login_url='dashboard_login')
def dashboard_view(request):
    total_properties = Property.objects.count()
    available_properties = Property.objects.filter(status='Available').count()
    sold_properties = Property.objects.filter(status='Sold').count()
    rented_properties = Property.objects.filter(status='Rented').count()
    new_enquiries = Enquiry.objects.filter(status='New').count()
    recent_enquiries = Enquiry.objects.select_related('property').order_by('-created_at')[:5]
    recent_properties = Property.objects.order_by('-created_at')[:5]

    context = {
        'total_properties': total_properties,
        'available_properties': available_properties,
        'sold_properties': sold_properties,
        'rented_properties': rented_properties,
        'new_enquiries': new_enquiries,
        'recent_enquiries': recent_enquiries,
        'recent_properties': recent_properties,
    }
    return render(request, 'dashboard/dashboard.html', context)


@staff_member_required(login_url='dashboard_login')
def dashboard_property_list(request):
    properties = Property.objects.all().order_by('-created_at')
    return render(request, 'dashboard/property_list.html', {'properties': properties})


def ensure_default_amenities():
    if not Amenity.objects.exists():
        default_list = [
            ("Parking", "fa-parking"),
            ("Garden", "fa-tree"),
            ("Security", "fa-shield"),
            ("Water Supply", "fa-tint"),
            ("Electricity", "fa-bolt"),
            ("Road Access", "fa-road"),
            ("Gym", "fa-dumbbell"),
            ("Swimming Pool", "fa-swimming-pool"),
            ("Lift", "fa-elevator"),
            ("Power Backup", "fa-plug"),
            ("CCTV Security", "fa-video"),
            ("Club House", "fa-users"),
            ("Children Play Area", "fa-child"),
        ]
        for name, icon in default_list:
            Amenity.objects.get_or_create(name=name, defaults={'icon': icon})


@staff_member_required(login_url='dashboard_login')
def dashboard_property_add(request):
    ensure_default_amenities()
    if request.method == 'POST':
        form = PropertyForm(request.POST, request.FILES)
        if form.is_valid():
            property_obj = form.save()
            
            # Process custom amenities
            custom_amenities_raw = request.POST.get('custom_amenities', '').strip()
            if custom_amenities_raw:
                new_amenities = []
                for item in custom_amenities_raw.split(','):
                    clean_name = item.strip()
                    if clean_name:
                        amenity_obj, _ = Amenity.objects.get_or_create(name=clean_name)
                        new_amenities.append(amenity_obj)
                if new_amenities:
                    property_obj.amenities.add(*new_amenities)

            # Process uploaded images (multiple files support)
            images = request.FILES.getlist('images')
            for index, img in enumerate(images):
                PropertyImage.objects.create(
                    property=property_obj,
                    image=img,
                    is_cover=(index == 0),
                    order=index
                )

            # Process uploaded video or video URL
            video_file = request.FILES.get('video')
            video_url = request.POST.get('video_url', '').strip()
            if video_file or video_url:
                video_title = request.POST.get('video_title', '').strip() or f"{property_obj.title} Video"
                PropertyVideo.objects.create(
                    property=property_obj,
                    video=video_file if video_file else None,
                    video_url=video_url if video_url else None,
                    title=video_title
                )

            messages.success(request, f"Property '{property_obj.title}' created successfully!")
            return redirect('dashboard_properties')
        else:
            messages.error(request, "Failed to create property. Please check form errors.")
    else:
        form = PropertyForm()

    amenities = Amenity.objects.all()
    return render(request, 'dashboard/property_form.html', {
        'form': form,
        'amenities': amenities,
        'title': 'Add New Property'
    })


@staff_member_required(login_url='dashboard_login')
def dashboard_property_edit(request, pk):
    ensure_default_amenities()
    property_obj = get_object_or_404(Property, pk=pk)
    if request.method == 'POST':
        form = PropertyForm(request.POST, request.FILES, instance=property_obj)
        if form.is_valid():
            property_obj = form.save()
            
            # Process custom amenities
            custom_amenities_raw = request.POST.get('custom_amenities', '').strip()
            if custom_amenities_raw:
                new_amenities = []
                for item in custom_amenities_raw.split(','):
                    clean_name = item.strip()
                    if clean_name:
                        amenity_obj, _ = Amenity.objects.get_or_create(name=clean_name)
                        new_amenities.append(amenity_obj)
                if new_amenities:
                    property_obj.amenities.add(*new_amenities)

            # Process new images if uploaded
            images = request.FILES.getlist('images')
            if images:
                existing_count = property_obj.images.count()
                for index, img in enumerate(images):
                    PropertyImage.objects.create(
                        property=property_obj,
                        image=img,
                        is_cover=(existing_count == 0 and index == 0),
                        order=existing_count + index
                    )

            # Process new video if uploaded or URL provided
            video_file = request.FILES.get('video')
            video_url = request.POST.get('video_url', '').strip()
            if video_file or video_url:
                video_title = request.POST.get('video_title', '').strip() or f"{property_obj.title} Video"
                PropertyVideo.objects.create(
                    property=property_obj,
                    video=video_file if video_file else None,
                    video_url=video_url if video_url else None,
                    title=video_title
                )

            messages.success(request, f"Property '{property_obj.title}' updated successfully!")
            return redirect('dashboard_properties')
        else:
            messages.error(request, "Failed to update property. Please check form errors.")
    else:
        form = PropertyForm(instance=property_obj)

    amenities = Amenity.objects.all()
    return render(request, 'dashboard/property_form.html', {
        'form': form,
        'property': property_obj,
        'amenities': amenities,
        'title': f'Edit Property: {property_obj.title}'
    })


@staff_member_required(login_url='dashboard_login')
def dashboard_property_delete(request, pk):
    property_obj = get_object_or_404(Property, pk=pk)
    if request.method == 'POST':
        title = property_obj.title
        property_obj.delete()
        messages.success(request, f"Property '{title}' deleted successfully.")
        return redirect('dashboard_properties')
    return render(request, 'dashboard/property_confirm_delete.html', {'property': property_obj})


@staff_member_required(login_url='dashboard_login')
def dashboard_property_image_delete(request, pk):
    image_obj = get_object_or_404(PropertyImage, pk=pk)
    property_id = image_obj.property.id
    if request.method == 'POST':
        was_cover = image_obj.is_cover
        image_obj.delete()
        
        # If deleted image was cover, set next available image as cover
        if was_cover:
            next_image = PropertyImage.objects.filter(property_id=property_id).first()
            if next_image:
                next_image.is_cover = True
                next_image.save()
                
        messages.success(request, "Image deleted successfully.")
    return redirect('dashboard_property_edit', pk=property_id)


@staff_member_required(login_url='dashboard_login')
def dashboard_property_video_delete(request, pk):
    video_obj = get_object_or_404(PropertyVideo, pk=pk)
    property_id = video_obj.property.id
    if request.method == 'POST':
        video_obj.delete()
        messages.success(request, "Video deleted successfully.")
    return redirect('dashboard_property_edit', pk=property_id)


@staff_member_required(login_url='dashboard_login')
def dashboard_site_settings(request):
    site_settings, created = SiteSettings.objects.get_or_create(id=1)
    if request.method == 'POST':
        form = SiteSettingsForm(request.POST, instance=site_settings)
        if form.is_valid():
            form.save()
            messages.success(request, "Site Settings, About Us, and Contact content updated successfully!")
            return redirect('dashboard_site_settings')
        else:
            messages.error(request, "Failed to update settings. Please check errors below.")
    else:
        form = SiteSettingsForm(instance=site_settings)

    return render(request, 'dashboard/site_settings.html', {'form': form})


def privacy_policy_view(request):
    return render(request, 'legal/privacy_policy.html')


def terms_of_service_view(request):
    return render(request, 'legal/terms_of_service.html')




