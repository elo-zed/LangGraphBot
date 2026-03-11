import random
import time
from playwright.sync_api import sync_playwright


VIDEO_URL = "https://www.youtube.com/watch?v=wWk1kG-8QYY"


def human_delay(a=0.5, b=1.5):
    time.sleep(random.uniform(a, b))


def random_mouse_move(page):
    width = random.randint(200, 800)
    height = random.randint(200, 600)
    page.mouse.move(width, height, steps=random.randint(10, 30))


def random_scroll(page):
    # for _ in range(random.randint(1, 3)):
    page.mouse.wheel(0, random.randint(100, 300))
    human_delay(1, 5)


def open_transcript(page):

    # 等页面加载 如果 30 秒内没有出现：报错
    # timeout=0 才是无限等待。
    # ytd-watch-flexy 是 YouTube 视频页面的根组件
    page.wait_for_selector("ytd-watch-flexy") # 默认 timeout = 30秒
    human_delay(2, 4)

    random_mouse_move(page)
    random_scroll(page)

    # 点击 More actions (三个点)
    # more_btn = page.locator('tp-yt-paper-button#expand')

    # more_btn.wait_for()
    # human_delay(0.5, 1.2)
    # page.locator("#expand").click() YouTube 的按钮 id 其实是 expand
    # more_btn.click() 默认 timeout 也是 30 秒
    # more_btn = page.get_by_role("button", name="更多") # 等价于 <button>更多</button>
    # more_btn.wait_for(state="visible")
    # more_btn.click()

    more_btn = page.get_by_role("button", name="更多")

    for _ in range(10):   # 最多滚动20次
        if more_btn.is_visible():
            break

        page.mouse.wheel(0, random.randint(100, 300))
        time.sleep(random.uniform(0.3, 0.8))

    if more_btn.is_visible():
        more_btn.click()

    human_delay(0.8, 1.8)

    # 点击 Show transcript

    transcript_btn = page.get_by_role("button", name="内容转文字")

    for _ in range(20):   # 最多滚动20次
        if transcript_btn.is_visible():
            break

        page.mouse.wheel(0, random.randint(100, 300))
        time.sleep(random.uniform(0.3, 0.8))

    if transcript_btn.is_visible():
        transcript_btn.click()


    page.wait_for_selector("transcript-segment-view-model")

    segments = page.locator("transcript-segment-view-model")

    count = segments.count()

    results = []

    for i in range(count):
        seg = segments.nth(i)

        time = seg.locator(".ytwTranscriptSegmentViewModelTimestamp").inner_text()
        text = seg.locator("span").inner_text()

        results.append(f"{time} {text}")

    print("\n".join(results))

    human_delay(1, 2)
    return "\n".join(results)


def scroll_transcript(page):

    container = page.locator("ytd-transcript-renderer")

    for _ in range(15):
        container.evaluate("el => el.scrollBy(0, 800)")
        human_delay(0.2, 0.5)



def subtitle_agent(s):

    with sync_playwright() as p:

        # 连接已经启动的 Chrome
        browser = p.chromium.connect_over_cdp("http://localhost:9222")

        context = browser.contexts[0]
        page = context.new_page()

        page.goto(s.URL)

        human_delay(3, 5)

        transcript = open_transcript(page)

        with open("transcript.txt", "w", encoding="utf-8") as f:
            f.write(transcript)

        print("\n字幕已保存到 transcript.txt")


if __name__ == "__main__":
    subtitle_agent()


