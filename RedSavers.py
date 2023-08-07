from pathlib import Path
from tkinter import *
from tkinter import Tk, Canvas, Entry, Text, Button, PhotoImage, ttk
from os.path import dirname
import tkinter.messagebox as messageBox
import mysql.connector as mysql
from datetime import datetime
from matplotlib import pyplot as plt

       #Variable Declaration

OUTPUT_PATH = dirname(__file__)
OUTPUT_PATH+= r'\RedSavers_test\assets\frame0'     #Variable Declaration
ASSETS_PATH = OUTPUT_PATH 
BG_options = ["A+","A-","B+","B-","AB+","AB-","O+","O-"] #Blood_Group Options
colors =['darkcyan','darkturquoise','paleturquoise','royalblue','aqua','steelblue','lightblue','cornflowerblue','aquamarine','seagreen']

def relative_to_assets(path: str) -> Path:  #Path Manager
    return ASSETS_PATH / Path(path)

#================================================ FUNCTIONS =======================================================#
            #-------     Insertion and Reading       ------#
def insert():
    DBG = entry_DonorBG.get()
    Dname = entry_DonorName.get()
    Dphone = entry_DonorContact.get()
    Dadd = entry_DonorAdd.get()

    if(DBG =="" or DBG =="Select Blood Group" or Dname== "" or Dphone== "" or Dadd== ""):
        messageBox.showinfo("Insert Status", "All Fields are required")
    else:
        con = mysql.connect(host="localhost", user="root", password="", database = "redsavers")
        cursor = con.cursor()
        try:
            cursor.execute("INSERT INTO `donor` VALUES(NULL,'"+DBG+"','"+Dname+"','"+Dphone+"',\""+Dadd+"\")")
            con.commit()
            con.close()
        except:messageBox.showerror("Donor Registration Status", "'Blood Group' inputted not registered. Input registered 'Blood Group' only.")
        else: messageBox.showinfo("Donor Registration Status", "Donor Registered Successfully")
        
def Donorread():
    columns = ("Donor ID", "Blood Group","Donor Name","Donor Phone","Donor Address")
    table.delete(*table.get_children())
    for i in range(1,8):table.heading(i,text ="")
    for i in range(1,6):table.heading(i,text =columns[i-1])
    con = mysql.connect(host="localhost", user="root", password="", database = "redsavers")
    cursor = con.cursor()
    cursor.execute("SELECT * FROM `donor`")
    data = cursor.fetchall()
    for i,(did, bg,dn,dp,da) in enumerate(data,1):
        table.insert("","end",values=(did, bg, dn, dp, da))
    con.close()
   
def Invinsert():
    InvDID = entry_InventoryDonorID.get()
    InvBag = entry_InventoryBagC.get()
    DT = datetime.now()
    Date = DT.strftime("%b-%d-%y")
    Time = DT.strftime("%I:%M %p")

    if(InvDID == "" or InvBag == ""):
        messageBox.showinfo("Insert Status", "All Fields are required")
    elif InvBag.isdigit() == False:
        messageBox.showerror("Insert Status", "'Bag Count' should only contain whole numbers")
    else:
        con = mysql.connect(host="localhost", user="root", password="", database = "redsavers")
        cursor = con.cursor()
        try:
            cursor.execute("INSERT INTO `inventory` VALUES(NULL,'"+InvDID+"','"+Date+"','"+Time+"','"+InvBag+"','"+InvBag+"')")
            con.commit()
            cursor.execute("SELECT `Blood Group` FROM `donor` WHERE `Donor ID` = "+InvDID)
            Bg = cursor.fetchall()
            cursor.execute("UPDATE `stocks` SET `Overall Bag Count` = `Overall Bag Count` + '"+InvBag+"' WHERE `Blood Group` = '"+Bg[0][0]+"'")
            con.commit()
            con.close()
        except:
            messageBox.showerror("ERROR Status", "Inputted 'Donor ID' not registered. Input registered 'Donor ID' only.")
        else:
            messageBox.showinfo("Donation Status", "Donation Recorded Successfully")

def Invread():
    columns = ("Donation ID", "Donor ID","Donation Date","Donation Time","Bags Donated","Stock")
    for i in range(1,8):table.heading(i,text ="")
    table.delete(*table.get_children())
    for i in range(1,7):table.heading(i,text =columns[i-1])
    con = mysql.connect(host="localhost", user="root", password="", database = "redsavers")
    cursor = con.cursor()
    cursor.execute("SELECT * FROM `inventory`")
    data = cursor.fetchall()
    for i,(di,did, dd,dt,bd,s) in enumerate(data,1):
        table.insert("","end",values=(di,did,dd,dt,bd,s))
    con.close()

def Patientinsert():
    PatBG = entry_PatientBG.get()
    PatName = entry_PatientName.get()
    PatPhone = entry_PatientCont.get()
    PatAdd = entry_PatientAdd.get()

    if(PatBG == "" or PatBG == "Select Blood Group" or PatName == "" or PatPhone == "" or PatAdd == ""):
        messageBox.showinfo("Insert Status", "All Fields are required")
    else:
        con = mysql.connect(host="localhost", user="root", password="", database = "redsavers")
        cursor = con.cursor()
        try:
            cursor.execute("INSERT INTO `patient` VALUES(NULL,'"+PatBG+"','"+PatName+"','"+PatPhone+"',\""+PatAdd+"\")")
            con.commit()
            con.close()
        except:messageBox.showerror("Patient Registration Status", "'Blood Group' inputted not registered. Input registered 'Blood Group' only.")
        else: messageBox.showinfo("Patient Registration Status", "Patient Registered Successfully")

def Patread():
    columns = ("Patient ID", "Blood Group","Patient Name","Patient Phone","Patient Address")
    for i in range(1,8):table.heading(i,text ="")
    table.delete(*table.get_children())
    for i in range(1,6):table.heading(i,text =columns[i-1])
    con = mysql.connect(host="localhost", user="root", password="", database = "redsavers")
    cursor = con.cursor()
    cursor.execute("SELECT * FROM `patient`")
    data = cursor.fetchall()
    for i,(pid,bg,pn,pp,pa) in enumerate(data,1):
        table.insert("","end",values=(pid,bg,pn,pp,pa))
    con.close()

def Transinsert():
    PatientID = entry_TransPatientID.get()
    Hospital = entry_TransHos.get()
    Bags = entry_TransBagC.get()

    if Hospital =="" or Bags == "" or PatientID == "":
        messageBox.showinfo("Insert Status", "All Fields are required")
    elif Bags.isdigit() == False:
        messageBox.showerror("ERROR Status", "'Bag Count' should only contain whole numbers")
    else:
        con = mysql.connect(host="localhost", user="root", password="", database = "redsavers")
        cursor = con.cursor()
        cursor.execute("SELECT * FROM `patient` WHERE `Patient ID` ='"+PatientID+"'")   
        PatExist = cursor.fetchall()
        
        if len(PatExist) == 0 :
            messageBox.showerror("ERROR Status", "Inputted `Patient ID` is not registered")
        else:
            cursor.execute("SELECT `Blood Group` FROM `patient` WHERE `Patient ID` ='"+PatientID+"'")   
            PBG = cursor.fetchall()
            cursor.execute("SELECT `Overall Bag Count` FROM `stocks` WHERE `Blood Group` ='"+PBG[0][0]+"'")   
            stock = cursor.fetchall()
            ostock = int(stock[0][0])
            uncollectedBags= int(Bags)
            if  ostock >= uncollectedBags:
                cursor.execute("SELECT `inventory`.`Donation ID` FROM `inventory` INNER JOIN `donor` ON `donor`.`Donor ID` = `inventory`.`Donor ID` AND `donor`.`Blood Group` = '"+PBG[0][0]+"' AND `inventory`.`Stock` > '0'")   
                DonIDs = cursor.fetchall()
                i = 0
                while uncollectedBags > 0:
                    DT = datetime.now()
                    Date = DT.strftime("%b-%d-%y")
                    Time = DT.strftime("%I:%M %p")
                    cursor.execute("SELECT `Stock`,`Donor ID` FROM `inventory` WHERE `Donation ID` ='"+str(DonIDs[i][0])+"'")   
                    temp = cursor.fetchall()
                    StockPerRec = int(temp[0][0])
                    DonorID = str(temp[0][1])
                    if StockPerRec <= uncollectedBags:
                        uncollectedBags -= StockPerRec
                        cursor.execute("UPDATE `inventory` SET `Stock` = '0' WHERE `Donation ID` ='"+str(DonIDs[i][0])+"'")   
                        con.commit()
                        cursor.execute("INSERT INTO `transaction` VALUES(NULL,'"+PatientID+"','"+str(DonorID)+"','"+Date+"','"+Time+"',\""+Hospital+"\",'"+str(StockPerRec)+"')")
                        con.commit()
                    else:
                        StockPerRec -= uncollectedBags
                        cursor.execute("UPDATE `inventory` SET `Stock` = '"+str(StockPerRec)+"' WHERE `Donation ID` ='"+str(DonIDs[i][0])+"'")   
                        con.commit()
                        cursor.execute("INSERT INTO `transaction` VALUES(NULL,'"+PatientID+"','"+str(DonorID)+"','"+Date+"','"+Time+"',\""+Hospital+"\",'"+str(uncollectedBags)+"')")
                        con.commit()
                        uncollectedBags = 0
                    i+=1
                ostock -= int(Bags)
                cursor.execute("UPDATE `stocks` SET `Overall Bag Count` = '"+str(ostock)+"' WHERE `Blood Group` = '"+PBG[0][0]+"'")
                con.commit()
                messageBox.showinfo("Transaction Status", "Patient transaction Success!")
            else: 
                if ostock == 0: messageBox.showinfo("Stock Status", "Blood Group '"+PBG[0][0]+"' out of stock")
                else: messageBox.showinfo("Stock Status", "Not enough stock for Blood Group '"+PBG[0][0]+"'")
    con.close()

