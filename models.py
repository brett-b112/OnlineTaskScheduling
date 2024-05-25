from math import sqrt, floor, ceil
from task import Task
from model import Model


class AmdahlModel(Model):
    name = "Amdahl"

    def get_alpha(self) -> float:
        return (sqrt(2) + 1 + sqrt(2 * sqrt(2) - 1)) / 2 #paper2

    def get_mu(self) -> float:
        return (1 - sqrt(8 * sqrt(2) - 11)) / 2 #paper2

    def time(self, task: Task, nb_proc: int) -> float:
        return task.get_w() * ((1 - task.get_d()) / nb_proc + task.get_d())

    def p_max(self, task: Task, p: int) -> int:
        return p


class CommunicationModel(Model):
    name = "Communication"

    def get_alpha(self) -> float:
        return 4 / 3   #from paper1

    def get_mu(self) -> float:
        return (23 - sqrt(313)) / 18  #paper2

    def time(self, task: Task, nb_proc: int) -> float:
        w, c = task.get_w(), task.get_c()
        return w / nb_proc + c * (nb_proc - 1)

    def p_max(self, task: Task, p: int) -> int:
        s = sqrt(task.get_w() / task.get_c())
        if task.get_execution_time(floor(s), self) <= task.get_execution_time(ceil(s), self):
            p_tild = floor(s)
        else:
            p_tild = ceil(s)

        return round(min(p, task.get_p(), p_tild))


class GeneralModel(Model):
    name = "General"

    def get_alpha(self) -> float:
        return 2

    def get_mu(self) -> float:
        return (33 - sqrt(738)) / 27

    def time(self, task: Task, nb_proc: int) -> float:
        w, d, p, c = task.get_w(), task.get_d(), task.get_p(), task.get_c()
        return w * ((1 - d) / min(nb_proc, p) + d) + c * (nb_proc - 1)

    def p_max(self, task: Task, p: int) -> int:
        s = sqrt(task.get_w() / task.get_c())
        if task.get_execution_time(floor(s), self) <= task.get_execution_time(ceil(s), self):
            p_tild = floor(s)
        else:
            p_tild = ceil(s)

        return round(min(p, task.get_p(), p_tild))


class RooflineModel(Model):
    name = "Roofline"

    def get_alpha(self) -> float:
        return 1

    # def get_mu(self) -> float:
    #     return 

    def time(self, task: Task, nb_proc: int) -> float:
        w, d, p, c = task.get_w(), task.get_d(), task.get_p(), task.get_c()
        return w / min(nb_proc, p)

    def p_max(self, task: Task, p: int) -> int:
        return min(ceil(task.get_p()), p) #max degree of parallelism, no.of proc
