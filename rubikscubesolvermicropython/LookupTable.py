
class NoSteps(Exception):
    pass


class LookupTable(object):

    def __init__(self, parent, filename, state_target, linecount, init_width=True):
        self.parent = parent
        self.filename = filename
        self.filename_gz = filename + ".gz"
        self.desc = filename.replace("lookup-table-", "").replace(".txt", "")
        self.linecount = linecount
        assert self.linecount, "%s linecount is %s" % (self, self.linecount)

        # Find the state_width for the entries in our .txt file
        if init_width:
            with open(self.filename, "r") as fh:
                first_line = next(fh)
                self.width = len(first_line)
                (state, steps) = first_line.strip().split(":")
                self.state_width = len(state)
        else:
            self.width = None
            self.state_width = None

        if isinstance(state_target, tuple):
            self.state_target = set(state_target)
        elif isinstance(state_target, list):
            self.state_target = set(state_target)
        elif isinstance(state_target, set):
            self.state_target = state_target
        else:
            self.state_target = set((state_target,))

        self.fh_txt = open(self.filename, mode="r")

    def __str__(self):
        return self.desc

    def get_line(self, line_number):
        self.fh_txt.seek(line_number * self.width)
        line = self.fh_txt.read(self.width)
        return line.rstrip()

    def get_character(self, index):
        self.fh_txt.seek(index)
        return self.fh_txt.read(1)

    def binary_search(self, state_to_find):
        first = 0
        last = self.linecount - 1

        while first <= last:
            midpoint = int((first + last) / 2)
            self.fh_txt.seek(midpoint * self.width)

            # Only read the 'state' part of the line (for speed)
            state = self.fh_txt.read(self.state_width)

            if state_to_find < state:
                last = midpoint - 1

            # If this is the line we are looking for, then read the entire line
            elif state_to_find == state:
                self.fh_txt.seek(midpoint * self.width)
                line = self.fh_txt.read(self.width)
                return line.rstrip()

            else:
                first = midpoint + 1

        return None

    def steps(self, state_to_find):
        """
        Return a list of the steps found in the lookup table for the current cube state
        """
        line = self.binary_search(state_to_find)

        if line:
            (state, steps) = line.strip().split(":")
            # print("state {}, steps {}".format(state, steps))
            steps_list = steps.split()
            return steps_list

        return []

    def solve(self):
        state = self.state()
        # print("%s: solve() state %s vs state_target %s" % (self, state, str(self.state_target)))

        while state not in self.state_target:
            steps = self.steps(state)

            if steps:
                for step in steps:
                    self.parent.rotate(step)
            else:
                raise NoSteps("%s: state %s does not have steps in %s" % (self, state, self.filename))

            state = self.state()
