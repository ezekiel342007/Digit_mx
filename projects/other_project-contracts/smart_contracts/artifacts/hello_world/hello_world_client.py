# flake8: noqa
# fmt: off
# mypy: disable-error-code="no-any-return, no-untyped-call, misc, type-arg"
# This file was automatically generated by algokit-client-generator.
# DO NOT MODIFY IT BY HAND.
# requires: algokit-utils@^1.2.0
import base64
import dataclasses
import decimal
import typing
from abc import ABC, abstractmethod

import algokit_utils
import algosdk
from algosdk.v2client import models
from algosdk.atomic_transaction_composer import (
    AtomicTransactionComposer,
    AtomicTransactionResponse,
    SimulateAtomicTransactionResponse,
    TransactionSigner,
    TransactionWithSigner
)

_APP_SPEC_JSON = r"""{
    "hints": {
        "hello(string)string": {
            "call_config": {
                "no_op": "CALL"
            }
        },
        "create_app(asset,uint64)void": {
            "call_config": {
                "no_op": "CREATE"
            }
        },
        "set_price(uint64)void": {
            "call_config": {
                "no_op": "CALL"
            }
        },
        "opt_in_to_asset(pay)void": {
            "call_config": {
                "no_op": "CALL"
            }
        },
        "buy(uint64,pay)void": {
            "call_config": {
                "no_op": "CALL"
            }
        },
        "delete_app()void": {
            "call_config": {
                "delete_application": "CALL"
            }
        }
    },
    "source": {
        "approval": "I3ByYWdtYSB2ZXJzaW9uIDEwCgpzbWFydF9jb250cmFjdHMuaGVsbG9fd29ybGQuY29udHJhY3QuSGVsbG9Xb3JsZC5hcHByb3ZhbF9wcm9ncmFtOgogICAgY2FsbHN1YiBfX3B1eWFfYXJjNF9yb3V0ZXJfXwogICAgcmV0dXJuCgoKLy8gc21hcnRfY29udHJhY3RzLmhlbGxvX3dvcmxkLmNvbnRyYWN0LkhlbGxvV29ybGQuX19wdXlhX2FyYzRfcm91dGVyX18oKSAtPiB1aW50NjQ6Cl9fcHV5YV9hcmM0X3JvdXRlcl9fOgogICAgcHJvdG8gMCAxCiAgICB0eG4gTnVtQXBwQXJncwogICAgYnogX19wdXlhX2FyYzRfcm91dGVyX19fYWZ0ZXJfaWZfZWxzZUAxMQogICAgbWV0aG9kICJoZWxsbyhzdHJpbmcpc3RyaW5nIgogICAgbWV0aG9kICJjcmVhdGVfYXBwKGFzc2V0LHVpbnQ2NCl2b2lkIgogICAgbWV0aG9kICJzZXRfcHJpY2UodWludDY0KXZvaWQiCiAgICBtZXRob2QgIm9wdF9pbl90b19hc3NldChwYXkpdm9pZCIKICAgIG1ldGhvZCAiYnV5KHVpbnQ2NCxwYXkpdm9pZCIKICAgIG1ldGhvZCAiZGVsZXRlX2FwcCgpdm9pZCIKICAgIHR4bmEgQXBwbGljYXRpb25BcmdzIDAKICAgIG1hdGNoIF9fcHV5YV9hcmM0X3JvdXRlcl9fX2hlbGxvX3JvdXRlQDIgX19wdXlhX2FyYzRfcm91dGVyX19fY3JlYXRlX2FwcF9yb3V0ZUAzIF9fcHV5YV9hcmM0X3JvdXRlcl9fX3NldF9wcmljZV9yb3V0ZUA0IF9fcHV5YV9hcmM0X3JvdXRlcl9fX29wdF9pbl90b19hc3NldF9yb3V0ZUA1IF9fcHV5YV9hcmM0X3JvdXRlcl9fX2J1eV9yb3V0ZUA2IF9fcHV5YV9hcmM0X3JvdXRlcl9fX2RlbGV0ZV9hcHBfcm91dGVANwogICAgaW50IDAKICAgIHJldHN1YgoKX19wdXlhX2FyYzRfcm91dGVyX19faGVsbG9fcm91dGVAMjoKICAgIHR4biBPbkNvbXBsZXRpb24KICAgICEKICAgIGFzc2VydCAvLyBPbkNvbXBsZXRpb24gaXMgTm9PcAogICAgdHhuIEFwcGxpY2F0aW9uSUQKICAgIGFzc2VydCAvLyBpcyBub3QgY3JlYXRpbmcKICAgIHR4bmEgQXBwbGljYXRpb25BcmdzIDEKICAgIGV4dHJhY3QgMiAwCiAgICBjYWxsc3ViIGhlbGxvCiAgICBkdXAKICAgIGxlbgogICAgaXRvYgogICAgZXh0cmFjdCA2IDIKICAgIHN3YXAKICAgIGNvbmNhdAogICAgYnl0ZSAweDE1MWY3Yzc1CiAgICBzd2FwCiAgICBjb25jYXQKICAgIGxvZwogICAgaW50IDEKICAgIHJldHN1YgoKX19wdXlhX2FyYzRfcm91dGVyX19fY3JlYXRlX2FwcF9yb3V0ZUAzOgogICAgdHhuIE9uQ29tcGxldGlvbgogICAgIQogICAgYXNzZXJ0IC8vIE9uQ29tcGxldGlvbiBpcyBOb09wCiAgICB0eG4gQXBwbGljYXRpb25JRAogICAgIQogICAgYXNzZXJ0IC8vIGlzIGNyZWF0aW5nCiAgICB0eG5hIEFwcGxpY2F0aW9uQXJncyAxCiAgICBidG9pCiAgICB0eG5hcyBBc3NldHMKICAgIHR4bmEgQXBwbGljYXRpb25BcmdzIDIKICAgIGJ0b2kKICAgIGNhbGxzdWIgY3JlYXRlX2FwcAogICAgaW50IDEKICAgIHJldHN1YgoKX19wdXlhX2FyYzRfcm91dGVyX19fc2V0X3ByaWNlX3JvdXRlQDQ6CiAgICB0eG4gT25Db21wbGV0aW9uCiAgICAhCiAgICBhc3NlcnQgLy8gT25Db21wbGV0aW9uIGlzIE5vT3AKICAgIHR4biBBcHBsaWNhdGlvbklECiAgICBhc3NlcnQgLy8gaXMgbm90IGNyZWF0aW5nCiAgICB0eG5hIEFwcGxpY2F0aW9uQXJncyAxCiAgICBidG9pCiAgICBjYWxsc3ViIHNldF9wcmljZQogICAgaW50IDEKICAgIHJldHN1YgoKX19wdXlhX2FyYzRfcm91dGVyX19fb3B0X2luX3RvX2Fzc2V0X3JvdXRlQDU6CiAgICB0eG4gT25Db21wbGV0aW9uCiAgICAhCiAgICBhc3NlcnQgLy8gT25Db21wbGV0aW9uIGlzIE5vT3AKICAgIHR4biBBcHBsaWNhdGlvbklECiAgICBhc3NlcnQgLy8gaXMgbm90IGNyZWF0aW5nCiAgICB0eG4gR3JvdXBJbmRleAogICAgaW50IDEKICAgIC0KICAgIGR1cAogICAgZ3R4bnMgVHlwZUVudW0KICAgIGludCBwYXkKICAgID09CiAgICBhc3NlcnQgLy8gdHJhbnNhY3Rpb24gdHlwZSBpcyBwYXkKICAgIGNhbGxzdWIgb3B0X2luX3RvX2Fzc2V0CiAgICBpbnQgMQogICAgcmV0c3ViCgpfX3B1eWFfYXJjNF9yb3V0ZXJfX19idXlfcm91dGVANjoKICAgIHR4biBPbkNvbXBsZXRpb24KICAgICEKICAgIGFzc2VydCAvLyBPbkNvbXBsZXRpb24gaXMgTm9PcAogICAgdHhuIEFwcGxpY2F0aW9uSUQKICAgIGFzc2VydCAvLyBpcyBub3QgY3JlYXRpbmcKICAgIHR4bmEgQXBwbGljYXRpb25BcmdzIDEKICAgIGJ0b2kKICAgIHR4biBHcm91cEluZGV4CiAgICBpbnQgMQogICAgLQogICAgZHVwCiAgICBndHhucyBUeXBlRW51bQogICAgaW50IHBheQogICAgPT0KICAgIGFzc2VydCAvLyB0cmFuc2FjdGlvbiB0eXBlIGlzIHBheQogICAgY2FsbHN1YiBidXkKICAgIGludCAxCiAgICByZXRzdWIKCl9fcHV5YV9hcmM0X3JvdXRlcl9fX2RlbGV0ZV9hcHBfcm91dGVANzoKICAgIHR4biBPbkNvbXBsZXRpb24KICAgIGludCBEZWxldGVBcHBsaWNhdGlvbgogICAgPT0KICAgIGFzc2VydCAvLyBPbkNvbXBsZXRpb24gaXMgRGVsZXRlQXBwbGljYXRpb24KICAgIHR4biBBcHBsaWNhdGlvbklECiAgICBhc3NlcnQgLy8gaXMgbm90IGNyZWF0aW5nCiAgICBjYWxsc3ViIGRlbGV0ZV9hcHAKICAgIGludCAxCiAgICByZXRzdWIKCl9fcHV5YV9hcmM0X3JvdXRlcl9fX2FmdGVyX2lmX2Vsc2VAMTE6CiAgICBpbnQgMAogICAgcmV0c3ViCgoKLy8gc21hcnRfY29udHJhY3RzLmhlbGxvX3dvcmxkLmNvbnRyYWN0LkhlbGxvV29ybGQuaGVsbG8obmFtZTogYnl0ZXMpIC0+IGJ5dGVzOgpoZWxsbzoKICAgIHByb3RvIDEgMQogICAgYnl0ZSAiSGVsbG8sICIKICAgIGZyYW1lX2RpZyAtMQogICAgY29uY2F0CiAgICByZXRzdWIKCgovLyBzbWFydF9jb250cmFjdHMuaGVsbG9fd29ybGQuY29udHJhY3QuSGVsbG9Xb3JsZC5jcmVhdGVfYXBwKGFzc2V0OiB1aW50NjQsIHVuaXRhcnlfcHJpY2U6IHVpbnQ2NCkgLT4gdm9pZDoKY3JlYXRlX2FwcDoKICAgIHByb3RvIDIgMAogICAgYnl0ZSAiYXNzZXRfaWQiCiAgICBmcmFtZV9kaWcgLTIKICAgIGFwcF9nbG9iYWxfcHV0CiAgICBieXRlICJ1bml0YXJ5X3ByaWNlIgogICAgZnJhbWVfZGlnIC0xCiAgICBhcHBfZ2xvYmFsX3B1dAogICAgcmV0c3ViCgoKLy8gc21hcnRfY29udHJhY3RzLmhlbGxvX3dvcmxkLmNvbnRyYWN0LkhlbGxvV29ybGQuc2V0X3ByaWNlKHVuaXRhcnlfcHJpY2U6IHVpbnQ2NCkgLT4gdm9pZDoKc2V0X3ByaWNlOgogICAgcHJvdG8gMSAwCiAgICB0eG4gU2VuZGVyCiAgICBnbG9iYWwgQ3JlYXRvckFkZHJlc3MKICAgID09CiAgICBhc3NlcnQKICAgIGJ5dGUgInVuaXRhcnlfcHJpY2UiCiAgICBmcmFtZV9kaWcgLTEKICAgIGFwcF9nbG9iYWxfcHV0CiAgICByZXRzdWIKCgovLyBzbWFydF9jb250cmFjdHMuaGVsbG9fd29ybGQuY29udHJhY3QuSGVsbG9Xb3JsZC5vcHRfaW5fdG9fYXNzZXQobWJyOiB1aW50NjQpIC0+IHZvaWQ6Cm9wdF9pbl90b19hc3NldDoKICAgIHByb3RvIDEgMAogICAgZ2xvYmFsIEN1cnJlbnRBcHBsaWNhdGlvbkFkZHJlc3MKICAgIGludCAwCiAgICBieXRlICJhc3NldF9pZCIKICAgIGFwcF9nbG9iYWxfZ2V0X2V4CiAgICBhc3NlcnQgLy8gY2hlY2sgc2VsZi5hc3NldF9pZCBleGlzdHMKICAgIGFzc2V0X2hvbGRpbmdfZ2V0IEFzc2V0QmFsYW5jZQogICAgYnVyeSAxCiAgICAhCiAgICBhc3NlcnQKICAgIGZyYW1lX2RpZyAtMQogICAgZ3R4bnMgUmVjZWl2ZXIKICAgIGdsb2JhbCBDdXJyZW50QXBwbGljYXRpb25BZGRyZXNzCiAgICA9PQogICAgYXNzZXJ0CiAgICBmcmFtZV9kaWcgLTEKICAgIGd0eG5zIEFtb3VudAogICAgZ2xvYmFsIE1pbkJhbGFuY2UKICAgIGdsb2JhbCBBc3NldE9wdEluTWluQmFsYW5jZQogICAgKwogICAgPT0KICAgIGFzc2VydAogICAgaXR4bl9iZWdpbgogICAgaW50IDAKICAgIGJ5dGUgImFzc2V0X2lkIgogICAgYXBwX2dsb2JhbF9nZXRfZXgKICAgIGFzc2VydCAvLyBjaGVjayBzZWxmLmFzc2V0X2lkIGV4aXN0cwogICAgZ2xvYmFsIEN1cnJlbnRBcHBsaWNhdGlvbkFkZHJlc3MKICAgIGludCAwCiAgICBpdHhuX2ZpZWxkIEFzc2V0QW1vdW50CiAgICBpdHhuX2ZpZWxkIEFzc2V0UmVjZWl2ZXIKICAgIGl0eG5fZmllbGQgWGZlckFzc2V0CiAgICBpbnQgYXhmZXIKICAgIGl0eG5fZmllbGQgVHlwZUVudW0KICAgIGludCAwCiAgICBpdHhuX2ZpZWxkIEZlZQogICAgaXR4bl9zdWJtaXQKICAgIHJldHN1YgoKCi8vIHNtYXJ0X2NvbnRyYWN0cy5oZWxsb193b3JsZC5jb250cmFjdC5IZWxsb1dvcmxkLmJ1eShxdWFudGl0eTogdWludDY0LCBidXlfdHhuOiB1aW50NjQpIC0+IHZvaWQ6CmJ1eToKICAgIHByb3RvIDIgMAogICAgZnJhbWVfZGlnIC0xCiAgICBndHhucyBTZW5kZXIKICAgIGR1cAogICAgdHhuIFNlbmRlcgogICAgPT0KICAgIGFzc2VydAogICAgZnJhbWVfZGlnIC0xCiAgICBndHhucyBSZWNlaXZlcgogICAgZ2xvYmFsIEN1cnJlbnRBcHBsaWNhdGlvbkFkZHJlc3MKICAgID09CiAgICBhc3NlcnQKICAgIGZyYW1lX2RpZyAtMQogICAgZ3R4bnMgQW1vdW50CiAgICBpbnQgMAogICAgYnl0ZSAidW5pdGFyeV9wcmljZSIKICAgIGFwcF9nbG9iYWxfZ2V0X2V4CiAgICBhc3NlcnQgLy8gY2hlY2sgc2VsZi51bml0YXJ5X3ByaWNlIGV4aXN0cwogICAgZnJhbWVfZGlnIC0yCiAgICAqCiAgICA9PQogICAgYXNzZXJ0CiAgICBpdHhuX2JlZ2luCiAgICBpbnQgMAogICAgYnl0ZSAiYXNzZXRfaWQiCiAgICBhcHBfZ2xvYmFsX2dldF9leAogICAgYXNzZXJ0IC8vIGNoZWNrIHNlbGYuYXNzZXRfaWQgZXhpc3RzCiAgICBmcmFtZV9kaWcgLTIKICAgIGl0eG5fZmllbGQgQXNzZXRBbW91bnQKICAgIGl0eG5fZmllbGQgWGZlckFzc2V0CiAgICBpdHhuX2ZpZWxkIEFzc2V0UmVjZWl2ZXIKICAgIGludCBheGZlcgogICAgaXR4bl9maWVsZCBUeXBlRW51bQogICAgaW50IDAKICAgIGl0eG5fZmllbGQgRmVlCiAgICBpdHhuX3N1Ym1pdAogICAgcmV0c3ViCgoKLy8gc21hcnRfY29udHJhY3RzLmhlbGxvX3dvcmxkLmNvbnRyYWN0LkhlbGxvV29ybGQuZGVsZXRlX2FwcCgpIC0+IHZvaWQ6CmRlbGV0ZV9hcHA6CiAgICBwcm90byAwIDAKICAgIHR4biBTZW5kZXIKICAgIGdsb2JhbCBDcmVhdG9yQWRkcmVzcwogICAgPT0KICAgIGFzc2VydAogICAgaXR4bl9iZWdpbgogICAgaW50IDAKICAgIGJ5dGUgImFzc2V0X2lkIgogICAgYXBwX2dsb2JhbF9nZXRfZXgKICAgIGFzc2VydCAvLyBjaGVjayBzZWxmLmFzc2V0X2lkIGV4aXN0cwogICAgZ2xvYmFsIENyZWF0b3JBZGRyZXNzCiAgICBkdXAKICAgIGl0eG5fZmllbGQgQXNzZXRDbG9zZVRvCiAgICBpbnQgMAogICAgaXR4bl9maWVsZCBBc3NldEFtb3VudAogICAgaXR4bl9maWVsZCBBc3NldFJlY2VpdmVyCiAgICBpdHhuX2ZpZWxkIFhmZXJBc3NldAogICAgaW50IGF4ZmVyCiAgICBpdHhuX2ZpZWxkIFR5cGVFbnVtCiAgICBpbnQgMAogICAgaXR4bl9maWVsZCBGZWUKICAgIGl0eG5fc3VibWl0CiAgICBpdHhuX2JlZ2luCiAgICBnbG9iYWwgQ3JlYXRvckFkZHJlc3MKICAgIGR1cAogICAgaXR4bl9maWVsZCBDbG9zZVJlbWFpbmRlclRvCiAgICBpbnQgMAogICAgaXR4bl9maWVsZCBBbW91bnQKICAgIGl0eG5fZmllbGQgUmVjZWl2ZXIKICAgIGludCBwYXkKICAgIGl0eG5fZmllbGQgVHlwZUVudW0KICAgIGludCAwCiAgICBpdHhuX2ZpZWxkIEZlZQogICAgaXR4bl9zdWJtaXQKICAgIHJldHN1Ygo=",
        "clear": "I3ByYWdtYSB2ZXJzaW9uIDEwCgpzbWFydF9jb250cmFjdHMuaGVsbG9fd29ybGQuY29udHJhY3QuSGVsbG9Xb3JsZC5jbGVhcl9zdGF0ZV9wcm9ncmFtOgogICAgaW50IDEKICAgIHJldHVybgo="
    },
    "state": {
        "global": {
            "num_byte_slices": 0,
            "num_uints": 2
        },
        "local": {
            "num_byte_slices": 0,
            "num_uints": 0
        }
    },
    "schema": {
        "global": {
            "declared": {
                "asset_id": {
                    "type": "uint64",
                    "key": "asset_id"
                },
                "unitary_price": {
                    "type": "uint64",
                    "key": "unitary_price"
                }
            },
            "reserved": {}
        },
        "local": {
            "declared": {},
            "reserved": {}
        }
    },
    "contract": {
        "name": "HelloWorld",
        "methods": [
            {
                "name": "hello",
                "args": [
                    {
                        "type": "string",
                        "name": "name"
                    }
                ],
                "returns": {
                    "type": "string"
                }
            },
            {
                "name": "create_app",
                "args": [
                    {
                        "type": "asset",
                        "name": "asset"
                    },
                    {
                        "type": "uint64",
                        "name": "unitary_price"
                    }
                ],
                "returns": {
                    "type": "void"
                }
            },
            {
                "name": "set_price",
                "args": [
                    {
                        "type": "uint64",
                        "name": "unitary_price"
                    }
                ],
                "returns": {
                    "type": "void"
                }
            },
            {
                "name": "opt_in_to_asset",
                "args": [
                    {
                        "type": "pay",
                        "name": "mbr"
                    }
                ],
                "returns": {
                    "type": "void"
                }
            },
            {
                "name": "buy",
                "args": [
                    {
                        "type": "uint64",
                        "name": "quantity"
                    },
                    {
                        "type": "pay",
                        "name": "buy_txn"
                    }
                ],
                "returns": {
                    "type": "void"
                }
            },
            {
                "name": "delete_app",
                "args": [],
                "returns": {
                    "type": "void"
                }
            }
        ],
        "networks": {}
    },
    "bare_call_config": {}
}"""
APP_SPEC = algokit_utils.ApplicationSpecification.from_json(_APP_SPEC_JSON)
_TReturn = typing.TypeVar("_TReturn")


