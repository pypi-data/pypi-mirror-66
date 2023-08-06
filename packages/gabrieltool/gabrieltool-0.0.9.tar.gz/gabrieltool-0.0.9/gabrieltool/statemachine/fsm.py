# -*- coding: utf-8 -*-
"""Finite State Machine Representation.

Each message type in the protobuf definition has a corresponding data class.
The data object is named as obj_<protobuf_msg_type>.
"""


import functools
import json

from gabrieltool.statemachine import (predicate_zoo, processor_zoo,
                                      wca_state_machine_pb2)


class FSMObjBase(object):
    """Adapter class to translate protobuf's serialized class.

    This adapter class exposes protobuf message attributes
    as class attributes.
    """
    _obj_cnt = 0

    def __init__(self, name=None):
        """Base Initializer

        Arguments:
            parent {FSMObjBase Children Classes} -- Pointer to the parent element.
            protobuf_message {ProtoBuf Class} -- Serialized description of the element.
        """

        super(FSMObjBase, self).__init__()
        FSMObjBase._obj_cnt += 1
        protobuf_message = getattr(wca_state_machine_pb2,
                                   self.__class__.__name__)()
        self._pb = protobuf_message
        self._expose_serializer_attr('name', 'rw')
        self.name = self._get_default_name()
        if name is not None:
            self.name = name

    def _get_default_name(self):
        return '{}_{}'.format(self.__class__.__name__,
                              FSMObjBase._obj_cnt)

    def __repr__(self):
        default = super(FSMObjBase, self).__repr__()
        return '<{} ({})>'.format(self.name, default)

    def _expose_serializer_attr(self, name, mode):
        """Helper method to provide easy access to serializer attribute."""
        if mode == 'r':
            setattr(FSMObjBase, name, property(
                lambda self: getattr(self._pb, name)))
        elif mode == 'rw':
            setattr(FSMObjBase,
                    name,
                    property(lambda self: getattr(self._pb, name),
                             lambda self, value: setattr(
                                 self._pb, name, value)
                             ))
        else:
            raise ValueError(
                'Unsupported mode {}. Valid modes are "r" or "rw"'.format(mode))

    def from_desc(self, desc):
        """Construct an object from its serialized description."""
        self._pb = desc

    def to_desc(self):
        """Returned serialized description as a protobuf message."""
        return self._pb


class TransitionPredicate(FSMObjBase):
    """A TriggerPredicate is an callable object."""

    def __init__(self, name=None, partial_obj=None):
        """TransitionPredicate callable object

        Keyword Arguments:
            name {[type]} -- [description] (default: {None})
            func {partial object} -- Partial Function Object (default: {None})
        """

        super(TransitionPredicate, self).__init__(name)
        self._partial_obj = partial_obj

    @property
    def callable_obj(self):
        return self._partial_obj

    @callable_obj.setter
    def callable_obj(self, val):
        if type(val) is not functools.partial:
            raise TypeError(
                'Invalid type ({}). '
                'TransitionPredicate\'s callable_obj requires '
                'a functool.parital object.'.format(type(val)))
        self._partial_obj = val

    def __call__(self, app_state):
        return self._partial_obj(app_state=app_state)

    def from_desc(self, data):
        super(TransitionPredicate, self).from_desc(data)
        func = getattr(predicate_zoo, self._pb.callable_name)
        kwargs = {}
        kwargs = json.loads(self._pb.callable_args)
        self._partial_obj = functools.partial(func, **kwargs)

    def to_desc(self):
        self._pb.callable_name = self._partial_obj.func.__name__
        self._pb.callable_args = json.dumps(self._partial_obj.keywords)
        return super(TransitionPredicate, self).to_desc()


class Instruction(FSMObjBase):
    """Instruction to user."""

    def __init__(self, name=None, audio=None, image=None, video=None):
        super(Instruction, self).__init__(name=name)
        expose_attrs = [('audio', 'rw'), ('image', 'rw'), ('video', 'rw')]
        for (attr, mode) in expose_attrs:
            self._expose_serializer_attr(attr, mode)
        if audio is not None:
            self.audio = audio
        if image is not None:
            self.image = image
        if video is not None:
            self.video = video


