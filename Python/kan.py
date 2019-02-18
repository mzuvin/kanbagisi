#!/usr/bin/env python
# -*- coding: utf-8 -*-

from tkinter import *
from tkinter import ttk
from tkFont import *
import psycopg2
from tkinter import messagebox,  FALSE, Tk

import time


class Kan:


    col_names=[]
    global kantipleri
    kantipleri=['','A+','A-','B+','B-','AB+','AB-','0+','0-']
    def __init__(self,wind):
        
        self.wind=wind
        self.wind.title('Kan Bagisi')
        self.secilen="hasta"
        Label(self.wind, text='KAN Bankasi').grid(row=0, column=0)
        options=['hasta','kanveren']
        global gnd
        gnd="e"
        
        cinsiyet=['Erkek','Kadin']
        

        frame = LabelFrame(self.wind, text='Yeni Kayit-------------------------------------------------Yakını')
        frame.grid(row=1, column=0)
        
        yakin = LabelFrame(self.wind, text='İşlemler')
        yakin.grid(row=1, column=1)
        #self.yakinin()


        Label(yakin, text='Butuna Tıkla').grid(row=0, column=0)


        self.var=StringVar()
        self.var.set(self.secilen)
        self.var2=StringVar()
        self.var2.set("Cinsiyeti secin")
        #hasta/kanveren option menu
        self.drop=OptionMenu(frame,self.var,*options,command=self.table).grid(row=13, column=0)

        Label(frame, text='isim:').grid(row=1, column=0)
        self.name= Entry(frame)
        self.name.grid(row=1, column=1)

        self.yname= Entry(frame)
        self.yname.grid(row=1, column=3)

        Label(frame, text='Soyad:').grid(row=2, column=0)
        self.surname= Entry(frame)
        self.surname.grid(row=2, column=1)
        self.ysurname= Entry(frame)
        self.ysurname.grid(row=2, column=3)

        Label(frame, text='Cinsiyet:').grid(row=3, column=0)
        self.gender=OptionMenu(frame,self.var2,*cinsiyet,command=self.fcinsiyet).grid(row=3, column=1)
        #self.gender.config(width=12)
        """
        Label(frame, text='Cinsiyet:').grid(row=3, column=0)
        self.gender= Entry(frame)
        self.gender.grid(row=3, column=2)
        """
        Label(frame, text='mail:').grid(row=4, column=0)
        self.mail= Entry(frame)
        self.mail.grid(row=4, column=1)

        Label(frame, text='adres:').grid(row=5, column=0)
        self.adres= Entry(frame)
        self.adres.grid(row=5, column=1)

        self.yadres= Entry(frame)
        self.yadres.grid(row=5, column=3)

        Label(frame, text='tel:').grid(row=6, column=0)
        self.tel= Entry(frame)
        self.tel.grid(row=6, column=1)
        self.ytel= Entry(frame)
        self.ytel.grid(row=6, column=3)

        Label(frame, text='tc:').grid(row=7, column=0)
        self.tc= Entry(frame)
        self.tc.grid(row=7, column=1)
        self.ytc= Entry(frame)
        self.ytc.grid(row=7, column=3)


        #Kan gruplarını radio button yap
        self.kanid = IntVar()
        
        Radiobutton(frame, text="A+", variable=self.kanid, value=1, width=1).grid(row=8, column=0)
        Radiobutton(frame, text="A-", variable=self.kanid, value=2, width=1).grid(row=8, column=1)
        Radiobutton(frame, text="B+", variable=self.kanid, value=3, width=1).grid(row=8, column=2)
        Radiobutton(frame, text="B-", variable=self.kanid, value=4, width=1).grid(row=8, column=3)
        Radiobutton(frame, text="AB+", variable=self.kanid, value=5, width=1).grid(row=9, column=0)
        Radiobutton(frame, text="AB-", variable=self.kanid, value=6, width=1).grid(row=9, column=1)
        Radiobutton(frame, text="0+", variable=self.kanid, value=7, width=1).grid(row=9, column=2)
        Radiobutton(frame, text="0+", variable=self.kanid, value=8, width=1).grid(row=9, column=3)
        #self.kanid.set(0)
        #Label(frame, text='kan grubu:').grid(row=8, column=0)
        #self.kan= Entry(frame)
        #self.kan.grid(row=8, column=2)
        

        ttk.Button(frame, text='Ekle', command=self.add).grid(row=12,column=3)
        self.aratc = Entry(frame)
        self.aratc.grid(row=13, column=2)
        ttk.Button(frame, text='Ara',command=self.ara).grid(row=13, column=3)
        #ttk.Button(frame, text='Yakını ile ekle', command=self.addyakin).grid(row=12,column=3)

        #-------------kan verme bolumu
        self.kanver=Button(yakin, text='Kan Ver!', width=10,command=self.kanver).grid(row=2,column=0)
        self.kanal=Button(yakin, text='Kan Al!', width=10,command=self.kanal).grid(row=3,column=0)
        ttk.Button(yakin, text='Admin Paneli Aç!',width=18,command=self.adminpaneli).grid(row=4,column=0)

        self.kantree=ttk.Treeview(yakin,height=8,columns=("kan", "Rh","Adet"))
      
        #self.tree.tag_configure('T', font='Arial 5')
        
        self.kantree.grid(row=5,column=0,columnspan=3)
        
        self.kantree.heading('#0', text='0', anchor=CENTER)
        self.kantree.heading('#1', text='Kan', anchor=CENTER)
        self.kantree.heading('#2', text='Rh', anchor=CENTER)
        self.kantree.heading('#3', text='Adet', anchor=CENTER)
        self.kantree.column('#0', stretch=True, minwidth=0, width=0)
        self.kantree.column('#1', stretch=True, minwidth=50, width=55)
        self.kantree.column('#2', stretch=True, minwidth=50, width=55)
        self.kantree.column('#3', stretch=True, minwidth=50, width=55)
        self.kanadetviewing()
        self.kanmsj=Label(text='',fg='blue')
        self.kanmsj.grid(row=4,column=0)
        #
        
        self.message=Label(text='MESAJ:',fg='red')
        self.message.grid(row=12,column=0)

        self.tree=ttk.Treeview(height=15,columns=("tel", "isim", "soyad","cinsiyet",'il','mail','kan','tc','rh'))
      
        #self.tree.tag_configure('T', font='Arial 5')
        
        self.tree.grid(row=2,column=0,columnspan=1)
        
        self.tree.heading('#0', text='index', anchor=CENTER)
        self.tree.heading('#1', text='isim', anchor=CENTER)
        self.tree.heading('#2', text='soyisim', anchor=CENTER)
        self.tree.heading('#3', text='cinsiyet', anchor=CENTER)
        self.tree.heading('#4', text='sehir', anchor=CENTER)
        self.tree.heading('#5', text='eposta', anchor=CENTER)
        self.tree.heading('#6', text='hastane', anchor=CENTER)
        self.tree.heading('#7', text='kan', anchor=CENTER)
        self.tree.heading('#8', text='tc', anchor=CENTER)
        self.tree.heading('#9', text='tel', anchor=CENTER)
        self.tree.column('#0', stretch=True, minwidth=0, width=0)
        self.tree.column('#1', stretch=True, minwidth=50, width=75)
        self.tree.column('#2', stretch=True, minwidth=50, width=75)
        self.tree.column('#3', stretch=True, minwidth=10, width=15)
        self.tree.column('#4', stretch=True, minwidth=50, width=75)
        self.tree.column('#5', stretch=True, minwidth=50, width=75)
        self.tree.column('#6', stretch=True, minwidth=10, width=10)
        self.tree.column('#7', stretch=True, minwidth=40, width=50)
        self.tree.column('#8', stretch=True, minwidth=50, width=70)
        self.tree.column('#9', stretch=True, minwidth=0, width=0)
        self.btn_text=StringVar()
        self.btnDuzenle=ttk.Button(frame, textvariable=self.btn_text,command=self.update).grid(row=12,column=0)
        self.btn_text.set("Düzenle")
        
        self.iptal=Button(frame, text='iptal',state = 'normal',command=self.iptal).grid(row=12,column=1)
        
        ttk.Button(frame, text='Sil', command=self.delete).grid(row=12,column=2)

        self.viewing_records()
   

    def treeinsert(self,sorgu):
        records = self.tree.get_children()
        for element in records:
            self.tree.delete(element)
        #sorgu='select blood_type, blood_rh, count(blood_adet) from stokadet where blood_adet>0 group by blood_type, blood_rh;'
        rows=self.run(self,sorgu)
        print rows
        for i,item in enumerate(rows):
            item=['None' if v is None else v for v in item]
            item[6]=kantipleri[item[6]]
            self.tree.insert('','end',text=str(i),values=item)
    
    def ara(self):
        if(self.kanid.get()==0 and str(self.aratc.get())==""):
            messagebox.showinfo("uyari", "Arama yapabilmek için kan tipi ya da tc numarası giriniz.")
        else:
            if(self.secilen=='kanveren'):
                if(not str(self.aratc.get())==""):
                    sorgu="select d_name,d_surname,d_gender,d_address,d_email,h_id,kan_grubu,d_tc,d_phone from donor where d_tc="+str(self.aratc.get())
                    self.treeinsert(sorgu)
                else:
                    sorgu="select d_name,d_surname,d_gender,d_address,d_email,h_id,kan_grubu,d_tc,d_phone from donor where kan_grubu="+str(self.kanid.get())
                    self.treeinsert(sorgu)
            if(self.secilen=='hasta'):
                if(not str(self.aratc.get())==""):
                    sorgu="select p_name,p_surname,p_gender,p_address,p_email,h_id,kan_grubu,p_tc,p_phone from patient where p_tc="+str(self.aratc.get())
                    self.treeinsert(sorgu)
                else:
                    sorgu="select p_name,p_surname,p_gender,p_address,p_email,h_id,kan_grubu,p_tc,p_phone from patient where kan_grubu="+str(self.kanid.get())
                    self.treeinsert(sorgu)
            

    def adminpanelikapat(self):
        
        self.adminwind.destroy()

    def adminpaneli(self):
        self.adminwind=Toplevel()
        self.adminwind.title('Admin Paneli')
        #Label(self.adminwind, text='Admin Paneli').grid(row=0, column=0)
        frameAdmin = LabelFrame(self.adminwind, text='Admin Paneli')
        frameAdmin.grid(row=0,column=0)
        Label(frameAdmin, text='Kullanici Adi:').grid(row=1, column=0)
        self.username= Entry(frameAdmin)
        self.username.grid(row=1, column=1)

        Label(frameAdmin, text='Şifre:').grid(row=2, column=0)
        self.password= Entry(frameAdmin)
        self.password.grid(row=2, column=1)
        Label(frameAdmin, text='Email:').grid(row=3, column=0)
        self.adminmail= Entry(frameAdmin)
        self.adminmail.grid(row=3, column=1)
        Label(frameAdmin, text='Adres:').grid(row=4, column=0)
        self.adminadres= Entry(frameAdmin)
        self.adminadres.grid(row=4, column=1)
        self.varc = StringVar()
        #self.varc.set('')
        self.varr = StringVar()
        #self.varc.set('')
        self.varu = StringVar()
        #self.varc.set('')
        self.vard = StringVar()
        #self.varc.set('')
        self.varrole = IntVar()
        admin = Radiobutton(frameAdmin, text="Admin", variable=self.varrole, value=1)
        admin.grid(row=0, column=0)

        personel = Radiobutton(frameAdmin, text="Personel", variable=self.varrole, value=2)
        personel.grid(row=0, column=1)
        R1 = Checkbutton(frameAdmin, text = "C", variable = self.varc, \
                 onvalue = 'C', offvalue = "", height=1, \
                 width = 1, command=self.sel)
        R1.grid(row=1, column=2)

        R2 = Checkbutton(frameAdmin, text = "R", variable = self.varr, \
                 onvalue = "R", offvalue = "", height=1, \
                 width = 1, command=self.sel)
        R2.grid(row=2, column=2)

        R3 = Checkbutton(frameAdmin, text = "U", variable = self.varu, \
                 onvalue = "U", offvalue = "", height=1, \
                 width = 1, command=self.sel)
        R3.grid(row=3, column=2)
        R4 = Checkbutton(frameAdmin, text = "D", variable = self.vard, \
                 onvalue = "D", offvalue = "", height=1, \
                 width = 1, command=self.sel)
        R4.grid(row=4, column=2)
        #------------------------Table---------------------------------
        

        self.treeAdmin=ttk.Treeview(frameAdmin,height=5,columns=("index","id","Username", "Password", "Email","Adres"))
      
        self.treeAdmin.grid(row=6,column=0,columnspan=3)
        self.treeAdmin.heading('#0', text='#', anchor=W)
        self.treeAdmin.heading('#1', text='id', anchor=W)
        self.treeAdmin.heading('#2', text='Kullanici Adi', anchor=W)
        self.treeAdmin.heading('#3', text='Sifre', anchor=W)
        self.treeAdmin.heading('#4', text='Email', anchor=W)
        self.treeAdmin.heading('#5', text='Adres', anchor=W)
        self.treeAdmin.column('#0', stretch=False, minwidth=0, width=0)
        self.treeAdmin.column('#1', stretch=False, minwidth=50, width=50)
        self.treeAdmin.column('#2', stretch=False, minwidth=70, width=80)
        self.treeAdmin.column('#3', stretch=False, minwidth=70, width=80)
        self.treeAdmin.column('#4', stretch=False, minwidth=60, width=60)
        self.treeAdmin.column('#5', stretch=False, minwidth=70, width=80)
        self.treeAdmin.column('#6', stretch=False, minwidth=0, width=0)
        
        
        ttk.Button(frameAdmin, text='Güncelle',command=self.adminguncelle).grid(row=7,column=0)
        ttk.Button(frameAdmin, text='Ekle',command=self.adminekle).grid(row=7,column=1)
        ttk.Button(frameAdmin, text='Sil',command=self.adminsil).grid(row=7,column=2)
        self.uyari=Label(frameAdmin,text='',fg='red')
        self.uyari.grid(row=8,column=1)
        self.admin_viewing_records()
        ttk.Button(self.adminwind, text='Kapat!',command=self.adminpanelikapat).grid(row=5,column=0)
        self.adminwind.mainloop()
    def kanverkapat(self):
        
        km=str(self.kanmiktar.get())
        self.donatedwind.destroy()
        self.kanmsj['text']=''
        kantipi=self.tree.item(self.tree.selection())['values'][6]
        kantipi=kantipleri.index(kantipi)
        print "************************************"
        print kantipi
        sorgustockid="select stock_id from stock where blood_id="+str(kantipi)+" and blood_adet>0"
        #messagebox.showinfo("uyari", str(self.kanmiktar.get()))
        a=self.run(self,sorgustockid)
        if(not(str(a)=="[]")):
            sorgu="insert into donated (patient_tc,donated_date,blood_id,blood_adet,stock_id) values("+str(self.tc)+",'"+str(self.zaman)+"',"+str(kantipi)+","+km+","+str(a[0][0])+")"
            self.run(self,sorgu)
        else:
            messagebox.showinfo("uyari", "Verilecek kan bulanamadi. :(")
        self.kanadetviewing()
    def kanver(self):
        try:
            self.tc=self.tree.item(self.tree.selection())['values'][7]
            
        except IndexError as e:
            self.kanmsj['text']='Lutfen secim yapınız.'
            return
        self.kanmsj['text']=str(self.tc)+" kişiye kan verilecek"
        self.donatedwind=Toplevel()
        self.donatedwind.title('Kan Bagısı Gir.')
        self.zaman=time.strftime("%Y-%m-%d")
        
        Label(self.donatedwind,text="Kan Adeti Yazın!",fg='red').grid(row=0,column=0)
        self.kanmiktar = Entry(self.donatedwind)
        self.kanmiktar.grid(row=1, column=0)
        Label(self.donatedwind,text=self.zaman,fg='red').grid(row=2,column=0)
        Label(self.donatedwind,text=self.tc,fg='red').grid(row=3,column=0)
        ttk.Button(self.donatedwind, text='Tamam',command=self.kanverkapat).grid(row=3,column=1)
        self.donatedwind.mainloop()

    def kanalkapat(self):
        
        km=str(self.kanmiktar.get())
        self.donatedwind.destroy()
        self.kanmsj['text']=''
        kantipi=self.tree.item(self.tree.selection())['values'][6]
        kantipi=kantipleri.index(kantipi)
        print "************************************"
        print kantipi
        sorgu="insert into donate (donor_tc,donate_date,donor_blood_id,blood_miktar) values("+str(self.tc)+",'"+str(self.zaman)+"',"+str(kantipi)+","+str(km)+")"
        self.run(self,sorgu)
        self.kanadetviewing()
    def kanal(self):
        try:
            self.tc=self.tree.item(self.tree.selection())['values'][7]
            print self.tc
        except IndexError as e:
            self.kanmsj['text']='Lutfen secim yapınız.'
            return
        self.kanmsj['text']=str(self.tc)+" kişiye kan verecek"
        self.donatedwind=Toplevel()
        self.donatedwind.title('Kan Miktarı Gir.')
        self.zaman=time.strftime("%Y-%m-%d")
        
        Label(self.donatedwind,text="Kan Adeti Yazın!",fg='red').grid(row=0,column=0)
        self.kanmiktar = Entry(self.donatedwind)
        self.kanmiktar.grid(row=1, column=0)
        Label(self.donatedwind,text=self.zaman,fg='red').grid(row=2,column=0)
        Label(self.donatedwind,text=self.tc,fg='red').grid(row=3,column=0)
        ttk.Button(self.donatedwind, text='Tamam',command=self.kanalkapat).grid(row=3,column=1)
        self.donatedwind.mainloop()
    def adminsil(self):
        try:
            kid=self.treeAdmin.item(self.treeAdmin.selection())['values'][0]
            print kid
            sorgusil="delete from user1 where user_id ="+str(kid)
            result = messagebox.askquestion("Sil", "Emin Misin ?", icon='warning')
            if result == 'yes':
                self.run(self,sorgusil)
                self.uyari['text']=str(kid)+" id li kullanici silindi."
                self.admin_viewing_records()
            else:
                self.uyari['text']='Silme iptal edildi.'
        except:
            self.uyari['text']="lütfen bir kullanici secin!"
    def roleset(self,rol):
        if(rol.find('Admin')>-1):
            self.varrole.set(1)
        if(rol.find('User')>-1):
            self.varrole.set(2)
    def crudset(self,crud):
        if(crud.find('C')>-1):
            self.varc.set('C')
        if(crud.find('R')>-1):
            self.varr.set('R')
        if(crud.find('U')>-1):
            self.varu.set('U')
        if(crud.find('D')>-1):
            self.vard.set('D')
    def adminguncelle(self):
        self.admintemizle();
        self.varc.set('')
        self.varr.set('')
        self.varu.set('')
        self.vard.set('')
        try:
            val=self.treeAdmin.item(self.treeAdmin.selection())['values']
        except IndexError as e:
            self.message['text']='Lutfen secim yapınız.'
            return
        if(not (self.username.get() and self.password.get() and self.adminmail.get()  and self.adminadres.get())):
            self.username.insert(0,str(val[1]))
            self.password.insert(0,str(val[2]))
            self.adminmail.insert(0,str(val[3]))
            self.adminadres.insert(0,str(val[4]))
            a=self.crudget(val[0])
            print "******************split********************"
            print a
            self.crudset(a)
            b=self.roleget(val[0])
            self.roleset(b)

            print "******************split********************"
        else:
            kid=self.treeAdmin.item(self.treeAdmin.selection())['values'][0]
            sorgu="update user1 (username,password,email,user_address)=('"+str(self.username.get())+"','"+str(self.password.get())+"','"+str(self.adminmail.get())+"','"+str(self.adminadres.get())+"') where user_id="+str(kid)
            self.run(self,sorgu)
            self.admin_viewing_records()
    def adminekle(self):
        #burası saçma olabilir mazur görün
        sorgu="insert into user1(username, password,email,user_address) values('"+self.username.get()+"','"+self.password.get()+"','"+self.adminmail.get()+"','"+self.adminadres.get()+"');"
        eklenenid="select user_id from user1 order by user_id desc limit 1"
        pername=str(self.varc.get()) +"," +str(self.varr.get()) +","+ str(self.varu.get()) +","+str(self.vard.get())
        persorgu="insert into permission(per_name) values ('"+pername+"');"
        print "-------"
        print persorgu
        perid="select per_id from permission order by per_id desc limit 1"
        a=self.run(self,sorgu)
        user_id=self.run(self,eklenenid)
        print user_id[0][0]
        self.run(self,persorgu)
        pid=self.run(self,perid)
        print pid[0][0]
        sorgu2="insert into have(user_id,per_id) values ("+str(user_id[0][0])+","+str(pid[0][0])+")"
        self.run(self,sorgu2)
        
        #self.admintemizle()
        self.admin_viewing_records()
    def admintemizle(self):
        self.username.delete(0,END)
        self.password.delete(0,END)
        self.adminmail.delete(0,END)
        self.adminadres.delete(0,END)
    def admin_viewing_records(self):
        records = self.treeAdmin.get_children()
        for element in records:
            self.treeAdmin.delete(element)
        sorgu='select * from user1'
        rows=self.run(self,sorgu)
        print rows
        for i,item in enumerate(rows):
            item=['None' if v is None else v for v in item]
            self.treeAdmin.insert('','end',text=str(i),values=item)
    def roleget(self,id):
        sorgu="select role_name from roller where user_id="+str(id)
        try:
            a= self.run(self,sorgu)
            return a[0][0]
        except:
            messagebox.showinfo("Zararli Hata!", "kullanicinin rolu yok")
            self.varrole.set(0)

    def crudget(self,id):
        sorgu="select per_name from izinler where user_id="+str(id)
        try:
            a=self.run(self,sorgu)
            return a[0][0]
        except:
            messagebox.showinfo("Zararli Hata!", "kullanicinin bir c,r,u,d izni yok!")
    def role(self,userid):
        sorgu='select role_id from has where user_id='+str(userid)
        try:
            a=self.run(self,sorgu)
            sorgu2="select per_id from have where user_id="+str(a[0][0])
            a=self.run(self,sorgu2)
            return a[0][0]
        except:
            print "has hata!"

    def izin(self,id):
        sorgu="select per_name from permission where per_id="+str(id)
        try:
            a=self.run(self,sorgu)
            return a[0][0]
            print a[0][0]
        except:
            print "izin hata!"

    def kanadetviewing(self):
        records = self.kantree.get_children()
        for element in records:
            self.kantree.delete(element)
        #sorgu='select blood_type, blood_rh, count(blood_adet) from stokadet where blood_adet>0 group by blood_type, blood_rh;'
        sorgu="select * from stokadet"
        rows=self.run(self,sorgu)
        print rows
        for i,item in enumerate(rows):
            item=['None' if v is None else v for v in item]
            self.kantree.insert('','end',text=str(i),values=item)
    def sel(self):
        print self.varc.get()
        print self.varr.get()
        print self.varu.get()
        print self.vard.get()

        
    @staticmethod
    def run(self, sorgu):
        try:
            con = psycopg2.connect("host='localhost' dbname='blood' user='postgres' password='blabla'")
            con.set_client_encoding('UTF8')
            cur = con.cursor()
            cur.execute(sorgu)
            con.commit()
            #global col_names
            #col_names = [i[0] for i in cur.description]
            #for n, name in enumerate(col_names):
            #    print name
            #    self.tree.heading('#'+str(i), text=str(name), anchor=W)
            #    self.tree.column('#'+str(i), stretch=True, minwidth=80, width=85)
            while True:
                row = cur.fetchall()
 
                if row == None:
                    break
 
                print(row)
                
                return list(row)
 
        except psycopg2.DatabaseError, e:
            if con:
                con.rollback()
 
            print 'Error %s' % e
            self.message['text']=e
            #sys.exit(1)
 
        finally:   
            if con:
                con.close()
        
    def fcinsiyet(self,value):
        global gnd
        if(value=="Erkek"):
            gnd="e"
        if(value=="Kadin"):
            gnd="k"

    def table(self,value):
        if(value==""):
            print secilen
            self.viewing_records()
            
        else:
            self.secilen=value
            print value
            #self.kanal['state']='normal'
            self.viewing_records()
        

    
        
    def temizle(self):
        self.name.delete(0,END)
        self.yname.delete(0,END)
        self.surname.delete(0,END)
        self.ysurname.delete(0,END)
        self.var2.set('')
        self.mail.delete(0,END)
        self.adres.delete(0,END)
        self.yadres.delete(0,END)
        self.tel.delete(0,END)
        self.ytel.delete(0,END)
        self.tc.delete(0,END)
        self.ytc.delete(0,END)
        self.kanid.set(0)

    def iptal(self):
        self.temizle()
        self.btn_text.set('Düzenle')
        self.iptal['state']='DISABLED'


    def viewing_records(self):
        
        records = self.tree.get_children()
        for element in records:
            self.tree.delete(element)
        if(self.secilen=='kanveren'):
            sorgu='select d_name,d_surname,d_gender,d_address,d_email,h_id,kan_grubu,d_tc,d_phone from donor'
            rows=self.run(self,sorgu)
            #print rows
            for i,item in enumerate(rows):
                item=['None' if v is None else v for v in item]
                item[6]=kantipleri[item[6]]
                self.tree.insert('','end',text=str(i),values=item)
        elif(self.secilen=='hasta'):
            sorgu='select p_name,p_surname,p_gender,p_address,p_email,h_id,kan_grubu,p_tc,p_phone from patient'
            rows=self.run(self,sorgu)
            #print rows
            for i,item in enumerate(rows):
                item=['None' if v is None else v for v in item]
                print "88888888888888888888888888888888888888"
                item[6]=kantipleri[item[6]]
                print item
                print "88888888888888888888888888888888888888"
                self.tree.insert('','end',text=str(i),values=item)
        self.kanadetviewing()

    def add(self):
        yakinEklenmisMi=False
        if(str(self.yname.get()) and str(self.ysurname.get()) and str(self.ytc.get())):
            sorguyk="insert into dfriend(d_f_name, d_f_surname,d_f_tc,d_f_phone,d_f_address) values('"+self.yname.get()+"','"+self.ysurname.get()+"',"+self.ytc.get()+","+self.ytel.get()+",'"+self.yadres.get()+"')"
            sorguyh="insert into pfriend(pf_name, pf_surname,pf_tc,pf_phone,pf_address) values('"+self.yname.get()+"','"+self.ysurname.get()+"',"+self.ytc.get()+","+self.ytel.get()+",'"+self.yadres.get()+"')"
            iliskisql="INSERT INTO \"PFRelative\" VALUES("+str(self.tc.get())+","+str(self.ytc.get())+");"
            iliskisql2="INSERT INTO \"DFRelative\" VALUES("+str(self.tc.get())+","+str(self.ytc.get())+");"
            yakinEklenmisMi=True

        if(self.secilen=='kanveren'):
            #parametre=(self.name.get(),self.surname.get(),self.gender.get(),self.mail.get(),self.adres.get(), int(self.tel.get()),long(self.tc.get()),1,int(self.kan.get()))
            sorgu="insert into donor values('"+self.name.get()+"','"+self.surname.get()+"','"+gnd+"', '"+self.mail.get()+"', '"+self.adres.get()+"', "+str(self.tel.get())+", "+str(self.tc.get())+", 1, "+str(self.kanid.get())+");"
            #print sorgu
            #parametre=(self.name.get(),self.surname.get(),self.gender.get(),self.mail.get(),self.adres.get(), int(self.tel.get()),long(self.tc.get()),1,int(self.kan.get()))
            self.run(self,sorgu)
            if yakinEklenmisMi:
                self.run(self,sorguyk)
                self.run(self,iliskisql2)
            self.temizle()
            self.viewing_records()
        elif(self.secilen=='hasta'):
            print "????????????????????????????????????????????????????????"
            sorguhasta="insert into patient values("+str(self.tel.get())+",'"+self.name.get()+"','"+self.surname.get()+"', '"+gnd+"', '"+self.adres.get()+"', '"+self.mail.get()+"', 1, "+str(self.tc.get())+", "+str(self.kanid.get())+");"
            print sorguhasta
            self.run(self,sorguhasta)
            if yakinEklenmisMi:

                print yakinEklenmisMi
                print sorguyh
                print iliskisql

                self.run(self,sorguyh)
                self.run(self,iliskisql)
            self.temizle()
            self.viewing_records()

    def delete(self):
        try:
            print self.tree.item(self.tree.selection())['values'][6]
        except IndexError as e:
            self.message['text']='Lutfen secim yapınız.'
            return
        self.message['text']=''
        
        if(self.secilen=='kanveren'):
            tc=self.tree.item(self.tree.selection())['values'][7]
            sorgu='DELETE FROM donor WHERE d_tc='+str(tc)
            sorgukanveren="delete from \"DFRelative\" where donor_tc="+str(tc)
            #sorgudfriend="delete from dfriend where d_f_tc="+
            self.run(self,sorgukanveren)
            self.run(self,sorgu)
            self.viewing_records()
        elif(self.secilen=='hasta'):
            print "hasta silme kodları yaz"
            tc=self.tree.item(self.tree.selection())['values'][7]
            sorgu='DELETE FROM patient WHERE p_tc='+str(tc)
            sorguhasta="delete from \"PFRelative\" where patient_tc="+str(tc)
            self.run(self,sorguhasta)
            self.run(self,sorgu)
            self.viewing_records()



    def update(self):
        self.message['text']=''
        try:
            print self.tree.item(self.tree.selection())['values'][6]
        except IndexError as e:
            self.message['text']='Lutfen secim yapınız.'
            return
        val=self.tree.item(self.tree.selection())['values']
        print val
        if(not (self.name.get() and self.surname.get() and gnd and self.mail.get()  and self.adres.get())):
            if(self.secilen=='hasta'):
                
                try:

                    hastayakinibul="select p_frient_tc from \"PFRelative\" where patient_tc="+str(val[7])
                    hastayakinibul=self.run(self,hastayakinibul)
                    pftc=hastayakinibul[0][0]
                    print "true yapildi....................."
                    print pftc
                    #raw_input('pftc.................')
                    hastabilgi="select * from pfriend where pf_tc="+str(pftc)
                    hb=self.run(self,hastabilgi)
                    print hb
                    #----Hasta ekrana basma
                    self.yname.insert(0,str(hb[0][0]))
                    self.ysurname.insert(0,str(hb[0][2]))
                    self.ytc.insert(0,str(hb[0][1]))
                    self.ytel.insert(0,str(hb[0][3]))
                    self.yadres.insert(0,str(hb[0][4]))
                except:
                    print "hastayakinibulunamadi."


                self.name.insert(0,val[0])
                self.surname.insert(0,val[1])
                if val[2]=='e':
                    self.var2.set('Erkek')
                else:
                    self.var2.set('Kadin')
                self.mail.insert(0,str(val[4]))
                self.adres.insert(0,val[3])
                self.tel.insert(0,str(val[8]))
                self.tc.insert(0,str(val[7]))
                self.kanid.set(kantipleri.index(val[6]))
                #self.kan.insert(0,val[8])
                self.btn_text.set('Düzenlemeyi Kaydet')
                print self.iptal
                self.iptal['state'] = 'normal'
            elif(self.secilen=='kanveren'):
                self.name.insert(0,val[0])
                self.surname.insert(0,val[1])
                if val[2]=='e':
                    self.var2.set('Erkek')
                else:
                    self.var2.set('Kadin')
                self.mail.insert(0,str(val[4]))
                self.adres.insert(0,str(val[3]))
                self.tel.insert(0,str(val[8]))
                self.tc.insert(0,str(val[7]))
                #self.kan.insert(0,val[8])
                self.kanid.set(kantipleri.index(val[6]))

                #hasta yakini kutucuk doldurma
                try:

                    hastayakinibul="select d_friend_tc from \"DFRelative\" where donor_tc="+str(val[7])
                    hastayakinibul=self.run(self,hastayakinibul)
                    dftc=hastayakinibul[0][0]
                    print "true yapildi....................."
                    print dftc
                    #raw_input('dftc.................')
                    hastabilgi="select * from dfriend where d_f_tc="+str(dftc)
                    hb=self.run(self,hastabilgi)
                    print hb
                    #----Hasta ekrana basma
                    self.yname.insert(0,str(hb[0][0]))
                    self.ysurname.insert(0,str(hb[0][4]))
                    self.ytc.insert(0,str(hb[0][1]))
                    self.ytel.insert(0,str(hb[0][2]))
                    self.yadres.insert(0,str(hb[0][3]))
                except:
                    print "...."
               

                self.btn_text.set('Düzenlemeyi Kaydet')
                print self.iptal
                #self.iptal['state'] = 'normal'
        else:
            if(self.secilen=='kanveren'):
                sorgu="update donor set (d_name,d_surname,d_gender,d_email,d_address,d_phone,d_tc,h_id,kan_grubu) =('"+self.name.get()+"','"+self.surname.get()+"','"+gnd+"','"+self.mail.get()+"','"+self.adres.get()+"',"+self.tel.get()+","+self.tc.get()+",1,"+str(self.kanid.get())+") where d_tc="+str(self.tc.get())+";"
                sorgudfriend="update dfriend set (d_f_name,d_f_surname,d_f_tc,d_f_phone,d_f_address)=('"+self.yname.get()+"','"+self.ysurname.get()+"','"+self.ytc.get()+"',"+self.ytel.get()+",'"+self.yadres.get()+"') where d_f_tc="+str(self.ytc.get())
                print gnd
                self.run(self,sorgu)
                try:
                    sorguyk="insert into dfriend(d_f_name, d_f_surname,d_f_tc,d_f_phone,d_f_address) values('"+self.yname.get()+"','"+self.ysurname.get()+"',"+self.ytc.get()+","+self.ytel.get()+",'"+self.yadres.get()+"')"
                    self.run(self,sorguyk)
                    iliskisql2="INSERT INTO \"DFRelative\" VALUES("+str(self.tc.get())+","+str(self.ytc.get())+");"
                    self.run(self,iliskisql2)
                except:
                    print "zaten var."
                self.run(self,sorgudfriend)#hasta yakini update
                self.viewing_records()
                self.btn_text.set('Düzenle')
                self.message['text']='Basarili'
                self.temizle()
            elif(self.secilen=='hasta'):
                print "hasta update kodları yaz"
                print gnd
                sorguhu="update patient set (p_name,p_surname,p_gender,p_email,p_address,p_phone,p_tc,h_id,kan_grubu) =('"+self.name.get()+"','"+self.surname.get()+"','"+gnd+"','"+self.mail.get()+"','"+self.adres.get()+"',"+self.tel.get()+","+str(self.tc.get())+",1,"+str(self.kanid.get())+") where p_tc="+str(self.tc.get())+";"
                sorgupfriend="update pfriend set (pf_name,pf_surname,pf_tc,pf_phone,pf_address)=('"+self.yname.get()+"','"+self.ysurname.get()+"','"+self.ytc.get()+"',"+self.ytel.get()+",'"+self.yadres.get()+"') where pf_tc="+str(self.ytc.get())
                #print sorgupfriend
                print "++++++++++++++++++++++++++++++++++++++"
                self.run(self,sorguhu)
                try:

                    sorguyh="insert into pfriend(pf_name, pf_surname,pf_tc,pf_phone,pf_address) values('"+self.yname.get()+"','"+self.ysurname.get()+"',"+self.ytc.get()+","+self.ytel.get()+",'"+self.yadres.get()+"')"
                    self.run(self,sorguyh)
                    iliskisql="INSERT INTO \"PFRelative\" VALUES("+str(self.tc.get())+","+str(self.ytc.get())+");"
                    self.run(self,iliskisql)
                except:
                    print "zaten var"
                self.run(self,sorgupfriend)
                self.viewing_records()
                self.btn_text.set('Düzenle')
                self.message['text']='Basarili'
                self.temizle()
        
