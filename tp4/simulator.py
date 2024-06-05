from copy import deepcopy
from generator.utils import StateItem

arrival_key = 'arrival'
inscription_key = 'inscription'
maintenance_key = 'maintenance'
return_key = 'return'


events = {
    '0': 'Inicio',
    'arrival': 'Llegada Alumno',
    'inscription': 'Fin de inscripcion',
    'maintenance': 'Fin de mantenimiento',
    'return': 'Regreso del tecnico',
}


class Technician():
    pending_return = "Regreso Pendiente"
    working = "Ocupado"
    free = "Libre"

    def __init__(self) -> None:
        self.state = self.pending_return

    def finish_maintenance(self, next_computer_index):
        if next_computer_index is None:
            self.state = Technician.pending_return
            self.computer_index = None
            return
        self.start_maintenance(next_computer_index)

    def start_maintenance(self, next_computer_index):
        assert next_computer_index is not None
        self.state = Technician.working
        self.computer_index = next_computer_index

    def display(self):
        return {
            'state': self.state,
        }


class Computer():
    free = 'Libre'
    busy = 'Ocupado'
    in_maintenance = "En Mantenimiento"
    dirty = 'Si'
    clean = 'No'

    def __init__(self) -> None:
        self.state = self.free
        self.needs_maintenance = self.dirty
        self.was_maintained = False
        self.client = None

    def finished_inscription(self, next_client=None):
        self.needs_maintenance = Computer.dirty
        if next_client is None:
            self.state = Computer.free
            self.client = None
            return
        self.client = next_client

    def finished_maintenance(self):
        self.needs_maintenance = Computer.clean
        self.was_maintained = True
        self.state = Computer.free

    def start_maintenance(self):
        self.state = Computer.in_maintenance

    def arrives_client(self, client):
        self.state = Computer.busy
        self.client = client

    def display(self):
        return {
            'state': self.state,
            'needs_maintenance': self.needs_maintenance
        }


class Student():
    inscription = "Siendo inscripto {computer}"
    in_queue = "Esperando inscripcion"

    def __init__(self, state, queue_arrival_time=None, used_computer=None):
        self.queue_arrival_time = queue_arrival_time
        self.state = state
        self.used_computer = used_computer

    def display(self):
        return {
            'queue_arrival_time': self.queue_arrival_time,
            'state': self.state.format(computer=self.used_computer + 1),
        }

    @staticmethod
    def display_default():
        return {
            'queue_arrival_time': None,
            'state': None
        }


