let bubbleContainer = document.querySelector('.bubble-container');  // ここでbubbleContainerを定義
let bubbleIndex = 0;

function rgbToHex(rgb) {
    // rgbの形式から数値を抽出
    let rgbValues = rgb.match(/\d+/g);

    // 各値を16進数に変換し、2桁の文字列にする
    let r = parseInt(rgbValues[0]).toString(16).padStart(2, '0');
    let g = parseInt(rgbValues[1]).toString(16).padStart(2, '0');
    let b = parseInt(rgbValues[2]).toString(16).padStart(2, '0');

    // #RRGGBB形式で文字列として返す
    return `#${r}${g}${b}`;
}

function deleteBubble(bubbleNumber) {
    var bubble = document.getElementById("bubble-" + bubbleNumber);
    if (bubble) {
        // rectを使用してバブルの位置とサイズを取得
        var rect = bubble.querySelector('button');
        var radiusx = window.getComputedStyle(rect).getPropertyValue('width'); // 半径を計
        var radius = parseFloat(radiusx) / 2;
        var bubbleXx = window.getComputedStyle(rect).getPropertyValue('left');  // スクロールオフセットを加える
        var bubbleX = parseFloat(bubbleXx) + radius;
        var bubbleYx = window.getComputedStyle(rect).getPropertyValue('top');  // スクロールオフセットを加える
        var bubbleY = parseFloat(bubbleYx) + radius;
        var colorx = window.getComputedStyle(rect).getPropertyValue('background-color');
        var color = rgbToHex(colorx);

        bubble.remove();  // バブルを削除

        // バブルが消えた後に小さな円を作成してアニメーションさせる
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
            console.log(color);
            smallCircle.style.left = (bubbleX + xMove - 5) + 'px';
            smallCircle.style.top = (bubbleY + yMove - 5) + 'px';
            bubbleContainer.appendChild(smallCircle);
            smallCircles.push(smallCircle);
        }

        // アニメーション処理
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

// 1つ目のバブルがクリックされたら1秒間隔で順に削除する
function startChainDeletion(startIndex) {
    bubbleIndex = 0;
    deleteNextBubble();
}

// 次のバブルを1秒間隔で削除する
function deleteNextBubble() {
    if (bubbleIndex < numBubbles) {
        deleteBubble(bubbleIndex);
        bubbleIndex++;
        setTimeout(function () {
            deleteNextBubble();  // 次のバブルを1秒後に削除
        }, 500);
    }
}
