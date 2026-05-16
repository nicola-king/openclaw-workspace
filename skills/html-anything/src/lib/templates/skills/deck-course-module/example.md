CS 101 · MODULE 04

# Recursion: solving problems by *calling yourself*.

In this module you'll learn why a function that calls itself is not a trick, but the most natural way to describe problems that contain smaller copies of themselves.

~ 45 min read
prereq · functions, if/else
lang · Python

Dr. A. Rivera · Spring 2026

CS 101 · M04

##### Learning objectives

* Define recursion
* Identify a base case
* Trace a recursive call
* Convert loop ↔ recursion
* Recognize when recursion helps

##### Module progress

Page 2 of 7 · ~5 min in

OBJECTIVES

## By the end, you will be able to…

#### ① Explain recursion in one sentence.

"A function that solves a problem by calling itself on a smaller version of that problem."

#### ② Write a base case that always terminates.

Every recursive function must have an exit door, or it runs forever.

#### ③ Trace a call stack on paper.

Given `fact(4)`, draw the stack frames top-to-bottom.

#### ④ Convert a while-loop to a recursive equivalent.

And explain when one is clearer than the other.

CS 101 · M04

##### Learning objectives

* Define recursion
* Identify a base case
* Trace a recursive call
* Convert loop ↔ recursion
* Recognize when recursion helps

##### Key terms

base case · recursive case · call stack · tail call

CORE CONCEPT

## Two parts, always.

A recursive function has exactly two things inside it: a **base case** (when to stop) and a **recursive case** (how to shrink the problem before calling yourself).

**Rule of thumb.** If you can't name the base case out loud, don't write the recursion yet. Draw it on paper first.

#### Base case

The smallest possible input — one the function answers directly, without calling itself.

e.g. **n == 0**

#### Recursive case

Every other input — delegate to a smaller version of the same problem.

e.g. **n × fact(n-1)**

CS 101 · M04

##### Learning objectives

* Define recursion
* Identify a base case
* Trace a recursive call
* Convert loop ↔ recursion
* Recognize when recursion helps

##### Try it yourself

Open repl.it and run the code on the right. Then try `fact(10)`.

WORKED EXAMPLE

## Factorial, 7 lines.

```
# fact(n) = n × (n-1) × … × 1,  and fact(0) = 1
def fact(n):
    if n == 0:          # base case
        return 1
    return n * fact(n - 1)   # recursive case

print(fact(4))   # → 24
```

**Trace fact(4).** 4 × fact(3) → 4 × (3 × fact(2)) → 4 × 3 × (2 × fact(1)) → 4 × 3 × 2 × 1 × fact(0) → 4 × 3 × 2 × 1 × 1 = **24**.

CS 101 · M04

##### Learning objectives

* Define recursion
* Identify a base case
* Trace a recursive call
* Convert loop ↔ recursion
* Recognize when recursion helps

##### Time

~10 minutes · solo

EXERCISE 4.1

## Write *sum\_to(n)*.

Return `1 + 2 + … + n` using recursion — no loops allowed.

**Your task**

1. Write the base case. What does `sum_to(0)` return?
2. Write the recursive case in terms of `sum_to(n - 1)`.
3. Test it: `sum_to(5) == 15`, `sum_to(10) == 55`.
4. Bonus: what happens if you call `sum_to(-3)`? Fix it.

Stuck? Remember: a base case is the smallest input you already know the answer to.

CS 101 · M04

##### Learning objectives

* Define recursion
* Identify a base case
* Trace a recursive call
* Convert loop ↔ recursion
* Recognize when recursion helps

##### Self-assess

You should get 3/3.

CHECK YOUR UNDERSTANDING

## Which function will recurse forever?

A

**def f(n): return 1 if n == 0 else n \* f(n - 1)**

Base case `n == 0`, shrinks toward it. Terminates.

B

**def f(n): return n + f(n + 1)**

**✓ Correct.** No base case, and `n` grows — infinite recursion.

C

**def f(n): return n if n < 2 else f(n - 1) + f(n - 2)**

Classic Fibonacci. Base case on `n < 2`. Terminates.

SUMMARY · MODULE 04

# You can now…

#### ✓ Define recursion

A function that calls itself on a smaller input.

#### ✓ Write a safe base case

Every recursion needs an exit door.

#### ✓ Trace a call stack

You can unwind `fact(4)` by hand.

#### ✓ Judge when to use it

Trees and self-similar problems → recursion. Flat iteration → loop.

**Up next · Module 05.** Divide & conquer: merge sort. We'll use everything you just learned — but on lists, not numbers.