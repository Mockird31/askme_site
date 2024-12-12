function getCookie(name) {
    let cookieValue = null;
    if (document.cookie && document.cookie !== '') {
        const cookies = document.cookie.split(';');
        for (let i = 0; i < cookies.length; i++) {
            const cookie = cookies[i].trim();
            // Проверяем, начинается ли эта строка с нужного нам имени
            if (cookie.substring(0, name.length + 1) === (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}

const answers = document.getElementsByClassName('card w-100 ans');
for (const answer of answers) {
    const correctButton = answer.querySelector('.form-check-input');

    const answer_id = answer.dataset.answerId;

    correctButton.addEventListener('change', () => {
        console.log('success');
        fetch(`/${answer_id}/pick_correct_answer`, {
            method: "POST",
            headers: {'X-CSRFToken': getCookie('csrftoken')},
        })
        .then(response => response.json())
        .then(data => {
            if (data.status == 'error') {
                alert(data.message);
            }

            if (data.is_correct == 'p') {
                correctButton.checked = false;
            }
            else {
                correctButton.checked = true;
            }
        });
    });
}