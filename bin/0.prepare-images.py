#!/usr/bin/env python

import argparse
import os
import shutil

class FileCopier:
    DESTINATION_DIR = '/tmp/WAGS/Faces'

    def __init__(self, fullpath):
        self.src_filename = fullpath

    @staticmethod
    def dst_dir(filename):
        """
        Return the name of a dir we can use for this file in the destination dir structure
        E.g. 001.jpg => /tmp/WAGS/Faces/001, 704.jpg => /tmp/WAGS/Faces/704
        :return:
        """
        basename = os.path.basename(filename)
        basename, ext = os.path.splitext(basename)
        dir = os.path.join(FileCopier.DESTINATION_DIR, basename)
        return dir

    def _inc_filename(self, filename):
        basename = os.path.basename(filename)
        name, ext = os.path.splitext(basename)
        last = int(name)  # name should be something like 001, 002, etc
        # Don't increment the filename for the first file (it would make it 002 instead of keeping it the same)
        if last >= 1:
            last += 1
        next_filename_base = "%03d" % last
        next_filename = next_filename_base + ext
        return next_filename

    def _dst_filename(self):
        """
        Given a filename (001.jpg), return a full path suitable for use as a destination name when copying the file
        :return:
        """
        dst_dir = self.dst_dir(self.src_filename)
        filenames = os.listdir(dst_dir)
        dst_filename = '001.jpg'
        if len(filenames) > 0:
            filenames.sort()
            dst_filename = self._inc_filename(filenames[-1])
        dst_filename = os.path.join(dst_dir, dst_filename)
        return dst_filename

    def copy_to_dst(self):
        """
        Copies the filename (full path) to it's destination folder, renaming it if necessary
        :return:
        """
        dst_filename = self._dst_filename()
        shutil.copy2(self.src_filename, dst_filename)


def create_face_dirs(src_dir):
    dirs = os.listdir(src_dir)
    dirs.sort()
    files = os.listdir(os.path.join(src_dir, dirs[0]))
    #files = os.listdir(os.path.join(src_dir, '00 Clean originals'))
    files.sort()
    for file in files:
        dir = FileCopier.dst_dir(file)
        try:
            os.makedirs(dir)
        except OSError:
            pass


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Re-structure images in preparation for 1.create-recognize-csv.py')
    parser.add_argument('src_dir', help='The root we want to copy from')
    parser.add_argument('-d', '--dst-dir', default='/tmp/WAGS/Faces', help='Destination directory root (default: /tmp/WAGS/Faces)')

    args = parser.parse_args()

    FileCopier.DESTINATION_DIR = args.dst_dir

    create_face_dirs(args.src_dir)

    dirs = os.listdir(args.src_dir)
    dirs.sort()
    for dirname in dirs:
        full_dirname = os.path.join(args.src_dir, dirname)
        filenames = os.listdir(full_dirname)
        filenames.sort()
        for filename in filenames:
            fullpath = os.path.join(full_dirname, filename)
            copier = FileCopier(fullpath)
            copier.copy_to_dst()
