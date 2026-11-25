'This class represents the model for dualoc data, storing all current data on duloc states'
class DualocObject:
    def __init__(self):
        self.current_iteration = 0
        self.selected_dataset = "Please Select Dataset..."
        self.iteration_steps = []
        self.num_iterations = 0
        self.c_ij = []
        self.f_j = []

    def clear(self):
        self.current_iteration = 0
        self.selected_dataset = "Please Select Dataset..."
        self.iteration_steps.clear()
        self.num_iterations = 0
        self.c_ij.clear()
        self.f_j.clear()
