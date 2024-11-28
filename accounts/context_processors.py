from .models import MenuItem

def menu_items(request):
    # Отримуємо всі пункти меню з бази і сортуємо за полем order
    menu_items = MenuItem.objects.all().order_by('order')
    return {'menu_items': menu_items}
