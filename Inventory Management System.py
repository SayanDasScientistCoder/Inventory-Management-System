# # Inventory Management System

# ## Product Details:- 
# #### 1. Product ID
# #### 2. Product Name
# #### 3. Product Price
# #### 4. Product Quantity

# In[1]:


import datetime
import os

fd=open(os.path.dirname(__file__)+"\Inventory.csv","a")
fd.close()


# ## Adding Products

# In[2]:


def newId(s):
    l=len(s)
    id_list=[False]*(l+1)
    n=0
    for i in s:
        s1=i.split(",")
        if(s1[0]!=''):
            id_list[int(s1[0])]=True
    
    for i in range(l):
        if(id_list[i]==False):
            break
    
    return i


# In[7]:


def addProduct(name,price,quantity):
    clearEmpty()
    fd1=open(os.path.dirname(__file__)+"\Inventory.csv","r")
    s=fd1.read().split("\n")
    c=newId(s)
    fd1.close()
    
    fd2=open(os.path.dirname(__file__)+"\Inventory.csv","a")
    fd2.write(str(c)+","+name+","+str(price)+","+str(quantity)+"\n")
    fd2.close()


# ## Product Details

# In[15]:


def productDetails(id):
    fd=open(os.path.dirname(__file__)+"\Inventory.csv","r")
    s=fd.read().split("\n")
    
    s2=""
    flag=False
    for i in s:
        s1=i.split(",")
        if(s1[0]==id):
            flag=True
            #print(s1[0],s1[1],s1[2],s1[3],sep="\t")
            s2=s1[0]+","+s1[1]+","+s1[2]+","+s1[3]
            break
    
    #if(flag==False):
    #    print("The product is not found.")       
    fd.close()
    return s2


# ## Updating Inventory

# In[17]:


import pandas as pd
def updateInventory2(id:int,quantity:int):
    flag=False
    fd=pd.read_csv(os.path.dirname(__file__)+"\Inventory.csv")
    
    l=len(fd)
    for i in range(l):
        if(fd.loc[i,"ID"]==id):
            flag=True
            fd.loc[i,"Quantity"]=fd.loc[i,"Quantity"]+quantity
            break
    
    if(flag==True):
        fd.to_csv(os.path.dirname(__file__)+"\Inventory.csv",index=False)
    else:
        print("Product is not found.")


# In[18]:


def updateInventory(id:str,quantity:int):
    fd=open(os.path.dirname(__file__)+"\Inventory.csv","r")
    s=fd.read().split("\n")
    
    flag=False
    for i in range(len(s)):
        s1=s[i].split(",")
        if(s1[0]==id):
            flag=True
            
            if(quantity<0 and int(s1[3])<-quantity):
                print("Not enough quantity present.")
                flag=False
            else:
                s[i]=s1[0]+","+s1[1]+","+s1[2]+","
                s[i]+=str(int(s1[3])+quantity)
        
        s[i]+="\n"
            
    
    fd.close()
    if(flag==True):
        fd=open(os.path.dirname(__file__)+"\Inventory.csv","w")
        fd.writelines(s)
        fd.close()
        clearEmpty()
    else:
        print("The product is not found.")
    
    return flag


# ## Updating The Unit Price

# In[2]:


def updatePrice(id,price:int):
    fd=open(os.path.dirname(__file__)+"\Inventory.csv","r")
    s=fd.read().split("\n")
    
    flag=False
    for i in range(len(s)):
        s1=s[i].split(",")
        if(s1[0]==id):
            flag=True
            s[i]=s1[0]+","+s1[1]+","+str(price)+","+s1[3]
            
        s[i]+="\n"
            
    
    fd.close()
    if(flag==True):
        fd=open(os.path.dirname(__file__)+"\Inventory.csv","w")
        fd.writelines(s)
        fd.close()
        clearEmpty()
    else:
        print("The product is not found.")
    
    return flag


