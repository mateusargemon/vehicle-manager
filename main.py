import json
import os
import re
import secrets
import string

# Define o caminho do arquivo JSON na mesma pasta onde este script está salvo
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
GARAGE_FILE = os.path.join(BASE_DIR, "data", "garage.json")

try: # se o arquivo existir, abre e carrega o conteúdo
    with open(GARAGE_FILE, "r") as archive:
        garage = json.load(archive)
    if type(garage) != list: # garante que a estrutura seja uma lista
        garage = []
        with open(GARAGE_FILE, "w") as archive:
            json.dump(garage, archive, indent=4)

except FileNotFoundError: # cria o arquivo se não existir
    garage = []
    with open(GARAGE_FILE, "w") as archive:
        json.dump(garage, archive, indent=4)

except json.JSONDecodeError: # trata arquivo vazio ou inválido
    garage = []
    with open(GARAGE_FILE, "w") as archive:
        json.dump(garage, archive, indent=4)

def askColor():
    while True:
        color = input("Insert the color: ").strip()
        if color.isalpha() and color != "":
            return color
        else:
            print("That's not a valid color! Try again.\n")
    
def addCar():
    print("===== Vehicle Registration =====\n")
    plate = newPlate()
    print(f"The plate for this vehicle is {plate}\n\n")
    print('If you want to leave, digit "1"\n\n')
    brand = input("Insert the brand of the vehicle: ")
    if brand == "1":
        print("You chose to leave.\n")
        return
    
    car = {
        "plate": plate,
        "brand": brand,
        "model": input("Insert the model: "),
        "color": askColor(),
        "year": int(input("Insert the year model: ")),
        "price": float(input("Insert the price: "))
    }
    
    garage.append(car)
    print(f"\nThe vehicle {car['model']} has registered successfully!\n")
    saveGarage()

def newPlate():
    while True:
        plate = ""
        for i in range(3):
            plate += secrets.choice(string.ascii_uppercase)
        plate += str(secrets.randbelow(10))
        plate += secrets.choice(string.ascii_uppercase)
        for i in range(2):
            plate += str(secrets.randbelow(10))
            
        plateExist = False
        for car in garage:
            if car["plate"] == plate:
                plateExist = True
                break
        if not plateExist:
            return plate
        
def saveGarage():
    with open(GARAGE_FILE, "w") as archive:
        json.dump(garage, archive, indent=4) 

def modifyCar():
    print("===== Vehicle Information Update =====\n")
    print('If you want to leave, digit "1"\n')
    
    carFound = False
    car = None
    while not carFound:
        plateSearch = input("Insert the license plate of the vehicle: ").upper().strip()
        if plateSearch == "1":
            print("You chose to leave.\n")
            return
        if not re.fullmatch(r"[A-Z]{3}[0-9][A-Z][0-9]{2}", plateSearch):
            print("Insert a valid license plate.\n")
            continue
        for item in garage:
            if item["plate"] == plateSearch:
                car = item
                carFound = True
                break
        if not carFound:
            print("Vehicle not found.\n")
                
    while True:
        print("\n===== Update Options =====\n")
        print(
            f'Plate: {car["plate"]}\n'
            f'Brand: {car["brand"]}\n'
            f'Model: {car["model"]}\n'
            f'Color: {car["color"]}\n'
            f'Year: {car["year"]}\n'
            f'Price: {car["price"]}\n'
        )
        modifyingCar = input(
            "What would you update?\n\n"
            "1. Plate\n"
            "2. Color\n"
            "3. Price\n"
            "4. Exit\n"
            "5. Change the vehicle\n"
            "Select an option: "
        )
       
        print()
        if modifyingCar == "1":
            modifyingPlate = input("Insert the new plate: ").upper().strip()
            if re.fullmatch(r"[A-Z]{3}[0-9][A-Z][0-9]{2}", modifyingPlate):
                print("The plate is valid.\n")
                car["plate"] = modifyingPlate
                saveGarage()
                print("The plate has been changed succesfully!\n") 
                break
            else:
                print("The plate inserted is invalid! Try again.")

        elif modifyingCar == "2":
            modifyingColor = askColor()
            car["color"] = modifyingColor
            saveGarage()
            print("The color has been changed succesfully!\n") 
            break
    
        elif modifyingCar == "3":
            try:
                modifyingPrice = float(input("Insert the new price: ").strip())
                if modifyingPrice > 0:
                    print("The price is valid.\n")
                    car["price"] = modifyingPrice
                    saveGarage()
                    print("The price has been changed succesfully!\n")
                    break
                else:
                    print("That's an invalid price! Try again.")
            except ValueError:
                print("That's an invalid price! Try again.")

        elif modifyingCar == "4":
            print("You preferred to leave.")
            return
        elif modifyingCar == "5":
            print("You chose 'update another vehicle'.\n")
            modifyCar()
            break
        else:
            print("That is not a valid option! Try again.")

