import unittest

from social_distancing_sim.agent.basic_agents.vaccination_agent import VaccinationAgent
from social_distancing_sim.environment.disease import Disease
from social_distancing_sim.environment.environment import Environment
from social_distancing_sim.environment.environment_plotting import EnvironmentPlotting
from social_distancing_sim.environment.graph import Graph
from social_distancing_sim.environment.healthcare import Healthcare
from social_distancing_sim.environment.observation_space import ObservationSpace
from social_distancing_sim.sim.sim import Sim

import os
import shutil


class TestSim(unittest.TestCase):

    def setUp(self):
        self._to_delete = None

    def tearDown(self):
        if self._to_delete is not None:
            shutil.rmtree(self._to_delete, ignore_errors=True)

    def test_default_sim_run(self):
        pop = Environment(disease=Disease(),
                          healthcare=Healthcare(),
                          observation_space=ObservationSpace(graph=Graph()))

        sim = Sim(env=pop,
                  agent=VaccinationAgent(),
                  plot=False,
                  save=False)

        sim.run()

    def test_example_sim_run(self):
        seed = 123

        pop = Environment(name="agent example environment 1",
                          disease=Disease(name='COVID-19',
                                          virulence=0.01,
                                          seed=seed,
                                          immunity_mean=0.95,
                                          immunity_decay_mean=0.05),
                          healthcare=Healthcare(capacity=5),
                          observation_space=ObservationSpace(graph=Graph(community_n=15,
                                                                         community_size_mean=10,
                                                                         seed=seed + 1),
                                                             test_rate=1,
                                                             seed=seed + 2),
                          seed=seed + 3,
                          environment_plotting=EnvironmentPlotting(ts_fields_g2=["Score", "Action cost",
                                                                                 "Overall score"],
                                                                   ts_obs_fields_g2=["Observed Score", "Action cost",
                                                                                     "Observed overall score"]))

        sim = Sim(env=pop,
                  agent=VaccinationAgent(actions_per_turn=25,
                                         seed=seed),
                  plot=False,
                  save=False)

        sim.run()

        self._to_delete = pop.name

    def test_example_sim_run_with_plotting(self):

        seed = 123

        pop = Environment(name="agent example environment 2",
                          disease=Disease(name='COVID-19',
                                          virulence=0.01,
                                          seed=seed,
                                          immunity_mean=0.95,
                                          immunity_decay_mean=0.05),
                          healthcare=Healthcare(capacity=5),
                          observation_space=ObservationSpace(graph=Graph(community_n=15,
                                                                         community_size_mean=10,
                                                                         seed=seed + 1),
                                                             test_rate=1,
                                                             seed=seed + 2),
                          seed=seed + 3,
                          environment_plotting=EnvironmentPlotting(ts_fields_g2=["Score", "Action cost",
                                                                                 "Overall score"],
                                                                   ts_obs_fields_g2=["Observed Score",
                                                                                     "Action cost",
                                                                                     "Observed overall score"]))

        sim = Sim(env=pop,
                  n_steps=3,
                  agent=VaccinationAgent(actions_per_turn=25,
                                         seed=seed),
                  plot=False,
                  save=True)

        sim.run()
        sim.env.replay()
        self._to_delete = pop.name

    def test_example_sim_run_with_extra_plotting(self):
        seed = 123

        pop = Environment(name="agent example environment 3",
                          disease=Disease(name='COVID-19',
                                          virulence=0.01,
                                          seed=seed,
                                          immunity_mean=0.95,
                                          immunity_decay_mean=0.05),
                          healthcare=Healthcare(capacity=5),
                          observation_space=ObservationSpace(graph=Graph(community_n=15,
                                                                         community_size_mean=10,
                                                                         seed=seed + 1),
                                                             test_rate=1,
                                                             seed=seed + 2),
                          seed=seed + 3,
                          environment_plotting=EnvironmentPlotting(ts_fields_g2=["Score", "Action cost",
                                                                                 "Overall score"],
                                                                   ts_obs_fields_g2=["Observed Score",
                                                                                     "Action cost",
                                                                                     "Observed overall score"]))

        sim = Sim(env=pop,
                  n_steps=3,
                  agent=VaccinationAgent(actions_per_turn=25,
                                         seed=seed),
                  plot=False,
                  save=True)

        sim.run()
        sim.env.replay()
        self._to_delete = pop.name

    def test_example_sim_run_with_all_plotting(self):
        seed = 123

        pop = Environment(name="agent example environment 4",
                          disease=Disease(name='COVID-19',
                                          virulence=0.01,
                                          seed=seed,
                                          immunity_mean=0.95,
                                          immunity_decay_mean=0.05),
                          healthcare=Healthcare(capacity=5),
                          observation_space=ObservationSpace(graph=Graph(community_n=15,
                                                                         community_size_mean=10,
                                                                         seed=seed + 1),
                                                             test_rate=0.1,
                                                             seed=seed + 2),
                          seed=seed + 3,
                          environment_plotting=EnvironmentPlotting(ts_fields_g2=["Score", "Action cost",
                                                                                 "Overall score"],
                                                                   ts_obs_fields_g2=["Observed Score",
                                                                                     "Action cost",
                                                                                     "Observed overall score"]))

        sim = Sim(env=pop,
                  n_steps=3,
                  agent=VaccinationAgent(actions_per_turn=25,
                                         seed=seed),
                  plot=False,
                  save=True)

        sim.run()
        sim.env.replay()
        self._to_delete = pop.name

