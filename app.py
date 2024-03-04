from tkinter import *
from tkinter import filedialog
from utils import * 


################################################################################


class LoginPage(Frame):
    def __init__(self, window):
        Frame.__init__(self, window)

        self.window = window
        self.canvas = Canvas(
            window,
            bg = 'grey15',
            height = 600, width = 800,
            bd = 0,
            highlightthickness = 0,
            relief = 'ridge'
        )
        self.canvas.pack(fill='both', expand=True)
        self.canvas.place(x = 0, y = 0) 

        ## - IMG
        self.background_img = PhotoImage(file=relative_to_assets('background.png'))
        self.canvas.create_image(400.0, 300.0, image=self.background_img)

        self.back_blur_img = PhotoImage(file=relative_to_assets('back_blur.png'))
        self.canvas.create_image(266.0,300.0, image=self.back_blur_img)

        self.close_icn_img = PhotoImage(file=relative_to_assets('icn_close.png'))
        self.icn_close = self.canvas.create_image(764.0, 36.0, image=self.close_icn_img)
        self.canvas.tag_bind(self.icn_close, '<Button-1>', lambda event: close_window(window))

        self.logo_img = PhotoImage(file=relative_to_assets('logo.png'))
        self.canvas.create_image(289.0, 310.0, image=self.logo_img)

        self.line_usr_img = PhotoImage(file=relative_to_assets('line_usr.png'))
        self.canvas.create_image(666.0, 209.0, image=self.line_usr_img)

        self.line_pswd_img = PhotoImage(file=relative_to_assets('line_pswd.png'))
        self.canvas.create_image(666.0, 282.0, image=self.line_pswd_img)

        ## - INFO CONNECTION
        self.username = Entry(
            window,
            bd=0,
            bg='#161225',
            fg='#FFFFFF',
            width=16,
            font=('Rubik Light', 16 * -1),
        )
        self.username.insert(0, "Username")
        self.username.bind('<FocusIn>', lambda event: on_username(event, self.username))
        self.username.bind('<FocusOut>', lambda event: out_username(event, self.username))
        self.username.place(x=585.0, y=180.0)

        self.password = Entry(
            window,
            bd=0,
            bg='#161225',
            fg='#FFFFFF',
            width=16,
            font=('Rubik Light', 16 * -1),
            exportselection=0
        )
        self.password.insert(0, "Password")
        self.password.bind('<FocusIn>', lambda event: on_password(event, self.password))
        self.password.bind('<FocusOut>', lambda event: out_password(event, self.password))
        self.password.place(x=585.0, y=253.0)

        ## - LOG IN
        self.img_log_rb = PhotoImage(file=relative_to_assets('frame_rb.png'))
        self.img_log_wh = PhotoImage(file=relative_to_assets('frame_log_wh.png'))
        self.log_button_rb = self.canvas.create_image(666.0, 363.0, 
                                                      image=self.img_log_rb)
        self.log = self.canvas.find_withtag(self.log_button_rb)

        self.text_login = self.canvas.create_text(
            644.0, 350.0, anchor='nw',
            text="Log In",
            fill='#FFFFFF',
            font=('Rubik Light', 16 * -1)
        )

        self.canvas.tag_bind(self.log, '<Enter>', lambda event: change_button(event, 
                            self.canvas, self.log, self.img_log_rb, self.img_log_wh, self.text_login))
        self.canvas.tag_bind(self.log, '<Button-1>', lambda event: self.check_login())

        ## - PROFILE
        #### - Github
        self.img_github = PhotoImage(file=relative_to_assets('github.png'))
        github = self.canvas.create_image(623.0, 508.0, image=self.img_github)
        self.canvas.tag_bind(github, '<Button-1>', git_link)

        #### - Linkedin
        self.img__linkedin = PhotoImage(file=relative_to_assets('linkedin.png'))
        linkedin = self.canvas.create_image(711.0, 508.0, image=self.img__linkedin)
        self.canvas.tag_bind(linkedin, '<Button-1>', linkedin_link)

        #### - Bug Report
        self.icn_bug = PhotoImage(file=relative_to_assets('icn_bug.png'))
        mail = self.canvas.create_image(569.0, 33.0, image=self.icn_bug)
        self.canvas.tag_bind(mail, '<Button-1>', mail_report)

    def check_login(self):
        """Check the login and open the loading page"""
        if button_valid_login(self.canvas, self.username, self.password):
            self.destroy()
            Loading(self.window)


