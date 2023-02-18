from ..benefit_cost_score import costBenefit

def test_cost_benefit():
        assert(costBenefit(11, 8, 9, 5, 4, 3, 2, 1, 0) == 0.5546218487394958)