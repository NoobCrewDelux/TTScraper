# TTScraper

## Description:

The purpose of this project is purely as a passion project for educational endeavour. It is to educate myself on the use of Node.js with Python and how web scrapers utilise the two languages to handle extremely large sets of raw JSON data in the gigabytes. By creating it I proved to myself the sheer amount of data that can be collected within mere hours. ~ 13 hrs = 1.2 GB = 1 million videos = ~ 6.3k TikTok hashtags.

This is a very crude and poorly optimised program, but I have proven to myself the effectiveness of these programs in a modern society and how profitable they can be. The profit for a simple setup like mine can range anywhere from hundreds of dollars to tens of thousands of dollars. These profits purely depend on the effort put into the data monetisation and post-processing done by the developer. Most marketers and data analysts are usually more interested in monetised *legal* documents of data rather than the raw JSON pulled directly from API response payloads.

Because of the nature of the data collection process, it is very grey in terms of the legality of the setup. In the case where one were to effectively bypass a TikTok-triggered captcha, in the sense that a human wasn't solving them, then one would be severely breaching TikTok's T&Cs. It is for this reason one must avoid the conditions where TikTok triggers a captcha, essentially spawning a chromium process with minimal red flags attached. For this reason I used Puppeteer.

I was initially using Playwright to conduct Chromium instance spawning; however, my Playwright instances had enough "missing details" in them for TikTok's captcha conditions to be met. This required periodic human intervention to solve the captcha and give limited immunity. This periodic cycle had an interval of ~10-15 minutes. It may also help to prevent captcha by blocking all other network traffic other than XHR / FETCH packets of data. This helps speed up network transfers, and reduces rendering requirements which leads to less ram and cpu usage overall. It is also required that separate Chromium instances be spawned as the quantity of videso loaded in a websocketed tab setup is far less than single instances. I believe  this is because TikTok.com is able to detect multiple tabs of TikTok.com open in the same browser and therefore cause the API to limit the amount of data sent.

Lastly, my program uses hashtags to collate data as it is proven to be the most efficient in terms of loading a high quantity of video data vs time. For the first ~1200 tags I had prompted ChatGPT to give me 1000 popular TikTok tags to which it gave ~1200. These were high quality tags that proved a 95.7% hit rate ( yielding greater than 0 videos ) with a 5% miss rate ( yielding 0 videos). Any other tags that I wanted to use were to be generated from the NLTK module in python. Simply write a script to dump x amount of words under x letters and put them into the tags file. These tags were surprisingly comparitable with the AI prompted tags, with a 90.4% hit rate and a 9.6% miss rate. These statistics are ofcourse subject to change as the content on the platform changes. However it is a baseline for when this program was created. It should be noted the scope of the data is across 6k+ tiktok tags. I have not yet analysed the data of my program's latest version but I assume it to be similarily ranked even thought it is across 35000+ tags.

It is not my within my intentions to sell personal data of any kind to a marketplace. It is not my responsibility what others do with this source code as it is a widely known method of scraping data among internet users. What I have created is a crude and rudimentary program collecting nothing but public api calls with cookies from a session with no account. I am deleting this data from my computer system after analysing it on my computer system. It is not being uploaded to the internet in any form.

## Data points collected:

| **JSON Path**    | **Key**          | **Python Type**   |
| ------------------------------ | ---------------------- | ---------------- |
| `tag`                        | `tag`                | `string`       |
| `id`                         | `video_id`           | `string`       |
| `createTime`                 | `created_at`         | `int (UNIX)`   |
| `desc`                       | `description`        | `string`       |
| `textExtra[].hashtagName`    | `hashtags[]`         | `list[string]` |
| `author.id`                  | `author_id`          | `string`       |
| `author.secUid`              | `author_secuid`      | `string`       |
| `author.uniqueId`            | `author_unique`      | `string`       |
| `author.nickname`            | `author_name`        | `string`       |
| `author.verified`            | `author_verified`    | `bool`         |
| `author.signature`           | `author_bio`         | `string`       |
| `authorStats.followerCount`  | `author_followers`   | `int`          |
| `authorStats.followingCount` | `author_following`   | `int`          |
| `authorStats.heartCount`     | `author_likes`       | `int`          |
| `authorStats.videoCount`     | `author_video_count` | `int`          |
| `stats.playCount`            | `video_plays`        | `int`          |
| `stats.diggCount`            | `video_likes`        | `int`          |
| `stats.commentCount`         | `video_comments`     | `int`          |
| `stats.shareCount`           | `video_shares`       | `int`          |
| `stats.collectCount`         | `video_favorites`    | `int`          |
| `music.id`                   | `music_id`           | `string`       |
| `music.title`                | `music_title`        | `string`       |
| `music.authorName`           | `music_author`       | `string`       |
| `duetEnabled`                | `duet_enabled`       | `bool`         |
| `stitchEnabled`              | `stitch_enabled`     | `bool`         |
