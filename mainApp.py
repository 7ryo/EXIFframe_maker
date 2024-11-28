import tkinter
from tkinter import filedialog
import customtkinter
from PIL import ImageTk, Image
import os
import EXIFframe

customtkinter.set_appearance_mode("System")
customtkinter.set_default_color_theme("blue")


bool_firstimport = True
tk_img = None
img_preview_id = None
outputdir = '/output'
first_file_path = None
class App(customtkinter.CTk):


    def runWatermark():
        #for e in selected_img_path:
            #utility.draw_watermark_frame(e)
        #selected_img_path = []
        return 0

    def __init__(self):
        super().__init__()

        self.title("EXIF WATERMARK MAKER")
        self.geometry(f"{800}x{600}")
        #self.maxsize(800, 600)

        def addtolistbox(file_path):
            self.listbox_importedfile.insert("end", file_path)
            global tk_img
            global bool_firstimport
            global img_preview_id
            global first_file_path
            if bool_firstimport == True:
                first_file_path = file_path
                previewimg = get_preview_img()
                tk_img = ImageTk.PhotoImage(image=previewimg)
                img_preview_id = self.canvas_preview.create_image(338, 227, anchor='center', image=tk_img)
                bool_firstimport = False
        def removefromlistbox():
            global bool_firstimport
            global img_preview_id
            global tk_img
            global first_file_path
            selected_index = self.listbox_importedfile.curselection()
            for i in reversed(selected_index): #tuple
                if (i == 0) and (self.listbox_importedfile.size() > 1):
                    first_file_path = self.listbox_importedfile.get(1)
                    get_preview_img()
                self.listbox_importedfile.delete(i)
            if self.listbox_importedfile.size() == 0:
                #listbox is empty
                bool_firstimport = True
                self.canvas_preview.delete(img_preview_id)
                img_preview_id = None

        def get_preview_img(image_path=first_file_path):
            global tk_img
            global first_file_path
            
            logo = self.combobox_logo.get()
            previewimg = EXIFframe.draw_watermark_frame(image_path=first_file_path, input_logo=logo)
            if bool_firstimport == False:
                tk_img = ImageTk.PhotoImage(previewimg)
                self.canvas_preview.itemconfig(img_preview_id, image=tk_img)
            return previewimg
        def removefromlistbox_all():
            global bool_firstimport
            global img_preview_id
            self.listbox_importedfile.delete(0, tkinter.END)
            if self.listbox_importedfile.size() == 0:
                #listbox is empty
                bool_firstimport = True
                self.canvas_preview.delete(img_preview_id)
                img_preview_id = None

        def browse_files():
            files = filedialog.askopenfilenames(initialdir=getcurrentdir(),
                                                title = "Select a File or Files",
                                                filetypes=(("JPG image", "*.jpg"),
                                                            ("PNG image", "*.png")
                                                            ))
            #add selected file into listbox
            for f in files:
                addtolistbox(f)

        def load_combobox_options(dir):
            list_logos = []
            list_filenames = os.listdir(dir)
            for n in list_filenames:
                list_logos.append(n.replace('.png', ''))
            return list_logos

        def getcurrentdir():
            cwd = os.getcwd()
            cwd = cwd.replace("\\", "/")
            return cwd

        def browse_directory():
            global outputdir
            selecteddir = filedialog.askdirectory(initialdir=f"{getcurrentdir()}",
                                          title="Select a Folder")
            if selecteddir:
                text_outputpath.set(selecteddir)
                outputdir = selecteddir

        def getvalues():
            self.progressbar_run.grid(row=8, column=1, padx=20, pady=10)
            self.progressbar_run.start()
            self.button_run['state'] = tkinter.DISABLED
            paths = self.listbox_importedfile.get(0, tkinter.END)
            logo = self.combobox_logo.get()
            dir = self.entry_outputpath.get()
            if dir == '':
                dir = "/output"
            text_entry = self.entry_outputsuffix.get()
            suffix = "_with_frame"
            if text_entry != '':
                suffix = text_entry
            i = EXIFframe.generate(paths, logo, dir, suffix)
            if i == 0:
                removefromlistbox_all()
                self.progressbar_run.grid_forget()
                self.button_run['state'] = tkinter.NORMAL

            


        # left frame: select files
        self.left_frame = customtkinter.CTkFrame(self, width=400, corner_radius=0)
        #self.left_frame.grid(row=0, column=0, columnspan=2, sticky="nsew")
        self.left_frame.pack(fill='y', side='left')
        self.left_frame.grid_rowconfigure(1, weight=1)

        self.button_browsefile = customtkinter.CTkButton(self.left_frame, text="Browse Image", command=browse_files)
        self.button_browsefile.grid(row=0, column=0, padx=20, pady=10, sticky="nesw")
        self.listbox_importedfile = tkinter.Listbox(self.left_frame, width=60, justify="left",
                                                    selectmode=tkinter.MULTIPLE, selectbackground="gray")
        self.listbox_importedfile.grid(row=1, column=0, columnspan=2, padx=20, pady=10, sticky="nesw")
        # function: get listbox option
        self.button_removefile = customtkinter.CTkButton(self.left_frame, text="Remove", command=removefromlistbox)
        self.button_removefile.grid(row=4, column=0, padx=20, pady=10, sticky="nesw")
        self.button_removefileall = customtkinter.CTkButton(self.left_frame, text="Remove All", command=removefromlistbox_all)
        self.button_removefileall.grid(row=5, column=0, padx=20, pady=10, sticky="nesw")
        

        # right frame: main
        self.right_frame = customtkinter.CTkFrame(self, corner_radius=0)
        #self.right_frame.grid(row=0, column=2, columnspan=3, sticky="nsew")
        self.right_frame.pack(fill='y', side='left')
        self.right_frame.grid_rowconfigure(1, weight=1)

        self.label_preview = customtkinter.CTkLabel(self.right_frame, text="Preview")
        self.label_preview.grid(row=0, column=0, padx=20, pady=(10, 0), sticky="nesw")
        self.canvas_preview = tkinter.Canvas(self.right_frame, relief="solid")
        self.canvas_preview.grid(row=1, columnspan=3, padx=40, pady=(10,20), sticky="nesw")
        # (canvas size is 382 x 268)
        self.label_logo = customtkinter.CTkLabel(self.right_frame, text="Logo")
        self.label_logo.grid(row=2, column=0, padx=20, pady=10, sticky="nsw")
        logo_option_list = load_combobox_options('./logo')
        default_var = customtkinter.StringVar()
        default_var.set(logo_option_list[0])
        self.combobox_logo = customtkinter.CTkComboBox(self.right_frame, 
                                                       values=logo_option_list, state="readonly", variable=default_var,
                                                       command=get_preview_img)
        self.combobox_logo.grid(row=2, column=1, padx=20, pady=10, sticky="nesw")


        self.label_outputpath = customtkinter.CTkLabel(self.right_frame, text="Output Path")
        self.label_outputpath.grid(row=4, column=0, columnspan=2, padx=20, pady=10, sticky="nsw")
        self.button_browsepath = customtkinter.CTkButton(self.right_frame, text="Browse", command=browse_directory)
        self.button_browsepath.grid(row=4, column=2, padx=20, pady=10)
        text_outputpath = customtkinter.StringVar()
        text_outputpath.set(f"{getcurrentdir()}/output")
        self.entry_outputpath = customtkinter.CTkEntry(self.right_frame, textvariable=text_outputpath, state=tkinter.DISABLED)
        self.entry_outputpath.grid(row=5, column=0, columnspan=3, padx=20, pady=10, sticky="nesw")


        self.label_outputname = customtkinter.CTkLabel(self.right_frame, text="Output Filename")
        self.label_outputname.grid(row=6, column=0, padx=20, pady=10, sticky="nsw")
        self.label_outputstem = customtkinter.CTkLabel(self.right_frame, text="original filename+")
        self.label_outputstem.grid(row=6, column=1, padx=10, pady=10)
        text_suffix = customtkinter.StringVar()
        text_suffix.set("_with_frame")
        self.entry_outputsuffix = customtkinter.CTkEntry(self.right_frame, textvariable=text_suffix)
        self.entry_outputsuffix.grid(row=6, column=2, padx=10, pady=10)

        self.progressbar_run = customtkinter.CTkProgressBar(self.right_frame, width=100, mode="indeterminate")
        
        self.button_run = customtkinter.CTkButton(self.right_frame, text="Run", command=getvalues)
        self.button_run.grid(row=8, column=2, padx=20, pady=10)


if __name__ == "__main__":
    app = App()
    app.mainloop()
