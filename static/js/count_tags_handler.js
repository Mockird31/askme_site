function validateForm() {
    const tagsInput = document.getElementById("tags").value.trim();
    const tagsArray = tagsInput.split(/\s+/);

    if (tagsArray.length > 3) {
        alert("Please enter no more than 3 tags!");
        return false;
    }

    alert("Form submitted successfully!");
    return true;
}