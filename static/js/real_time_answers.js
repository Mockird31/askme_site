function createAnswerCard(data) {
    const cardHtml = `
        <div class="card w-100 ans" style="width: 18rem;" data-answer-id="${data.answer_id}" data-user-id="${data.user_id}">
            <div class="card-body">
                <div class="row">
                    <div class="col-3">
                        <div class="border mb-2" style="height: 100px">
                            ${data.image_path
            ? `<img src="${data.image_path}" alt="Avatar" class="img-fluid img-field" style="height: 100px; margin-left: 53px; margin-right: 43px;">`
            : `<img src="/static/img/common_member.png" alt="Avatar" class="img-fluid" style="height: 100px; margin-left: 53px; margin-right: 43px;">`}
                        </div>
                        <div class="d-flex gap-3 mt-3">
                            <button type="submit" class="btn btn-success d-flex align-items-center like-button-answer">
                                <span class="me-1">👍</span>
                                <span class="badge bg-success ms-2 like-counter-answer">0</span>
                            </button>
                            <button type="submit" class="btn btn-danger d-flex align-items-center dislike-button-answer" style="margin-left: 30px;">
                                <span class="me-1">👎</span>
                                <span class="badge bg-danger ms-2 dislike-counter-answer">0</span>
                            </button>
                        </div>
                    </div>
                    <div class="col-9">
                        <div><b class="answer-username">${data.username} replied:</b></div>
                        <p class="card-text">${data.text}</p>
                        <div class="form-check mt-5">
                   
                            <input class="form-check-input" type="checkbox" value="" id="flexCheckDefault">
                            <label class="form-check-label" for="flexCheckDefault">
                                Correct!    
                            </label>
                        </div>
                    </div>
                </div>
            </div>
        </div>
    `;

    const template = document.createElement('div');
    template.innerHTML = cardHtml.trim();
    return template.firstChild;
}
