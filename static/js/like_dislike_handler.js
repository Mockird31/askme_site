// script.js

document.addEventListener('click', function(event) {
    // Проверяем, была ли нажата кнопка лайка
    if (event.target.closest('.like-button')) {
        const likeButton = event.target.closest('.like-button');
        const dislikeButton = likeButton.closest('.card-body').querySelector('.dislike-button');
        toggleButton(likeButton, dislikeButton);
    }
    // Проверяем, была ли нажата кнопка дизлайка
    else if (event.target.closest('.dislike-button')) {
        const dislikeButton = event.target.closest('.dislike-button');
        const likeButton = dislikeButton.closest('.card-body').querySelector('.like-button');
        toggleButton(dislikeButton, likeButton);
    }
});

function toggleButton(button, oppositeButton) {
    // Получаем текущий счетчик из data-атрибута
    let count = parseInt(button.getAttribute('data-count'));

    // Убираем активность с противоположной кнопки и уменьшаем её счетчик, если она активна
    if (oppositeButton.classList.contains('active')) {
        oppositeButton.classList.remove('active');
        let oppositeCount = parseInt(oppositeButton.getAttribute('data-count')) - 1;
        oppositeButton.setAttribute('data-count', oppositeCount);
        oppositeButton.querySelector('.badge').textContent = oppositeCount;
    }

    // Если кнопка активна, уменьшаем счетчик, иначе увеличиваем
    count = button.classList.toggle('active') ? count + 1 : count - 1;

    // Обновляем отображаемый счетчик
    button.querySelector('.badge').textContent = count;

    // Сохраняем обновленный счетчик в data-атрибут
    button.setAttribute('data-count', count);
}
