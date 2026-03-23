import { test, expect, type Page } from '@playwright/test';

// Viewports to test
const VIEWPORTS = [
  { name: 'laptop', width: 1280, height: 720 },
  { name: 'desktop', width: 1920, height: 1080 },
  { name: 'mobile', width: 375, height: 812 },
];

/** Navigate to homepage and wait for the asciinema player to fully render. */
async function loadPlayerPage(page: Page) {
  await page.goto('/', { waitUntil: 'networkidle' });

  // Wait for the CDN script to define AsciinemaPlayer
  await page.waitForFunction(() => typeof (window as any).AsciinemaPlayer !== 'undefined', {
    timeout: 20_000,
  });

  // Wait for the player terminal to appear in the DOM
  const term = page.locator('#hero-terminal .ap-term');
  await expect(term).toBeVisible({ timeout: 20_000 });

  return term;
}

for (const vp of VIEWPORTS) {
  test.describe(`Hero screencast @ ${vp.name} (${vp.width}x${vp.height})`, () => {
    test.use({ viewport: { width: vp.width, height: vp.height } });

    test('player renders visible content', async ({ page }) => {
      await loadPlayerPage(page);

      // Wait for text lines to render content (first frame may clear the screen)
      await page.waitForTimeout(3000);

      // At least some lines should have non-whitespace content
      const hasContent = await page.evaluate(() => {
        const lineEls = document.querySelectorAll('.ap-line');
        for (const line of lineEls) {
          const text = (line.textContent ?? '').trim();
          if (text.length > 0) return true;
        }
        return false;
      });
      expect(hasContent).toBe(true);
    });

    test('no horizontal overflow', async ({ page }) => {
      await loadPlayerPage(page);
      await page.waitForTimeout(2000);

      const overflow = await page.evaluate(() => {
        const player = document.querySelector('#hero-terminal .ap-player') as HTMLElement;
        if (!player) return { scrollWidth: 0, clientWidth: 0 };
        return {
          scrollWidth: player.scrollWidth,
          clientWidth: player.clientWidth,
        };
      });

      // scrollWidth should not exceed clientWidth (1px tolerance for rounding)
      expect(overflow.scrollWidth).toBeLessThanOrEqual(overflow.clientWidth + 1);
    });

    test('font size is reasonable', async ({ page }) => {
      const term = await loadPlayerPage(page);

      const fontSize = await term.evaluate((el) =>
        parseFloat(getComputedStyle(el).fontSize)
      );

      // With fit:'width' and many cols, font may be small on mobile, large on desktop
      expect(fontSize).toBeGreaterThanOrEqual(3);
      expect(fontSize).toBeLessThanOrEqual(25);
    });

    if (vp.name !== 'mobile') {
      test('player fills container width', async ({ page }) => {
        await loadPlayerPage(page);

        const widths = await page.evaluate(() => {
          const container = document.querySelector('.hero-screencast') as HTMLElement;
          const parent = container?.parentElement as HTMLElement;
          return {
            containerWidth: container?.getBoundingClientRect().width ?? 0,
            parentWidth: parent?.getBoundingClientRect().width ?? 0,
          };
        });

        // Hero screencast should fill its parent column width
        expect(widths.containerWidth).toBeGreaterThanOrEqual(widths.parentWidth * 0.9);
        // And should be at least 600px on desktop/laptop viewports
        expect(widths.containerWidth).toBeGreaterThanOrEqual(600);
      });

      test('terminal lines do not wrap (line count matches player rows)', async ({ page }) => {
        const term = await loadPlayerPage(page);
        await page.waitForTimeout(2000);

        const data = await term.evaluate((el) => {
          const rows = parseInt(
            getComputedStyle(el).getPropertyValue('--term-rows'),
            10
          );
          const lineCount = el.querySelectorAll('.ap-line').length;
          return { rows, lineCount };
        });

        // If wrapping occurred, there would be MORE lines than the player expects
        expect(data.lineCount).toBeLessThanOrEqual(data.rows + 2);
      });
    }

    test('animation plays (content changes over time)', async ({ page }) => {
      await loadPlayerPage(page);

      // Wait for initial render
      await page.waitForTimeout(2000);

      // Capture content snapshot
      const contentBefore = await page.evaluate(() => {
        const lines = document.querySelectorAll('.ap-line');
        return Array.from(lines).map((l) => l.textContent ?? '').join('\n');
      });

      // Wait for animation to advance
      await page.waitForTimeout(3000);

      const contentAfter = await page.evaluate(() => {
        const lines = document.querySelectorAll('.ap-line');
        return Array.from(lines).map((l) => l.textContent ?? '').join('\n');
      });

      // Content should change as frames advance
      expect(contentAfter).not.toEqual(contentBefore);
    });
  });
}
