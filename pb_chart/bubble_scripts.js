function rgbToHex(rgb) {
    let rgbValues = rgb.match(/\d+/g);
    let r = parseInt(rgbValues[0]).toString(16).padStart(2, '0');
    let g = parseInt(rgbValues[1]).toString(16).padStart(2, '0');
    let b = parseInt(rgbValues[2]).toString(16).padStart(2, '0');
    return `#${r}${g}${b}`;
}

function deleteBubble(bubbleNumber) {
    var bubble = document.getElementById("bubble-" + bubbleNumber);
    if (bubble) {
        var rect = bubble.querySelector('button');
        var radius = parseFloat(window.getComputedStyle(rect).getPropertyValue('width')) / 2;
        var bubbleX = parseFloat(window.getComputedStyle(rect).getPropertyValue('left')) + radius;
        var bubbleY = parseFloat(window.getComputedStyle(rect).getPropertyValue('top')) + radius;
        var color = rgbToHex(window.getComputedStyle(rect).getPropertyValue('background-color'));

        bubble.remove();

        var numSmallCircles = Math.floor(Math.PI * Math.pow(radius, 2) / 10) * 0.50;
        var smallCircles = [];
        for (var i = 0; i < numSmallCircles; i++) {
            var angle = Math.random() * 2 * Math.PI;
            var r = Math.sqrt(Math.random()) * radius;
            var xMove = r * Math.cos(angle);
            var yMove = r * Math.sin(angle);

            var smallCircle = document.createElement('div');
            smallCircle.className = 'small-circle';
            smallCircle.style.width = '10px';
            smallCircle.style.height = '10px';
            smallCircle.style.backgroundColor = color;
            smallCircle.style.left = (bubbleX + xMove - 5) + 'px';
            smallCircle.style.top = (bubbleY + yMove - 5) + 'px';
            document.querySelector('.bubble-container').appendChild(smallCircle);
            smallCircles.push(smallCircle);
        }

        setTimeout(() => {
            smallCircles.forEach((circle) => {
                var angle = Math.random() * 2 * Math.PI;
                var distance = Math.random() * 200 + 50;
                circle.style.setProperty('--x', (distance * Math.cos(angle)) + 'px');
                circle.style.setProperty('--y', (distance * Math.sin(angle)) + 'px');
                circle.classList.add('animate-out');
            });
        }, 10);
    }
}

function startChainDeletion(startIndex) {
    let bubbleIndex = 0;
    deleteNextBubble();

    function deleteNextBubble() {
        if (bubbleIndex < numBubbles) {
            deleteBubble(bubbleIndex);
            bubbleIndex++;
            setTimeout(deleteNextBubble, 500);
        }
    }
}

function showOverlay(Word, mean, example, count) {
    var overlay = document.getElementById('overlay');
    var title = document.getElementById('overlay-title');
    var message = document.getElementById('overlay-message');
    title.innerText = Word;  // ボタン名をオーバーレイのタイトルに設定
    message.innerText = `単語の意味: ${mean}\n例文: ${example}\n回数: ${count}`;
    overlay.classList.add('active');
}

function closeOverlay() {
    var overlay = document.getElementById('overlay');
    overlay.classList.remove('active');
}