def Transread():
    columns = ("Transaction ID", "Patient ID", "Donor ID","Accept Date","Accept Time","Hospital","Bags Received")
    for i in range(1,8):table.heading(i,text ="")
    table.delete(*table.get_children())
    for i in range(1,8):table.heading(i,text =columns[i-1])
    con = mysql.connect(host="localhost", user="root", password="", database = "redsavers")
    cursor = con.cursor()
    cursor.execute("SELECT * FROM `transaction`")
    data = cursor.fetchall()
    for i,(tid,pid,did,ad,at,h,br) in enumerate(data,1):
        table.insert("","end",values=(tid,pid,did,ad,at,h,br))
    con.close()

def BGinsert():
    bg = entry_StocksBGAdd.get()

    if(bg == ""):
        messageBox.showinfo("Insert Status", "No Blood Group inputted")
    else:
        con = mysql.connect(host="localhost", user="root", password="", database = "redsavers")
        cursor = con.cursor()
        try:
            cursor.execute("INSERT INTO `stocks` VALUES('"+bg+"','0')")
            con.commit()
            con.close()
        except:messageBox.showerror("Blood Group Addition Status", "'Blood Group' already registered. Input unregistered 'Blood Group' to add")
        else: messageBox.showinfo("Blood Group Addition Status", "Blood Group Added Successfully")

def BGread():
    columns = ("Blood Group", "Overall Bag Count")
    for i in range(1,8):table.heading(i,text ="")
    table.delete(*table.get_children())
    for i in range(1,3):table.heading(i,text =columns[i-1])
    con = mysql.connect(host="localhost", user="root", password="", database = "redsavers")
    cursor = con.cursor()
    cursor.execute("SELECT * FROM `stocks`")
    data = cursor.fetchall()
    for i,(bg, obg) in enumerate(data,1):
        table.insert("","end",values=(bg, obg))
    con.close()


                #======      Deletion and Updation       ======#

def delete():
    DrId = entry_DonorID.get()
    if(DrId ==""):
        messageBox.showinfo("ERROR Status", "The 'Donor ID' field must not be empty")
    else:
        con = mysql.connect(host="localhost", user="root", password="", database = "redsavers")
        cursor = con.cursor()
        cursor.execute("SELECT * FROM `donor` WHERE `donor id` = "+DrId)
        cursor.fetchall()
        rwcnt = cursor.rowcount
        if rwcnt == 0:
            messageBox.showerror("ERROR Status", "Inputted 'Donor ID' not registered. Input registered 'Donor ID' only.")
            con.close()
            return
        else:
            cursor.execute("DELETE FROM donor WHERE `donor id` = "+DrId)
            con.commit()
            con.close()     
        messageBox.showinfo("Delete Status", "Record Deleted Successfully") 

def update():
    DrId = entry_DonorID.get()  #Gets needed PK

    if(DrId ==""):          #PK not inputted
        messageBox.showinfo("ERROR Status", "The 'Donor ID' field must not be empty")
    else:
        #-------------------------New Window Creation-------------------------------------------------
        top = Toplevel()
        l_Didtop = Label(top, text = "Donor ID", font =('bold', 10))    #Labels
        l_DBGtop = Label(top, text = "Blood Group", font =('bold', 10))  
        l_Dnametop = Label(top, text = "Donor Name", font =('bold', 10))
        l_Dphonetop = Label(top, text = "Phone no.", font =('bold', 10))
        l_Daddtop = Label(top, text = "Address", font =('bold', 10))

        e_Didtop = Entry(top)  #Textfields
        e_DBGtop = Entry(top)
        e_Dnametop = Entry(top)
        e_Dphonetop = Entry(top)
        e_Daddtop = Entry(top)    
        
        d_updatetop = Button(top, text="Update", font=("italic",10), bg="white", command = lambda: dbupdate(e_Didtop.get(),   #Update Button
        e_DBGtop.get(), e_Dnametop.get(),e_Dphonetop.get(),e_Daddtop.get(),DrId,top)) 

        #-------------------------Sql Database Connection-------------------------------------------------
        con = mysql.connect(host="localhost", user="root", password="", database = "redsavers")
        cursor = con.cursor()
        cursor.execute("SELECT * FROM donor WHERE `donor id` = "+DrId)   #Traverse Record
        cursor.fetchall()
        rwcnt = cursor.rowcount   
        con.close()
        if rwcnt == 0:    #PK doesnt exist
            top.destroy()
            messageBox.showerror("ERROR Status", "Inputted 'Donor ID' not registered. Input registered 'Donor ID' only.")
            return
        else:
            top.title('Update Donor Table')
            top.geometry('200x240')
            l_Didtop.pack()
            e_Didtop.pack()
            l_DBGtop.pack()
            e_DBGtop.pack()
            l_Dnametop.pack()
            e_Dnametop.pack()
            l_Dphonetop.pack()
            e_Dphonetop.pack()
            l_Daddtop.pack()
            e_Daddtop.pack()
            d_updatetop.pack()
            top.grab_set()

def dbupdate(Did, DBG, Dname, Dphone, Dadd,Drid,top):
    con = mysql.connect(host="localhost", user="root", password="", database = "redsavers")
    cursor1 = con.cursor()
    if Did != "":
        try:
            cursor1.execute("UPDATE `donor` SET `Donor ID`= "+ Did+" WHERE `Donor ID` = " + Drid)
        except Exception as e:
            messageBox.showerror("ERROR Status", "Inputted 'Donor ID' already registered. Please input unregistered 'Donor ID'")
            return
        else: 
            Drid = Did
    if DBG != "Select Blood Group" and  DBG != "":
        try:
            cursor1.execute("UPDATE `donor` SET `Blood Group`= '"+ DBG+"' WHERE `Donor ID` = " + Drid)
        except Exception as e:
            messageBox.showerror("ERROR Status", "Inputted 'Blood Group' not registered. Please input registered 'Blood Group' only")
            return
    if Dname != "":
        cursor1.execute("UPDATE `donor` SET `Donor Name`= '"+ Dname+"' WHERE `Donor ID` = " + Drid)
    if Dphone != "":
        cursor1.execute("UPDATE `donor` SET `Donor Phone`= '"+ Dphone+"' WHERE `Donor ID` = " + Drid)
    if Dadd != "":
        cursor1.execute("UPDATE `donor` SET `Donor Address`= \""+ Dadd+"\" WHERE `Donor ID` = " + Drid)
    messageBox.showinfo("Update Status", "Record Updated Successfully")
    con.commit()
    con.close() 
    top.destroy()

def Invdelete():
    DonID = entry_InventoryDtnID.get()
    if(DonID ==""):
        messageBox.showinfo("Delete Status", "No inputted 'Donation ID'")
    else:
        con = mysql.connect(host="localhost", user="root", password="", database = "redsavers")
        cursor = con.cursor()
        cursor.execute("SELECT * FROM `inventory` WHERE `Donation ID` = '"+DonID+"'")
        cursor.fetchall()
        rwcnt = cursor.rowcount
        if rwcnt == 0:
            messageBox.showerror("ERROR Status", "Inputted 'Donation ID' not registered. Input registered 'Donation ID' only.")
            con.close()
            return
        else:
            cursor.execute("DELETE FROM `inventory` WHERE `Donation ID` = '"+DonID+"'")
            con.commit()
            con.close()     
        messageBox.showinfo("Delete Status", "Record Deleted Successfully") 

