=====
Usage
=====

To use kcrw.apple_news in a project::

    from kcrw.apple_news import API

    api = API('MY_KEY', 'MY_SECRET', 'MY_CHANNEL_ID')
    channel_data = api.channel()
    new_article = api.create_article(article_data, metadata, {'asset1.jpg: ...})
    updated_article = api.update_article(
        'ARTICLE_ID', metadata, article_data, {'updated_asset.jpg': ...}
    )
    article = api.read('ARTICLE_ID')
    api.delete('ARTICLE_ID')


You can also use the included command line tool:

    $ apple_news_api channel
    $ apple_news_api create path/to/folder
    $ apple_news_api updated ARTICLE_ID path/to_folder
    $ apple_news_api read ARTICLE_ID
    $ apple_news_api delete ARTICLE_ID
