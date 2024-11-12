function previewImage() {
    const file = document.getElementById('avatar').files[0];
    const preview = document.getElementById('avatarPreview');

    const reader = new FileReader();
    reader.addEventListener("load", function () {
        preview.src = reader.result;
    }, false);

    if (file) {
        reader.readAsDataURL(file);
    }
}