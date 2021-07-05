# Aly Mohammed Taha Hazem       - 17-00150
# Amr Ahmed Hussien             - 17-00105
# Mohamed Samir Mohamed         - 17-00267
# Ali Mohammed Khalil           - 17-00309

import pickle
from tkinter import *
from PIL import ImageTk, Image
from bs4 import BeautifulSoup
from sklearn.metrics import accuracy_score
from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
import time
import matplotlib.pyplot as plt
from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import (FigureCanvasTkAgg, NavigationToolbar2Tk)
from tkinter import filedialog as fd


def model(reviewslist):
    global outputList
    outputList = []
    model = pickle.load(open('savedModel/finalized_model.sav', 'rb'))
    X_test = pickle.load(open('savedModel/X_test.sav', 'rb'))
    y_test = pickle.load(open('savedModel/y_test.sav', 'rb'))
    tfidf = pickle.load(open('savedModel/tfidf.sav', 'rb'))
    y_pred = model.predict(X_test)

    score = accuracy_score(y_test, y_pred)
    print("ML Done with score = ", score)

    for review in reviewslist:
        text_tfidf = tfidf.transform([review])
        text_predict = model.predict(text_tfidf)
        rate = text_predict[0]
        finishReview = {'text': review, 'rate': rate}
        outputList.append(finishReview)
    print(outputList)

def amazonLink(url):
    global reviewsList
    reviewsList = []
    option = webdriver.ChromeOptions()
    option.add_argument("--headless")
    driver = webdriver.Chrome(executable_path=ChromeDriverManager().install(), options=option)
    for x in range(1,999):
        driver.get(url+f'&pageNumber={x}')
        soup = BeautifulSoup(driver.page_source, 'html.parser')
        reviews = soup.find_all('div', {'data-hook': 'review'})
        try:
            for item in reviews:
                review = item.find('span', {'data-hook': 'review-body'}).text.strip()
                reviewsList.append(review)
        except:
            pass
        if soup.find('li', {'class': 'a-disabled a-last'}):
            break
    driver.quit()
    model(reviewsList)

def youtubeLink(url):
    global reviewsList
    reviewsList = []
    option = webdriver.ChromeOptions()
    option.add_argument("--headless")
    driver = webdriver.Chrome(executable_path=ChromeDriverManager().install(), options=option)
    driver.get(url)
    time.sleep(1.5)
    prev_h = 0
    while True:
        height = driver.execute_script("""
                function getActualHeight() {
                    return Math.max(
                        Math.max(document.body.scrollHeight, document.documentElement.scrollHeight),
                        Math.max(document.body.offsetHeight, document.documentElement.offsetHeight),
                        Math.max(document.body.clientHeight, document.documentElement.clientHeight)
                    );
                }
                return getActualHeight();
            """)
        driver.execute_script(f"window.scrollTo({prev_h},{prev_h + 700})")
        time.sleep(1.5)
        prev_h +=700
        if prev_h >= height:
            break
    soup = BeautifulSoup(driver.page_source, 'html.parser')
    driver.quit()
    comment_div = soup.select("#content #content-text")
    for x in comment_div:
        reviewsList.append(x.text.replace("\n", " "))
    model(reviewsList)

