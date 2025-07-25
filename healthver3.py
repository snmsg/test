import sys, sqlite3
from datetime import datetime
from collections import defaultdict
import matplotlib.pyplot as plt
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.backends.backend_qt5agg import NavigationToolbar2QT as NavigationToolbar
from matplotlib.figure import Figure
import matplotlib.font_manager as fm
from PyQt5.QtWidgets import QApplication, QMenu, QAction, QCalendarWidget, QMainWindow, QWidget, QVBoxLayout, QTabWidget, QLabel, QPushButton, QGridLayout, QComboBox, QLineEdit, QTableWidget, QTableWidgetItem, QMessageBox, QHBoxLayout, QSizePolicy, QGraphicsScene
from PyQt5.QtGui import QIcon, QPen, QColor, QBrush, QRegExpValidator
from PyQt5.QtCore import Qt, QPoint, QDate, QRegExp



class ExerciseRecordForm(QWidget):
    def __init__(self):
        super().__init__()

        # 입력 위젯 생성
        self.date_edit = QCalendarWidget()
        self.exercise_type_edit = QComboBox()
        self.exercise_type_edit.addItems(['어깨', '가슴', '등', '복근', '팔', '다리', '스쿼트', '러닝', '프랭크'])
        self.reps_edit = QComboBox()
        self.reps_edit.addItems(['15', '20', '25'])
        self.sets_edit = QComboBox()
        self.sets_edit.addItems(['3', '5', '7', '8', '9', '10'])
        self.rest_time_edit = QLineEdit()
        self.exercise_time_edit = QLineEdit()

        # 입력 레이블 생성
        date_label = QLabel('날짜: ')
        exercise_type_label = QLabel('운동 종류: ')
        reps_label = QLabel('횟수: ')
        sets_label = QLabel('세트 수: ')
        rest_time_label = QLabel('휴식 시간(초): ')
        exercise_time_label = QLabel('운동 시간(분): ')
        
        # 추가 버튼 생성
        add_button = QPushButton('추가')
        add_button.clicked.connect(self.add_exercise_record)

        # 레이아웃 생성
        layout = QGridLayout()
        layout.addWidget(date_label, 0, 0)
        layout.addWidget(self.date_edit, 0, 1)
        layout.addWidget(exercise_type_label, 1, 0)
        layout.addWidget(self.exercise_type_edit, 1, 1)
        layout.addWidget(reps_label, 2, 0)
        layout.addWidget(self.reps_edit, 2, 1)
        layout.addWidget(sets_label, 3, 0)
        layout.addWidget(self.sets_edit, 3, 1)
        layout.addWidget(rest_time_label, 4, 0)
        layout.addWidget(self.rest_time_edit, 4, 1)
        layout.addWidget(exercise_time_label, 5, 0)
        layout.addWidget(self.exercise_time_edit, 5, 1)
        layout.addWidget(add_button, 6, 1)
        self.setLayout(layout)


    def add_exercise_record(self):
        
        # 입력값 가져오기
        date = self.date_edit.selectedDate().toString('yyyy-MM-dd')
        exercise_type = self.exercise_type_edit.currentText()
        reps = self.reps_edit.currentText()
        sets = self.sets_edit.currentText()
        rest_time = self.rest_time_edit.text()
        exercise_time = self.exercise_time_edit.text()

        # SQLite DB에 운동 기록 추가
        conn = sqlite3.connect('exercise_records.db')
        c = conn.cursor()
        c.execute('CREATE TABLE IF NOT EXISTS exercise_records (date TEXT, exercise_type TEXT, reps INTEGER, sets INTEGER, rest_time INTEGER, exercise_time INTEGER)')
        c.execute('INSERT INTO exercise_records VALUES (?, ?, ?, ?, ?, ?)', (date, exercise_type, reps, sets, rest_time, exercise_time))
        conn.commit()
        QMessageBox.information(self, '성공', '운동 기록이 추가되었습니다.')

        # 입력값 초기화
        self.date_edit.setSelectedDate(QDate.currentDate())
        self.exercise_type_edit.setCurrentIndex(0)
        self.reps_edit.setCurrentIndex(0)
        self.sets_edit.setCurrentIndex(0)
        self.rest_time_edit.clear()
        self.exercise_time_edit.clear()



class ExerciseViewForm(QWidget):
    def __init__(self):
        super().__init__()

        # 테이블 위젯 생성
        self.table = QTableWidget()
        self.table.setColumnCount(6)
        self.table.setHorizontalHeaderLabels(['날짜', '운동 종류', '횟수', '세트 수', '휴식 시간', '운동 시간'])
        self.load_data()

        # 레이아웃 생성
        layout = QVBoxLayout()
        layout.addWidget(self.table)
        self.setLayout(layout)

        # context menu 생성
        self.context_menu = QMenu(self)
        delete_action = QAction("삭제", self)
        delete_action.triggered.connect(self.delete_record)
        self.context_menu.addAction(delete_action)

        # context menu를 테이블 위젯에 연결
        self.table.setContextMenuPolicy(Qt.CustomContextMenu)
        self.table.customContextMenuRequested.connect(self.show_context_menu)


    def load_data(self):
        # SQLite DB에서 운동 기록 가져오기
        conn = sqlite3.connect('exercise_records.db')
        c = conn.cursor()
        c.execute('CREATE TABLE IF NOT EXISTS exercise_records (date TEXT, exercise_type TEXT, reps INTEGER, sets INTEGER, rest_time INTEGER, exercise_time INTEGER)')
        rows = c.execute('SELECT * FROM exercise_records ORDER BY date').fetchall()

        # 테이블 위젯에 데이터 추가
        self.table.setRowCount(len(rows))
        for i, row in enumerate(rows):
            for j, item in enumerate(row):
                self.table.setItem(i, j, QTableWidgetItem(str(item)))


    def show_context_menu(self, pos):
        # 마우스 오른쪽 버튼 클릭 위치에 context menu를 표시
        self.context_menu.exec_(self.table.mapToGlobal(pos))


    def delete_record(self):
        # 선택된 행 삭제
        row = None  # 변수 초기화
        for index in self.table.selectedIndexes():
            row = index.row()
            self.table.removeRow(row)

            # SQLite DB에서도 삭제
            conn = sqlite3.connect('exercise_records.db')
            c = conn.cursor()
            c.execute('CREATE TABLE IF NOT EXISTS exercise_records (date TEXT, exercise_type TEXT, reps INTEGER, sets INTEGER, rest_time INTEGER, exercise_time INTEGER)')

            # 선택된 행의 날짜를 가져와서 DB에서 해당 기록 삭제
            selected_date = self.table.item(row, 0).text()
            c.execute('DELETE FROM exercise_records WHERE date=?', (selected_date,))
            conn.commit()
            QMessageBox.information(self, '성공', '운동 기록이 삭제되었습니다.')



