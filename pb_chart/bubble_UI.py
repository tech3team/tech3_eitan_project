import numpy as np
import pandas as pd

def write_UI(num_bubbles, radii, x, y, name, mean, example):
    button_html = """
    <style>
    .bubble-container {
        position: relative;
        width: 600px;
        height: 600px;
        margin: 0 auto;
    }

    .bubble-container button {
        position: absolute;
        border-radius: 50%;
        background-color: #FF5722;
        color: white;
        border: none;
        cursor: pointer;
        font-size: 10px;
    }

    /* オーバーレイスタイル */
    .overlay {
        display: none;
        position: fixed;
        top: 0;
        left: 0;
        width: 100%;
        height: 100%;
        background-color: rgba(0, 0, 0, 0.5);
        justify-content: center;
        align-items: center;
        z-index: 1000;
    }

    .overlay.active {
        display: flex;
    }

    .overlay-content {
        background-color: white;
        padding: 20px;
        border-radius: 10px;
        text-align: center;
        position: relative;
        width: 300px;
    }

    /* バツボタンのスタイル */
    .close-button {
        position: absolute;
        top: 10px;
        right: 10px;
        cursor: pointer;
        font-size: 18px;
        background: none;
        border: none;
    }
    </style>

    <div class="bubble-container">
    """

    # for i in range(num_bubbles):
    #     # ボタンの位置とサイズを計算してHTML生成
    #     button_html += f'<button style="width: {radii[i]*2}px; height: {radii[i]*2}px; top: {y[i]-radii[i]+100}px; left: {x[i]-radii[i]}px;">{name[i]}</button>'
    for i in range(num_bubbles):

        button_html += '<button style="width: {0}px; height: {0}px; top: {1}px; left: {2}px;" ' \
                    'onclick="showOverlay(\'{3}\', \'{4}\', \'{5}\')">' \
                    '{3}</button>'.format(radii[i] * 2, y[i]-radii[i]+100, x[i]-radii[i], name[i], mean[i], example[i])

    button_html += """
    </div>

    <!-- オーバーレイのHTML -->
    <div id="overlay" class="overlay">
        <div class="overlay-content">
            <button class="close-button" onclick="closeOverlay()">×</button>
            <h3 id="overlay-title">Overlay</h3>
            <p id="overlay-message"></p>
        </div>
    </div>
    """

    # JavaScriptを埋め込む
    button_html += """
    <script>
    function showOverlay(Word, mean, example) {
        var overlay = document.getElementById('overlay');
        var title = document.getElementById('overlay-title');
        var message = document.getElementById('overlay-message');
        title.innerText = Word ;  // ボタン名をオーバーレイのタイトルに設定
        message.innerText = '単語の意味:'+mean+ '\\n 例文:' + example;
        overlay.classList.add('active');
    }

    function closeOverlay() {
        var overlay = document.getElementById('overlay');
        overlay.classList.remove('active');
    }
    </script>
    """

    return button_html