def Invupdate():
    DonID= entry_InventoryDtnID.get()
    if(DonID ==""):          #PK not inputted
        messageBox.showinfo("Update Status", "No inputted 'Donation ID'")
    else:
        #-------------------------New Window Creation-------------------------------------------------
        top = Toplevel()
        l_DonIDtop = Label(top, text = "Donation ID", font =('bold', 10))    #Labels
        l_DIDtop = Label(top, text = "Donor ID", font =('bold', 10))  
        l_DDatetop = Label(top, text = "Donation Date", font =('bold', 10))
        l_DTimetop = Label(top, text = "Donation Time", font =('bold', 10))
        l_Bagstop = Label(top, text = "Bags Donated", font =('bold', 10))
        l_Stocktop = Label(top, text = "Stock", font =('bold', 10))

        e_DonIDtop = Entry(top)  #Textfields
        e_DIDtop = Entry(top)
        e_DDatetop = Entry(top)
        e_DTimetop = Entry(top)
        e_Bagstop = Entry(top)    
        e_Stocktop = Entry(top) 
        
        b_invupdatetop = Button(top, text="Update", font=("italic",10), bg="white", command = lambda: Invupdate2(e_DonIDtop.get(),   #Update Button
        e_DIDtop.get(), e_DDatetop.get(),e_DTimetop.get(),e_Bagstop.get(),e_Stocktop.get(),DonID,top)) 

        #-------------------------Sql Database Connection-------------------------------------------------
        con = mysql.connect(host="localhost", user="root", password="", database = "redsavers")
        cursor = con.cursor()
        cursor.execute("SELECT * FROM `inventory` WHERE `Donation ID` = "+DonID)   #Traverse Record
        cursor.fetchall()
        rwcnt = cursor.rowcount   
        con.close()
        if rwcnt == 0:    #PK doesnt exist
            top.destroy()
            messageBox.showerror("ERROR Status", "Inputted 'Donation ID' not registered. Input registered 'Donation ID' only.")
            return
        else:
            top.title('Update Inventory Table')
            top.geometry('230x300')
            l_DonIDtop.pack()
            e_DonIDtop.pack()
            l_DIDtop.pack()
            e_DIDtop.pack()
            l_DDatetop.pack()
            e_DDatetop.pack()
            l_DTimetop.pack()
            e_DTimetop.pack()
            l_Bagstop.pack()
            e_Bagstop.pack()
            l_Stocktop.pack()
            e_Stocktop.pack()
            b_invupdatetop.place(x=87,y=255)
            top.grab_set()
            
def Invupdate2(DonIDtop, DIDtop, DDatetop, DTimetop, Bagstop,Stocktop,DonID,top):
    con = mysql.connect(host="localhost", user="root", password="", database = "redsavers")
    cursor1 = con.cursor()
    if DonIDtop!= "":
        try:
            cursor1.execute("UPDATE `inventory` SET `Donation ID`= '"+DonIDtop+"' WHERE `Donation ID` = " + DonID)
        except Exception as e:
            messageBox.showerror("ERROR Status", "Inputted 'Donation ID' already registered. Please input unregistered 'Donation ID'")
            return
        else: 
            DonID = DonIDtop
    if DIDtop != "":
        try:cursor1.execute("UPDATE `inventory` SET `Donor ID`= '"+ DIDtop+"' WHERE `Donation ID` = " + DonID)
        except: 
            messageBox.showerror("ERROR Status", "Inputted 'Donor ID' not registered. Input registered 'Donor ID' only.")
            return
    if DDatetop != "":
        cursor1.execute("UPDATE `inventory` SET `Donation Date`= '"+ DDatetop+"' WHERE `Donation ID` = " + DonID)
    if DTimetop != "":
        cursor1.execute("UPDATE `inventory` SET `Donation Time`= '"+DTimetop+"' WHERE `Donation ID` = " + DonID)
    if Bagstop != "":
        cursor1.execute("UPDATE `inventory` SET `Bags Donated`= '"+ Bagstop+"' WHERE `Donation ID` = " + DonID)
    if Stocktop != "":
        cursor1.execute("UPDATE `inventory` SET `Stock`= '"+ Stocktop+"' WHERE `Donation ID` = " + DonID)  
    messageBox.showinfo("Update Status", "Record Updated Successfully")
    con.commit()
    con.close() 
    top.destroy()


def Transdelete():
    TransID = entry_TransID.get()
    if(TransID ==""):
        messageBox.showinfo("Delete Status", "No inputted 'Transaction ID'")
    else:
        con = mysql.connect(host="localhost", user="root", password="", database = "redsavers")
        cursor = con.cursor()
        cursor.execute("SELECT * FROM `transaction` WHERE `Transaction ID` = '"+TransID+"'")
        cursor.fetchall()
        rwcnt = cursor.rowcount
        if rwcnt == 0:
            messageBox.showerror("ERROR Status", "Inputted 'Transaction ID' not registered. Input registered 'Transaction ID' only.")
            con.close()
            return
        else:
            cursor.execute("DELETE FROM `transaction` WHERE `Transaction ID` = '"+TransID+"'")
            con.commit()
            con.close()     
        messageBox.showinfo("Delete Status", "Record Deleted Successfully") 

def Transupdate():
    TransID = entry_TransID.get()
    if(TransID ==""):          #PK not inputted
        messageBox.showinfo("Delete Status", "No inputted 'Transaction ID'")
    else:
        #-------------------------New Window Creation-------------------------------------------------
        top = Toplevel()
        l_TransIDtop = Label(top, text = "Transaction ID", font =('bold', 10))    #Labels
        l_PatIDtop = Label(top, text = "Patient ID", font =('bold', 10))  
        l_DIDtop = Label(top, text = "Donor ID", font =('bold', 10))  
        l_Adatetop = Label(top, text = "Accept Date", font =('bold', 10))
        l_ATimetop = Label(top, text = "Accept Time", font =('bold', 10))
        l_Hostop = Label(top, text = "Hospital", font =('bold', 10))
        l_Bagstop = Label(top, text = "Bags Received", font =('bold', 10))

        e_TransIDtop= Entry(top)  #Textfields
        e_PatIDtop = Entry(top)
        e_DIDtop = Entry(top)
        e_Adatetop = Entry(top)
        e_ATimetop = Entry(top)    
        e_Hostop = Entry(top) 
        e_Bagstop = Entry(top) 

        b_transupdatetop = Button(top, text="Update", font=("italic",10), bg="white", command = lambda: Transupdate2(e_TransIDtop.get(),   #Update Button
        e_PatIDtop.get(), e_DIDtop.get(),e_Adatetop.get(),e_ATimetop.get(),e_Hostop.get(),e_Bagstop.get(),TransID,top)) 

        #-------------------------Sql Database Connection-------------------------------------------------
        con = mysql.connect(host="localhost", user="root", password="", database = "redsavers")
        cursor = con.cursor()
        cursor.execute("SELECT * FROM `transaction` WHERE `Transaction ID` = "+TransID)   #Traverse Record
        cursor.fetchall()
        rwcnt = cursor.rowcount   
        con.close()
        if rwcnt == 0:    #PK doesnt exist
            top.destroy()
            messageBox.showerror("ERROR Status", "Inputted 'Transaction ID' not registered. Input registered 'Transaction ID' only.")
            return
        else:
            top.title('Update Inventory Table')
            top.geometry('230x345')
            l_TransIDtop.pack()
            e_TransIDtop.pack()
            l_PatIDtop.pack()
            e_PatIDtop.pack()
            l_DIDtop.pack()
            e_DIDtop.pack()
            l_Adatetop.pack()
            e_Adatetop.pack()
            l_ATimetop.pack()
            e_ATimetop.pack()
            l_Hostop.pack()
            e_Hostop.pack()
            l_Bagstop.pack()
            e_Bagstop.pack()
            b_transupdatetop.place(x=87,y=295)
            top.grab_set()
            
