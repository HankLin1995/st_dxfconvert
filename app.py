import streamlit as st
import pandas as pd
import ezdxf
import base64

# Step 1: 上传 CSV 文件

st.title("CSV to DXF 轉換工具")

# 使用 st.markdown 函數來設置作者名稱的樣式
st.markdown(":boy:**作者：HankLin** ")

# 使用 st.write 函數來設置超連結的樣式
st.markdown("""
    <a href="https://hankvba.blogspot.com/" target="_blank" style="display: inline-block; background-color: #ffcccc; color: black; padding: 5px 20px; border-radius: 5px; text-decoration: none;">部落格</a>
""", unsafe_allow_html=True)


st.divider()

uploaded_file = st.file_uploader(" ##### Step1.上傳 CSV 文件", type="csv")

st.divider()

# Step 2: 选择选项
if uploaded_file is not None:

    st.write(" ##### Step2.CSV檔案配置:")

    has_header = st.radio("是否具有標題行?", ('是', '否'),1)
    nez_order = st.selectbox("選擇 N.E.Z.CD 顺序", ['N,E,Z,CD', 'E,N,Z,CD'])
    txtheight=st.text_input("請輸入文字高度",1.5)

    st.divider()

    # 根据用户选择读取 CSV 文件
    if has_header == '是':
        df = pd.read_csv(uploaded_file)
    else:
        df = pd.read_csv(uploaded_file, header=None)

    st.write("CSV檔案內容")

    st.dataframe(df)

    st.divider()
    # Step 3: 转换成 DXF 文件
    # 创建一个新的 DXF 文档
    if(st.button("Step3.繪製點資料","submit")):

        doc = ezdxf.new('R2010')
        msp = doc.modelspace()
        
        # 根据 NEZ 顺序添加点到 DXF
        order_mapping = {
            'N,E,Z,CD': (0, 1, 2,3),
            'E,N,Z,CD': (1, 0, 2,3),
        }
        order = order_mapping[nez_order]
        
        for index, row in df.iterrows():
            x, y, z = row[order[0]], row[order[1]], row[order[2]]
            point = (x,y,z)
            cd=row[order[3]]
            msp.add_point(point)
            text_content = f'{cd}'
            text = msp.add_text(text_content, dxfattribs={'insert': (x + 1, y + 1, z), 'height': txtheight})
        
        # 保存 DXF 文件
        dxf_file = "output.dxf"
        doc.saveas(dxf_file)
        
        st.balloons()

        st.success("DXF 文件已生成並可供下載！")

 
        download_html = """
        <a href="data:file/output.dxf;base64,{file_data}" download="output.dxf">
        <button style="background-color: #1f77b4; color: white; padding: 10px 10px; border-radius: 5px; border: none; cursor: pointer;">
            Step4.下載DXF
        </button>
        </a>
        """

        # 讀取 DXF 文件並轉換為 base64 格式
        with open(dxf_file, "rb") as file:
            file_data = file.read()
            file_data = base64.b64encode(file_data).decode('utf-8')

        # 在 Streamlit 中顯示 HTML
        st.markdown(download_html.format(file_data=file_data), unsafe_allow_html=True)


