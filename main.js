let cards = [
    { text: "Карточка 1" },
    { text: "Карточка 2" },
    { text: "Карточка 3" },
    // Добавьте свои карточки здесь
];

let cardHistory = [];
let currentCardIndex = 0;

function showCard(index) {
    currentCardIndex = index;
    document.getElementById('card-content').textContent = cards[currentCardIndex].text;
}

function nextCard() {
    cardHistory.push(currentCardIndex);
    currentCardIndex++;
    if (currentCardIndex >= cards.length) {
        currentCardIndex = 0; // Вернуться к первой карточке, если достигнут конец
    }
    showCard(currentCardIndex);
}

function previousCard() {
    if (cardHistory.length > 0) {
        currentCardIndex = cardHistory.pop();
        showCard(currentCardIndex);
    }
}

function updateButtonsVisibility() {
    const prevButton = document.getElementById('prev-card-btn');
    if (prevButton) {
        prevButton.style.display = cardHistory.length > 0 ? 'block' : 'none';
    }
}

document.addEventListener('DOMContentLoaded', function() {
    showCard(currentCardIndex);

    const prevButton = document.getElementById('prev-card-btn');
    if (prevButton) {
        prevButton.addEventListener('click', previousCard);
    }

    const nextButton = document.getElementById('next-card-btn');
    if (nextButton) {
        nextButton.addEventListener('click', nextCard);
    }

    updateButtonsVisibility();
});