#  Copyright 2023 Google LLC
#
#  Licensed under the Apache License, Version 2.0 (the "License");
#  you may not use this file except in compliance with the License.
#  You may obtain a copy of the License at
#
#      https://www.apache.org/licenses/LICENSE-2.0
#
#  Unless required by applicable law or agreed to in writing, software
#  distributed under the License is distributed on an "AS IS" BASIS,
#  WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
#  See the License for the specific language governing permissions and
#  limitations under the License.

import dataclasses
import inspect
from typing import Any, Callable, Dict, List, Optional

import attrs
import cirq
import numpy as np
import sympy
from sympy.parsing.sympy_parser import parse_expr

from qualtran import (
    Bloq,
    BloqInstance,
    CompositeBloq,
    Connection,
    Controlled,
    DanglingT,
    DecomposeNotImplementedError,
    DecomposeTypeError,
    LeftDangle,
    QDType,
    RightDangle,
    Signature,
    Soquet,
)
from qualtran._infra.adjoint import Adjoint
from qualtran.bloqs import arithmetic, basic_gates, factoring, swap_network
from qualtran.bloqs.arithmetic import sorting
from qualtran.bloqs.data_loading.qrom import QROM
from qualtran.bloqs.mcmt import and_bloq
from qualtran.bloqs.util_bloqs import Allocate, ArbitraryClifford, Free, Join, Split
from qualtran.cirq_interop import CirqGateAsBloq
from qualtran.protos import bloq_pb2
from qualtran.serialization import annotations, args, data_types, registers

RESOLVER_DICT = {
    'CNOT': basic_gates.CNOT,
    'Rx': basic_gates.Rx,
    'Ry': basic_gates.Ry,
    'Rz': basic_gates.Rz,
    'CSwap': basic_gates.CSwap,
    'TwoBitCSwap': basic_gates.TwoBitCSwap,
    'TwoBitSwap': basic_gates.TwoBitSwap,
    'TGate': basic_gates.TGate,
    'MinusEffect': basic_gates.MinusEffect,
    'MinusState': basic_gates.MinusState,
    'PlusState': basic_gates.PlusState,
    'PlusEffect': basic_gates.PlusEffect,
    'XGate': basic_gates.XGate,
    'IntEffect': basic_gates.IntEffect,
    'IntState': basic_gates.IntState,
    'OneEffect': basic_gates.OneEffect,
    'OneState': basic_gates.OneState,
    'ZeroEffect': basic_gates.ZeroEffect,
    'ZeroState': basic_gates.ZeroState,
    'ZGate': basic_gates.ZGate,
    'CtrlAddK': factoring.CtrlAddK,
    'CtrlModAddK': factoring.CtrlModAddK,
    'CtrlScaleModAdd': factoring.CtrlScaleModAdd,
    'ModExp': factoring.ModExp,
    'CtrlModMul': factoring.CtrlModMul,
    'And': and_bloq.And,
    'MultiAnd': and_bloq.MultiAnd,
    'Add': arithmetic.Add,
    'Square': arithmetic.Square,
    'SumOfSquares': arithmetic.SumOfSquares,
    'Product': arithmetic.Product,
    'GreaterThan': arithmetic.GreaterThan,
    'Comparator': sorting.Comparator,
    'BitonicSort': sorting.BitonicSort,
    'CSwapApprox': swap_network.CSwapApprox,
    'SwapWithZero': swap_network.SwapWithZero,
    'Split': Split,
    'Join': Join,
    'Allocate': Allocate,
    'Free': Free,
    'ArbitraryClifford': ArbitraryClifford,
    'Controlled': Controlled,
    'CirqGateAsBloq': CirqGateAsBloq,
    'Toffoli': basic_gates.Toffoli,
    'QROM': QROM,
    'Adjoint': Adjoint,
}


def arg_to_proto(*, name: str, val: Any) -> bloq_pb2.BloqArg:
    if isinstance(val, int):
        return bloq_pb2.BloqArg(name=name, int_val=val)
    if isinstance(val, float):
        return bloq_pb2.BloqArg(name=name, float_val=val)
    if isinstance(val, str):
        return bloq_pb2.BloqArg(name=name, string_val=val)
    if isinstance(val, sympy.Expr):
        return bloq_pb2.BloqArg(name=name, sympy_expr=str(val))
    if isinstance(val, np.ndarray):
        return bloq_pb2.BloqArg(name=name, ndarray=args.ndarray_to_proto(val))
    if isinstance(val, cirq.Gate):
        return bloq_pb2.BloqArg(name=name, cirq_json_gzip=cirq.to_json_gzip(val))
    if isinstance(val, QDType):
        return bloq_pb2.BloqArg(name=name, qdata_type=data_types.data_type_to_proto(val))
    if isinstance(val, tuple):
        return bloq_pb2.BloqArg(name=name, tuple_val=args.list_or_tuple_to_proto(val))
    if isinstance(val, list):
        if isinstance(val[0], np.ndarray):
            return bloq_pb2.BloqArg(name=name, list_of_arrays_val=args.list_or_tuple_to_proto(val))
        else:
            return bloq_pb2.BloqArg(name=name, list_val=args.list_or_tuple_to_proto(val))
    raise ValueError(f"Cannot serialize {val} of unknown type {type(val)}")


