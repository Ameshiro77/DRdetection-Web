# 运行此函数以搭建后端，提供api。
# ==================================
from flask import Flask, jsonify, abort, request, make_response, url_for, redirect, render_template, Response
from flask_httpauth import HTTPBasicAuth
from flask_cors import *
from werkzeug.utils import secure_filename
import os
import shutil
import numpy as np
from tensorflow.python.platform import gfile
import PIL
# ==================================

UPLOAD_FOLDER = 'uploads'
ALLOWED_EXTENSIONS = set(['png', 'jpg', 'jpeg'])
app = Flask(__name__,
            static_folder="./template",
            template_folder="./template",
            static_url_path="")
CORS(app, supports_credentials=True)  # 跨域
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
auth = HTTPBasicAuth()


#================================================#
#                 以下是对API的定义               #
#================================================#

"""
用于图像输入进模型，返回结果图像
"""


@app.route('/imgUpload', methods=['GET', 'POST'])
def upload_img():
    print("image upload")
    result = 'static/result'  # 结果放到/static/result
    if not gfile.Exists(result):  # 如果没有就开一个新的
        os.mkdir(result)
    shutil.rmtree(result)  # 先删除下面所有文件 也就是过往记录

    if request.method == 'POST' or request.method == 'GET':
        print(request.method)
        if 'file' not in request.files:  # 如果没有检测到上传了文件
            print('No file part')
            return redirect(request.url)  # 重定向

        file = request.files['file']  # 如果检测到了文件，传给file
        print(file.filename)
        if file.filename == '':  # 如果用户没有选择文件，浏览器仍然会提交一个没有filename的part，所以要再判断
            print('No selected file')
            return redirect(request.url)
        if file:
            filename = secure_filename(file.filename)  # 提取文件名
            # 把文件存到/upload 因为flask的file是封装好的，不能直接拿
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            fileurl = os.path.join(
                app.config['UPLOAD_FOLDER'], filename)  # 存的url

            # 需要自定义的函数：
            # 给出上传文件的位置 ， 输入到模型，得到图像列表：第一个是分割结果，第二个是分类结果
            image, classify = getResult(fileurl)
            return jsonify({"image:": image,
                           "classify": classify})


#================================================#
#                 主 函 数 入 口                 #
#================================================#
@app.route("/")
def main():
    return render_template('index.html', name='index')


if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=8080)
