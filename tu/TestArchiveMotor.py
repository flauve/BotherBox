__author__ = 'root'
import os
import shutil
import tarfile
import unittest

from exception.ExceptionExistingFile import ExceptionExistingFile
from exception.ExceptionExistingTar import ExceptionExistingTar
from exception.ExceptionMissingFile import ExceptionMissingFile
from exception.ExceptionNbLoop import ExceptionNbLoop
from motor.ArchiveMotor import ArchiveMotor


class TestArchiveMotor(unittest.TestCase):

    # Tests work but maybe not at the first or second time

    NB_LOOP = 10  # bug when you exceed 19, don't know why
    TMP_PATH = "tmp"

    def setUp(self):
        if os.path.isdir(self.TMP_PATH):
            shutil.rmtree('tmp')
        os.makedirs(self.TMP_PATH)
        os.rename("__init__.py", self.TMP_PATH + "/__init__.py")
        fichier = open("__init__.py", "w")
        fichier.close()

    def test_wrong_input(self):
        # input : a loop number which is a word
        with self.assertRaises(ValueError):
            ArchiveMotor.archive("a", "a")

        # input : a loop number negative
        with self.assertRaises(ExceptionNbLoop):
            ArchiveMotor.archive("a", (-1))

        # input : a wrong file name
        with self.assertRaises(ExceptionMissingFile):
            ArchiveMotor.archive("svsodoaae", 1)

        # input : is not a tar file
        with self.assertRaises(tarfile.ReadError):
            file_name = self.TMP_PATH + "/mario"
            file = open(file_name, "w")
            file.close()
            ArchiveMotor.unarchive(file_name)

    def test_unarchive(self):
        # creation du fichier
        file = open("mario", "w")
        file.writelines("luigi")
        file.close()
        # creation de l'archive
        tar = tarfile.open("mario.tar", "w")
        tar.add("mario")
        tar.close()
        os.remove("mario")

        tar = tarfile.open("peach.tar", "w")
        tar.add("mario.tar")
        tar.close()
        os.remove("mario.tar")

        tar = tarfile.open("mario.tar", "w")
        tar.add("peach.tar")
        tar.close()
        os.remove("peach.tar")
        os.rename("mario.tar", "tmp/mario.tar")

        path = os.path.dirname(os.path.abspath(__file__)) + "/tmp/mario.tar"
        ArchiveMotor.unarchive(path)

        self.assertTrue(os.path.exists("tmp/mario"))

    def test_unarchive_existing_file(self):
        file_name = "mario"
        file = open(file_name, "w")
        file.writelines("luigi")
        file.close()
        filetar_path = "mario.tar"
        tar = tarfile.open(filetar_path, "w")
        tar.add("mario")
        tar.close()

        os.rename(file_name, "tmp\\" + file_name)
        tar_path = os.path.dirname(os.path.abspath(__file__)) + "\\tmp\\mario.tar"
        os.rename(filetar_path, tar_path)
        with self.assertRaises(ExceptionExistingFile):
            ArchiveMotor.unarchive(tar_path)

    def test_archive_keep_original_file_safe(self):
        path_cur_directory = os.path.dirname(os.path.abspath(__file__))
        file_path = path_cur_directory + "\\tmp\mario"
        file = open(file_path, "w")
        content = "luigi"
        file.writelines(content)
        file.close()

        ArchiveMotor.archive(file_path, self.NB_LOOP)
        self.assertTrue(os.path.exists(file_path))

        file = open(file_path, "r")
        line = file.readline()
        file.close()
        self.assertEqual(content, line)

    def test_archive_existing_tar(self):
        path_cur_directory = os.path.dirname(os.path.abspath(__file__))
        file_path = path_cur_directory + "\\tmp\mario"
        file = open(file_path, "w")
        file.writelines("luigi")
        file.close()

        tar_path = path_cur_directory + "\\tmp\mario.tar"
        file = open(tar_path, "w")
        file.writelines("luigi")
        file.close()

        with self.assertRaises(ExceptionExistingTar):
            ArchiveMotor.archive(file_path, self.NB_LOOP)

    def test_archive(self):
        path_cur_directory = os.path.dirname(os.path.abspath(__file__))
        file_path = path_cur_directory + "\\tmp\mario"
        file = open(file_path, "w")
        file.writelines("luigi")
        file.close()

        ArchiveMotor.archive(file_path, self.NB_LOOP)
        os.remove(file_path)

        file_tar = file_path + ".tar"
        ArchiveMotor.unarchive(file_tar)

        path = "tmp/mario"
        self.assertTrue(os.path.exists(path))

    def tearDown(self):
        if os.path.isdir(self.TMP_PATH):
            shutil.rmtree('tmp')