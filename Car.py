import pigpio


class Car():
    def __init__(self):
        self.pi2 = pigpio.pi()
        self.pi2.set_mode(18, pigpio.OUTPUT)

    def turn(self, num):
        print("num:", num)
        try:
                set = int(float(num)*1000)
                print("servo gets:", set)
        except ValueError:
                set = 70000

        if set < 61000:
            self.pi2.hardware_PWM(18, 50, 61000)

        elif set > 80000:
            self.pi2.hardware_PWM(18, 50, 80000)

        else:
            self.pi2.hardware_PWM(18, 50, set)

    def setSpeed(self, pow):
        pi2 = self.pi2
        if pow >= 0:
            direction = "forw"

        elif pow < 0:
            direction = "backw"

        pow = abs(pow)
        if pow > 90:
            # change direction to numbers then use the numbers here instread of direction in strings
            if direction == "forw":
                pi2.write(27, 1)
                pi2.write(22, 0)
                pi2.write(5, 1)
                pi2.write(6, 0)

            elif direction == "backw":
                pi2.write(27, 0)
                pi2.write(22, 1)
                pi2.write(5, 0)
                pi2.write(6, 1)

            pi2.set_mode(20, pigpio.OUTPUT)
            pi2.set_mode(21, pigpio.OUTPUT)

            pi2.set_PWM_dutycycle(20, pow)
            pi2.set_PWM_dutycycle(21, pow)

        else:
            pi2.write(27, 0)
            pi2.write(22, 0)
            pi2.write(5, 0)
            pi2.write(6, 0)

            pi2.set_mode(20, pigpio.OUTPUT)
            pi2.set_mode(21, pigpio.OUTPUT)

            pi2.set_PWM_dutycycle(20, 0)
            pi2.set_PWM_dutycycle(21, 0)

    def stop(self):
        pi2 = self.pi2
        pi2.write(27, 0)
        pi2.write(22, 0)
        pi2.write(5, 0)
        pi2.write(6, 0)

        pi2.set_mode(20, pigpio.OUTPUT)
        pi2.set_mode(21, pigpio.OUTPUT)

        pi2.set_PWM_dutycycle(20, 0)
        pi2.set_PWM_dutycycle(21, 0)
