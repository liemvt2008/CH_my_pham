from flask import Flask
app=Flask(__name__, static_url_path="", static_folder="Media",template_folder='Giao_dien')

app.secret_key = "super secret key"
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///un_dung/Du_lieu/ql_CH_My_pham.db'
# Create in-memory database
#import QL_ban_sach_239.sach_theo_loai
import ung_dung.app_san_pham
import ung_dung.appAdmin