#!/usr/bin/env python
# coding: utf-8

# # 준비

# In[78]:


import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import numpy as np

plt.rc("font", family='Malgun Gothic')
plt.rc('axes', unicode_minus=False)

pd.Series([-4,1,0,3,4,5]).plot(title='한글폰트 설정')


# In[79]:


df= pd.read_csv('C:/Users/zhddl/data/서울특별시 사회복지시설 목록.csv', encoding='CP949')


# # 데이터 분석

# In[80]:


df.head()


# In[81]:


df.tail()


# In[82]:


df.info()


# In[83]:


df.dtypes


# # 정리

# ## 컬럼 삭제

# In[84]:


df= df.drop(['시설코드','시군구코드'], axis=1)
df.head()


# ## 시군구명 정리

# In[85]:


df['시군구명'].value_counts()


# In[86]:


# 시군구명에 있는 서울특별시들 확인

df_del= df[df['시군구명'].str.contains('서울')]
df_del


# In[87]:


# 경기도 제거

df= df.drop([1508,1581,1663,1688,1966], axis=0)
df.reset_index(inplace=True, drop=True)
df[df['시군구명'].str.contains('서울')]


# In[88]:


# 서울 시군구명 변경... 하...........

df.loc[df.시설명 == '한국아동복지시설연합회', ('시군구명')] = '용산구'
df.loc[df.시설명 == '행복이가득한집2호', ('시군구명')] = '강서구'
df.loc[df.시설명 == '(사)굿하트데이케어센터', ('시군구명')] = '동작구'
df.loc[df.시설명 == '서울시학대피해노인전용쉼터', ('시군구명')] = '도봉구'
df.loc[df.시설명 == '서울시건강가정지원센터', ('시군구명')] = '중구'
df.loc[df.시설명 == '서울시정신보건센터', ('시군구명')] = '강남구'


# In[89]:


# 확인
df['시군구명'].value_counts()


# ## 요약하고 확인

# In[90]:


df[['시군구명','시설종류상세명(시설종류)']]


# In[91]:


df['시설종류상세명(시설종류)'].describe()


# In[92]:


df['시설종류상세명(시설종류)'].value_counts()


# In[93]:


df['시설종류명(시설유형)'].value_counts()


# In[94]:


h= df['시설종류명(시설유형)'].value_counts()
h.sort_values().plot.barh(figsize=(7,18))


# In[95]:


#
n= df['시설종류상세명(시설종류)'].value_counts()
n.sort_values().plot.barh(figsize=(7,8))


# In[ ]:





# # 시각화

# In[96]:


plt.figure(figsize=(17,4))
sns.countplot(data=df,x='시군구명')


# ## 서브셋

# In[97]:


df_old= df[df['시설종류명(시설유형)'].str.contains('노인')]
df_old


# In[98]:


df_chi= df[df['시설종류명(시설유형)'].str.contains('아동')]
df_chi


# In[99]:


df_dis= df[df['시설종류명(시설유형)'].str.contains('장애인')]
df_dis


# ## 구별 시설 수

# In[100]:


df_t= df.groupby(['시군구명','시설종류상세명(시설종류)'])['자치구(시)구분'].count()
df_t.loc['노원구']


# In[101]:


t= df.groupby(['시군구명','시설종류상세명(시설종류)'])['자치구(시)구분'].count()
t


# In[102]:


# 노인 관련 시설이 가장 많다.

t.sort_values().loc['노원구'].plot.barh(figsize=(10,7))


# In[103]:


# 노원구와는 다르게 노인복지시설 다음으로 장애인 거주시설이 많다.

t.sort_values().loc['강서구'].plot.barh(figsize=(10,7))


# In[121]:


t.sort_values().loc['송파구'].plot.barh(figsize=(10,7))


# In[120]:


# 제일 시설 수가 적은 중구를 확인해보니 이곳도 역시 노인 복지시설이 많다.

t.sort_values().loc['중구'].plot.barh(figsize=(10,7))


# In[105]:


t_re= t.reset_index()
df_t= t_re.rename(columns={'자치구(시)구분':'시설수'})
df_t.head()


# In[106]:


sns.catplot(data=df_t, x='시설종류상세명(시설종류)',y='시설수', kind='bar'
            ,col='시군구명',col_wrap=4)


# ## 노인/ 장애인으로 구별

# ### 노인

# In[107]:


old= df_old.groupby(['시군구명','시설종류상세명(시설종류)'])['자치구(시)구분'].count()
old


# In[108]:


n= old.reset_index()
df_o= n.rename(columns={'자치구(시)구분':'시설수'})
df_o.head()


# In[109]:


plt.figure(figsize=(13,5))
sns.barplot(data=df_o, x='시설종류상세명(시설종류)',y='시설수',ci=None)


# ### 장애인

# In[110]:


disabled= df_dis.groupby(['시군구명','시설종류상세명(시설종류)'])['자치구(시)구분'].count()
disabled


# In[111]:


x= disabled.reset_index()
df_d= x.rename(columns={'자치구(시)구분':'시설수'})
df_d.head()


# In[112]:


plt.figure(figsize=(13,5))
sns.barplot(data=df_d, x='시설종류상세명(시설종류)',y='시설수',ci=None)


# In[ ]:





# # 지도에 표시

# In[123]:


import geopy
# Nominatim 서비스 객체에 대한 핸들러 가져 오기
service = geopy.Nominatim(user_agent = "myGeocoder")
# Nominatim (예 : OSM) 서비스를 사용하여 도시 이름을 지오 코딩합니다.
service.geocode('대한민국')


# In[127]:


df.head()


# In[124]:


# 위에서 보고 주소 가져오기
loc_se = service.geocode('서울특별시 중랑구 신내로 194')
#위도
print(loc_se.latitude)
#경도 
print(loc_se.longitude)


# In[128]:


m = folium.Map(location = [loc_se.latitude,loc_se.longitude], zoom_start = 15)

folium.Marker(location = [loc_se.latitude,loc_se.longitude],tooltip="서울꽃동네신내노인요양원").add_to(m)


m

