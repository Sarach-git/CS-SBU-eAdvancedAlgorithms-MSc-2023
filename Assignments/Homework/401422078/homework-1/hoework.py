def long_multiplication(num1, num2):
    # تبدیل عدد ورودی به رشته ها
    str_num1 = str(num1)
    str_num2 = str(num2)

    # به دست آوردن تعداد ارقام هر عدد
    len_num1 = len(str_num1)
    len_num2 = len(str_num2)

    # در صورتی که یکی از اعداد صفر باشد، حاصل ضرب نیز صفر است
    if num1 == 0 or num2 == 0:
        return 0

    # در صورتی که یکی از اعداد دارای یک رقم باشد، ضرب آن با عدد دیگر برابر است با خود آن عدد
    if len_num1 == 1:
        return num2 * num1
    if len_num2 == 1:
        return num1 * num2

    # به دست آوردن تعداد ارقامی که باید در هر مرحله ضرب شوند
    n = max(len_num1, len_num2)
    if n % 2 != 0:
        n += 1

    # جداسازی اعداد در هر بخش
    num1_high = int(str_num1[:len_num1//2])
    num1_low = int(str_num1[len_num1//2:])
    num2_high = int(str_num2[:len_num2//2])
    num2_low = int(str_num2[len_num2//2:])

    # فراخوانی بازگشتی برای محاسبه مقادیر بخش های ضرب
    z0 = long_multiplication(num1_low, num2_low)
    z1 = long_multiplication((num1_low + num1_high), (num2_low + num2_high))
    z2 = long_multiplication(num1_high, num2_high)

    # محاسبه مقادیر جمع شونده در حاصل ضرب نهایی
    result = z2 * (10 ** n) + (z1 - z2 - z0) * (10 ** (n//2)) + z0

    return result
  
  
  
 