def Transupdate2(TransIDtop, PatIDtop, DIDtop,Adatetop, ATimetop,Hostop,Bagstop,TransID,top):
    con = mysql.connect(host="localhost", user="root", password="", database = "redsavers")
    cursor1 = con.cursor()
    if TransIDtop!= "":
        try:
            cursor1.execute("UPDATE `transaction` SET `Transaction ID`= '"+TransIDtop+"' WHERE `Transaction ID` = '" + TransID+"'")
        except Exception as e:
            messageBox.showerror("ERROR Status", "Inputted 'Transaction ID' already registered. Please input unregistered 'Transaction ID'")
            return
        else: 
            TransID = TransIDtop
    if PatIDtop != "":
        try:cursor1.execute("UPDATE `transaction` SET `Patient ID`= '"+ PatIDtop+"' WHERE `Transaction ID` = '"+ TransID+"'")
        except: 
            messageBox.showerror("ERROR Status", "Inputted 'Patient ID' not registered. Input registered 'Patient ID' only.")
            return
    if DIDtop != "":
        try:cursor1.execute("UPDATE `transaction` SET `Donor ID`= '"+ DIDtop+"' WHERE `Transaction ID` = '" + TransID+"'")
        except: 
            messageBox.showerror("ERROR Status", "Inputted 'Donor ID' not registered. Input registered 'Donor ID' only.")
            return
    if Adatetop != "":
        cursor1.execute("UPDATE `transaction` SET `Accept Date`= '"+ Adatetop+"' WHERE `Transaction ID` = '" + TransID+"'")
    if ATimetop != "":
        cursor1.execute("UPDATE `transaction` SET `Accept Time`= '"+ATimetop+"' WHERE `Transaction ID` = '" + TransID+"'")
    if Hostop != "":
        print(f'Trans: {TransID}', f'Trans: {Hostop}')
        cursor1.execute("UPDATE `transaction` SET `Hospital`= \""+Hostop+"\" WHERE `Transaction ID` = '" + TransID+"'")
    if Bagstop != "":
        cursor1.execute("UPDATE `transaction` SET `Bags Received`= '"+ Bagstop+"' WHERE `Transaction ID` = '" + TransID+"'")
    messageBox.showinfo("Update Status", "Record Updated Successfully")
    con.commit()
    con.close() 
    top.destroy()

def Patientdelete():
    PatID = entry_PatientID.get()
    if(PatID ==""):
        messageBox.showinfo("Delete Status", "No inputted 'Patient ID'")
    else:
        con = mysql.connect(host="localhost", user="root", password="", database = "redsavers")
        cursor = con.cursor()
        cursor.execute("SELECT * FROM `patient` WHERE `Patient ID` = '"+PatID+"'")
        cursor.fetchall()
        rwcnt = cursor.rowcount
        if rwcnt == 0:
            messageBox.showerror("ERROR Status", "Inputted 'Patient ID' not registered. Input registered 'Patient ID' only.")
            con.close()
            return
        else:
            cursor.execute("DELETE FROM `patient` WHERE `Patient ID` = '"+PatID+"'")
            con.commit()
            con.close()     
        messageBox.showinfo("Delete Status", "Record Deleted Successfully") 

def Patientupdate():
    PatID = entry_PatientID.get()
    if(PatID ==""):
        messageBox.showinfo("Delete Status", "No inputted 'Patient ID'")
    else:
        #-------------------------New Window Creation-------------------------------------------------
        top = Toplevel()
        l_PatIDtop = Label(top, text = "Patient ID", font =('bold', 10))    #Labels
        l_BGtop = Label(top, text = "Blood Group", font =('bold', 10))  
        l_PatNametop = Label(top, text = "Patient Name", font =('bold', 10))  
        l_PatPhonetop = Label(top, text = "Patient Phone", font =('bold', 10))
        l_PatAddtop = Label(top, text = "Patient Address", font =('bold', 10))

        e_PatIDtop= Entry(top)  #Textfields
        e_BGtop = Entry(top)
        e_PatNametop = Entry(top)
        e_PatPhonetop = Entry(top)
        e_PatAddtop = Entry(top)    

        b_patupdatetop = Button(top, text="Update", font=("italic",10), bg="white", command = lambda: Patientupdate2(e_PatIDtop.get(),   #Update Button
        e_BGtop.get(),e_PatNametop .get(),e_PatPhonetop.get(),e_PatAddtop.get(),PatID,top)) 

        #-------------------------Sql Database Connection-------------------------------------------------
        con = mysql.connect(host="localhost", user="root", password="", database = "redsavers")
        cursor = con.cursor()
        cursor.execute("SELECT * FROM `patient` WHERE `Patient ID` = "+PatID)   #Traverse Record
        cursor.fetchall()
        rwcnt = cursor.rowcount   
        con.close()
        if rwcnt == 0:    #PK doesnt exist
            top.destroy()
            messageBox.showerror("ERROR Status", "Inputted 'Patient ID' not registered. Input registered 'Patient ID' only.")
            return
        else:
            top.title('Update Inventory Table')
            top.geometry('230x270')
            l_PatIDtop.pack()
            e_PatIDtop.pack()
            l_BGtop.pack()
            e_BGtop.pack()
            l_PatNametop.pack()
            e_PatNametop.pack()
            l_PatPhonetop.pack()
            e_PatPhonetop.pack()
            l_PatAddtop.pack()
            e_PatAddtop.pack()
            b_patupdatetop.place(x=87,y=220)
            top.grab_set()
            
def Patientupdate2(PatIDtop, BGtop, PatNametop,PatPhonetop, PatAddtop,PatID,top):       #Patient Update 
    con = mysql.connect(host="localhost", user="root", password="", database = "redsavers")
    cursor1 = con.cursor()
    if PatIDtop!= "":
        try:
            cursor1.execute("UPDATE `patient` SET `Patient ID`= '"+PatIDtop+"' WHERE `Patient ID` = '" + PatID+"'")
        except Exception as e:
            messageBox.showerror("ERROR Status", "Inputted 'Patient ID' already registered. Please input unregistered 'Patient ID'")
            return
        else: 
            PatID = PatIDtop
    if BGtop != "":
        try:cursor1.execute("UPDATE `patient` SET `Blood Group`= '"+ BGtop+"' WHERE `Patient ID` = '"+PatID+"'")
        except: 
            messageBox.showerror("ERROR Status", "Inputted 'Blood Group' not recognized. Input recognized/registered 'Blood Group' only.")
            return
    if PatNametop != "":
        cursor1.execute("UPDATE `patient` SET `Patient Name`= '"+PatNametop+"' WHERE `Patient ID` = '" + PatID+"'")
    if PatPhonetop != "":
        cursor1.execute("UPDATE `patient` SET `Patient Phone`= '"+PatPhonetop+"' WHERE `Patient ID` = '" +PatID+"'")
    if PatAddtop != "":
        cursor1.execute("UPDATE `patient` SET `Patient Address`= \""+PatAddtop+"\" WHERE `Patient ID` = '" +PatID+"'")
    messageBox.showinfo("Update Status", "Record Updated Successfully")
    con.commit()
    con.close() 
    top.destroy()


def Stocksdelete():     #Stocks Delete
    BG = entry_StocksBGDel.get()
    if(BG ==""):
        messageBox.showinfo("Delete Status", "No inputted 'Blood Group'")
    else:
        con = mysql.connect(host="localhost", user="root", password="", database = "redsavers")
        cursor = con.cursor()
        cursor.execute("SELECT * FROM `stocks` WHERE `Blood Group` = '"+BG+"'")
        cursor.fetchall()
        rwcnt = cursor.rowcount
        if rwcnt == 0:
            messageBox.showerror("ERROR Status", "Inputted 'Blood Group' not registered. Input registered 'Blood Group' only.")
            con.close()
            return
        else:
            cursor.execute("DELETE FROM `stocks` WHERE `Blood Group` = '"+BG+"'")
            con.commit()
            con.close()     
        messageBox.showinfo("Delete Status", "Record Deleted Successfully") 

def Stocksupdate():     #Stocks Update
    BG = entry_StocksBGDel.get()
    if(BG ==""):
        messageBox.showinfo("Delete Status", "No inputted 'Blood Group'")
    else:
        #-------------------------New Window Creation-------------------------------------------------
        top = Toplevel()
        l_nBG = Label(top, text = "Blood Group", font =('bold', 10))    #Labels
        l_Stock = Label(top, text = "Overall Bag Count", font =('bold', 10))  

        e_nBG= Entry(top)  #Textfields
        e_Stock = Entry(top)

        b_stocksupdatetop = Button(top, text="Update", font=("italic",10), bg="white", command = lambda: Stocksupdate2(e_nBG.get(),   #Update Button
        e_Stock.get(),BG,top)) 

        #-------------------------Sql Database Connection-------------------------------------------------
        con = mysql.connect(host="localhost", user="root", password="", database = "redsavers")
        cursor = con.cursor()
        cursor.execute("SELECT * FROM `stocks` WHERE `Blood Group` = '"+BG+"'")   #Traverse Record
        cursor.fetchall()
        rwcnt = cursor.rowcount   
        con.close()
        if rwcnt == 0:    #PK doesnt exist
            top.destroy()
            messageBox.showerror("ERROR Status", "Inputted 'Blood Group' not registered. Input registered 'Blood Group' only.")
            return
        else:
            top.title('Update Inventory Table')
            top.geometry('230x145')
            l_nBG.pack()
            e_nBG.pack()
            l_Stock.pack()
            e_Stock.pack()
            b_stocksupdatetop.place(x=87,y=95)
            top.grab_set()
            
