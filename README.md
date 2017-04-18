# kobeengineer Crawler #

記錄用 FB Graph API 爬取**靠北工程師**的貼文讚數、分享數和回應數的過程，以及遇到的一些地雷。

官方並沒有提供 Python 的 SDK，不過直接從 HTTP 取資料還滿簡單，所以這次全用 requests 來抓資料。

> pip install requests

> 註: 其實 Python 其實有個第三方的套件 [facebook-sdk](https://github.com/mobolic/facebook-sdk) 可以用。

## 參考資料 ##
- [Explorer](https://developers.facebook.com/tools/explorer/) 可以用來快速測試 API 。

- [Graph API Document](https://developers.facebook.com/docs/graph-api) 


## 使用 Graph API ##

Facebook 上的資料想成是一個樹狀的節點，以這個例子來說根節點是粉絲頁，可以從這裡開始取得所有粉絲團相關的資料。

    GET /v2.8/{page-id} HTTP/1.1
    Host: graph.facebook.com

用 requests 的話可以這樣做:

    requests.get("https://graph.facebook.com/v2.8/{page-id}/?access_token={token}")

取回來的 JSON 格式資料:

    {
    "name": "靠北工程師",
    "id": "1632027893700148"
    }

- {page-id} 是資料節點的 id (粉絲團、貼文、使用者...)，以靠北工程師粉絲團為例，可以是

>    kobeengine 或
>    1632027893700148

- {tokken} 使用時必須給 [access_token](https://developers.facebook.com/docs/facebook-login/access-tokens) 參數，可以從 [Explorer](https://developers.facebook.com/tools/explorer/) 取得，以這例子來說因為要取得的資料都是公開，不需要另外給其他權限。
不過這邊取得的是短期 token ，大約 1 個多小時後就會失效，要取得更長期限的 token 可以參考 [這篇](https://developers.facebook.com/docs/facebook-login/access-tokens/expiration-and-extension) ，或是直接從 [Access Token Debugger](https://developers.facebook.com/tools/debug/accesstoken/) 這裡點下面的 **Extend Access Token** 拿到更長期限的 token 。

## 取得貼文資料 ##

取得所有的貼文請求可以用 */{page-id}/posts* 。在 Explorer 中會提示目前在查詢的節點類型可以使用的參數。
不管是哪種類型的節點 (貼文、讚、回應...) 或是參數，回應的結構都差不多。

### Pagination ###
- data : 如果請求有成功，回應中一定會有這個 list。
- limit : 一次回傳的資料筆數，最多 100 。 回應資料的數量有可能因為權限問題拿不到而小於這個值，但不代表後面沒有資料了。
- paging : 總共有三種分頁的方法，不過這次程式碼偷懶沒有記游標或時間，所以是判斷 paging 這個參數中有沒有給 next 欄位來決定要不要繼續往下抓。

詳細可以參考 [Pagination](https://developers.facebook.com/docs/graph-api/using-graph-api/#paging) 一節。

另外這次是想找出最熱門貼文，評估的方式是用 likes 、 comments 跟 shares 這三項欄位。 likes 跟 comments 都跟 posts 一樣，超過 limit 的資料數會分頁，可以用下面這樣讓他只回傳點讚或留言的 user id 就好:

    /posts/?fields=likes{id},comments{id}

但是 shares 比較不大一樣，只有 count 可以抓，如果要抓別人轉貼後的內容要用 sharedposts 。後來發現要算讚數跟回覆數除了一筆一筆算以外可以在參數後面加 summary(true)，[Object Comments](https://developers.facebook.com/docs/graph-api/reference/v2.8/object/comments)。

    /posts/?fields=id,comments.summary(true){id},likes.summary(true){id}

- full_picture : 靠北工程師大部分貼文都是圖片，這個參數才會拿到原圖，如果用 picture 只會拿到縮圖。
- message : 拿貼文的文字。

## 結果 ##

- 最多讚:
[https://www.facebook.com/kobeengineer/posts/1844548255781443](https://www.facebook.com/kobeengineer/posts/1844548255781443)
![](https://scontent.xx.fbcdn.net/v/t1.0-9/14718850_1844548255781443_6147732678196358046_n.png?oh=391754e34d6048448bb6e7156f806a46&oe=59232C35)
    - likes: 35048
    - shares: 584
    - comments: 1849

- 最多分享
[https://www.facebook.com/kobeengineer/posts/1735415103361426](https://www.facebook.com/kobeengineer/posts/1735415103361426)
![](https://scontent.xx.fbcdn.net/v/t1.0-9/12799127_1735415103361426_7941877299204214601_n.png?oh=3564b5ddb2f51f9973447f611cda8b38&oe=590A9D6C)
    - likes: 31661
    - shares: 19843
    - comments: 1844

- 最多留言以及總和最高:
[https://www.facebook.com/kobeengineer/posts/1789860681250201](https://www.facebook.com/kobeengineer/posts/1789860681250201)
![](https://scontent.xx.fbcdn.net/v/t1.0-9/13612181_1789860681250201_1216737244862186553_n.png?oh=42e76d0666fce1e65dd50a9783433101&oe=591CEBEF)
    - likes: 31661
    - shares: 19843
    - comments: 1844
