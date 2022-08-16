import pandas as pd
import matplotlib.pyplot as plt
import random

df = pd.read_excel('C:\\Users\\Mate\\Desktop\\wltp\\wltp2.xlsx', 'wltp2')
df1 = pd.read_excel('C:\\Users\\Mate\\Desktop\\wltp\\wltp2.xlsx', 'Munka1')
df2 = pd.read_excel('C:\\Users\\Mate\\Desktop\\wltp\\wltp2.xlsx', 'Munka2')
plt.plot(df['speed'], df['Time'])
plt.plot(df1['minusz'], df['Time'])
plt.plot(df2['plusz'], df['Time'])


plt.xlabel('speed(km\h)')
plt.ylabel('time(sec)')
plt.title('wltp')
plt.legend()

plt.show()
