import base64
import config
import math
import io
import json
import mysql.connector as mysqlco
import os
import webbrowser

from datetime import datetime
from pathlib import Path
from tkinter import *
from PIL import Image, ImageTk
from transformers import pipeline as ppl


CONFIG = config.get_db_config()

OUTPUT_PATH = Path(__file__).parent
ASSETS_PATH = OUTPUT_PATH / Path(r"")
SAVING_PATH = OUTPUT_PATH / Path(r"")

MAIL = ""

WINDOW_CLOSING = False

THRESHOLD = 80




class ImageDisplay:
    """Create an miniature image and its zoom version.
    Work with mouseover.
    """
    def __init__(self, canvas, file, x, y):
        self.canvas = canvas
        self.file = file
        self.x = x
        self.y = y

        if self.file:
            image = base64.b64decode(self.file[5])
            pic = Image.open(io.BytesIO(image))

            self.res_min_pic = preprocess_img(pic, 48)
            self.res_large_pic = preprocess_img(pic)

            self.min_pic = self.canvas.create_image(self.x, self.y, image=self.res_min_pic)
            self.canvas.tag_bind(self.min_pic, '<Enter>', self.on_enter)

    def on_enter(self, event):
        self.canvas.itemconfig(self.min_pic, state="hidden")
        self.large_pic = self.canvas.create_image(self.x, self.y, image=self.res_large_pic)
        self.canvas.tag_bind(self.large_pic, '<Leave>', self.on_leave)
        self.canvas.tag_bind(self.large_pic, '<Button-1>', self.on_click)

    def on_leave(self, event):
        self.canvas.delete(self.large_pic)
        self.canvas.itemconfig(self.min_pic, state="normal")
        self.canvas.tag_bind(self.min_pic, '<Enter>', self.on_enter)

    def on_click(self, event):
        name = self.file[1].replace(" ", "").lower()
        date = self.file[2].strftime('%Y-%m-%d').replace("-", "")

        filename = f"image_{name}{date}.png"
        save_path = os.path.join(SAVING_PATH, filename)

        with open(save_path, "wb") as save_file:
            image = base64.b64decode(self.file[5])
            save_file.write(image)
            print("saved")


#### - DATABASE

def count_archives_row():
    """Get the number of entries in a table"""
    try:
        db = mysqlco.connect(**CONFIG)
        cursor = db.cursor()

        # Get the count of archives rows
        sql = f"""SELECT count(*) as no from tblArchives;"""
        cursor.execute(sql)
        result = cursor.fetchone()
        no_record = result[0]

        return no_record

    except Exception as e:
        print(f"Error 'count_archives_row': {e}")
        return False

    finally:
        if db.is_connected():
            db.close
            cursor.close()

def get_archives(offset):
    """Get a batch of archive records and send a tuple list"""
    try:
        db = mysqlco.connect(**CONFIG)
        cursor = db.cursor()

        sql = f"""SELECT * FROM tblArchives LIMIT {str(offset)}, {str(5)};"""
        cursor.execute(sql)
        query_result = cursor.fetchmany(5)  ## - /!\ get a tuple list

        ## - Modification id's to display a number between 1 and 5 
        ## - instead of the entry number and send a new tuple list.
        result_batch = []
        for number, result in enumerate(query_result, start=1):
            modified_tuple = (number,) + result[1:]
            result_batch.append(modified_tuple)

        return result_batch, query_result[-1][0] # for pagination

    except Exception as e:
        print(f"Error 'get_archives': {e}")
        ## - Default return to avoid a ug
        return [("Name","date","access_result","result", "picture")], 1

    finally:
        if db.is_connected():
            db.close
            cursor.close()