class Loading(Frame):
    def __init__(self, window):
        Frame.__init__(self, window)

        self.window = window
        self.canvas = Canvas(
            window,
            bg = 'grey15',
            height = 600, width = 800,
            bd = 0,
            highlightthickness = 0,
            relief = 'ridge'
        )
        self.canvas.pack(fill='both', expand=True)
        self.canvas.place(x = 0, y = 0) 

        ## - IMG
        self.background_img = PhotoImage(file=relative_to_assets('background.png'))
        self.canvas.create_image(400.0, 300.0, image=self.background_img)

        self.load_bck_img = PhotoImage(file=relative_to_assets('loading_bck.png'))
        self.canvas.create_image(400.0, 300.0, image=self.load_bck_img)

        self.logo_img = PhotoImage(file=relative_to_assets('logo.png'))
        self.canvas.create_image(400.0, 284.0, image=self.logo_img)

        self.window.after(1000, self.destroy)
        self.window.after(1000, lambda: self.loading_to_predictHome())

    def loading_to_predictHome(self):
        PredictHome(self.window)


class PredictHome(Frame):
    def __init__(self, window):
        Frame.__init__(self, window)

        self.window = window
        self.canvas = Canvas(
            window,
            bg = 'grey15',
            height = 600, width = 800,
            bd = 0,
            highlightthickness = 0,
            relief = 'ridge'
        )
        self.canvas.pack(fill='both', expand=True)
        self.canvas.place(x = 0, y = 0) 


        ## - Left Panel - Predict Panel

        self.background_img = PhotoImage(file=relative_to_assets('background.png'))
        self.canvas.create_image(400.0, 300.0, image=self.background_img)

        #### - Upload 
        self.frame_large_rb = PhotoImage(file=relative_to_assets('frame_large_rb.png'))
        self.frame_large_wh = PhotoImage(file=relative_to_assets('frame_large_wh.png'))
        self.img_icn_upload_wh = PhotoImage(file=relative_to_assets('icn_upload_white.png'))

        self.upload_button = self.canvas.create_image(266.0, 300.0, image=self.frame_large_rb)
        self.upload = self.canvas.find_withtag(self.upload_button)
        self.icn_upload_wh = self.canvas.create_image(202.0, 300.0, image=self.img_icn_upload_wh)
        self.text_upload = self.canvas.create_text(261.0, 282.0, anchor='nw',
            text="Upload", fill='#FFFFFF', font=('Rubik Medium', 24 * -1))

        # # - Currently bug
        # self.canvas.tag_bind(self.upload, '<Enter>', lambda event: change_button(event, 
        #             self.canvas, self.upload, self.frame_large_rb, self.frame_large_wh, self.text_upload))
        self.image_uploaded = self.canvas.tag_bind(self.upload, '<Button-1>', lambda event: self.load_image())


        #### - Which eye
        self.eye_text_item = self.canvas.create_text(233.0, 211.0, anchor='nw',
            font=('Rubik Light', 10 * -1, 'italic'))

        #### - Employee info
        self.employee_name_item = self.canvas.create_text(48.0, 346.0, anchor='nw',
            font=('Rubik Medium', 10 * -1))
        self.employee_name = self.canvas.create_text(90.0, 346.0, anchor='nw',
            font=('Rubik Light', 10 * -1))

        self.employee_year_item = self.canvas.create_text(48.0, 378.0, anchor='nw',
            font=('Rubik Medium', 10 * -1))
        self.employee_year = self.canvas.create_text(115.0, 378.0, anchor='nw',
            font=('Rubik Light', 10 * -1))

        self.employee_job_item = self.canvas.create_text(48.0, 410.0, anchor='nw',
            font=('Rubik Medium', 10 * -1))
        self.employee_job = self.canvas.create_text(126.0, 410.0, anchor='nw',
            font=('Rubik Light', 10 * -1))

        #### - Prediction Circle
        self.score_eye_item = self.canvas.create_text(447.0, 366.0, anchor='nw',
            font=('Rubik Medium', 12 * -1))

        self.score_employee_item = self.canvas.create_text(323.0, 428.0, anchor='nw',
            font=('Rubik Medium', 48 * -1))

        #### - Access or not
        self.access_item = self.canvas.create_text(48.0, 505.0, anchor='nw',
            font=('Rubik Medium', 16 * -1))

        # -------------------------------------------------------------------- #

        ## - Right Panel - Option Panel

        self.back_right = PhotoImage(file=relative_to_assets('back_blur_right.png'))
        self.canvas.create_image(666.0, 300.0, image=self.back_right)

        self.close_icn_img = PhotoImage(file=relative_to_assets('icn_close.png'))
        self.icn_close = self.canvas.create_image(764.0, 36.0, image=self.close_icn_img)
        self.canvas.tag_bind(self.icn_close, '<Button-1>', lambda event: close_window(window))

        #### - Past Checks - Histo
        self.icn_histo = PhotoImage(file=relative_to_assets('icn_histo.png'))
        self.histo_button = self.canvas.create_image(573.0, 34.0, 
                                                     image=self.icn_histo)
        self.histo = self.canvas.find_withtag(self.histo_button)
        self.canvas.tag_bind(self.histo, '<Button-1>', lambda event: self.to_history())

        #### - Profile
        self.icn_profile = PhotoImage(file=relative_to_assets('icn_large_profile.png'))
        self.canvas.create_image(668, 204.0, image=self.icn_profile)

        self.canvas.create_text(643.0, 264.0, anchor='nw',
            text="Admin", fill='#FFFFFF', font=('Rubik Light', 16 * -1))

        #### - Bug Report
        self.icn_bug = PhotoImage(file=relative_to_assets('icn_bug.png'))
        mail = self.canvas.create_image(569.0, 565.0, image=self.icn_bug)
        self.canvas.tag_bind(mail, '<Button-1>', mail_report)

        #### - Version + Logo
        self.canvas.create_text(585.0, 560.0, anchor='nw',
            text="V1.0 - 2023", fill='#FFFFFF', font=("Rubik Light", 8 * -1))

        self.small_logo = PhotoImage(file=relative_to_assets('small_logo.png'))
        linkedin = self.canvas.create_image(733.0, 536.0, image=self.small_logo)
        self.canvas.tag_bind(linkedin, '<Button-1>', linkedin_link)

    def display_icn_upload(self):
        self.reupload_button = self.canvas.create_image(668.0, 366.0, image=self.img_icn_upload_wh)
        self.reupload = self.canvas.find_withtag(self.reupload_button)

        self.image_reuploaded = self.canvas.tag_bind(self.reupload, '<Button-1>', 
            lambda event: self.load_image())

    def load_image(self):
        self.file_path = filedialog.askopenfilename()
        if self.file_path:
            self.path_pic = Image.open(self.file_path)
            self.resize_pic = preprocess_img(self.path_pic, 176)
            self.canvas.create_image(265.0, 127.0, image=self.resize_pic)

            self.frame_pic = PhotoImage(file=relative_to_assets('frame_pic.png'))
            self.canvas.create_image(265.0, 127.0, image=self.frame_pic)

            delete_items(self.canvas, self.upload_button, self.upload, 
                         self.text_upload, self.icn_upload_wh)

            self.prediction_lr_eye()

    def prediction_lr_eye(self):
        ## - LR Eye
        self.pred_LREyes = model_LREyes(self.file_path)

        #### - Label
        self.eye = self.pred_LREyes[0]['label']
        update_text(self.canvas, self.eye_text_item, f"Scan: {self.eye} eye", "#DCDDFF")

        #### - Score
        self.small_circle = PhotoImage(file=relative_to_assets('small_circle.png'))
        self.canvas.create_image(464.0, 379.0, image=self.small_circle)

        self.icn_eye = PhotoImage(file=relative_to_assets('icn_eye.png'))
        self.canvas.create_image(464.0, 389.0,image=self.icn_eye)

        self.score_eye = round(self.pred_LREyes[0]['score'] * 100, 1)
        update_text(self.canvas, self.score_eye_item, f"{self.score_eye}%")

        self.prediction_employee()

    def prediction_employee(self):
        if self.eye == 'right':
            self.pred_employee = model_RightEye(self.file_path)
        else:
            self.pred_employee = model_LeftEye(self.file_path)

        ## -- Valid Employee Access
        self.score_employee = round(((self.pred_employee[0]['score'] - self.pred_employee[1]['score']) / self.pred_employee[0]['score']) * 100, 1)
        self.access_result, self.color = valid_access(self.score_employee)
        print(self.score_employee, self.access_result)

        if self.access_result == "ACCESS DENIED":
            self.frame_lrg_circle = PhotoImage(file=relative_to_assets('large_circle.png'))
            self.canvas.create_image(394.0, 477.0, image=self.frame_lrg_circle)

            self.icn_employee = PhotoImage(file=relative_to_assets('icn_employee.png'))
            self.canvas.create_image(394.0, 520.0,image=self.icn_employee)

            self.score_denied = round((100 - self.pred_employee[0]['score']), 1)
            self.score_denied = 100 if self.score_denied == 100.0 else self.score_denied

            update_text(self.canvas, self.access_item, 
                        self.access_result, self.color)
            update_text(self.canvas, self.score_employee_item, 
                        f"{self.score_denied}%")

            save_in_db("--", self.access_result, self.score_denied, self.file_path)
        else:
            ## - Info Employee
            print(self.pred_employee[0]['label'])
            self.employee_info = id_employee(self.pred_employee[0]['label'])

            self.icn_sexe = "♂" if self.employee_info[2] == "Homme" else "♀"

            self.employee_info_img = PhotoImage(file=relative_to_assets('employee_info.png'))
            self.canvas.create_image(145.975, 295.5, image=self.employee_info_img)

            self.line_employee = PhotoImage(file=relative_to_assets('line_employee.png'))
            self.canvas.create_image(145.975, 311.5, image=self.line_employee)

            update_text(self.canvas, self.employee_name_item, f"Name: ")
            update_text(self.canvas, self.employee_name, 
                        f"{self.employee_info[0]} | {self.icn_sexe}")

            update_text(self.canvas, self.employee_year_item, 
                        "Hiring Year: ", "#DCDDFF")
            update_text(self.canvas, self.employee_year, 
                        f"{self.employee_info[1]}", "#DCDDFF")

            update_text(self.canvas, self.employee_job_item, "Job Position: ")
            update_text(self.canvas, self.employee_job, 
                        f"{self.employee_info[3]}", "#DCDDFF")

            ## -- Score
            self.frame_lrg_circle = PhotoImage(file=relative_to_assets('large_circle.png'))
            self.canvas.create_image(394.0, 477.0, image=self.frame_lrg_circle)

            self.icn_employee = PhotoImage(file=relative_to_assets('icn_employee.png'))
            self.canvas.create_image(394.0, 520.0,image=self.icn_employee)

            update_text(self.canvas, self.access_item, self.access_result, self.color)
            update_text(self.canvas, self.score_employee_item, f"{self.score_employee}%")

            save_in_db(self.employee_info[0], self.access_result, self.score_employee, self.file_path)

        self.display_icn_upload()

    def to_history(self):
        self.destroy()
        History(self.window)