# ## Deleting Products

# In[20]:


def deleteProduct(id):
    fd=open(os.path.dirname(__file__)+"\Inventory.csv","r")
    s=fd.read().split("\n")
    
    flag=False
    j=0
    for i in range(len(s)):
        s1=s[i].split(",")
        if(s1[0]==id):
            flag=True
            j=i
        
        s[i]+="\n"
    fd.close()
    
    if(flag==True):
        fd=open(os.path.dirname(__file__)+"\Inventory.csv","w")
        fd.writelines(s[:j])
        fd.writelines(s[j+1:])
        fd.close()
        
        clearEmpty()
    else:
        print("The product is not found.")
        
def clearEmpty():
    fd=open(os.path.dirname(__file__)+"\Inventory.csv","r")
    s=fd.read().split("\n")
    s2=""
    for i in s:
        if(i!=""):
            s2+=i+"\n"
    
    fd.close()
    fd=open(os.path.dirname(__file__)+"\Inventory.csv","w")
    fd.write(s2)
    fd.close()


# ## Generating Purchase and Sales Records

# #### Purchase Details:- 
# #### 1. Merchant Name
# #### 2. Contact Details of the merchant
# #### 3. Product ID
# #### 4. Quantity 
# #### 5. Total Cost
# #### 6. Purchase Time

# In[34]:


def purchase():
    fd=open(os.path.dirname(__file__)+"\Purchase.csv","a")
    
    s=[]
    merchant=input("Please enter the merchant name:- ")
    contact=input("Please enter the contact details of the merchant:- ")
    while(True):
        id=input("Please enter the product id:- ")
        q=int(input("Please enter the quantity:-"))
        
        if(updateInventory(id,q)==True):
            s.append(productDetails(id))
            p=int(s[len(s)-1].split(",")[2])
            fd.write(merchant+","+contact+","+id+","+str(q)+","+str(p*q)+","+str(datetime.datetime.now())+"\n")
            s[len(s)-1]+=","+str(q)+","+str(p*q)
        flag=input("Do you want to purchase more from the current merchant(Yes:- 1 or No:- 0)?:- ")
        if(flag=="0"):
            break
    fd.close()
    
    d=datetime.datetime.now()
    filepath=os.path.dirname(__file__)+"\\Purchasing Receipts\\"+merchant+" "+str(d.date())+" "+d.strftime("%H-%M-%S.%f")+".csv"
    fd=open(filepath,"a")
    print("_"*200)
    print("Purchasing Receipt on ",datetime.datetime.now(),":- ",sep="")
    fd.write("Purchasing Receipt on:-,"+str(datetime.datetime.now())+"\n")
    print("Merchant Name:- "+merchant,sep="")
    fd.write("Merchant Name:-,"+merchant+"\n")
    print("Merchant Contact:- "+contact)
    fd.write("Merchant Contact:-,"+contact+"\n")
    print("_"*200)
    print("Serial Number\tProduct ID\tProduct Name\tUnit Price\t\tQuantity Purchased\tTotal Price")
    fd.write("Serial Number,Product ID,Product Name,Unit Price,Quantity Purchased,Total Price\n")
    print("_"*200)
    
    t=0
    for i in range(len(s)):
        s1=s[i].split(",")
        print((i+1),"\t",s1[0],s1[1],s1[2],"\t",s1[4],"\t",s1[5],sep="\t")
        fd.write(str(i+1)+","+s1[0]+","+s1[1]+","+s1[2]+","+s1[4]+","+s1[5]+"\n")
        t+=int(s1[5])
    print("\t\t\t\t\t\t\t\t\tTotal Amount\t",t,sep="\t")
    print("_"*200)
    fd.write(",,,,Total Amount,"+str(t))
    fd.close()


# #### Sales Details:- 
# #### 1. User Name
# #### 2. Contact Details of the user
# #### 3. Product ID
# #### 4. Quantity 
# #### 5. Total Price
# #### 6. Sales Time

