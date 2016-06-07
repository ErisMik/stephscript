def FIBO ( n ) :
    if n == 1 or n == 2 :
        return 1
    return FIBO ( n - 1 ) + FIBO ( n - 2 )
print FIBO ( 99 )