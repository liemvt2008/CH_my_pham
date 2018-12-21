from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import Column, ForeignKey, Integer, String, Float
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from sqlalchemy import create_engine
from flask_login import UserMixin, LoginManager, current_user, login_user

Base = declarative_base()
engine = create_engine('sqlite:///ung_dung/Du_lieu/ql_CH_My_pham.db?check_same_thread=False')

class bai_viet(Base):
    __tablename__='bai_viet'
    ma_bai_viet = Column(Integer, nullable=False, primary_key=True)
    ma_nguoi_dung = Column(Integer, nullable=False)
    tieu_de = Column(String(200), nullable=False)
    noi_dung_tom_tat = Column(String, nullable=False)
    noi_dung_chi_tiet = Column(String, nullable=False)
    ngay_gui_bai = Column(String, nullable=False)
    ngay_xuat_ban = Column(String)
    ngay_het_han = Column(String)
    So_lan_xem = Column(Integer)
    xuat_ban = Column(Integer)
    def __str__(self):
        return self.tieu_de

class nguoi_dung(Base):
    __tablename__='nguoi_dung'
    ma_nguoi_dung = Column(Integer, nullable=False, primary_key=True)
    ten_khach_hang = Column(String(200), nullable=False)
    gioi_tinh = Column(String(50), nullable=False)
    dia_chi = Column(String(50), nullable=False)
    dien_thoai = Column(String(50), nullable=False)
    email = Column(String(50), nullable=False)

    def __str__(self):
        return self.ho_ten

class san_pham(Base):
    __tablename__='san_pham'
    ma_san_pham = Column(String(100), nullable=False, primary_key=True)
    ten_san_pham = Column(String(100), nullable=False)
    noi_dung_tom_tat = Column(String)
    mo_ta_chi_tiet = Column(String)
    don_gia = Column(Integer, nullable=False, default=0)
    DVT = Column(String, nullable=False, default="Cai")
    tinh_trang = Column(String,nullable=False, default="Còn hàng")
    hinh = Column(String)
    san_pham_moi = Column(Integer)
    def __str__(self):
        return self.ten_san_pham

class khach_hang(Base):
    __tablename__='khach_hang'
    ma_khach_hang = Column(Integer, nullable=False, primary_key=True)
    ten_khach_hang = Column(String(100), nullable=False)
    phai = Column(String(3), nullable=False)
    dia_chi = Column(String(200), nullable=False)
    dien_thoai = Column(String(20), nullable=False)
    email = Column(String(100), nullable=False)
    mat_khau = Column(String(50), nullable=False)

    def __str__(self):
        return self.ten_khach_hang

class hoa_don(Base):
    __tablename__='hoa_don'
    so_hoa_don = Column(Integer, nullable=False, primary_key=True)
    ngay_hd = Column(String, nullable=False)
    thong_tin_khach = Column(String, nullable=False)
    Thong_tin_sp = Column(Integer, nullable=False)
    Tong_tien = Column(Integer, nullable=False)
    
    def __str__(self):
        return self.so_hoa_don

class ct_hoa_don(Base):
    __tablename__='ct_hoa_don'
    so_hoa_don = Column(String(100), primary_key=True)
    ten_san_pham = Column(String(100))
    so_luong = Column(Integer, nullable=False)
    don_gia = Column(Integer, nullable=False)
    thanh_tien = Column(Integer, nullable=False)
    ten_khach_hang = Column(String(100),nullable=False)
    email = Column(String(100),nullable=False)
    dia_chi = Column(String(100),nullable=False)
    dien_thoai = Column(String(100),nullable=False)
    def __str__(self):
        return self.ten_san_pham

class san_pham_khuyen_mai(Base):
    __tablename__='san_pham_khuyen_mai'
    ma_san_pham = Column(Integer, nullable=False, primary_key=True)
    ma_loai = Column(Integer, nullable=False)
    ma_loai_cha = Column(Integer, nullable=False)
    don_gia_khuyen_mai = Column(Integer, nullable=False)
    noi_dung_khuyen_mai = Column(Integer, nullable=False)
    dot_Khuyen_mai = Column(String(200), nullable=False)
    tu_ngay = Column(String(20), nullable=False)
    den_ngay = Column(String(20), nullable=False)
    hinh_khuyen_mai = Column(String(100))
    def __str__(self):
        return self.dot_Khuyen_mai

class thuong_hieu(Base):
    __tablename__='thuong_hieu'
    ma_thuong_hieu = Column(Integer, nullable=False, primary_key=True)
    ten_thuong_hieu = Column(String(100), nullable=False)
    ten_thuong_hieu_url = Column(String(200))
    dia_chi = Column(String(200))
    dien_thoai = Column(String(20))
    email = Column(String(100))
    fax = Column(String(100))
    thuong_hieu_hang_dau = Column(Integer)
    hinh_thuong_hieu = Column(String(100))
    def __str__(self):
        return self.ten_thuong_hieu


class Quan_tri(Base, UserMixin):
    __tablename__ = 'Quan_tri'
    id = Column(Integer, primary_key= True) 
    Ho_ten = Column(String(200), nullable=False)
    Ten_dang_nhap = Column(String(50), nullable=False) 
    Mat_khau = Column(String(50), nullable=False) 

if __name__ == '__main__':
    Base.metadata.create_all(engine)
    print('Finished')
