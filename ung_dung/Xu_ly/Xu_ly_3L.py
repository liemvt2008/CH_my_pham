class Dia_diem(object):
    def __init__(self, Ma_so, Ten,Vi_do, Kinh_do):
        #lat: vi do, long: kinh do
        self.Ma_so = Ma_so
        self.Ten = Ten
        self.Vi_do = Vi_do
        self.Kinh_do = Kinh_do

from flask import   Markup, url_for
import json
import os
import sqlite3
from datetime import datetime
from ung_dung.Xu_ly.Xu_ly_san_pham import *

Thu_mu_y_kien = "ung_dung/Du_lieu/Y_kien/"
Du_lieu = "ung_dung/Du_lieu/ql_CH_My_pham.db"

def Ghi_y_kien(Y_kien):
    Ngay = datetime.now().strftime("%d-%m-%Y-%H-%M")
    Ten_tap_tin = Thu_mu_y_kien + Ngay + '_' + Y_kien['Ho_ten']+ '.json'
    f = open(Ten_tap_tin, 'w', encoding='utf-8')
    json.dump(Y_kien, f, indent=4, ensure_ascii=False)
    f.close()
    return True

def Them_thanh_vien(Khach_hang):
    result = False
    conn = sqlite3.connect(Du_lieu)
    sql = "INSERT INTO khach_hang (ten_khach_hang,phai,dia_chi,dien_thoai,email,mat_khau) \
                  VALUES (?, ?, ?, ?, ?, ?)"
    if conn.execute(sql,(Khach_hang["Ho_ten"], Khach_hang["Phai"],Khach_hang["Dia_chi"], Khach_hang["Dien_thoai"], Khach_hang["Email"], Khach_hang["Mat_khau"])):
        print('Khach hang is inserted successfully!')
        result = True
    conn.commit()    
    conn.close()
    return result

def Them_nguoi_dung(Khach_hang):
    result = False
    conn = sqlite3.connect(Du_lieu)
    sql = "INSERT INTO nguoi_dung (ten_khach_hang,gioi_tinh,dia_chi,dien_thoai,email) \
                  VALUES (?, ?, ?, ?, ?)"
    if conn.execute(sql,(Khach_hang["ten_khach_hang"], Khach_hang["gioi_tinh"],Khach_hang["dia_chi"], Khach_hang["dien_thoai"], Khach_hang["email"])):
        print('Nguoi dung is inserted successfully!')
        result = True
    conn.commit()    
    conn.close()
    return result

# doc du_lieu tu CSDL
def Doc_bang_CSDL(Ten_bang):
    conn = sqlite3.connect(Du_lieu)
    print(conn)
    print ("Opened database successfully")
    list_dong = []    
    cursor = conn.execute("select * from " +Ten_bang)
    for row in cursor:        
        print(row)
        list_dong.append(row)          
    print ("Operation done successfully")
    #print(list_dong)
    conn.commit()
    conn.close()
    return list_dong

def Doc_danh_sach_Khach_hang():
    Danh_sach = []    
    danh_sach_khach_hang = Doc_bang_CSDL("khach_hang")
    #print(danh_sach_khach_hang)
    for KH in danh_sach_khach_hang:    
        KH_dict = {}
        KH_dict["ma_khach_hang"] = KH[0]
        KH_dict["ten_khach_hang"] = KH[1]
        KH_dict["phai"] = KH[2]
        KH_dict["dia_chi"] = KH[3]
        KH_dict["dien_thoai"] = KH[4]
        KH_dict["email"] = KH[5]
        KH_dict["mat_khau"] = KH[6]
        Danh_sach.append(KH_dict)
    return Danh_sach

def Doc_danh_sach_san_pham():
    Danh_sach = []    
    danh_sach_sp = Doc_bang_CSDL("san_pham")
    #print(danh_sach_khach_hang)
    for SP in danh_sach_sp:    
        SP_dict = {}
        SP_dict["ma_san_pham"] = SP[0]
        SP_dict["ten_san_pham"] = SP[1]
        SP_dict["noi_dung_tom_tat"] = SP[2]
        SP_dict["mo_ta_chi_tiet"] = SP[3]
        SP_dict["don_gia"] = SP[4]
        SP_dict["DVT"] = SP[5]
        SP_dict["tinh_trang"] = SP[6]
        SP_dict["hinh"] = SP[7]
        SP_dict["san_pham_moi"] = SP[8]
        Danh_sach.append(SP_dict)
    return Danh_sach

