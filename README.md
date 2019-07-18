# PIXIV DOWNLOADER

* 根據指定圖片大量下載相關圖
* 根據排行榜大量下載圖片
* 根據繪師大量下載作品
* 根據關鍵字大量下載圖片
* 檢查相似圖片並分類

---

### 結果圖

![結果圖](https://github.com/sherry110534/pixiv_downloader/blob/master/picture.png)

----

### 說明

* GUI.py: 由tkinter撰寫介面程式
* pixiv_spider.py: 爬蟲程式，一次性下載大量圖片
* find_same.py: 用dHash進行圖片比對，尋找相似圖
  * 縮小圖片尺寸(去除細節，程式中aHash取8x8，dHash取9x8)，轉成灰階圖片(去除色彩)
  * Hash
    * aHash: average hash，簡單速度快但不準確。
      * 計算所有畫素平均值，每個畫素的灰度和平均值比較，大於等於平均值計為1，小於則記為0。
      * 將比較結果組合起來即得64位整數(此圖片指紋)，計算與其他圖片指紋的Hamming distance，距離越小，相似度越大。
      * ![](https://i.imgur.com/XJjIX95.png)
    * dHash: difference hash，精確度高且速度較pHash快。
      * 計算每個畫素之間的差異值，程式中9個畫素取8個差值，共8行，因此有64個差值。
      * 若左邊的畫素比右邊亮，記為1，否則為0，比較完後計算Hamming distance。