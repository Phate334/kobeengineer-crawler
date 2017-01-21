#!/usr/bin/python
# -*- coding: utf-8 -*-
"""
facebook fan page crawler for kobeengineer.
"""
import json

from fb.page import PageParser

ACCESS_TOKEN = "EAADNJGFzmZBIBAPDI2afQ9U9GJVOpQUZCiLrXeRAkRk2ZAP2ZBgFicoJmye5oekFZBrb4gyaVWXyxEZCi0McZAJZCQxnzxy5wfIDzDer1nxvo97xBQQeg0ZCthBZAjI8ExtU6THOvDcxdBUoC2h8jJb5IqG0kOtZAQzMP0ZD"
PAGE_ID = "kobeengineer"

if __name__ == "__main__":
    temp = []
    PP = PageParser(PAGE_ID, ACCESS_TOKEN)
    for p in PP.get_posts():
        temp.append(p)
        c = len(temp)
        if c % 1000 == 0:
            print(c)

    with open('kobeengineer-posts.json', 'w', encoding='utf-8') as f:
        f.write(json.dumps(temp, ensure_ascii=False))
