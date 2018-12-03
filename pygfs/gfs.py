import requests
import os
import shutil
from pygfs.utils import *

class gfs:
    def connect(self, email, passwd):
        '''
        login to the server with user credentials
        '''
        site_url = "https://rda.ucar.edu/cgi-bin/login"
        self.session = requests.Session()
        self.check_response(self.session.get(site_url))
        self.check_response(self.session.post
                            (site_url,
                             data={'email': email,
                                   'passwd': passwd,
                                   'action': 'login'}))

    def download(self, date, fcsthours, resolution):
        self.date = date
        self.fcsthours = fcsthours
        self.resolution = resolution
        self.check_fcsthours()
        self.build_filelist()
        self.download_files()

    def build_filelist(self):
        self.filelist = [self.get_filename(fcsthour)
                         for fcsthour in self.fcsthours]

    def get_filename(self, fcsthour):
        int_, dec = (str(float(self.resolution))).split('.')
        yr = str(self.date.year).zfill(4)
        mnth = str(self.date.month).zfill(2)
        day = str(self.date.day).zfill(2)
        baseurl = 'https://rda.ucar.edu/data/ds084.1/'
        fpath = os.path.join(yr, yr + mnth + day, 'gfs.' +
                             int_ + 'p' + dec.zfill(2) + '.' +
                             yr + mnth + day + '00.f' +
                             str(fcsthour).zfill(3) + '.grib2')
        return (os.path.join(baseurl, fpath))

    def download_files(self):
        '''
        Download the actual files
        '''
        [self.download_file(fl) for fl in self.filelist]

    def download_file(self, url):
        '''
        Stream download url to localfile
        '''
        local_filename = url.split('/')[-1]
        with self.session.get(url, stream=True) as r:
            with open(local_filename, 'wb') as f:
                shutil.copyfileobj(r.raw, f)
        #check_gribfile(local_filename)
        return local_filename

    @staticmethod
    def check_response(request):
        '''
        check if the request returns an ok request code
        '''
        if (request.status_code == requests.codes.ok):
            return
        else:
            raise IOError('Http request failed with status code: ' +
                          request.status_code)

    def check_fcsthours(self):
        '''
        Check if the forecast hours specified are all valid and unique
        '''
        # check if all fcsthours are unique
        checked = set()
        if any(i in checked or checked.add(i) for i in self.fcsthours):
            raise IOError('Error: Not all supplied forecast hours are unique')
        # check if all individual ints are valid forecast hours
        valid = [*range(6, 48, 6)]  # python >3.5
        if not set(self.fcsthours).issubset(set(valid)):
            raise IOError('\n Error: Not a valid subset of forecast hours,',
                          'valid hours are' + str(valid) + '\n')
