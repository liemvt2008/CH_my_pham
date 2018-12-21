from flask import Flask, flash, redirect, render_template, request, session, abort, url_for, Markup
from flask_admin import Admin 
from flask_admin.contrib.sqla import ModelView
from flask_login import UserMixin, LoginManager, current_user, login_user, logout_user
from flask_admin.contrib import sqlamodel
from ung_dung.Xu_ly.Xu_ly_Model import *
from sqlalchemy.orm import sessionmaker
from sqlalchemy import exc
from sqlalchemy.orm import configure_mappers
from flask_admin import BaseView, expose
from ung_dung import app

configure_mappers()
Base.metadata.bind = engine
DBSession = sessionmaker(bind=engine)
session = DBSession()

admin = Admin(app, name='Quản lý mỹ phẫm', template_mode='bootstrap3') 

login = LoginManager(app)

@login.user_loader
def load_user(id):
    quan_tri = session.query(Quan_tri).filter(Quan_tri.id == id).first() # Truy vấn quan_tri theo id
    return quan_tri

class MyModelView(ModelView): # MyModelView kế thừa ModelView
    def is_accessible(self):
        return current_user.is_authenticated

class LogoutView(BaseView):
    @expose('/')
    def index(self):       
        logout_user() 
        return redirect(url_for('quan_tri_index'))



# Add administrative views here 
class san_pham_view(MyModelView):
    column_display_pk = True    
    can_create = True
    can_delete = True
    can_export = True
    
admin.add_view(san_pham_view(san_pham, session, "Sản phẩm"))

class bai_viet_view(MyModelView):
    column_display_pk = True    
    can_create = True
    can_delete = True
    can_export = True
    
admin.add_view(bai_viet_view(bai_viet, session, "Bài viết"))

class nguoi_dung_view(MyModelView):
    column_display_pk = True    
    can_create = True
    can_delete = True
    can_export = True
    
admin.add_view(nguoi_dung_view(nguoi_dung, session, "Khách hàng"))

class khach_hang_view(MyModelView):
    column_display_pk = True    
    can_create = True
    can_delete = True
    can_export = True
    
admin.add_view(khach_hang_view(khach_hang, session, "Thành viên"))

class hoa_don_view(MyModelView):
    column_display_pk = True    
    can_create = True
    can_delete = True
    can_export = True
    
admin.add_view(hoa_don_view(hoa_don, session, "Hóa đơn"))

class ct_hoa_don_view(MyModelView):
    column_display_pk = True    
    can_create = True
    can_delete = True
    can_export = True
    
admin.add_view(ct_hoa_don_view(ct_hoa_don, session, "Chi tiết Hóa đơn"))

class san_pham_khuyen_mai_view(MyModelView):
    column_display_pk = True    
    can_create = True
    can_delete = True
    can_export = True
    
admin.add_view(san_pham_khuyen_mai_view(san_pham_khuyen_mai, session, "Sản phẩm khuyến mãi"))

class thuong_hieu_view(MyModelView):
    column_display_pk = True    
    can_create = True
    can_delete = True
    can_export = True
    
admin.add_view(thuong_hieu_view(thuong_hieu, session, "Thương hiệu"))

class MyView(BaseView):
    @expose('/')
    def index(self):               
        return self.render('admin/myview.html')  

admin.add_view(MyView(name='View của tôi', menu_icon_type='glyph'))
admin.add_view(LogoutView(name='Đăng xuất', menu_icon_type='glyph'))

@app.route("/quan_tri", methods=['GET', 'POST'])
def quan_tri_index(): 
    Chuoi_Thong_bao = ""
    if request.method == 'POST':
        Ten_dang_nhap = request.form.get('Th_Ten_dang_nhap')
        Mat_khau = request.form.get('Th_Mat_khau')
        #try:
        quan_tri = session.query(Quan_tri).filter(Quan_tri.Ten_dang_nhap == Ten_dang_nhap and Quan_tri.Mat_khau == Mat_khau).first()
        Hop_le = quan_tri
        if Hop_le:
            login_user(quan_tri)                        
            return redirect(url_for('admin.index'))    # Trả về trang đầu tiên của màn hình Admin                  
        else:
            Chuoi_Thong_bao = "Đăng nhập không hợp lệ"
        #except:
            #Chuoi_Thong_bao = "Đăng nhập không hợp lệ"
    Khung= render_template('quan_tri/dang_nhap.html', Chuoi_Thong_bao = Chuoi_Thong_bao) 
    return Khung

