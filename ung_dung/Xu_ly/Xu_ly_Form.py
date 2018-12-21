from flask_wtf import FlaskForm
# from flask.ext.wtf import FlaskForm
from wtforms import TextField, IntegerField, TextAreaField, SubmitField, RadioField, SelectField, PasswordField, StringField
from wtforms.widgets import PasswordInput
from wtforms import validators, ValidationError

class Form_Lien_he(FlaskForm):
    Th_Ho_ten = TextField('Tên khách hàng', [validators.Required('Vui lòng nhập tên.')])
    Th_Gioi_tinh = RadioField('Giới tính', choices=[('M', 'Nam'), ('F', 'Nữ'), ('D', 'Khác')])
    Th_Dia_chi = TextAreaField('Địa chỉ')

    Th_Email = TextField('Email', [validators.Required('Vui lòng nhập email)'), validators.Email('Email phải đúng quy định')])
    Th_Tuoi = IntegerField('Tuổi')
    Th_Ly_do = SelectField('Góp ý cho', choices=[('TGGH', 'Thời gian giao hàng'), ('CSKH', 'Chăm sóc khách hàng'), ('TVSP', 'Tư vấn sản phẩm')])
    
    Th_Noi_dung = TextField('Nội dung')
    Th_submit = SubmitField('Gửi ý kiến')

class Form_Dang_ky(FlaskForm):
    Th_Ho_ten = TextField('Họ tên', [validators.Required('Vui lòng nhập tên.')])
    Th_Gioi_tinh = RadioField('Giới tính', choices=[('0', 'Nam'), ('1', 'Nữ'), ('?', 'Khác')])
    Th_Dia_chi = TextField('Địa chỉ', [validators.Required('Vui lòng nhập địa chỉ)')])
    Th_Dien_thoai = TextField('Điện thoại', [validators.Required('Vui lòng nhập điện thoại)')])
    Th_Email = TextField('Email', [validators.Required('Vui lòng nhập email)'), validators.Email('Email phải đúng quy định')])
    Th_Mat_khau = PasswordField('Mật khẩu', [validators.InputRequired(), validators.EqualTo('Th_Mat_khau')])
    Th_Mat_khau_Xac_nhan = PasswordField('Mật khẩu xác nhận')    
    Th_Dia_chi_giao_hang = TextAreaField('Địa chỉ giao hàng')
    Th_submit = SubmitField('Đăng ký')

class Form_Dat_hang(FlaskForm):
    Th_Ho_ten = TextField('Tên khách hàng', [validators.Required('Vui lòng nhập tên.')])
    Th_Gioi_tinh = RadioField('Giới tính', choices=[('M', 'Nam'), ('F', 'Nữ'), ('D', 'Khác')])
    Th_Dia_chi = TextAreaField('Địa chỉ')
    Th_Email = TextField('Email', [validators.Required('Vui lòng nhập email)'), validators.Email('Email phải đúng quy định')])
    Th_Dien_thoai = TextField('Điện thoại liên hệ', [validators.Required('Vui lòng nhập tên.')])
    Th_submit = SubmitField('Xác nhận thông tin')