def arg_from_proto(arg: bloq_pb2.BloqArg) -> Dict[str, Any]:
    if arg.HasField("int_val"):
        return {arg.name: arg.int_val}
    if arg.HasField("float_val"):
        return {arg.name: arg.float_val}
    if arg.HasField("string_val"):
        return {arg.name: arg.string_val}
    if arg.HasField("sympy_expr"):
        return {arg.name: parse_expr(arg.sympy_expr)}
    if arg.HasField("ndarray"):
        return {arg.name: args.ndarray_from_proto(arg.ndarray)}
    if arg.HasField("cirq_json_gzip"):
        return {arg.name: cirq.read_json_gzip(gzip_raw=arg.cirq_json_gzip)}
    if arg.HasField("qdata_type"):
        return {arg.name: data_types.data_type_from_proto(arg.qdata_type)}
    if arg.HasField("tuple_val"):
        return {arg.name: args.tuple_from_proto(arg.tuple_val)}
    if arg.HasField("list_val"):
        return {arg.name: args.list_from_proto(arg.list_val)}
    if arg.HasField("list_of_arrays_val"):
        array_list = [np.array(array) for array in args.list_from_proto(arg.list_of_arrays_val)]
        return {arg.name: array_list}
    raise ValueError(f"Cannot deserialize {arg=}")


class _BloqLibDeserializer:
    def __init__(self, lib: bloq_pb2.BloqLibrary):
        self.idx_to_proto: Dict[int, bloq_pb2.BloqLibrary.BloqWithDecomposition] = {
            b.bloq_id: b for b in lib.table
        }
        self.idx_to_bloq: Dict[int, Bloq] = {}
        self.dangling_to_singleton = {"LeftDangle": LeftDangle, "RightDangle": RightDangle}

    def bloq_id_to_bloq(self, bloq_id: int):
        """Constructs a Bloq corresponding to a `bloq_id` given an `idx_to_proto` mapping.

        The `idx_to_proto` mappping is constructed using a `BloqLibrary`.
        The `idx_to_bloq` mapping acts as a cache to avoid redundant deserialization of Bloqs.
        """
        if bloq_id in self.idx_to_bloq:
            return self.idx_to_bloq[bloq_id]
        bloq_proto: bloq_pb2.BloqLibrary.BloqWithDecomposition = self.idx_to_proto[bloq_id]
        if bloq_proto.bloq.name == 'CompositeBloq':
            self.idx_to_bloq[bloq_id] = CompositeBloq(
                connections=tuple(
                    self._connection_from_proto(cxn) for cxn in bloq_proto.decomposition
                ),
                signature=Signature(registers.registers_from_proto(bloq_proto.bloq.registers)),
            )
        elif bloq_proto.bloq.name in RESOLVER_DICT:
            kwargs = {}
            for arg in bloq_proto.bloq.args:
                if arg.HasField('subbloq'):
                    kwargs[arg.name] = self.bloq_id_to_bloq(arg.subbloq)
                else:
                    kwargs.update(arg_from_proto(arg))
            self.idx_to_bloq[bloq_id] = self._construct_bloq(bloq_proto.bloq.name, **kwargs)
        else:
            raise ValueError(f"Unable to find a Bloq corresponding to {bloq_proto.bloq.name=}")
        return self.idx_to_bloq[bloq_id]

    def _construct_bloq(self, name: str, **kwargs):
        """Construct a Bloq using serialized name and BloqArgs. Initializes bloq with builder
        if 'set_builder_with_kwargs' is overriden. Otherwise, it will try to initialize the bloq directly with kwargs."""
        return RESOLVER_DICT[name](**kwargs)

    def _connection_from_proto(self, cxn: bloq_pb2.Connection) -> Connection:
        return Connection(
            left=self._soquet_from_proto(cxn.left), right=self._soquet_from_proto(cxn.right)
        )

    def _soquet_from_proto(self, soq: bloq_pb2.Soquet) -> Soquet:
        binst = (
            self.dangling_to_singleton[soq.dangling_t]
            if soq.HasField('dangling_t')
            else BloqInstance(
                i=soq.bloq_instance.instance_id,
                bloq=self.bloq_id_to_bloq(soq.bloq_instance.bloq_id),
            )
        )
        return Soquet(
            binst=binst, reg=registers.register_from_proto(soq.register), idx=tuple(soq.index)
        )


