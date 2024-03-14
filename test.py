import {expect, test} from "@playwright/test"; // ^1.30.0

const url = "<Your URL>";
const userAgent =
  "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/69.0.3497.100 Safari/537.36";

test.describe("with user agent", () => {
  test.use({userAgent});

  test("is able to retrieve offers", async ({page}) => {
    await page.goto(url);
    const selector = page.locator('[id="Body offers-panel"] li');
    const offers = await selector.count();
    console.log("Num of offers:", offers); // => Num of offers: 11
  });
});