def save_in_db(name, access_result, score, path):
    """Save the prediction information into SQL Database
    > Information save : Name, Datetime, Access_Result, Score and Score
    """

    ## - convert Image to binaryData
    with open(path, 'rb') as file:
        file_data = file.read()
    binary_picture = base64.b64encode(file_data).decode('utf-8')

    try:
        db = mysqlco.connect(**CONFIG)
        cursor = db.cursor()

        now = datetime.now()
        date = now.strftime("%Y-%m-%d %H:%M:%S")

        sql = f"""
                INSERT INTO tblArchives (name, date, access_result, score, picture)
                VALUES ("{name}", 
                        "{date}",
                        "{access_result}",
                        "{score}",
                        "{binary_picture}");
                """
        # print(sql)
        cursor.execute(sql)
        db.commit()

    except Exception as e:
        print(f"Error 'save_in_db' : {e}")

    finally:
        if db.is_connected():
            db.close
            cursor.close()

def verify_login(username, password):
    """Verify if username and password match with authentification Database"""
    try:
        db = mysqlco.connect(**CONFIG)
        cursor = db.cursor()

        sql = f"""SELECT * FROM tblRegistration
                  WHERE auth='{username}' AND password='{password}';"""
        cursor.execute(sql)
        log_result = cursor.fetchone()

        if not log_result:
            return False
        else:
            return True
    except Exception as e:
        print(f"Error 'verify_login': {e}")

    finally:
        if db.is_connected():
            db.close
            cursor.close()


#### - GENERAL UTILS

def change_button(event, canvas, button, img_initial, img_after, text_button):
    """Change the color button when mouse pass over it"""
    canvas.itemconfig(button, image=img_after)
    canvas.itemconfig(text_button, fill="#161225")
    canvas.tag_bind(button, "<Leave>", lambda event: restore_button(event,
                        canvas, button, img_initial, img_after, text_button))

def change_color(entry):
    """change the font color for history access_result"""
    if entry == "ACCESS GRANTED": return '#19D215'
    elif entry == "RESCAN REQUIRED": return '#D28715'
    else: return '#D21542'

def delete_items(canvas, upload_button, upload, text_upload, img_icn_upload_wh):
    """Delete upload button items (1st upload) to display prediction"""
    canvas.delete(upload_button)
    canvas.delete(upload)
    canvas.delete(text_upload)
    canvas.delete(img_icn_upload_wh)

def relative_to_assets(path: str) -> Path:
    return ASSETS_PATH / Path(path)

def restore_button(event, canvas, button, img_initial, img_after, text_button):
    """Change the button color to initial state"""
    canvas.itemconfig(button, image=img_initial)
    canvas.itemconfig(text_button, fill="#FFFFFF")
    canvas.tag_bind(button, "<Enter>", lambda event: change_button(event, 
                        canvas, button, img_initial, img_after, text_button))

def update_text(canvas, text_item, text, fill="#FFFFFF"): 
    """Update a text into the tkinter canvas
    >>> update_text(canvas, foo_item, "fooo", "#336699")"""
    canvas.itemconfig(text_item, text=text, fill=fill)


#### - HISTORY - Last Checks

