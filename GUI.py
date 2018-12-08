from tkinter import *
from tkinter import messagebox
from tkinter.font import Font
import tkinter.filedialog
from  tkinter  import ttk
from PIL import Image, ImageTk 
import os
import datetime
import threading
import pixiv_spider
import find_same

class GUI:
    #initial the GUI
    def __init__(self):
        #initial the class
        self.pixiv = pixiv_spider.pixiv('sherry110534@gmail.com', 's003668110534')
        self.find = find_same.findSame()
        #inital the win
        self.app = tkinter.Tk()
        self.app.title('PIXIV DOWNLOADER')
        self.app.resizable(width = False, height = False)
        self.app.geometry('1000x650')
        self.app.config(background = '#f3ecfd')
        self.app.option_add('*Font', '王漢宗細圓體繁')
        self.app.option_add('*background', '#f3ecfd')
        self.efont = Font(family = '王漢宗細圓體繁', size = 12)

        #variable
        self.path = os.path.join(os.getcwd(), 'download')
        self.size = 'large'
        self.bookmark = 1000
        self.count = 100
        self.mode = 'day'
        yes_time = datetime.date.today() - datetime.timedelta(days = 1)
        self.time = yes_time.strftime('%Y-%m-%d')
        self.type = 'partial_match_for_tags'
        self.sort = 'date_desc'
        self.during = None
        self.key = ''
        self.cpath = os.path.join(os.getcwd(), 'download')
        self.classi = ''

        #title & bg
        bgimg =  self.openImg('./img/title.png', 1000, 160)
        backbround = tkinter.Label(self.app, image = bgimg)
        backbround.bgimg = bgimg
        backbround.pack(side = 'top')

        #frames
        f1 = tkinter.Frame(self.app, width = 800, height = 50)
        f1.pack_propagate(0)
        self.save_path(f1)
        f1.pack()
        f2 = tkinter.Frame(self.app, width = 800, height = 50)
        f2.pack_propagate(0)
        self.select_set(f2)
        f2.pack()
        f3 = tkinter.Frame(self.app, width = 800, height = 350)
        f3.pack_propagate(0)
        self.functions(f3)
        f3.pack()

        self.app.mainloop()

    def save_path(self, frame):
        dimg =  self.openImg('./img/download.png', 32, 32)
        downImg = tkinter.Label(frame, image = dimg)
        downImg.dimg = dimg
        downImg.pack(padx = (15, 0), pady = 5, side = 'left')
        pathText = tkinter.Label(frame)
        pathText['text'] = '下載路徑:'
        pathText.pack(pady = 5, side = 'left')
        self.pathField = tkinter.Entry(frame)
        self.pathField.config(borderwidth = 0, highlightthickness = 0, font = self.efont)
        self.pathField['bg'] = 'white'
        self.pathField['width'] = 55
        self.pathField.pack(padx = 5, pady = 5, ipadx = 0, ipady = 4, side = 'left')
        self.pathField.insert(0, self.path)
        img = self.openImg('./img/folder.png', 26, 26)
        pathBtn = tkinter.Button(frame, image = img)
        pathBtn.img = img
        pathBtn.config(borderwidth = 0, highlightthickness = 0)
        pathBtn.pack(padx = 5, pady = 5, side = 'left')
        pathBtn['command'] = self.selectPath
        
    def select_set(self, frame):
        #select size
        sizeFrame = tkinter.Frame(frame)
        simg =  self.openImg('./img/size-tag.png', 32, 32)
        sizeImg = tkinter.Label(sizeFrame, image = simg)
        sizeImg.simg = simg
        sizeImg.pack(pady = 5, side = 'left')
        sizeText = tkinter.Label(sizeFrame)
        sizeText['text'] = '圖片大小:'
        sizeText.pack(pady = 5, side = 'left')
        self.sizeList = ttk.Combobox(sizeFrame, width = 3, state = 'readonly') 
        self.sizeList['values'] = ('大', '中', '小')
        self.sizeList.current(0)
        self.sizeList.pack(padx = 5, pady = 5, side = 'left')
        sizeFrame.pack(padx = (30, 20), side = 'left')

        #select bookmark
        markFrame = tkinter.Frame(frame)
        mimg =  self.openImg('./img/star.png', 32, 32)
        markImg = tkinter.Label(markFrame, image = mimg)
        markImg.pack(pady = 5, side = 'left')
        markImg.mimg = mimg
        markText = tkinter.Label(markFrame)
        markText['text'] = '收藏數量:'
        markText.pack(pady = 5, side = 'left')
        self.markField = tkinter.Entry(markFrame)
        self.markField.config(borderwidth = 0, highlightthickness = 0, font = self.efont)
        self.markField['bg'] = 'white'
        self.markField['width'] = 6
        self.markField.pack(pady = 5, ipadx = 0, ipady = 4, side = 'left')
        self.markField.insert(0, self.bookmark)
        markText2 = tkinter.Label(markFrame)
        markText2['text'] = '以上'
        markText2.pack(pady = 5, side = 'left')
        markFrame.pack(padx = 20, side = 'left')

        #count
        countFrame = tkinter.Frame(frame)
        cimg =  self.openImg('./img/notes.png', 32, 32)
        countImg = tkinter.Label(countFrame, image = cimg)
        countImg.pack(pady = 5, side = 'left')
        countImg.cimg = cimg
        countText = tkinter.Label(countFrame)
        countText['text'] = '下載數量:'
        countText.pack(pady = 5, side = 'left')
        self.countField = tkinter.Entry(countFrame)
        self.countField.config(borderwidth = 0, highlightthickness = 0, font = self.efont)
        self.countField['bg'] = 'white'
        self.countField['width'] = 6
        self.countField.pack(pady = 5, ipadx = 0, ipady = 4, side = 'left')
        self.countField.insert(0, self.count)
        countText2 = tkinter.Label(countFrame)
        countText2['text'] = '張'
        countText2.pack(pady = 5, side = 'left')
        countFrame.pack(padx = (20, 30), side = 'left')

    def functions(self, frame):
        #relative
        reFrame = tkinter.Frame(frame, width = 800, height = 45)
        reFrame.pack_propagate(0)
        reText = tkinter.Label(reFrame)
        reText['text'] = '下載相關圖片'
        reText.pack(padx = (20, 0), side = 'left')
        rimg =  self.openImg('./img/right-arrow.png', 26, 26)
        reImg = tkinter.Label(reFrame, image = rimg)
        reImg.pack(pady = 5, side = 'left')
        reImg.rimg = rimg
        imgText = tkinter.Label(reFrame)
        imgText['text'] = '圖片 ID:'
        imgText.pack(padx = (40, 5), side = 'left')
        self.imgField = tkinter.Entry(reFrame)
        self.imgField.config(borderwidth = 0, highlightthickness = 0, font = self.efont)
        self.imgField['bg'] = 'white'
        self.imgField['width'] = 35
        self.imgField.pack(pady = 10, ipadx = 0, ipady = 4, side = 'left')
        re_simg = self.openImg('./img/movie-player-play-button.png', 32, 32)
        re_sBtn = tkinter.Button(reFrame, image = re_simg)
        re_sBtn.re_simg = re_simg
        re_sBtn.config(borderwidth = 0, highlightthickness = 0)
        re_sBtn.pack(padx = 30, side = 'right')
        re_sBtn['command'] = lambda:self.thread(self.download_related)
        reFrame.pack(side = 'top', anchor = 'w')
        #Collection
        coFrame = tkinter.Frame(frame, width = 800, height = 45)
        coFrame.pack_propagate(0)
        coText = tkinter.Label(coFrame)
        coText['text'] = '下載作品集  '
        coText.pack(padx = (20, 0), side = 'left')
        cimg =  self.openImg('./img/right-arrow.png', 26, 26)
        coImg = tkinter.Label(coFrame, image = cimg)
        coImg.pack(pady = 5, side = 'left')
        coImg.cimg = cimg
        userText = tkinter.Label(coFrame)
        userText['text'] = '繪者 ID:'
        userText.pack(padx = (40, 5), side = 'left')
        self.userField = tkinter.Entry(coFrame)
        self.userField.config(borderwidth = 0, highlightthickness = 0, font = self.efont)
        self.userField['bg'] = 'white'
        self.userField['width'] = 35
        self.userField.pack(pady = 10, ipadx = 0, ipady = 4, side = 'left')
        co_simg = self.openImg('./img/movie-player-play-button.png', 32, 32)
        co_sBtn = tkinter.Button(coFrame, image = co_simg)
        co_sBtn.re_simg = co_simg
        co_sBtn.config(borderwidth = 0, highlightthickness = 0)
        co_sBtn.pack(padx = 30, side = 'right')
        co_sBtn['command'] = lambda:self.thread(self.download_collection)
        coFrame.pack(side = 'top', anchor = 'w')
        #rank
        raFrame = tkinter.Frame(frame, width = 800, height = 45)
        raFrame.pack_propagate(0)
        raText = tkinter.Label(raFrame)
        raText['text'] = '下載排行榜  '
        raText.pack(padx = (20, 0), side = 'left')
        aimg =  self.openImg('./img/right-arrow.png', 26, 26)
        raImg = tkinter.Label(raFrame, image = aimg)
        raImg.pack(pady = 5, side = 'left')
        raImg.aimg = aimg
        modeText = tkinter.Label(raFrame)
        modeText['text'] = '模式:'
        modeText.pack(padx = (40, 5), side = 'left')
        self.modeList = ttk.Combobox(raFrame, width = 8, state = 'readonly') 
        self.modeList['values'] = ('單日排行', '單周排行', '單月排行', '新人排行', '原創排行', '受男性歡迎', '受女性歡迎')
        self.modeList.current(0)
        self.modeList.pack(padx = (8, 10), pady = 5, side = 'left')
        timeText = tkinter.Label(raFrame)
        timeText['text'] = '時間:'
        timeText.pack(padx = (30, 5), side = 'left')
        self.timeField = tkinter.Entry(raFrame)
        self.timeField.config(borderwidth = 0, highlightthickness = 0, font = self.efont)
        self.timeField['bg'] = 'white'
        self.timeField['width'] = 15
        self.timeField.pack(pady = 10, ipadx = 0, ipady = 4, side = 'left')
        self.timeField.insert(0, self.time) 
        ra_simg = self.openImg('./img/movie-player-play-button.png', 32, 32)
        ra_sBtn = tkinter.Button(raFrame, image = ra_simg)
        ra_sBtn.ra_simg = ra_simg
        ra_sBtn.config(borderwidth = 0, highlightthickness = 0)
        ra_sBtn.pack(padx = 30, side = 'right')
        ra_sBtn['command'] = lambda:self.thread(self.download_rank)
        raFrame.pack(side = 'top', anchor = 'w')
        #search part1
        seFrame1 = tkinter.Frame(frame, width = 800, height = 45)
        seFrame1.pack_propagate(0)
        seText = tkinter.Label(seFrame1)
        seText['text'] = '下載搜尋結果'
        seText.pack(padx = (20, 0), side = 'left')
        simg =  self.openImg('./img/right-arrow.png', 26, 26)
        seImg = tkinter.Label(seFrame1, image = simg)
        seImg.pack(pady = 5, side = 'left')
        seImg.simg = simg
        typeText = tkinter.Label(seFrame1)
        typeText['text'] = '模式:'
        typeText.pack(padx = (10, 5), side = 'left')
        self.typeList = ttk.Combobox(seFrame1, width = 10, state = 'readonly') 
        self.typeList['values'] = ('標籤部分符合', '標籤完全符合', '標題說明文符合')
        self.typeList.current(0)
        self.typeList.pack(padx = (2, 10), pady = 5, side = 'left')
        sortText = tkinter.Label(seFrame1)
        sortText['text'] = '排序:'
        sortText.pack(padx = (5, 5), side = 'left')
        self.sortList = ttk.Combobox(seFrame1, width = 6, state = 'readonly') 
        self.sortList['values'] = ('由新到舊', '由舊到新')
        self.sortList.current(0)
        self.sortList.pack(padx = (2, 10), pady = 5, side = 'left')
        durText = tkinter.Label(seFrame1)
        durText['text'] = '時間:'
        durText.pack(padx = (5, 5), side = 'left')
        self.durList = ttk.Combobox(seFrame1, width = 5, state = 'readonly') 
        self.durList['values'] = ('不限制', '一天', '一周', '一個月')
        self.durList.current(0)
        self.durList.pack(padx = (2, 10), pady = 5, side = 'left')
        seFrame1.pack(side = 'top', anchor = 'w')
        #search part2
        seFrame2 = tkinter.Frame(frame, width = 800, height = 45)
        seFrame2.pack_propagate(0)
        keyText = tkinter.Label(seFrame2)
        keyText['text'] = '關鍵字:'
        keyText.pack(padx = (200, 5), side = 'left')
        self.keyField = tkinter.Entry(seFrame2)
        self.keyField.config(borderwidth = 0, highlightthickness = 0, font = self.efont)
        self.keyField['bg'] = 'white'
        self.keyField['width'] = 35
        self.keyField.pack(pady = 10, ipadx = 0, ipady = 4, side = 'left')
        se_simg = self.openImg('./img/movie-player-play-button.png', 32, 32)
        se_sBtn = tkinter.Button(seFrame2, image = se_simg)
        se_sBtn.se_simg = se_simg
        se_sBtn.config(borderwidth = 0, highlightthickness = 0)
        se_sBtn.pack(padx = 30, side = 'right')
        se_sBtn['command'] = lambda:self.thread(self.download_search)
        seFrame2.pack(side = 'top', anchor = 'w')
        #find same part1
        fiFrame1 = tkinter.Frame(frame, width = 800, height = 45)
        fiFrame1.pack_propagate(0)
        fimg =  self.openImg('./img/search.png', 32, 32)
        finImg = tkinter.Label(fiFrame1, image = fimg)
        finImg.fimg = fimg
        finImg.pack(padx = (15, 0), pady = 5, side = 'left')
        cpathText = tkinter.Label(fiFrame1)
        cpathText['text'] = '搜尋路徑:'
        cpathText.pack(side = 'left')
        self.cpathField = tkinter.Entry(fiFrame1)
        self.cpathField.config(borderwidth = 0, highlightthickness = 0, font = self.efont)
        self.cpathField['bg'] = 'white'
        self.cpathField['width'] = 55
        self.cpathField.pack(padx = 5, pady = 5, ipadx = 0, ipady = 4, side = 'left')
        self.cpathField.insert(0, self.cpath)
        cpimg = self.openImg('./img/folder.png', 26, 26)
        cpathBtn = tkinter.Button(fiFrame1, image = cpimg)
        cpathBtn.cpimg = cpimg
        cpathBtn.config(borderwidth = 0, highlightthickness = 0)
        cpathBtn.pack(padx = 5, side = 'left')
        cpathBtn['command'] = self.selectCpath
        fiFrame1.pack(side = 'top', anchor = 'w')
        #find same part2
        fiFrame2 = tkinter.Frame(frame, width = 800, height = 45)
        fiFrame2.pack_propagate(0)
        fiText = tkinter.Label(fiFrame2)
        fiText['text'] = '檢查重複圖片'
        fiText.pack(padx = (20, 0), side = 'left')
        iimg =  self.openImg('./img/right-arrow.png', 26, 26)
        fiImg = tkinter.Label(fiFrame2, image = iimg)
        fiImg.pack(pady = 5, side = 'left')
        fiImg.iimg = iimg
        fmodeText = tkinter.Label(fiFrame2)
        fmodeText['text'] = '模式:'
        fmodeText.pack(padx = (10, 5), side = 'left')
        self.fmodeList = ttk.Combobox(fiFrame2, width = 10, state = 'readonly') 
        self.fmodeList['values'] = ('分類至資料夾', '輸出成文字檔案')
        self.fmodeList.current(0)
        self.fmodeList.pack(padx = (8, 10), pady = 5, side = 'left')
        fiFrame2.pack(side = 'top', anchor = 'w')
        fi_simg = self.openImg('./img/movie-player-play-button.png', 32, 32)
        fi_sBtn = tkinter.Button(fiFrame2, image = fi_simg)
        fi_sBtn.fi_simg = fi_simg
        fi_sBtn.config(borderwidth = 0, highlightthickness = 0)
        fi_sBtn.pack(padx = 30, side = 'right')
        fi_sBtn['command'] = lambda:self.thread(self.find_same_img)

    def selectPath(self):
        filename = tkinter.filedialog.askdirectory()
        if filename != '':
            self.pathField.delete(0, END) 
            self.pathField.insert(0, filename)
        else:
            print('None')

    def selectCpath(self):
        filename = tkinter.filedialog.askdirectory()
        if filename != '':
            self.cpathField.delete(0, END) 
            self.cpathField.insert(0, filename)
        else:
            print('None')

    def download_related(self):
        self.app.config(cursor = 'watch')
        self.setData()
        num = self.pixiv.download_picture_related(self.path, self.size, self.imgField.get(), self.bookmark, self.count)
        if num == None:
            messagebox.showerror("錯誤", "下載出錯了！")
        else:
            messagebox.showinfo('下載完畢', '共下載' + str(num) + '張')
        self.app.config(cursor = '')

    def download_collection(self):
        self.app.config(cursor = 'watch')
        self.setData()
        num = self.pixiv.download_user_picture(self.path, self.size, self.userField.get())
        if num == None:
            messagebox.showerror("錯誤", "下載出錯了！")
        else:
            messagebox.showinfo('下載完畢', '共下載' + str(num) + '張')
        self.app.config(cursor = '')
    
    def download_rank(self):
        self.app.config(cursor = 'watch')
        self.setData()
        num = self.pixiv.download_by_rank(self.path, self.size, self.select_mode(), self.timeField.get(), self.bookmark, self.count)
        if num == None:
            messagebox.showerror("錯誤", "下載出錯了！")
        else:
            messagebox.showinfo('下載完畢', '共下載' + str(num) + '張')
        self.app.config(cursor = '')

    def download_search(self):
        self.app.config(cursor = 'watch')
        self.setData()
        num = self.pixiv.download_by_search(self.path, self.size, self.bookmark, self.count, self.keyField.get(), self.select_type(), self.select_sort(), self.select_duration())
        if num == None:
            messagebox.showerror("錯誤", "下載出錯了！")
        else:
            messagebox.showinfo('下載完畢', '共下載' + str(num) + '張')
        self.app.config(cursor = '')

    def find_same_img(self):
        self.app.config(cursor = 'watch')
        self.cpath = self.cpathField.get()
        self.classi = self.select_fmode()
        sameList = self.find.find_in_file(self.cpath, 20)
        num = 0
        if self.classi:
            #into .txt
            num = self.find.write_into_file(self.cpath, sameList)
        else:
            #into file
            num = self.find.classification(self.cpath, sameList)
        if num == None:
            messagebox.showerror("錯誤", "比對出錯了！")
        elif num == 0:
            messagebox.showinfo('比對完畢', '找不到相同圖片')
        else:
            messagebox.showinfo('比對完畢', '請打開資料夾查看')
        self.app.config(cursor = '')


    def openImg(self, imagePath, w_box, h_box):
        def resize( w, h, w_box, h_box, pil_image):
            f1 = 1.0 * w_box / w    
            f2 = 1.0 * h_box / h    
            factor = min([f1, f2])       
            # use best down-sizing filter    
            width = int(w * factor)    
            height = int(h*factor)    
            return pil_image.resize((width, height), Image.ANTIALIAS) 

        pil_image = Image.open(imagePath)
        w, h = pil_image.size
        pil_image_resize = resize(w, h, w_box, h_box, pil_image)
        tk_image = ImageTk.PhotoImage(pil_image_resize)
        return tk_image

    def setData(self):
        self.path = self.pathField.get()
        self.size = self.select_size()
        self.count = int(self.countField.get())
    
    def select_size(self):
        if self.sizeList.get() == '大':
            return 'large'
        elif self.sizeList.get() == '中':
            return 'medium'
        elif self.sizeList.get() == '小':
            return 'square_medium'

    def select_mode(self):
        if self.modeList.get() == '單日排行':
            return 'day'
        elif self.modeList.get() == '單周排行':
            return 'week'
        elif self.modeList.get() == '單月排行':
            return 'month'
        elif self.modeList.get() == '受男性歡迎':
            return 'day_male'
        elif self.modeList.get() == '受女性歡迎':
            return 'day_female'
        elif self.modeList.get() == '原創排行':
            return 'week_original'
        elif self.modeList.get() == '新人排行':
            return 'week_rookie'

    def select_type(self):
        if self.typeList.get() == '標籤部分符合':
            return 'partial_match_for_tags'
        elif self.typeList.get() == '標籤完全符合':
            return 'exact_match_for_tags'
        elif self.typeList.get() == '標題說明文符合':
            return 'title_and_caption'

    def select_sort(self):
        if self.typeList.get() == '由新到舊':
            return 'date_desc'
        elif self.typeList.get() == '由舊到新':
            return 'date_asc'   

    def select_duration(self):
        if self.typeList.get() == '不限制':
            return None
        elif self.typeList.get() == '一天':
            return 'within_last_day'
        elif self.typeList.get() == '一周':
            return 'within_last_week'
        elif self.typeList.get() == '一個月':
            return 'within_last_month'   

    def select_fmode(self):
        if self.fmodeList.get() == '分類至資料夾':
            return 0
        elif self.fmodeList.get() == '輸出成文字檔案':
            return 1

    def thread(self, func, *args):
        t = threading.Thread(target = func, args = args)
        t.setDaemon(True)
        t.start() 


GUI = GUI()



