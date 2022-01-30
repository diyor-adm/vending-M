def read_file(filename: str) -> list:
    import csv
    csv_list = []
    with open(f'{filename}', 'r') as file:
        csv_file = csv.DictReader(file, delimiter=';')
        for i in csv_file:
            csv_list.append(i)
    return csv_list


def write_file(fields: list, mydict: list, filename: str): 
    import csv
    with open(filename, 'w') as csvfile: 
    # creating a csv dict writer object 
        writer = csv.DictWriter(csvfile, fieldnames = fields, delimiter=';') 
    # writing headers (field names) 
        writer.writeheader() 
    # writing data rows 
        writer.writerows(mydict) 


def check_banknote_bool(banknote: int)-> bool:
    if banknote == 5000 or banknote == 10000 or banknote == 20000 or banknote == 50000:
        return True
    else:
        return False


balance = {
    5000:0, 10000:0,
    20000:0, 50000:0 }


sell_price = 0


def print_balace(money):
    balance[money] = balance[money] + 1
    
    sum = 0
    for i in balance:
        if balance[i]!= 0:
            print( f'You entered {balance[i]} banknote of {i} UZS')
    sum = calc_balance()
    print(f'Your balance {sum} UZS')
    
    
def calc_balance() -> int:
    sum = 0
    for i in balance:
        sum += i*balance[i]
    return sum-sell_price


def my_balance():
    flag, a = all_chacker()
    if flag:
        my_bln = calc_balance()
        print(f'Your balance: {my_bln} UZS')


def input_money() -> int:
    while True:
        try:
            money = int(input('Enter money: '))
            return money
        except:
            print('Please just enter money')


def options() -> int:
    print('\nSelect an action:\n1 - Insert a banknote\n2 - Show available products\n3 - Select a product\n4 - My balance\n5 - Get the change')
    while True:
        try:
            value = int(input('Your choice: '))
            print('')
            if 0< value < 6 or value == 12345:
                return value
            else:
                print('Please select a section in the menu!')
        except:
            print('Please select a section in the menu!')


def add_cash(money):
    banknote_list = read_file('banknotes.csv')
    for banknote in banknote_list:
        if banknote['banknote']==str(money):
            banknote['numberOf'] = int(banknote['numberOf'])+1 
    write_file(['banknote','numberOf'], banknote_list, 'banknotes.csv')


def insert_a_banknote():
    flag,a = all_chacker()
    if flag:
        while True:
            money = input_money()
            value_bool = check_banknote_bool(money)
            if value_bool:
                print_balace(money)
                add_cash(money)
                break
            else:
                print('You can only enter 5 000 UZS, 10 000 UZS, 20 000 UZS, 50 000 UZS banknotes')


def check_quantity(product_list, quantity):
    new_list = []
    for product in product_list:
        if int(product[quantity])>0:
            new_list.append(product)
    return new_list


def all_chacker():
    product_list = read_file('product.csv')
    product_list = check_quantity(product_list,'quantity')
    coin_list = read_file('coins.csv')
    coin_list = check_quantity(coin_list,'numberOf')
    if len(product_list)>0 and len(coin_list)>0:
        return True, product_list
    return False, 0


def print_all_product():
    flag,product_list = all_chacker()
    if flag:
        for num, product in enumerate(product_list,1):
            name = product['name']
            price = product['price']
            print(f'{num}. {name} is {price} UZS')



def find_enough_money_pr(all_product_list) -> list:
    user_balance = calc_balance()
    product_list = []
    for product in all_product_list:
        price = int(product['price'])
        if price<= user_balance:
            product_list.append(product)
    if len(product_list) == 0:
        print('Your money is not enough for the products we have. Please make enough money!')
    else:
        return product_list


def select_product(product_list):
    while True:
        try:
            option = int(input('Select product: '))
            if 0<option<=len(product_list):
                value = minus_balance(product_list[option-1])
                break
        except:
            print('Please select a product in the menu!')


def minus_balance(product):
    user_balance = calc_balance()
    narx = product['price']
    global sell_price
    sell_price += int(narx)
    product['quantity'] = int(product['quantity']) - 1
    all_product = read_file('product.csv')
    for i in all_product:
        if i['name']==product['name']:
            i['quantity'] = int(i['quantity']) - 1
    all_product = sorted(all_product, key=lambda prod: int(prod['quantity']), reverse=True)
    write_file(['name','price','quantity'],all_product,'product.csv')
    print(f'{narx} UZS have been deducted from your account')
    print(f'Your balace: {calc_balance()} UZS')


