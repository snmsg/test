import sqlite3
import datetime

# Create a connection to the SQLite database
conn = sqlite3.connect("vehicle_management5.db")
c = conn.cursor()

# Create the table if it doesn't exist
c.execute("CREATE TABLE IF NOT EXISTS repairs (license_plate TEXT, repair_date TEXT, description TEXT, cost REAL, repair_history TEXT, part_replacement_history TEXT)")
c.execute("CREATE TABLE IF NOT EXISTS part_replacements (license_plate TEXT, repair_date TEXT, part_name TEXT, cost REAL, repair_history TEXT, part_replacement_history TEXT)")

class Vehicle:
    def __init__(self, license_plate):
        self.license_plate = license_plate       

    def add_repair(self, date, description, cost):
        # Connect to the database
        conn = sqlite3.connect("vehicle_management5.db")
        c = conn.cursor()
        # Insert the repair into the repairs table
        c.execute("INSERT INTO repairs (license_plate, repair_date, description, cost) VALUES (?, ?, ?, ?)",
                (self.license_plate, date, description, cost))
        # Commit the changes and close the connection
        conn.commit()
        conn.close()

    def add_part_replacement(self, date, part_name, cost):   
        # Connect to the database
        conn = sqlite3.connect("vehicle_management5.db")
        c = conn.cursor()
        # Insert the repair into the repairs table
        c.execute("INSERT INTO part_replacements (license_plate, repair_date, part_name, cost) VALUES (?, ?, ?, ?)",
                (self.license_plate, date, part_name, cost))       
        # Commit the changes and close the connection
        conn.commit()
        conn.close()

    def delete_repair(self, index):
        # Connect to the database
        conn = sqlite3.connect("vehicle_management5.db")
        c = conn.cursor()
        # Retrieve the rowids of part replacements for the vehicle
        c.execute("SELECT rowid FROM repairs WHERE license_plate = ?", (self.license_plate,))
        rows = c.fetchall()
        if index < len(rows):
            rowid = rows[index][0]
            c.execute("DELETE FROM repairs WHERE rowid = ?", (rowid,))
            conn.commit()
        else:
            print("유효하지 않은 인덱스입니다.")
        # Close the connection
        conn.close()

    def delete_part_replacement(self, index):
        # Connect to the database
        conn = sqlite3.connect("vehicle_management5.db")
        c = conn.cursor()
        # Retrieve the rowids of part replacements for the vehicle
        c.execute("SELECT rowid FROM part_replacements WHERE license_plate = ?", (self.license_plate,))
        rows = c.fetchall()
        if index < len(rows):
            rowid = rows[index][0]
            c.execute("DELETE FROM part_replacements WHERE rowid = ?", (rowid,))
            conn.commit()
        else:
            print("유효하지 않은 인덱스입니다.")
        # Close the connection
        conn.close()

    def update_repair(self, index, date, description, cost):
        # Connect to the database
        conn = sqlite3.connect("vehicle_management5.db")
        c = conn.cursor()
        # Retrieve the rowids of repairs for the vehicle
        c.execute("SELECT rowid FROM repairs WHERE license_plate = ?", (self.license_plate,))
        rows = c.fetchall()
        if index < len(rows):
            rowid = rows[index][0]
            # Update the repair entry
            c.execute("UPDATE repairs SET repair_date = ?, description = ?, cost = ? WHERE rowid = ?",
                      (date, description, cost, rowid))
            conn.commit()
            print("수리 내역이 수정되었습니다.")
        else:
            print("유효하지 않은 인덱스입니다.")
        # Close the connection
        conn.close()

    def update_part_replacement(self, index, date, part_name, cost):
        # Connect to the database
        conn = sqlite3.connect("vehicle_management5.db")
        c = conn.cursor()
        # Retrieve the rowids of part replacements for the vehicle
        c.execute("SELECT rowid FROM part_replacements WHERE license_plate = ?", (self.license_plate,))
        rows = c.fetchall()
        if index < len(rows):
            rowid = rows[index][0]
            # Update the part replacement entry
            c.execute("UPDATE part_replacements SET repair_date = ?, part_name = ?, cost = ? WHERE rowid = ?",
                      (date, part_name, cost, rowid))
            conn.commit()
            print("소모품 교체 기록이 수정되었습니다.")
        else:
            print("유효하지 않은 인덱스입니다.")
        # Close the connection
        conn.close()

    def print_maintenance_history(self):
        print("수리 내역:")
        total_repair_cost = 0
        c.execute("SELECT rowid, repair_date, description, cost FROM repairs WHERE license_plate = ?", (self.license_plate,))
        repairs = c.fetchall()
        for index, row in enumerate(repairs, 1):
            rowid, date, description, cost = row
            print("[{}] 번호: {}, 날짜: {}, 내용: {}, 비용: {}원".format(index-1, rowid, date, description, cost))
            total_repair_cost += cost
        print("총 수리 비용: {}원".format(total_repair_cost))

        print("\n소모품 교체 기록:")
        total_replacement_cost = 0
        c.execute("SELECT rowid, repair_date, part_name, cost FROM part_replacements WHERE license_plate = ?", (self.license_plate,))
        replacements = c.fetchall()
        for index, row in enumerate(replacements, 1):
            rowid, date, part_name, cost = row
            print("[{}] 번호: {}, 날짜: {}, 부품명: {}, 비용: {}원".format(index-1, rowid, date, part_name, cost))
            total_replacement_cost += cost
        print("총 교체 비용: {}원".format(total_replacement_cost))

        print("\n총 비용: {}원".format(total_repair_cost + total_replacement_cost))



