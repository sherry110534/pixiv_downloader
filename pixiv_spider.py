from pixivpy3 import *
import os
from PIL import Image

class pixiv():
    def __init__(self, username, password):
        self.username = username
        self.password = password
        self.aapi = AppPixivAPI()
        self.aapi.login(self.username, self.password)
    
    #download the related recommended picture
    def download_picture_related(self, path, size, pid, bookmarks, count):
        try:
            if not os.path.exists(path):
                os.makedirs(path)
            json_result = self.aapi.illust_related(pid)
            num = 0
            while True:
                #check the number of picture
                if num >= count:
                    break  
                for illust in json_result.illusts:
                    if illust.total_bookmarks >= bookmarks and num < count:
                        num += 1
                        print(illust.title)
                        self.aapi.download(illust.image_urls[size], path = path, name = str(illust.id) + '.jpg')
                #whether there is next page ot not
                if json_result.next_url == None:
                    break
                else:
                    next_qs = self.aapi.parse_qs(json_result.next_url)
                    json_result = self.aapi.illust_related(**next_qs)
            return num
        except Exception as e:
            print(e)

    #download the picture of the user
    def download_user_picture(self, path, size, uid):
        try:
            if not os.path.exists(path):
                os.makedirs(path)
            json_result = self.aapi.user_illusts(uid)
            num = 0
            while True:
                #check the number of picture  
                for illust in json_result.illusts:
                    num += 1
                    print(illust.title)
                    self.aapi.download(illust.image_urls[size], path = path, name = str(illust.id) + '.jpg')
                #whether there is next page ot not
                if json_result.next_url == None:
                    break
                else:
                    next_qs = self.aapi.parse_qs(json_result.next_url)
                    json_result = self.aapi.user_illusts(**next_qs)
            return num
        except Exception as e:
            print(e)

    #download by the rank
    def download_by_rank(self, path, size, mode, date, bookmarks, count):
        try:
            if not os.path.exists(path):
                os.makedirs(path)
            json_result = self.aapi.illust_ranking(mode, date = date)
            num = 0
            while True:
                #check the number of picture
                if num >= count:
                    break  
                for illust in json_result.illusts:
                    if illust.total_bookmarks >= bookmarks and num < count:
                        num += 1
                        print(illust.title)
                        self.aapi.download(illust.image_urls[size], path = path, name = str(illust.id) + '.jpg')
                #whether there is next page ot not
                if json_result.next_url == None:
                    break
                else:
                    next_qs = self.aapi.parse_qs(json_result.next_url)
                    json_result = self.aapi.illust_ranking(**next_qs)
            return num
        except Exception as e:
            print(e)

    #download by search 
    def download_by_search(self, path, size, bookmarks, count, keyword, target, sort, duration):
        try:
            if not os.path.exists(path):
                os.makedirs(path)
            json_result = self.aapi.search_illust(keyword, search_target = target, sort = sort, duration = duration)
            num = 0
            while True:
                #check the number of picture
                if num >= count:
                    break  
                for illust in json_result.illusts:
                    if illust.total_bookmarks >= bookmarks and num < count:
                        num += 1
                        print(illust.title)
                        self.aapi.download(illust.image_urls[size], path = path, name = str(illust.id) + '.jpg')
                #whether there is next page ot not
                if json_result.next_url == None:
                    break
                else:
                    next_qs = self.aapi.parse_qs(json_result.next_url)
                    json_result = self.aapi.search_illust(**next_qs)
            return num
        except Exception as e:
            print(e)

        

if __name__ == '__main__':
    pixiv = pixiv('yourname', 'yourpassword')
    path = os.path.join(os.getcwd(), 'download')
    bookmarks = 10000
    count = 20
    pictureId = 69067313
    userId = 27087
    #large medium square_medium
    size = 'large'
    # mode: [day, week, month, day_male, day_female, week_original, week_rookie, day_manga]
    # date: '2018-06-18'
    # mode(r18): [day_r18, day_male_r18, day_female_r18, week_r18, week_r18g]
    mode = 'week'
    date = None  
    # search_target - 搜索類型
    #   partial_match_for_tags  - 標籤部分一致
    #   exact_match_for_tags    - 標籤完全一致
    #   title_and_caption       - 和標題說明文一致
    # sort: [date_desc, date_asc]
    # duration: [within_last_day, within_last_week, within_last_month]
    search_target = 'partial_match_for_tags'
    sort = 'date_desc'
    duration = None
    keyword = '花'
    
    num = pixiv.download_picture_related(path, size, pictureId, bookmarks, count)
    #pixiv.download_user_picture(path, size, userId)
    #pixiv.download_by_rank(path, size, mode, date, bookmarks, count)
    #pixiv.download_by_search(path, size, bookmarks, count, keyword, search_target, sort, duration)
    print(num)
    
    
        
    

