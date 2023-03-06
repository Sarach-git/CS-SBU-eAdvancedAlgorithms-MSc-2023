## First Section:
Our problem:

Input: two n-digit integers a and b

Output: multiplication of a and b

### 1. Divide

We divide each integer into two halves. Then we multiply each half like below:

          aL = 2395  |  8233 = aR
                     |
          bL = 58    |  30 = bR


               aL          aR
    x          bL          bR
  -----------------------------
               aL bR       aR bR
    aL bL      aR bL       
  -----------------------------
    aL bL   aL bR + aR bL   aR bR

We can prove that for multiplication of two integers we can just calculate the result of these three multiplication:

+ Multipication(aL, bL)
+ Multipication(aL + aR, bL + bR)
+ Multipication(aR, bR)

And then calculate these formula:

+ x1 * 10 ^ n + (x2 - x1 - x3) * 10 ^ n/2 + x3


### 2. Conquer
Each of multipication above is a new multipication for calculate till we get to multipication of a one digit number.

### 3. Combine

When we get to point that we have one digit number, we can combine the multipication by formula are shown in psudocode below for combine each multipication.

----

    Algorithm Divide and Conquer Multipication(a,b):

    if a or b has one digit, then:
    return a * b

    else:
        Let n be the number of digits in max{a, b}
        Let aL and aR be left and right halves of a
        Let bL and bR be left and right halves of b
        Let x1 hold Divide and Conquer Multipication(aL, bL)
        Let x2 hold Divide and Conquer Multipication(aL + aR, bL + bR)
        Let x3 hold Divide and Conquer Multipication(aR, bR)
        return x1 * 10 ^ n + (x2 - x1 - x3) * 10 ^ n/2 + x3
    

## Second Section

When one of our numbers (a or b) has only one digit, we can stop dividing the numbers and return. So we can call the first digit multipication smallest sub problem.

## Fourth Section

This algorithm is to compute x1, x2, and x3, and add. Time complexity of this algorithm is: O(n ^ 1.58)

For prove this time complexity, we have:

    T(n) = 1, if n = 1
    T(n) = 3T(n/2), if n > 1

Which T(n) is just one function call of our problem with maximum n digit numbers.

In first iteration we have: 

    T(n) = 3 * T(n/2)

And then in next iteration:

    T(n/2) = 3 * T(n/4)

We can put this value in first equation:

    T(n) = 3(3 * T(n/4)) = 3^2 * T(n/2^2)

After k iterations we have:

    T(n) = 3^k * T(n / 2^k)

Every time number of digits in number reduces by factor 2, so it can go as deep as log n, So, k = log n ⇒ n = 2^k

Thus from equation above we have: T(n) = 3^k * T(2^k/2^k)
And then:
T (n) = nlog3 × T(1)

So, T(n) = nlog3 = O(n ^ 1.58)
