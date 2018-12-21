from ung_dung import app
from flask import Flask, flash, redirect, render_template, request, session, abort, url_for, Markup
from ung_dung.Xu_ly.Xu_ly_3L import *
from datetime import datetime
from ung_dung.Xu_ly.Xu_ly_Form import *
#from ung_dung.Xu_ly.Xu_ly_san_pham import *
from flask_mail import Mail, Message

app.config['MAIL_SERVER'] = 'smtp.gmail.com'
app.config['MAIL_PORT'] = 465
app.config['MAIL_USERNAME'] = 'pythonshop245@gmail.com'
app.config['MAIL_PASSWORD'] = 'SEHC2018'
app.config['MAIL_USE_TLS'] = False
app.config['MAIL_USE_SSL'] = True

mail = Mail(app)

@app.route('/', methods=['GET','POST'])
def index():
    Danh_sach_sp_chon = []
    if session.get('Gio_hang'):
        Danh_sach_sp_chon = session['Gio_hang']['Gio_hang']

    return render_template('khach/index.html',gio_hang=Danh_sach_sp_chon)

@app.route('/danh_sach_sp', methods=['GET','POST'])
def danh_sach_sp():
#    session['Khach_hang_Dang_nhap'] = Khach_hang
    Danh_sach_sp_chon = []
    Ds_san_pham =Doc_danh_sach_san_pham()
    Chuoi_Tra_cuu=""
    Ds_san_pham_xem = Ds_san_pham

    if (request.form.get('Th_Chuoi_Tra_cuu') !=None):
        Chuoi_Tra_cuu=request.form.get('Th_Chuoi_Tra_cuu')

    Ds_san_pham_xem= Tra_cuu_sp(Chuoi_Tra_cuu,Ds_san_pham)
# xu ly them vao gio hang
    if request.method == 'POST':
        #them vao gio hang      
        if request.form.get('Th_Ma_so') !=None: 
            if session.get('Gio_hang'):
                Danh_sach_sp_chon = session['Gio_hang']['Gio_hang']

            Ma_so = request.form.get('Th_Ma_so')   
            So_luong = int(request.form.get("Th_So_luong"))
            sp_Chon = Lay_chi_tiet_sp(Ds_san_pham, Ma_so)
            if Lay_chi_tiet_sp(Danh_sach_sp_chon, Ma_so)!=None:
                #sp da co trong Danh_sach_sp_chon
                sp_cu = Lay_chi_tiet_sp(Danh_sach_sp_chon, Ma_so)
                So_luong_cu = sp_cu["So_luong"]
                So_luong = So_luong + So_luong_cu
                Danh_sach_sp_chon.remove(sp_cu)
            sp_Chon["So_luong"] = So_luong
            print(sp_Chon)   
            Danh_sach_sp_chon.append(sp_Chon)
            print(Danh_sach_sp_chon)
            session['Gio_hang'] = {'Gio_hang':Danh_sach_sp_chon}
        #cap nhat gio hang
        if request.form.get('Th_Ma_so_1') !=None: 
            Danh_sach_sp_chon = []
            if session.get('Gio_hang'):
                Danh_sach_sp_chon = session['Gio_hang']['Gio_hang']            
            Ma_so_1 = request.form.get('Th_Ma_so_1') 
            print("Ma so 1:", Ma_so_1)  
            So_luong_1 = int(request.form.get("Th_So_luong_1"))              
            sp_Chon = Lay_chi_tiet_sp(Danh_sach_sp_chon, Ma_so_1)

            print("SP chọn:", sp_Chon)
            if sp_Chon!=None:
                Danh_sach_sp_chon.remove(sp_Chon)
            if So_luong_1>0 and sp_Chon!=None:
                sp_Chon['So_luong'] = So_luong_1
                Danh_sach_sp_chon.append(sp_Chon)
            session['Gio_hang'] = {'Gio_hang':Danh_sach_sp_chon}
            
    if session.get('Gio_hang'):
        Danh_sach_sp_chon = session['Gio_hang']['Gio_hang']

    return render_template('khach/danh_sach_sp.html', Ds_san_pham=Ds_san_pham_xem, gio_hang=Danh_sach_sp_chon)

