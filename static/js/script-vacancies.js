let vacancies = document.querySelectorAll('.vacancy');

for (let vacancy of vacancies) {
    let hiddenParts = vacancy.querySelectorAll('.hidden');
    let hiddenImg = vacancy.querySelector('.hidden-img');
    vacancy.onclick = function (evt) {
        evt.preventDefault();
        for (let hiddenPart of hiddenParts) {
        hiddenPart.classList.remove('hidden');
        }
        hiddenImg.classList.remove('hidden-img');
        vacancy.classList.remove("vacancy-hidden");
    }
};