def Tao_chuoi_HTML_Khach_hang(Khach_hang):    
#    Chuoi_HTML_Khach_hang = '<div class="row" >'
#    Chuoi_Hinh = '<img  style="width:60px;height:60px"  src="'+ url_for('static', filename = 'user.png') + '" />'
    Chuoi_Thong_tin = '<a class="btn btn-outline-success my-2 my-sm-0" type="submit" +\
    style="text-align:left" href="/Dang_xuat"> Xin chào quý khách ' + Khach_hang["ten_khach_hang"] + "</a>"    
    Chuoi_HTML_Khach_hang = Chuoi_Thong_tin  
    return Markup(Chuoi_HTML_Khach_hang)

def Tao_chuoi_HTML_Dang_nhap():    
#    Chuoi_HTML_Khach_hang = '<div class="row" >'
#    Chuoi_Hinh = '<img  style="width:60px;height:60px"  src="'+ url_for('static', filename = 'user.png') + '" />'
    Chuoi_Thong_tin = '<a class="btn btn-outline-success my-2 my-sm-0" type="submit" +\
    style="text-align:left" href="/Dang_nhap"> Đăng nhập </a>'    
    Tao_chuoi_HTML_Dang_nhap = Chuoi_Thong_tin  
    return Markup(Tao_chuoi_HTML_Dang_nhap)

# Xử lý Nghiệp vụ 
def Tra_cuu_sp(Chuoi_Tra_cuu, Danh_sach_sp):
    Danh_sach=list(filter(
        lambda sp: Chuoi_Tra_cuu.upper() in  sp["ma_san_pham"].upper(),Danh_sach_sp))
    return Danh_sach

#lay chi tiet sp
def Lay_chi_tiet_sp(Danh_sach_sp, Ma_so):
    Danh_sach  = list(filter(
        lambda sp: sp["ma_san_pham"] == Ma_so, Danh_sach_sp))
    kq = Danh_sach[0] if len(Danh_sach)==1 else None
    return kq

# lay thong tin NV
def Dang_nhap_Khach_hang(Danh_sach_Khach_hang, Ten_dang_nhap, Mat_khau):
    Danh_sach = list(filter(
        lambda Khach_hang: Khach_hang['email'] == Ten_dang_nhap and Khach_hang["mat_khau"] == Mat_khau
        , Danh_sach_Khach_hang))
    khach_hang = Danh_sach[0] if len(Danh_sach)==1 else None
    
    return khach_hang

def Tao_Chuoi_HTML_Danh_sach_Dat_hang(Danh_sach_sp):
    Tong_so_tien = 0
    Chuoi_HTML_Danh_sach = '<div class="container-fluid" style="text-align:center; color:green">'
    Chuoi_HTML_Danh_sach +='<h5 style="color:green"><div class="btn"> ĐƠN HÀNG <br/> Chi tiết đơn hàng </div></h5>'    
    Chuoi_HTML_Danh_sach +='<div class="container-fluid" style="color:green;text-align:left">'
    for san_pham in Danh_sach_sp:
        Chuoi_Don_gia_Ban="Đơn giá Bán: {:,}".format(san_pham["don_gia"]).replace(",",".")    
        Chuoi_Hinh_nho='<img  style="width:60px;height:60px"  src="'+ \
                 url_for('static', filename = san_pham['hinh']) + '" />'
        Thanh_tien = san_pham["So_luong"] * san_pham["don_gia"]
        Tong_so_tien += Thanh_tien
        Chuoi_thanh_tien = "Thành tiền:" +str(san_pham["So_luong"]) +"x" + \
                            "{:,}".format(san_pham["don_gia"]).replace(",",".") + " = " +\
                            "{:,}".format(Thanh_tien).replace(",",".")
        Chuoi_Thong_tin='<div class="btn" style="text-align:left">' + \
                 san_pham["ten_san_pham"] + "<br />" + Chuoi_Don_gia_Ban + "<br/>" + Chuoi_thanh_tien + "</div>"
        
        Chuoi_HTML ='<div>' +  \
                Chuoi_Hinh_nho + Chuoi_Thong_tin + '</div>' 
        Chuoi_HTML_Danh_sach +=Chuoi_HTML 

    Chuoi_HTML_Danh_sach +="</div>"
    Chuoi_Tong_tien="<br/>Tổng tiền {:,}".format(Tong_so_tien).replace(",",".")
    Chuoi_HTML_Danh_sach +="<div class= 'container-fluid'><h5 style='color:green'>" + Chuoi_Tong_tien + "</h5></div>"

    Chuoi_Dat_hang = '''<br/><div ><form method="POST" action="/Thanh_toan"> 
                <input type="hidden" name="Th_Dat_hang" value="DH_OK" />                               
                 &nbsp;&nbsp;&nbsp;<button class="btn btn-success" type="submit">Đặt hàng</button><br/>
                </form></div>'''

    Chuoi_HTML_Danh_sach += Chuoi_Dat_hang + '</div>'               
    return Markup(Chuoi_HTML_Danh_sach)  

