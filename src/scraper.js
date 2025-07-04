const puppeteer = require('puppeteer-extra');
const StealthPlugin = require('puppeteer-extra-plugin-stealth');
const fs = require('fs');

const tag = process.argv[2];


if (!tag) {
  console.error('❗ Missing arguments: tag, wsEndpoint required.');
  process.exit(1);
}

const fileName = `.\\data\\temp\\temp_${tag}.json`;

puppeteer.use(StealthPlugin());

(async () => {
  const browser = await puppeteer.launch({
      headless: false,
      args: [
          '--window-size= 1080, 1080',
          '--force-device-scale-factor=1',
          '--disable-notifications',
          '--window-position=-1920,0',
          '--disable-gpu',
          '--disable-dev-shm-usage',
          '--no-sandbox',
          '--disable-extensions',
          '--disable-background-networking',
          '--disable-default-apps',
          '--disable-sync',
          '--disable-translate',
          '--hide-scrollbars',
          '--mute-audio',
          '--no-first-run',
          '--no-default-browser-check',
          '--disable-infobars',
          '--start-minimized'
      ],
  });
  const page = await browser.newPage( {headless : true} );
  await page.setViewport({ width: 1080, height: 5000 });

  const client = await page.target().createCDPSession();
  await client.send('Network.enable');
  await client.send('Network.setCookies', {
    cookies: [
      {
        name: 'ttwid',
        value: '1%7ClWLWpdOn_GJGp8c6jOfw99ekA7pq5WaQW2kMyAqrepc%7C1749739091%7C7113d6f9f7ce894ce13e72c925f7c5b4036dc0f4f02d3d052d6ace341a7b201d',
        domain: '.tiktok.com',
        path: '/',
        expires: Math.floor(new Date('2026-06-06T14:24:23Z').getTime() / 1000),
        httpOnly: true, secure: true, sameSite: 'Lax'
      },
      {
        name: 'tt_csrf_token',
        value: 'qVWO7GQG-swtzEe7uPvA3mVGw1DH6EmHHfFQ',
        domain: '.tiktok.com',
        path: '/',
        expires: Math.floor(new Date('2030-01-01').getTime() / 1000),
        httpOnly: true, secure: true, sameSite: 'Lax'
      },
      {
        name: 'tt_chain_token',
        value: 'IBvoD5qDoKVZlZSn+DuShw==',
        domain: '.tiktok.com',
        path: '/',
        expires: Math.floor(new Date('2025-12-08T14:24:23Z').getTime() / 1000),
        httpOnly: true, secure: true, sameSite: 'Lax'
      }
    ]
  });

  let allData = [];
  let lastResponseTime = Date.now();
  let scrolling = false;

  await page.setRequestInterception(true);
  page.on('request', req => {
    if (['image', 'media', 'font', 'stylesheet'].includes(req.resourceType())) {
      req.abort();
    } else {
      req.continue();
    }
  });

  page.on('response', async (response) => {
    const url = response.url();
    if (url.includes('challenge/item_list') || url.includes('item_list')) {
      lastResponseTime = Date.now();

      if (response.status() !== 200) {
        console.error(`Non-200 status ${response.status()} from ${url}`);
        return;
      }

      const text = await response.text();
      try {
        const json = JSON.parse(text);
        if (json && Array.isArray(json.itemList)) {
          allData.push(...json.itemList);
        }
      } catch (err) {}

      // Scroll *after* processing each API response
      if (scrolling) {
        await new Promise(resolve => setTimeout(resolve, 100)); // Delay before scrolling
        await page.evaluate(() => window.scrollBy(0, window.innerHeight * 2));
      }
    }
  });

  await page.goto(`https://www.tiktok.com/tag/${encodeURIComponent(tag)}`, { waitUntil: 'networkidle2' });
  scrolling = true;
  await new Promise(resolve => setTimeout(resolve, 2500));
  await page.reload({ waitUntil: 'networkidle2' });
  await new Promise(resolve => setTimeout(resolve, 500));
  console.log(`⬇️ Starting scroll for tag #${tag}...`);

  // Watchdog: Stop everything if no responses after 3 seconds
  const watchdog = setInterval(() => {
    if (Date.now() - lastResponseTime > 3000) {
      console.log(`⏱️ No API response for 3s → exiting...`);
      scrolling = false;
      clearInterval(watchdog);

      fs.writeFileSync(fileName, JSON.stringify(allData, null, 2));
      console.log(`✅ Saved ${allData.length} entries to ${fileName}`);

      browser.close();
    }
  }, 500);

})();