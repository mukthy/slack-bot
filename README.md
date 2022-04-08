# slack-bot

It is a SlackAPP which integrates between Slack and Internal AntibotPedia API, NetlocSmith, and other products (ZyteDataAPI, AutomaticExtraction).

It is Flask based web-app.

If you have slack channel access then usage is:

Usage is given below:

`/antibot https://example.com.` <= check for Antibot using Antibotpedia API

`/regioncheck https://example.com.` <= checks for GeoLocked  

`/zytedataapi https://example.com` <= ZyteDataAPI

`/netlock-dc https://example.com` <= Netlocsmith with Slack

`/auto-x-product https://example.com` <= product-extraction

`/auto-x-product-list https://example.com` <= product-list-extraction

`/auto-x-article https://example.com` <= article-extraction

`/auto-x-article-list https://example.com` <= article-list-extraction

`/dataset-project-log org_id dataset_id` <= To get the Auto-Extraction Dataset Project Link.
