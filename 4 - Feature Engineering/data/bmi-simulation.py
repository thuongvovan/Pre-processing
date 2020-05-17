import pandas as pd
import numpy as np

bmi= np.random.normal(loc= 23, size= 300, scale= 2.5)
bmi= np.round(bmi, 2)
ton_giao= []

for i in range(247):
    ton_giao.append('Khong')
    
for i in range(24):
    ton_giao.append('Cong_Giao')

for i in range(21):
    ton_giao.append('Phat_Giao')
    
for i in range(2):
    ton_giao.append('Cao_Dai')  

for i in range(3):
    ton_giao.append('Hoi_Giao')

for i in range(2):
    ton_giao.append('Tin_Lanh')

for i in range(1):
    ton_giao.append('Hoa_Hao')

gioi_tinh= []
for i in range(188):
    gioi_tinh.append('Nam')
for i in range(300 - 188):
    gioi_tinh.append('Nu')

for i in range(10):
    np.random.shuffle(ton_giao)
    np.random.shuffle(gioi_tinh)


data= pd.DataFrame({'gioi_tinh': gioi_tinh, 'ton_giao': ton_giao, 'bmi': bmi})
data.to_csv('/Users/vovanthuong/Desktop/5 - Data Pre-processing and analysis/Chapter 5 - Feature Engineering/data/bmi-simulation.csv')
