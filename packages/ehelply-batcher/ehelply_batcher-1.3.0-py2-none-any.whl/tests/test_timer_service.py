from ehelply_batcher.tests.simulated_timer_service import SimulatedTimerService


# Max message delay = 2
# Sleep interval = 20
def test_simulation():
    timing_service = SimulatedTimerService(delay_seconds=5)


if __name__ == "__main__":
    test_simulation()