class _ArgsBase(ABC, typing.Generic[_TReturn]):
    @staticmethod
    @abstractmethod
    def method() -> str:
        ...


_TArgs = typing.TypeVar("_TArgs", bound=_ArgsBase[typing.Any])


@dataclasses.dataclass(kw_only=True)
class _TArgsHolder(typing.Generic[_TArgs]):
    args: _TArgs


@dataclasses.dataclass(kw_only=True)
class DeployCreate(algokit_utils.DeployCreateCallArgs, _TArgsHolder[_TArgs], typing.Generic[_TArgs]):
    pass


@dataclasses.dataclass(kw_only=True)
class Deploy(algokit_utils.DeployCallArgs, _TArgsHolder[_TArgs], typing.Generic[_TArgs]):
    pass


def _filter_none(value: dict | typing.Any) -> dict | typing.Any:
    if isinstance(value, dict):
        return {k: _filter_none(v) for k, v in value.items() if v is not None}
    return value


def _as_dict(data: typing.Any, *, convert_all: bool = True) -> dict[str, typing.Any]:
    if data is None:
        return {}
    if not dataclasses.is_dataclass(data):
        raise TypeError(f"{data} must be a dataclass")
    if convert_all:
        result = dataclasses.asdict(data) # type: ignore[call-overload]
    else:
        result = {f.name: getattr(data, f.name) for f in dataclasses.fields(data)}
    return _filter_none(result)


