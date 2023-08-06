"Microapp gzip module wrapper for uncompressing"

from microapp import App

import gzip
import shutil


class Gunzip(App):

    _name_ = "micro-gunzip"
    _version_ = "0.1.2"
    _description_ = "Microapp gunzip"
    _long_description_ = "Microapp gunzip"
    _author_ = "Youngsung Kim"
    _author_email_ = "youngsung.kim.act2@gmail.com"
    _url_ = "https://github.com/grnydawn/microapp-gunzip"

    def __init__(self, mgr):

        self.add_argument("zipfile", type=str, help="zipped file")
        self.add_argument("-o", "--outfile", type=str, help="file path for a unzipped file")

    def perform(self, mgr, args):

        zipfile = args.zipfile["_"]

        with gzip.open(zipfile, 'rb') as f_in:
            if args.outfile:
                with open(args.outfile["_"], 'wb') as f_out:
                    shutil.copyfileobj(f_in, f_out)
            else:
                root, ext = os.path.splitext(zipfile)
                outfile = root if ext == ".gz" else "%s.uncompressed" % zipfile

                with open(outfile, 'wb') as f_out:
                    shutil.copyfileobj(f_in, f_out)

