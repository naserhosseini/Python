def solution(S, K):
    # write your code in Python 3.6
    days = ['Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat', 'Sun']
    if S not in days:
        return "Please select the day of week from 'Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat', 'Sun'"
    if K  not in range(0,501):
        return "Please select the k from 0 to 500"
    day_no = days.index(S)
    day_add = day_no + K
    day = day_add % 7
    day_week = days[day]
    return day_week


print(solution('Mon',7))