def _convert_transaction_parameters(
    transaction_parameters: algokit_utils.TransactionParameters | None,
) -> algokit_utils.TransactionParametersDict:
    return typing.cast(algokit_utils.TransactionParametersDict, _as_dict(transaction_parameters))


def _convert_call_transaction_parameters(
    transaction_parameters: algokit_utils.TransactionParameters | None,
) -> algokit_utils.OnCompleteCallParametersDict:
    return typing.cast(algokit_utils.OnCompleteCallParametersDict, _as_dict(transaction_parameters))


def _convert_create_transaction_parameters(
    transaction_parameters: algokit_utils.TransactionParameters | None,
    on_complete: algokit_utils.OnCompleteActionName,
) -> algokit_utils.CreateCallParametersDict:
    result = typing.cast(algokit_utils.CreateCallParametersDict, _as_dict(transaction_parameters))
    on_complete_enum = on_complete.replace("_", " ").title().replace(" ", "") + "OC"
    result["on_complete"] = getattr(algosdk.transaction.OnComplete, on_complete_enum)
    return result


def _convert_deploy_args(
    deploy_args: algokit_utils.DeployCallArgs | None,
) -> algokit_utils.ABICreateCallArgsDict | None:
    if deploy_args is None:
        return None

    deploy_args_dict = typing.cast(algokit_utils.ABICreateCallArgsDict, _as_dict(deploy_args))
    if isinstance(deploy_args, _TArgsHolder):
        deploy_args_dict["args"] = _as_dict(deploy_args.args)
        deploy_args_dict["method"] = deploy_args.args.method()

    return deploy_args_dict


