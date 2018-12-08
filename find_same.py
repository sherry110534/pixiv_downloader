import hashlib
import os
from PIL import Image
import shutil

class findSame():
    
    def get_dhash(self, img):
        resize_width = 9
        resize_height = 8
        #resize
        img = img.resize((resize_width, resize_height), Image.ANTIALIAS)
        #grayscale
        img = img.convert('L')
        #compare
        pixels = list(img.getdata())
        difference = []
        for row in range(resize_height):
            row_start_index = row * resize_width
            for col in range(resize_width - 1):
                left_pixel_index = row_start_index + col
                difference.append(1 if pixels[left_pixel_index] > pixels[left_pixel_index + 1] else 0)
        #transfer into hex
        decimal_value = 0
        hash_string = ''
        for index, value in enumerate(difference):
            if value:
                decimal_value += value * (2 ** (index % 8))
            if index % 8 == 7:
                hash_string += str(hex(decimal_value)[2:].rjust(2, '0'))
                decimal_value = 0
        return hash_string

    def get_ahash(self, img):
        img = img.resize((8, 8), Image.ANTIALIAS).convert('L')
        avg = sum(list(img.getdata())) / 64.0
        dis = ''.join(map(lambda i: '0' if i < avg else '1', img.getdata()))
        return ''.join(map(lambda x:'%x' % int(dis[x:x+4], 2), range(0, 64, 4)))

    def count_hamming(self, hash1, hash2):
        difference = (int(hash1, 16)) ^ (int(hash2, 16))
        return bin(difference).count('1')

    def compare(self, img1, img2):
        dH1 = self.get_dhash(img1)
        dH2 = self.get_dhash(img2)
        distance = self.count_hamming(dH1, dH2)
        return distance

    def find_in_file(self, path, value):
        try:
            sameList = dict()
            tree = os.walk(path)
            for dirname, subdir, files in tree:
                allfiles = []
                for f in files:
                    ext = f.split('.')[-1]
                    #get all .png or .jpg files, save in filelist
                    if ext == 'png' or ext == 'jpg':
                        allfiles.append(dirname + '/' + f)
                if len(allfiles) > 0:
                    for i in range(len(allfiles)):
                        num = 0
                        img = Image.open(allfiles[i])
                        dh = self.get_dhash(img)
                        for key in sameList:
                            if self.count_hamming(key, dh) <= value:
                                sameList[key].append((os.path.abspath(allfiles[i]), dh))
                                num += 1    #add in a class
                            else:
                                for f in sameList[key]:
                                    if self.count_hamming(f[1], dh) <= value:
                                        sameList[key].append((os.path.abspath(allfiles[i]), dh))
                                        num += 1
                        if num == 0:
                            sameList[dh] = [(os.path.abspath(allfiles[i]), dh)]
            return sameList
        except Exception as e:
            print(e)
    
    def write_into_file(self, path, sameList):
        with open(os.path.join(path, 'same.txt'), 'w') as f:
            index = 1
            num = 0
            if  not sameList:
                num = 0
            for key, value in sameList.items():
                if len(value) == 1:
                    continue
                else:
                    num += 1
                    f.writelines(str(index) + '. ')
                    same = []
                    for tun in value:
                        same.append(tun[0])
                    f.writelines(','.join(same))
                    f.writelines('\n')
                    index += 1
            return num

    def classification(self, path, sameList):
        try:
            index = 1
            num = 0
            if  not sameList:
                num = 0
            for key, value in sameList.items():
                if len(value) == 1:
                    continue
                else:
                    num += 1
                    while os.path.isdir(os.path.join(path, 'sameImg' + str(index))):
                        index += 1
                    os.mkdir(os.path.join(path, 'sameImg' + str(index)))
                    for tun in value:
                        shutil.move(tun[0], os.path.join(path, 'sameImg' + str(index)))
                    index += 1
            #get all files in this path
            files = os.listdir(path)
            for f in files:
                if os.path.isdir(os.path.join(path, f)):
                    #empty file
                    if len(os.listdir(os.path.join(path, f))) == 0:
                        os.rmdir(os.path.join(path, f))
            return num
        except Exception as e:
            print(e)



                        
                                
        
                        
        
'''
c = findSame()
img1 = Image.open('C:/Users/Jing/Desktop/test/original.jpg')
img2 = Image.open('C:/Users/Jing/Desktop/test/square.jpg')
print(c.compare(img1, img2))
#aaa = c.find_in_file('C:/Users/Jing/Desktop/test', 20)
#c.classification('C:/Users/Jing/Desktop/test', aaa)
'''
        
