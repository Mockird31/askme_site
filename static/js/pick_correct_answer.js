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