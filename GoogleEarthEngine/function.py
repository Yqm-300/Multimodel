import ee

#ndvi计算函数，返回增加ndvi的图片
def ndvi(image):
    ndvi = image.normalizedDifference(['B5', 'B4']).rename('NDVI')
    return image.addBands(ndvi)

# 创建一个函数来计算NDVI的均值
#算的是一张图片所有像素点的平均值
def ndvi_mean_single(image):
    mean = image.reduceRegion(reducer=ee.Reducer.mean(),  scale=30, maxPixels=1e9)#计算所有波段的平均值
    return image.set('meanNDVI', mean.get('NDVI'))

#计算一张图片的平均lst
def lst_mean_single(image):
    mean = image.reduceRegion(reducer=ee.Reducer.mean(),  scale=30, maxPixels=1e9)#计算所有波段的平均值
    return image.set('meanLst', mean.get('LST_Day_1km'))

#从图片中获取日期和值的列表
def ndvi_dates_values(ndvi_data):
    dates = [ee.Date(image['properties']['system:time_start']).format('YYYY-MM-dd').getInfo() for image in ndvi_data['features']]
    ndvi_values = [image['properties']['meanNDVI'] for image in ndvi_data['features']]
    return dates, ndvi_values

#对两个列表的数据去重（取平均）
from collections import defaultdict
def remove_duplicates(Dates,Values):
    # 使用 defaultdict 存储相同日期的值
    date_to_values = defaultdict(list)

    # 将相同日期的值存储在 defaultdict 中
    for date, value in zip(Dates, Values):
        date_to_values[date].append(value)

    # 计算每个日期的平均值
    unique_dates = []
    average_ndvi_values = []

    for date, values in date_to_values.items():
        unique_dates.append(date)
        average_value = sum(values) / len(values)
        average_ndvi_values.append(average_value)

    # 将日期和 NDVI 值列表进行排序并分别保存
    sorted_data = sorted(zip(unique_dates, average_ndvi_values), key=lambda x: x[0])
    sorted_dates, sorted_values = zip(*sorted_data)
    return sorted_dates,sorted_values

#先计算最大值图片的平均最大值
def ndvi_meanMax(image):
    mean = image.reduceRegion(reducer=ee.Reducer.mean(), scale=30, maxPixels=1e9)#计算所有波段的平均值
    return image.set('meanNDVI', mean.get('NDVI'))