class login:
    global skan
    skan=Kan
    def __init__(self,window):
        self.window=window
        self.username="m"
        self.window.resizable(width=FALSE, height=FALSE)
        self.window.title("Log-In")
        self.window.geometry("200x150")
        #Creating the username & password entry boxes
        self.username_text = Label(window, text="Username:")
        self.username_guess = Entry(window)
        self.password_text = Label(window, text="Password:")
        self.password_guess = Entry(window, show="*")

        #attempt to login button
        self.attempt_login = Button(text="Login", command=self.giris)

        self.username_text.pack()
        self.username_guess.pack()
        self.password_text.pack()
        self.password_guess.pack()
        self.attempt_login.pack()
        #Main Starter
        #window.mainloop()
    def anaekran(self):
        messagebox.showinfo("-- COMPLETE --", "You Have Now Logged In.", icon="info")
        self.window.destroy()
        wind=Tk()
        #wind.attributes('-zoomed',True)
        w, h = wind.winfo_screenwidth(), wind.winfo_screenheight()
        wind.geometry("%dx%d+0+0" % (w/2, h-70))
        #wind.geometry('800x800')
        style = ttk.Style(wind)
        f=Font(family='Arial',size=10, weight=BOLD)
        style.configure('Treeview', rowwidth=15,font=f)
        application = Kan(wind)
        wind.mainloop()

    
    

    
    def giris(self):
        
        print "Kan Bagisi Giris Ekrani"
        kadi=self.username_guess.get()#raw_input('Kullanici Adi')
        ksifre=self.password_guess.get()#raw_input('Sifre')
        print kadi
        print ksifre
        sorgu="select user_id from user1 u where u.username='"+str(kadi)+"' and u.password='"+str(ksifre)+"'"
        try:
            a=skan.run(self,sorgu)
            print a
            if(str(a)=='[]'):
                return
        except:
            print "hata!"
        print "hello "+str(kadi)
        #print "id:"+str(a[0][0])
        #rolu=self.role(a[0][0])
        #crud=self.izin(rolu)
        #print crud
        self.anaekran()
        
    
    def role(self,userid):
        sorgu='select role_id from has where user_id='+str(userid)
        try:
            a=skan.run(self,sorgu)
            #print a[0]
            global sorgu2
            sorgu2="select per_id from have where role_id="+str(a[0][0])
        except:
            print "has hata!"

        
        try:
            a=skan.run(self,sorgu2)
            #print a[0]
            return a[0][0]
        except:
            print "role!"
        
    
    def izin(self,id):
        sorgu="select per_name from permission where per_id="+str(id)
        try:
            a=skan.run(self,sorgu)
            return a[0][0]
            print a[0][0]
        except:
            print "izin hata!"

"""
wind=Tk()
    wind.geometry('400x200')
    style = ttk.Style(wind)
    f=Font(family='Arial',size=10, weight=BOLD)
    style.configure('Treeview', rowwidth=5,font=f)
    application = Kan(wind)
    wind.mainloop()


"""

if __name__=='__main__':
    wind=Tk()
    application = login(wind)
    wind.mainloop()