def Stocksupdate2(nBG, Stock,BG,top):       #Stocks Update
    con = mysql.connect(host="localhost", user="root", password="", database = "redsavers")
    cursor1 = con.cursor()
    if nBG!= "":
        try:
            cursor1.execute("UPDATE `stocks` SET `Blood Group`= '"+nBG+"' WHERE `Blood Group` = '"+BG+"'")
        except Exception as e:
            messageBox.showerror("ERROR Status", "Inputted 'Blood Group' already registered. Please input unregistered 'Blood Group'")
            return
        else: 
            BG = nBG
    if Stock != "":
        try:cursor1.execute("UPDATE `stocks` SET `Overall Bag Count`= '"+Stock+"' WHERE `Blood Group` = '"+BG+"'")
        except: 
            messageBox.showerror("ERROR Status", "Input whole numbers only for 'Stock'.")
            return
    messageBox.showinfo("Update Status", "Record Updated Successfully")
    con.commit()
    con.close() 
    top.destroy()

def PiePlot():  #Plot Pie Chart Stocks
    con = mysql.connect(host="localhost", user="root", password="", database = "redsavers")
    cursor = con.cursor()
    cursor.execute("SELECT * FROM `stocks`")
    data = cursor.fetchall()
    stocks = []
    bg = []
    for i in range(0,len(data)):
        if data[i][1] > 0:
            bg.append(data[i][0])
            stocks.append(data[i][1])
    con.close()
    plt.pie(stocks, labels=bg, wedgeprops={'edgecolor':"#2bcccc"}, autopct="%1.1f%%")
    plt.title("Blood Group Overall Stock Chart")
    plt.tight_layout()
    plt.show()

def BarDonations():     #Bar Graph Donations
    con = mysql.connect(host="localhost", user="root", password="", database = "redsavers")
    cursor = con.cursor()
    cursor.execute("SELECT DISTINCT `Donor ID` FROM `inventory`")
    donIds = cursor.fetchall()
    bagsdon = []
    donorsno = []
    for i in range(0,len(donIds)):
        donorsno.append(str(donIds[i][0]))
        cursor.execute("SELECT SUM(`Bags Donated`) FROM `inventory` WHERE `Donor ID` ='"+str(donIds[i][0])+"'")
        bagsdon.append(cursor.fetchall()[0][0])
    con.close()
    plt.bar(donorsno,bagsdon, color=colors, width=0.2)
    plt.xlabel("Donor IDs")
    plt.ylabel("Bag Count")
    plt.title("Donations of Donors")
    plt.tight_layout()
    plt.show()

def DonorBar():     #Bar Graph Donor
    con = mysql.connect(host="localhost", user="root", password="", database = "redsavers")
    cursor = con.cursor()
    cursor.execute("SELECT `Blood Group` FROM `stocks`")
    temp = cursor.fetchall()
    BGs = []
    DonorCount  = []
    for i in range(0,len(temp)):
        BGs.append(str(temp[i][0]))
        cursor.execute("SELECT COUNT(`Donor ID`) FROM `donor` WHERE `Blood Group`='"+str(temp[i][0])+"'")
        DonorCount.append(cursor.fetchall()[0][0])
    con.close()
    plt.bar(BGs,DonorCount, color=colors, width=1)
    plt.xlabel("Blood Groups")
    plt.ylabel("Registered Donors")
    plt.title("Overall Registered Donors")
    plt.tight_layout()
    plt.show()

def PatientBar():   #Bar Graph Patient
    con = mysql.connect(host="localhost", user="root", password="", database = "redsavers")
    cursor = con.cursor()
    cursor.execute("SELECT `Blood Group` FROM `stocks`")
    temp = cursor.fetchall()
    BGs = []
    DonorCount  = []
    for i in range(0,len(temp)):
        BGs.append(str(temp[i][0]))
        cursor.execute("SELECT COUNT(`Patient ID`) FROM `patient` WHERE `Blood Group`='"+str(temp[i][0])+"'")
        DonorCount.append(cursor.fetchall()[0][0])
    con.close()
    plt.bar(BGs,DonorCount, color=colors, width=1)
    plt.xlabel("Blood Groups")
    plt.ylabel("Registered Patients")
    plt.title("Overall Registered Patients")
    plt.tight_layout()
    plt.show()
def checktext():
    print("2")
#======================== MAIN FRAME ============================#

window = Tk()           #GUI Main Design
window.geometry("1600x600")
window.configure(bg = "#C4C4C4")

canvas = Canvas(        #GUI Main Proportions
    window, bg = "#C4C4C4",
    height = 600,
    width = 1600,
    bd = 0,
    highlightthickness = 0,
    relief = "ridge"
)

canvas.place(x = 0, y = 0)
image_image_1 = PhotoImage(
    file=relative_to_assets("image_1.png"))
image_1 = canvas.create_image(
    0,
    0,
    image=image_image_1
)

#======================== DONOR FRAME ============================#
canvas.create_rectangle(   #Container for  Update
    101.0,
    25.0,
    354.0,
    300.0,
    fill="#FFFFFF",
    outline="")

        #----------------- Donor Buttons ---------------------#
button_donorupdate_image = PhotoImage(      #Donor Update Button
    file=relative_to_assets("button_1.png"))     
button_donorupdate = Button(
    image=button_donorupdate_image,
    borderwidth=0,
    highlightthickness=0,
    command=update,
    relief="flat"
)
button_donorupdate.place(       
    x=272.0,
    y=266.0,
    width=57.0,
    height=18.0
)

button_donordelete_image = PhotoImage(      #Donor Delete Button                  
    file=relative_to_assets("button_2.png"))   
button_donordelete = Button(
    image=button_donordelete_image,
    borderwidth=0,
    highlightthickness=0,
    command=delete,
    relief="flat"
)
button_donordelete.place(        
    x=210.0,
    y=266.0,
    width=57.0,
    height=18.0
)

entry_image_1 = PhotoImage(     #Donor Donor_ID TextField
    file=relative_to_assets("entry_1.png"))
entry_bg_1 = canvas.create_image(
    269.5,
    247.0,
    image=entry_image_1
)
entry_DonorID = Entry(      
    bd=0,
    bg="#D9CDCD",
    fg="#000716",
    highlightthickness=0
)
entry_DonorID.place(    
    x=210.0,
    y=240.0,
    width=119.0,
    height=12.0
)

canvas.create_text(     #Donor Donor_ID Label
    117.0,
    242.0,
    anchor="nw",
    text="Donor ID",
    fill="#000000",
    font=("Inter Bold", 10 * -1)
)

canvas.create_rectangle(   #Line below Donor Label
    114.0,
    230.0,
    340.6697540283203,
    231.0,
    fill="#000000",
    outline="")

button_adddonor_image = PhotoImage(           #Donor Add Button
    file=relative_to_assets("button_3.png"))
button_adddonor = Button(
    image=button_adddonor_image,
    borderwidth=0,
    highlightthickness=0,
    command=insert,
    relief="flat"
)
button_adddonor.place(      
    x=239.0,
    y=204.0,
    width=42.0,
    height=18.0
)

button_showdonor_image = PhotoImage(       #Donor Show Button
    file=relative_to_assets("button_4.png"))
button_showdonor = Button(
    image=button_showdonor_image,
    borderwidth=0,
    highlightthickness=0,
    command=Donorread,
    relief="flat"
)
button_showdonor.place(
    x=287.0,
    y=204.0,
    width=42.0,
    height=18.0
)

entry_DonorBG_image = PhotoImage(            #Donor Blood_Group TextField
    file=relative_to_assets("entry_2.png"))
entry_bg_2 = canvas.create_image(
    260.2963104248047,
    187.23445892333984,
    image=entry_DonorBG_image
)
entry_DonorBG = Entry(      
    bd=0,
    bg="#D9CDCD",
    fg="#000716",
    highlightthickness=0
)
entry_DonorBG .place(
    x=191.58026123046875,
    y=180.0875701904297,
    width=137.43209838867188,
    height=12.293777465820312
)

