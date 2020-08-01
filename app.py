import numpy as np
import os, sys
from PIL import Image
import streamlit as st
import base64 #encode images to display format web
import cv2
from tensorflow.keras.models import load_model

#app layout
class AppgoLayout:

    def __init__(self):

        self.styleholder = st.empty()

    def call_markdown(self):
       
        cs = self.cssht()
        return cs

    def bytesTo64(self, bytes_file, header):
        encoded = base64.b64encode(bytes_file).decode()
        base64file = "data:%s;base64,%s" % (header, encoded)
        return base64file


    def setBackground(self, filename, filetype='image/jpeg'):
        fig = filename
        image = open(fig, 'rb').read()
        image64 = self.bytesTo64(image, filetype)
        return image64

    def cssht(self):

        footer = "./stimages/index.jpeg"

        csstyle = f"""<style>

                    html{{
                    background-color: #fdfefe !important;
                    }}

                    .reportview-container .main .block-container {{
                    max-width:1000px;
                    
                    }}
   
                    .reportview-container .main footer{{
                    background:url({self.setBackground(footer, 'image/jpg')});
                    background-repeat: no-repeat;
                    background-size:150px;
                    background-position: right;
                    text-align: left;
                    opacity: 1;
                    padding: 20px;
                    max-width: 100%;
                    background-color:  #ebf5fb;
                    width: 100% !important;

                    }}
                  
                    .fullScreenFrame div{{
                        display: flex;
                        justify-content: center;
                    }}

                    .markdown-text-container.stMarkdown{{
                    font-size:1px;
                    }}

                    .reportview-container .markdown-text-container {{
                    position: relative;
                    text-align: justify;
                    }}
                    
                    .sidebar{{
                    background-color: #ebf5fb;
                    }}
                       
                    </style>"""

        return csstyle