def bloqs_from_proto(lib: bloq_pb2.BloqLibrary) -> List[Bloq]:
    """Deserializes a BloqLibrary as a list of Bloqs."""
    deserializer = _BloqLibDeserializer(lib)
    return [deserializer.bloq_id_to_bloq(bloq.bloq_id) for bloq in lib.table]


def bloqs_to_proto(
    *bloqs: Bloq,
    name: str = '',
    pred: Callable[[BloqInstance], bool] = lambda _: True,
    max_depth: int = 1,
) -> bloq_pb2.BloqLibrary:
    """Serializes one or more Bloqs as a `BloqLibrary`."""

    bloq_to_idx: Dict[Bloq, int] = {}
    for bloq in bloqs:
        _add_bloq_to_dict(bloq, bloq_to_idx)
        _populate_bloq_to_idx(bloq, bloq_to_idx, pred, max_depth)

    # Decompose[..]Error is raised if `bloq` does not have a decomposition.
    # KeyError is raised if `bloq` has a decomposition, but we do not wish to serialize it
    # because of conditions checked by `pred` and `max_depth`.
    stop_recursing_exceptions = (DecomposeNotImplementedError, DecomposeTypeError, KeyError)

    # `bloq_to_idx` would now contain a list of all bloqs that should be serialized.
    library = bloq_pb2.BloqLibrary(name=name)
    for bloq, bloq_id in bloq_to_idx.items():
        try:
            cbloq = bloq if isinstance(bloq, CompositeBloq) else bloq.decompose_bloq()
            decomposition = [_connection_to_proto(cxn, bloq_to_idx) for cxn in cbloq.connections]
        except stop_recursing_exceptions:
            decomposition = None

        try:
            bloq_counts = {
                bloq_to_idx[b]: args.int_or_sympy_to_proto(c)
                for b, c in sorted(bloq.bloq_counts().items(), key=lambda x: x[1])
            }
        except stop_recursing_exceptions:
            bloq_counts = None
        except TypeError:
            bloq_counts = None

        library.table.add(
            bloq_id=bloq_id,
            decomposition=decomposition,
            bloq_counts=bloq_counts,
            bloq=_bloq_to_proto(bloq, bloq_to_idx=bloq_to_idx),
        )
    return library


def _iter_fields(bloq: Bloq):
    """Yields fields of `bloq` iff `type(bloq)` is implemented using `dataclasses` or `attr`.

    The method only yields Fields corresponding to attributes that are part of the __init__ method
    of the bloq. This ensures that for attrs / dataclasses based Bloqs that have a custom init
    method, we yield only the fields that are accepted by the constructor (eg: `IntState` Bloq).
    Note that this is a hacky solution and a more generalized long-term approach would be to have
    a protocol to query init params for each class and use them as Bloq args during
    serialization / deserialization.
    """

    if dataclasses.is_dataclass(type(bloq)):
        for field in dataclasses.fields(bloq):
            if field.name in inspect.signature(type(bloq).__init__).parameters:
                yield field
    elif attrs.has(type(bloq)):
        for field in attrs.fields(type(bloq)):
            if field.name in inspect.signature(type(bloq).__init__).parameters:
                yield field


def _connection_to_proto(cxn: Connection, bloq_to_idx: Dict[Bloq, int]):
    return bloq_pb2.Connection(
        left=_soquet_to_proto(cxn.left, bloq_to_idx), right=_soquet_to_proto(cxn.right, bloq_to_idx)
    )


def _soquet_to_proto(soq: Soquet, bloq_to_idx: Dict[Bloq, int]) -> bloq_pb2.Soquet:
    if isinstance(soq.binst, DanglingT):
        return bloq_pb2.Soquet(
            dangling_t=repr(soq.binst), register=registers.register_to_proto(soq.reg), index=soq.idx
        )
    else:
        return bloq_pb2.Soquet(
            bloq_instance=_bloq_instance_to_proto(soq.binst, bloq_to_idx),
            register=registers.register_to_proto(soq.reg),
            index=soq.idx,
        )