class History(Frame):
    def __init__(self, window):
        Frame.__init__(self, window)

        self.window = window
        self.canvas = Canvas(
            window,
            bg = 'grey15',
            height = 600, width = 800,
            bd = 0,
            highlightthickness = 0,
            relief = 'ridge'
        )
        self.canvas.pack(fill='both', expand=True)
        self.canvas.place(x = 0, y = 0)


        ## - Left panel - History

        self.background_img = PhotoImage(file=relative_to_assets('background.png'))
        self.canvas.create_image(400.0, 300.0, image=self.background_img)

        self.past_checks = PhotoImage(file=relative_to_assets('past_checks.png'))
        self.canvas.create_image(101.0, 56.0, image=self.past_checks)

        self.line_checks = PhotoImage(file=relative_to_assets('line_checks.png'))
        self.canvas.create_image(145.0, 85.49, image=self.line_checks)

        self.line_white_sep = PhotoImage(file=relative_to_assets('line_white_check.png'))

        #### - first entry
        self.fe_name_item = self.canvas.create_text(48.0, 131.0, anchor='nw', font=('Rubik Light', 10 * -1))
        self.fe_date_item = self.canvas.create_text(48.0, 151.0, anchor='nw', font=('Rubik Light', 10 * -1, 'italic'))
        self.fe_access_item = self.canvas.create_text(416.0, 131.0, anchor='ne', font=('Rubik Medium', 12 * -1))
        self.fe_score_item = self.canvas.create_text(416.0, 151.0, anchor='ne', font=('Rubik Medium', 12 * -1))
        self.canvas.create_image(266.0, 184.0, image=self.line_white_sep)

        #### - second entry
        self.se_name_item = self.canvas.create_text(48.0, 203.0, anchor='nw', font=('Rubik Light', 10 * -1))
        self.se_date_item = self.canvas.create_text(48.0, 223.0, anchor='nw', font=('Rubik Light', 10 * -1, 'italic'))
        self.se_access_item = self.canvas.create_text(416.0, 203.0, anchor='ne', font=('Rubik Medium', 12 * -1))
        self.se_score_item = self.canvas.create_text(416.0, 223.0, anchor='ne',font=('Rubik Medium', 12 * -1))
        self.canvas.create_image(266.0, 256.0, image=self.line_white_sep)

        #### - third entry
        self.te_name_item = self.canvas.create_text(48.0, 275.0, anchor='nw', font=('Rubik Light', 10 * -1))
        self.te_date_item = self.canvas.create_text(48.0, 295.0, anchor='nw', font=('Rubik Light', 10 * -1, 'italic'))
        self.te_access_item = self.canvas.create_text(416.0, 275.0, anchor='ne', font=('Rubik Medium', 12 * -1))
        self.te_score_item = self.canvas.create_text(416.0, 295.0, anchor='ne', font=('Rubik Medium', 12 * -1))
        self.canvas.create_image(266.0, 328.0, image=self.line_white_sep)

        #### - fourth entry
        self.foe_name_item = self.canvas.create_text(48.0, 347.0, anchor='nw',font=("Rubik Light", 10 * -1))
        self.foe_date_item = self.canvas.create_text(48.0, 367.0, anchor='nw',font=('Rubik Light', 10 * -1, 'italic'))
        self.foe_access_item = self.canvas.create_text(416.0, 347.0, anchor='ne',font=('Rubik Medium', 12 * -1))
        self.foe_score_item = self.canvas.create_text(416.0, 367.0, anchor='ne',font=('Rubik Medium', 12 * -1))
        self.canvas.create_image(266.0, 400.0, image=self.line_white_sep)

        #### - fifth entry
        self.fie_name_item = self.canvas.create_text(48.0, 419.0, anchor='nw',font=('Rubik Light', 10 * -1))
        self.fie_date_item = self.canvas.create_text(48.0, 439.0, anchor='nw',font=('Rubik Light', 10 * -1, 'italic'))
        self.fie_access_item = self.canvas.create_text(416.0, 419.0, anchor='ne',font=('Rubik Medium', 12 * -1))
        self.fie_score_item = self.canvas.create_text(416.0, 439.0, anchor='ne',font=('Rubik Medium', 12 * -1))
        self.canvas.create_image(266.0, 472.0, image=self.line_white_sep)

        #### - Arrow pagination
        self.page = self.canvas.create_text(264.0, 529.0, anchor='nw',  font=('Rubik Light', 10 * -1, 'italic'))

        self.arrow_left_img = PhotoImage(file=relative_to_assets('arrow_left.png'))
        self.arrow_left = self.canvas.create_image(227.0, 537.0, image=self.arrow_left_img)

        self.arrow_right_img = PhotoImage(file=relative_to_assets('arrow_right.png'))
        self.arrow_right = self.canvas.create_image(307.0, 537.0, image=self.arrow_right_img)

        pagination(0, self.canvas, self.arrow_left, self.arrow_right, self.page,
            self.fe_name_item, self.fe_date_item, self.fe_access_item, self.fe_score_item, 
            self.se_name_item, self.se_date_item, self.se_access_item, self.se_score_item, 
            self.te_name_item, self.te_date_item, self.te_access_item, self.te_score_item, 
            self.foe_name_item, self.foe_date_item, self.foe_access_item, self.foe_score_item, 
            self.fie_name_item, self.fie_date_item, self.fie_access_item, self.fie_score_item)

        # -------------------------------------------------------------------- #
        ## - Right panel
        self.back_right = PhotoImage(file=relative_to_assets('back_blur_right.png'))
        self.canvas.create_image(666.0, 300.0, image=self.back_right)

        self.close_icn_img = PhotoImage(file=relative_to_assets('icn_close.png'))
        self.icn_close = self.canvas.create_image(764.0, 36.0, image=self.close_icn_img)
        self.canvas.tag_bind(self.icn_close, '<Button-1>', lambda event: close_window(window))

        self.icn_eye = PhotoImage(file=relative_to_assets('icn_large_eye.png'))
        self.predict_button_eye = self.canvas.create_image(573.0, 36.0, image=self.icn_eye)
        self.button_eye = self.canvas.find_withtag(self.predict_button_eye)
        self.canvas.tag_bind(self.button_eye, '<Button-1>', lambda event: self.to_predict())

        #### - Profil
        self.icn_profile = PhotoImage(file=relative_to_assets('icn_large_profile.png'))
        self.canvas.create_image(668.0,204.0,image=self.icn_profile)

        self.canvas.create_text(643.0, 264.0, anchor='nw', text="Admin",
            fill='#FFFFFF', font=('Rubik Light', 16 * -1))

        #### - Bug Report
        self.icn_bug = PhotoImage(file=relative_to_assets('icn_bug.png'))
        mail = self.canvas.create_image(569.0, 565.0, image=self.icn_bug)
        self.canvas.tag_bind(mail, '<Button-1>', mail_report)

        #### - Version + Logo
        self.canvas.create_text(585.0, 560.0, anchor='nw',
            text="V1.0 - 2023", fill='#FFFFFF', font=("Rubik Light", 8 * -1))

        self.small_logo = PhotoImage(file=relative_to_assets('small_logo.png'))
        linkedin = self.canvas.create_image(733.0, 536.0, image=self.small_logo)
        self.canvas.tag_bind(linkedin, '<Button-1>', linkedin_link)

    def to_predict(self):
        self.destroy()
        PredictHome(self.window)




def main():
    window = Tk()
    window.geometry('800x600')
    window.overrideredirect(True)
    window.attributes('-topmost', False, '-transparentcolor', 'grey15')
    window.config(bg='grey15')
    window.resizable(False, False)
    center_window(window)

    login_page = LoginPage(window)
    # login_page = PredictHome(window)
    # login_page = History(window)
    login_page.pack(fill='both', expand=True)

    window.mainloop()


if __name__ == '__main__':
    main()