def display_entries(canvas, result_batch, last_id, page, fe_name_item, fe_date_item, 
    fe_access_item, fe_score_item, se_name_item, se_date_item, se_access_item, 
    se_score_item, te_name_item, te_date_item, te_access_item, te_score_item, 
    foe_name_item, foe_date_item, foe_access_item, foe_score_item, fie_name_item, 
    fie_date_item, fie_access_item, fie_score_item):

    ## - page
    update_text(canvas, page, str(math.ceil(last_id / 5)),'#DCDDFF')

    for entry in result_batch:
        font_color = change_color(entry[3])

        match entry[0]:
            case 1:     #### - first entry
                update_text(canvas, fe_name_item, entry[1],'#DCDDFF')
                update_text(canvas, fe_date_item, entry[2],'#DCDDFF')
                update_text(canvas, fe_access_item, entry[3], font_color)
                update_text(canvas, fe_score_item, f"{entry[4]}%",'#DCDDFF')
                img_1 = ImageDisplay(canvas, entry, 461.0, 150.0)
            case 2:     #### - second entry
                update_text(canvas, se_name_item, entry[1],'#DCDDFF')
                update_text(canvas, se_date_item, entry[2],'#DCDDFF')
                update_text(canvas, se_access_item, entry[3],font_color)
                update_text(canvas, se_score_item, f"{entry[4]}%",'#DCDDFF')
                img_2 = ImageDisplay(canvas, entry, 461.0, 217.0)
            case 3:     #### - third entry
                update_text(canvas, te_name_item, entry[1],'#DCDDFF')
                update_text(canvas, te_date_item, entry[2],'#DCDDFF')
                update_text(canvas, te_access_item, entry[3],font_color)
                update_text(canvas, te_score_item, f"{entry[4]}%",'#DCDDFF')
                img_3 = ImageDisplay(canvas, entry, 461.0, 289.0)
            case 4:     #### - fourth entry
                update_text(canvas, foe_name_item, entry[1],'#DCDDFF')
                update_text(canvas, foe_date_item, entry[2],'#DCDDFF')
                update_text(canvas, foe_access_item, entry[3],font_color)
                update_text(canvas, foe_score_item, f"{entry[4]}%",'#DCDDFF')
                img_4 = ImageDisplay(canvas, entry, 461.0, 361.0)
            case 5:     #### - fifth entry
                update_text(canvas, fie_name_item, entry[1],'#DCDDFF')
                update_text(canvas, fie_date_item, entry[2],'#DCDDFF')
                update_text(canvas, fie_access_item, entry[3],font_color)
                update_text(canvas, fie_score_item, f"{entry[4]}%",'#DCDDFF')
                img_5 = ImageDisplay(canvas, entry, 461.0, 432.0)

def pagination(offset, canvas, arrow_left, arrow_right, page, fe_name_item, 
    fe_date_item, fe_access_item, fe_score_item, se_name_item, se_date_item,
    se_access_item, se_score_item, te_name_item, te_date_item, te_access_item, 
    te_score_item, foe_name_item, foe_date_item, foe_access_item, foe_score_item, 
    fie_name_item, fie_date_item, fie_access_item, fie_score_item):

    count_rec = count_archives_row()
    result_batch, last_id = get_archives(offset)

    display_entries(canvas, result_batch, last_id, page, fe_name_item, 
    fe_date_item, fe_access_item, fe_score_item, se_name_item, se_date_item, 
    se_access_item, se_score_item, te_name_item, te_date_item, te_access_item, 
    te_score_item, foe_name_item, foe_date_item, foe_access_item, foe_score_item, 
    fie_name_item, fie_date_item, fie_access_item, fie_score_item)

    # Show buttons 
    back = offset - 5
    next = offset + 5

    if(count_rec >= next): 
        canvas.tag_bind(arrow_right, '<Button-1>', 
            lambda event: pagination(next, canvas, arrow_left, arrow_right, page,
                fe_name_item, fe_date_item, fe_access_item, fe_score_item, 
                se_name_item, se_date_item, se_access_item, se_score_item, 
                te_name_item, te_date_item, te_access_item, te_score_item, 
                foe_name_item, foe_date_item, foe_access_item, foe_score_item, 
                fie_name_item, fie_date_item, fie_access_item, fie_score_item))
    if(back >= 0):
        canvas.tag_bind(arrow_left, '<Button-1>', 
            lambda event: pagination(back, canvas, arrow_left, arrow_right, page,
                fe_name_item, fe_date_item, fe_access_item, fe_score_item, 
                se_name_item, se_date_item, se_access_item, se_score_item, 
                te_name_item, te_date_item, te_access_item, te_score_item, 
                foe_name_item, foe_date_item, foe_access_item, foe_score_item, 
                fie_name_item, fie_date_item, fie_access_item, fie_score_item))


#### - INFORMATION

def git_link(event): webbrowser.open("https://github.com/CharleyDL/")

def linkedin_link(event): webbrowser.open("https://linkedin.com/in/charleylebarbier/")

def mail_report(event):
    webbrowser.open(f"mailto:?to={MAIL}&subject=Bug Report : yourbug", new=1)

#### - LOGIN FORM

