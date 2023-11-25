from matplotlib import pyplot as plt
from abc import ABC, abstractmethod
import random
import copy
import sys
from time import sleep


class Unbuffered(object):
    """This automatically makes the python program run unbuffered, across platforms ensuring the print statements
    output as intended."""

    def __init__(self, stream):
        self.stream = stream

    def write(self, data):
        self.stream.write(data)
        self.stream.flush()

    def writelines(self, data):
        self.stream.writelines(data)
        self.stream.flush()

    def __getattr__(self, attr):
        return getattr(self.stream, attr)


class News:
    """The News class represents the news objects that will be distributed and consumed."""

    # class attributes for tracking how often real and fakes news were distributed
    fake_distribution_count = 0
    real_distribution_count = 0

    # dictionary of all news instances
    news_media = {}
    fake_news_count = 0

    def __init__(self, uid, is_fake, polarization, credibility):
        self.uid = uid
        self._is_fake = is_fake
        self._polarization = polarization
        self._alignment = "Left" if self._polarization <= 5 else "Right"
        self.credibility = credibility
        self.distributed_count = 0
        News.news_media[self.uid] = self

    def __str__(self):
        return f"ID: {self.uid}; is_fake: {self.is_fake}; " \
               f"polarization: {self.polarization}; credibility: {self.credibility}"

    @classmethod
    def track_distribution(cls, news):
        if news.is_fake:
            News.fake_distribution_count += 1
        else:
            News.real_distribution_count += 1

    @property
    def is_fake(self):
        return self._is_fake

    @property
    def polarization(self):
        return self._polarization

    @property
    def alignment(self):
        return self._alignment


# abstract base class
class Distributor(ABC):
    """The Distributor class is an abstract base class for the Media and Person classes and represents
    objects which distribute news in some manner."""

    fakes_shared = 0
    real_shared = 0

    def __init__(self, uid, polarization, credibility):
        self.uid = uid
        self.polarization = polarization
        self.credibility = credibility
        super().__init__()

    @abstractmethod
    def distribute(self):
        pass

    @classmethod
    def track_news_shared(cls, news):
        # Tracks fake and real news shared
        if news.is_fake:
            cls.fakes_shared += 1
        else:
            cls.real_shared += 1


