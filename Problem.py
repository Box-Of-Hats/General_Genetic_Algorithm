import math


class Problem():
    def __init__(self):
        self.parameters = {}

    def bitlist_to_int(self, bitlist, min_value=0, max_value=math.inf):
        """
        Convert a bitlist to an integer.
        e.g [0,1,0,1,1] -> 11
        """
        return min_value + int(int("".join([str(x) for x in bitlist]), 2) % max_value)

    def add_parameter(self, name, option_list):
        """
        Add a parameter to the problems parameter list
        """
        self.parameters[name] = option_list

    def get_bitlist(self, param=None):
        """
        By default, return bitlist for entire problem.
        If a parameter is supplied, simply provide bitlist for that param.
        """
        if param:
            return [0 for i in range((len(self.parameters[param])-1).bit_length())]
        else:
            return [0 for i in range(0, sum([(len(self.parameters[param])-1).bit_length() for param in self.parameters]))]

    def get_score(self, param_values):
        """
        get the score when given values for parameters?
        """
        pass

    def get_parameter_value(self, param_name, index):
        """
        index: either a bitlist or integer that represents an index for a parameter
        """
        if type(index) == int:
            return self.parameters[param_name][index % (len(self.parameters[param_name]))]
        elif type(index) == list:
            index = self.bitlist_to_int(
                index, min_value=0, max_value=len(self.parameters[param_name]))
            return self.parameters[param_name][index % (len(self.parameters[param_name]))]


if __name__ == "__main__":
    cannonball_problem = Problem()
    cannonball_problem.add_parameter("angle", range(0, 181))
    cannonball_problem.add_parameter("power", range(0, 101))

    choices = {
        "angle": 45,
        "power": 100,
    }

    def cannonball_distance(problem, choices):
        g = 9.8  # gravity

        angle = 0
        angle = problem.get_parameter_value("angle", choices["angle"])
        velocity = problem.get_parameter_value("power", choices["power"])
        print("Angle = {}".format(angle))
        print("Velocity = {}".format(velocity))

        angle = math.radians(angle)

        distance_launched = (velocity*velocity * math.sin(2 * angle)) / g
        print("Distance = {}".format(distance_launched))
        if distance_launched <= 0:
            return 0
        else:
            return distance_launched

    cannonball_distance(cannonball_problem, choices)