class InscriptionSimulation():
    @staticmethod
    def get_event_display(event_number):
        return events[f'{event_number}']

    @staticmethod
    def generate_next_event(generator, current_time):
        generated_event = generator.get_next_event()
        return {
            **generated_event,
            'next_time': current_time + generated_event.get('generated_time')
        }

    def generate_next_inscription(self, current_time, inscription_data):
        generated_time = self.generate_next_event(
            self.inscription_generator, current_time)
        next_time = generated_time.pop('next_time')

        for key, value in inscription_data.items():
            if not key.startswith('next_time'):
                continue
            if value is not None:
                continue
            inscription_data[key] = next_time
            break

        return {
            **inscription_data,
            **generated_time,
        }

    def get_next_event(self, state):
        events_keys = ['arrival', 'inscription', 'maintenance', 'return']
        next_event_key = None
        next_event_time = None
        for event_key in events_keys:
            for key, value in getattr(state, event_key).items():
                if not key.startswith('next_time') or value is None:
                    continue
                if next_event_key is None:
                    next_event_key = f'{event_key}/{key}'
                    next_event_time = value
                    continue
                if value < next_event_time:
                    next_event_key = f'{event_key}/{key}'
                    next_event_time = value
        return next_event_key

    def display_computers(self):
        return [computer.display() for computer in self.computers]

    def display_students(self):
        return [student.display() if student is not None else Student.display_default() for student in self.students]

    def get_next_student_in_queue(self):
        most_recent_time = None
        next_student = None
        for student in self.students:
            if student is None or student.state != Student.in_queue:
                continue
            if most_recent_time is None or \
               most_recent_time > student.queue_arrival_time:
                most_recent_time = student.queue_arrival_time
                next_student = student
            continue
        return next_student

    def get_next_dirty_computer(self):
        for index in range(len(self.computers)):
            computer = self.computers[index]
            if computer.state == Computer.busy or \
               computer.was_maintained is True or \
               computer.needs_maintenance == Computer.clean:
                continue
            return index
        return None

    def set_computers_as_maintainable(self):
        for cpu in self.computers:
            cpu.was_maintained = False

    def delete_student(self, student_to_delete):
        for i in range(len(self.students)):
            student = self.students[i]
            if student_to_delete == student:
                self.students[i] = None
                del student

    def __init__(
        self, history_callback, inscription_generator,
        arrivals_generator, maintenance_generator, return_generator
    ):
        self.history_callback = history_callback
        self.inscription_generator = inscription_generator
        self.arrivals_generator = arrivals_generator
        self.maintennace_generator = maintenance_generator
        self.return_generator = return_generator
        self.history = []
        self.computers = [
            Computer(),
            Computer(),
            Computer(),
            Computer(),
            Computer(),
            Computer(),
        ]
        self.technician = Technician()
        self.students = []
        initial_state = StateItem(**{
            'iteration': 0,
            'event': '0',
            'event_display': 0,
            'time': 0,
            'arrival': self.generate_next_event(self.arrivals_generator, 0),
            'inscription': {
                'random': None,
                'generated_time': None,
                'next_time_1': None,
                'next_time_2': None,
                'next_time_3': None,
                'next_time_4': None,
                'next_time_5': None,
                'next_time_6': None,
            },
            'maintenance': {
                'random': None,
                'generated_time': None,
                'next_time': None
            },
            'return': self.generate_next_event(self.return_generator, 0),
            'computers': self.display_computers(),
            'technician': self.technician.display(),
            'queue': 0,
            'total_students': 0,
            'students_returning': 0,
            'students_passed_queue': 0,
            'total_wait_time': 0,
            'students_leaving_percentage': 0,
            'avg_wait_time': 0,
            'students': []
        })
        self._state = [initial_state]

    def update_state(self, next_state):
        self._state.pop()
        self._state.insert(0, next_state)

    def process_a_client(self, next_state, computer, computer_key, from_inscription=None, from_maintenance=None):
        next_student = self.get_next_student_in_queue()
        if from_inscription is True:
            computer.finished_inscription(next_client=next_student)
        if from_maintenance is True:
            computer.arrives_client(next_student)
        next_student.state = Student.inscription
        next_student.used_computer = computer_key
        next_state.queue -= 1

        # Count this last variables when is the last iteration of the simulation since there
        # are some students that are not yet still accounted for this variables.
        self.calculate_analitics(next_student, next_state)

        next_state.inscription = self.generate_next_inscription(
            next_state.time,  next_state.inscription)

    def calculate_analitics(self, student, next_state):
        next_state.students_passed_queue += 1
        next_state.total_wait_time += \
            (next_state.time - student.queue_arrival_time)
        next_state.students_leaving_percentage = next_state.students_returning * 100 / next_state.total_students
        next_state.avg_wait_time = \
            next_state.total_wait_time / next_state.students_passed_queue

    def run(self, time_target, show_from, show_count):
        for i in range(time_target):
            prev_state = self._state[0]
            next_state = deepcopy(prev_state)
            next_state.iteration = i + 1

            next_event_full_key = self.get_next_event(next_state)
            event_key, time_key = next_event_full_key.split('/')
            next_time = getattr(next_state, event_key)[time_key]

            next_state.event = event_key
            next_state.event_display = self.get_event_display(event_key)
            next_state.time = next_time

            current_time = next_time

            event_data = getattr(next_state, event_key)
            setattr(next_state, event_key, {
                **event_data,
                f'{time_key}': None
            })

            if event_key == arrival_key:
                next_state.arrival = self.generate_next_event(
                    self.arrivals_generator, current_time)

                are_computers_available = any([
                    True
                    if computer.state == Computer.free else False
                    for computer in self.computers
                ])
                if are_computers_available:
                    # Start working on one
                    picked_computer = None
                    for i in range(len(self.computers)):
                        computer = self.computers[i]
                        if computer.state == Computer.free:
                            picked_computer = i
                    new_student = Student(
                        Student.inscription, used_computer=picked_computer
                    )
                    added_within_list = False
                    for index in range(len(self.students)):
                        student = self.students[index]
                        if student is None:
                            self.students[index] = new_student
                            added_within_list = True
                            break
                    if added_within_list is False:
                        self.students.append(new_student)

                    next_state.inscription = self.generate_next_inscription(
                        current_time,
                        next_state.inscription
                    )
                    self.computers[picked_computer].arrives_client(new_student)
                elif next_state.queue < 5:
                    self.students.append(Student(
                        Student.in_queue,
                        queue_arrival_time=current_time
                    ))
                    # No computer available so you have to go to a queue
                    next_state.queue += 1
                else:
                    # Cola llena
                    next_state.students_returning += 1
                next_state.total_students += 1

            if event_key == inscription_key:
                next_state.inscription[time_key] = None
                computer_key = int(time_key.split('next_time_')[-1]) - 1
                print(computer_key)
                computer = self.computers[computer_key]
                inscribed_student = computer.client
                if next_state.queue > 0:
                    self.delete_student(inscribed_student)
                    self.process_a_client(
                        next_state, computer, computer_key, from_inscription=True)

                elif next_state.queue == 0:
                    computer.finished_inscription()
                    self.delete_student(inscribed_student)

            if event_key == maintenance_key:
                # Fin de mantenimiento
                computer_index = self.technician.computer_index
                computer = self.computers[computer_index]
                computer.finished_maintenance()
                if next_state.queue > 0:
                    self.process_a_client(
                        next_state, computer, computer_index, from_maintenance=True)
                next_computer_index = self.get_next_dirty_computer()
                if next_computer_index is None:
                    self.set_computers_as_maintainable()
                    setattr(next_state, 'return', self.generate_next_event(self.return_generator, current_time))
                else:
                    next_cpu = self.computers[next_computer_index]
                    next_cpu.start_maintenance()
                    next_state.maintenance = self.generate_next_event(self.maintennace_generator, current_time)
                self.technician.finish_maintenance(next_computer_index)

            if event_key == return_key:
                # Regreso de tecnico
                next_computer_index = self.get_next_dirty_computer()
                if next_computer_index is None:
                    self.set_computers_as_maintainable()
                    setattr(next_state, 'return', self.generate_next_event(self.return_generator, current_time))
                else:
                    next_cpu = self.computers[next_computer_index]
                    next_cpu.start_maintenance()
                    self.technician.start_maintenance(next_computer_index)
                    next_state.maintenance = self.generate_next_event(self.maintennace_generator, current_time)

            if i == time_target - 1:
                # Last iteration
                for student in self.students:
                    if student is None or student.state != Student.in_queue:
                        continue
                    self.calculate_analitics(student, next_state)

            next_state.computers = self.display_computers()
            next_state.technician = self.technician.display()
            next_state.students = self.display_students()

            history_item = self.history_callback(
                next_state, show_from, show_count, time_target)
            if history_item is not None:
                self.history.append(history_item.__dict__)

            self.update_state(next_state)
        return self.history
