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

    // 2. Video File Selection & Size Preview Indicator
    const videoInput = document.getElementById('videoInput');
    const videoFileInfo = document.getElementById('videoFileInfo');

    if (videoInput && videoFileInfo) {
        videoInput.addEventListener('change', (e) => {
            const file = e.target.files[0];
            if (file) {
                const fileSizeMB = (file.size / (1024 * 1024)).toFixed(2);
                let warningText = '';
                if (fileSizeMB > 50) {
                    warningText = ` <br><strong style="color: #e11d48;">⚡ Large video file (${fileSizeMB} MB)! Upload may take 1-2 minutes depending on connection. Consider using YouTube or Cloudinary URL for faster loading.</strong>`;
                }
                videoFileInfo.style.display = 'block';
                videoFileInfo.innerHTML = `📹 <strong>Selected Video:</strong> ${file.name} (${fileSizeMB} MB)${warningText}`;
            } else {
                videoFileInfo.style.display = 'none';
                videoFileInfo.innerHTML = '';
            }
        });
    }

    // 3. Form Submit Progress Loader Overlay
    const formCard = document.querySelector('form.form-card');
    const uploadProgressOverlay = document.getElementById('uploadProgressOverlay');
    const uploadOverlayMessage = document.getElementById('uploadOverlayMessage');
    const savePropertyBtn = document.getElementById('savePropertyBtn');

    if (formCard && uploadProgressOverlay) {
        formCard.addEventListener('submit', () => {
            const hasVideo = videoInput && videoInput.files && videoInput.files.length > 0;
            const hasImages = imageInput && imageInput.files && imageInput.files.length > 0;

            if (hasVideo) {
                const file = videoInput.files[0];
                const fileSizeMB = (file.size / (1024 * 1024)).toFixed(1);
                uploadOverlayMessage.innerHTML = `Uploading property video (${fileSizeMB} MB) and saving data...<br>Please wait, do not close or refresh this page.`;
            } else if (hasImages) {
                uploadOverlayMessage.innerHTML = `Uploading images and saving property...<br>Please wait a moment.`;
            } else {
                uploadOverlayMessage.innerHTML = `Saving property details...`;
            }

            uploadProgressOverlay.style.display = 'flex';
            if (savePropertyBtn) {
                savePropertyBtn.disabled = true;
                savePropertyBtn.innerHTML = '⌛ Saving...';
            }
        });
    }
});