@app.route('/contact', methods=['GET','POST'])
def contact():   
    ### Phần này để tạo google map cho khách tìm các chi nhánh cửa hàng
    Danh_sach_dia_chi = [
    Dia_diem("CH1",'Số 10 Lê Văn Sỹ, P.11, Q.PN', 10.790544, 106.673829),
    Dia_diem("CH2",'Số 352 Đường 3/2, P12, Q.10', 10.769529, 106.670195), 
    Dia_diem("CH3",'Số 255 Nguyễn Thị Thập, P.TP, Q.7', 10.737313, 106.716625)  
    ]

    Danh_sach_dia_chi_theo_ma_so = {dia_chi.Ma_so: dia_chi for dia_chi in Danh_sach_dia_chi}

    dia_chi=None
    if request.form.get('Th_Ma_so')!=None:
        dia_chi = Danh_sach_dia_chi_theo_ma_so.get(request.form.get('Th_Ma_so'))
    ### Phần này dùng để tạo form và nhận phản hồi từ khách hàng
    Chuoi_ket_qua=''
    form = Form_Lien_he()
    if form.validate_on_submit():
        Ho_ten = request.form['Th_Ho_ten']
        Gioi_tinh = request.form['Th_Gioi_tinh']
        Dia_chi = request.form['Th_Dia_chi']
        Email = request.form['Th_Email']
        Ly_do = request.form['Th_Ly_do']
        Noi_dung = request.form['Th_Noi_dung']
        if len(Ho_ten)>2 and len(Email)>6:
            Ngay = datetime.now().strftime("%d-%m-%Y")
            Y_kien ={"Ho_ten": Ho_ten, "Gioi_tinh": Gioi_tinh ,"Dia_chi": Dia_chi,"Email": Email,
            "Ly_do": Ly_do,"Noi_dung": Noi_dung,"Ngay_gui": Ngay}
            Ghi_y_kien(Y_kien)
            print(Y_kien)
            Chuoi_ket_qua+="Cảm ơn khách hàng " + Ho_ten + ' Đã gửi ý kiến'
        flash("Cảm ơn khách hàng " + Ho_ten + ' Đã gửi ý kiến')
    else:
        flash("Error: Vui long nhap day du cac noi dung yeu cau")

    return render_template('khach/contact.html', Dia_chi=dia_chi, Danh_sach_dia_chi=Danh_sach_dia_chi,
    form=form, Chuoi_ket_qua=Chuoi_ket_qua)

@app.route("/Dang_ky", methods=['GET', 'POST'])
def Dang_ky():
    Chuoi_ket_qua = ''
    form = Form_Dang_ky()
    if form.validate_on_submit():
        Ho_ten = request.form['Th_Ho_ten']
        Gioi_tinh = request.form['Th_Gioi_tinh']
        Dia_chi = request.form['Th_Dia_chi']
        Dien_thoai = request.form['Th_Dien_thoai']
        Email = request.form['Th_Email']
        Mat_Khau = request.form['Th_Mat_khau']
        Th_Mat_khau_Xac_nhan = request.form['Th_Mat_khau_Xac_nhan']
        Dia_chi_giao_hang = request.form['Th_Dia_chi_giao_hang']
        if (str(Mat_Khau)==str(Th_Mat_khau_Xac_nhan)):
            print('Du lieu hop le')
            Khach_hang = {'Ho_ten':Ho_ten,'Phai':Gioi_tinh,
                        'Dia_chi':Dia_chi,'Dien_thoai':Dien_thoai,'Email':Email,'Mat_khau':Mat_Khau,
                        'Dia_chi_giao_hang':Dia_chi_giao_hang}
            if(Them_thanh_vien(Khach_hang)):
                Chuoi_ket_qua = 'Tài khoản của quý khách đã được tạo thành công'
                return redirect(url_for('Dang_nhap'))
            flash('Đăng ký tài khoản thành công')
        else:
            flash('Mật khẩu và mật khẩu xác nhận không giống nhau, vui lòng kiểm tra lại')
    else:
        flash('Error: Vui lòng nhập đầy đủ các thông tin')
    return render_template('khach/DK_moi.html', form=form, Chuoi_ket_qua=Markup(Chuoi_ket_qua))

