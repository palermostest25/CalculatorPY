import os
import math
import time
import sys
import random
from statistics import *
import re
from decimal import Decimal, getcontext
import subprocess
import requests
from dotenv import load_dotenv
from openai import OpenAI
import urllib3
from deep_translator import GoogleTranslator
import kanu # type: ignore

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

sys.setrecursionlimit(2147483647)
os.system("title Caluclator")

versionnumber = float(3.8)

dotenv_path = ".env"
load_dotenv(dotenv_path)

openai_api_key = os.getenv("OPENAI_API_KEY")

if openai_api_key is None:
    print("OPENAI_API_KEY not Found in .env. Setting it to 'undefined'.")
    api_key = "undefined"
else:
    print(f"OPENAI_API_KEY is Set.")
    try:
        client = OpenAI(openai_api_key=os.getenv("OPENAI_API_KEY"))
    except:
        print("API Key is Not Working")


currency_api_key = os.environ.get("CURRENCY_API_KEY")

check_for_updates = os.getenv('CHECKFORUPDATES')

if check_for_updates is None:
    print("CHECKFORUPDATES Not Found in .env. Setting it to 'yes'.")
    check_for_updates = "yes"
else:
    print(f"CHECKFORUPDATES is Set to: {check_for_updates.strip().lower()}")


def help():
    print("Welcome to the Calculator!")
    print(f"==========V {versionnumber} (Python)==========")
    print("PI")
    print("E")
    print("POW")
    print("SQRT")
    print("Square")
    print("Round")
    print("ABS")
    print("AVG")
    print("Algebra")
    print("Conv for Conversions")
    print("Guess for Guessing Game")
    print("Sum for Solve Sum Game")
    print("TF for True or False Game")
    print("Simp for Simplification")
    print("Prime for Prime Number Generator")
    print("F for Fibonacci Calculator")
    print("D for Decibel Calculator")
    print("C for Currecy Converter")

def parse_ymxc(equation):
    match = re.match(r"y\s*=\s*([+-]?\d*\.?\d*)\s*x\s*([+-]\s*\d*\.?\d*)", equation.replace(" ", ""))
    
    if match:
        m = float(match.group(1)) if match.group(1) else 1.0
        c = float(match.group(2).replace(" ", "")) if match.group(2) else 0.0
        
        return m, c
    else:
        raise ValueError("The Equation is Not in the Expected Format: y = mx + c")

def calculate_ymxc_y(m, c, x):
    return m * x + c

def calculate_ymxc_x(y, m, c):
    return (y - c) / m


def chatbot():
    messages = [
        {"role": "system", "content": "You are a Helpful Maths Assistant."},
    ]
    while True:
        user_input = input("User: ")

        if user_input.lower() == "quit":
            break

        messages.append({"role": "user", "content": user_input})
        try:
            response = client.chat.completions.create(
                model="gpt-3.5-turbo",
                messages=messages
            )

            assistant_reply = response.choices[0].message.content
            print(f"Bot: {assistant_reply}")
            messages.append({"role": "assistant", "content": assistant_reply})
        except Exception as e:
            print(f"An Error Occurred: {e}")

def update():
    current_directory = os.getcwd()

    batch_script = os.path.join(current_directory, "updater.bat")

    subprocess.Popen(['start', '', batch_script], shell=True)
    sys.exit()

def asktoupdate(prompt):
    if prompt == "1":
        print("What Would You Like to Do?")
        print("1: Update")
        print("2: Don't Update")
        while True:
            updateornot = input("What Would You Like to Do? [1,2]: ")
            if updateornot == "1":
                update()
                break
            if updateornot == "2":
                break
    if prompt == "2":
        print("Updating...")
        update()

def checkgithub():
    global versionnumber
    global githubversionnumber
    try:
        githubversionnumber = (requests.get("https://api.github.com/repos/palermostest25/CalculatorPY/releases/latest"))
        githubversionnumber = float(githubversionnumber.json()["name"])
        if githubversionnumber == versionnumber:
            print("Calculator is Up-to-Date, Continuing...")
        if githubversionnumber > versionnumber:
            asktoupdate("1")
        if githubversionnumber < versionnumber:
            print("Local Version is Higher Than Github Version...")
            print("1: Continue")
            print("2: Grab Latest Release from Github")
            while True:
                biglocalversion = input("What Would You Like to Do? [1, 2]: ")
                if biglocalversion == "1":
                    print("Continuing...")
                    break
                if biglocalversion == "2":
                    asktoupdate("2")
                    break
                else:
                    print("Enter a Valid Response...")
                    pass
    except:
        print("Unable to Connect to Github...")
        print("Continuing...")

def fibonacciall():
    fib = [0, 1]
    count = 2

    while True:
        try:
            amnt = int(input("How Many Numbers of the Fibonacci Sequence Would You Like to Calculate?- "))
            break
        except ValueError:
            print("Error: Please enter an integer.")
            continue

    try:
        while count < amnt:
            fib.append(fib[count - 2] + fib[count - 1])
            count += 1
            frendlyfib = ', '.join(map(str, fib))
            print(f"Fibonacci: {frendlyfib} -- Amount of Numbers: {count}\n")

        input("Press Enter to Exit...")

    except KeyboardInterrupt:
        frendlyfib = ', '.join(map(str, fib))
        print(f"\nFibonacci: {frendlyfib} -- Amount of Numbers: {count}\n")
        input("Press Enter to Exit...")

def fibonaccisingle():
    fib = [0,1]
    while True:
        try:
            numbertogoto = int(input('Which Number in the Fibonacci Sequence Would You Like to Calculate?- '))
            break
        except ValueError:
            print('Please Enter A Number.')
            continue
    num = 2
    try:
        for loop1 in range(2, numbertogoto):
            nextfib = fib[0] + fib[1]
            fib.append(nextfib)
            fib = fib[1:]
            num += 1
            print(num, end='\r')
    except KeyboardInterrupt:
        pass

    print(f"Fibonacci: \r{fib[1]}, Number: {num}")

def goback():
    input("Press Enter to Go Back to The Start...")
    print()

def format_algebraic_expression(expression):
    expression = re.sub(r'(\d)([A-Z])', r'\1*\2', expression)
    expression = re.sub(r'([A-Z])(\()', r'\1*\2', expression)
    expression = re.sub(r'(\))([A-Z])', r'\1*\2', expression)
    expression = re.sub(r'(\))(\d)', r'\1*\2', expression)
    return expression

def is_prime(n):
    if n <= 1:
        return False
    for i in range(2, int(n**0.5) + 1):
        if n % i == 0:
            return False
    return True

def prime_nums_generator():
    n = 2
    while True:
        if is_prime(n):
            yield n
        n += 1

