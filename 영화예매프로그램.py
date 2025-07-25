# ver3-영화 정보
# 영화 제목, 장르, 개봉일, 감독, 출연 배우 등의 정보를 포함 영화 정보는 관리자가 추가, 수정, 삭제할 수 있는 프로그램

import sqlite3
from sqlite3 import Error
from datetime import datetime

def create_connection():
    conn = None
    try:
        conn = sqlite3.connect('movies.db')
        print("Connection to SQLite DB successful")
        create_table(conn)  # 테이블 생성
    except Error as e:
        print(f"The error '{e}' occurred while connecting to SQLite DB")
    return conn

def create_table(conn):
    cur = conn.cursor()
    cur.execute('''CREATE TABLE IF NOT EXISTS movies 
                (id INTEGER PRIMARY KEY AUTOINCREMENT,
                title TEXT NOT NULL,
                genre TEXT,
                release_date TEXT,
                director TEXT,
                actors TEXT);''')
    print("Table created successfully")

def add_movie(conn, movie):
    sql = '''INSERT INTO movies(title, genre, release_date, director, actors)
             VALUES(?,?,?,?,?)'''
    cur = conn.cursor()
    cur.execute(sql, movie)
    conn.commit()
    print(f"{movie[0]} added successfully.")

def update_movie(conn, movie):
    sql = '''UPDATE movies SET genre=?, release_date=?, director=?, actors=?
             WHERE title=?'''
    cur = conn.cursor()
    cur.execute(sql, (movie[1], movie[2], movie[3], movie[4], movie[0]))
    conn.commit()
    print(f"{movie[0]} updated successfully.")

def delete_movie(conn, title):
    sql = 'DELETE FROM movies WHERE title=?'
    cur = conn.cursor()
    cur.execute(sql, (title,))
    conn.commit()
    print(f"{title} deleted successfully.")

conn = create_connection()

movie1 = ('The Shawshank Redemption', 'Drama', '1994-09-23', 'Frank Darabont', 'Tim Robbins, Morgan Freeman')
add_movie(conn, movie1)
movie2 = ('The Godfather', 'Crime', '1972-03-24', 'Francis Ford Coppola', 'Marlon Brando, Al Pacino')
add_movie(conn, movie2)
movie3 = ('The Dark Knight', 'Action', '2008-07-18', 'Christopher Nolan', 'Christian Bale, Heath Ledger')
add_movie(conn, movie3)

update_movie(conn, ('The Godfather', 'Crime/Drama', '1972-03-24', 'Francis Ford Coppola', 'Marlon Brando, Al Pacino'))
delete_movie(conn, 'The Shawshank Redemption')

conn.close()


# 상영 정보-상영일시, 상영관, 상영시간 등의 정보를 포함, 상영 정보는 관리자가 추가, 수정, 삭제할 수 있어야 합니다.

import sqlite3
from sqlite3 import Error

# 데이터베이스 연결 함수
def create_connection():
    conn = None
    try:
        conn = sqlite3.connect('movies.db')
        print("Connection to SQLite DB successful")
    except Error as e:
        print(f"The error '{e}' occurred while connecting to SQLite DB")
    return conn

# 상영 정보 추가 함수
def add_screening(conn, screening):
    sql = '''INSERT INTO screenings(datetime, theater, duration, movie_id) 
             VALUES(?,?,?,?)'''
    cur = conn.cursor()
    cur.execute(sql, screening)
    conn.commit()
    print("Screening added successfully")

# 상영 정보 수정 함수
def update_screening(conn, screening):
    sql = '''UPDATE screenings 
             SET datetime = ?, theater = ?, duration = ?, movie_id = ?
             WHERE id = ?'''
    cur = conn.cursor()
    cur.execute(sql, screening)
    conn.commit()
    print("Screening updated successfully")

# 상영 정보 삭제 함수
def delete_screening(conn, screening_id):
    sql = '''DELETE FROM screenings WHERE id = ?'''
    cur = conn.cursor()
    cur.execute(sql, (screening_id,))
    conn.commit()
    print("Screening deleted successfully")

# 상영 정보 조회 함수
def get_screenings(conn):
    sql = '''SELECT * FROM screenings'''
    cur = conn.cursor()
    cur.execute(sql)
    rows = cur.fetchall()
    for row in rows:
        print(row)

# 예제 상영 정보
screening1 = ('2023-05-01 15:00', '1관', '120분', 1)

# 데이터베이스 연결
conn = create_connection()

# screenings 테이블 생성
def create_table(conn):
    cur = conn.cursor()
    cur.execute('''CREATE TABLE IF NOT EXISTS screenings 
                (id INTEGER PRIMARY KEY AUTOINCREMENT,
                datetime TEXT NOT NULL,
                theater TEXT NOT NULL,
                duration TEXT NOT NULL,
                movie_id INTEGER NOT NULL,
                FOREIGN KEY (movie_id) REFERENCES movies (id));''')
    print("Table created successfully")

# screenings 테이블 생성
create_table(conn)

# 상영 정보 추가
add_screening(conn, screening1)

# 상영 정보 수정
update_screening(conn, ('2023-05-01 15:30', '1관', '120분', 1, 1))

# 상영 정보 삭제
delete_screening(conn, 1)

