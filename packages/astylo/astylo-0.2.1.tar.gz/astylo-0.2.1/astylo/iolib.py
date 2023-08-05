#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""

Basic Input & Output

"""
import sys, logging
logging.disable(sys.maxsize)

import subprocess as SP
import numpy as np
from astropy.io import fits
import h5py as H5
import csv

global fitsext, h5ext
fitsext = '.fits'
h5ext = '.h5'
ascext = '.txt'
csvext = '.csv'

def fclean(file, *alert):
    '''
    Clean folder/files
    '''
    SP.call('rm -rf '+file, shell=True)
    for text in alert:
        print(text)

def read_fits(file, file_unc=None, wmod=0):
    '''
    Read fits file (auto detect dim)

    ------ INPUT ------
    file                input fits file
    file_unc            input uncertainty file
    wmod                output wave mode (Default: 0)
                          0 - 1darray; 
                          1 - FITS_rec.
    ------ OUTPUT ------
    ds                  output dataset
      header              header of primary HDU
      data                data in primary HDU
      header_w            header of W-TAB
      wave                data in table 1 (None if does not exist)
      unc                 uncertainty array
    '''
    ## Initialize output object
    ds = type('', (), {})()
    ds.header_w = None
    ds.wave = None
    ds.unc = None

    ## Read header & data
    with fits.open(file+fitsext) as hdul:
        ds.HDUL = hdul
        hdr = hdul[0].header
        ds.data = hdul[0].data
        ds.header = hdr

        ## Read wavelength
        if len(hdul)==2:
            ds.header_w = hdul[1].header
            wave = hdul[1].data

            if isinstance(hdul[1], fits.BinTableHDU):
                if wmod==0:
                    wave = wave[0][0][:,0] ## Convert FITS_rec to 1darray
            elif isinstance(hdul[1], fits.ImageHDU):
                Nw = len(wave)
                if wmod==1:
                    wave = np.array(wave).reshape((Nw,1))
                    col = fits.Column(array=[wave], format=str(Nw)+'E', \
                        name='WAVE-TAB', unit='um', dim='(1,{})'.format(Nw))
                    tab = fits.BinTableHDU.from_columns([col], name='WCS-TAB ')
                    wave = tab.data
            
            ds.wave = wave
    
    if file_unc is not None:
        ## Read uncertainty data
        with fits.open(file_unc+fitsext) as hdul:
            ds.unc = hdul[0].data

    return ds

def write_fits(file, header, data, wave=None, wmod=0, **hdrl):
    '''
    Write fits file

    ------ INPUT ------
    file                input fits file
    header              header of primary HDU
    data                data in primary HDU
    wave                data in table 1 (ndarray. default: None)
    wmod                wave table format (0 - Image; 1 - BinTable. default: 0)
    ------ OUTPUT ------
    '''
    for key, value in hdrl.items():
        header[key] = value
    primary_hdu = fits.PrimaryHDU(header=header, data=data)
    hdul = fits.HDUList(primary_hdu)
    
    ## Add table
    if wave is not None:
        ## Convert wave format
        if isinstance(wave, fits.fitsrec.FITS_rec):
            if wmod==0:
                wave = wave[0][0][:,0]
        else:
            Nw = len(wave)
            if wmod==1:
                wave = np.array(wave).reshape((Nw,1))
                col = fits.Column(array=[wave], format=str(Nw)+'E', \
                    name='WAVE-TAB', unit='um', dim='(1,{})'.format(Nw))
                tab = fits.BinTableHDU.from_columns([col], name='WCS-TAB ')
                wave = tab.data
        ## Create table
        if wmod==0:
            hdu = fits.ImageHDU(data=wave, name='WAVE-TAB')
        elif wmod==1:
            hdu = fits.BinTableHDU(data=wave, name='WCS-TAB ')

        hdul.append(hdu)

    hdul.writeto(file+fitsext, overwrite=True)

def read_hdf5(file, *header):
    '''
    Read h5 file

    ------ INPUT ------
    file                input h5 file
    header              labels of data to read
    ------ OUTPUT ------
    dataset             data
    '''
    hf = H5.File(file+h5ext, 'r')
    dataset = []
    for hdr in header:
        data = hf.get(hdr)
        data = np.array(data)
        dataset.append(data)

    hf.close()

    return dataset

def write_hdf5(file, header, data, append=False, amod=True):
    '''
    Write h5 file

    ------ INPUT ------
    file                file name of the new h5 file
    header              label of data (one at a time)
    data                data (dim < 4 if elements consist of strings)
    append              True: if not overwrite (default: False)
    amod                auto ASCII data mode (default: True)
    ------ OUTPUT ------
    '''
    if append==True:
        hf = H5.File(file+h5ext, 'a')
    else:
        hf = H5.File(file+h5ext, 'w')

    if amod==True:
        ## Correct create_dataset string input issue
        ## "these strings are supposed to store only ASCII-encoded text"
        ## See http://docs.h5py.org/en/stable/strings.html
        if isinstance(data, np.ndarray):
            data_list = data.tolist()
            isndarray = True
        else:
            data_list = data
            isndarray = False
        
        ## With the previous step, lists with diff dtype are compatible;
        ## Irregular lists are compatible;
        ## However list dim is limited (dim < 4 if string elements present)
        if isinstance(data_list, list):
            ## 1D list
            for i,e1 in enumerate(data_list):
                if isinstance(e1, str):
                    data_list[i] = e1.encode('ascii', 'ignore')
                elif isinstance(e1, list):
                    ## 2D list
                    for j,e2 in enumerate(e1):
                        if isinstance(e2, str):                        
                            data_list[i][j] = e2.encode('ascii', 'ignore')
                        elif isinstance(e2, list):
                            ## 3D list
                            for k,e3 in enumerate(e2):
                                if isinstance(e3, str):
                                    data_list[i][j][k] = e3.encode('ascii', 'ignore')
        if isndarray==True:
            data_modif = np.array(data_list) # ndarray
        else:
            data_modif = data_list
    else:
        data_modif = data
        
    hf.create_dataset(header, data=data_modif)

    hf.flush()
    hf.close()

def read_ascii(file, ascext=ascext, dtype=str):
    '''
    Read ASCII file

    ------ INPUT ------
    file                input ASCII file
    dtype               data type (default: 'str')
    ------ OUTPUT ------
    dataset             output data array
    '''
    with open(file+ascext, 'r') as f:
        ## f.read() -> str | f.readlines() -> list
        dataset = []
        for line in f.readlines():
            line = line.strip()
            # print(line)
            if line[0]!='#':
                line = list(map(dtype, line.split()))
                data = []
                for vec in line:
                    data.append(vec)
                dataset.append(data)

    dataset = np.array(dataset)

    return dataset

def read_csv(file, *header):
    '''
    Read csv file

    ------ INPUT ------
    file                input csv file
    header              labels of data to read
    ------ OUTPUT ------
    dataset             dataset
    '''
    with open(file+csvext, 'r', newline='') as csvfile:
        reader = csv.DictReader(csvfile)
        dataset = []
        for hdr in header:
            csvfile.seek(0) # reset pointer
            data = []
            for row in reader:
                data.append(row[hdr])
            data = np.array(data)
            dataset.append(data)

    return dataset

def write_csv(file, header, dataset, append=False):
    '''
    Read fits file

    ------ INPUT ------
    file                file name of the csv file
    header              labels of data, list('label1', 'label2', ...)
    dataset             data, list([d11, d12, ...], [d21, d22, ...], ...)
    ------ OUTPUT ------
    '''
    if append==True:
        mod = 'a'
    else:
        mod = 'w'

    with open(file+csvext, mod, newline='') as csvfile:
        writer = csv.DictWriter(csvfile, fieldnames=header)

        writer.writeheader()

        for i in range(len(dataset)):
            ## Init dict
            row = {hdr: [] for hdr in header}
            data = dataset[i]
            ## Write dict
            for j in range(len(header)):
                row[header[j]] = data[j]
            ## Write csv row
            writer.writerow(row)
