import xlrd
import csv

def csv_from_excel():
    wb = xlrd.open_workbook('excel_file.xlsx')
    sh = wb.sheet_by_name('sheet_name')
    your_csv_file = open('your_csv_file.csv', 'w')
    wr = csv.writer(your_csv_file, quoting=csv.QUOTE_ALL)

    for rownum in range(sh.nrows):
        wr.writerow(sh.row_values(rownum))

    your_csv_file.close()

# runs the csv_from_excel function:
csv_from_excel()