# 상영 정보 조회
get_screenings(conn)

# 데이터베이스 연결 종료
conn.close()



# 상영 정보-상영일시, 상영관, 상영시간 등의 정보를 포함, 상영 정보는 관리자가 추가, 수정, 삭제할 수 있어야 합니다.

import sqlite3

def create_table_bookings(conn):
    cur = conn.cursor()
    cur.execute('''CREATE TABLE IF NOT EXISTS bookings
                (id INTEGER PRIMARY KEY AUTOINCREMENT,
                customer_name TEXT NOT NULL,
                customer_phone TEXT NOT NULL,
                movie_title TEXT NOT NULL,
                screening_time TEXT NOT NULL,
                seat_number TEXT NOT NULL,
                payment INTEGER NOT NULL,
                FOREIGN KEY(movie_title) REFERENCES movies(title)
                );''')
    conn.commit()

def add_booking(conn, booking):
    cur = conn.cursor()
    sql = '''INSERT INTO bookings (customer_name, customer_phone, movie_title, screening_time, seat_number, payment)
            VALUES (?, ?, ?, ?, ?, ?)'''
    cur.execute(sql, booking)
    conn.commit()
    print("예매가 완료되었습니다.")

def view_bookings(conn):
    cur = conn.cursor()
    cur.execute("SELECT * FROM bookings")
    rows = cur.fetchall()
    for row in rows:
        print(row)

def update_booking(conn, booking_id, new_payment):
    cur = conn.cursor()
    sql = '''UPDATE bookings SET payment = ? WHERE id = ?'''
    cur.execute(sql, (new_payment, booking_id))
    conn.commit()
    print("예매 정보가 수정되었습니다.")

def delete_booking(conn, booking_id):
    cur = conn.cursor()
    sql = '''DELETE FROM bookings WHERE id = ?'''
    cur.execute(sql, (booking_id,))
    conn.commit()
    print("예매 정보가 삭제되었습니다.")









'''
# ver2
# 필요한 변수 초기화
movie_list = ["명량", "인터스텔라", "어벤져스"]
seat_list = ["S", "A", "B"]
reserved_seats = {}

# 영화 목록 출력
print("영화 목록:")
for i, movie in enumerate(movie_list):
    print(f"{i+1}. {movie}")

# 사용자로부터 영화 선택 및 좌석 예약
while True:
    movie_choice = int(input("예약하실 영화 번호를 입력하세요: "))
    if movie_choice < 1 or movie_choice > len(movie_list):
        print("잘못된 입력입니다. 다시 시도해주세요.")
    else:
        break

while True:
    seat_choice = input("예약하실 좌석 등급을 입력하세요 (S, A, B): ")
    if seat_choice not in seat_list:
        print("잘못된 입력입니다. 다시 시도해주세요.")
    else:
        break

while True:
    row_choice = int(input("예약하실 좌석 행을 입력하세요 (1~10): "))
    if row_choice < 1 or row_choice > 10:
        print("잘못된 입력입니다. 다시 시도해주세요.")
    else:
        break

while True:
    col_choice = int(input("예약하실 좌석 열을 입력하세요 (1~10): "))
    if col_choice < 1 or col_choice > 10:
        print("잘못된 입력입니다. 다시 시도해주세요.")
    else:
        break

# 예약된 좌석 확인
seat_id = f"{row_choice}-{col_choice}"
if seat_id in reserved_seats:
    print("이미 예약된 좌석입니다.")
else:
    # 예약된 좌석 등록
    reserved_seats[seat_id] = {"movie": movie_list[movie_choice-1], "seat_type": seat_choice}

    # 예약 내역 출력
    print("예약이 완료되었습니다.")
    print(f"영화 제목: {movie_list[movie_choice-1]}")
    print(f"좌석 등급: {seat_choice}")
    print(f"좌석 위치: {seat_id}")


# ver1
movies = [
    {"title": "기생충", "time": ["13:00", "15:30", "18:00"]},
    {"title": "조커", "time": ["14:00", "16:30", "19:00"]},
    {"title": "겨울왕국 2", "time": ["13:30", "16:00", "18:30"]}
]

seats = [
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
]

def show_movies():
    for i, movie in enumerate(movies):
        print(f"{i + 1}. {movie['title']}")
    print()
    
def show_seats():
    print("   1  2  3  4  5  6  7  8  9  10")
    for i, row in enumerate(seats):
        print(f"{i + 1}  {'  '.join([str(x) for x in row])}")
    print()
    
def book_seat():
    show_movies()
    movie_choice = int(input("예매할 영화 번호를 선택하세요: "))
    movie = movies[movie_choice - 1]
    show_seats()
    row_choice = int(input("좌석을 선택할 행 번호를 입력하세요: "))
    seat_choice = int(input("좌석을 선택할 열 번호를 입력하세요: "))
    if seats[row_choice - 1][seat_choice - 1] == 1:
        print("이미 예약된 좌석입니다.")
        book_seat()
    else:
        seats[row_choice - 1][seat_choice - 1] = 1
        print(f"예매가 완료되었습니다. {movie['title']} {movie['time'][0]} {row_choice}행 {seat_choice}열")
        print()

book_seat()
'''


