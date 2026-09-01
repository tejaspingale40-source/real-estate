// GALLERY SWITCHER FOR PROPERTY DETAIL PAGE

function switchMainImage(imageUrl, thumbnailElement) {
    const mainImg = document.getElementById('mainGalleryImage');
    if (mainImg) {
        mainImg.src = imageUrl;
    }

    // Toggle active thumbnail class
    const thumbnails = document.querySelectorAll('.thumbnail-item');
    thumbnails.forEach(thumb => thumb.classList.remove('active'));
    if (thumbnailElement) {
        thumbnailElement.classList.add('active');
    }
}