@dataclasses.dataclass(kw_only=True)
class HelloArgs(_ArgsBase[str]):
    name: str

    @staticmethod
    def method() -> str:
        return "hello(string)string"


@dataclasses.dataclass(kw_only=True)
class SetPriceArgs(_ArgsBase[None]):
    unitary_price: int

    @staticmethod
    def method() -> str:
        return "set_price(uint64)void"


@dataclasses.dataclass(kw_only=True)
class OptInToAssetArgs(_ArgsBase[None]):
    mbr: TransactionWithSigner

    @staticmethod
    def method() -> str:
        return "opt_in_to_asset(pay)void"


@dataclasses.dataclass(kw_only=True)
class BuyArgs(_ArgsBase[None]):
    quantity: int
    buy_txn: TransactionWithSigner

    @staticmethod
    def method() -> str:
        return "buy(uint64,pay)void"


@dataclasses.dataclass(kw_only=True)
class CreateAppArgs(_ArgsBase[None]):
    asset: int
    unitary_price: int

    @staticmethod
    def method() -> str:
        return "create_app(asset,uint64)void"


@dataclasses.dataclass(kw_only=True)
class DeleteAppArgs(_ArgsBase[None]):
    @staticmethod
    def method() -> str:
        return "delete_app()void"


class GlobalState:
    def __init__(self, data: dict[bytes, bytes | int]):
        self.asset_id = typing.cast(int, data.get(b"asset_id"))
        self.unitary_price = typing.cast(int, data.get(b"unitary_price"))


