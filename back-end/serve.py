# 运行此函数以搭建后端，提供api。
# ==================================
from flask import Flask, jsonify, abort, request, make_response, url_for, redirect, render_template
from flask_httpauth import HTTPBasicAuth
from werkzeug.utils import secure_filename
import os
from predict.predictLabel import predict
from predict.predict_DR_grading import DO_Efficientnet
from flask_cors import CORS

# ==================================

UPLOAD_FOLDER = 'uploads'
ALLOWED_EXTENSIONS = set(['png', 'jpg', 'jpeg'])
app = Flask(__name__, static_folder='static/label', static_url_path="/label")
CORS(app, resources=r'/*')  # 注册CORS, "/*" 允许访问所有api
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
auth = HTTPBasicAuth()

# ================================================#
#                 以下是对API的定义               #
# ================================================#
"""
（待改进）
完成图像上传->预测->保存图片。
流程：
1. 规定api名称，前端调用后，上传图片，图片放到 ./uploads里
2. 然后调用predict函数，从/uploads里读取图片，预测，然后把结果图片保存到./static/label
3. 然后前端获取文件名，从label/文件名 拿图
"""


@app.route('/imgUpload', methods=['GET', 'POST'])
def upload_img():
    print("image upload")
    if request.method == 'POST' or request.method == 'GET':
        if 'file' not in request.files:  # 如果没有检测到上传了文件
            print('No file part')
            return redirect(request.url)  # 重定向

        file = request.files['file']  # 如果检测到了文件，传给file
        # print(file.filename) 
        if file.filename == '':  # 如果用户没有选择文件，浏览器仍然会提交一个没有filename的part，所以要再判断
            print('No selected file')
            return redirect(request.url)

        if file:  # and allowed_file(file.filename):
            filename = secure_filename(file.filename)  # 提取文件名
            # 把文件存到/upload 因为flask的file是封装好的，不能直接拿
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            fileurl = os.path.join(app.config['UPLOAD_FOLDER'], filename)  # 存文件的地方，即：upload/xxx.jpg
            predict(filename)  # get the label pic and store it in the result folder
            # os.remove(fileurl) 暂时先不删除 测试接口是否正常

            # label=os.path.join(result,filename)

            do_efficientnet = DO_Efficientnet()

            do_efficientnet.get_efficientnet('b3', False, './models/best_model for 20epoch - EfficientNetB3 .pth', 5)
            result = do_efficientnet.predict(filename)

            result.update({'filename': filename})

            print(result)

            return jsonify(result)  # 返回名称便于拿


# ==============================================================================================================================
#                                                                                                                              
#                                           Main function                                                        	            #						     									       
#  				                                                                                                
# ==============================================================================================================================
@app.route("/")
def main():
    return render_template("main.html")


if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=8000)