def simplify_ratio(ratio):
    num_list = list(map(int, ratio.split(":")))
    hcf = num_list[0]
    for num in num_list[1:]:
        hcf = math.gcd(hcf, num)
    simplified_nums = [str(num // hcf) for num in num_list]
    return ":".join(simplified_nums)

def find_lcm(numbers):
    def lcm(a, b):
        return abs(a * b) // math.gcd(a, b)
    
    num_list = list(map(int, numbers.split(",")))
    
    result = num_list[0]
    
    for num in num_list[1:]:
        result = lcm(result, num)
    
    return result


def find_hcf(numbers):
    num_list = list(map(int, numbers.split(",")))
    result = num_list[0]
    
    for num in num_list[1:]:
        result = math.gcd(result, num)
    
    return result


# def clean_units(unit):
    # unit = unit.rstrip('s')  # remove plural
    # words_to_remove = ['m', 'l', 'g']  # remove type of unit
    # for word in words_to_remove:
        # unit = unit.replace(word, '')
    # return unit


def pi_bbp():
    count = 0
    pi = Decimal(0)
    k = 0
    while count < accuracy:
        term = (Decimal(1)/(16**k)) * (
            Decimal(4)/(8*k + 1) - Decimal(2)/(8*k + 4) - Decimal(1)/(8*k + 5) - Decimal(1)/(8*k + 6))
        if term == 0:
            break
        pi += term
        k += 1
        print(pi, end='\r')
        count +=1
    os.system("cls")
    return f"{pi}"

def definevars():
    print("\nEnter Variables, Press Enter to Skip")
    
    vars_dict = {}
    
    for letter in "ABCDEFGHIJKLMNOPQRSTUVWXYZ":
        value = input(f"{letter}: ")
        if value.isnumeric():
            vars_dict[letter] = float(value)
        else:
            vars_dict[letter] = None
    
    return vars_dict

def convert(val, unit_in, unit_out=''):
    SI = {'mm': 0.001, 'cm': 0.01, 'm': 1,
          'i': 0.00393701, 
          'deci': 0.1, '': 1.0, 'deka': 10,
          'hecto': 100, 'kilo': 1000, 'l': 1000, 'ml': 1,
          'mi': 1609, 'km': 1000, 'g': 1, 'kg': 1000, 'p': 453.592}
    return val*SI[unit_in]/SI[unit_out]

def simplify_fraction(numerator, denominator):
    if math.gcd(numerator, denominator) == denominator:
        return int(numerator/denominator)
    elif math.gcd(numerator, denominator) == 1:
        return str(numerator) + "/" + str(denominator)
    else:
        top = numerator / math.gcd(numerator, denominator)
        bottom = denominator / math.gcd(numerator, denominator)
        return str(top) + "/" + str(bottom)


os.system("cls")
if check_for_updates == 'yes':
    print("Checking for Updates...")
    checkgithub()
elif check_for_updates == 'no':
    print("Not Checking for Updates.")
else:
    print("CHECKFORUPDATES Has an Unexpected Value:", check_for_updates)

help()
while True:
    try:
        sum = input("Please Enter Your Sum(Type ? for Information)- ")
        sum = sum.lower()
        if "=" in sum:
            sum = sum.split("=")
            calc1 = sum[0]
            calc2 = sum[1]
            result = eval(calc1)
            if str(calc2) == str(result):
                print("True")
            else:
                print("False")
            goback()
            continue
        if sum.lower() == "cls" or sum.lower() == "clear":
            os.system("cls")
            continue
        if sum.lower() == "power":
            usersum = input("Enter the Number: ")
            userthepower = input("To the Power of: ")
            usersum = float(usersum)
            userthepower = float(userthepower)
            result = (pow(usersum, userthepower))
            print(f"{usersum} to the Power of {userthepower} is {result}")
            goback()
            continue
        if sum.lower() == "sqrt":
            usersum = input("Enter the Number: ")
            usersum = float(usersum)
            result = math.sqrt(usersum)
            print(f"The Square Root of {usersum} is {result}")
            goback()
            continue
        if sum.lower() == "square":
            usersum = input("Enter the Number to be Squared: ")
            usersum = float(usersum)
            result = (usersum*usersum)
            print(f"The Square of {usersum} is {result}")
            goback()
            continue
        if sum.lower() == "round":
            usersum = input("Enter the Number to be Rounded: ")
            userto = int(input("Enter the amount of Decimal Places to Round to: "))
            result = round(float(usersum), userto)
            print(f"{usersum} Rounded to {userto} Decimal Places is {result}")
            goback()
            continue
        if sum.lower() == "abs":
            usersum = input("Enter the Number to Find the Absolute Value of: ")
            usersum = float(usersum)
            result = abs(usersum)
            print(f"The Absolute Value of {usersum} is {result}")
            goback()
            continue
        if sum.lower() == "avg":
            str1 = input('Enter the Following Syntax: "num1, num2, num3, etc": ')
            result = list(str1.split(','))
            total = 0
            for i in result:
                total += float(i)
            result1 = total / len(result)
            result1 = round(result1, 3)
            print(f"The Average of {str1} is {result1}")
            goback()
            continue
        if sum.lower() == "median":
            str1 = input('Enter the Following Syntax: "num1, num2, num3, etc": ')
            result = str1.split(', ')
            result1 = median(result)
            print(f"The Median of {str1} is {result1}")
            goback()
            continue
        if sum.lower() == "exit":
            exit()
        if sum.lower() == "mode":
            str1 = input('Enter the Following Syntax: "num1, num2, num3, etc": ')
            result = str1.split(', ')
            result1 = mode(result)
            print(f"The Mode of {str1} is {result1}")
            goback()
            continue
        if sum.lower() == "floor":
            usersum = input("Enter the Number: ")
            usersum = float(usersum)
            result = math.floor(usersum)
            print(f"The Floor of {usersum} is {result}")
            goback()
            continue
        if sum.lower() == "ceiling" or sum.lower() == "ceil":
            usersum = input("Enter the Number: ")
            usersum = float(usersum)
            result = math.ceil(usersum)
            print(f"The Ceiling of {usersum} is {result}")
            goback()
            continue
        if sum.lower() == "simp":
            print("1 = Simplify Fractions")
            print("2 = Simplify Ratios")
            simpopt = input("Which Option Would You Like? [1, 2]: ")
            if simpopt == "1":
                nume = int(input("Numerator: "))
                deno = int(input("Denominator: "))
                result = (simplify_fraction(nume, deno))
                print("The / Between The Numbers is the Line in the Middle of the Fraction (Vinculum)")
                print(f"{nume}/{deno} Simplified is {result}")
            if simpopt == "2":
                ratio = input("Enter Ratio (e.g., 10:20): ")
                print(f"Simplified Ratio: {simplify_ratio(ratio)}")
            goback()
            continue
        if sum.lower() == "algebra" or sum.lower() == "alg" or sum.lower() == "alge":
            print("1 = Linear Equation Solver")
            print("2 = Expression Simplifier")
            print("3 = General Algebra")

            algebraopt = input("What Option Would You Like [1, 2, 3]: ")
            if algebraopt == "1":
                print('Enter the Linear Equation: ', end='')
                try:
                    print(kanu.solve_single_linear_equation(input()))
                except kanu.NonLinearEquationError:
                    print('You Entered a Non-Linear Equation.')
            if algebraopt == "2":
                print('Enter the Expression to Simplify: ', end='')
                print(kanu.all_together_now(input()))
            if algebraopt == "3":
                print("1 = Set Variables")
                print("2 = Evaluate Sum")
                generalalgopt = input("What Option Would You Like [1, 2]: ")
                if generalalgopt == "1":
                    variables = definevars()
                if generalalgopt == "2": 
                    while True:
                        try:
                            algebrasum = input("Enter Your Algebraic Expression (use A-Z): ")
                            algebrasum = algebrasum.upper()
                            algebrasum = format_algebraic_expression(algebrasum)
                            used_vars = set(re.findall(r'[A-Z]', algebrasum))
                            variable_assignments = ', '.join([f"{var} is {variables[var]}" for var in used_vars if variables[var] is not None])
                            algebraicresult = eval(algebrasum, {}, variables)
                            break
                        except KeyboardInterrupt:
                            break
                        except:
                            pass
                    print(f"The Result of {algebrasum} is {algebraicresult} Where {variable_assignments}")
            goback()
            continue
        if sum.lower() == "conv" or sum.lower() == "convert" or sum.lower() == "converter":
            print("1 = Miles to KM")
            print("2 = Pounds to KG")
            print("3 = Celsius to Fahrenheit")
            print("4 = Fractions to Decimals")
            print("5 = Percentages to Fractions")
            print("6 = Percentages to Decimals")
            print("7 = Percent of a number")
            print("8 = Percent off")
            print("9 = Inches to CM")
            print("10 = Tax Calculator")
            print("11 = Add Percentage to a Number")
            print("12 = Language Translation")
            print("13 = Month Information")
            print("14 = What percentage of a number is in a number")
            print("15 = Celsius to Kelvin")
            print("16 = Fahrenheit to Kelvin")
            print("17 = Circle Tools")
            print("18 = LCM")
            print("19 = HCF")
            print("20 = Gradient of a Linear Function")
            print("21 = DST Calculator")
            print("22 = DMV Calculator")
            print("23 = y=mx+c Given Graph")
            print("24 = y=mx+c Given 2 Points")
            print("25 = x, y Points for y=mx+c Graph")
            convopt = input("What Option Would You Like [1-24]: ")
            print()

            if convopt == "1":
                print("1 = Miles to KM")
                print("2 = KM to Miles")
                milesorkm = input("What Option Would You Like? [1,2]: ")
                if milesorkm == "1":
                    miles = input("Miles: ")
                    miles = float(miles)
                    result = convert(miles, 'mi', 'km')
                    print(f"{miles} Miles is {result} KM")
                if milesorkm == "2":
                    km = input("KM: ")
                    km = float(km)
                    result = convert(km, 'km', 'mi')
                    print(f"{km} KM is {result} Miles")

            if convopt == "2":
                print("1 = Pound to KG")
                print("2 = KG to Pound")
                poundorkg = input("What Option Would You Like? [1,2]: ")
                if poundorkg == "1":
                    pound = input("Pound: ")
                    pound = float(pound)
                    result = convert(pound, 'p', 'kg')
                    print(f"{pound} Pounds is {result} KG")
                if poundorkg == "2":
                    kg = input("KG: ")
                    kg = float(kg)
                    result = convert(kg, 'kg', 'p')
                    print(f"{kg} KG is {result} Pounds")

            if convopt == "3":
                print("1 = Celsius to Fahrenheit")
                print("2 = Fahrenheit to Celsius")
                corf = input("What Option Would You Like? [1,2]: ")
                if corf == "1":
                    celsius = input("Celsius: ")
                    celsius = float(celsius)
                    # Manual because it's a Formula
                    result = eval("(celsius*9/5)+32")
                    print(f"{celsius} Degrees Celsius is {result} Fahrenheit")
                if corf == "2":
                    fahrenheit = input("Fahrenheit: ")
                    fahrenheit = float(fahrenheit)
                    # Manual because it's a Formula
                    result = eval("(fahrenheit-32)*9/5")
                    print(f"{fahrenheit} Degrees Fahrenheit is {result} Celsius")

            if convopt == "4":
                print("1 = Fraction to Decimal")
                print("2 = Decimal to Fraction")
                dorf = input("What Option Would You Like? [1,2]: ")
                if dorf == "1":
                    numerator = input("Numerator: ")
                    denominator = input("Denominator: ")
                    numerator = float(numerator)
                    denominator = float(denominator)
                    result = eval("numerator / denominator")
                    print("The / Between The Numbers is the Line in the Middle of the Fraction (Vinculum)")
                    print(f"{numerator} / {denominator} Expressed as a Decimal is {result}")
                if dorf == "2":
                    d = input("Decimal: ")
                    d = float(d)
                    result = (d).as_integer_ratio()
                    result = str(result)
                    result = result.replace('(', '')
                    result = result.replace(')', '')
                    result = result.replace(', ', ' / ')
                    print("The / Between The Numbers is the Line in the Middle of the Fraction (Vinculum)")
                    print(f"{d} Expressed as a Fraction is {result}")
            
            if convopt == "5":
                print("1 = Percentage to Fraction")
                print("2 = Fraction to Percentage")
                porf = input("What Option Would You Like? [1,2]: ")
                if porf == "1":
                    p = input("Percentage: ")
                    d = 100
                    p = float(p)
                    d = float(d)
                    print("The / Between The Numbers is the Line in the Middle of the Fraction (Vinculum)")
                    print(f"{p}% Expressed as a Fraction is {p} / {d}")
                if porf == "2":
                    f = input("Fraction (eg. 1/2) (The / Is the Line in the Middle of the Fraction (Vinculum)): ")
                    f1 = eval(f)
                    d = f1 * 100
                    result = eval("(round(d,4))")
                    print(f"{f} Expressed as a Percentage is {result}%")
                
            if convopt == "6":
                print("1 = Percentages to Decimals")
                print("2 = Decimals to Percentages")
                dorp = input("What Option Would You Like? [1,2]: ")
                if dorp == "1":
                    p = input("Percentage (No Percentage Sign): ")
                    print(f"{p}% as a Decimal is 0.{p}")
                if dorp == "2":
                    d = input("Decimal: ")
                    d = float(d)
                    result = float(eval("(d*100)"))
                    print(f"{d} as a Percentage is {result}%")

            if convopt == "7":
                p = input("Percentage (No Percentage Sign): ")
                num = input("Number to Find the Percentage of: ")
                p = float(p)
                num = float(num)
                result = eval("(p/100)*num")
                print(f"{p}% of {num} is {result}")
            
            if convopt == "8":
                print("1 = Price After Sale")
                print("2 = Price Before Sale")
                porp = input("What Option Would You Like? [1,2]: ")
                if porp == "1":
                    price = input("Origional Price (No Dollar Sign): ")
                    p = input("Percent Off (No Percentage Sign): ")
                    price = float(price)
                    p = float(p)
                    result = eval("price-(p/100)*price")
                    print(f"{p}% off ${price} is ${result}")
                if porp == "2":
                    price = input("Discounted Price (No Dollar Sign): ")
                    p = input("Percent Off (No Percentage Sign): ")
                    price = float(price)
                    p = float(p)
                    result = eval("price/((100-p)/100)")
                    print(f"The Origional Price of the Discounted Price ${price} After a Discount of {p}% is ${result}")

            if convopt == "9":
                print("1 = Inches to CM")
                print("2 = CM to Inches")
                iorc = input("What Option Would You Like? [1,2]: ")
                if iorc == "1":
                    inches = input("Inches: ")
                    inches = float(inches)
                    # Flipped because Math and to Correct the Convert Function
                    result = convert(inches, 'cm', 'i')
                    print(f"{inches} Inches to CM is {result}")
                if iorc == "2":
                    cm = input("CM: ")
                    cm = float(cm)
                    result = convert(cm, 'i', 'cm')
                    print(f"{cm} CM to Inches is {result}")

            if convopt == "10":
                price = input("Origional Price (No Dollar Sign): ")
                per = input("Tax Percentage (No Percentage Sign): ")
                price = float(price)
                per = float(per)
                result = eval("price+(price*(per/100))")
                print(f"${price} With Added Tax of {per}% is ${result}")

            if convopt == "11":
                value = input("Origional Value: ")
                per = input("Percentage to Add (No Percentage Sign): ")
                value = float(value)
                per = float(per)
                result = eval("value+(value*(per/100))")
                print(f"{value} With Added Percentage of {per}% is {result}")
            
            if convopt == "12":
                fromlang = input("From Language [eg. fr]: ")
                fromlang = fromlang.lower()
                tolang = input("To Language [eg. en]: ")
                tolang = tolang.lower()
                sentance = input("Input: ")
                translated = GoogleTranslator(source=fromlang, target=tolang).translate(sentance)
                print(f"{sentance} Translated from {fromlang} to {tolang} is {translated}")
                goback()
                continue

            if convopt == "13":
                print("Month Data: ")
                print("Number - Month - Short Form - Days")
                print("1 - January - Jan - 31")
                print("2 - Feburary - Feb - 28/29")
                print("3 - March - Mar - 31")
                print("4 - April - Apr - 30")
                print("5 - May - May - 31")
                print("6 - June - Jun - 30")
                print("7 - July - Jul - 31")
                print("8 - August - Aug - 31")
                print("9 - September - Sep - 30")
                print("10 - October - Oct - 31")
                print("11 - November - Nov - 30")
                print("12 - December - Dec - 31")
            
            if convopt == "14":
                fracnum = input("Part of a Number: ")
                totnum = input("Total Number: ")
                result = eval("(float(fracnum)/float(totnum)*100)")
                print(f"{fracnum} is {result}% of {totnum}")

            if convopt == "15":
                print("1 = Celsius to Kelvin")
                print("2 = Kelvin to Celsius")
                korc = input("What Option Would You Like? [1,2]: ")
                if korc == "1":
                    c = input("Celsius: ")
                    c = float(c)
                    result = eval("c+273.15")
                    print(f"{c} Degrees Celsius is {result} Degrees Kelvin")
                if korc == "2":
                    k = input("Kelvin: ")
                    k = float(k)
                    result = eval("k-273.15")
                    print(f"{k} Degrees Kelvin is {result} Degrees Celsius")

            if convopt == "16":
                print("1 = Fahrenheit to Kelvin")
                print("2 = Kelvin to Fehrenheit")
                fork = input("What Option Would You Like? [1,2]: ")
                if fork == "1":
                    f = input("Fahrenheit: ")
                    f = float(f)
                    # Manual because it's a formula
                    result = eval("(f-32)*5/9+273.15")
                    print(f"{f} Fahrenheit is {result} Kelvin")
                if fork == "2":
                    k = input("Kelvin: ")
                    k = float(k)
                    # Manual because it's a formula
                    result = eval("(k-273.15)*9/5+32")
                    print(f"{k} Kelvin is {result} Fahrenheit")

            if convopt == "17":
                print("1 = Area to Radius")
                print("2 = Radius to Area")
                print("3 = Area to Diameter")
                print("4 = Diameter to Area")
                print("5 = Area to Circumfrence")
                print("6 = Circumfrence to Area")
                print("7 = Diameter to Radius")
                print("8 = Radius to Diameter")
                print("9 = Diameter to Circumfrance")
                print("10 = Circumfrance to Diameter")
                print("11 = Radius to Circumfrance")
                print("12 = Circumfrance to Radius")
                corc = input("What Option Would You Like? [1-12]: ")
                print()
                if corc == "1":
                    a = input("Area (No Units)- ")
                    r = (math.sqrt(float(a)/3.14159265358979))
                    print(f"The Radius of a Cirle with an Area of {a} is {r}")
                if corc == "2":
                    r = input("Radius (No Units): ")
                    a = (3.14159265358979*(float(r)*float(r)))
                    print(f"The Area of a Circle with a Radius of {r} is {a}")
                if corc == "3":
                    a = input("Area (No Units)- ")
                    d = (2*math.sqrt(float(a)/3.14159265358979))
                    print(f"The Diameter of a Circle with an Area of {a} is {d}")
                if corc == "4":
                    d = input("Diameter (No Units)- ")
                    a = ((float(d)/2)**2)*3.14159265358979
                    print(f'The Area of a Circle with a Diameter of {d} is {a}')
                if corc == "5":
                    a = input("Area (No Units)- ")
                    c = 2*math.sqrt(float(a)*3.14159265358979)
                    print(f'The Circumfrence of a Circle with Area {a} is {c}')
                if corc == "6":
                    c = input("Circumfrence (No Units)- ")
                    d = (float(c)/3.14159265358979)
                    a = ((float(d)/2)**2)*3.14159265358979
                    print(f'The Area of a Circle with Circumfrence {c} is {a}')
                if corc == "7":
                    d = input("Diameter (No Units)- ")
                    r = float(d)/2
                    print(f"The Radius of a Circle with Diameter {d} is {r}")
                if corc == "8":
                    r = input("Radius (No Units)- ")
                    d = float(r)*2
                    print(f'The Diameter of a Circle with Radius {r} is {d}')
                if corc == "9":
                    d = input("Diameter (No Units)- ")
                    c = float(d)*3.14159265358979
                    print(f'The Circumfrence of a Circle with Diameter {d} is {c}')
                if corc == "10":
                    c = input("Circumfrence (No Units)- ")
                    d = float(c)/3.14159265358979
                if corc == "11":
                    r = input("Radius (No Units)- ")
                    c = 2*float(r)*3.14159265358979
                    print(f'The Circumfrence of a Circle with Radius {r} is {c}')
                if corc == "12":
                    c = input("Circumfrence (No Units)- ")
                    r = float(c)/3.14159265358979/2
                    print(f'The Radius of a Circle with Circumfrence {c} is {r}')
            if convopt == "18":
                lcmnumbers = input("Enter Numbers to Find the Lowest Common Multiple of (Separated by Commas): ")
                print(f"The LCM of These Numbers is: {find_lcm(lcmnumbers)}")
                goback()
                continue
            if convopt == "19":
                hcfnumbers = input("Enter Numbers to Find the Highest Common Factor of (Separated By Commas): ")
                print(f"The HCF Of The Numbers is: {find_hcf(hcfnumbers)}")
                goback()
                continue

            if convopt == "20":
                c = float(input("Starting Constant: "))
                x = float(input("Rate: "))
                m = float(input("Number of Rate: "))
                y = (m*x)+c
                print(f"The Total of a Linear Function with a Constant of {c}, a Rate of {x} and an Amount of Rate of {m} is {y}")
                goback()
                continue
            
            if convopt == "21":
                print("1 = Distance")
                print("2 = Speed")
                print("3 = Time")
                dstopt = int(input("Which Would You Like to Find?- "))
                if dstopt == "1":
                    speed = float(input("Speed (No Units): "))
                    dsttime = float(input("Time (No Units): "))
                    distance = speed * dsttime
                    print(f"The Distance Travelled After {dsttime} at {speed} is {distance}")
                if dstopt == "2":
                    distance = float(input("Distance (No Units): "))
                    dsttime = float(input("Time (No Units): "))
                    speed = distance / dsttime
                    print(f"The Speed Travelled Over {distance} for {dsttime} is {speed}")
                if dstopt == "3":
                    distance = float(input("Distance (No Units): "))
                    speed = float(input("Speed (No Units): "))
                    dsttime = distance / speed
                    print(f"The Time Taken to Travel {distance} at {speed} is {dsttime}")
                goback()
                continue
                
            if convopt == "22":
                print("1 = Density")
                print("2 = Mass")
                print("3 = Volume")
                dmvopt = int(input("Which Would You Like to Find?- "))
                if dmvopt == "1":
                    mass = float(input("Mass (No Units): "))
                    dmvvolume = float(input("Volume (No Units): "))
                    density = mass / dmvvolume
                    print(f"The Density Travelled After {dmvvolume} at {mass} is {density}")
                if dmvopt == "2":
                    density = float(input("Density (No Units): "))
                    dmvvolume = float(input("Volume (No Units): "))
                    mass = density * dmvvolume
                    print(f"The Mass Travelled Over {density} for {dmvvolume} is {mass}")
                if dmvopt == "3":
                    density = float(input("Density (No Units): "))
                    mass = float(input("Mass (No Units): "))
                    dmvvolume = mass / density
                    print(f"The Volume Taken to Travel {density} at {mass} is {dmvvolume}")
                goback()
                continue
            
            if convopt == "23":
                change = float(input("Change on the Y Axis Per x (Can Enter Per Any Number of x and Input That Number Next)- "))
                perx = float(input("Per Number of x- "))
                gradient = change / perx
                intercept = float(input("Y Intercept- "))
                print(f"Calculation: y={gradient}x+{intercept}")
                goback()
                continue

            if convopt == "24":
                x1 = float(input("First X Value (No Units): "))
                y1 = float(input("First Y Value (No Units): "))
                x2 = float(input("Second X Value (No Units): "))
                y2 = float(input("Second Y Value (No Units): "))
                slope = (y2-y1) / (x2-x1)
                constant = y1 - (slope * x1)
                print(f"The y=mx+c Formula for the 2 Points ({x1}, {y1}) and ({x2}, {y2}) is y = {slope}x + {constant}")
                goback()
                continue

            if convopt == "25":
                equation = input("Enter the Equation in the Form 'y = mx + c' (e.g., y = 10x + 2): ")
                try:
                    m, c = parse_ymxc(equation)
                    xycalc = input("Which Would You Like to Calculate? [x, y]: ")
                    if xycalc.lower() == "x":
                        y = float(input("Enter the Value of y: "))
                        x = calculate_ymxc_x(y, m, c)
                        print(f"The Value for x for y = {y} is: {x}")
                    if xycalc.lower() == "y":
                        x = float(input("Enter the Value of x: "))
                        y = calculate_ymxc_y(m, c, x)
                        print(f"The Value of y for x = {x} is: {y}")

                except ValueError as e:
                    print(f"Error: {e}")

                goback()
                continue

            goback()
            continue

        if sum.lower() == "guess":
            print("1 = I Guess")
            print("2 = You Guess")
            meoryou = input("Which Game Would You Like? [1, 2]- ")
            if meoryou == "1":
                print("Pick a Number.")
                print("I Will Try to Guess It!")
                guessrange = input("Enter Your Range (eg., 1-100): ")
                tries = 0
                try:
                    start, end = map(int, guessrange.split('-'))
                    if start > end:
                        print("Error: The Start Number Must Be Less Than Or Equal to the End Number.")
                    else:
                        while True:
                            guess = random.randint(start, end)
                            print(f"I Guess {guess} Current Tries: {tries}")
                            hlc = input("Higher, Lower Or Correct? [1, 2, 3]: ")
                            if hlc == "3":
                                print(f"Yay! I Guessed Your Number: {guess} in {tries} Tries")
                                break
                            elif hlc == "1":
                                start = guess + 1
                            elif hlc == "2":
                                end = guess - 1
                            else:
                                print("Invalid Input! Please Enter 1 (Higher), 2 (Lower), or 3 (Correct).")
                            tries += 1
                except ValueError:
                    print("Error: Please Enter A Valid Range In The Format 'Start-End' (eg., 1-100).")
            if meoryou == "2":
                lowest = int(input("Between- "))
                highest = int(input("And- "))
                randomnumber = random.randint(lowest, highest)
                guessamnt = 0
                while True:
                    guess = input("Guess the Number: ")
                    guess = int(guess)
                    guessamnt += 1
                    if guess == randomnumber:
                        print("Great Job!")
                        print(f"You Guessed It In {guessamnt} Tries!")
                    if guess > highest:
                        print("Guess is Outside Range!")
                        continue
                    if guess < lowest:
                        print("Guess is Outside Range!")
                        continue
                    if guess > randomnumber:
                        print("Lower!")
                        continue
                    if guess < randomnumber:
                        print("Higher!")
                        continue
                    goback()
                    break
            goback()
            continue

            
        if sum.lower() == "sum":
            choice = input("1 = Addition\n2 = Subtraction\n3 = Multiplication\n4 = Division\n5 = All\nWhat Type of Operations Would You Like?: ")
            level = input("What Level Would You Like? [1, 2, 3]: ")
            rounds = int(input("How Many Rounds Would You Like to Play?: "))
            score = 0
            besttime = 100

            if choice == "1": #addition
                count = 0
                while count < rounds:
                    start = time.time()
                    if level == "1":
                        sum1 = random.randint(1, 50)
                        sum2 = random.randint(1, 50)
                    if level == "2":
                        sum1 = random.randint(1, 100)
                        sum2 = random.randint(1, 100)
                    if level == "3":
                        sum1 = round(random.uniform(1.0, 100.0), 1)
                        sum2 = round(random.uniform(1.0, 100.0), 1)
                    answer = round(float(eval(f"{sum1} + {sum2}")), 1)
                    print(f"What is the Answer to {sum1} + {sum2}?")
                    while True:
                        try:
                            useranswer = input(">>> ")
                            break
                        except TypeError:
                            pass
                    end = time.time()
                    timetaken = round(end-start, 2)
                    if timetaken < besttime:
                        besttime = timetaken
                    if useranswer == answer:
                        score += 1
                        print(f"Correct! Score: {score} Time Taken: {round(end-start, 2)}s\n")
                    if useranswer != answer:
                        print(f"Incorrect! Score: {score}")
                        print(f"Answer: {answer}, You Put: {useranswer} Time Taken: {round(end-start, 2)}s\n")
                    count += 1

            if choice == "2": #subtraction
                count = 0
                while count < rounds:
                    start = time.time()
                    if level == "1":
                        sum1 = random.randint(1, 50)
                        sum2 = random.randint(1, 50)
                    if level == "2":
                        sum1 = random.randint(1, 100)
                        sum2 = random.randint(1, 100)
                    if level == "3":
                        sum1 = round(random.uniform(1.0, 100.0), 1)
                        sum2 = round(random.uniform(1.0, 100.0), 1)
                    answer = round(float(eval(f"{sum1} - {sum2}")), 1)
                    print(f"What is the Answer to {sum1} - {sum2}?")
                    while True:
                        try:
                            useranswer = input(">>> ")
                            break
                        except TypeError:
                            pass
                    end = time.time()
                    timetaken = round(end-start, 2)
                    if timetaken < besttime:
                        besttime = timetaken
                    if useranswer == answer:
                        score += 1
                        print(f"Correct! Score: {score} Time Taken: {round(end-start, 2)}s\n")
                    if useranswer != answer:
                        print(f"Incorrect! Score: {score}")
                        print(f"Answer: {answer}, You Put: {useranswer} Time Taken: {round(end-start, 2)}s\n")
                    count += 1

            if choice == "3": #multiplication
                count = 0
                while count < rounds:
                    start = time.time()
                    if level == "1":
                        sum1 = random.randint(1, 50)
                        sum2 = random.randint(1, 50)
                    if level == "2":
                        sum1 = random.randint(1, 100)
                        sum2 = random.randint(1, 100)
                    if level == "3":
                        sum1 = round(random.uniform(1.0, 100.0), 1)
                        sum2 = round(random.uniform(1.0, 100.0), 1)
                    answer = round(float(eval(f"{sum1} * {sum2}")), 1)
                    print(f"What is the Answer to {sum1} * {sum2}?")
                    while True:
                        try:
                            useranswer = input(">>> ")
                            break
                        except TypeError:
                            pass
                    end = time.time()
                    timetaken = round(end-start, 2)
                    if timetaken < besttime:
                        besttime = timetaken
                    if useranswer == answer:
                        score += 1
                        print(f"Correct! Score: {score} Time Taken: {round(end-start, 2)}s\n")
                    if useranswer != answer:
                        print(f"Incorrect! Score: {score}")
                        print(f"Answer: {answer}, You Put: {useranswer} Time Taken: {round(end-start, 2)}s\n")
                    count += 1

            if choice == "4": #division
                count = 0
                while count < rounds:
                    start = time.time()
                    if level == "1":
                        sum1 = random.randint(1, 50)
                        sum2 = random.randint(1, 50)
                    if level == "2":
                        sum1 = random.randint(1, 100)
                        sum2 = random.randint(1, 100)
                    if level == "3":
                        sum1 = round(random.uniform(1.0, 100.0), 1)
                        sum2 = round(random.uniform(1.0, 100.0), 1)
                    answer = round(float(eval(f"{sum1} / {sum2}")), 1)
                    print(f"What is the Answer to {sum1} / {sum2}?")
                    while True:
                        try:
                            useranswer = input(">>> ")
                            break
                        except TypeError:
                            pass
                    end = time.time()
                    timetaken = round(end-start, 2)
                    if timetaken < besttime:
                        besttime = timetaken
                    if useranswer == answer:
                        score += 1
                        print(f"Correct! Score: {score} Time Taken: {round(end-start, 2)}s\n")
                    if useranswer != answer:
                        print(f"Incorrect! Score: {score}")
                        print(f"Answer: {answer}, You Put: {useranswer} Time Taken: {round(end-start, 2)}s\n")
                    count += 1

            if choice == "5": #all
                count = 0
                start = time.time()
                while count < rounds:
                    if level == "1":
                        sum1 = random.randint(1, 50)
                        sum2 = random.randint(1, 50)
                    if level == "2":
                        sum1 = random.randint(1, 100)
                        sum2 = random.randint(1, 100)
                    if level == "3":
                        sum1 = round(random.uniform(1.0, 100.0), 1)
                        sum2 = round(random.uniform(1.0, 100.0), 1)
                    
                    sign = random.choice(["+", "-", "*", "/"])
                    answer = round(float(eval(f"{sum1} {sign} {sum2}")), 1)
                    print(f"What is the Answer to {sum1} {sign} {sum2}?")
                    while True:
                        try:
                            useranswer = input(">>> ")
                            break
                        except TypeError:
                            pass
                    end = time.time()
                    timetaken = round(end-start, 2)
                    if timetaken < besttime:
                        besttime = timetaken
                    if useranswer == answer:
                        score += 1
                        print(f"Correct! Score: {score} Time Taken: {round(end-start, 2)}s\n")
                    if useranswer != answer:
                        print(f"Incorrect! Score: {score}")
                        print(f"Answer: {answer}, You Put: {useranswer} Time Taken: {round(end-start, 2)}s\n")
                    count += 1
            goback()
            continue

        if sum.lower() == "tf":
            while True:
                try:
                    choice = input("1 = Addition\n2 = Subtraction\n3 = Multiplication\n4 = Division\n5 = All\nWhat Type of Operations Would You Like?: ")
                    level = input("What Level Would You Like? [1, 2, 3]: ")
                    rounds = int(input("How Many Rounds Would You Like to Play?: "))
                    break
                except:
                    print("\nEnter a Valid Input\n")
                    pass

            print("When Answering,\n1 = True\n2 = False")

            if choice == "1": #addition
                score = 0
                count = 0
                while count < rounds:
                    start = time.time()
                    changeornot = random.randint(0, 1)
                    if level == "1":
                        sum1 = random.randint(1, 50)
                        sum2 = random.randint(1, 50)
                        answer = eval(f"{sum1} + {sum2}")
                        difference = random.randint(-50, 50)
                    if level == "2":
                        sum1 = random.randint(1, 100)
                        sum2 = random.randint(1, 100)
                        answer = eval(f"{sum1} + {sum2}")
                        difference = random.randint(-100, 100)
                    if level == "3":
                        sum1 = round(random.uniform(1.0, 100.0), 1)
                        sum2 = round(random.uniform(1.0, 100.0), 1)
                        answer = eval(f"{sum1} + {sum2}")
                        difference = round(random.uniform(1.0, 100.0), 1)

                    if changeornot == 0:
                        print(f"Does {sum1} + {sum2} = {answer}? [1, 2]- ")
                        while True:
                            try:
                                useranswer = input(">>> ")
                                break
                            except:
                                pass
                        end = time.time()
                        timetaken = round((end - start), 1)
                        if useranswer == "1":
                            score += 1
                            print(f"Correct! Score: {score} Time: {timetaken}")
                        if useranswer == "2":
                            print(f"Wrong! Score: {score} Time: {timetaken}")

                    if changeornot == 1:
                        print(f"Does {sum1} + {sum2} = {answer + difference}? [1, 2]-")
                        while True:
                            try:
                                useranswer = input(">>> ")
                                break
                            except:
                                pass
                        end = time.time()
                        timetaken = round((end - start), 1)
                        if useranswer == "1":
                            print(f"Wrong! Score: {score} Time: {timetaken}")
                        if useranswer == "2":
                            score += 1
                            print(f"Correct! Score: {score} Time: {timetaken}")
                    count += 1

            if choice == "2": #subtraction
                score = 0
                count = 0
                while count < rounds:
                    start = time.time()
                    changeornot = random.randint(0, 1)
                    if level == "1":
                        sum1 = random.randint(1, 50)
                        sum2 = random.randint(1, 50)
                        answer = eval(f"{sum1} - {sum2}")
                        difference = random.randint(-50, 50)
                    if level == "2":
                        sum1 = random.randint(1, 100)
                        sum2 = random.randint(1, 100)
                        answer = eval(f"{sum1} - {sum2}")
                        difference = random.randint(-100, 100)
                    if level == "3":
                        sum1 = round(random.uniform(1.0, 100.0), 1)
                        sum2 = round(random.uniform(1.0, 100.0), 1)
                        answer = eval(f"{sum1} - {sum2}")
                        difference = round(random.uniform(1.0, 100.0), 1)

                    if changeornot == 0:
                        print(f"Does {sum1} - {sum2} = {answer}? [1, 2]- ")
                        while True:
                            try:
                                useranswer = input(">>> ")
                                break
                            except:
                                pass
                        end = time.time()
                        timetaken = round((end - start), 1)
                        if useranswer == "1":
                            score += 1
                            print(f"Correct! Score: {score} Time: {timetaken}")
                        if useranswer == "2":
                            print(f"Wrong! Score: {score} Time: {timetaken}")

                    if changeornot == 1:
                        print(f"Does {sum1} - {sum2} = {answer + difference}? [1, 2]-")
                        while True:
                            try:
                                useranswer = input(">>> ")
                                break
                            except:
                                pass
                        end = time.time()
                        timetaken = round((end - start), 1)
                        if useranswer == "1":
                            print(f"Wrong! Score: {score} Time: {timetaken}")
                        if useranswer == "2":
                            score += 1
                            print(f"Correct! Score: {score} Time: {timetaken}")
                    count += 1

            if choice == "3": #multiplication
                score = 0
                count = 0
                while count < rounds:
                    start = time.time()
                    changeornot = random.randint(0, 1)
                    if level == "1":
                        sum1 = random.randint(1, 50)
                        sum2 = random.randint(1, 50)
                        answer = eval(f"{sum1} * {sum2}")
                        difference = random.randint(-50, 50)
                    if level == "2":
                        sum1 = random.randint(1, 100)
                        sum2 = random.randint(1, 100)
                        answer = eval(f"{sum1} * {sum2}")
                        difference = random.randint(-100, 100)
                    if level == "3":
                        sum1 = round(random.uniform(1.0, 100.0), 1)
                        sum2 = round(random.uniform(1.0, 100.0), 1)
                        answer = eval(f"{sum1} * {sum2}")
                        difference = round(random.uniform(1.0, 100.0), 1)

                    if changeornot == 0:
                        print(f"Does {sum1} * {sum2} = {answer}? [1, 2]- ")
                        while True:
                            try:
                                useranswer = input(">>> ")
                                break
                            except:
                                pass
                        end = time.time()
                        timetaken = round((end - start), 1)
                        if useranswer == "1":
                            score += 1
                            print(f"Correct! Score: {score} Time: {timetaken}")
                        if useranswer == "2":
                            print(f"Wrong! Score: {score} Time: {timetaken}")

                    if changeornot == 1:
                        print(f"Does {sum1} * {sum2} = {answer + difference}? [1, 2]-")
                        while True:
                            try:
                                useranswer = input(">>> ")
                                break
                            except:
                                pass
                        end = time.time()
                        timetaken = round((end - start), 1)
                        if useranswer == "1":
                            print(f"Wrong! Score: {score} Time: {timetaken}")
                        if useranswer == "2":
                            score += 1
                            print(f"Correct! Score: {score} Time: {timetaken}")
                    count += 1

            if choice == "4": #division
                score = 0
                count = 0
                while count < rounds:
                    start = time.time()
                    changeornot = random.randint(0, 1)
                    if level == "1":
                        sum1 = random.randint(1, 50)
                        sum2 = random.randint(1, 50)
                        answer = eval(f"{sum1} / {sum2}")
                        difference = random.randint(-50, 50)
                    if level == "2":
                        sum1 = random.randint(1, 100)
                        sum2 = random.randint(1, 100)
                        answer = eval(f"{sum1} / {sum2}")
                        difference = random.randint(-100, 100)
                    if level == "3":
                        sum1 = round(random.uniform(1.0, 100.0), 1)
                        sum2 = round(random.uniform(1.0, 100.0), 1)
                        answer = eval(f"{sum1} / {sum2}")
                        difference = round(random.uniform(1.0, 100.0), 1)

                    if changeornot == 0:
                        print(f"Does {sum1} / {sum2} = {answer}? [1, 2]- ")
                        while True:
                            try:
                                useranswer = input(">>> ")
                                break
                            except:
                                pass
                        end = time.time()
                        timetaken = round((end - start), 1)
                        if useranswer == "1":
                            score += 1
                            print(f"Correct! Score: {score} Time: {timetaken}")
                        if useranswer == "2":
                            print(f"Wrong! Score: {score} Time: {timetaken}")

                    if changeornot == 1:
                        print(f"Does {sum1} / {sum2} = {answer + difference}? [1, 2]-")
                        while True:
                            try:
                                useranswer = input(">>> ")
                                break
                            except:
                                pass
                        end = time.time()
                        timetaken = round((end - start), 1)
                        if useranswer == "1":
                            print(f"Wrong! Score: {score} Time: {timetaken}")
                        if useranswer == "2":
                            score += 1
                            print(f"Correct! Score: {score} Time: {timetaken}")
                    count += 1

            if choice == "5": #all
                score = 0
                count = 0
                while count < rounds:
                    start = time.time()
                    changeornot = random.randint(0, 1)
                    sign = random.choice(["+", "-", "*", "/"])
                    if level == "1":
                        sum1 = random.randint(1, 50)
                        sum2 = random.randint(1, 50)
                        answer = round(float(eval(f"{sum1} {sign} {sum2}")), 1)
                        difference = random.randint(-50, 50)
                    if level == "2":
                        sum1 = random.randint(1, 100)
                        sum2 = random.randint(1, 100)
                        answer = round(float(eval(f"{sum1} {sign} {sum2}")), 1)
                        difference = random.randint(-100, 100)
                    if level == "3":
                        sum1 = round(random.uniform(1.0, 100.0), 1)
                        sum2 = round(random.uniform(1.0, 100.0), 1)
                        answer = round(float(eval(f"{sum1} {sign} {sum2}")), 1)
                        difference = round(random.uniform(1.0, 100.0), 1)

                    if changeornot == 0:
                        print(f"Does {sum1} {sign} {sum2} = {answer}? [1, 2]- ")
                        while True:
                            try:
                                useranswer = input(">>> ")
                                break
                            except:
                                pass
                        end = time.time()
                        timetaken = round((end - start), 1)
                        if useranswer == "1":
                            score += 1
                            print(f"Correct! Score: {score} Time: {timetaken}")
                        if useranswer == "2":
                            print(f"Wrong! Score: {score} Time: {timetaken}")

                    if changeornot == 1:
                        print(f"Does {sum1} {sign} {sum2} = {answer + difference}? [1, 2]-")
                        while True:
                            try:
                                useranswer = input(">>> ")
                                break
                            except:
                                pass
                        end = time.time()
                        timetaken = round((end - start), 1)
                        if useranswer == "1":
                            print(f"Wrong! Score: {score} Time: {timetaken}")
                        if useranswer == "2":
                            score += 1
                            print(f"Correct! Score: {score} Time: {timetaken}")
                    count += 1
            goback()
            continue

        if sum.lower() == "pi":
            decimals = int(input("How Many Decimals Would You Like in Your Number? [1-x]: "))
            accuracy = input("How Accurate Would You Like Your Number? [1-x] (x for Infinity): ")
            getcontext().prec = decimals
            if accuracy.isnumeric():
                try:
                    accuracy = int(accuracy)
                    pi = pi_bbp()
                    print(f"Pi: {pi}, Accuracy: {accuracy}")
                except KeyboardInterrupt:
                    print(f"Final: {pi}, Accuracy: {accuracy}")
            else:
                print("Invalid input or non-numeric value.")
                count = 0
                pi = Decimal(0)
                k = 0
                try:
                    while True:
                        term = (Decimal(1)/(16**k)) * (
                            Decimal(4)/(8*k + 1) - Decimal(2)/(8*k + 4) - Decimal(1)/(8*k + 5) - Decimal(1)/(8*k + 6))
                        if term == 0:
                            break
                        pi += term
                        k += 1
                        print(f"Pi: {pi}, Accuracy: {count}", end='\r')
                        count +=1
                except KeyboardInterrupt:
                    os.system("cls")
                    print(f"Final: {pi}, Accuracy: {accuracy}")
            goback()
            continue

        if sum.lower() == "e":
            decimals = int(input("Decimals- "))
            getcontext().prec = decimals
            e = Decimal(0)
            f = Decimal(1)
            n = Decimal(1)
            while True:
                olde = e
                e += Decimal(1) / f
                if e == olde: # if there was no change in the 40 places, stop.
                    break
                f *= n
                n += Decimal(1)
            print(f"E Correct to {decimals} Decimal Places is {Decimal(e)}")
            goback()
            continue
            
        if sum.lower() == "prime":
            primes = prime_nums_generator()
            n = int(input("Input the Number of Prime Numbers You Want to Generate- "))

            print("First",n,"Prime Numbers:")
            for _ in range(n):
                print(next(primes))
            goback()
            continue

        if sum.lower() == "chatgpt" or sum.lower() == "gpt":
            print("Start Chatting with the Bot (Type 'quit' to Stop)!")
            chatbot()
            goback()
            continue

        if sum.lower() == "?" or sum.lower() == "help":
            os.system("cls")
            help()
            goback()
            continue

        if "!" in sum:
            sum = sum[:-1]
            sum = int(sum)
            fact = 1

            for i in range(1, sum+1):
                fact = fact * i

            print(f"The Factorial of {sum} is: {fact}")
            goback()
            continue

        if sum.lower() == "f" or sum.lower() == "fibonacci":
            fib = [0,1]
            count = 0
            sys.set_int_max_str_digits(2147483647)
            print("1- Single")
            print("2- Whole Sequence")
            option = input("Would you Like to Find a Single Digit or the Whole Sequence?- ")
            try:
                option = int(option)
            except:
                print("Error: Not an Int")
                input("Press Enter to Exit...")
                exit()
            if option == 1:
                fibonaccisingle()
            if option == 2:
                fibonacciall()
            goback()
            continue
        
        if sum.lower() == "d" or sum.lower() == "decibel":
            input_values = input("Enter the Decibel Values and Operations (e.g., 10 + 20 - 5): ").split()
            total_intensity = 10 ** (float(input_values[0]) / 10)
            i = 1
            while i < len(input_values):
                operator = input_values[i]
                next_value = float(input_values[i + 1])
                next_intensity = 10 ** (next_value / 10)
                
                if operator == '+':
                    total_intensity += next_intensity
                elif operator == '-':
                    total_intensity -= next_intensity
                i += 2
            total_dB = 10 * math.log10(total_intensity)
            print(f"The Resulting Decibel Level After Performing {input_values} is Approximately {total_dB:.2f} dB")
            goback()
            continue

        if sum.lower() == "c" or sum.lower() == "currency":
            url = f'https://api.currencyapi.com/v3/latest?apikey={currency_api_key}'

            response = requests.get(url, verify=False)
            data = response.json()

            rates = data['data']

            def convert_currency(amount, from_currency, to_currency, rates):
                if from_currency != 'USD':
                    amount = amount / rates[from_currency]['value']
                return amount * rates[to_currency]['value']


            amount = float(input("Enter Amount: $"))
            #amount = amount.replace("$", "")
            from_currency = input("From Currency (e.g., USD): ").upper()
            to_currency = input("To Currency (e.g., EUR): ").upper()

            converted_amount = convert_currency(amount, from_currency, to_currency, rates)
            print(f"{amount} {from_currency} = {converted_amount:.2f} {to_currency}")
            goback()
            continue

        if sum.endswith("/0"):
            input("Are You Sure You Want to Do This? Press Enter to Continue...")
            input("But I am Just Reccomending That You Don't Do This...")
            input("I Told You, Don't Do It...")
            input("Actually, Screw It, I Want to See What Happens Too...")
            print("5")
            time.sleep(1)
            print("4")
            time.sleep(1)
            print("3")
            time.sleep(1)
            print("2")
            time.sleep(1)
            print("1")
            time.sleep(1)
            print("Creating Wormhole to the Future...")
            time.sleep(1)
            print("Reality Engine Shutting Down...")
            time.sleep(1)
            print("Inverting Matter...")
            time.sleep(1)
            print("Creating Synthetic Universe...")
            time.sleep(1)
            print("Untangling String Theory...")
            time.sleep(2)
            print("\n\n\n\n\n\n\n\nContacting the Ghost of Stephen Hawking...")
            time.sleep(3)
            print("YOU FOOL, YOU HAVE DOOMED US ALL!!!!!!! DEATH!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!")
            time.sleep(2)
            os.system(f'python "{os.getcwd()}\\dino.py"')
            goback()
            continue

        else:
            try:
                sum = sum.lower()
                sum = sum.replace("m", "000000")
                sum = sum.replace("b", "000000000")
                sum = sum.replace("t", "000000000000")
                sum = re.sub(r"(\d+)\(", r"\1*(", sum)
                
                try:
                    result = eval(sum)
                    print(f"The Answer to {sum} is {result}")
                except Exception as e:
                    print("Error")
                    goback()
                    continue

            except:
                print("Error")
                goback()
                continue
            goback()
            continue
    except KeyboardInterrupt:
        print()
        goback()
        continue
    except:
        print("Error")
        goback()
        continue
        goback()