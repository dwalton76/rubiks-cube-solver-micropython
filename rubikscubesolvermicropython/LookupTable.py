import logging


log = logging.getLogger(__name__)


class NoSteps(Exception):
    pass


class LookupTable(object):

    def __init__(self, parent, filename, state_target, linecount):
        self.parent = parent
        self.filename = filename
        self.filename_gz = filename + ".gz"
        self.desc = filename.replace("lookup-table-", "").replace(".txt", "")
        self.linecount = linecount
        assert self.linecount, "%s linecount is %s" % (self, self.linecount)

        # Find the state_width for the entries in our .txt file
        with open(self.filename, "r") as fh:
            first_line = next(fh)
            self.width = len(first_line)
            (state, steps) = first_line.strip().split(":")
            self.state_width = len(state)

        if isinstance(state_target, tuple):
            self.state_target = set(state_target)
        elif isinstance(state_target, list):
            self.state_target = set(state_target)
        elif isinstance(state_target, set):
            self.state_target = state_target
        else:
            self.state_target = set((state_target,))

        # 'rb' mode is about 3x faster than 'r' mode
        self.fh_txt = open(self.filename, mode="rb")

    def __str__(self):
        return self.desc

    def binary_search(self, state_to_find):
        first = 0
        last = self.linecount - 1
        state_to_find = bytes(state_to_find, encoding="utf-8")

        while first <= last:
            midpoint = int((first + last) / 2)
            self.fh_txt.seek(midpoint * self.width)

            # Only read the 'state' part of the line (for speed)
            b_state = self.fh_txt.read(self.state_width)

            if state_to_find < b_state:
                last = midpoint - 1

            # If this is the line we are looking for, then read the entire line
            elif state_to_find == b_state:
                self.fh_txt.seek(midpoint * self.width)
                line = self.fh_txt.read(self.width)
                return line.decode("utf-8").rstrip()

            else:
                first = midpoint + 1

        return None

    def steps(self, state_to_find=None):
        """
        Return a list of the steps found in the lookup table for the current cube state
        """
        assert state_to_find

        # If we are at one of our state_targets we do not need to do anything
        if state_to_find in self.state_target:
            return None

        line = self.binary_search(state_to_find)

        if line:
            (state, steps) = line.strip().split(":")
            steps_list = steps.split()
            return steps_list

        return None

    def steps_cost(self, state_to_find):
        steps = self.steps(state_to_find)

        if steps is None:
            # log.info("%s: steps_cost None for %s (stage_target)" % (self, state_to_find))
            return 0
        else:
            # log.info("%s: steps_cost %d for %s (%s)" % (self, len(steps), state_to_find, ' '.join(steps)))
            return len(steps)

    def solve(self):

        if "TBD" in self.state_target:
            tbd = True
        else:
            tbd = False

        while True:
            state = self.state()

            if tbd:
                log.info(
                    "%s: solve() state %s vs state_target %s"
                    % (self, state, str(self.state_target))
                )

            if state in self.state_target:
                break

            steps = self.steps(state)

            if steps:
                for step in steps:
                    self.parent.rotate(step)
            else:
                raise NoSteps("%s: state %s does not have steps" % (self, state))
