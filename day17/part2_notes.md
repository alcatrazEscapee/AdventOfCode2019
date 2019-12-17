
Key Notes:
 - robot starts facing up
 - turns are relative, not absolute (forgot this the first time around)
 - main function can only call subroutines, not additional move commands

Robot Program:
```
                 11111111112
        12345678901234567890
Main:   A,A,B,B,C,B,C,B,C,A
A:      L,10,L,10,R,6
B:      R,12,L,12,L,12
C:      L,6,L,10,R,12,R,12
```

Actual path:

```
A   L,10
    L,10
    R,6
A   L,10
    L,10 
    R,6
B   R,12
    L,12
    L,12
B   R,12
    L,12
    L,12
C   L,6
    L,10
    R,12
    R,12
B   R,12
    L,12
    L,12
C   L,6
    L,10
    R,12
    R,12
B   R,12
    L,12
    L,12
C   L,6
    L,10
    R,12
    R,12
A   L,10
    L,10
    R,6
```