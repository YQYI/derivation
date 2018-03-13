#-*-coding:utf-8-*-
import numpy as np
import statistc

#拟合
def polyfit(x, y, maxDegree):
    """

    :param x:feature
    :param y: class
    :param maxDegree: maxDgree
    :return: args meas function parameters
    """
    args=[]
    for i in range(maxDegree+1):
        args.append(list(np.polyfit(x, y, i)))
    return args


#find each park's range
def locate_park(file_name, table_name, ID):
    """

    :param file_name: xlsx file name
    :param table_name: sheet name
    :param ID: such as '_FID_'
    :return: tag means row range,parkID records park name
    """
    import xlrd
    data = xlrd.open_workbook(file_name).sheet_by_name(table_name)
    park_name=[]
    tag=[]
    for i in range(data.nrows):
        cell_value1 = data.cell_value(i, 0) # 获取第一行第二列单元格的值
        if cell_value1==ID:
            tag.extend([i-1, i+1])
            park_name.append(data.cell_value(i-1, 0))
    del tag[0]
    tag.append(data.nrows)
    return tag, park_name


def loop_compute(file_name, table_name, ID):
    """

    :param file_name: xlsx file name
    :param table_name: sheet name
    :return:
    """
    import xlrd
    # file_name='March.xlsx'
    # table_name='Sheet1'
    data = xlrd.open_workbook(file_name).sheet_by_name(table_name)
    tag, park_name = locate_park(file_name, table_name, ID)
    l=len(tag)//2
    i=0
    content=[]
    while(i<l):
        yRaw=data.col_slice(4,tag[i*2],tag[i*2+1])
        xRaw=data.col_slice(5,tag[i*2],tag[i*2+1])
        y=[cell.value for cell in yRaw]
        x=[cell.value for cell in xRaw]
        #拟合
        result=polyfit(x, y, 6)
        r = []
        aic = []
        bic = []
        peak_x_y = []
        for args in result:
            r.append(statistc.r2(args,x,y))
            aic.append(statistc.AIC(args, x, y))
            bic.append(statistc.BIC(args, x, y))
            peak_x_y.append(statistc.min_local_max(args))
        #计算峰值
        #sta=statistc.computeLocalMax(result[0])
        #print(sta)
        content.append([park_name[i],result,r,aic,bic,peak_x_y])
        i+=1
    return content


def write_file(content,file_name):
    #write
    import xlwt
    f = xlwt.Workbook()
    sheet1 = f.add_sheet(u'sheet1', cell_overwrite_ok=True)  # 创建sheet
    row0 = [u' ', u'多项式', u'R*2', u'AIC', u'BIC', u'P', u'peakX', u'peakY']
    #column0 = [i[0] for i in (content)]
    for i in range(0, len(row0)):
        sheet1.write(0, i, row0[i])
    for i in range(0, len(content)):
        sheet1.write(i*8+1, 0, content[i][0])
        for j in range(7):
            sheet1.write(i*8+j+1, 1, str(content[i][1][j]))
            sheet1.write(i*8+j+1, 2, str(content[i][2][j]))
            sheet1.write(i * 8 + j + 1, 3, str(content[i][3][j]))
            sheet1.write(i * 8 + j + 1, 4, str(content[i][4][j]))
            sheet1.write(i * 8 + j + 1, 6, str(content[i][5][j][0]))
            sheet1.write(i * 8 + j + 1, 7, str(content[i][5][j][1]))
    f.save(file_name)  # 保存文件


file_name = 'March.xlsx'
save_file = 'MarchResult1.xlsx'
table_name = 'Sheet1'
ID = 'FID_'
content = loop_compute(file_name, table_name, ID)
print(content)
write_file(content, save_file)
