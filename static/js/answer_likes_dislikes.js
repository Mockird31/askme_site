
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

const answers_likes = document.getElementsByClassName('card w-100 ans');

for (const answer of answers_likes) {
    const likeButton_answer = answer.querySelector('.like-button-answer');
    const likeCounter_answer = answer.querySelector('.like-counter-answer');

    const dislikeButton_answer = answer.querySelector('.dislike-button-answer');
    const dislikeCounter_answer = answer.querySelector('.dislike-counter-answer');

    const answer_id = answer.dataset.answerId;

    likeButton_answer.addEventListener('click', () => {
        fetch(`/${answer_id}/like_answer_async`, {
            method: "POST",
            headers: {'X-CSRFToken': getCookie('csrftoken')},
        })
        .then(response => response.json())
        .then(data => {
            likeCounter_answer.innerHTML = data.likes_count;
            dislikeCounter_answer.innerHTML = data.dislikes_count;
        });
    });

    dislikeButton_answer.addEventListener('click', () => {
        fetch(`/${answer_id}/dislike_answer_async`, {
            method: "POST",
            headers: {'X-CSRFToken': getCookie('csrftoken')},
        })
        .then(response => response.json())
        .then(data => {
            likeCounter_answer.innerHTML = data.likes_count;
            dislikeCounter_answer.innerHTML = data.dislikes_count;
        });
    });
}