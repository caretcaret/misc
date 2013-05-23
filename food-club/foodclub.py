#!/usr/bin/env python
# -*- encoding: utf-8 -*-

from pprint import pformat
from collections import defaultdict
from copy import deepcopy
from math import log1p


class Round(object):
    def __init__(self, day, max_bet, probability, odds):
        self.day = day
        self.max_bet = max_bet
        self.probability = probability
        self.odds = odds

    def get_probability(self, arena, pirate):
        return self.probability[arena][pirate]

    def get_odds(self, arena, pirate):
        return self.odds[arena][pirate]

    def __repr__(self):
        return "Round(" + str(self.max_bet) + ", " + str(self.probability) + ", " + str(self.odds) + ")"

    def __str__(self):
        return ("Max Bet:\n" + str(self.max_bet) + "\n" +
                "Probabilities:\n" + pformat(self.probability) + "\n" +
                "Odds:\n" + pformat(self.odds) + "\n")


# will automatically suggest the best amount to use given round_.max_bet
class Bet(object):
    def __init__(self, round_, pirates):
        self._round = round_
        self.pirates_tuple = tuple(pirates)
        # convert (4, 3, 2, 1, 0) to (3, 2, 1, 0, None) internally
        self._pirates = [None if pirate == 0 else pirate - 1 for pirate in pirates]
        self.calculate()

    @property
    def round(self):
        return self._round

    @round.setter
    def round(self, round_):
        self._round = round_
        self.calculate()

    @property
    def pirates(self):
        return self._pirates

    @pirates.setter
    def pirates(self, pirates):
        self.pirates_tuple = pirates
        # convert (4, 3, 2, 1, 0) to (3, 2, 1, 0, None) internally
        self._pirates = [None if pirate == 0 else pirate - 1 for pirate in pirates]
        self.calculate()

    def calculate(self):
        self.ratio = reduce(lambda a, b: a * b, [arena_odds[pick] if pick is not None else 1 for pick, arena_odds in zip(self.pirates, self.round.odds)])
        self.amount = min(1000000 // self.ratio, self.round.max_bet)
        self.paid_ratio = float(self.amount) / self.round.max_bet
        self.gross_payout = min(1000000, self.amount * self.ratio)
        self.net_payout = self.gross_payout - self.amount
        self.probability = reduce(lambda a, b: a * b, [arena_probability[pick] if pick is not None else 1.0 for pick, arena_probability in zip(self.pirates, self.round.probability)])
        self.expected_gross = self.probability * self.gross_payout
        self.expected_net = self.expected_gross - self.amount
        self.expected_gross_units = self.expected_gross / self.amount
        self.expected_net_units = self.expected_net / self.amount

    def pirate_in_arena(self, arena):
        return self.pirates[arena]

    def match_results(self, result):
        # result argument is a Bet with the numbers of the winner pirates.
        return [None if pick is None else True if pick == winner else False for pick, winner in zip(self.pirates, result.pirates)]

    def is_winner(self, result):
        return not False in self.match_results(result)

    def __repr__(self):
        return "Bet(" + "<Round object>" + ", " + str(list(self.pirates_tuple)) + ")"

    def __str__(self):
        return str([0 if pirate == None else pirate + 1 for pirate in self.pirates]) + ": " + str(self.amount)

    def __eq__(self, other):
        return self.pirates_tuple == other.pirates_tuple


class BetList(object):
    def __init__(self, bets=None, tag=None):
        if bets is None:
            bets = []
        self._counter = 0
        self.bets = bets
        self.tag = tag

    def truncated(self, length=10):
        return BetList(self.bets[:length])

    def truncate(self, length=10):
        self.bets = self.bets[:length]

    def __iter__(self):
        self._counter = 0
        return self

    def next(self):
        if self._counter >= len(self.bets):
            raise StopIteration
        else:
            self._counter += 1
            return self.bets[self._counter - 1]

    def append(self, item):
        self.bets.append(item)
        return self

    def get(self, other):
        for bet in self.bets:
            if other.pirates_tuple == bet.pirates_tuple:
                return bet
        return None

    def sorted(self, *args, **kwargs):
        return BetList(sorted(self.bets, *args, **kwargs))

    def sort(self, *args, **kwargs):
        self.bets.sort(*args, **kwargs)

    def filter(self, function):
        self.bets = filter(function, self.bets)

    def calculate(self):
        if len(self.bets) == 0:
            return (0, 0, 0, 0, 0)
        self.expected_gross = sum([bet.expected_gross for bet in self.bets])
        self.expected_net = sum([bet.expected_net for bet in self.bets])
        self.paid = sum([bet.amount for bet in self.bets])
        self.expected_gross_units = sum([bet.expected_gross / bet.round.max_bet for bet in self.bets])
        self.paid_units = float(self.paid) / sum([bet.round.max_bet for bet in self.bets]) * len(self.bets)
        self.payout_distribution = self._payout_distribution()
        #self.odds_distribution = self._odds_distribution()
        for payout, probability in self.payout_distribution[::-1]:
            if self.expected_gross < payout:
                self.heuristic = probability * self.expected_net
                break
        else:
            self.heuristic = 0
        self.heuristic2 = self.expected_gross * self.expected_net / self.payout_distribution[0][0]
        return (self.expected_gross, self.expected_net, self.paid, self.expected_gross_units, self.paid_units, self.heuristic, self.heuristic2)

    def calculation_str(self):
        return ("Expected gross: %.2f\n"
                "  Expected net: %.2f\n"
                "          Paid: %d\n"
                "Expected ratio: %.2f : %.2f\n"
                "     Heuristic: %.2f"
                "    Heuristic2: %.2f") % self.calculate()

    def __str__(self):
        header = ("+-------------------------------------------------------------+\n"
                  "|    #   Paid  A  B  C  D  E    Chance    Expected      Ratio |\n"
                  "+-------------------------------------------------------------+\n")
        string_output = ""
        for count, bet in enumerate(self.bets):
            if count % 20 == 0:
                string_output += header
            string_output += "| %4d  %5d  %d  %d  %d  %d  %d  %7.3f%%  %10.2f  %5d : 1 |\n" % ((count + 1, bet.amount) + bet.pirates_tuple + (bet.probability * 100, bet.expected_net, bet.ratio))
        string_output += header
        return string_output

    def __len__(self):
        return len(self.bets)

    @staticmethod
    def all_bets(round_):
        l = [Bet(round_, (a, b, c, d, e)) for a in xrange(5)
                                          for b in xrange(5)
                                          for c in xrange(5)
                                          for d in xrange(5)
                                          for e in xrange(5)]
        l.pop(0)
        return BetList(l)

    @staticmethod
    def all_results(round_):
        return BetList([Bet(round_, (a, b, c, d, e)) for a in xrange(1, 5)
                                                     for b in xrange(1, 5)
                                                     for c in xrange(1, 5)
                                                     for d in xrange(1, 5)
                                                     for e in xrange(1, 5)])

    def _odds_distribution(self):
        if len(self.bets) == 0:
            return [(0, 1.0)]
        odds = defaultdict(int)
        # collect the odds of all winning bets
        for test_result in BetList.all_results(self.bets[0].round):
            for bet in self.bets:
                if bet.is_winner(test_result):
                    odds[test_result] += bet.ratio
                else:
                    odds[test_result] += 0
        # now collect the probabilities of those odds
        distribution = defaultdict(float)
        for result, ratio in odds.iteritems():
            distribution[ratio] += result.probability
        # now collect the cumulative probabilities
        cumulative = defaultdict(float)
        so_far = 0.0
        for ratio in sorted(distribution.iterkeys(), reverse=True):
            so_far += distribution[ratio]
            cumulative[ratio] = so_far
        # now return in sortable manner
        cumulative_list = []
        for key in sorted(cumulative.iterkeys(), reverse=True):
            cumulative_list.append((key, cumulative[key]))
        return cumulative_list

    def _payout_distribution(self):
        if len(self.bets) == 0:
            return [(0, 1.0)]
        payouts = defaultdict(int)
        # collect the payouts of all winning bets
        for test_result in BetList.all_results(self.bets[0].round):
            for bet in self.bets:
                if bet.is_winner(test_result):
                    payouts[test_result] += bet.gross_payout
                else:
                    payouts[test_result] += 0
        # now collect the probabilities of those payouts
        distribution = defaultdict(float)
        for result, payout in payouts.iteritems():
            distribution[payout] += result.probability
        # now collect the cumulative probabilities
        cumulative = defaultdict(float)
        so_far = 0.0
        for payout in sorted(distribution.iterkeys(), reverse=True):
            so_far += distribution[payout]
            cumulative[payout] = so_far
        # now return in sortable manner
        cumulative_list = []
        for key in sorted(cumulative.iterkeys(), reverse=True):
            cumulative_list.append((key, cumulative[key]))
        return cumulative_list

    def daqtools(self):
        html = """<!doctype html><body><form action="http://foodclub.daqtools.info/Bets_Calc1.php" method="POST">
        <input type="hidden" name="requestday" value="%d"><input type="hidden" name="opt" value="CHECKED">
        <input type="hidden" name="safety" value="0">""" % (self.bets[0].round.day + 1)
        for bet_index, bet in enumerate(self.bets, start=1):
            html += """<input type="hidden" name="bet[%d][0]" value="%d">""" % (bet_index, bet.amount)
            for arena_index, pirate in enumerate(bet.pirates_tuple, start=1):
                html += """<input type="hidden" name="bet[%d][%d]" value="%d">""" % (bet_index, arena_index, pirate)
        html += """<input type="submit" value="Submit" name="submit"></body>"""
        with open('out.html', 'w') as f:
            f.write(html)
        import webbrowser
        webbrowser.open('out.html', new=2)
        return self


def highest_expected_net(round_, final=True):
    by_expected_net = BetList.all_bets(round_)
    by_expected_net.filter(lambda bet: bet.expected_net > 0)
    by_expected_net.sort(key=lambda bet: -bet.expected_net)
    if final:
        by_expected_net.truncate(10)
        print "Strategy: Pick bets with highest net expected payout."
        print str(by_expected_net) + by_expected_net.calculation_str()
    return by_expected_net


def highest_probability(round_, final=True):
    by_probability = BetList.all_bets(round_)
    by_probability.filter(lambda bet: bet.expected_net > 0)
    by_probability.sort(key=lambda bet: -bet.probability)
    if final:
        by_probability.truncate(10)
        print "Strategy: Pick bets with highest probability with positive net\nexpected payout."
        print str(by_probability) + by_probability.calculation_str()
    return by_probability


def best_rankings(round_, final=True):
    by_expected_net, by_probability = highest_expected_net(round_, final=False), highest_probability(round_, final=False)
    # tagging each bet with their ranking
    for ranking, bet in enumerate(by_expected_net):
        bet.tag = ranking
    for ranking, bet in enumerate(by_probability):
        bet.tag = ranking
    # consolidating both lists into the by_expected list, adding together their rankings
    for bet in by_probability:
        by_expected_net.get(bet).tag += bet.tag
    by_expected_net.sort(key=lambda bet: bet.tag)
    if final:
        by_expected_net.truncate(10)
        print ("Strategy: Rank probability and expected net payout\n"
               "rankings in parallel and select bets that have the lowest\n"
               "ranking sum.")
        print str(by_expected_net) + by_expected_net.calculation_str()
    return by_expected_net


def rankings_walk(round_, final=True):
    by_expected_net, by_probability = highest_expected_net(round_, final=False), highest_probability(round_, final=False)
    ev_list, p_list = BetList(), BetList()
    output = BetList()
    for x, y in zip(by_expected_net, by_probability):
        if len(output) >= 10:
            break
        if x in p_list:
            output.append(x)
        else:
            ev_list.append(x)
        if len(output) >= 10:
            break
        if y in ev_list:
            output.append(y)
        else:
            p_list.append(y)
    if final:
        print ("Strategy: Walk down probability and expected net payout\n"
               "rankings in parallel and select bets that have appear\n"
               "first in the walk.")
        print str(output) + output.calculation_str()
    return output


def bet_spreading(round_, final=True):
    result = BetList()
    working_round = deepcopy(round_)
    for count in range(10):
        best = Bet(working_round, (0, 0, 0, 0, 0))
        # look for bets with the highest expected net payout
        for bet in BetList.all_bets(working_round):
            if bet in result:
                continue
            if bet.expected_net > best.expected_net:
                best = bet
        # there are no more positive payouts remaining, return the current list
        if best == Bet(working_round, (0, 0, 0, 0, 0)):
            break
        # calculate the probability of pirates winning, assuming that the new bet has lost.
        postprobability = deepcopy(working_round.probability)
        # we only want the arenas selected in our bet, because those are the only arenas in
        # which the probability has changed.
        selected_arenas = [(arena_index, postprobability[arena_index]) for arena_index in range(5) if best.pirate_in_arena(arena_index) is not None]
        # selected_arenas now looks like:
        # [(0, [0.292, 0.370, 0.183, 0.155]),
        #  (1, [0.444, 0.225, 0.225, 0.106])]
        # for each of those arenas,
        for arena_index, arena in selected_arenas:
            # go through each pirate.
            for pirate_index, pirate_probability in enumerate(arena):
                # if the pirate was selected in our bet:
                if pirate_index == best.pirate_in_arena(arena_index):
                    # then the new probability is (the old probability of the pirate - the old probability of the bet)/(1 - the old probability of the bet)
                    postprobability[arena_index][pirate_index] = (pirate_probability - best.probability) / (1 - best.probability)
                # if the pirate was not selected in our bet:
                else:
                    # then the new probability is the old probability of the pirate/(1 - the old probability of the bet)
                    postprobability[arena_index][pirate_index] = pirate_probability / (1 - best.probability)
        # add our best bet to the list with the actual round probabilities
        result.append(Bet(round_, best.pirates_tuple))
        # make our new probability the old one
        working_round.probability = postprobability
    if final == True:
        print ("Place bet 1 with highest expected payout. Using Bayes'\n"
               "rule, calculate the new probabilities of the pirates\n"
               "winning, assuming that the bet failed, in order to\n"
               "spread the bets (the other bets are less likely to\n"
               "repeat the same pirates = safety). Place bet 2 with the\n"
               "new probabilities, with the highest payout. Continue.")
        print str(result) + result.calculation_str()
    return result


def cumulative_highest_heuristic(round_, final=True):
    # resource intensive!
    result = BetList()
    while len(result) < 10:
        best_test_bet = None
        best_heuristic = 0
        for test_bet, test_list in [(test_bet, deepcopy(result).append(test_bet)) for test_bet in BetList.all_bets(round_)]:
            if test_bet in result:
                continue
            test_list.calculate()
            if test_list.heuristic2 > best_heuristic:
                best_test_bet = test_bet
                best_heuristic = test_list.heuristic2
        if best_test_bet is None:
            break
        else:
            result.append(best_test_bet)
    if final == True:
        print ("Assemble all 1-bet lists. Choose the one with the\n"
               "highest heuristic value. Assemble all 2-bet lists\n"
               "including that 1-bet list, get highest heuristic.\n"
               "Repeat.")
        print str(result) + result.calculation_str()
    return result


def highest_utility(round_, final=True):
    # get all bets and calculate their utility:
    # utility = log (1 + bet amount * (odds - 1) / (10 * max bet))
    # sort by probability of bet * utility
    def weighted_utility(bet):
        return bet.probability * log1p(bet.net_payout / (100*round_.max_bet))
    by_utility = BetList.all_bets(round_)
    by_utility.sort(key=weighted_utility, reverse=True)

    if final:
        by_utility.truncate(10)
        print ("Sort bets by weighted utility =\n"
               "prob * log(1 + net payout / (10 * max bet)).")
        print str(by_utility) + by_utility.calculation_str()

    return by_utility

if __name__ == '__main__':
    r4835 = Round(4835, 5276,
                  [[0.292, 0.370, 0.183, 0.155],
                   [0.444, 0.225, 0.225, 0.106],
                   [0.050, 0.292, 0.050, 0.608],
                   [0.050, 0.183, 0.050, 0.717],
                   [0.050, 0.050, 0.850, 0.050]],
                  [[3, 2, 5, 6],
                   [2, 4, 6, 11],
                   [13, 2, 13, 2],
                   [13, 7, 13, 2],
                   [13, 13, 2, 13]])
    r4836 = Round(4836, 5278,
                  [[0.225, 0.080, 0.645, 0.050],
                   [0.050, 0.363, 0.363, 0.225],
                   [0.155, 0.134, 0.118, 0.593],
                   [0.155, 0.080, 0.155, 0.610],
                   [0.050, 0.850, 0.050, 0.050]],
                  [[4, 13, 2, 13],
                   [13, 2, 2, 4],
                   [9, 9, 12, 2],
                   [9, 13, 9, 2],
                   [13, 2, 13, 13]])
    r4837 = Round(4837, 5280,
                  [[0.05000, 0.18333, 0.63274, 0.13393],
                   [0.05000, 0.05000, 0.45000, 0.45000],
                   [0.18333, 0.05000, 0.47500, 0.29167],
                   [0.18333, 0.29167, 0.15476, 0.37024],
                   [0.08712, 0.18333, 0.05000, 0.67955]],
                  [[13, 7, 2, 9],
                   [13, 13, 2, 2],
                   [6, 13, 2, 3],
                   [5, 3, 6, 2],
                   [13, 7, 13, 2]])
    r4838 = Round(4838, 5282,
                  [[0.450, 0.050, 0.450, 0.050],
                   [0.218, 0.218, 0.282, 0.282],
                   [0.487, 0.134, 0.087, 0.292],
                   [0.080, 0.645, 0.050, 0.225],
                   [0.080, 0.225, 0.155, 0.540]],
                  [[2, 13, 2, 13],
                   [4, 4, 3, 3],
                   [2, 9, 13, 3],
                   [13, 2, 13, 3],
                   [13, 5, 7, 2]])
    r4839 = Round(4839, 5284,
                  [[0.433, 0.050, 0.292, 0.225],
                   [0.301, 0.098, 0.301, 0.301],
                   [0.292, 0.183, 0.342, 0.183],
                   [0.118, 0.397, 0.087, 0.397],
                   [0.080, 0.155, 0.225, 0.540]],
                  [[2, 13, 3, 5],
                   [2, 12, 3, 4],
                   [3, 6, 2, 7],
                   [10, 2, 13, 2],
                   [13, 9, 6, 2]])
    r4840 = Round(4840, 5286,
                  [[0.367, 0.292, 0.050, 0.292],
                   [0.050, 0.050, 0.225, 0.675],
                   [0.080, 0.183, 0.080, 0.656],
                   [0.225, 0.050, 0.050, 0.675],
                   [0.080, 0.183, 0.603, 0.134]],
                  [[2, 3, 13, 3],
                   [13, 13, 5, 2],
                   [13, 7, 13, 2],
                   [4, 13, 13, 2],
                   [13, 7, 2, 9]])
    r4841 = Round(4841, 5288,
                  [[.282, .218, .282, .218],
                   [.095, .050, .427, .427],
                   [.080, .095, .599, .225],
                   [.225, .134, .416, .225],
                   [.050, .050, .050, .850]],
                  [[3, 4, 3, 5],
                   [10, 13, 2, 2],
                   [13, 12, 2, 4],
                   [6, 9, 2, 6],
                   [13, 13, 13, 2]])
    r4842 = Round(4842, 5290,
                  [[.155, .225, .333, .287],
                   [.578, .050, .292, .080],
                   [.675, .050, .050, .225],
                   [.155, .080, .183, .582],
                   [.183, .118, .183, .515]],
                  [[6, 5, 2, 3],
                   [2, 13, 3, 12],
                   [2, 13, 13, 6],
                   [9, 13, 7, 2],
                   [7, 12, 7, 2]])
    r4843 = Round(4843, 5292,
                  [[.292, .050, .050, .608],
                   [.292, .095, .225, .388],
                   [.134, .507, .225, .134],
                   [.050, .292, .524, .134],
                   [.050, .433, .292, .225]],
                  [[3, 13, 13, 2],
                   [2, 12, 5, 2],
                   [10, 2, 6, 10],
                   [13, 3, 2, 8],
                   [13, 2, 3, 5]])
    r4844 = Round(4844, 5294,
                  [[.292, .367, .292, .050],
                   [.134, .134, .292, .440],
                   [.050, .225, .292, .433],
                   [.155, .050, .134, .661],
                   [.774, .050, .095, .080]],
                  [[3, 2, 3, 13],
                   [7, 7, 3, 2],
                   [13, 4, 3, 2],
                   [9, 13, 9, 2],
                   [2, 13, 13, 13]])
    r4845 = Round(4845, 5296,
                  [[.608, .050, .292, .050],
                   [.287, .333, .155, .225],
                   [.183, .292, .370, .155],
                   [.183, .419, .106, .292],
                   [.118, .134, .614, .134]],
                  [[2, 13, 2, 13],
                   [3, 2, 6, 5],
                   [6, 3, 2, 7],
                   [6, 2, 9, 3],
                   [12, 10, 2, 10]])
    r4846 = Round(4846, 5298,
                  [[.087, .134, .487, .292],
                   [.134, .408, .408, .050],
                   [.225, .050, .542, .183],
                   [.155, .080, .582, .183],
                   [.050, .155, .050, .745]],
                  [[12, 7, 2, 3],
                   [7, 2, 2, 13],
                   [4, 13, 2, 7],
                   [7, 13, 2, 7],
                   [13, 9, 13, 2]])
    r4935 = Round(4935, 5476,
                  [[.183, .050, .717, .050],
                   [.118, .292, .407, .183],
                   [.183, .050, .183, .583],
                   [.183, .596, .134, .087],
                   [.183, .134, .095, .587]],
                  [[7, 13, 2, 13],
                   [8, 3, 2, 6],
                   [6, 13, 7, 2],
                   [7, 2, 10, 13],
                   [7, 9, 13, 2]])
    current_round = r4839
    highest_expected_net(current_round)
    best_rankings(current_round).daqtools()
    rankings_walk(current_round)
    highest_probability(current_round)
    highest_utility(current_round).daqtools()
    #cumulative_highest_heuristic(current_round)
