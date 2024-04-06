import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

def predict_rfm_segment(R, F, M):
    
    R_Score = None
    F_Score = None
    M_Score = None

    
    R_Quartiles = [143, 50, 17]  
    F_Quartiles = [1, 2, 5]     
    M_Quartiles = [307, 674, 1661]  

    R_Score = 4 - sum(R > q for q in R_Quartiles)
    F_Score = 1 + sum(F > q for q in F_Quartiles)
    M_Score = 1 + sum(M > q for q in M_Quartiles)

    # Segment assignment logic
    if R_Score >= 3 and F_Score >= 3 and M_Score >= 3:
        return 'Top Customers'
    elif F_Score >= 3:
        return 'Loyal Customers'
    elif M_Score >= 3:
        return 'Big Spenders'
    elif R_Score == 1 or R_Score == 2:
        return 'At Risk'
    else:
        return 'Lost/Inactive'
    


# Using menu
st.title("Project 3: Customer Segmentation")
menu = ["Giới thiệu Project", "Insight dữ liệu", "Mô hình dự đoán"]
choice = st.sidebar.selectbox('Danh mục', menu)
if choice == 'Giới thiệu Project':    
    # st.subheader("Customer Segmentation")  
# elif choice == 'Giới thiệu Project':    
    # st.subheader("Project 3: Customer Segmentation")
    st.write("""### Mục tiêu:
    - Tìm hiểu insight tập dữ liệu
    - Dự đoán customer segmentation""")
    st.write("""### Quy trình xây dựng mô hình:
    - Tiền xử lý dữ liệu, EDA
    - Xử lý dữ liệu trùng, handle missing Customer ID as Unknown Customer
    - Xây dựng model
    - Dự đoán
    - Xây dựng giao diện""")
    st.write("""### Tác giả:
    Trần Thanh Phong
    Nguyễn Ngọc Quỳnh""")
elif choice == 'Insight dữ liệu':
    st.subheader("1. Thống kê về các quốc gia mua hàng")
    st.write("10 quốc gia mua hàng nhiều nhất và ít nhất (ngoại trừ UK)")
    st.image("country.jpg")
    st.write("Số lượng hàng bán ở các quốc gia (ngoại trừ UK)")
    st.image("country_wise.png")
    
    st.subheader("2. Thống kê về sản phẩm")
    st.write("Các sản phẩm có giá cao nhất")
    st.image("products.png")
    st.write("Các sản phẩm được bán nhiều nhất")
    st.image("most_products_sale.png")
    
    st.subheader("3. Thống kê về thời gian mua hàng trong năm")
    st.image("time.png")

    st.subheader("4. Phân phối RFM của tập dữ liệu")
    st.image("RFM.png")

    st.subheader("5. Customer Segments")
    st.image("treemap.png")
    st.image("newplot.png")

    st.subheader("Top Customers:")
    st.write("""Những khách hàng này là những người mua thường xuyên, mới mua gần đây và chi tiêu một số tiền đáng kể.
             Chiến lược: tập trung vào việc giữ chân, upsell và cross-sell. Các ưu đãi độc quyền, khả năng tiếp cận sớm các sản phẩm mới và các chương trình khách hàng thân thiết""")
    
    st.subheader("Loyal Customers:")
    st.write("""Tần suất mua hàng cao và mức chi tiêu của đáng kể nhưng không phải là cao nhất. 
                Chiến lược: Khuyến khích những khách hàng này tăng chi tiêu bằng cách cá nhân hóa và các ưu đãi theo gói, duy trì sự gắn kết""")

    st.subheader("Big Spenders:")
    st.write("""Những khách hàng này chi tiêu rất nhiều khi mua hàng nhưng họ có thể không thực hiện việc này thường xuyên hoặc gần đây. 
                Chiến lược: Thu hút lại những khách hàng này bằng hoạt động tiếp thị được cá nhân hóa, tập trung vào các mặt hàng có giá trị cao phù hợp với lịch sử mua hàng của họ.""")

    st.subheader("At Risk:")
    st.write("""Khách hàng đã lâu không mua nhưng họ đã thường xuyên mua sắm hoặc chi tiêu nhiều. 
                Chiến lược: triển khai các chiến dịch thu hút lại bằng các ưu đãi đặc biệt hoặc lời nhắc nhở về những gì họ đang thiếu. Khảo sát để hiểu lý do tại sao họ ko thường xuyên mua nữa.""")
    
    st.subheader("Lost/Inactive:")
    st.write("""Nhóm KH đã không mua hàng trong một thời gian dài, không mua hàng thường xuyên và chi tiêu rất ít.
    Chiến lược: Xem xét các chiến dịch  với các ưu đãi hoặc cập nhật sản phẩm hấp dẫn có thể khiến họ quan tâm dựa trên hành vi trước đây của họ. Tuy nhiên, ưu tiên tập trung nguồn lực trên các phân khúc có khả năng tạo giá trị cao hơn, đặc biệt là Top Customers.""")