# In[31]:


def sales():
    fd=open(os.path.dirname(__file__)+"\Sales.csv","a")
    
    s=[]
    un=input("Please enter your username:- ")
    contact=input("Please enter your contact details:- ")
    while(True):
        id=input("Please enter the product id:- ")
        q=int(input("Please enter the quantity:- "))
        
        if(updateInventory(id,-q)==True):
            s.append(productDetails(id))
            p=int(s[len(s)-1].split(",")[2])
            fd.write(un+","+contact+","+id+","+str(q)+","+str(p*q)+","+str(datetime.datetime.now())+"\n")
            s[len(s)-1]+=","+str(q)+","+str(p*q)
            
        flag=input("Do you want to buy more(Yes:- 1 or No:- 0)?:- ")
        if(flag=="0"):
            break
    fd.close()
    
    d=datetime.datetime.now()
    filepath=os.path.dirname(__file__)+"\\Sales Bills\\"+un+" "+str(d.date())+" "+d.strftime("%H-%M-%S.%f")+".csv"
    fd=open(filepath,"a")
    print("_"*200)
    print("Sales Bill on ",datetime.datetime.now(),":- ",sep="")
    fd.write("Sales Bill on:- "+","+str(datetime.datetime.now())+"\n")
    print("User Name:- ",un,sep="")
    fd.write("User Name:- ,"+un+"\n")
    print("User Contact:- ",contact,sep="")
    fd.write("User Contact:- ,"+contact+"\n")
    print("_"*200)
    print("Serial Number\tProduct ID\tProduct Name\tUnit Price\t\tQuantity Bought\tTotal Price")
    fd.write("Serial Number,Product ID,Product Name,Unit Price,Quantity Bought,Total Price\n")
    print("_"*200)
    t=0
    for i in range(len(s)):
        s1=s[i].split(",")
        print((i+1),"\t",s1[0],s1[1],s1[2],"\t",s1[4],"\t",s1[5],sep="\t")
        fd.write(str(i+1)+","+s1[0]+","+s1[1]+","+s1[2]+","+s1[4]+","+s1[5]+"\n")
        t+=int(s1[5])
    print("\t\t\t\t\t\t\t\t\tTotal Amount\t",t,sep="\t")
    print("_"*200)
    fd.write(",,,,Total Amount,"+str(t))
    fd.close()


# ## Integrating all functions together

# In[46]:


while(True):
    print("Please enter you choice by entering the corresponding numbers associated with the choices:- ")
    print("1. Adding Products")
    print("2. Deleting products")
    print("3. Displaying Product details")
    print("4. Updating Inventory")
    print("5. Updating Price")
    print("6. Purchasing Items")
    print("7. Selling Items")
    print("8. Exiting Options")
    choice=input("Please enter your choice:- ")
    
    match choice:
        case "1":
            name=input("Please enter product name:- ")
            p=int(input("Please enter unint price:- "))
            q=int(input("Please enter available quantity:- "))
            addProduct(name,p,q)
        
        case "2":
            id=input("Please enter id of the product to be deleted:- ")
            deleteProduct(id)

        case "3":
            id=input("Please enter product id:- ")
            print("ID\tName\tUnit Price\tQuantity Available")
            s=productDetails(id).split(",")
            print(s[0],s[1],s[2],s[3],sep="\t")
            
        case "4":
            id=input("Please enter product id:- ")
            q=input("Please enter quantity to be added:- ")
            updateInventory(id,int(q))

        case "5":
            id=input("Please enter id of the product whose unit price is to be updated:- ")
            price=int(input("Please enter the new unit price of the product:- "))
            updatePrice(id,price)
        
        case "6":
            purchase()
            
        case "7":
            sales()
        
        case "8":
            break
        case _:
            print("You have entered an invalid choice. You may please try again.")

