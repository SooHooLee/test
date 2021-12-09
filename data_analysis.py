import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import warnings
warnings.filterwarnings("ignore")
import streamlit as st
from windrose import WindroseAxes
from statsmodels.tsa.stattools import acf
from statsmodels.graphics.tsaplots import plot_acf
warnings.filterwarnings("ignore")
plt.rcParams['font.sans-serif'] = ['SimHei'] #正常显示中文标签
plt.rcParams['axes.unicode_minus'] = False #正常显示负号


if __name__ == '__main__' :
    st.title("SCADA数据分析")
    # ---------------------------主栏-----------------------
    # ---------------------------读入数据-----------------------
    st.write("")
    st.write("")
    st.header('------------------------数据读入------------------------')  # 设置主栏第一部分
    st.sidebar.header('-----------------数据读入-----------------')  # 设置设置侧栏第一部分
    st.sidebar.subheader('* 数据上传 *')
    st.subheader('* 数据说明 *')
    file = st.sidebar.file_uploader('上传数据', type=['csv'], key=None)
    scada_data = pd.read_csv(file)
    # df = get_data(file)
    st.dataframe(scada_data)

    # ---------------------------选择时间序列-----------------------
    st.sidebar.subheader('* 时间序列 *')
    st.subheader('* 时间序列 *')
    options = np.array(scada_data['real_time']).tolist()
    (start_time, end_time) = st.select_slider("请选择时间序列：", options=options,
                                              value=(options[0], options[len(options) - 1]))
    # setting index as date
    scada_data['real_time'] = pd.to_datetime(scada_data['real_time'], format='%Y-%m-%d')
    scada_data.index = scada_data['real_time']
    st.write("序列开始时间：", start_time)
    st.write("序列结束时间：", end_time)
    scada_data = scada_data[start_time:end_time]
    st.dataframe(scada_data)
    # ---------------------------数据分析-----------------------
    st.header('------------------------数据分析------------------------')  # 设置主栏第一部分
    st.sidebar.header('-----------------数据分析-----------------')  # 设置设置侧栏第一部分
    # -----------时变特性分析-----------------
    st.sidebar.subheader('* 时变特性分析 *')
    st.subheader('* 时变特性分析 *')
    type = st.sidebar.selectbox('请选择分析对象：',
                                ('ActivePower', 'WindSpeed', 'NacellePosition', 'WindDirction', 'AirPressure',
                                 'Temperature',
                                 'PitchAngle', 'ErrorMode', 'OperationMode', 'GeratorSpeed', 'RotorSpeed',
                                 'AirDensity'))
    st.write("选择的分析对象为：", type)
    st.line_chart(scada_data[type])
    # -----------风玫瑰图-----------------
    st.sidebar.subheader('* 风玫瑰图 *')
    st.subheader('* 风玫瑰图 *')
    ws = scada_data['WindSpeed']
    wd = scada_data['WindDirction']
    ax = WindroseAxes.from_ax()
    fig = ax.bar(wd, ws, normed=True, opening=0.8, edgecolor='white')
    st.set_option('deprecation.showPyplotGlobalUse', False)
    st.pyplot(fig)
    # -----------相关性分析-----------------
    st.sidebar.subheader('* 相关性分析 *')
    st.subheader('* 相关性分析 *')
    # data.corr()计算相关系数
    # Pearson相关性
    st.sidebar.subheader(" (1) Pearson相关系数")
    st.subheader(" (1) Pearson相关系数")
    corr = scada_data.corr()
    st.write("相关性系数:", corr)
    fig, ax = plt.subplots(figsize=(8, 8))  # 调整画布大小
    ax = sns.heatmap(corr, vmax=.8, square=True, annot=True)  # 画热力图   annot=True 显示系数
    st.pyplot(fig)
    # 自相关性acf
    st.sidebar.subheader(" (2) 自相关性")
    st.subheader(" (2) 自相关性")
 

    type_acf = st.sidebar.selectbox('请选择自相关性分析对象：',
                                    (
                                        'ActivePower', 'WindSpeed', 'NacellePosition', 'WindDirction', 'AirPressure',
                                        'Temperature',
                                        'PitchAngle', 'ErrorMode', 'OperationMode', 'GeratorSpeed', 'RotorSpeed',
                                        'AirDensity'))
    st.write("选择的自相关性分析对象为：", type_acf)
    lags = st.sidebar.number_input("请输入自相关性的阶数：", min_value=1, max_value=200, value=30, step=1)
    st.write("选择的自相关性阶数为：", lags)
#     data_acf = acf(scada_data[type_acf], unbiased=False, nlags=lags, qstat=False, fft=None, alpha=None, missing='none')
#     st.write("自相关性系数：", data_acf)
    plot_acf(scada_data[type_acf])
    st.pyplot()




