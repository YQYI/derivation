#-*-coding:utf-8-*-
import numpy as np
import statistc

#拟合
def polyfit(x, y, maxDegree):
    result =[0,-1]
    for i in range(maxDegree+1):
        args = np.polyfit(x, y, i)
        r=statistc.r2(args,x,y)
        AIC=statistc.AIC(args,x,y)
        BIC=statistc.BIC(args,x,y)

    return result



#extract data
import xlrd
data = xlrd.open_workbook('july.xlsx')
data = data.sheet_by_name('Sheet1')
nr = data.nrows # 获取总行数
parkID=[]
tag=[]
for i in range(nr):
    cell_value1 = data.cell_value(i, 0) # 获取第一行第二列单元格的值
    if cell_value1=="FID_":
        tag.append(i-1)
        tag.append(i+1)
        parkID.append(data.cell_value(i-1, 0))
del tag[0]
tag.append(nr)
#print(tag)

#process
l=len(tag)
i=0
j=0
forWrite=[]
while(i<=l-2):
    yRaw=data.col_slice(4,tag[i],tag[i+1])
    xRaw=data.col_slice(5,tag[i],tag[i+1])
    y=[cell.value for cell in yRaw]
    print(y)
    x=[cell.value for cell in xRaw]
    print(x)
    #拟合
    result=polyfit(x,y,3)
    #计算峰值
    sta=statistc.computeLocalMax(result[0])
    #print(sta)
    forWrite.append([parkID[j],result,sta])
    i+=2
    j+=1

#write
print(forWrite)
import xlwt
f = xlwt.Workbook()
sheet1 = f.add_sheet(u'sheet1', cell_overwrite_ok=True)  # 创建sheet
row0 = [u' ', u'polynomial fitting', u'R^2', u'L', u'LCI']
column0 = [" "]+[i[0] for i in (forWrite)]
for i in range(0, len(row0)):
    sheet1.write(0, i, row0[i])
for i in range(0, len(column0)):
    sheet1.write(i, 0, column0[i])
    if i!=0:
        sheet1.write(i, 1, str(forWrite[i-1][1][0]))
        sheet1.write(i, 2, str(forWrite[i-1][1][1]))
        sheet1.write(i, 3, str(forWrite[i-1][2][0]))
        sheet1.write(i, 4, str(forWrite[i-1][2][1]))
f.save('julyResult.xlsx')  # 保存文件