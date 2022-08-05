# slack-bot

It is a SlackAPP which integrates between Slack and Internal AntibotPedia API, NetlocSmith, and other products (ZyteDataAPI, AutomaticExtraction).

It is Flask based web-app.

If you have slack channel access then usage is:

Usage is given below:

`/zytebot-antibot https://example.com.` <= check for Antibot using Antibotpedia API

`/zytebot-regioncheck https://example.com.` <= checks for GeoLocked  

`/zytebot-zytedataapi https://example.com` <= ZyteDataAPI

`/zytebot-netlock-dc https://example.com` <= Netlocsmith with Slack

`/zytebot-auto-x-product https://example.com` <= product-extraction

`/zytebot-auto-x-product-list https://example.com` <= product-list-extraction

`/zytebot-auto-x-article https://example.com` <= article-extraction

`/zytebot-auto-x-article-list https://example.com` <= article-list-extraction

`/zytebot-dataset-project-log org_id dataset_id` <= To get the Auto-Extraction Dataset Project Link.

`/zytebot-fetchapiscreenshot https://google.com` <= To get the FullPage Screenshot using FetchAPI (Uses different BrowserStack).

`/zytebot-netloc-config google.com` <= To get the Default/Global Netloc-Config from CCM to Slack.

`/zytebot-uncork-config google.com` <= To get the Default/Global Uncork-Config from CCM to Slack.

`/zytebot-playwright google.com` <= To get a screenshot of domain using playwright.

`/zytebot-puppeteer google.com` <= To get a screenshot of domain using puppeteer.

`/zytebot-zytedataapi-screenshot https://example.com` <= ZyteDataAPI Screenshot API

`/zytebot-curlconvertor curl -U APIKEY: -x proxy.crawlera.com:8010 ‘https://www.amazon.in/Pure-Source-India-Reed-Sticks/dp/B079KCG68Y/'` <= ZyteDataAPI Screenshot API

`/zytebot-antibot-bulk https://www.usphonebook.com/, menards.com, https://allegro.pl/, https://google.com, petflow` <= Performs Bulk AntiBot Scan. Make sure there is a coma and space between domains. 