from flask import (
    Flask, app, json, jsonify,request,Response,make_response
)
from flask_cors import CORS  # 前后端分离跨域
import matplotlib.pyplot as plt
import requests as req
import cv2
import numpy as np
from urllib.request import urlopen


avatarUrl='https://wx.qlogo.cn/mmopen/vi_32/U7OAMHA6apqgylfWpowxWH62aSZGUQTTRpNXnRGRRwtGs25jx1tAURYwDek7SViczicC3eCDqg2bxfhWqQr6PdlA/132'
# response = req.get(avatarUrl)
req = urlopen(avatarUrl)
arr = np.asarray(bytearray(req.read()), dtype=np.uint8)
img = cv2.imdecode(arr, -1) # 'Load it as it is'
cv2.circle(img, (66,66), 66, (0, 0, 255), 2)
cv2.imshow('lalala', img)
cv2.waitKey(0)
cv2.destroyAllWindows()
# array_bytes = img.tobytes()