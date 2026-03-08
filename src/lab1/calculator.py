#!/usr/bin/env python3
"""Simple calculator program."""


def main():
    """Main function that runs the calculator."""
    try:
        # Get input from user
        num1 = float(input("Введите первое число: "))
        num2 = float(input("Введите второе число: "))
        operation = input("Введите операцию (+, -, *, /): ")

        # Perform calculation
        if operation == "+":
            result = num1 + num2
        elif operation == "-":
            result = num1 - num2
        elif operation == "*":
            result = num1 * num2
        elif operation == "/":
            if num2 != 0:
                result = num1 / num2
            else:
                result = "Ошибка: деление на ноль"
        else:
            result = "Неизвестная операция"

        # Display result
        print(f"Результат: {result}")

    except ValueError:
        print("Ошибка: введите корректные числа")
    except KeyboardInterrupt:
        print("\nПрограмма прервана пользователем")
    except Exception as e:
        print(f"Произошла ошибка: {e}")


if __name__ == "__main__":
    main()
