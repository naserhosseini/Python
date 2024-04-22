class Solution:
    def angleClock(self, hour: int, minutes: int) -> float:
        hr = 0 if hour == 12 else hour
        hr_angle = hr * 30 + (minutes / 2)
        mn_angle = minutes * 6
        angle = abs(mn_angle - hr_angle)
        angle = angle if angle < 180 else 360 - angle
        return angle


test = Solution()
print(test.angleClock(hour=1, minutes=57))