@app.route("/Dang_nhap", methods=['GET', 'POST'])
def Dang_nhap():
    # ****** Khởi động Dữ liệu Nguồn/Nội bộ ********
    if session.get("Khach_hang_Dang_nhap"):
        return redirect(url_for('danh_sach_sp'))
    Danh_sach_khach_hang = Doc_danh_sach_Khach_hang()
    print(Danh_sach_khach_hang)
    Ten_dang_nhap = ""
    Mat_khau = ""
    Chuoi_Thong_bao = "Xin vui lòng Nhập Tên đăng nhập (email) và Mật khẩu"
    if request.method == 'POST':
        Ten_dang_nhap = request.form.get('Th_Ten_dang_nhap')
        Mat_khau = request.form.get('Th_Mat_khau')
        Khach_hang = Dang_nhap_Khach_hang(Danh_sach_khach_hang, Ten_dang_nhap, Mat_khau)

        Hop_le = (Khach_hang != None)
        if Hop_le:            
            session['Khach_hang_Dang_nhap'] = Khach_hang
            return redirect(url_for('danh_sach_sp'))
        else:
            Chuoi_Thong_bao = "Đăng nhập không hợp lệ"
    return render_template('khach/Dang_nhap.html',Chuoi_Thong_bao=Markup(Chuoi_Thong_bao))

@app.route("/Dang_xuat", methods=['GET', 'POST'])
def Dang_xuat():
    session.pop('Khach_hang_Dang_nhap', None)
    return redirect(url_for('index'))

@app.route('/about_us', methods=['GET','POST'])
def about_us():    
    return render_template('khach/about_us.html')

@app.route("/Dat_hang", methods=['GET', 'POST'])
def Dat_hang():
    Chuoi_ket_qua = ""
    form = Form_Dat_hang()
    Danh_sach_sp_chon = []
    if session.get('Khach_hang_Dang_nhap'):
        Khach_hang_Dang_nhap = session["Khach_hang_Dang_nhap"]
        return redirect(url_for('Thanh_toan'))
    else:
        if form.validate_on_submit():
            Ho_ten = request.form['Th_Ho_ten']
            Gioi_tinh = request.form['Th_Gioi_tinh']
            Dia_chi = request.form['Th_Dia_chi']
            Email = request.form['Th_Email']
            Dien_thoai = request.form['Th_Dien_thoai']
            khach_hang = {'ten_khach_hang':Ho_ten,'gioi_tinh':Gioi_tinh,'dia_chi':Dia_chi,'dien_thoai':Dien_thoai,'email':Email}
            if(Them_nguoi_dung(khach_hang)):
                session["Khach_hang_Dang_nhap"] = khach_hang
                return redirect(url_for('Thanh_toan'))
                flash('Đã thu thập thông tin khách hàng thành công')
            else:
                flash('Error: chưa thu thập thông tin người mua được')
        else:
            flash('Error: Vui lòng nhập đầy đủ các thông tin')
    if session.get('Gio_hang'):
        Danh_sach_sp_chon = session['Gio_hang']['Gio_hang']

    return render_template('khach/Dat_hang.html', form=form, Chuoi_ket_qua=Chuoi_ket_qua,
    gio_hang=Danh_sach_sp_chon)

@app.route("/Thanh_toan", methods=['GET', 'POST'])
def Thanh_toan():
    Danh_sach_sp_chon = []
    Chuoi_hoa_don = ''
    Chuoi_Thong_bao = ""
    if session.get('Khach_hang_Dang_nhap'):
        Khach_hang_Dang_nhap = session["Khach_hang_Dang_nhap"]
