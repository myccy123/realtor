import xlrd
import sys






def get_sheets(filename):

    workbook = xlrd.open_workbook(filename)
    sheets = workbook.sheet_names()
    return sheets

def get_content(filename,sheetname,skiprow=0,skipcol=0):
    workbook = xlrd.open_workbook(filename)
    sheet = workbook.sheet_by_name(sheetname)
    
    data = []
    
    skiprow = int(skiprow)
    skipcol = int(skipcol)
    
    for i in range(skiprow,sheet.nrows):
        row = []
        for j in range(skipcol,sheet.ncols):
            row.append(xlrd.xldate_as_datetime(sheet.cell(i,j).value, workbook.datemode) if sheet.cell(i,j).ctype == 3 else sheet.cell(i,j).value)
        data.append(row)
    return data

def default_colname(n):
    a = ['A','B','C','D','E','F','G','H','I','J','K','L','M','N','O','P','Q','R','S','T','U','V','W','X','Y','Z']
    if n < 1:
        return ''
    elif n <= 26:
        return a[n-1]
    else:
        ten = int(n / 26) if n % 26 != 0 else int(n / 26) -1
        ge  = n % 26
        return a[ten-1] + a[ge-1]

def max_col_length(sheet,firstrow='1',skiprow=0,skipcol=0):
    if firstrow == '1':
        skiprow += 1
    
    l = []
    
    for i in range(skiprow,sheet.nrows):
        
        k = 0
        for j in range(skipcol,sheet.ncols):
            try:
                if len(str(sheet.cell(i,j).value)) > int(l[k]):
                    l[k] = len(str(sheet.cell(i,j).value))
            except IndexError:
                l.append(len(str(sheet.cell(i,j).value)))
            k += 1
    
    return l
    
    