class ExerciseAnalysisForm(QWidget):
    def __init__(self):
        super().__init__()

        # 요일별 운동 빈도수 분석 레이블 생성
        self.weekday_frequency_label = QLabel('요일별 총 출석 일수')

        # 요일별 운동 빈도수 테이블 위젯 생성
        self.weekday_frequency_table = QTableWidget()
        self.weekday_frequency_table.setColumnCount(2)
        self.weekday_frequency_table.setHorizontalHeaderLabels(['요일', '총 출석 일수'])

        # 레이아웃 생성
        layout = QVBoxLayout()
        layout.addWidget(self.weekday_frequency_label)
        layout.addWidget(self.weekday_frequency_table)
        self.setLayout(layout)
       
        # FigureCanvas 생성
        self.figure = Figure(figsize=(5, 4), dpi=100)
        self.canvas = FigureCanvas(self.figure)
        layout.addWidget(self.canvas)

        # NavigationToolbar 생성
        self.toolbar = NavigationToolbar(self.canvas, self)
        layout.addWidget(self.toolbar)

        # 그래프 업데이트
        self.canvas.draw()

        # 데이터 로드
        self.load_data()


    def load_data(self):
        # SQLite DB에서 운동 기록 가져오기
        conn = sqlite3.connect('exercise_records.db')
        c = conn.cursor()
        rows = c.execute('SELECT date FROM exercise_records').fetchall()

        # 요일별 출석 일수 계산
        weekday_frequency = defaultdict(int)
        for row in rows:
            weekday = self.get_weekday(row[0])
            weekday_frequency[weekday] += 1

        # 테이블 위젯에 요일별 출석 일수 추가
        self.weekday_frequency_table.setRowCount(len(weekday_frequency))
        for i, (weekday, frequency) in enumerate(sorted(weekday_frequency.items(), key=lambda x: x[0])):
            self.weekday_frequency_table.setItem(i, 0, QTableWidgetItem(weekday))
            self.weekday_frequency_table.setItem(i, 1, QTableWidgetItem(str(frequency)))

        # 요일별 출석일 그래프 생성
        weekdays = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']
        counts = [weekday_frequency[weekday] for weekday in weekdays]
        ax = self.figure.add_subplot(111)
        ax.bar(weekdays, counts)
        ax.set_title('출석한 요일 수')
        ax.set_xlabel('요일')
        ax.set_ylabel('출석한 일 수')


    def get_weekday(self, date_str):
        # 날짜 문자열을 년, 월, 일로 분리
        year, month, day = map(int, date_str.split('-'))
        # datetime 모듈을 이용하여 요일 계산
        import datetime
        weekday = datetime.datetime(year, month, day).strftime("%A")
        return weekday



class ExerciseAnalysisWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle('운동 기록 분석')
        self.setGeometry(100, 100, 600, 500)

        # 운동 분석 폼 생성
        self.exercise_analysis_form = ExerciseAnalysisForm()
        self.setCentralWidget(self.exercise_analysis_form)



class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        # 메인 윈도우 설정
        self.setWindowTitle('운동 기록 프로그램')
        self.setWindowIcon(QIcon('icon.png'))
        self.setGeometry(100, 100, 800, 600)

        # 탭 위젯 생성
        tab_widget = QTabWidget()

        # 운동 기록 탭 생성
        record_tab = QWidget()
        record_layout = QVBoxLayout()
        record_layout.addWidget(ExerciseRecordForm())
        record_tab.setLayout(record_layout)
        tab_widget.addTab(record_tab, '기록')

        # 운동 기록 보기 탭 생성
        view_tab = QWidget()
        view_layout = QVBoxLayout()
        view_layout.addWidget(ExerciseViewForm())
        view_tab.setLayout(view_layout)
        tab_widget.addTab(view_tab, '보기')

        # 운동 기록 분석 탭 생성
        analysis_tab = QWidget()
        analysis_layout = QVBoxLayout()
        analysis_layout.addWidget(ExerciseAnalysisForm())
        analysis_tab.setLayout(analysis_layout)
        tab_widget.addTab(analysis_tab, '분석')

        self.setCentralWidget(tab_widget)



if __name__ == '__main__':
    app = QApplication(sys.argv)
    main_window = MainWindow()
    main_window.show()
    sys.exit(app.exec_())