def deleteCar():
    print("===== Vehicle Deletion =====\n")
    print('If you want to leave, digit "1"\n')
    carFound = False
    car = None
    while not carFound:
        plateSearch = input("Insert the license plate of the vehicle: ").upper().strip()
        if plateSearch == "1":
            print("You chose to leave.\n")
            return
        if not re.fullmatch(r"[A-Z]{3}[0-9][A-Z][0-9]{2}", plateSearch):
            print("Insert a valid license plate.\n")
            continue
        for item in garage:
            if item["plate"] == plateSearch:
                car = item
                carFound = True
                break
        if not carFound:
            print("Vehicle not found.\n")

    while True:
        print("\n===== Deletion Options =====\n")
        print(
            f'Plate: {car["plate"]}\n'
            f'Brand: {car["brand"]}\n'
            f'Model: {car["model"]}\n'
            f'Color: {car["color"]}\n'
            f'Year: {car["year"]}\n'
            f'Price: {car["price"]}\n'
        )
        option = input(
            "Are you sure you want to delete this vehicle?\n"
            "1. Yes\n"
            "2. No, exit\n"
            "Select an option: "
        )

        if option == "1":
            print("\nYou chose to delete it.")
            garage.remove(car)
            print("Vehicle has deleted successfully!\n")
            saveGarage()
            break
        elif option == "2":
            print("\nYou chose to leave.")
            break
        else:
            print("Select a valid option.")

def viewCars():
    print("===== Registered Vehicles =====\n")
    carFound = False
    car = None
    for item in garage:
        print(f'Model: {item["model"]}\n'
              f'Year: {item["year"]}\n'
              f'Plate: {item["plate"]}\n')
    
    while not carFound:
        print('If you want to leave, digit "1"\n')
        plateSearch = input("Insert the license plate of the vehicle to look closely: ").upper().strip()
        if plateSearch == "1":
            return
        if not re.fullmatch(r"[A-Z]{3}[0-9][A-Z][0-9]{2}", plateSearch):
            print("\nInsert a valid license plate.\n")
            continue
        for item in garage:
            if item["plate"] == plateSearch:
                car = item
                carFound = True
                break
        if not carFound:
            print("Vehicle not found.\n")
    
    print("\n===== Vehicle Information =====\n")
    print(
        f'Plate: {car["plate"]}\n'
        f'Brand: {car["brand"]}\n'
        f'Model: {car["model"]}\n'
        f'Color: {car["color"]}\n'
        f'Year: {car["year"]}\n'
        f'Price: {car["price"]}\n'
    )

    while True:
        option = input("1. Update vehicle information\n"
                       "2. Delete the vehicle record\n"
                       "3. Exit\n"
                       "Select an option: ")
        if option == "1":
            print()
            modifyCar()
            break
        elif option == "2":
            print()
            deleteCar()
            break
        elif option == "3":
            print("You chose to leave.\n")
            return
        else:
            print("\nSelect a valid option.")

def menuCar():
    while True:
        print("===== Garage Management System =====\n")

        option = input(
            "1. View registered vehicles\n"
            "2. Register a new vehicle\n"
            "3. Update vehicle information\n"
            "4. Delete a vehicle record\n"
            "5. Exit\n\n"
            "Select an option: "
        )
        print()
        
        if option == "1":
            viewCars()
        elif option == "2":
            addCar()
        elif option == "3":
            modifyCar()
        elif option == "4":
            deleteCar()
        elif option == "5":
            print("You chose to leave.")
            return
        else:
            print("Invalid option.\n")

menuCar()
