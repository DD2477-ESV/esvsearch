from pyppeteer import launch


class Browser:

    def __init__(self) -> None:
        self.browser = None
        self.page = None

    async def start(self):
        self.browser = await launch()
        self.page = await self.browser.newPage()
        return self