@dataclasses.dataclass(kw_only=True)
class SimulateOptions:
    allow_more_logs: bool = dataclasses.field(default=False)
    allow_empty_signatures: bool = dataclasses.field(default=False)
    extra_opcode_budget: int = dataclasses.field(default=0)
    exec_trace_config: models.SimulateTraceConfig | None         = dataclasses.field(default=None)


class Composer:

    def __init__(self, app_client: algokit_utils.ApplicationClient, atc: AtomicTransactionComposer):
        self.app_client = app_client
        self.atc = atc

    def build(self) -> AtomicTransactionComposer:
        return self.atc

    def simulate(self, options: SimulateOptions | None = None) -> SimulateAtomicTransactionResponse:
        request = models.SimulateRequest(
            allow_more_logs=options.allow_more_logs,
            allow_empty_signatures=options.allow_empty_signatures,
            extra_opcode_budget=options.extra_opcode_budget,
            exec_trace_config=options.exec_trace_config,
            txn_groups=[]
        ) if options else None
        result = self.atc.simulate(self.app_client.algod_client, request)
        return result

    def execute(self) -> AtomicTransactionResponse:
        return self.app_client.execute_atc(self.atc)

    def hello(
        self,
        *,
        name: str,
        transaction_parameters: algokit_utils.TransactionParameters | None = None,
    ) -> "Composer":
        """Adds a call to `hello(string)string` ABI method
        
        :param str name: The `name` ABI parameter
        :param algokit_utils.TransactionParameters transaction_parameters: (optional) Additional transaction parameters
        :returns Composer: This Composer instance"""

        args = HelloArgs(
            name=name,
        )
        self.app_client.compose_call(
            self.atc,
            call_abi_method=args.method(),
            transaction_parameters=_convert_call_transaction_parameters(transaction_parameters),
            **_as_dict(args, convert_all=True),
        )
        return self

    def set_price(
        self,
        *,
        unitary_price: int,
        transaction_parameters: algokit_utils.TransactionParameters | None = None,
    ) -> "Composer":
        """Adds a call to `set_price(uint64)void` ABI method
        
        :param int unitary_price: The `unitary_price` ABI parameter
        :param algokit_utils.TransactionParameters transaction_parameters: (optional) Additional transaction parameters
        :returns Composer: This Composer instance"""

        args = SetPriceArgs(
            unitary_price=unitary_price,
        )
        self.app_client.compose_call(
            self.atc,
            call_abi_method=args.method(),
            transaction_parameters=_convert_call_transaction_parameters(transaction_parameters),
            **_as_dict(args, convert_all=True),
        )
        return self

    def opt_in_to_asset(
        self,
        *,
        mbr: TransactionWithSigner,
        transaction_parameters: algokit_utils.TransactionParameters | None = None,
    ) -> "Composer":
        """Adds a call to `opt_in_to_asset(pay)void` ABI method
        
        :param TransactionWithSigner mbr: The `mbr` ABI parameter
        :param algokit_utils.TransactionParameters transaction_parameters: (optional) Additional transaction parameters
        :returns Composer: This Composer instance"""

        args = OptInToAssetArgs(
            mbr=mbr,
        )
        self.app_client.compose_call(
            self.atc,
            call_abi_method=args.method(),
            transaction_parameters=_convert_call_transaction_parameters(transaction_parameters),
            **_as_dict(args, convert_all=True),
        )
        return self

    def buy(
        self,
        *,
        quantity: int,
        buy_txn: TransactionWithSigner,
        transaction_parameters: algokit_utils.TransactionParameters | None = None,
    ) -> "Composer":
        """Adds a call to `buy(uint64,pay)void` ABI method
        
        :param int quantity: The `quantity` ABI parameter
        :param TransactionWithSigner buy_txn: The `buy_txn` ABI parameter
        :param algokit_utils.TransactionParameters transaction_parameters: (optional) Additional transaction parameters
        :returns Composer: This Composer instance"""

        args = BuyArgs(
            quantity=quantity,
            buy_txn=buy_txn,
        )
        self.app_client.compose_call(
            self.atc,
            call_abi_method=args.method(),
            transaction_parameters=_convert_call_transaction_parameters(transaction_parameters),
            **_as_dict(args, convert_all=True),
        )
        return self

    def create_create_app(
        self,
        *,
        asset: int,
        unitary_price: int,
        on_complete: typing.Literal["no_op"] = "no_op",
        transaction_parameters: algokit_utils.CreateTransactionParameters | None = None,
    ) -> "Composer":
        """Adds a call to `create_app(asset,uint64)void` ABI method
        
        :param int asset: The `asset` ABI parameter
        :param int unitary_price: The `unitary_price` ABI parameter
        :param typing.Literal[no_op] on_complete: On completion type to use
        :param algokit_utils.CreateTransactionParameters transaction_parameters: (optional) Additional transaction parameters
        :returns Composer: This Composer instance"""

        args = CreateAppArgs(
            asset=asset,
            unitary_price=unitary_price,
        )
        self.app_client.compose_create(
            self.atc,
            call_abi_method=args.method(),
            transaction_parameters=_convert_create_transaction_parameters(transaction_parameters, on_complete),
            **_as_dict(args, convert_all=True),
        )
        return self

    def delete_delete_app(
        self,
        *,
        transaction_parameters: algokit_utils.TransactionParameters | None = None,
    ) -> "Composer":
        """Adds a call to `delete_app()void` ABI method
        
        :param algokit_utils.TransactionParameters transaction_parameters: (optional) Additional transaction parameters
        :returns Composer: This Composer instance"""

        args = DeleteAppArgs()
        self.app_client.compose_delete(
            self.atc,
            call_abi_method=args.method(),
            transaction_parameters=_convert_transaction_parameters(transaction_parameters),
            **_as_dict(args, convert_all=True),
        )
        return self

    def clear_state(
        self,
        transaction_parameters: algokit_utils.TransactionParameters | None = None,
        app_args: list[bytes] | None = None,
    ) -> "Composer":
        """Adds a call to the application with on completion set to ClearState
    
        :param algokit_utils.TransactionParameters transaction_parameters: (optional) Additional transaction parameters
        :param list[bytes] | None app_args: (optional) Application args to pass"""
    
        self.app_client.compose_clear_state(self.atc, _convert_transaction_parameters(transaction_parameters), app_args)
        return self