class Transition(FSMObjBase):
    """A Transition has satisfying predicates, next_state, and instructions."""

    def __init__(self, name=None, predicates=None, instruction=None, next_state=None):
        """Transition among states

        Keyword Arguments:
            name {string} -- name of the transition. (default: {None})
            predicates {list of TransitionPredicate} -- a list of
            TransitionPredicates. They are daisy-chained (AND) together when
            evaluating whether this transition should be taken.  (default: {None})
            instruction {Instruction} -- Instruction to give when taking a transition. (default: {None})
            next_state {State} -- State to transit to. (default: {None})
        """

        super(Transition, self).__init__(name)
        self.predicates = predicates if predicates is not None else []
        self.instruction = instruction
        self.next_state = next_state

    @property
    def predicates(self):
        return self._predicates

    @predicates.setter
    def predicates(self, val):
        if type(val) != list:
            raise TypeError("Predicates needs to be type list.")
        self._predicates = val

    def __call__(self, app_state):
        """Given the current app_state, check if a transition should be taken.

        The condition of taking a transition is that all the trigger predicates
        are satisfied. When all of them are satisfied, return True, next state,
        and instruction. Otherwise, return False, None, None.
        """
        for predicate in self._predicates:
            if not predicate(app_state):
                return None
        return self

    def to_desc(self):
        for pred in self._predicates:
            self._pb.predicates.extend([pred.to_desc()])
        if self.instruction is not None:
            self._pb.instruction.CopyFrom(self.instruction.to_desc())
        if self.next_state:
            self._pb.next_state = self.next_state.name
        return super(Transition, self).to_desc()

    def from_desc(self):
        raise NotImplementedError("Transition itself does not know enough information "
                                  "to build from its description. "
                                  "next_state variable depends on a FSM. "
                                  "Use StateMachine Helper Class instead.")


class Processor(FSMObjBase):
    """Processsor is a FSM element that processes image in a state."""

    def __init__(self, name=None, callable_obj=None):
        """

        Keyword Arguments:
            name {string} -- name (default: {None})
            callable_obj {A callable object (e.g. funtools.partial)} -- A instance from
            classes in processor_zoo. (default: {None})
        """

        super(Processor, self).__init__(name)
        self._callable_obj = callable_obj if callable(callable_obj) else lambda x: None

    @property
    def callable_obj(self):
        return self._callable_obj

    def prepare(self):
        """Prepare's a processor.

        Invoke prepare() method of the callable if it has any. """
        prepare_func = getattr(self._callable_obj, "prepare", None)
        if callable(prepare_func):
            prepare_func()

    def __call__(self, img):
        return self._callable_obj(img)

    def from_desc(self, data):
        super(Processor, self).from_desc(data)
        callable_class = getattr(processor_zoo, self._pb.callable_name)
        initializer_args = json.loads(self._pb.callable_args)
        self._callable_obj = callable_class.from_json(initializer_args)

    def to_desc(self):
        self._pb.callable_name = self._callable_obj.__class__.__name__
        self._pb.callable_args = json.dumps(self._callable_obj.kwargs)
        return super(Processor, self).to_desc()