canvas.create_text(       #Donor Blood Group Label
    192.0,
    168.0,
    anchor="nw",
    text="Blood Group",
    fill="#000000",
    font=("Inter Regular", 9 * -1)
)

entry_DonorAdd_image= PhotoImage(       #Donor Home_Address TextField
    file=relative_to_assets("entry_3.png"))
entry_bg_3 = canvas.create_image(
    260.2963104248047,
    156.50282287597656,
    image=entry_DonorAdd_image
)
entry_DonorAdd = Entry(     
    bd=0,
    bg="#D9CDCD",
    fg="#000716",
    highlightthickness=0
)
entry_DonorAdd.place(
    x=191.58026123046875,
    y=149.35592651367188,
    width=137.43209838867188,
    height=12.293792724609375
)

canvas.create_text(         #Donor Home_Address Label
    192.0,
    138.0,
    anchor="nw",
    text="Home Address",
    fill="#000000",
    font=("Inter Regular", 9 * -1)
)

entry_image_4 = PhotoImage(      #Donor Contact_Number TexField
    file=relative_to_assets("entry_4.png"))
entry_bg_4 = canvas.create_image(
    260.2963104248047,
    125.77119445800781,
    image=entry_image_4
)
entry_DonorContact = Entry(    
    bd=0,
    bg="#D9CDCD",
    fg="#000716",
    highlightthickness=0
)
entry_DonorContact .place(      
    x=191.58026123046875,
    y=118.62429809570312,
    width=137.43209838867188,
    height=12.293792724609375
)

canvas.create_text(     #Donor Contect_number Label
    192.0,
    107.0,
    anchor="nw",
    text="Contact Number",
    fill="#000000",
    font=("Inter Regular", 9 * -1)
)

entry_image_5 = PhotoImage(     #Donor Full_Name TexField
    file=relative_to_assets("entry_5.png"))
entry_bg_5 = canvas.create_image(
    260.2963104248047,
    95.03953552246094,
    image=entry_image_5
)
entry_DonorName = Entry(        
    bd=0,
    bg="#D9CDCD",
    fg="#000716",
    highlightthickness=0
)
entry_DonorName.place(
    x=191.58026123046875,
    y=87.89263916015625,
    width=137.43209838867188,
    height=12.293792724609375
)

canvas.create_text(     #Donor Full_Name Label
    192.0,
    76.0,
    anchor="nw",
    text="Full Name",
    fill="#000000",
    font=("Inter Regular", 9 * -1)
)
canvas.create_text(     #Donor Contact Label
    117.0,
    76.0,
    anchor="nw",
    text="Account",
    fill="#000000",
    font=("Inter Bold", 10 * -1)
)


canvas.create_rectangle(   #Line
    115.61727905273438,
    61.8785400390625,
    342.2870330810547,
    62.8785400390625,
    fill="#000000",
    outline="")

canvas.create_text(     #Donor Label
    117.0,
    35.0,
    anchor="nw",
    text="Donor",
    fill="#000000",
    font=("Inter Regular", 18 * -1)
)

canvas.create_rectangle(   #Transaction White Box Frame 
    673.0,
    25.0,
    926.0,
    300.0,
    fill="#FFFFFF",
    outline="")

button_image_5 = PhotoImage(        #Transaction Update Button
    file=relative_to_assets("button_5.png"))
button_TransUpd = Button(
    image=button_image_5,
    borderwidth=0,
    highlightthickness=0,
    command=Transupdate,
    relief="flat"
)
button_TransUpd.place(      
    x=844.0,
    y=266.0,
    width=57.0,
    height=18.0
)

button_image_6 = PhotoImage(        #Transaction Delete Button
    file=relative_to_assets("button_6.png"))
button_TransDel = Button(
    image=button_image_6,
    borderwidth=0,
    highlightthickness=0,
    command=Transdelete,
    relief="flat"
)
button_TransDel.place(       
    x=782.0,
    y=266.0,
    width=57.0,
    height=18.0
)

entry_image_6 = PhotoImage(      #Transaction Transaction_ID TextField
    file=relative_to_assets("entry_6.png"))
entry_bg_6 = canvas.create_image(
    841.5,
    247.0,
    image=entry_image_6
)
entry_TransID = Entry(
    bd=0,
    bg="#D9CDCD",
    fg="#000716",
    highlightthickness=0
)
entry_TransID.place(       
    x=782.0,
    y=240.0,
    width=119.0,
    height=12.0
)

canvas.create_text(     #Transaction Transaction_ID Label  
    689.0,
    242.0,
    anchor="nw",
    text="Transaction ID",
    fill="#000000",
    font=("Inter Bold", 10 * -1)
)

canvas.create_rectangle( #Line above Transaction_ID
    686.0,
    230.0,
    912.6697387695312,
    231.0,
    fill="#000000",
    outline="")

button_image_7 = PhotoImage(        #Transaction Add Button 
    file=relative_to_assets("button_7.png"))
button_TransAdd = Button(
    image=button_image_7,
    borderwidth=0,
    highlightthickness=0,
    command=Transinsert,
    relief="flat"
)
button_TransAdd.place(      
    x=811.0,
    y=173.0,
    width=42.0,
    height=18.0
)

button_image_8 = PhotoImage(        #Transaction Show Button
    file=relative_to_assets("button_8.png"))
button_TransShow = Button(
    image=button_image_8,
    borderwidth=0,
    highlightthickness=0,
    command=Transread,
    relief="flat"
)
button_TransShow.place(     
    x=859.0,
    y=173.0,
    width=42.0,
    height=18.0
)

entry_image_7 = PhotoImage(       #Transaction Bag_Count TextField
    file=relative_to_assets("entry_7.png"))
entry_bg_7 = canvas.create_image(
    832.2962951660156,
    156.50282287597656,
    image=entry_image_7
)
entry_TransBagC = Entry(
    bd=0,
    bg="#D9CDCD",
    fg="#000716",
    highlightthickness=0
)
entry_TransBagC.place(      
    x=763.5802612304688,
    y=149.35592651367188,
    width=137.43206787109375,
    height=12.293792724609375
)

canvas.create_text(     #Transaction Bag_Count Label
    764.0,
    138.0,
    anchor="nw",
    text="Bag Count",
    fill="#000000",
    font=("Inter Regular", 9 * -1)
)

entry_image_8 = PhotoImage(     #Transaction Hospital TextField
    file=relative_to_assets("entry_8.png"))
entry_bg_8 = canvas.create_image(
    832.2962951660156,
    125.77119445800781,
    image=entry_image_8
)
entry_TransHos = Entry(     
    bd=0,
    bg="#D9CDCD",
    fg="#000716",
    highlightthickness=0
)
entry_TransHos.place(       
    x=763.5802612304688,
    y=118.62429809570312,
    width=137.43206787109375,
    height=12.293792724609375
)

canvas.create_text(     #Transaction Hospital Label
    764.0,
    107.0,
    anchor="nw",
    text="Hospital",
    fill="#000000",
    font=("Inter Regular", 9 * -1)
)

entry_image_9 = PhotoImage(     #Transaction Patient_ID TextField
    file=relative_to_assets("entry_9.png"))
entry_bg_9 = canvas.create_image(
    832.2962951660156,
    95.03953552246094,
    image=entry_image_9
)
entry_TransPatientID = Entry(
    bd=0,
    bg="#D9CDCD",
    fg="#000716",
    highlightthickness=0
)
entry_TransPatientID .place(        
    x=763.5802612304688,
    y=87.89263916015625,
    width=137.43206787109375,
    height=12.293792724609375
)

canvas.create_text(     #Transaction Patient_ID Label
    764.0,
    76.0,
    anchor="nw",
    text="Patient ID",
    fill="#000000",
    font=("Inter Regular", 9 * -1)
)

canvas.create_text(     #Transaction Account Label
    689.0,
    76.0,
    anchor="nw",
    text="Account",
    fill="#000000",
    font=("Inter Bold", 10 * -1)
)

canvas.create_rectangle(        #Line below Transaction Label
    687.6173095703125,
    61.8785400390625,
    914.2870483398438,
    62.8785400390625,
    fill="#000000",
    outline="")

canvas.create_text(     #Transaction Label
    689.0,
    35.0,
    anchor="nw",
    text="Transaction",
    fill="#000000",
    font=("Inter Regular", 18 * -1)
)

canvas.create_rectangle(        #Patient White Box Frame
    959.0,
    25.0,
    1212.0,
    300.0,
    fill="#FFFFFF",
    outline="")

button_image_9 = PhotoImage(         #Patient Update  Button
    file=relative_to_assets("button_9.png"))