def button_valid_login(canvas, username, password):
    username_get = username.get()
    password_get = password.get()

    result_auth = verify_login(username_get, password_get)

    if (username_get != 'Username') and (password_get != 'Password'):
        # if username_get == AUTH and password_get == PWRD:
        #     canvas.delete("error")
        #     return True
        if result_auth == True:
            canvas.delete("error")
            return True
        else:
            canvas.delete("error")
            canvas.create_text(
                615.0, 305.0, anchor="nw",
                text="Invalid login Token",
                fill="#D21542",
                font=("Rubik Light", 12 * -1),
                tags='error'
            )
    else:
        canvas.delete("error")

        if username_get == 'Username' and password_get == 'Password':
            canvas.create_text(
                608.0, 296.0, anchor="nw",
                text="Enter your username\n      and password",
                fill="#D21542",
                font=("Rubik Light", 12 * -1),
                tags='error'
            )
        elif username_get == 'Username':
            canvas.create_text(
                602.0, 305.0, anchor="nw",
                text="The Username is empty",
                fill="#D21542",
                font=("Rubik Light", 12 * -1),
                tags='error'
            )
        elif password_get == 'Password':
            canvas.create_text(
                602.0, 305.0, anchor="nw",
                text="The Password is empty",
                fill="#D21542",
                font=("Rubik Light", 12 * -1),
                tags='error'
            )

def on_password(event, password):
    if password.get() == "Password":
        password.delete(0, 'end')
        password.config(show="*")

def out_password(event, password):
    if not password.get():
        password.insert(0, "Password")
        password.config(show="")

def on_username(event, username):
    if username.get() == "Username":
        username.delete(0, 'end')

def out_username(event, username):
    if not username.get():
        username.insert(0, "Username")
        username.config(show="")


#### - PREDICTION

def id_employee(id):
    """Research and return employee information"""
    with open('C:/Users/utilisateur/Documents/SIMPLON_x_ISEN/env_VSC-Windows/Cas_pratique/employees_info.json', 'r', encoding='utf-8') as json_file:
        data = json.load(json_file)
        info = data[str(id)]

    employee_name = info['nom']
    employee_year = info['annee_embauche']
    employee_gender = info['genre']
    employee_job = info['poste']

    return [employee_name, employee_year, employee_gender, employee_job]

def model_LREyes(file_path):
    """Load model for Left or Right Eye detection"""
    ppl_lrEye = ppl(task='image-classification', model='IstarD/VIT_Iris_LR')
    return ppl_lrEye(Image.open(file_path))

def model_LeftEye(file_path):
    """Load model and use it for left eye employees detection"""
    ppl_leftEye = ppl(task="image-classification", model="IstarD/VIT_Iris_Left")
    return ppl_leftEye(Image.open(file_path))

def model_RightEye(file_path):
    """Load model and use it for right eye employees detection"""
    ppl_rightEye = ppl(task='image-classification', model='IstarD/VIT_Iris_Right')
    return ppl_rightEye(Image.open(file_path))

def preprocess_img(path_photo, WIDTH=176):
    """Resizing picture with fixed width size"""
    # WIDTH = 176

    factor = WIDTH / path_photo.width
    pic_height = int(path_photo.height * factor)
    pic_resize = path_photo.resize((WIDTH, pic_height), Image.ANTIALIAS)
    photo = ImageTk.PhotoImage(pic_resize)

    return photo

def valid_access(score):
    if score >= THRESHOLD:
        return "ACCESS GRANTED", "#19D215"
    elif (score >= 50) and (score < THRESHOLD):
        return "RESCAN REQUIRED", "#D28715"
    else:
        return "ACCESS DENIED", "#D21542"


#### - WINDOW CONFIG

def center_window(window):
    """Center window in relation to the screen"""
    window.update_idletasks()
    width = window.winfo_width()
    height = window.winfo_height()

    screen_width = window.winfo_screenwidth()
    screen_height = window.winfo_screenheight()

    x = (screen_width - width) // 2
    y = (screen_height - height) // 3

    window.geometry(f"{width}x{height}+{x}+{y}")

def close_window(window):
    """Close the app window"""
    global WINDOW_CLOSING
    if not WINDOW_CLOSING:
        WINDOW_CLOSING = True
        window.destroy()