def sell_product():
    flag,product_list = all_chacker()
    if flag:
        try:
            product_list = find_enough_money_pr(product_list)
            product_list = sorted(product_list, key=lambda product: int(product['quantity']), reverse=True)
            for num, product in enumerate(product_list,1):
                name = product['name']
                price = product['price']
                print(f'{num}. {name} is {price} UZS')
            select_product(product_list)
        except:
            pass


def write_coin_file(get_coin):
    all_coins = read_file('coins.csv')
    for row in range(4):
        for i in get_coin:
            if all_coins[row]['coin'] == str(i):
                all_coins[row]['numberOf']= int(all_coins[row]['numberOf'])-get_coin[i]
    write_file(['coin','numberOf'], all_coins, 'coins.csv')


def get_change():
    get_coin = {
        1000:0, 500:0,
        200:0, 100:0 }
    balan = calc_balance()
    all_coins = read_file('coins.csv')
    while balan>0:
        if balan>=1000 and int(all_coins[0]['numberOf'])>0:
            balan -= 1000
            get_coin[1000]+=1
            all_coins[0]['numberOf']= int(all_coins[0]['numberOf'])-1

        elif balan>=500 and int(all_coins[1]['numberOf'])>0:
            balan -= 500
            get_coin[500]+=1
            all_coins[1]['numberOf']= int(all_coins[1]['numberOf'])-1
        elif balan>=200 and int(all_coins[2]['numberOf'])>0:
            balan -= 200
            get_coin[200]+=1
            all_coins[2]['numberOf']= int(all_coins[2]['numberOf'])-1
        else:
            balan-=100
            get_coin[100]+=1

    print_get_change(get_coin)
    write_coin_file(get_coin)


def print_get_change(get_coin):
    get_change_sum = 0
    for coin in get_coin:
        if get_coin[coin]>0:
            print(f'You were refunded {get_coin[coin]} UZS {coin} ')
            get_change_sum += get_coin[coin]*coin
    for i in balance:
        balance[i]=0
    global sell_price
    sell_price = 0
    print(f'Get changed: {get_change_sum} UZS')


def max_coin():
    all_coins = read_file('coins.csv')
    for i in range(4):
        all_coins[i]['numberOf'] = 400
    write_file(['coin','numberOf'], all_coins, 'coins.csv')
    print('The quantity of all coins has been maximized\n')


def clean_banknotes():
    banknotes_list = read_file('banknotes.csv')
    for i in range(4):
        banknotes_list[i]['numberOf'] = 0
    write_file(['banknote','numberOf'], banknotes_list, 'banknotes.csv')
    print('<<< All the money was taken! >>>\n')


def max_product():
    all_products = read_file('product.csv')
    for i in range(10):
        all_products[i]['quantity'] = 15
    write_file(['name','price','quantity'], all_products, 'product.csv')
    print('The quantity of all products has been maximized\n')


def show_banknotes():
    banknotes_list = read_file('banknotes.csv')
    sum = 0
    for i in banknotes_list:
        banknote = i['banknote']
        num = i['numberOf']
        if int(i['numberOf']) != 0:
            print(f'{num} banknote of {banknote}')
            sum+= int(banknote)*int(num)
        else:
            print(f'{num} banknote of {banknote}')
    print(f'\nBalance: {sum} UZS\n')
    clean_banknotes()


def admin_options() -> int:
    print('Select an action:\n1 - Maximize the quantity of all products\n2 - Set the remaining amount of each coin denomination to maximum\n3 - Indicate the number of cash banknotes received\n4 - Return to the main menu')
    while True:
        try:
            value = int(input('Your choice: '))
            print('')
            if 0 < value < 5:
                return value
            else:
                print('Please select a section in the menu!')
        except:
            print('Please select a section in the menu!')


def admin_panel():
    while True:
        option = admin_options()
        if option == 1:
            max_product()
        elif option == 2:
            max_coin()
        elif option == 3:
            show_banknotes()
        else:
            break
        

def dashboard():
    while True:
        option = options()
        if option == 1:
            insert_a_banknote()
        elif option == 2:
            print_all_product()
        elif option == 3:
            sell_product()
        elif option == 4:
            my_balance()
        elif option == 5:
            get_change()
        elif option == 12345:
            admin_panel()
        else:
            print('Qalesan')


dashboard()