button_PatientUpd = Button(
    image=button_image_9,
    borderwidth=0,
    highlightthickness=0,
    command=Patientupdate,
    relief="flat"
)
button_PatientUpd.place(       
    x=1130.0,
    y=266.0,
    width=57.0,
    height=18.0
)

button_image_10 = PhotoImage(       #Patient Delete  Button
    file=relative_to_assets("button_10.png"))
button_PatientDel = Button(
    image=button_image_10,
    borderwidth=0,
    highlightthickness=0,
    command=Patientdelete,
    relief="flat"
)
button_PatientDel.place(        
    x=1068.0,
    y=266.0,
    width=57.0,
    height=18.0
)

entry_image_10 = PhotoImage(        #Patient Patient_ID TextField
    file=relative_to_assets("entry_10.png"))
entry_bg_10 = canvas.create_image(
    1127.5,
    247.0,
    image=entry_image_10
)
entry_PatientID = Entry(
    bd=0,
    bg="#D9CDCD",
    fg="#000716",
    highlightthickness=0
)
entry_PatientID.place(      
    x=1068.0,
    y=240.0,
    width=119.0,
    height=12.0
)

canvas.create_text(     #Patient Patient_ID  Label
    975.0,
    242.0,
    anchor="nw",
    text="Patient ID",
    fill="#000000",
    font=("Inter Bold", 10 * -1)
)

canvas.create_rectangle(        #Line above Patient_ID Label
    972.0,
    230.0,
    1198.6697387695312,
    231.0,
    fill="#000000",
    outline="")

button_image_11 = PhotoImage(       #Patient Add Button
    file=relative_to_assets("button_11.png"))
button_PatiendAdd = Button(
    image=button_image_11,
    borderwidth=0,
    highlightthickness=0,
    command=Patientinsert,
    relief="flat"
)
button_PatiendAdd.place(        
    x=1097.0,
    y=204.0,
    width=42.0,
    height=18.0
)

button_image_12 = PhotoImage(       #Patien Show Button
    file=relative_to_assets("button_12.png"))
button_PatientShow = Button(
    image=button_image_12,
    borderwidth=0,
    highlightthickness=0,
    command=Patread,
    relief="flat"
)
button_PatientShow.place(       
    x=1145.0,
    y=204.0,
    width=42.0,
    height=18.0
)

entry_image_11 = PhotoImage(        #Patient Blood_Group TextField
    file=relative_to_assets("entry_11.png"))
entry_bg_11 = canvas.create_image(
    1118.29638671875,
    187.23445892333984,
    image=entry_image_11
)
entry_PatientBG = Entry(
    bd=0,
    bg="#D9CDCD",
    fg="#000716",
    highlightthickness=0
)
entry_PatientBG.place(      
    x=1049.580322265625,
    y=180.0875701904297,
    width=137.43212890625,
    height=12.293777465820312
)

canvas.create_text(     #Patient Blood_Group Label
    1050.0,
    168.0,
    anchor="nw",
    text="Blood Group",
    fill="#000000",
    font=("Inter Regular", 9 * -1)
)

entry_image_12 = PhotoImage(        #Patient Home_Address TextField
    file=relative_to_assets("entry_12.png"))
entry_bg_12 = canvas.create_image(
    1118.29638671875,
    156.50282287597656,
    image=entry_image_12
)
entry_PatientAdd = Entry(
    bd=0,
    bg="#D9CDCD",
    fg="#000716",
    highlightthickness=0
)
entry_PatientAdd.place(     
    x=1049.580322265625,
    y=149.35592651367188,
    width=137.43212890625,
    height=12.293792724609375
)

canvas.create_text(     #Patient Home_Address Label
    1050.0,
    138.0,
    anchor="nw",
    text="Home Address",
    fill="#000000",
    font=("Inter Regular", 9 * -1)
)

entry_image_13 = PhotoImage(        #Patient Contact_Number TextField
    file=relative_to_assets("entry_13.png"))
entry_bg_13 = canvas.create_image(
    1118.29638671875,
    125.77119445800781,
    image=entry_image_13
)
entry_PatientCont = Entry(
    bd=0,
    bg="#D9CDCD",
    fg="#000716",
    highlightthickness=0
)
entry_PatientCont.place(        
    x=1049.580322265625,
    y=118.62429809570312,
    width=137.43212890625,
    height=12.293792724609375
)

canvas.create_text(     #Patient Contact_Number Label
    1050.0,
    107.0,
    anchor="nw",
    text="Contact Number",
    fill="#000000",
    font=("Inter Regular", 9 * -1)
)

entry_image_14 = PhotoImage(        #Patient Full_Name TextField
    file=relative_to_assets("entry_14.png"))
entry_bg_14 = canvas.create_image(
    1118.29638671875,
    95.03953552246094,
    image=entry_image_14
)
entry_PatientName = Entry(
    bd=0,
    bg="#D9CDCD",
    fg="#000716",
    highlightthickness=0
)
entry_PatientName.place(        
    x=1049.580322265625,
    y=87.89263916015625,
    width=137.43212890625,
    height=12.293792724609375
)

canvas.create_text(      #Patient Full_Name Label
    1050.0,
    76.0,
    anchor="nw",
    text="Full Name",
    fill="#000000",
    font=("Inter Regular", 9 * -1)
)

canvas.create_text(      #Patient Account Label
    975.0,
    76.0,
    anchor="nw",
    text="Account",
    fill="#000000",
    font=("Inter Bold", 10 * -1)
)

canvas.create_rectangle(        #Line Below Patient Label
    973.6173095703125,
    61.8785400390625,
    1200.2870483398438,
    62.8785400390625,
    fill="#000000",
    outline="")

canvas.create_text(     #Patient Label
    975.0,
    35.0,
    anchor="nw",
    text="Patient",
    fill="#000000",
    font=("Inter Regular", 18 * -1)
)

canvas.create_rectangle(        #Inventory White Box Frame
    387.0,
    25.0,
    640.0,
    300.0,
    fill="#FFFFFF",
    outline="")

button_image_13 = PhotoImage(       #Inventory Update Button
    file=relative_to_assets("button_13.png"))
button_InventoryUpd = Button(
    image=button_image_13,
    borderwidth=0,
    highlightthickness=0,
    command=Invupdate,
    relief="flat"
)
button_InventoryUpd.place(      
    x=558.0,
    y=266.0,
    width=57.0,
    height=18.0
)

button_image_14 = PhotoImage(        #Inventory Delete Button
    file=relative_to_assets("button_14.png"))
button_InventoryDel = Button(
    image=button_image_14,
    borderwidth=0,
    highlightthickness=0,
    command=Invdelete,
    relief="flat"
)
button_InventoryDel.place(     
    x=496.0,
    y=266.0,
    width=57.0,
    height=18.0
)

entry_image_15 = PhotoImage(        #Inventory Donation_ID TextField
    file=relative_to_assets("entry_15.png"))
entry_bg_15 = canvas.create_image(
    555.5,
    247.0,
    image=entry_image_15
)
entry_InventoryDtnID = Entry(
    bd=0,
    bg="#D9CDCD",
    fg="#000716",
    highlightthickness=0
)
entry_InventoryDtnID.place(     
    x=496.0,
    y=240.0,
    width=119.0,
    height=12.0
)

canvas.create_text(     #Inventory Donation_ID Label
    401.0,
    242.0,
    anchor="nw",
    text="Donation ID",
    fill="#000000",
    font=("Inter Bold", 10 * -1)
)

canvas.create_rectangle(        #Line Above Donation_Id Label
    400.0,
    230.0,
    626.6697387695312,
    231.0,
    fill="#000000",
    outline="")

button_image_15 = PhotoImage(
    file=relative_to_assets("button_15.png"))
button_InventoryAdd = Button(
    image=button_image_15,
    borderwidth=0,
    highlightthickness=0,
    command=Invinsert,
    relief="flat"
)
button_InventoryAdd.place(      #Inventory Add button
    x=525.0,
    y=142.0,
    width=42.0,
    height=18.0
)

button_image_16 = PhotoImage(
    file=relative_to_assets("button_16.png"))
button_InventoryShow = Button(
    image=button_image_16,
    borderwidth=0,
    highlightthickness=0,
    command=Invread,
    relief="flat"
)
button_InventoryShow.place(     #Inventory Show Button
    x=573.0,
    y=142.0,
    width=42.0,
    height=18.0
)

entry_image_16 = PhotoImage(        #Inventory Bag_Count TextField
    file=relative_to_assets("entry_16.png"))