class State(FSMObjBase):
    """A state has many processors and transitions.

    This class is used to represent all the actions/code that can be called for
    a state.
    """

    def __init__(self, name=None, processors=None, transitions=None):
        super(State, self).__init__(name)
        self.processors = processors if processors is not None else []
        self.transitions = transitions if transitions is not None else []

    @property
    def processors(self):
        return self._processors

    @processors.setter
    def processors(self, val):
        if type(val) != list:
            raise TypeError("Predicates needs to be type list.")
        self._processors = val

    @property
    def transitions(self):
        return self._transitions

    @transitions.setter
    def transitions(self, val):
        if type(val) != list:
            raise TypeError("Predicates needs to be type list.")
        self._transitions = val

    def _run_processors(self, img):
        app_state = {'raw': img}
        for obj_processor in self.processors:
            app_state.update(obj_processor(img))
        return app_state

    def _get_one_satisfied_transition(self, app_state):
        for transition in self.transitions:
            if transition(app_state) is not None:
                return transition
        return None

    def prepare(self):
        """Prepare a state to be run.

        Invokes prepare function of all processors
        """
        for obj_processor in self.processors:
            obj_processor.prepare()

    def __call__(self, img):
        """React to the image.

        Within each state, the processors should first run based on their order
        to get application state.
        Then, the triggerPredicates should be run.

        Arguments:
            img {np array} -- input image

        Returns:
            next state {State}
        """
        app_state = self._run_processors(img)
        transition = self._get_one_satisfied_transition(app_state)
        if transition is None:
            return self, Instruction()
        else:
            return transition.next_state, transition.instruction

    def to_desc(self):
        for proc in self.processors:
            self._pb.processors.extend([proc.to_desc()])
        for tran in self.transitions:
            self._pb.transitions.extend([tran.to_desc()])
        return super(State, self).to_desc()

    def from_desc(self):
        raise NotImplementedError("State itself does not know enough information "
                                  "to build from its description. "
                                  "next_state variable depends on a FSM. "
                                  "Use StateMachine Helper Class instead.")


class StateMachine(object):
    """State Machine helper class to serialize/deserialize a state machine.
    """

    @classmethod
    def _load_generic_from_desc(cls, GenericType, desc):
        item = GenericType()
        item.from_desc(desc)
        return item

    @classmethod
    def _load_transition(cls, desc, state_lut):
        tran = Transition(name=desc.name)
        tran.instruction = cls._load_generic_from_desc(Instruction,
                                                       desc.instruction)
        preds = [cls._load_generic_from_desc(
            TransitionPredicate, pred_desc)
            for pred_desc in desc.predicates]
        tran._predicates = preds
        tran.next_state = state_lut[desc.next_state]
        return tran

    @classmethod
    def _load_state(cls, desc, state_lut):
        state = state_lut[desc.name]
        state.processors = [cls._load_generic_from_desc(
            Processor, proc_desc) for proc_desc in desc.processors]
        state.transitions = [cls._load_transition(
            tran_desc, state_lut) for tran_desc in desc.transitions]
        return state

    @classmethod
    def from_bytes(cls, data):
        """Load a State Machine from bytes.

        Return the start state of the state machine.
        """
        pb_fsm = wca_state_machine_pb2.StateMachine()
        pb_fsm.ParseFromString(data)
        state_lut = {}
        # 1st pass get all states
        for state_desc in pb_fsm.states:
            state = State(name=state_desc.name)
            if state.name in state_lut:
                raise ValueError(
                    "Duplicate State Name: {}. Invalid State Machine Data.".format(
                        state.name))
            state_lut[state.name] = state
        # 2nd pass to load all state details
        for state_desc in pb_fsm.states:
            cls._load_state(state_desc, state_lut)
        return state_lut[pb_fsm.start_state]

    @classmethod
    def bfs(cls, start_state):
        """Breadth-first Search on the graph, starting from start_state node."""
        visited = set([start_state])
        work_queue = [start_state]
        while work_queue:
            state = work_queue.pop(0)
            for tran in state.transitions:
                if tran.next_state is not None and tran.next_state not in visited:
                    work_queue.append(tran.next_state)
                    visited.add(tran.next_state)
            yield state

    @classmethod
    def to_bytes(cls, name, start_state):
        """Dump a State Machine rooted at start_state.

        Arguments:
            start_state {State} -- Start state of the state machine.
        """
        # TODO(junjuew) optimize/dedup assets/kwargs
        visited = {}
        for state in cls.bfs(start_state):
            if state.name in visited and visited[state.name] is not state:
                raise ValueError("Found duplicate state name {}. "
                                 "Cannot serialize a FSM with duplicate state name".format(state.name))
            visited[state.name] = state

        # serialize
        pb_fsm = wca_state_machine_pb2.StateMachine(
            name=name, start_state=start_state.name)
        for (state_name, state) in list(visited.items()):
            pb_fsm.states.extend([state.to_desc()])
        return pb_fsm.SerializeToString()
