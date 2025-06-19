import os


def write_UI_burst(num_bubbles, radii, x, y, name, mean, example, color):
    # CSSとJavaScriptファイルの絶対パスを取得
    css_path = os.path.join(os.path.dirname(__file__), "bubble_burst_styles.css")
    js_path = os.path.join(os.path.dirname(__file__), "bubble_burst_script.js")

    # 外部CSSとJavaScriptファイルを読み込む
    with open(css_path, "r") as css_file:
        css_content = css_file.read()
    with open(js_path, "r") as js_file:
        js_script = js_file.read()

    button_html = f"""
    <style>
    {css_content}
    </style>
    <div class="bubble-container">
    """
    for i in range(num_bubbles):
        button_html += f'''
            <div id="bubble-{i}" style="position:absolute; width: {radii[i] * 2}px; height: {radii[i] * 2}px; text-align:center;">
                <button style="width: {radii[i] * 2}px; height: {radii[i] * 2}px; font-size: {10+radii[i]/5}px; top:{y[i]-radii[i]+100}px; left:{x[i]-radii[i]}px; background-color: {color[i]};"
                        onclick="startChainDeletion({i})">{name[i]}</button>
            </div>
        '''
    button_html += f"""
    </div>

    <script>
    let numBubbles = {num_bubbles};
    {js_script}
    </script>
    """
    return button_html


def write_UI_visualize(num_bubbles, radii, x, y, name, mean, example, colors, count):
    # CSSとJavaScriptファイルの絶対パスを取得
    css_path = os.path.join(os.path.dirname(__file__), "bubble_styles.css")
    js_path = os.path.join(os.path.dirname(__file__), "bubble_scripts.js")

    # 外部CSSとJavaScriptファイルを読み込む
    with open(css_path, "r") as css_file:
        css_content = css_file.read()
    with open(js_path, "r") as js_file:
        js_content = js_file.read()

    button_html = f"""
    <style>
    {css_content}
    </style>
    <div class="bubble-container">
    """
    for i in range(num_bubbles):
        button_html += '''
        <button style="width: {0}px; height: {0}px; font-size: {7}px; top: {1}px; left: {2}px; background-color: {6};"
                onclick="showOverlay('{3}', '{4}', '{5}', '{8}')">
                {3}
        </button>'''.format(radii[i] * 2, y[i], x[i], name[i], mean[i], example[i], colors[i], 10 + radii[i] / 5, count[i])
    button_html += f"""
    </div>
    <div id="overlay" class="overlay">
        <div class="overlay-content">
            <button class="close-button" onclick="closeOverlay()">×</button>
            <h3 id="overlay-title">Overlay</h3>
            <p id="overlay-message"></p>
        </div>
    </div>
    <script>
    {js_content}
    </script>
    """
    return button_html


def write_paper_UI_visualize(num_bubbles, radii, x, y, name, mean, colors, count):
    # CSSとJavaScriptファイルの絶対パスを取得
    css_path = os.path.join(os.path.dirname(__file__), "bubble_styles.css")
    js_path = os.path.join(os.path.dirname(__file__), "bubble_scripts.js")

    # 外部CSSとJavaScriptファイルを読み込む
    with open(css_path, "r") as css_file:
        css_content = css_file.read()
    with open(js_path, "r") as js_file:
        js_content = js_file.read()

    button_html = f"""
    <style>
    {css_content}
    </style>
    <div class="bubble-container">
    """
    for i in range(num_bubbles):
        button_html += '''
        <button style="width: {0}px; height: {0}px; font-size: {6}px; top: {1}px; left: {2}px; background-color: {5};"
                onclick="showOverlay('{3}', '{4}', '{7}')">
                {3}
        </button>'''.format(radii[i] * 2, y[i]-radii[i]+100, x[i]-radii[i], name[i], mean[i], colors[i], 10+radii[i]/5, count[i])
    button_html += f"""
    </div>
    <div id="overlay" class="overlay">
        <div class="overlay-content">
            <button class="close-button" onclick="closeOverlay()">×</button>
            <h3 id="overlay-title">Overlay</h3>
            <p id="overlay-message"></p>
        </div>
    </div>
    <script>
    {js_content}
    </script>
    """
    return button_html