entry_bg_16 = canvas.create_image(
    546.2963104248047,
    125.77119445800781,
    image=entry_image_16
)
entry_InventoryBagC = Entry(
    bd=0,
    bg="#D9CDCD",
    fg="#000716",
    highlightthickness=0
)
entry_InventoryBagC.place(      
    x=477.58026123046875,
    y=118.62429809570312,
    width=137.43209838867188,
    height=12.293792724609375
)

canvas.create_text(     #Inventory Bag_Count Label
    478.0,
    107.0,
    anchor="nw",
    text="Bag Count",
    fill="#000000",
    font=("Inter Regular", 9 * -1)
)

entry_image_17 = PhotoImage(        #Inventory Donor_ID TextField
    file=relative_to_assets("entry_17.png"))
entry_bg_17 = canvas.create_image(
    546.2963104248047,
    95.03953552246094,
    image=entry_image_17
)
entry_InventoryDonorID = Entry(     
    bd=0,
    bg="#D9CDCD",
    fg="#000716",
    highlightthickness=0
)
entry_InventoryDonorID.place(       
    x=477.58026123046875,
    y=87.89263916015625,
    width=137.43209838867188,
    height=12.293792724609375
)

canvas.create_text(     #Inventory Donor_ID Label
    478.0,
    76.0,
    anchor="nw",
    text="Donor ID",
    fill="#000000",
    font=("Inter Regular", 9 * -1)
)

canvas.create_text(     #Inventory Account Label
    403.0,
    75.0,
    anchor="nw",
    text="Account",
    fill="#000000",
    font=("Inter Bold", 10 * -1)
)

canvas.create_rectangle(        #Line Below Inventory Label
    401.6172790527344,
    61.8785400390625,
    628.2870483398438,
    62.8785400390625,
    fill="#000000",
    outline="")

canvas.create_text(     #Inventory Label
    403.0,
    35.0,
    anchor="nw",
    text="Inventory",
    fill="#000000",
    font=("Inter Regular", 18 * -1)
)

canvas.create_rectangle(        #Inventory White Box Frame
    1245.0,
    25.0,
    1498.0,
    300.0,
    fill="#FFFFFF",
    outline="")

button_image_17 = PhotoImage(       #Stocks Update Button
    file=relative_to_assets("button_17.png"))
button_StocksUpd = Button(
    image=button_image_17,
    borderwidth=0,
    highlightthickness=0,
    command=Stocksupdate,
    relief="flat"
)
button_StocksUpd .place(        
    x=1416.0,
    y=266.0,
    width=57.0,
    height=18.0
)

button_image_18 = PhotoImage(       #Stocks Delete Button
    file=relative_to_assets("button_18.png"))
button_StocksDel= Button(
    image=button_image_18,
    borderwidth=0,
    highlightthickness=0,
    command=Stocksdelete,
    relief="flat"
)
button_StocksDel.place(     
    x=1354.0,
    y=266.0,
    width=57.0,
    height=18.0
)

button_image_19 = PhotoImage(       #Plot Stocks Button
    file=relative_to_assets("button_19.png"))
button_PlotStocks = Button(
    image=button_image_19,
    borderwidth=0,
    highlightthickness=0,
    command=PiePlot,
    relief="flat"
)
button_PlotStocks.place(    
    x=1411.0,
    y=407.0,
    width=168.0,
    height=30.0
)

button_image_20 = PhotoImage(       #Plot Donor Blood Group Button
    file=relative_to_assets("button_20.png"))
button_PlotDonorBG = Button(
    image=button_image_20,
    borderwidth=0,
    highlightthickness=0,
    command=DonorBar,
    relief="flat"
)
button_PlotDonorBG.place(   
    x=1411.0,
    y=489.0,
    width=168.0,
    height=30.0
)

button_image_21 = PhotoImage(       #Plot Donations Button
    file=relative_to_assets("button_21.png"))
button_PlotDonations = Button(
    image=button_image_21,
    borderwidth=0,
    highlightthickness=0,
    command=BarDonations,
    relief="flat"
)
button_PlotDonations.place(     
    x=1411.0,
    y=448.0,
    width=168.0,
    height=30.0
)

button_image_22 = PhotoImage(       #Plot Patient Blood Group Button
    file=relative_to_assets("button_22.png"))
button_PlotPatientBG = Button(
    image=button_image_22,
    borderwidth=0,
    highlightthickness=0,
    command=PatientBar,
    relief="flat"
)
button_PlotPatientBG.place(     
    x=1411.0,
    y=530.0,
    width=168.0,
    height=30.0
)

entry_image_18 = PhotoImage(        #Stocks Blood_Group  TextField
    file=relative_to_assets("entry_18.png"))
entry_bg_18 = canvas.create_image(
    1413.5,
    247.0,
    image=entry_image_18
)
entry_StocksBGDel = Entry(
    bd=0,
    bg="#D9CDCD",
    fg="#000716",
    highlightthickness=0
)
entry_StocksBGDel.place(    
    x=1354.0,
    y=240.0,
    width=119.0,
    height=12.0
)

canvas.create_text(     #Inventory Blood Group Label
    1259.0,
    242.0,
    anchor="nw",
    text="Blood Group",
    fill="#000000",
    font=("Inter Bold", 10 * -1)
)

canvas.create_rectangle(        #Line Above Blood_Group TextField
    1258.0,
    230.0,
    1484.6697998046875,
    231.0,
    fill="#000000",
    outline="")

button_image_23 = PhotoImage(       #Stocks add Button
    file=relative_to_assets("button_23.png"))
button_StocksAdd = Button(
    image=button_image_23,
    borderwidth=0,
    highlightthickness=0,
    command=BGinsert,
    relief="flat"
)
button_StocksAdd.place(     
    x=1383.0,
    y=111.0,
    width=42.0,
    height=18.0
)

button_image_24 = PhotoImage(       #Stocks Show Button
    file=relative_to_assets("button_24.png"))
button_StocksShow = Button(
    image=button_image_24,
    borderwidth=0,
    highlightthickness=0,
    command=BGread,
    relief="flat"
)
button_StocksShow.place(        
    x=1431.0,
    y=111.0,
    width=42.0,
    height=18.0
)

entry_image_19 = PhotoImage(        #Stocks Record Bloud_Group TextField
    file=relative_to_assets("entry_19.png"))
entry_bg_19 = canvas.create_image(
    1404.29638671875,
    95.03953552246094,
    image=entry_image_19
)
entry_StocksBGAdd = Entry(
    bd=0,
    bg="#D9CDCD",
    fg="#000716",
    highlightthickness=0
)
entry_StocksBGAdd.place(        
    x=1335.580322265625,
    y=87.89263916015625,
    width=137.43212890625,
    height=12.293792724609375
)

canvas.create_text(     #Stocks Blood_Group Label
    1336.0,
    76.0,
    anchor="nw",
    text="Blood Group",
    fill="#000000",
    font=("Inter Regular", 9 * -1)
)

canvas.create_text(     #Stocks Record Label
    1261.0,
    75.0,
    anchor="nw",
    text="Record",
    fill="#000000",
    font=("Inter Bold", 10 * -1)
)

canvas.create_rectangle(        #Line Below Stocks Label
    1259.6173095703125,
    61.8785400390625,
    1486.287109375,
    62.8785400390625,
    fill="#000000",
    outline="")

canvas.create_text(     #Stocks Label
    1259.0,
    34.0,
    anchor="nw",
    text="Stocks",
    fill="#000000",
    font=("Inter Regular", 18 * -1)
)
  
canvas.create_rectangle(    #Database Label Background
    34.0,
    325.0,
    1390.0,
    386.0,
    fill="#000000",
    outline="")


canvas.create_text(     #Database Label
    634.0,
    336.0,
    anchor="nw",
    text="DATABASE",
    fill="#FFFFFF",
    font=("Inter Bold", 30 * -1)
)
       #-----------        Table            --------#
style = ttk.Style()
style.theme_use("clam")
style.configure("Treeview.Heading", background="#6fc8e0", relief="ridge")
table = ttk.Treeview(window, columns=(1,2,3,4,5,6,7),show="headings")   #Table
table.column(1,anchor=CENTER, stretch=NO,width=150)
table.column(2,anchor=CENTER, stretch=NO,width=200)
table.column(3,anchor=CENTER, stretch=NO,width=200)
table.column(4,anchor=CENTER, stretch=NO,width=200)
table.column(5,anchor=CENTER, stretch=NO,width=200)
table.column(6,anchor=CENTER, stretch=NO,width=200)
table.column(7,anchor=CENTER, stretch=NO,width=200)
table.place(x=34, y=386)

     #-----------     Placing Main Frame        --------#
window.resizable(False, False)
window.title("RED SAVERS")
window.mainloop()