class HelloWorldClient:
    """A class for interacting with the HelloWorld app providing high productivity and
    strongly typed methods to deploy and call the app"""

    @typing.overload
    def __init__(
        self,
        algod_client: algosdk.v2client.algod.AlgodClient,
        *,
        app_id: int = 0,
        signer: TransactionSigner | algokit_utils.Account | None = None,
        sender: str | None = None,
        suggested_params: algosdk.transaction.SuggestedParams | None = None,
        template_values: algokit_utils.TemplateValueMapping | None = None,
        app_name: str | None = None,
    ) -> None:
        ...

    @typing.overload
    def __init__(
        self,
        algod_client: algosdk.v2client.algod.AlgodClient,
        *,
        creator: str | algokit_utils.Account,
        indexer_client: algosdk.v2client.indexer.IndexerClient | None = None,
        existing_deployments: algokit_utils.AppLookup | None = None,
        signer: TransactionSigner | algokit_utils.Account | None = None,
        sender: str | None = None,
        suggested_params: algosdk.transaction.SuggestedParams | None = None,
        template_values: algokit_utils.TemplateValueMapping | None = None,
        app_name: str | None = None,
    ) -> None:
        ...

    def __init__(
        self,
        algod_client: algosdk.v2client.algod.AlgodClient,
        *,
        creator: str | algokit_utils.Account | None = None,
        indexer_client: algosdk.v2client.indexer.IndexerClient | None = None,
        existing_deployments: algokit_utils.AppLookup | None = None,
        app_id: int = 0,
        signer: TransactionSigner | algokit_utils.Account | None = None,
        sender: str | None = None,
        suggested_params: algosdk.transaction.SuggestedParams | None = None,
        template_values: algokit_utils.TemplateValueMapping | None = None,
        app_name: str | None = None,
    ) -> None:
        """
        HelloWorldClient can be created with an app_id to interact with an existing application, alternatively
        it can be created with a creator and indexer_client specified to find existing applications by name and creator.
        
        :param AlgodClient algod_client: AlgoSDK algod client
        :param int app_id: The app_id of an existing application, to instead find the application by creator and name
        use the creator and indexer_client parameters
        :param str | Account creator: The address or Account of the app creator to resolve the app_id
        :param IndexerClient indexer_client: AlgoSDK indexer client, only required if deploying or finding app_id by
        creator and app name
        :param AppLookup existing_deployments:
        :param TransactionSigner | Account signer: Account or signer to use to sign transactions, if not specified and
        creator was passed as an Account will use that.
        :param str sender: Address to use as the sender for all transactions, will use the address associated with the
        signer if not specified.
        :param TemplateValueMapping template_values: Values to use for TMPL_* template variables, dictionary keys should
        *NOT* include the TMPL_ prefix
        :param str | None app_name: Name of application to use when deploying, defaults to name defined on the
        Application Specification
            """

        self.app_spec = APP_SPEC
        
        # calling full __init__ signature, so ignoring mypy warning about overloads
        self.app_client = algokit_utils.ApplicationClient(  # type: ignore[call-overload, misc]
            algod_client=algod_client,
            app_spec=self.app_spec,
            app_id=app_id,
            creator=creator,
            indexer_client=indexer_client,
            existing_deployments=existing_deployments,
            signer=signer,
            sender=sender,
            suggested_params=suggested_params,
            template_values=template_values,
            app_name=app_name,
        )

    @property
    def algod_client(self) -> algosdk.v2client.algod.AlgodClient:
        return self.app_client.algod_client

    @property
    def app_id(self) -> int:
        return self.app_client.app_id

    @app_id.setter
    def app_id(self, value: int) -> None:
        self.app_client.app_id = value

    @property
    def app_address(self) -> str:
        return self.app_client.app_address

    @property
    def sender(self) -> str | None:
        return self.app_client.sender

    @sender.setter
    def sender(self, value: str) -> None:
        self.app_client.sender = value

    @property
    def signer(self) -> TransactionSigner | None:
        return self.app_client.signer

    @signer.setter
    def signer(self, value: TransactionSigner) -> None:
        self.app_client.signer = value

    @property
    def suggested_params(self) -> algosdk.transaction.SuggestedParams | None:
        return self.app_client.suggested_params

    @suggested_params.setter
    def suggested_params(self, value: algosdk.transaction.SuggestedParams | None) -> None:
        self.app_client.suggested_params = value

    def get_global_state(self) -> GlobalState:
        """Returns the application's global state wrapped in a strongly typed class with options to format the stored value"""

        state = typing.cast(dict[bytes, bytes | int], self.app_client.get_global_state(raw=True))
        return GlobalState(state)

    def hello(
        self,
        *,
        name: str,
        transaction_parameters: algokit_utils.TransactionParameters | None = None,
    ) -> algokit_utils.ABITransactionResponse[str]:
        """Calls `hello(string)string` ABI method
        
        :param str name: The `name` ABI parameter
        :param algokit_utils.TransactionParameters transaction_parameters: (optional) Additional transaction parameters
        :returns algokit_utils.ABITransactionResponse[str]: The result of the transaction"""

        args = HelloArgs(
            name=name,
        )
        result = self.app_client.call(
            call_abi_method=args.method(),
            transaction_parameters=_convert_call_transaction_parameters(transaction_parameters),
            **_as_dict(args, convert_all=True),
        )
        return result

    def set_price(
        self,
        *,
        unitary_price: int,
        transaction_parameters: algokit_utils.TransactionParameters | None = None,
    ) -> algokit_utils.ABITransactionResponse[None]:
        """Calls `set_price(uint64)void` ABI method
        
        :param int unitary_price: The `unitary_price` ABI parameter
        :param algokit_utils.TransactionParameters transaction_parameters: (optional) Additional transaction parameters
        :returns algokit_utils.ABITransactionResponse[None]: The result of the transaction"""

        args = SetPriceArgs(
            unitary_price=unitary_price,
        )
        result = self.app_client.call(
            call_abi_method=args.method(),
            transaction_parameters=_convert_call_transaction_parameters(transaction_parameters),
            **_as_dict(args, convert_all=True),
        )
        return result

    def opt_in_to_asset(
        self,
        *,
        mbr: TransactionWithSigner,
        transaction_parameters: algokit_utils.TransactionParameters | None = None,
    ) -> algokit_utils.ABITransactionResponse[None]:
        """Calls `opt_in_to_asset(pay)void` ABI method
        
        :param TransactionWithSigner mbr: The `mbr` ABI parameter
        :param algokit_utils.TransactionParameters transaction_parameters: (optional) Additional transaction parameters
        :returns algokit_utils.ABITransactionResponse[None]: The result of the transaction"""

        args = OptInToAssetArgs(
            mbr=mbr,
        )
        result = self.app_client.call(
            call_abi_method=args.method(),
            transaction_parameters=_convert_call_transaction_parameters(transaction_parameters),
            **_as_dict(args, convert_all=True),
        )
        return result

    def buy(
        self,
        *,
        quantity: int,
        buy_txn: TransactionWithSigner,
        transaction_parameters: algokit_utils.TransactionParameters | None = None,
    ) -> algokit_utils.ABITransactionResponse[None]:
        """Calls `buy(uint64,pay)void` ABI method
        
        :param int quantity: The `quantity` ABI parameter
        :param TransactionWithSigner buy_txn: The `buy_txn` ABI parameter
        :param algokit_utils.TransactionParameters transaction_parameters: (optional) Additional transaction parameters
        :returns algokit_utils.ABITransactionResponse[None]: The result of the transaction"""

        args = BuyArgs(
            quantity=quantity,
            buy_txn=buy_txn,
        )
        result = self.app_client.call(
            call_abi_method=args.method(),
            transaction_parameters=_convert_call_transaction_parameters(transaction_parameters),
            **_as_dict(args, convert_all=True),
        )
        return result

    def create_create_app(
        self,
        *,
        asset: int,
        unitary_price: int,
        on_complete: typing.Literal["no_op"] = "no_op",
        transaction_parameters: algokit_utils.CreateTransactionParameters | None = None,
    ) -> algokit_utils.ABITransactionResponse[None]:
        """Calls `create_app(asset,uint64)void` ABI method
        
        :param int asset: The `asset` ABI parameter
        :param int unitary_price: The `unitary_price` ABI parameter
        :param typing.Literal[no_op] on_complete: On completion type to use
        :param algokit_utils.CreateTransactionParameters transaction_parameters: (optional) Additional transaction parameters
        :returns algokit_utils.ABITransactionResponse[None]: The result of the transaction"""

        args = CreateAppArgs(
            asset=asset,
            unitary_price=unitary_price,
        )
        result = self.app_client.create(
            call_abi_method=args.method(),
            transaction_parameters=_convert_create_transaction_parameters(transaction_parameters, on_complete),
            **_as_dict(args, convert_all=True),
        )
        return result

    def delete_delete_app(
        self,
        *,
        transaction_parameters: algokit_utils.TransactionParameters | None = None,
    ) -> algokit_utils.ABITransactionResponse[None]:
        """Calls `delete_app()void` ABI method
        
        :param algokit_utils.TransactionParameters transaction_parameters: (optional) Additional transaction parameters
        :returns algokit_utils.ABITransactionResponse[None]: The result of the transaction"""

        args = DeleteAppArgs()
        result = self.app_client.delete(
            call_abi_method=args.method(),
            transaction_parameters=_convert_transaction_parameters(transaction_parameters),
            **_as_dict(args, convert_all=True),
        )
        return result

    def clear_state(
        self,
        transaction_parameters: algokit_utils.TransactionParameters | None = None,
        app_args: list[bytes] | None = None,
    ) -> algokit_utils.TransactionResponse:
        """Calls the application with on completion set to ClearState
    
        :param algokit_utils.TransactionParameters transaction_parameters: (optional) Additional transaction parameters
        :param list[bytes] | None app_args: (optional) Application args to pass
        :returns algokit_utils.TransactionResponse: The result of the transaction"""
    
        return self.app_client.clear_state(_convert_transaction_parameters(transaction_parameters), app_args)

    def deploy(
        self,
        version: str | None = None,
        *,
        signer: TransactionSigner | None = None,
        sender: str | None = None,
        allow_update: bool | None = None,
        allow_delete: bool | None = None,
        on_update: algokit_utils.OnUpdate = algokit_utils.OnUpdate.Fail,
        on_schema_break: algokit_utils.OnSchemaBreak = algokit_utils.OnSchemaBreak.Fail,
        template_values: algokit_utils.TemplateValueMapping | None = None,
        create_args: DeployCreate[CreateAppArgs],
        update_args: algokit_utils.DeployCallArgs | None = None,
        delete_args: Deploy[DeleteAppArgs],
    ) -> algokit_utils.DeployResponse:
        """Deploy an application and update client to reference it.
        
        Idempotently deploy (create, update/delete if changed) an app against the given name via the given creator
        account, including deploy-time template placeholder substitutions.
        To understand the architecture decisions behind this functionality please see
        <https://github.com/algorandfoundation/algokit-cli/blob/main/docs/architecture-decisions/2023-01-12_smart-contract-deployment.md>
        
        ```{note}
        If there is a breaking state schema change to an existing app (and `on_schema_break` is set to
        'ReplaceApp' the existing app will be deleted and re-created.
        ```
        
        ```{note}
        If there is an update (different TEAL code) to an existing app (and `on_update` is set to 'ReplaceApp')
        the existing app will be deleted and re-created.
        ```
        
        :param str version: version to use when creating or updating app, if None version will be auto incremented
        :param algosdk.atomic_transaction_composer.TransactionSigner signer: signer to use when deploying app
        , if None uses self.signer
        :param str sender: sender address to use when deploying app, if None uses self.sender
        :param bool allow_delete: Used to set the `TMPL_DELETABLE` template variable to conditionally control if an app
        can be deleted
        :param bool allow_update: Used to set the `TMPL_UPDATABLE` template variable to conditionally control if an app
        can be updated
        :param OnUpdate on_update: Determines what action to take if an application update is required
        :param OnSchemaBreak on_schema_break: Determines what action to take if an application schema requirements
        has increased beyond the current allocation
        :param dict[str, int|str|bytes] template_values: Values to use for `TMPL_*` template variables, dictionary keys
        should *NOT* include the TMPL_ prefix
        :param DeployCreate[CreateAppArgs] create_args: Arguments used when creating an application
        :param algokit_utils.DeployCallArgs | None update_args: Arguments used when updating an application
        :param Deploy[DeleteAppArgs] delete_args: Arguments used when deleting an application
        :return DeployResponse: details action taken and relevant transactions
        :raises DeploymentError: If the deployment failed"""

        return self.app_client.deploy(
            version,
            signer=signer,
            sender=sender,
            allow_update=allow_update,
            allow_delete=allow_delete,
            on_update=on_update,
            on_schema_break=on_schema_break,
            template_values=template_values,
            create_args=_convert_deploy_args(create_args),
            update_args=_convert_deploy_args(update_args),
            delete_args=_convert_deploy_args(delete_args),
        )

    def compose(self, atc: AtomicTransactionComposer | None = None) -> Composer:
        return Composer(self.app_client, atc or AtomicTransactionComposer())