# 유효성 검사 번호판, 날짜, 비용 등

def validate_license_plate(license_plate):
    # Check if the license plate has the correct format
    if len(license_plate) != 7:
        return False    
    if not license_plate[2].isalpha():
        return False    
    for i in range(3, 7):
        if not license_plate[i].isdigit():
            return False    
    return True

def validate_date(date):
    # Add your date validation logic here
    # Example: Check if the date has the correct format (YYYYMMDD)
    try:
        datetime.datetime.strptime(date, '%Y%m%d')
        return True
    except ValueError:
        return False

def validate_cost(cost):
    # Add your cost validation logic here
    # Example: Check if the cost is a positive number
    try:
        cost = float(cost)
        if cost >= 0:
            return True
        else:
            return False
    except ValueError:
        return False



def main():
    while True:
        license_plate = input("차량의 등록 번호를 입력하세요: ")
        if validate_license_plate(license_plate):
            break
        else:
            print("유효하지 않은 차량 등록 번호입니다. 다시 입력해주세요.")
    vehicle = Vehicle(license_plate)   
    # Rest of the code remains the same
    license_plate = input("차량의 등록 번호를 입력하세요: ")
    vehicle = Vehicle(license_plate)

    while True:
        print("\n차량 관리 프로그램")
        print("1. 수리 내역 추가")
        print("2. 소모품 교체 추가")
        print("3. 수리 및 교체 조회")
        print("4. 삭제")
        print("5. 차 교체")
        print("6. 종료")
        choice = input("메뉴를 선택하세요: ")

        if choice == "1":
            while True:
                date = input("수리 일자를 입력하세요 (YYYYMMDD): ")
                if validate_date(date):
                    break
                else:
                    print("유효하지 않은 날짜 형식입니다. 다시 입력해주세요.")
            description = input("수리 내용을 입력하세요: ")
            while True:
                cost = input("비용을 입력하세요: ")
                if validate_cost(cost):
                    cost = float(cost)
                    break
                else:
                    print("유효하지 않은 비용 형식입니다. 숫자로만 입력해주세요.")
            vehicle.add_repair(date, description, cost)
            print("수리 내역이 추가되었습니다.")

        elif choice == "2":
            date = input("교체 일자를 입력하세요 (YYYYMMDD): ")
            part_name = input("교체한 부품명을 입력하세요: ")
            while True:
                cost = input("비용을 입력하세요: ")
                if validate_cost(cost):
                    cost = float(cost)
                    break
                else:
                    print("유효하지 않은 비용 형식입니다. 숫자로만 입력해주세요.")
            vehicle.add_part_replacement(date, part_name, cost)
            print("소모품 교체 기록이 추가되었습니다.")

        elif choice == "3":
            vehicle.print_maintenance_history()

        elif choice == "4":
            vehicle.print_maintenance_history()
            deletion_choice = input("삭제할 항목의 번호를 입력하세요 (수리: 1, 교체: 2, 수정: 3, 뒤로 가기: 4): ")
            if  deletion_choice == "1":
                # Connect to the database
                conn = sqlite3.connect("vehicle_management5.db")
                c = conn.cursor()
                # Check if there are any repair entries for the vehicle
                c.execute("SELECT rowid FROM repairs WHERE license_plate = ?", (vehicle.license_plate,))
                rows = c.fetchall()
                if not rows:
                     # Close the connection
                    conn.close()
                    print("삭제할 수리 항목이 없습니다.")
                else:
                    num_repairs = len(rows)
                    print(f"수리 항목의 개수: {num_repairs}")
                    repair_index = int(input("삭제할 수리 항목의 번호를 입력하세요: "))
                    vehicle.delete_repair(repair_index)
                    print("수리 내역이 삭제되었습니다.")
            elif deletion_choice == "2":
                # Connect to the database
                conn = sqlite3.connect("vehicle_management5.db")
                c = conn.cursor()
                # Check if there are any repair entries for the vehicle
                c.execute("SELECT rowid FROM part_replacements WHERE license_plate = ?", (vehicle.license_plate,))
                rows = c.fetchall()
                if not rows:
                     # Close the connection
                    conn.close()
                    print("삭제할 소모품 교체 항목이 없습니다.")
                else:
                    num_repairs = len(rows)
                    print(f"수리 항목의 개수: {num_repairs}")
                    replacement_index = int(input("삭제할 소모품 교체 항목의 번호를 입력하세요: "))
                    vehicle.delete_part_replacement(replacement_index)
                    print("소모품 교체 기록이 삭제되었습니다.")
            elif deletion_choice == "3":
                update_choice = input("수정할 항목의 종류를 선택하세요 (수리: 1, 교체: 2, 뒤로 가기: 3): ")
                if update_choice == "1":
                    vehicle.print_maintenance_history()
                    repair_index = int(input("수정할 수리 항목의 번호를 입력하세요: "))
                    date = input("새로운 수리 일자를 입력하세요 (YYYYMMDD): ")
                    description = input("새로운 수리 내용을 입력하세요: ")
                    while True:
                        cost = input("새로운 비용을 입력하세요: ")
                        if validate_cost(cost):
                            cost = float(cost)
                            break
                        else:
                            print("유효하지 않은 비용 형식입니다. 숫자로만 입력해주세요.")
                    vehicle.update_repair(repair_index, date, description, cost)
                elif update_choice == "2":
                    vehicle.print_maintenance_history()
                    replacement_index = int(input("수정할 소모품 교체 항목의 번호를 입력하세요: "))
                    date = input("새로운 교체 일자를 입력하세요 (YYYYMMDD): ")
                    part_name = input("새로운 교체한 부품명을 입력하세요: ")
                    while True:
                        cost = input("새로운 비용을 입력하세요: ")
                        if validate_cost(cost):
                            cost = float(cost)
                            break
                        else:
                            print("유효하지 않은 비용 형식입니다. 숫자로만 입력해주세요.")
                    vehicle.update_part_replacement(replacement_index, date, part_name, cost)
                elif update_choice == "3":
                    continue
                else:
                    print("유효하지 않은 선택입니다.")
            elif deletion_choice == "4":
                continue
            else:
                print("유효하지 않은 선택입니다.")        

        elif choice == "5":
            license_plate = input("새로운 차량의 등록 번호를 입력하세요: ")
            if validate_license_plate(license_plate):
                vehicle = Vehicle(license_plate)  # Switch to a new vehicle
                print("차량이 변경되었습니다.")
            else:
                print("유효하지 않은 차량 등록 번호입니다.")

        elif choice == "6":
            break
 
        else:
            print("유효하지 않은 선택입니다. 다시 선택해주세요.")
            
if __name__ == '__main__':
    main()
