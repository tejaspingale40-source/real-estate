// DASHBOARD INTERACTIVE JAVASCRIPT

document.addEventListener('DOMContentLoaded', () => {
    // 1. Multiple Image Upload Preview
    const imageInput = document.getElementById('imageInput');
    const previewContainer = document.getElementById('imagePreviewContainer');

    if (imageInput && previewContainer) {
        imageInput.addEventListener('change', (e) => {
            previewContainer.innerHTML = ''; // Clear previous previews
            const files = Array.from(e.target.files);

            files.forEach((file, index) => {
                if (file.type.startsWith('image/')) {
                    const reader = new FileReader();
                    reader.onload = (evt) => {
                        const card = document.createElement('div');
                        card.className = 'preview-card';
                        
                        const img = document.createElement('img');
                        img.src = evt.target.result;
                        card.appendChild(img);

                        if (index === 0) {
                            const badge = document.createElement('span');
                            badge.className = 'badge-cover';
                            badge.innerText = 'Cover';
                            card.appendChild(badge);
                        }

                        previewContainer.appendChild(card);
                    };
                    reader.readAsDataURL(file);
                }
            });
        });
    }
});
