import sqlite3


DB_PATH = "booking.db"


def ClientMenu(Client):  # 選單
    print()
    print(f"你好 {Client} 需要什麼服務?")
    print("0 / Enter 離開\n" + "1 預定席位\n" + "2 修改訂位資訊\n" + "3 取消訂位\n" + "4 查詢訂位內容")
    print("-" * 24)


def ClientBK(uid, uphone, unumber, sday, stime) -> bool:  # 客戶訂位
    try:
        conn = sqlite3.connect(DB_PATH)
        conn.execute(
            """
            INSERT INTO Booking (Day, Name, Phone, Number, Time)
            SELECT ?, ?, ?, ?, ?
            WHERE NOT EXISTS (
                SELECT 1 FROM Booking
                WHERE Name = ? AND Phone = ? AND Number = ? AND Day = ? AND Time = ?
            );
            """,
            (sday, uid, uphone, unumber, stime, uid, uphone, unumber, sday, stime),
        )
        conn.commit()
        conn.close()
    except Exception as e:
        print(f"=>資料庫連接或資料表建立失敗，錯誤訊息為{e}")
        return False
    else:
        print("訂位成功")
        return True


def ClientEdit(uid, uphone, unumber, sday, stime):  # 修改訂位內容
    try:
        conn = sqlite3.connect(DB_PATH)
        cursor = conn.execute("select * from Booking where Phone=?", uphone)
        data = cursor.fetchall()
        print("\n原訂位內容：")
        if len(data) > 0:
            for record in data:
                print(f"日期:{record[3]}，時段:{record[4]}")
        conn.execute(
            "update Booking set Day=? and Time=?\
                where Name=? and Phone=? and Number=?",
            (sday, stime, uid, uphone, unumber),
        )
        cursor = conn.execute(
            "select * from Booking where Name=? and Phone=? and Number=?",
            (uid, uphone, unumber),
        )
        data = cursor.fetchall()
        print("修改成功")
        print("\n修改後訂位內容：", end="")
        if len(data) > 0:
            for record in data:
                print(f"日期:{record[3]}，時段:{record[4]}")
        conn.commit()
        conn.close()
    except Exception as e:
        print(f"=>資料庫連接或資料表建立失敗，錯誤訊息為{e}")


def ClientSearch(uphone):  # 查詢訂位內容
    if type(uphone) is not tuple:
        uphone = (uphone,)
    try:
        conn = sqlite3.connect(DB_PATH)
        cursor = conn.execute("select * from Booking where Phone=?", uphone)
        data = cursor.fetchall()
        print("\n已訂位時段：")
        if len(data) > 0:
            for record in data:
                return record
        conn.commit()
        conn.close()
    except Exception as e:
        print(f"=>資料庫連接或資料表建立失敗，錯誤訊息為{e}")
