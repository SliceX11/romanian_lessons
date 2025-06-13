import React, { useState } from 'react';

const Lesson = () => {
  const [currentCard, setCurrentCard] = useState(0);
  const [cardHistory, setCardHistory] = useState<number[]>([]);
  const [showAnswer, setShowAnswer] = useState(false);

  const handleNext = () => {
    setCardHistory([...cardHistory, currentCard]);
    setCurrentCard(currentCard + 1);
    setShowAnswer(false);
  };

  const handlePrevious = () => {
    if (cardHistory.length > 0) {
      const prev = cardHistory[cardHistory.length - 1];
      setCardHistory(cardHistory.slice(0, -1));
      setCurrentCard(prev);
      setShowAnswer(false);
    }
  };

  return (
    <div className="lesson-container">
      {/* ...existing code for lesson content... */}
      <div className="lesson-controls">
        {/* ...existing code for other controls... */}
        {cardHistory.length > 0 && (
          <button onClick={handlePrevious} className="btn btn-secondary">
            ← Предыдущая карточка
          </button>
        )}
      </div>
      {/* ...existing code for lesson footer... */}
    </div>
  );
};

export default Lesson;