if choice=='Mô hình dự đoán':
    # import pickle
    # with open("customer_segment.pkl", 'wb') as file:  
    #     customer_segment = pickle.load(file)
    st.write("##### 1. Some data")
    # Chọn nhập mã khách hàng hoặc nhập thông tin khách hàng vào dataframe
    st.write("##### 1. Chọn cách nhập thông tin khách hàng")
    type = st.radio("Chọn cách nhập thông tin khách hàng", options=["Nhập mã khách hàng", 
                                                                    "Nhập thông tin khách hàng vào dataframe"])
    if type == "Nhập mã khách hàng":
        # Nếu người dùng chọn nhập mã khách hàng
        st.subheader("Nhập mã khách hàng")
        # Tạo điều khiển để người dùng nhập mã khách hàng
        customer_id = st.text_input("Nhập mã khách hàng")
        # Nếu người dùng nhập mã khách hàng, thực hiện các xử lý tiếp theo
        # Có KH này trong dữ liệu không (nếu có thì tiếp tục xử lý, nếu không thì thông báo không có KH này trong dữ liệu)
        # Đề xuất khách hàng thuộc cụm nào
        # In kết quả ra màn hình
        st.write("Mã khách hàng đề xuất: 16333, 14733, 12435")
        # st.write("Mã khách hàng:", customer_id)
        segments_df = pd.read_csv('rfm2.csv')
        segments_df['CustomerID'] = segments_df['CustomerID'].astype(str)
        if st.button('Find Customer Segment'):
            segment = segments_df.loc[segments_df['CustomerID'] == str(customer_id)]
        if not segment.empty:
            st.write(segment)
        else:
            st.write("Không tìm thấy Customer ID")
        # segment = customer_segment(customer_id)
        # st.write(f"The segment for Customer ID {customer_id} is: {segment}")
    else:
        # Nếu người dùng chọn nhập thông tin khách hàng vào dataframe có 3 cột là Recency, Frequency, Monetary
        st.write("##### 2. Thông tin khách hàng")
        # Tạo điều khiển table để người dùng nhập thông tin khách hàng trực tiếp trên table
        st.write("Nhập thông tin khách hàng")
        # Tạo dataframe để người dùng nhập thông tin khách hàng
        df_customer = pd.DataFrame(columns=["Recency", "Frequency", "Monetary"])
        for i in range(1):
            st.write(f"Khách hàng {i+1}")
            # Tạo các slider để nhập giá trị cho cột Recency, Frequency, Monetary
            recency = st.slider("Recency", 1, 365, 100, key=f"recency_{i}")
            frequency = st.slider("Frequency", 1, 50, 5, key=f"frequency_{i}")
            monetary = st.slider("Monetary", 1, 1000, 100, key=f"monetary_{i}")

            
            if st.button('Predict'):
                          
        # Thực hiện phân cụm khách hàng dựa trên giá trị của 3 cột này
                segment = predict_rfm_segment(R=recency, F=frequency, M=monetary)  # Example R, F, M values
                st.success(f'The predicted customer segment is: {segment}')
               
       # Done
    
    
    
        

        
        

    



