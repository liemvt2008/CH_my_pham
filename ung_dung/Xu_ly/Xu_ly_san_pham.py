from ung_dung.Xu_ly.Xu_ly_Model import *
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
Base.metadata.bind = engine
DBSession= sessionmaker(bind=engine)
session_1 = DBSession()

def Doc_danh_sach_Khach_hang():
    DSKhach_hang = session_1.query(khach_hang).all()
    return DSKhach_hang


def Doc_danh_sach_san_pham():
    DSSanPham = session_1.query(san_pham).all()
    return DSSanPham

def Doc_san_pham_theo_ID(_id):
    SanPham = session_1.query(san_pham).filter(san_pham.ma_san_pham==_id).first()
    return SanPham