def showPage1():
    global myLabel1
    global myLabel2
    global myLabel3
    global myLabel4
    global myLabel5
    global mybutton
    global label1
    myLabel1 = Label(root, text="Welcome to", bg='#2B2D4C', fg='white', font="highlightFont")
    myLabel1.config(font=("Bree Serif", 15))
    myLabel1.place(x=60, y=90)
    myLabel2 = Label(root, text="Feedbacker", bg='#2B2D4C', fg='white', font="highlightFont")
    myLabel2.config(font=("Bree Serif", 20))
    myLabel2.place(x=60, y=120)
    myLabel3 = Label(root, text="A faster way to make your decision", bg='#2B2D4C', fg='white', font="highlightFont")
    myLabel3.config(font=("Bree Serif", 17))
    myLabel3.place(x=100, y=180)
    myLabel4 = Label(root, text="we help you find your best item by analyzing the", bg='#2B2D4C', fg='white',
                     font="highlightFont")
    myLabel4.config(font=("Bree Serif", 12))
    myLabel4.place(x=100, y=240)
    myLabel5 = Label(root, text="previous feedbacks of the customers.", bg='#2B2D4C', fg='white', font="highlightFont")
    myLabel5.config(font=("Bree Serif", 12))
    myLabel5.place(x=100, y=270)
    image2 = Image.open("img/get-start.png")
    image2 = image2.resize((150, 50), Image.ANTIALIAS)
    test2 = ImageTk.PhotoImage(image2)
    mybutton = Button(root, text="Get started", bg='#2B2D4C', activebackground='#2B2D4C', fg='#2B2D4C',
                      command=moveToPage2, image=test2, highlightthickness=0, bd=0)
    mybutton.config(font=("Bree Serif", 15))
    mybutton.place(x=60, y=360)

    image1 = Image.open("img/chart.png")
    image1 = image1.resize((300, 300), Image.ANTIALIAS)
    test = ImageTk.PhotoImage(image1)
    label1 = Label(image=test, bg='#2B2D4C')
    label1.image = test
    label1.place(x=550, y=90)
    image2 = Image.open("img/amazon-logo.png")
    image2 = image2.resize((150, 58), Image.ANTIALIAS)
    test_img = ImageTk.PhotoImage(image2)
    amazonImg = Label(image=test_img, bg='#2B2D4C')
    amazonImg.image = test_img
    amazonImg.place(x=280, y=430)
    image3 = Image.open("img/youtube-logo.png")
    image3 = image3.resize((150, 64), Image.ANTIALIAS)
    test_img = ImageTk.PhotoImage(image3)
    youtubeImg = Label(image=test_img, bg='#2B2D4C')
    youtubeImg.image = test_img
    youtubeImg.place(x=480, y=415)
    root.mainloop()


def openFile():
    global reviewsList
    global fileFlag
    reviewsList = []
    filename = fd.askopenfilename()
    with open(filename+"") as f:
        lines = f.readlines()
    for x in lines:
        reviewsList.append(x.replace("\n",""))
    fileFlag = True



def showPage2():
    global myLabel6
    global myLabel7
    global myLabel8
    global myLabel9
    global searchImgLabel
    global letsGoButton
    global textinput
    global browseButton
    global fileFlag
    fileFlag = False
    myLabel8 = Label(root, text="Add links from Youtube or Amazon or browse from existing text file", bg='#2B2D4C', fg='white', font="highlightFont")
    myLabel8.config(font=("Bree Serif", 15))
    myLabel8.place(x=150, y=50)
    myLabel6 = Label(root, text="Put product's link here and Go", bg='#2B2D4C', fg='white', font="highlightFont")
    myLabel6.config(font=("Bree Serif", 15))
    myLabel6.place(x=170, y=150)
    textinput = Text(root, bg="#40425E", fg="#ffffff", bd="0", height=1, width=60, padx=10)
    textinput.place(x=58, y=200)
    searchImg = Image.open("img/search.png")
    searchImg = searchImg.resize((17, 17), Image.ANTIALIAS)
    searchImg = ImageTk.PhotoImage(searchImg)
    searchImgLabel = Label(image=searchImg, bg='#2B2D4C')
    searchImgLabel.image = searchImg
    searchImgLabel.place(x=560, y=198)
    myLabel7 = Label(root, text="Invalid Link", bg='#2B2D4C', fg='red', font="highlightFont")
    myLabel7.config(font=("Bree Serif", 15))
    myLabel9 = Label(root, text="Browse file", bg='#2B2D4C', fg='white', font="highlightFont")
    myLabel9.config(font=("Bree Serif", 15))
    myLabel9.place(x=685, y=130)
    browseFile = Image.open("img/browseFile.png")
    browseFile = browseFile.resize((75, 68), Image.ANTIALIAS)
    browseFile = ImageTk.PhotoImage(browseFile)
    browseButton = Button(root, text="Get started", bg='#2B2D4C', activebackground='#2B2D4C', fg='#2B2D4C',
                          command=openFile, image=browseFile, highlightthickness=0, bd=0)
    browseButton.config(font=("Bree Serif", 15))
    browseButton.place(x=700, y=180)
    letsGo = Image.open("img/lets-go-button.png")
    letsGo = letsGo.resize((183, 74), Image.ANTIALIAS)
    letsGo = ImageTk.PhotoImage(letsGo)
    letsGoButton = Button(root, text="Get started", bg='#2B2D4C', activebackground='#2B2D4C', fg='#2B2D4C', command=moveToPage3, image=letsGo, highlightthickness=0, bd=0)
    letsGoButton.config(font=("Bree Serif", 15))
    letsGoButton.place(x=358, y=285)
    root.mainloop()


