
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

const cards = document.getElementsByClassName('card w-100');
for (const card of cards) {
    const likeButton_question = card.querySelector('.like-button-question');
    const likeCounter_question = card.querySelector('.like-counter-question');

    const dislikeButton_question = card.querySelector('.dislike-button-question');
    const dislikeCounter_question = card.querySelector('.dislike-counter-question');

    const question_id = card.dataset.questionId;

    likeButton_question.addEventListener('click', () => {
        fetch(`/${question_id}/like_question_async`, {
            method: "POST",
            headers: {'X-CSRFToken': getCookie('csrftoken')},
        })
        .then(response => response.json())
        .then(data => {
            likeCounter_question.innerHTML = data.likes_count;
            dislikeCounter_question.innerHTML = data.dislikes_count;
        });
    });

    dislikeButton_question.addEventListener('click', () => {
        fetch(`/${question_id}/dislike_question_async`, {
            method: "POST",
            headers: {'X-CSRFToken': getCookie('csrftoken')},
        })
        .then(response => response.json())
        .then(data => {
            likeCounter_question.innerHTML = data.likes_count;
            dislikeCounter_question.innerHTML = data.dislikes_count;
        });
    });
}