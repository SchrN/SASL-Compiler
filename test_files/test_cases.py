# Testcases
from SASL.Driver.Driver import *

# constant
assert compile_from_expr("42") == 42
assert compile_from_expr("true") == "true"
assert compile_from_expr("false") == "false"


# arithmetics
assert compile_from_expr("-42") == -42
assert compile_from_expr("+42") == 42
assert compile_from_expr("40 + 2") == 42
assert compile_from_expr("43 - 1") == 42
assert compile_from_expr("21 * 2") == 42
assert compile_from_expr("126 / 3") == 42


# relops
assert compile_from_expr("42 = 42") == "true"
assert compile_from_expr("42 ~= 42") == "false"
assert compile_from_expr("7 < 3") == "false"
assert compile_from_expr("43 > 42") == "true"
assert compile_from_expr("7 <= 3") == "false"
assert compile_from_expr("42 <= 42") == "true"
assert compile_from_expr("43 >= 42") == "true"
assert compile_from_expr("42 >= 42") == "true"

# bools
assert compile_from_expr("not true") == "false"
assert compile_from_expr("not false") == "true"

assert compile_from_expr("true and true") == "true"
assert compile_from_expr("true and false") == "false"
assert compile_from_expr("false and true") == "false"
assert compile_from_expr("false and false") == "false"

assert compile_from_expr("true or true") == "true"
assert compile_from_expr("false or true") == "true"
assert compile_from_expr("true or false") == "true"
assert compile_from_expr("false or false") == "false"


# defs no args
assert compile_from_expr("def x = 42 . x") == 42
assert compile_from_expr("def x = 22 def y = 20 . x") == 22
assert compile_from_expr("def x = 22 def y = 20 . y") == 20
assert compile_from_expr("def x = 22 def y = 20 . x + y") == 42
assert compile_from_expr("def y = 20 . 22 + y") == 42

# defs with args
assert compile_from_expr("def incr x = x + 1 . incr 41") == 42
assert compile_from_expr("def add x y = x + y . add 18 24") == 42
assert compile_from_expr("def add3 x y z = x + y + z . add3 1 2 3") == 6

# cond
assert (
    compile_from_expr(
        "def my_positive x = if x > 0 then true else false . my_positive 1",
        True,
        True,
        True,
    )
    == "true"
)


# one local def
assert compile_from_expr("x where x = 42") == 42
assert compile_from_expr("x + 3 where x = 39") == 42
assert compile_from_expr("add 3 4 where add x y = x + y") == 7
assert compile_from_expr("incr 41 where incr x = x + 1") == 42

# multiple local defs
assert compile_from_expr("x + 2 where x = 40; y = 2") == 42


# lazy reduction
assert (
    compile_from_expr("def first x y = x def bomb n = bomb(n+1). first 42 (bomb 0)")
    == 42
)

# test Lists
assert compile_from_expr("[1]") == [1]
assert compile_from_expr("hd [1, 2, 3]") == 1
assert compile_from_expr("tl [1, 2, 3, 4]") == [2, 3, 4]

# make sure compile_from_path works too
assert compile_from_path("../SASL_test_files/simple_test.sasl") == 42