def showPage3():
    sum = 0
    one = 0
    two = 0
    three = 0
    four = 0
    five = 0
    for x in outputList:
        rate = int(x["rate"])
        sum += rate
        if rate == 1:
            one+=1
        elif rate == 2:
            two+=1
        elif rate == 3:
            three+=1
        elif rate == 4:
            four+=1
        elif rate == 5:
            five+=1
    avg = sum / len(outputList)
    print(avg)
    fig = Figure(figsize=(5, 4), dpi=100, facecolor='#2B2D4C')
    ax = fig.add_subplot(111)
    ax.bar([1, 2, 3, 4, 5], [one, two, three, four, five], width=0.5, bottom=None, color=['#1F77B4', '#FE7F0E', '#2BA02D', '#D52728', '#9766BC'])
    ax.set_facecolor("#2B2D4C")
    ax.spines['bottom'].set_color('white')
    ax.spines['top'].set_color('#2B2D4C')
    ax.spines['right'].set_color('#2B2D4C')
    ax.spines['left'].set_color('white')
    ax.tick_params(axis='x', colors='white')
    ax.tick_params(axis='y', colors='white')
    ax.set_title('Ratings Cloumns Chart', fontsize=18, color="white")
    canvas = FigureCanvasTkAgg(fig, master=root)
    canvas.draw()
    canvas.get_tk_widget().place(x=0, y=0)
    fig1 = Figure(figsize=(5, 4), dpi=100, facecolor='#2B2D4C')
    ax1 = fig1.add_subplot(111)
    patches, texts, pcts = ax1.pie([one, two, three, four, five], labels=[1, 2, 3, 4, 5], autopct='%1.0f%%', shadow=True, startangle=90)
    for i, patch in enumerate(patches):
        texts[i].set_color(patch.get_facecolor())
    plt.setp(texts, fontweight=600)
    ax1.set_title('Ratings Pie Chart', fontsize=18, color="white")
    plt.tight_layout()
    canvas1 = FigureCanvasTkAgg(fig1, master=root)
    canvas1.draw()
    canvas1.get_tk_widget().place(x=450, y=0)


def moveToPage2():
    myLabel1.place_forget()
    myLabel2.place_forget()
    myLabel3.place_forget()
    myLabel4.place_forget()
    myLabel5.place_forget()
    mybutton.place_forget()
    label1.place_forget()
    showPage2()

def clearPage2():
    global textinput
    global myLabel7
    global myLabel8
    global browseButton
    global myLabel9
    myLabel6.place_forget()
    searchImgLabel.place_forget()
    letsGoButton.place_forget()
    textinput.place_forget()
    myLabel7.place_forget()
    myLabel8.place_forget()
    myLabel9.place_forget()
    browseButton.place_forget()
    root.update()

def moveToPage3():
    global link
    global textinput
    global myLabel7
    global myLabel8
    global reviewsList
    global browseButton
    global fileFlag
    global myLabel9
    if fileFlag == False:
        link = textinput.get("1.0", 'end-1c')
        if "https://www.amazon." in link:
            clearPage2()
            amazonLink(link)
            showPage3()
        elif "https://www.youtube.com" in link:
            clearPage2()
            youtubeLink(link)
            showPage3()
        else:
            myLabel7.place(x=250, y=230)
    else:
        clearPage2()
        model(reviewsList)
        fileFlag = False
        showPage3()





root = Tk(className='Feedbacker')
root.configure(bg='#2B2D4C')
root.geometry("900x500")
root.resizable(width=False, height=False)
showPage1()
