__author__ = 'root'

from tkinter import *
from tkinter import messagebox
from tkinter.filedialog import askopenfilename
from tkinter.messagebox import showerror
import tarfile

from LocalisationFr import LocalisationFr
from exception.ExceptionMissingFile import ExceptionMissingFile
from exception.ExceptionMissingTar import ExceptionMissingTar
from exception.ExceptionExistingTar import ExceptionExistingTar
from exception.ExceptionExistingFile import ExceptionExistingFile
from ArchiveMotor import ArchiveMotor


class Interface(Tk):
    def __init__(self):
        Tk.__init__(self)
        self.title(LocalisationFr.WINDOW_PROGRAM_NAME.value)
        self.panel_archive = self.panel_archive()
        self.panel_unarchive = self.panel_unarchive()
        self.panel_about = self.panel_about()
        self.menu()
        self.resizable(width=FALSE, height=FALSE)
        self.show_panel_archive()

    def menu(self):
        menubar = Menu(self, tearoff=0)
        menubar.add_command(label=LocalisationFr.PANEL_ARCHIVE.value, command=self.show_panel_archive)
        menubar.add_command(label=LocalisationFr.PANEL_UNARCHIVE.value, command=self.show_panel_unarchive)
        menubar.add_command(label=LocalisationFr.PANEL_ABOUT.value, command=self.show_panel_about)

        self.config(menu=menubar)

    def show_panel_archive(self):
        self.panel_unarchive.pack_forget()
        self.panel_about.pack_forget()
        self.panel_archive.pack()

    def show_panel_unarchive(self):
        self.panel_archive.pack_forget()
        self.panel_about.pack_forget()
        self.panel_unarchive.pack()

    def show_panel_about(self):
        self.panel_archive.pack_forget()
        self.panel_unarchive.pack_forget()
        self.panel_about.pack()

    def panel_archive(self):
        panel_archive = PanedWindow(self, orient=HORIZONTAL)
        p_file_name = PanedWindow(panel_archive, orient=HORIZONTAL)
        p_file_name.add(Label(p_file_name, text=LocalisationFr.PANEL_ARCHIVE_FILE_NAME.value))
        self.archive_input_file_path = Entry(p_file_name, textvariable=StringVar(), width=50)
        p_file_name.add(self.archive_input_file_path)
        p_file_name.add(Button(panel_archive, text=LocalisationFr.TEXT_BROWSE.value, command=self.load_file))
        p_file_name.pack(side=TOP, fill=BOTH, padx=5)

        p_count = PanedWindow(panel_archive, orient=HORIZONTAL)
        p_count.add(Label(p_count, text=LocalisationFr.PANEL_ARCHIVE_LOOP.value))
        self.archive_input_loop = Entry(self, textvariable=StringVar(), width=4)
        p_count.add(self.archive_input_loop)
        p_count.pack(side=TOP, padx=10)

        Button(panel_archive, text=LocalisationFr.PANEL_ARCHIVE_BUTTON.value, command=self.launchArchiving).pack(
            padx=10, pady=10)

        return panel_archive

    def panel_unarchive(self):
        panel_unarchive = PanedWindow(self, orient=HORIZONTAL)
        p_file_name = PanedWindow(panel_unarchive, orient=HORIZONTAL)
        p_file_name.add(Label(p_file_name, text=LocalisationFr.PANEL_ARCHIVE_FILE_NAME.value))
        self.unarchive_input_file_path = Entry(p_file_name, textvariable=StringVar(), width=50)
        p_file_name.add(self.unarchive_input_file_path)
        p_file_name.add(Button(panel_unarchive, text=LocalisationFr.TEXT_BROWSE.value, command=self.load_file))
        p_file_name.pack(side=TOP, fill=BOTH, padx=5)

        Button(panel_unarchive, text=LocalisationFr.PANEL_UNARCHIVE_BUTTON.value, command=self.launchUnarchiving).pack(
            padx=10, pady=10)

        return panel_unarchive

    def panel_about(self):
        panel_about = PanedWindow(self, orient=HORIZONTAL)
        p_file_name = PanedWindow(panel_about, orient=HORIZONTAL)
        p_file_name.add(Label(p_file_name, text=LocalisationFr.PANEL_ABOUT_CONTENT.value))
        p_file_name.pack(side=TOP, fill=BOTH, padx=5)

        return panel_about

    def launchArchiving(self):
        try:
            file_name = str(self.archive_input_file_path.get())
            nb_loop = int(self.archive_input_loop.get())
            ArchiveMotor.archive(file_name, nb_loop)
            message = "Félicitation ! Le fichier '" + file_name + "' a bien été archivé récursivement " + str(
                nb_loop) + " fois."
            messagebox.showinfo("Information", message)
        except ValueError:
            messagebox.showerror(LocalisationFr.MESSAGE_ERROR.value,
                                 LocalisationFr.MESSAGE_EMPTY_NAME_FILE_OR_LOOP.value)
        except IOError:
            messagebox.showerror(LocalisationFr.ExceptionFileMissing(file_name))
        except ExceptionMissingFile as e:
            messagebox.showerror(LocalisationFr.MESSAGE_ERROR.value, e.value)
        except ExceptionExistingTar as e:
            messagebox.showerror(LocalisationFr.MESSAGE_ERROR.value, e.value)

    def launchUnarchiving(self):
        try:
            file_name = str(self.unarchive_input_file_path.get())
            ArchiveMotor.unarchive(file_name)
            message = "Félicitation ! Le fichier '" + file_name + "' a bien été désarchivé récursivement "
            messagebox.showinfo(LocalisationFr.MESSAGE_INFORMATION.value, message)
        except ValueError:
            messagebox.showerror(LocalisationFr.MESSAGE_WARNING.value,
                                 LocalisationFr.MESSAGE_EMPTY_NAME.value)
        except IOError:
                messagebox.showerror(LocalisationFr.MESSAGE_ERROR.value, ExceptionMissingFile(file_name))
        except ExceptionMissingFile as e:
            messagebox.showerror(LocalisationFr.MESSAGE_ERROR.value, e.value)
        except tarfile.ReadError:
            messagebox.showerror(LocalisationFr.MESSAGE_ERROR.value, ExceptionMissingTar(file_name))
        except ExceptionExistingFile as e:
            messagebox.showerror(LocalisationFr.MESSAGE_ERROR.value, e.value)

    def load_file(self):
        fname = askopenfilename()
        if fname:
            try:
                self.archive_input_file_path.delete(0, 10000)
                self.unarchive_input_file_path.delete(0, 10000)
                self.archive_input_file_path.insert(0, fname)
                self.unarchive_input_file_path.insert(0, fname)
            except:
                showerror("Open Source File", "Failed to read file\n'%s'" % fname)