#        print(Khach_hang_Dang_nhap)
        if session.get('Gio_hang'):
            Danh_sach_sp_chon = session['Gio_hang']['Gio_hang']
#            print(Danh_sach_sp_chon)
            Chuoi_HTML_Mua_hang = Tao_Chuoi_HTML_Danh_sach_Dat_hang(Danh_sach_sp_chon) 
            hoa_don = Tao_hoa_don(Danh_sach_sp_chon)
            print(hoa_don)
            Chuoi_hoa_don = '<table border="1px"> <tr> <th> Tên sản phẩm </th>' +\
            '<th> Đơn giá </th> <th> Số lượng </th> <th> Thành Tiền </th> </tr>'
            Tong_tien = hoa_don.pop()
            for item in hoa_don:
                Chuoi_hoa_don += '<tr><td>' +item['ten_san_pham'] + '</td>'+\
                '<td>' + str(item['don_gia']) + '</td>' +\
                '<td>' + str(item['So_luong']) + '</td>' +\
                '<td>' + str(item['Thanh_tien']) + '</td>' + '</tr>'
            if request.method == 'POST':
                    if request.form.get('Th_Dat_hang') == "DH_OK":
                    # nguoi dung da nhan nut dat hang
                    # ghi don hang vao CSDL
                        print(request.form.get('Th_Dat_hang'))
                        Don_hang = {}
                        Don_hang["Ngay_dat_hang"] = datetime.now().strftime('%d-%m-%Y')
                        Don_hang["Khach_hang"] = {"Khach_hang":Khach_hang_Dang_nhap}
                        Don_hang["Chi_tiet_don_hang"] = {"Chi_tiet_don_hang":Danh_sach_sp_chon}
                        Don_hang["Tong_tien"] = Tong_tien
                        print(Don_hang)
                        if Them_Don_hang(Don_hang) and Them_Don_hang_chi_tiet(Don_hang):
                            # Thông báo đã đặt hàng thành công
                            Chuoi_Thong_bao = "<div><h5 style='color:blue; text-align:center'> Đơn hàng của quý khách đã đặt thành công. <br/>"+\
                            "Cảm ơn quý khách đã ủng hộ cửa hàng.<br/></h5>"+\
                            "<a style='color:green; text-align:center' href='/danh_sach_sp'>Tiếp tục mua hàng</a></div>"
                            #Gửi mail cho khách hàng thông báo đơn hàng 
                            Chuoi_tieu_de = 'Thông báo đơn hàng của quý khách -'  + Don_hang['Ngay_dat_hang']
                            msg = Message(Chuoi_tieu_de, sender = 'pythonkhoa245@gmail.com', recipients=[Khach_hang_Dang_nhap['email']])
                            Noi_dung_mail = 'NanaShop gửi đến ' + Khach_hang_Dang_nhap['ten_khach_hang'] +\
                            '<br/> Dưới đây là đơn hàng của quý khách' +\
                            Chuoi_hoa_don + '</table>' +\
                            '<br/> Tổng tiền: ' + str(Tong_tien['Tong_tien']) + ' VND </br>' +\
                            '<br/> Xin cảm ơn quý khách đã mua hàng - Nhân viên chúng tôi sẽ liên hệ sớm nhất có thể </br>'
                            mail.body = Noi_dung_mail
                            msg.html = mail.body
                            mail.send(msg)
                            print ('Da gui email den khach hang')
                            #giai phong gio hang
                            session.pop('Gio_hang', None)                            
                            Danh_sach_sp_chon = []
                            Chuoi_HTML_Mua_hang = ""

    return render_template('khach/Thanh_toan.html', 
    gio_hang=Danh_sach_sp_chon, Chuoi_HTML_Mua_hang=Chuoi_HTML_Mua_hang, 
    Chuoi_Thong_bao = Markup(Chuoi_Thong_bao))