# 运行此函数以搭建后端，提供api。
#==================================
from flask import Flask, jsonify, abort, request, make_response, url_for,redirect, render_template
from flask_httpauth import HTTPBasicAuth
from werkzeug.utils import secure_filename
import os
from predict.predictLabel import predict
from flask_cors import CORS
#==================================

UPLOAD_FOLDER = 'uploads'
UPLOAD_FOLDER = 'static/result'
ALLOWED_EXTENSIONS = set(['png', 'jpg', 'jpeg'])
app = Flask(__name__, static_folder='static/label',static_url_path = "/label")
CORS(app, resources=r'/*')	# 注册CORS, "/*" 允许访问所有api
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
auth = HTTPBasicAuth()

#================================================#
#                 以下是对API的定义               #
#================================================#
@app.route('/imgUpload', methods=['GET', 'POST'])
def upload_img():
    print("image upload")
    result = 'static/label' # 结果放到/static/result
    if request.method == 'POST' or request.method == 'GET':    
        if 'file' not in request.files:   # 如果没有检测到上传了文件
            print('No file part')
            return redirect(request.url)  # 重定向
        
        file = request.files['file']  # 如果检测到了文件，传给file
        # print(file.filename) 
        if file.filename == '':  # 如果用户没有选择文件，浏览器仍然会提交一个没有filename的part，所以要再判断
            print('No selected file')
            return redirect(request.url)
        
        if file:# and allowed_file(file.filename):
            filename = secure_filename(file.filename)  # 提取文件名
            # 把文件存到/upload 因为flask的file是封装好的，不能直接拿
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            fileurl = os.path.join(app.config['UPLOAD_FOLDER'], filename)  # 存文件的地方，即：upload/xxx.jpg
            predict(filename)  #get the label pic and store it in the result folder
            # os.remove(fileurl) 暂时先不删除 测试接口是否正常
            
            #label=os.path.join(result,filename)	
            return jsonify(filename)  # 返回名称便于拿

#==============================================================================================================================
#                                                                                                                              
#                                           Main function                                                        	            #						     									       
#  				                                                                                                
#==============================================================================================================================
@app.route("/")
def main():
    
    return render_template("main.html")   
if __name__ == '__main__':
    app.run(debug = True, host= '0.0.0.0',port=8000)