class Classificador:
    """Class classificador"""
    def __init__(self):

        model_file = "./resources/trained_model_thumbs_job.hdf5"
        self.model = load_model(model_file)
        self.min_th = np.array([0,133,85], np.uint8)
        self.max_th = np.array([255,170,125], np.uint8 )


    def up_down(self, frame):

        if frame is not None:

            (h, w) = frame.shape[:2]
            x = w // 2
            y = h // 2
            upper_left = (int(x-w/6), int(y-h/4))
            bottom_right = (int(x+w/4), int((y+h/4)))
            cv2.rectangle(frame, upper_left, bottom_right, (0, 255, 0), 2)
            xcc = int((int(x-w/2) + int((x+w/8)-300))/2)
            ycc = int((int(y-h/2) +int((y+h/4)-100)) /2)
            rect_img = frame[upper_left[1] : bottom_right[1], upper_left[0] : bottom_right[0]]
            color_ycc = cv2.cvtColor(rect_img, cv2.COLOR_BGR2YCR_CB)

            new_img_array = cv2.resize(color_ycc, dsize=(100, 100))
            input_img = np.array(new_img_array).reshape(-1, 100,100,3)
            normalized = input_img/255.0
            #predicting
            y_pred = self.model.predict(normalized)
            y_pred = np.argmax(y_pred, axis=-1)

            skin  = cv2.inRange(color_ycc, self.min_th, self.max_th)
            opening = cv2.morphologyEx(skin, cv2.MORPH_OPEN, np.ones((5,5), np.uint8), iterations=3)
            sure_bg = cv2.dilate(opening,np.ones((3,3),np.uint8), iterations=2)
            cnts = cv2.findContours(sure_bg, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
            cnts = cnts[0] if len(cnts) == 2 else cnts[1]

            if len(cnts) > 0:
                for contour in cnts:
                    x, y, w, h = cv2.boundingRect(contour)
                    xc = int((x + x+w)/2)
                    yc = int((y+y+h)/2)
                if y_pred==0:
                    text = "{}".format(":(")
                    cv2.putText(rect_img, text, (xc, yc), cv2.FONT_HERSHEY_SIMPLEX, 2, (0, 255, 0), 3)
                elif y_pred == 1:
                    text = "{}".format("(:")
                    cv2.putText(rect_img, text, (xc, yc), cv2.FONT_HERSHEY_SIMPLEX, 2, (0, 255, 0), 3)
                else:
                    text = "{}".format("No hands!!!")
                    cv2.putText(rect_img, text, (xc, yc), cv2.FONT_HERSHEY_SIMPLEX,  0.5, (0, 255, 0), 2)
            else:
                text = "{}".format("put your hand here!!!")
                cv2.putText(rect_img, text, (xcc, ycc), cv2.FONT_HERSHEY_SIMPLEX,  0.5, (0, 255, 0), 2)
        frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        return frame


    def image_classify(self, pathfolder):

        lista = os.listdir(pathfolder)

        lista_img = []
        y_test = []
        y_predicted = []
        count = 0

        for i in lista:
            label = i.split(".")[0]
            frame = cv2.imread(pathfolder+"/"+ i)
            (h, w) = frame.shape[:2]
            x = w // 2
            y = h // 2

            color_ycc = cv2.cvtColor(frame, cv2.COLOR_BGR2YCR_CB)
            new_img_array = cv2.resize(color_ycc, dsize=(100, 100))
            input_img = np.array(new_img_array).reshape(-1, 100,100,3)
            normalized = input_img/255.0
            y_pred = self.model.predict(normalized)
            y_pred = np.argmax(y_pred, axis=-1)
 
            if y_pred==0:
                text = "{}".format(":( Down")
                cv2.putText(frame, text, (x-100, y), cv2.FONT_HERSHEY_SIMPLEX, 2, (0, 255, 0), 3)
            elif y_pred == 1:
                text = "{}".format("(: Up")
                cv2.putText(frame, text, (x-100, y), cv2.FONT_HERSHEY_SIMPLEX, 2, (0, 255, 0), 3)
            frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            lista_img.append(frame)
            y_test.append(1) if label == "thumbsup"  else y_test.append(0)
            y_predicted.append(y_pred)
            count +=1

        erros = sum(1 for i, j in zip(y_test, y_predicted) if i != j)
        acertos = len(lista_img) - erros
        st.markdown("---")
        st.success('Number of processed images: `%s`\n\nFail: `%s`\n\nSuccess:`%s` ' % (len(lista_img), erros, acertos))
        st.markdown("---")
        st.success("Done!")

        return lista_img


    def show_images(self, lista_img):
        import matplotlib.pyplot as plt
        fig = plt.figure(0)
        count = 0
        for i in range(5):
            for j in range(4):
                ax = plt.subplot2grid((5,4), (i,j))
                count +=1
                img = cv2.resize(lista_img[count-1], (200,200))
                ax.imshow(img)
                plt.axis('off')
            count -= 1

        plt.suptitle("Classified Images")
        plt.subplots_adjust(hspace=0.5, wspace=0.5)
        plt.show()
        st.pyplot(fig)



def main():
    #class applayout
    app = AppgoLayout()
    cs = app.call_markdown()
    app.styleholder.markdown(cs, unsafe_allow_html=True)
    st.markdown("<h1 style= 'font-size:40px; text-align:center; color: #005580;'>Classificador (:thumbsup: | :thumbsdown:)</h5>", unsafe_allow_html=True)
    option = st.sidebar.radio("",("Video", "Images"))
    clc = Classificador()
    if option == "Video":

        image_placeholder = st.empty()
        holderbutton = st.empty()
        if holderbutton.button('Start'):
            stop = holderbutton.button('Stop')
            video = cv2.VideoCapture(0)
            test =  video.isOpened()
            if test ==True:
                while True:
                    _, frame = video.read()
                    frame = cv2.flip(frame, 1)
                    result = clc.up_down(frame)
                    image_placeholder.image(result)
                    if stop:
                        break
            else:
                st.error("can't open camera by")

    if option == "Images":
        try:
            dirname = [di for di in os.listdir("./") if os.path.isdir(os.path.join("./", di))]
            dirname.insert(0,"")
            selected_dir = st.multiselect('Select a directory 📁', dirname)
            if len(selected_dir) == 1:
                selected_dir  = os.path.join('./', selected_dir[0]+'/')
                if st.button("Start"):
                    lista_img = clc.image_classify(selected_dir)
                    clc.show_images(lista_img)

            else:
                st.info("You can insert only one folder at a time!!")
        except Exception as e:
            st.error(e)
            st.error("oh oh :(")


if __name__ == '__main__':
    main()
