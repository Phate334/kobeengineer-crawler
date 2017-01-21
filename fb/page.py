#!/usr/bin/python
# -*- coding: utf-8 -*-
"""
Facebook Page parser
"""
import json

import requests

class PageParser():
    """ parsing facebook page
    """
    META_TEMPLATE = "https://graph.facebook.com/v2.8/{pid}/?access_token={token}"
    POSTS_TEMPLATE = "https://graph.facebook.com/v2.8/{pid}/posts?access_token={token}\
    &fields=id,message,full_picture,likes.summary(true){{id}},comments.summary(true){{id}}\
    ,shares&limit=100"

    def __init__(self, page_id, token):
        meta = self._getter(self.META_TEMPLATE.format(pid=page_id, token=token))
        if "id" in meta:
            self.set_config(meta["id"], token)
        else:
            print(meta["error"]["message"])
            raise KeyError

    def get_info(self):
        """get page meta.
        """
        return self._getter(self.page_meta_url)

    def get_posts(self):
        """gerenter, find all post id.
        """
        posts = self._getter(self.posts_url)
        if "data" not in posts:
            with open("error.txt", "a", encoding="utf-8") as e:
                e.write(json.dumps(posts, ensure_ascii=False) + "\n\n")

        while posts["data"]:
            for post in posts["data"]:
                if "message" not in post:
                    continue
                yield {
                    "id":post["id"],
                    "likes":post["likes"]["summary"]["total_count"],
                    "comments":post["comments"]["summary"]["total_count"],
                    "shares":post["shares"]["count"] if "shares" in post else 0,
                    "content":post["full_picture"] if "full_picture" in post else post["message"]
                }

            if "next" not in posts["paging"]:
                break

            posts = self._getter(posts["paging"]["next"])

    def _getter(self, url):
        return json.loads(requests.get(url).text)

    def set_config(self, object_id, token):
        self.token = token
        self.page_id = object_id
        self.page_meta_url = self.META_TEMPLATE.format(pid=object_id, token=token)
        self.posts_url = self.POSTS_TEMPLATE.format(pid=object_id, token=token)

