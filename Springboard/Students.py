"""
 Your customer is a school. They want you to write a program that will accept a student's attendance record for a 6-day week and return whether or not a student's attendance is satisfactory.


 The record will be a string containing 6 uppercase characters, representing the student's attendance for each day in the week, Monday through Saturday. The record contains the following three characters only:
 'A' : Absent.
 'L' : Late.
 'P' : Present.


 Within the 6-day week, the attendance is not satisfactory if the student is absent twice or is late more than 2 days in a row.

Return False if 2 A or 3 Lates in a row
Otherwise True


 Examples:
 Input: "PPALLP" This is a string, expected always caps
 Output: True

 Input: "PPALLL"
 Output: False

 Input: "PAPALL"
 Output: False

 Input: "PLPALL"
 Output: True
"""


def satis(status):
    if 'LLL' in status:
        return False
    if status.count('A') >= 2:
        return False
    return True


print(satis('PPALLP'))
print(satis('PPALLL'))
print(satis('PAPALL'))
print(satis('PLPALL'))
