import streamlit as st
import pandas as pd

import requests

# サンプルのリスト
data_list = [
    {
        "serial_number": "1421723021274",
        "camera_id": "b5fc1e7d-27fd-4a2f-bc2b-415761c20152",
        "transactionId": "80cf96ed-08f5-4528-8e79-b6c9deb80c7e",
        "camera_name": "6faisle",
        "camera_ip": "192.168.1.194",
        "integration_type": "box",
        "timezone": "Asia/Tokyo",
        "category": "ids",
        "date": "2023-12-22T13:33:42.212Z",
        "label[]": "person",
        "object_probability[]": "0.83839",
        "height[]": "0.271443",
        "width[]": "0.225684",
        "x[]": "0.732196",
        "y[]": "0.71357",
    },
    {
        "serial_number": "1421723021275",
        "camera_id": "b5fc1e7d-27fd-4a2f-bc2b-415761c20153",
        "transactionId": "80cf96ed-08f5-4528-8e79-b6c9deb80c7f",
        "camera_name": "7faisle",
        "camera_ip": "192.168.1.195",
        "integration_type": "box",
        "timezone": "Asia/Tokyo",
        "category": "ods",
        "date": "2023-12-23T13:33:42.212Z",
        "label[]": "person",
        "object_probability[]": "0.83839",
        "height[]": "0.271443",
        "width[]": "0.225684",
        "x[]": "0.732196",
        "y[]": "0.71357",
    },
    {
        "serial_number": "1421723021276",
        "camera_id": "b5fc1e7d-27fd-4a2f-bc2b-415761c20154",
        "transactionId": "80cf96ed-08f5-4528-8e79-b6c9deb80c7g",
        "camera_name": "8faisle",
        "camera_ip": "192.168.1.196",
        "integration_type": "box",
        "timezone": "Asia/Tokyo",
        "category": "ids",
        "date": "2023-12-24T13:33:42.212Z",
        "label[]": "person",
        "object_probability[]": "0.83839",
        "height[]": "0.271443",
        "width[]": "0.225684",
        "x[]": "0.732196",
        "y[]": "0.71357",
    },
]

# DataFrameの作成
df = pd.DataFrame(data_list)

# 日付をdatetime型に変換
df["date"] = pd.to_datetime(df["date"])

# 日付でソート
df.sort_values(by="date", inplace=True)

# カテゴリを選択してチャートに表示をする項目を変更するチェックボックス
selected_categories = st.sidebar.multiselect(
    "表示するカテゴリを選択してください", df["category"].unique()
)

# カメラを選択してチャートに表示をする項目を変更するチェックボックス
selected_cameras = st.sidebar.multiselect(
    "表示するカメラを選択してください", df["camera_name"].unique()
)


# 特定のカメラ名を入力する入力ボックス
specific_camera_name = st.sidebar.text_input("特定のカメラ名を入力してください")

# "特定のカメラ名を入力する入力ボックス"に入力された値でフィルターされたデータを一覧表示するチャート
if specific_camera_name:
    filtered_df = df[df["camera_name"] == specific_camera_name]
    st.subheader(f"{specific_camera_name} のデータ")
    st.write(filtered_df)

# 選択されたカテゴリとカメラでデータをフィルタリング
filtered_df = df[
    (df["category"].isin(selected_categories))
    & (df["camera_name"].isin(selected_cameras))
]

# カメラ名ごとの件数を数える
camera_name_counts = filtered_df["camera_name"].value_counts()
# categoryごとの件数を数える
category_counts = filtered_df["category"].value_counts()

# Streamlitアプリ
st.title("Cameleo メタデータ取得")

# カメラ名ごとの棒グラフ
st.subheader("カメラ名ごとの件数")
st.bar_chart(camera_name_counts)

# カテゴリごとの棒グラフ
st.subheader("カテゴリごとの件数")
st.bar_chart(category_counts)


# 関数: データを更新する
def update_data():
    try:
        # リクエストを送信してデータを取得
        response = requests.get(
            "https://humane-sharply-toucan.ngrok-free.app/get_1hour_metadata"
        )
        if response.status_code == 200:
            return response.json()
        else:
            st.error(
                f"データの更新に失敗しました。ステータスコード: {response.status_code}"
            )
            return None
    except requests.exceptions.RequestException as e:
        st.error(f"データの更新に失敗しました。エラー: {e}")
        return None


# データの更新ボタン
if st.sidebar.button("データを更新する"):
    new_data = update_data()
    print("newdata", new_data)
    if new_data is not None:
        new_data_list = new_data["event_info"]
        if new_data_list:
            st.success("データを取得しました")
            df = pd.DataFrame(new_data_list)
            df["date"] = pd.to_datetime(df["date"])
            df.sort_values(by="date", inplace=True)
            st.success("データを更新しました。")
        else:
            st.success("データ0件取得")
            # 失敗時はデフォルトデータを表示
            df = pd.DataFrame(data_list)
            df["date"] = pd.to_datetime(df["date"])
            df.sort_values(by="date", inplace=True)
            st.success("デフォルトデータを表示しました。")
    else:
        # 失敗時はデフォルトデータを表示
        df = pd.DataFrame(data_list)
        df["date"] = pd.to_datetime(df["date"])
        df.sort_values(by="date", inplace=True)
        st.success("デフォルトデータを表示しました。")

# 更新後のデータを表示
st.write(df)
