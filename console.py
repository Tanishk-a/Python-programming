employees = []
customers = []
products = []

while True:

    print("\n===== ERP SYSTEM =====")
    print("1. Add Employee")
    print("2. View Employees")
    print("3. Add Customer")
    print("4. View Customers")
    print("5. Add Product")
    print("6. View Products")
    print("7. Exit")

    choice = input("Enter Choice : ")

    if choice == "1":

        name = input("Employee Name : ")
        department = input("Department : ")
        salary = float(input("Salary : "))

        employee = {
            "Name": name,
            "Department": department,
            "Salary": salary
        }

        employees.append(employee)

        print("Employee Added Successfully")

    elif choice == "2":

        print("\nEmployee List")

        for emp in employees:
            print(emp)

    elif choice == "3":

        name = input("Customer Name : ")
        phone = input("Phone : ")

        customer = {
            "Name": name,
            "Phone": phone
        }

        customers.append(customer)

        print("Customer Added Successfully")

    elif choice == "4":

        print("\nCustomer List")

        for customer in customers:
            print(customer)

    elif choice == "5":

        name = input("Product Name : ")
        price = float(input("Price : "))
        quantity = int(input("Quantity : "))

        product = {
            "Name": name,
            "Price": price,
            "Quantity": quantity
        }

        products.append(product)

        print("Product Added Successfully")

    elif choice == "6":

        print("\nProduct List")

        for product in products:
            print(product)

    elif choice == "7":

        print("Thank You")
        break

    else:

        print("Invalid Choice")