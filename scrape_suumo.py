import os
import sys
import csv
import time
import requests
import chromedriver_binary

from selenium import webdriver
from selenium.webdriver.chrome.options import Options

url = sys.argv[1]

options = Options()
options.add_argument('--window-size=1280,3000')
options.add_argument('--headless')
driver = webdriver.Chrome(options=options)

driver.get(url)
time.sleep(5)


def w_febcn(clname):
    try:
        e = driver.find_element_by_class_name(clname).text
    except:
        e = ''
    return e


def w_febx(xpath):
    try:
        e = driver.find_element_by_xpath(xpath).text
    except:
        e = ''
    return e


# GET DATA
name = w_febcn('page-title__text').replace('/', ' ')
chinryo = w_febcn('getsugaku')
kanrihi = w_febcn('kanrihi')
shikikin = w_febcn('shikikinHoshokinDisp')
reikin = w_febcn('reikinShikibikiDisp')
madori = w_febcn('madori')
menseki = w_febcn('menseki')
shubetsu = w_febcn('tatemonoShuDisp')
kozo = w_febcn('kozoDisp')
chikunen = w_febcn('chikugonenDisp')
kaidate = w_febcn('kaidateDisp')
houi = w_febcn('houi')

joken = w_febx('//*[text()="入居条件"]/following-sibling::*')
bath = w_febx('//*[text()="バス・トイレ"]/following-sibling::*')
kitchen = w_febx('//*[text()="キッチン"]/following-sibling::*')
security = w_febx('//*[text()="セキュリティ"]/following-sibling::*')
setsubi = w_febx('//*[text()="室内設備"]/following-sibling::*')
tokucho = w_febx('//*[text()="部屋の特徴"]/following-sibling::*')
kyoyo = w_febx('//*[text()="共用部"]/following-sibling::*')
gihokozo = w_febx('//*[text()="構造・工法"]/following-sibling::*')
other = w_febx('//*[text()="その他の特徴"]/following-sibling::*')

data = [
    url,
    name,
    chinryo,
    kanrihi,
    shikikin,
    reikin,
    madori,
    menseki,
    shubetsu,
    kozo,
    chikunen,
    kaidate,
    houi,
    joken,
    bath,
    kitchen,
    security,
    setsubi,
    tokucho,
    kyoyo,
    gihokozo,
    other
]

if not os.path.exists('suumo_data.csv'):
    col_name = [
        'URL',
        '物件名',
        '賃料',
        '管理費・共益費',
        '敷金（保証金）',
        '礼金（敷引・償却金）',
        '間取り',
        '専有面積',
        '種別',
        '構造',
        '築年',
        '階建',
        '向き',
        '入居条件',
        'バス・トイレ',
        'キッチン',
        'セキュリティ',
        '室内設備',
        '部屋の特徴',
        '共用部',
        '構造・工法',
        'その他の特徴'
    ]
    with open('suumo_data.csv', 'w') as f:
        writer = csv.writer(f, lineterminator='\n')
        writer.writerow(col_name)

with open('suumo_data.csv', 'a') as f:
    writer = csv.writer(f, lineterminator='\n')
    writer.writerow(data)

# GET IMAGES
img_dir = 'img/%s' % name
os.makedirs(img_dir, exist_ok=True)
driver.save_screenshot('%s/screenshot.png' % img_dir)
imgs = driver.find_elements_by_xpath('//section[@class="carouselLstWrap"]//img')
img_id = 1
for img in imgs:
    img_bin = requests.get(img.get_attribute('data-src')).content
    img_name = '%s/photo_%s.png' % (img_dir, img_id)
    with open(img_name, mode='wb') as f:
        f.write(img_bin)
    img_id += 1

driver.close()
print('DONE!!')
