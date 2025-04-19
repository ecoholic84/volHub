// Typing effect for Volhub landing page (vanilla JS)
// Usage: typingEffect(targetElement, ["word1", "word2", ...])
function typingEffect(element, words, typeSpeed = 110, pauseEnd = 1500, pauseStart = 20) {
    let textIndex = 0;
    let charIndex = 0;
    let direction = 'forward';
    let typingInterval;
    const cursor = element.querySelector('.typing-cursor');

    function startTyping() {
        const current = words[textIndex];
        if (charIndex > current.length) {
            direction = 'backward';
            clearInterval(typingInterval);
            setTimeout(() => {
                typingInterval = setInterval(startTyping, typeSpeed);
            }, pauseEnd);
        }
        element.querySelector('.typing-text').textContent = current.substring(0, charIndex);
        if (direction === 'forward') {
            charIndex++;
        } else {
            if (charIndex === 0) {
                direction = 'forward';
                clearInterval(typingInterval);
                setTimeout(() => {
                    textIndex++;
                    if (textIndex >= words.length) textIndex = 0;
                    typingInterval = setInterval(startTyping, typeSpeed);
                }, pauseStart);
            }
            charIndex--;
        }
    }

    typingInterval = setInterval(startTyping, typeSpeed);
    setInterval(() => {
        if (cursor) cursor.classList.toggle('hidden');
    }, 550);
}

// To use: after DOM loaded
// typingEffect(document.getElementById('volhub-typing'), ["made alone", "possible without unity", "done without teamwork"]);