def Them_Don_hang(Don_hang):
    result = False
    conn = sqlite3.connect(Du_lieu, timeout=10)
    sql = "INSERT INTO hoa_don(ngay_hd,thong_tin_khach,thong_tin_sp,Tong_tien) \
                  VALUES (?, ?, ?, ?)"
    Khach_hang = json.dumps(Don_hang["Khach_hang"],ensure_ascii=False)
    Chi_tiet_don_hang = json.dumps(Don_hang["Chi_tiet_don_hang"],ensure_ascii=False)
    if conn.execute(sql,(Don_hang["Ngay_dat_hang"],Khach_hang,Chi_tiet_don_hang,Don_hang["Tong_tien"]["Tong_tien"])):
        print('Don_hang is inserted successfully!')
        result = True
    conn.commit()    
    conn.close()
    return result

def Them_Don_hang_chi_tiet(Don_hang):
    ten_kh = Don_hang['Khach_hang']['Khach_hang']['ten_khach_hang']
    email_kh = Don_hang['Khach_hang']['Khach_hang']['email']
    dia_chi_kh = Don_hang['Khach_hang']['Khach_hang']['dia_chi']
    dien_thoai_kh = Don_hang['Khach_hang']['Khach_hang']['dien_thoai']

    for sp in Don_hang["Chi_tiet_don_hang"]["Chi_tiet_don_hang"]:
        ten_sp = sp['ten_san_pham']
        sl_sp = sp['So_luong']
        don_gia_sp = sp['don_gia']
        thanh_tien = sl_sp*don_gia_sp

        result = False
        conn = sqlite3.connect(Du_lieu, timeout=10)
        sql = "INSERT INTO ct_hoa_don(ten_san_pham,so_luong,don_gia,thanh_tien,ten_khach_hang,email,dia_chi,dien_thoai) \
                    VALUES (?, ?, ?, ?, ?, ?, ?, ?)"
    #    Khach_hang = json.dumps(Don_hang["Khach_hang"],ensure_ascii=False)
    #    Chi_tiet_don_hang = json.dumps(Don_hang["Chi_tiet_don_hang"],ensure_ascii=False)
        if conn.execute(sql,(ten_sp,sl_sp,don_gia_sp,thanh_tien,ten_kh,email_kh,dia_chi_kh,dien_thoai_kh)):
            print('Don_hang_chi_tiet is inserted successfully!')            
            result = True
            conn.commit()    
            conn.close()
    return result

def Tao_hoa_don(Danh_sach_sp):
    Tong_so_tien = 0
    hoa_don = []
    total = {}
    for san_pham in Danh_sach_sp:
        SP_dict = {}
        SP_dict["ten_san_pham"] = san_pham['ten_san_pham']
        SP_dict["don_gia"] = san_pham['don_gia']
        SP_dict["So_luong"] = san_pham['So_luong']
        Thanh_tien = san_pham["So_luong"] * san_pham["don_gia"]
        SP_dict["Thanh_tien"] = Thanh_tien
        hoa_don.append(SP_dict)
        Tong_so_tien += Thanh_tien
    total["Tong_tien"] = Tong_so_tien
    hoa_don.append(total)
    return hoa_don