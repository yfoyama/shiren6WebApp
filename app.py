import pandas as pd
import streamlit as st

st.title('シレン６ アイテム価格判別')

# Excelファイルのパス
file_path = r'C:\Users\yyy_f\OneDrive\デスクトップ\sandbox\shiren6WebApp\itemList.xlsx'

# Excelファイルを読み込む
df = pd.read_excel(file_path)

# fullname列を作成（correctionValueを整数で表示）
df['fullname'] = df.apply(lambda x: f"{x['name']}({x['status']})" + (f"[{int(x['correctionValue'])}]" if pd.notnull(x['correctionValue']) else ''), axis=1)

# サイドバー
with st.sidebar:
    # 入力フォーム
    price_input = st.number_input('価格を入力してください（10~10000）', min_value=10, max_value=10000, step=10,value=100)
    price_type = st.radio('価格タイプを選択してください', ('売値', '買値'))
    kind_selection = st.radio('種類を選択してください', ('すべて', '腕輪', '壺', '巻物', '草種', '杖'))

    # 検索ボタン
    search_clicked = st.button('検索')

# 検索結果の処理と表示
if search_clicked:
    if price_type == '売値':
        result_df = df[df['sellingPrice'] == price_input]
    else:  # 買値の場合
        result_df = df[df['buyingPrice'] == price_input]
    
    # 種類でフィルタリング
    if kind_selection != 'すべて':
        result_df = result_df[result_df['kind'] == kind_selection]
    
    # 結果をkind列でソート
    result_df = result_df.sort_values(by='kind')
    
    # 検索結果の表示
    if not result_df.empty:
        # st.write('検索結果:')
        for fullname in result_df['fullname']:
            # 呪いや祝福の項目に色を付ける
            if '(呪い)' in fullname:
                st.markdown(f"<span style='color: red;'>{fullname}</span>", unsafe_allow_html=True)
            elif '(祝福)' in fullname:
                st.markdown(f"<span style='color: blue;'>{fullname}</span>", unsafe_allow_html=True)
            else:
                st.write(fullname)
    else:
        st.write('該当するデータがありません。')