class Media(Distributor):
    """The Media class represents news/media distributors.
    These media distributors distribute the news objects to the person objects."""

    num_rounds = 0
    news_uid = 1
    extreme = set()
    moderate = set()
    weak = set()

    # dictionary of all media distributor instances
    media = {}

    # The distributions determine the classification of how polarized a media distributor is
    weak_pol_dist = {4, 5, 6, 7}
    moderate_pol_dist = {2, 3, 8, 9}
    extreme_pol_dist = {1, 10}

    def __init__(self, uid, polarization, credibility):
        super().__init__(uid, polarization, credibility)
        self.news = set()
        self.dist_network = set()
        self._fake_news_quantity = 0
        self._real_news_quantity = 0
        self._num_news = 0
        self._news_per_round = 0
        self.add_distributor()

    def __str__(self):
        return f"ID: {self.uid}; pol_dist: {self.polarization}; credibility: {self.credibility}"

    def add_distributor(self):
        Media.media[self.uid] = self

        # Determines polarization categorization
        if self.polarization in Media.extreme_pol_dist:
            Media.extreme.add(self.uid)
        elif self.polarization in Media.moderate_pol_dist:
            Media.moderate.add(self.uid)
        else:
            Media.weak.add(self.uid)

    def add_person(self, person):
        self.dist_network.add(person.uid)

    def add_news(self, news):
        self.news.add(news)

    @property
    def fake_news_quantity(self):
        return self._fake_news_quantity

    @fake_news_quantity.setter
    def fake_news_quantity(self, fake_news_batch):
        self._fake_news_quantity = fake_news_batch

    @property
    def real_news_quantity(self):
        return self._real_news_quantity

    @real_news_quantity.setter
    def real_news_quantity(self, real_news_batch):
        self._real_news_quantity = real_news_batch

    @property
    def num_news(self):
        return self._num_news

    @num_news.setter
    def num_news(self, num):
        self._num_news = num

    @property
    def news_per_round(self):
        return self._news_per_round

    @news_per_round.setter
    def news_per_round(self, num):
        self._news_per_round = num

    def create_news(self, fake_news_batch, real_news_batch):
        """Creates all of the news objects for a given distributor"""

        # batch sizes are determined by types of distributors randomly generated
        self.fake_news_quantity = fake_news_batch
        self.real_news_quantity = real_news_batch
        self.num_news = self.real_news_quantity + self.fake_news_quantity
        self.news_per_round = int(self.num_news // Media.num_rounds)

        for x in range(self.fake_news_quantity):
            News(Media.news_uid, True, self.polarization, self.credibility)
            self.add_news(Media.news_uid)
            Media.news_uid += 1
            News.fake_news_count += 1
        for x in range(self.real_news_quantity):
            News(Media.news_uid, False, self.polarization, self.credibility)
            self.add_news(Media.news_uid)
            Media.news_uid += 1

    def distribute(self):
        """"Distributes news to every person in distribution network.
        The amount distributed is calculated based on the amount of news and the number of rounds."""

        count = 0
        while count <= self.news_per_round and self.news:
            news = News.news_media[self.news.pop()]
            for person_uid in self.dist_network:
                person = Person.persons[person_uid]
                person.add_to_newsfeed(news)
                News.track_distribution(news)
                self.track_news_shared(news)
            count += 1


class Person(Distributor):
    """Person is a subclass of distributor as they are able to distribute news as well,
    but are limited to distributing within their networks.
    Person have certain other attributes that determine how much news they consume and what they believe."""

    # Dictionary of all person objects
    persons = {}

    # Tracks belief in news
    fake_news_belief = 0
    real_news_belief = 0

    def __init__(self, uid, polarization, credibility, consumption_pref):
        super().__init__(uid, polarization, credibility)
        self.alignment = "Left" if self.polarization <= 5 else "Right"
        self.consumption_pref = consumption_pref
        self.dist_network = []
        self.newsfeed = []
        self.news_to_share = []
        self.news_consumed = {}
        Person.persons[self.uid] = self

    def __str__(self):
        return f"ID: {self.uid}; polarization: {self.polarization}; " \
               f"credibility: {self.credibility}; consumption_pref: {self.consumption_pref}"

    @classmethod
    def track_belief(cls, news):
        """This method adjusts the tracker for belief in real and fake news."""

        if news.is_fake:
            cls.fake_news_belief += 1

        else:
            cls.real_news_belief += 1

    def add_network(self, network_uid):
        """Adds all the networks the person is a part of to a list for news re-distribution."""

        self.dist_network.append(network_uid)

    def add_to_newsfeed(self, news):
        """Adds a news article to a person's newsfeed for consumption."""

        self.newsfeed.append(news.uid)

    def adjust_polarization(self, news):
        """Determines how much a person's polarization adjusts based on the news article believed. Similarities in
        alignment and polarization lead to stronger changes in polarization."""

        adjust_belief_probability = random.randint(1, 10)

        if news.alignment == "Left" and self.alignment == "Left":

            if self.polarization < news.polarization:
                if adjust_belief_probability >= 8:
                    self.polarization = random.randint(self.polarization, news.polarization)

            elif self.polarization > news.polarization:
                if adjust_belief_probability >= 6:
                    self.polarization = random.randint(news.polarization, self.polarization)

        elif news.alignment == "Right" and self.alignment == "Right":

            if self.polarization > news.polarization:
                if adjust_belief_probability >= 8:
                    self.polarization = random.randint(news.polarization, self.polarization)
            elif self.polarization < news.polarization:
                if adjust_belief_probability >= 6:
                    self.polarization = random.randint(self.polarization, news.polarization)
        else:

            lower_bound = min(self.polarization, news.polarization)
            upper_bound = max(self.polarization, news.polarization)

            if adjust_belief_probability >= 2:
                self.polarization = random.randint(lower_bound, upper_bound)

        if self.polarization >= 6:
            self.alignment = "Right"

        else:
            self.alignment = "Left"

    def consume(self):
        """This method represents a person's news consumption. It factors in a person's consumption preferences
        and the polarization and alignment of both the person and the news article to determine what actions take place:
        consume, belief, and redistribution."""

        amount_to_consume = self.consumption_pref + random.randint(-1, 1)
        for _ in range(amount_to_consume):
            if self.newsfeed:
                news = News.news_media[self.newsfeed.pop()]

                # This section determines whether the person believes an article.
                # People are more likely to believe if their alignment is the same as the news article.
                if self.alignment == news.alignment:

                    # If people are weakly aligned with news, their belief in the credibility increases only slightly.
                    if abs(self.polarization - news.polarization) >= 2:
                        pov_credibility = news.credibility + 4

                    # If people are perfectly aligned with news, they will believe the news.
                    elif self.polarization == news.polarization:
                        pov_credibility = 10

                    # If people are strongly aligned with news, their belief increases dramatically.
                    else:
                        pov_credibility = news.credibility + 7

                # If people aren't aligned, their beliefs decrease
                else:

                    # If people aren't aligned and their polarization is too disparate, they won't believe the news.
                    if abs(self.polarization - news.polarization) >= 4:
                        pov_credibility = 0

                    # If people are somewhat close on the spectrum, the news will lose a moderate amount of credibility.
                    elif abs(self.polarization - news.polarization) == 3:
                        pov_credibility = news.credibility - 3

                    # If people are close on the spectrum, the news credibility only drops a bit.
                    else:
                        pov_credibility = news.credibility - 1

                if pov_credibility >= 9:
                    believed = True

                    # A person will share if the news is completely credible in their eyes.
                    self.news_to_share.append(news.uid)

                elif pov_credibility >= 6:
                    believed = True

                    likelihood_to_share = random.randint(1, 10)

                    # A person is moderately likely to share article if news is moderately credible in their eyes.
                    if likelihood_to_share > 5:
                        self.news_to_share.append(news.uid)

                elif pov_credibility >= 4:
                    # If the news is somewhat credible, people may or not believe it.
                    believed = random.choice((False, True))

                else:
                    believed = False

                # The consequences of belief or disbelief
                if believed:
                    self.adjust_polarization(news)
                    self.news_consumed[news.uid] = True
                    Person.track_belief(news)
                else:
                    self.news_consumed[news.uid] = False

            else:
                break

    def distribute(self):
        """This distribute method represents peer-to-peer distribution. A person only shares news articles with a select
        few in their network."""

        for _ in range(len(self.news_to_share)):
            network = Network.networks[random.choice(self.dist_network)]
            person_uid = random.choice(network.persons)

            # checks to make sure the person chosen from the network isn't the same person
            while person_uid == self.uid:
                person_uid = random.choice(network.persons)

            person = Person.persons[person_uid]
            news = News.news_media[self.news_to_share.pop()]
            person.add_to_newsfeed(news)
            News.track_distribution(news)
            person.track_news_shared(news)


class Network:
    """The network class is a composition of Persons and determines who persons interact with.
    It will be created semi-randomly based on the amount of networks the user wishes to create
    and have users randomly assigned into each network."""

    # keeps track of all network instances
    networks = {}

    def __init__(self, uid):
        self.uid = uid
        self.persons = []
        self.size = len(self.persons)
        Network.networks[self.uid] = self

    def __str__(self):
        return f"ID: {self.uid}; size: {self.size}"

    def add_person(self, person):
        """Keeps track of all persons in a particular network."""

        self.persons.append(person.uid)


class Simulator:
    """Simulator is the main class of the program.
    It acts as the user interface and will be used to create all of the objects based on the input parameters,
    run the simulation, graph the results, and display the results."""

    sys.stdout = Unbuffered(sys.stdout)

    welcome = ["I'm gonna ask you for a few parameters and then perform some behind the scenes magic, run the "
               "the simulation, and show you your results. Exciting right?!? \n", "A few other notes:",
               "Our simulation focuses heavily on the effects of polarization.",
               "Media distributors will distribute media that reflects their polarization and people distributors "
               "will do the same with their networks.",
               "Though these distribution networks aren't homogenous.",
               "Lastly, highly polarized media distributors are more likely to share fake news.",
               "If you want more details, check out or simulation flow diagram and model assumptions documents. \n",
               "Enough of my yapping, let's start simulating!\n"]

    ranges = {"Media": (3, 50), "People": (500, 2000), "News": (500, 5000),
              "Fake": (5, 95), "Networks": (10, 100), "Time": (5, 25)}

    def __init__(self):
        self.is_error = False
        self.sim_history = {"Weeks": [], "Fake News Belief": [], "Real News Distributed": [],
                            "Fake News Distributed": [], "Media Fake News Shared": [],
                            "Media Real News Shared": [], "Peer to Peer Fake News Shared": [],
                            "Peer to Peer Real News Shared": []}

        # Prints out welcome message in a readable manner if the user is new
        print("Hi there! My name is Simmothy and I simulate fake news distribution. \n")
        greet = input("Would you like some information about the simulation before getting started (Y or N)?:  ")
        if greet.upper() == "Y":
            print("\nHere the gist:\n")
            sleep(1)
            for line in Simulator.welcome:
                print(line)
                sleep(4)
        else:
            print("\nLet's get started then! \n")
            sleep(1)

        # The next stages take in a user input and check if the input is acceptable.
        # It is broken out so the user doesn't have to restart the whole process if they enter an incorrect input.
        stage = "Media"
        low, high = Simulator.ranges[stage]
        self.num_media = 0
        while self.num_media == 0:
            user_input = input(f"Please enter the number ({low} - {high}) of media distributors you'd like: ")
            msg = self.check_input(user_input, low, high)
            if self.is_error:
                print(msg)
            else:
                self.num_media = int(user_input)

        stage = "People"
        low, high = Simulator.ranges[stage]
        self.num_people = 0
        while self.num_people == 0:
            user_input = input(f"Please enter the number ({low} - {high}) of people you'd like: ")
            msg = self.check_input(user_input, low, high)
            if self.is_error:
                print(msg)
            else:
                self.num_people = int(user_input)

        stage = "News"
        low, high = Simulator.ranges[stage]
        self.num_news = 0
        while self.num_news == 0:
            user_input = input(f"Please enter the number ({low} - {high}) of news articles you'd like: ")
            msg = self.check_input(user_input, low, high)
            if self.is_error:
                print(msg)
            else:
                self.num_news = int(user_input)

        stage = "Fake"
        low, high = Simulator.ranges[stage]
        self.fake_percentage = 0
        while self.fake_percentage == 0:
            user_input = input(f"Please enter the percentage ({low} - {high}) of "
                               "fake news articles you'd like: ")
            msg = self.check_input(user_input, low, high)
            if self.is_error:
                print(msg)
            else:
                self.fake_percentage = int(user_input)
        self.num_fake = int(round((self.fake_percentage / 100) * self.num_news, 0))
        self.num_real = self.num_news - self.num_fake

        stage = "Networks"
        low, high = Simulator.ranges[stage]
        self.num_networks = 0
        while self.num_networks == 0:
            user_input = input(f"Please enter the number ({low} - {high}) of networks you'd like: ")
            msg = self.check_input(user_input, low, high)
            if self.is_error:
                print(msg)
            else:
                self.num_networks = int(user_input)

        stage = "Time"
        low, high = Simulator.ranges[stage]
        self.time = 0
        while self.time == 0:
            user_input = input(f"Please enter the duration ({low} - {high}) weeks of the simulation: ")
            msg = self.check_input(user_input, low, high)
            if self.is_error:
                print(msg)
            else:
                self.time = int(user_input)
        self.time_left = copy.copy(self.time)
        Media.num_rounds = self.time
        print("Simulating...\n")

    def check_input(self, user_input, low, high):
        """Checks to see if there are any inputs that would cause errors in the program."""

        # Potential Input Error Messages
        error_msg = None
        no_input_msg = "Please enter an input and try again."
        invalid_char_msg = "Please only enter integers and try again. No special characters (e.g., %, ., +, etc.)"
        negative_num_msg = "Please enter a positive integer and try again."
        out_of_range_msg = f"Please enter a number between {low} and {high} and try again."

        if len(user_input) == 0:
            self.is_error = True
            error_msg = no_input_msg
        elif not user_input.isdigit():
            self.is_error = True
            error_msg = invalid_char_msg
        elif int(user_input) < 0:
            self.is_error = True
            error_msg = negative_num_msg
        elif int(user_input) < low or int(user_input) > high:
            self.is_error = True
            error_msg = out_of_range_msg
        else:
            self.is_error = False

        if self.is_error:
            return error_msg

    def simulate(self):
        """The simulate method runs the simulation by calling the appropriate methods at the appropriate time."""

        self.create_media()
        self.create_news()
        self.create_networks()
        self.create_persons()
        while self.time_left != 0:
            self.time_step()
        print("Check out your results by expanding the charts! "
              "When you're ready, please close the chart window to end the program. No rush :) \n")
        self.plot()
        print("Thank you for simulating with me! I recommend playing around more with new inputs! "
              "It is the best way to gain cool, new insights.")

    def create_media(self):
        """Create media distributor objects with randomized polarization and corresponding credibility."""

        # The while loop ensures at least one distributor is created for each polarization distribution
        while len(Media.extreme) == 0 or len(Media.moderate) == 0 or len(Media.weak) == 0:
            Media.media.clear()
            Media.extreme.clear()
            Media.moderate.clear()
            Media.weak.clear()
            for x in range(1, self.num_media + 1):

                polarization = random.randint(1, 10)

                if polarization in Media.extreme_pol_dist:
                    credibility = random.randint(1, 2)

                elif polarization in Media.moderate_pol_dist:
                    credibility = random.randint(3, 6)

                else:
                    credibility = random.randint(7, 10)

                Media(x, polarization, credibility)

    def create_news(self):
        """Creates news objects for each media distributor based on the polarization of the distributor."""

        fakes_unassigned = copy.copy(self.num_fake)
        real_unassigned = copy.copy(self.num_real)
        distributors_left = copy.copy(self.num_media)

        extreme_fake_batch = int((.68 * self.num_fake) // len(Media.extreme))
        extreme_real_batch = int(.05 * self.num_real // len(Media.extreme))
        moderate_fake_batch = int((.27 * self.num_fake) // len(Media.moderate))
        moderate_real_batch = int((.27 * self.num_real) // len(Media.moderate))
        low_fake_batch = int((.05 * self.num_fake) // len(Media.weak))
        low_real_batch = int((.68 * self.num_real) // len(Media.weak))

        for distributor in Media.media.values():

            if distributor.polarization in Media.extreme_pol_dist:
                fake_news_batch = extreme_fake_batch
                real_news_batch = extreme_real_batch

            elif distributor.polarization in Media.moderate_pol_dist:
                fake_news_batch = moderate_fake_batch
                real_news_batch = moderate_real_batch

            else:
                fake_news_batch = low_fake_batch
                real_news_batch = low_real_batch

            if distributors_left == 0:
                real_news_batch = real_unassigned
                fake_news_batch = fakes_unassigned
                distributor.create_news(fake_news_batch, real_news_batch)
                real_unassigned -= real_news_batch
                fakes_unassigned -= fake_news_batch

            else:
                distributor.create_news(fake_news_batch, real_news_batch)
                fakes_unassigned -= fake_news_batch
                real_unassigned -= real_news_batch
                distributors_left -= 1

    def create_networks(self):
        """Creates network objects."""

        for x in range(1, self.num_networks + 1):
            Network(x)

    def create_persons(self):
        """Creates person objects and assigns them to networks and media distributors."""

        for x in range(1, self.num_people + 1):
            polarization = random.randint(1, 10)
            credibility = random.randint(1, 10)
            consumption_pref = random.randint(1, 10)
            person = Person(x, polarization, credibility, consumption_pref)

            # assigns person to (up to 3) networks
            num_networks = random.randint(1, 3)
            for _ in range(num_networks):
                network_uid = random.randint(1, self.num_networks)
                Network.networks[network_uid].add_person(person)
                person.add_network(network_uid)

            # assigns person to (up to 3) media distributors
            num_distributors = random.randint(1, 3)
            for _ in range(num_distributors):
                distributor_uid = random.randint(1, self.num_media)
                Media.media[distributor_uid].add_person(person)

    def time_step(self):
        """Moves the simulation forward through each time step (round). Each round has 4 phases: distribute,
        consumption, redistribution, and reconsumption."""

        current_time_step = (self.time - self.time_left) + 1

        # Phase 1: Media distribute news to persons.
        for distributor in Media.media.values():
            distributor.distribute()

        # Phase 2: Persons consume news.
        for person in Person.persons.values():
            person.consume()

        # Phase 3: Persons re-distribute news to their networks.
        for person in Person.persons.values():
            person.distribute()

        # Phase 4: Persons consume news.
        for person in Person.persons.values():
            person.consume()

        self.log(current_time_step)
        self.time_left -= 1

    def log(self, time_step):
        """Keeps track of changes we are looking to graph from round to round."""

        self.sim_history["Weeks"].append(time_step)
        self.sim_history["Fake News Belief"].append(Person.fake_news_belief)
        self.sim_history["Fake News Distributed"].append(News.fake_distribution_count)
        self.sim_history["Real News Distributed"].append(News.real_distribution_count)
        self.sim_history["Media Fake News Shared"].append(Media.fakes_shared)
        self.sim_history["Media Real News Shared"].append(Media.real_shared)
        self.sim_history["Peer to Peer Fake News Shared"].append(Person.fakes_shared)
        self.sim_history["Peer to Peer Real News Shared"].append(Person.real_shared)

    def plot(self):
        """Plots our desired outputs and displays them to the user."""

        # X axis is the same for all charts
        x_label = "Weeks"
        x_values = self.sim_history[x_label]

        # Creates figure and axes objects
        fig, axs = plt.subplots(2, 2, clear=True)
        fig.set_size_inches(14, 10)
        ax1 = axs[0][0]
        ax2 = axs[0][1]
        ax3 = axs[1][0]
        ax4 = axs[1][1]

        # Axis 1 variables
        ax1_y_label = "Fake News Belief"
        ax1_y_values = self.sim_history[ax1_y_label]

        # Plots Axis 1
        ax1.plot(x_values, ax1_y_values)
        ax1.set_xlabel(x_label)
        ax1.set_ylabel(ax1_y_label)
        ax1.set_title("Fake News Belief Over Time")

        # Axis 2 variables
        ax2_y_label = "Total Distribution Count"
        line1_label = "Fake News Distributed"
        ax2_line1_y_values = self.sim_history[line1_label]
        line2_label = "Real News Distributed"
        ax2_line2_y_values = self.sim_history[line2_label]

        # Plot Axis 2
        ax2.plot(x_values, ax2_line1_y_values),
        ax2.plot(x_values, ax2_line2_y_values),
        ax2.set_xlabel(x_label)
        ax2.set_ylabel(ax2_y_label)
        ax2.legend([line1_label, line2_label], loc=0)
        ax2.set_title("Fake vs Real News Distribution")

        # Axis 3 variables
        ax3_y_label = "News Shared"
        ax3_line1_y_values = self.sim_history["Media Fake News Shared"]
        ax3_line2_y_values = self.sim_history["Media Real News Shared"]

        # Plots Axis 3
        ax3.plot(x_values, ax3_line1_y_values),
        ax3.plot(x_values, ax3_line2_y_values),
        ax3.set_xlabel(x_label)
        ax3.set_ylabel(ax3_y_label)
        ax3.legend([line1_label, line2_label], loc=0)
        ax3.set_title("Media to Person News Distribution")

        # Axis 4 variables
        ax4_y_label = "News Shared"
        ax4_line1_y_values = self.sim_history["Peer to Peer Fake News Shared"]
        ax4_line2_y_values = self.sim_history["Peer to Peer Real News Shared"]

        # Plots Axis 4
        ax4.plot(x_values, ax4_line1_y_values),
        ax4.plot(x_values, ax4_line2_y_values),
        ax4.set_xlabel(x_label)
        ax4.set_ylabel(ax4_y_label)
        ax4.legend([line1_label, line2_label], loc=0)
        ax4.set_title("Peer to Peer News Distribution")

        plt.show()


Simmothy = Simulator()
Simmothy.simulate()