def _bloq_instance_to_proto(
    binst: BloqInstance, bloq_to_idx: Dict[Bloq, int]
) -> bloq_pb2.BloqInstance:
    return bloq_pb2.BloqInstance(instance_id=binst.i, bloq_id=bloq_to_idx[binst.bloq])


def _add_bloq_to_dict(bloq: Bloq, bloq_to_idx: Dict[Bloq, int]):
    """Adds `{bloq: len(bloq_to_idx)}` to `bloq_to_idx` dictionary if it doesn't exist already."""
    if bloq not in bloq_to_idx:
        next_idx = len(bloq_to_idx)
        bloq_to_idx[bloq] = next_idx


def _cbloq_dot_bloq_instances(cbloq: CompositeBloq) -> List[BloqInstance]:
    """Equivalent to `cbloq.bloq_instances`, but preserves insertion order among Bloq instances."""
    ret = {}
    for cxn in cbloq.connections:
        for soq in [cxn.left, cxn.right]:
            if not isinstance(soq.binst, DanglingT):
                ret[soq.binst] = 0
    return list(ret.keys())


def _populate_bloq_to_idx(
    bloq: Bloq, bloq_to_idx: Dict[Bloq, int], pred: Callable[[BloqInstance], bool], max_depth: int
):
    """Recursively track all primitive Bloqs to be serialized, as part of `bloq_to_idx` dictionary."""

    assert bloq in bloq_to_idx
    if max_depth > 0:
        # Decompose the current Bloq and track it's decomposed Bloqs.
        try:
            cbloq = bloq if isinstance(bloq, CompositeBloq) else bloq.decompose_bloq()
            for binst in _cbloq_dot_bloq_instances(cbloq):
                _add_bloq_to_dict(binst.bloq, bloq_to_idx)
                if pred(binst):
                    _populate_bloq_to_idx(binst.bloq, bloq_to_idx, pred, max_depth - 1)
                else:
                    _populate_bloq_to_idx(binst.bloq, bloq_to_idx, pred, 0)
        except NotImplementedError:
            # NotImplementedError is raised if `bloq` does not have a decomposition.
            ...
        except DecomposeTypeError:
            ...

        # Approximately decompose the current Bloq and its decomposed Bloqs.
        try:
            for subbloq, _ in bloq.bloq_counts().items():
                _add_bloq_to_dict(subbloq, bloq_to_idx)
                _populate_bloq_to_idx(subbloq, bloq_to_idx, pred, 0)

        except NotImplementedError:
            # NotImplementedError is raised if `bloq` does not implement bloq_counts.
            ...

    # If the current Bloq contains other Bloqs as sub-bloqs, add them to the `bloq_to_idx` dict.
    # This is only supported for Bloqs implemented as dataclasses / attrs.
    for field in _iter_fields(bloq):
        subbloq = getattr(bloq, field.name)
        if isinstance(subbloq, Bloq):
            _add_bloq_to_dict(subbloq, bloq_to_idx)
            _populate_bloq_to_idx(subbloq, bloq_to_idx, pred, 0)


def _bloq_to_proto(bloq: Bloq, *, bloq_to_idx: Dict[Bloq, int]) -> bloq_pb2.Bloq:
    try:
        t_complexity = annotations.t_complexity_to_proto(bloq.t_complexity())
    except (DecomposeTypeError, DecomposeNotImplementedError, TypeError):
        t_complexity = None

    return bloq_pb2.Bloq(
        name=bloq.__class__.__name__,
        registers=registers.registers_to_proto(bloq.signature),
        t_complexity=t_complexity,
        args=_bloq_args_to_proto(bloq, bloq_to_idx=bloq_to_idx),
    )


def _bloq_args_to_proto(
    bloq: Bloq, *, bloq_to_idx: Dict[Bloq, int]
) -> Optional[List[bloq_pb2.BloqArg]]:
    if isinstance(bloq, CompositeBloq):
        return None

    try:
        ret = [_bloq_to_proto(name=key, val=val) for key, val in bloq._kwargs_().items()]
    except NotImplementedError:
        ret = [
            _bloq_arg_to_proto(
                name=field.name, val=getattr(bloq, field.name), bloq_to_idx=bloq_to_idx
            )
            for field in _iter_fields(bloq)
        ]
    return ret if ret else None


def _bloq_arg_to_proto(name: str, val: Any, bloq_to_idx: Dict[Bloq, int]) -> bloq_pb2.BloqArg:
    if isinstance(val, Bloq):
        return bloq_pb2.BloqArg(name=name, subbloq=bloq_to_idx[val])
    return arg_to_proto(name=name, val=val)
