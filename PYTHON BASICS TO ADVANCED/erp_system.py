from fastapi import FastAPI
from pydantic import BaseModel

app = FastAPI(
    title="ERP System",
    version="1.0.0",
    description="Simple ERP System using FastAPI"
)

# Store data temporarily (for learning)
employees = []

# Employee Model
class Employee(BaseModel):
    id: int
    name: str
    department: str
    salary: float

# Home Page
@app.get("/")
def home():
    return {
        "message": "Welcome to ERP System",
        "status": "Running Successfully"
    }

# Add Employee
@app.post("/employee")
def add_employee(employee: Employee):
    employees.append(employee)
    return {
        "message": "Employee Added Successfully",
        "employee": employee
    }

# View All Employees
@app.get("/employees")
def get_employees():
    return employees

# Get Employee by ID
@app.get("/employee/{emp_id}")
def get_employee(emp_id: int):
    for employee in employees:
        if employee.id == emp_id:
            return employee
    return {"message": "Employee Not Found"}

# Update Employee
@app.put("/employee/{emp_id}")
def update_employee(emp_id: int, updated_employee: Employee):
    for index, employee in enumerate(employees):
        if employee.id == emp_id:
            employees[index] = updated_employee
            return {
                "message": "Employee Updated Successfully",
                "employee": updated_employee
            }
    return {"message": "Employee Not Found"}

# Delete Employee
@app.delete("/employee/{emp_id}")
def delete_employee(emp_id: int):
    for employee in employees:
        if employee.id == emp_id:
            employees.remove(employee)
            return {"message": "Employee Deleted Successfully"}
    return {"message": "Employee Not Found"}