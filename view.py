from django.shortcuts import render
from django.apps import apps

# Use apps.get_model to avoid import-time resolution issues in some editors/environments
Employee = apps.get_model('employees', 'Employee')
Customer = apps.get_model('customers', 'Customer')
Product = apps.get_model('products', 'Product')
Supplier = apps.get_model('suppliers', 'Supplier')
Sale = apps.get_model('sales', 'Sale')
Payment = apps.get_model('payments', 'Payment')

def dashboard(request):

    employee_count = Employee.objects.count()
    customer_count = Customer.objects.count()
    product_count = Product.objects.count()
    supplier_count = Supplier.objects.count()
    sales_count = Sale.objects.count()

    total_revenue = 0

    for sale in Sale.objects.all():
        total_revenue += sale.total

    total_payment = 0

    for payment in Payment.objects.all():
        total_payment += payment.amount

    context = {
        "employee_count": employee_count,
        "customer_count": customer_count,
        "product_count": product_count,
        "supplier_count": supplier_count,
        "sales_count": sales_count,
        "total_revenue": total_revenue,
        "total_payment": total_payment,
    }

    return render(request, "dashboard/index.html", context)