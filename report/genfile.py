import os,sys,random,string
import re

from copy import copy
from StringIO import StringIO
from xlwt import Workbook

from django.db import models
from django.db.models.query import QuerySet
from django.db.models import Max, Min
from django.conf import settings

from report.utils import utils as ReportUtils

class genfile(object):
    limit = ReportUtils.record_limit
    def setLimit(self, limit):
        self.limit = limit
        
        ## creating xls
    def genXlsByJson(self, jData, fullFilePath):
        book = Workbook(encoding='utf-8')

        for s in jData:
            sheet = book.add_sheet(s)
            rowindex = 0
            maxcolWidth = dict();

            for row in jData[s]: ## row
                if self.limit < rowindex and self.limit != -1:
                    break

                colindex = 0
                for cell in row: ## column
                    cellLen = len(str(cell))
                    sheet.write(rowindex, colindex, cell)
                    if colindex not in maxcolWidth:
                        maxcolWidth[colindex] = cellLen
                
                        if cellLen > maxcolWidth[colindex]:
                            maxcolWidth[colindex] = cellLen
                    
                        if type(cell) == 'float':
                            sheet.row(rowindex).set_cell_number(colindex, cell)

                        sheet.col(colindex).width = (2 + maxcolWidth[colindex]) * 256
                            
                    colindex = colindex + 1
                # End for cell in row: ## column                    
                rowindex = rowindex + 1
            # End for row in jData[s]: ## row
            sheet.flush_row_data()

        book.save(fullFilePath)            
        return 0

    def genXlsByText(self, tData, fullFilePath):
        book = Workbook(encoding='utf-8')
        sio = StringIO(tData)
        lines = sio.readlines()
        rowindex = 0
        sheet = 0
        sheet_created = 0
        delimiter = ','

        for l in lines:
            l = l.rstrip()
            colindex = 0
            if 0 == sheet_created:
                m = re.search('delimiter:(.)', l)
                if m:
                    delimiter = m.group(1)
                    continue

            if l[0] == '[' and sheet_created == 0:
                sheet = book.add_sheet(l[1:(len(l)-2)])
                rowindex = 0
                sheet_created = 1
                continue
            
            cells = l.split(delimiter)

            if self.limit < rowindex and self.limit != -1:
                break

            for cell in cells:
                if cell.isdigit():
                    cell = float(cell)
                    sheet.row(rowindex).set_cell_number(colindex, cell)
                else:    
                    sheet.write(rowindex, colindex, cell)
                colindex = colindex + 1
            sheet.flush_row_data()
            rowindex = rowindex + 1

        book.save(fullFilePath)            

        return 0
