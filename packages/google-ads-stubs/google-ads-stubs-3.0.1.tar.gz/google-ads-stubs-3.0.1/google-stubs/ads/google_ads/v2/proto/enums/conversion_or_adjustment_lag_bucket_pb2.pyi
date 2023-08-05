# @generated by generate_proto_mypy_stubs.py.  Do not edit!
import sys
from google.protobuf.descriptor import (
    Descriptor as google___protobuf___descriptor___Descriptor,
    EnumDescriptor as google___protobuf___descriptor___EnumDescriptor,
)

from google.protobuf.message import Message as google___protobuf___message___Message

from typing import (
    List as typing___List,
    Tuple as typing___Tuple,
    Union as typing___Union,
    cast as typing___cast,
)

builtin___bytes = bytes
builtin___int = int
builtin___str = str
if sys.version_info < (3,):
    builtin___buffer = buffer
    builtin___unicode = unicode

class ConversionOrAdjustmentLagBucketEnum(google___protobuf___message___Message):
    DESCRIPTOR: google___protobuf___descriptor___Descriptor = ...
    class ConversionOrAdjustmentLagBucket(builtin___int):
        DESCRIPTOR: google___protobuf___descriptor___EnumDescriptor = ...
        @classmethod
        def Name(cls, number: builtin___int) -> builtin___str: ...
        @classmethod
        def Value(
            cls, name: builtin___str
        ) -> "ConversionOrAdjustmentLagBucketEnum.ConversionOrAdjustmentLagBucket": ...
        @classmethod
        def keys(cls) -> typing___List[builtin___str]: ...
        @classmethod
        def values(
            cls,
        ) -> typing___List[
            "ConversionOrAdjustmentLagBucketEnum.ConversionOrAdjustmentLagBucket"
        ]: ...
        @classmethod
        def items(
            cls,
        ) -> typing___List[
            typing___Tuple[
                builtin___str,
                "ConversionOrAdjustmentLagBucketEnum.ConversionOrAdjustmentLagBucket",
            ]
        ]: ...
        UNSPECIFIED = typing___cast(
            "ConversionOrAdjustmentLagBucketEnum.ConversionOrAdjustmentLagBucket", 0
        )
        UNKNOWN = typing___cast(
            "ConversionOrAdjustmentLagBucketEnum.ConversionOrAdjustmentLagBucket", 1
        )
        CONVERSION_LESS_THAN_ONE_DAY = typing___cast(
            "ConversionOrAdjustmentLagBucketEnum.ConversionOrAdjustmentLagBucket", 2
        )
        CONVERSION_ONE_TO_TWO_DAYS = typing___cast(
            "ConversionOrAdjustmentLagBucketEnum.ConversionOrAdjustmentLagBucket", 3
        )
        CONVERSION_TWO_TO_THREE_DAYS = typing___cast(
            "ConversionOrAdjustmentLagBucketEnum.ConversionOrAdjustmentLagBucket", 4
        )
        CONVERSION_THREE_TO_FOUR_DAYS = typing___cast(
            "ConversionOrAdjustmentLagBucketEnum.ConversionOrAdjustmentLagBucket", 5
        )
        CONVERSION_FOUR_TO_FIVE_DAYS = typing___cast(
            "ConversionOrAdjustmentLagBucketEnum.ConversionOrAdjustmentLagBucket", 6
        )
        CONVERSION_FIVE_TO_SIX_DAYS = typing___cast(
            "ConversionOrAdjustmentLagBucketEnum.ConversionOrAdjustmentLagBucket", 7
        )
        CONVERSION_SIX_TO_SEVEN_DAYS = typing___cast(
            "ConversionOrAdjustmentLagBucketEnum.ConversionOrAdjustmentLagBucket", 8
        )
        CONVERSION_SEVEN_TO_EIGHT_DAYS = typing___cast(
            "ConversionOrAdjustmentLagBucketEnum.ConversionOrAdjustmentLagBucket", 9
        )
        CONVERSION_EIGHT_TO_NINE_DAYS = typing___cast(
            "ConversionOrAdjustmentLagBucketEnum.ConversionOrAdjustmentLagBucket", 10
        )
        CONVERSION_NINE_TO_TEN_DAYS = typing___cast(
            "ConversionOrAdjustmentLagBucketEnum.ConversionOrAdjustmentLagBucket", 11
        )
        CONVERSION_TEN_TO_ELEVEN_DAYS = typing___cast(
            "ConversionOrAdjustmentLagBucketEnum.ConversionOrAdjustmentLagBucket", 12
        )
        CONVERSION_ELEVEN_TO_TWELVE_DAYS = typing___cast(
            "ConversionOrAdjustmentLagBucketEnum.ConversionOrAdjustmentLagBucket", 13
        )
        CONVERSION_TWELVE_TO_THIRTEEN_DAYS = typing___cast(
            "ConversionOrAdjustmentLagBucketEnum.ConversionOrAdjustmentLagBucket", 14
        )
        CONVERSION_THIRTEEN_TO_FOURTEEN_DAYS = typing___cast(
            "ConversionOrAdjustmentLagBucketEnum.ConversionOrAdjustmentLagBucket", 15
        )
        CONVERSION_FOURTEEN_TO_TWENTY_ONE_DAYS = typing___cast(
            "ConversionOrAdjustmentLagBucketEnum.ConversionOrAdjustmentLagBucket", 16
        )
        CONVERSION_TWENTY_ONE_TO_THIRTY_DAYS = typing___cast(
            "ConversionOrAdjustmentLagBucketEnum.ConversionOrAdjustmentLagBucket", 17
        )
        CONVERSION_THIRTY_TO_FORTY_FIVE_DAYS = typing___cast(
            "ConversionOrAdjustmentLagBucketEnum.ConversionOrAdjustmentLagBucket", 18
        )
        CONVERSION_FORTY_FIVE_TO_SIXTY_DAYS = typing___cast(
            "ConversionOrAdjustmentLagBucketEnum.ConversionOrAdjustmentLagBucket", 19
        )
        CONVERSION_SIXTY_TO_NINETY_DAYS = typing___cast(
            "ConversionOrAdjustmentLagBucketEnum.ConversionOrAdjustmentLagBucket", 20
        )
        ADJUSTMENT_LESS_THAN_ONE_DAY = typing___cast(
            "ConversionOrAdjustmentLagBucketEnum.ConversionOrAdjustmentLagBucket", 21
        )
        ADJUSTMENT_ONE_TO_TWO_DAYS = typing___cast(
            "ConversionOrAdjustmentLagBucketEnum.ConversionOrAdjustmentLagBucket", 22
        )
        ADJUSTMENT_TWO_TO_THREE_DAYS = typing___cast(
            "ConversionOrAdjustmentLagBucketEnum.ConversionOrAdjustmentLagBucket", 23
        )
        ADJUSTMENT_THREE_TO_FOUR_DAYS = typing___cast(
            "ConversionOrAdjustmentLagBucketEnum.ConversionOrAdjustmentLagBucket", 24
        )
        ADJUSTMENT_FOUR_TO_FIVE_DAYS = typing___cast(
            "ConversionOrAdjustmentLagBucketEnum.ConversionOrAdjustmentLagBucket", 25
        )
        ADJUSTMENT_FIVE_TO_SIX_DAYS = typing___cast(
            "ConversionOrAdjustmentLagBucketEnum.ConversionOrAdjustmentLagBucket", 26
        )
        ADJUSTMENT_SIX_TO_SEVEN_DAYS = typing___cast(
            "ConversionOrAdjustmentLagBucketEnum.ConversionOrAdjustmentLagBucket", 27
        )
        ADJUSTMENT_SEVEN_TO_EIGHT_DAYS = typing___cast(
            "ConversionOrAdjustmentLagBucketEnum.ConversionOrAdjustmentLagBucket", 28
        )
        ADJUSTMENT_EIGHT_TO_NINE_DAYS = typing___cast(
            "ConversionOrAdjustmentLagBucketEnum.ConversionOrAdjustmentLagBucket", 29
        )
        ADJUSTMENT_NINE_TO_TEN_DAYS = typing___cast(
            "ConversionOrAdjustmentLagBucketEnum.ConversionOrAdjustmentLagBucket", 30
        )
        ADJUSTMENT_TEN_TO_ELEVEN_DAYS = typing___cast(
            "ConversionOrAdjustmentLagBucketEnum.ConversionOrAdjustmentLagBucket", 31
        )
        ADJUSTMENT_ELEVEN_TO_TWELVE_DAYS = typing___cast(
            "ConversionOrAdjustmentLagBucketEnum.ConversionOrAdjustmentLagBucket", 32
        )
        ADJUSTMENT_TWELVE_TO_THIRTEEN_DAYS = typing___cast(
            "ConversionOrAdjustmentLagBucketEnum.ConversionOrAdjustmentLagBucket", 33
        )
        ADJUSTMENT_THIRTEEN_TO_FOURTEEN_DAYS = typing___cast(
            "ConversionOrAdjustmentLagBucketEnum.ConversionOrAdjustmentLagBucket", 34
        )
        ADJUSTMENT_FOURTEEN_TO_TWENTY_ONE_DAYS = typing___cast(
            "ConversionOrAdjustmentLagBucketEnum.ConversionOrAdjustmentLagBucket", 35
        )
        ADJUSTMENT_TWENTY_ONE_TO_THIRTY_DAYS = typing___cast(
            "ConversionOrAdjustmentLagBucketEnum.ConversionOrAdjustmentLagBucket", 36
        )
        ADJUSTMENT_THIRTY_TO_FORTY_FIVE_DAYS = typing___cast(
            "ConversionOrAdjustmentLagBucketEnum.ConversionOrAdjustmentLagBucket", 37
        )
        ADJUSTMENT_FORTY_FIVE_TO_SIXTY_DAYS = typing___cast(
            "ConversionOrAdjustmentLagBucketEnum.ConversionOrAdjustmentLagBucket", 38
        )
        ADJUSTMENT_SIXTY_TO_NINETY_DAYS = typing___cast(
            "ConversionOrAdjustmentLagBucketEnum.ConversionOrAdjustmentLagBucket", 39
        )
        ADJUSTMENT_NINETY_TO_ONE_HUNDRED_AND_FORTY_FIVE_DAYS = typing___cast(
            "ConversionOrAdjustmentLagBucketEnum.ConversionOrAdjustmentLagBucket", 40
        )
        CONVERSION_UNKNOWN = typing___cast(
            "ConversionOrAdjustmentLagBucketEnum.ConversionOrAdjustmentLagBucket", 41
        )
        ADJUSTMENT_UNKNOWN = typing___cast(
            "ConversionOrAdjustmentLagBucketEnum.ConversionOrAdjustmentLagBucket", 42
        )
    UNSPECIFIED = typing___cast(
        "ConversionOrAdjustmentLagBucketEnum.ConversionOrAdjustmentLagBucket", 0
    )
    UNKNOWN = typing___cast(
        "ConversionOrAdjustmentLagBucketEnum.ConversionOrAdjustmentLagBucket", 1
    )
    CONVERSION_LESS_THAN_ONE_DAY = typing___cast(
        "ConversionOrAdjustmentLagBucketEnum.ConversionOrAdjustmentLagBucket", 2
    )
    CONVERSION_ONE_TO_TWO_DAYS = typing___cast(
        "ConversionOrAdjustmentLagBucketEnum.ConversionOrAdjustmentLagBucket", 3
    )
    CONVERSION_TWO_TO_THREE_DAYS = typing___cast(
        "ConversionOrAdjustmentLagBucketEnum.ConversionOrAdjustmentLagBucket", 4
    )
    CONVERSION_THREE_TO_FOUR_DAYS = typing___cast(
        "ConversionOrAdjustmentLagBucketEnum.ConversionOrAdjustmentLagBucket", 5
    )
    CONVERSION_FOUR_TO_FIVE_DAYS = typing___cast(
        "ConversionOrAdjustmentLagBucketEnum.ConversionOrAdjustmentLagBucket", 6
    )
    CONVERSION_FIVE_TO_SIX_DAYS = typing___cast(
        "ConversionOrAdjustmentLagBucketEnum.ConversionOrAdjustmentLagBucket", 7
    )
    CONVERSION_SIX_TO_SEVEN_DAYS = typing___cast(
        "ConversionOrAdjustmentLagBucketEnum.ConversionOrAdjustmentLagBucket", 8
    )
    CONVERSION_SEVEN_TO_EIGHT_DAYS = typing___cast(
        "ConversionOrAdjustmentLagBucketEnum.ConversionOrAdjustmentLagBucket", 9
    )
    CONVERSION_EIGHT_TO_NINE_DAYS = typing___cast(
        "ConversionOrAdjustmentLagBucketEnum.ConversionOrAdjustmentLagBucket", 10
    )
    CONVERSION_NINE_TO_TEN_DAYS = typing___cast(
        "ConversionOrAdjustmentLagBucketEnum.ConversionOrAdjustmentLagBucket", 11
    )
    CONVERSION_TEN_TO_ELEVEN_DAYS = typing___cast(
        "ConversionOrAdjustmentLagBucketEnum.ConversionOrAdjustmentLagBucket", 12
    )
    CONVERSION_ELEVEN_TO_TWELVE_DAYS = typing___cast(
        "ConversionOrAdjustmentLagBucketEnum.ConversionOrAdjustmentLagBucket", 13
    )
    CONVERSION_TWELVE_TO_THIRTEEN_DAYS = typing___cast(
        "ConversionOrAdjustmentLagBucketEnum.ConversionOrAdjustmentLagBucket", 14
    )
    CONVERSION_THIRTEEN_TO_FOURTEEN_DAYS = typing___cast(
        "ConversionOrAdjustmentLagBucketEnum.ConversionOrAdjustmentLagBucket", 15
    )
    CONVERSION_FOURTEEN_TO_TWENTY_ONE_DAYS = typing___cast(
        "ConversionOrAdjustmentLagBucketEnum.ConversionOrAdjustmentLagBucket", 16
    )
    CONVERSION_TWENTY_ONE_TO_THIRTY_DAYS = typing___cast(
        "ConversionOrAdjustmentLagBucketEnum.ConversionOrAdjustmentLagBucket", 17
    )
    CONVERSION_THIRTY_TO_FORTY_FIVE_DAYS = typing___cast(
        "ConversionOrAdjustmentLagBucketEnum.ConversionOrAdjustmentLagBucket", 18
    )
    CONVERSION_FORTY_FIVE_TO_SIXTY_DAYS = typing___cast(
        "ConversionOrAdjustmentLagBucketEnum.ConversionOrAdjustmentLagBucket", 19
    )
    CONVERSION_SIXTY_TO_NINETY_DAYS = typing___cast(
        "ConversionOrAdjustmentLagBucketEnum.ConversionOrAdjustmentLagBucket", 20
    )
    ADJUSTMENT_LESS_THAN_ONE_DAY = typing___cast(
        "ConversionOrAdjustmentLagBucketEnum.ConversionOrAdjustmentLagBucket", 21
    )
    ADJUSTMENT_ONE_TO_TWO_DAYS = typing___cast(
        "ConversionOrAdjustmentLagBucketEnum.ConversionOrAdjustmentLagBucket", 22
    )
    ADJUSTMENT_TWO_TO_THREE_DAYS = typing___cast(
        "ConversionOrAdjustmentLagBucketEnum.ConversionOrAdjustmentLagBucket", 23
    )
    ADJUSTMENT_THREE_TO_FOUR_DAYS = typing___cast(
        "ConversionOrAdjustmentLagBucketEnum.ConversionOrAdjustmentLagBucket", 24
    )
    ADJUSTMENT_FOUR_TO_FIVE_DAYS = typing___cast(
        "ConversionOrAdjustmentLagBucketEnum.ConversionOrAdjustmentLagBucket", 25
    )
    ADJUSTMENT_FIVE_TO_SIX_DAYS = typing___cast(
        "ConversionOrAdjustmentLagBucketEnum.ConversionOrAdjustmentLagBucket", 26
    )
    ADJUSTMENT_SIX_TO_SEVEN_DAYS = typing___cast(
        "ConversionOrAdjustmentLagBucketEnum.ConversionOrAdjustmentLagBucket", 27
    )
    ADJUSTMENT_SEVEN_TO_EIGHT_DAYS = typing___cast(
        "ConversionOrAdjustmentLagBucketEnum.ConversionOrAdjustmentLagBucket", 28
    )
    ADJUSTMENT_EIGHT_TO_NINE_DAYS = typing___cast(
        "ConversionOrAdjustmentLagBucketEnum.ConversionOrAdjustmentLagBucket", 29
    )
    ADJUSTMENT_NINE_TO_TEN_DAYS = typing___cast(
        "ConversionOrAdjustmentLagBucketEnum.ConversionOrAdjustmentLagBucket", 30
    )
    ADJUSTMENT_TEN_TO_ELEVEN_DAYS = typing___cast(
        "ConversionOrAdjustmentLagBucketEnum.ConversionOrAdjustmentLagBucket", 31
    )
    ADJUSTMENT_ELEVEN_TO_TWELVE_DAYS = typing___cast(
        "ConversionOrAdjustmentLagBucketEnum.ConversionOrAdjustmentLagBucket", 32
    )
    ADJUSTMENT_TWELVE_TO_THIRTEEN_DAYS = typing___cast(
        "ConversionOrAdjustmentLagBucketEnum.ConversionOrAdjustmentLagBucket", 33
    )
    ADJUSTMENT_THIRTEEN_TO_FOURTEEN_DAYS = typing___cast(
        "ConversionOrAdjustmentLagBucketEnum.ConversionOrAdjustmentLagBucket", 34
    )
    ADJUSTMENT_FOURTEEN_TO_TWENTY_ONE_DAYS = typing___cast(
        "ConversionOrAdjustmentLagBucketEnum.ConversionOrAdjustmentLagBucket", 35
    )
    ADJUSTMENT_TWENTY_ONE_TO_THIRTY_DAYS = typing___cast(
        "ConversionOrAdjustmentLagBucketEnum.ConversionOrAdjustmentLagBucket", 36
    )
    ADJUSTMENT_THIRTY_TO_FORTY_FIVE_DAYS = typing___cast(
        "ConversionOrAdjustmentLagBucketEnum.ConversionOrAdjustmentLagBucket", 37
    )
    ADJUSTMENT_FORTY_FIVE_TO_SIXTY_DAYS = typing___cast(
        "ConversionOrAdjustmentLagBucketEnum.ConversionOrAdjustmentLagBucket", 38
    )
    ADJUSTMENT_SIXTY_TO_NINETY_DAYS = typing___cast(
        "ConversionOrAdjustmentLagBucketEnum.ConversionOrAdjustmentLagBucket", 39
    )
    ADJUSTMENT_NINETY_TO_ONE_HUNDRED_AND_FORTY_FIVE_DAYS = typing___cast(
        "ConversionOrAdjustmentLagBucketEnum.ConversionOrAdjustmentLagBucket", 40
    )
    CONVERSION_UNKNOWN = typing___cast(
        "ConversionOrAdjustmentLagBucketEnum.ConversionOrAdjustmentLagBucket", 41
    )
    ADJUSTMENT_UNKNOWN = typing___cast(
        "ConversionOrAdjustmentLagBucketEnum.ConversionOrAdjustmentLagBucket", 42
    )
    global___ConversionOrAdjustmentLagBucket = ConversionOrAdjustmentLagBucket
    def __init__(self,) -> None: ...
    if sys.version_info >= (3,):
        @classmethod
        def FromString(
            cls, s: builtin___bytes
        ) -> ConversionOrAdjustmentLagBucketEnum: ...
    else:
        @classmethod
        def FromString(
            cls, s: typing___Union[builtin___bytes, builtin___buffer, builtin___unicode]
        ) -> ConversionOrAdjustmentLagBucketEnum: ...
    def MergeFrom(self, other_msg: google___protobuf___message___Message) -> None: ...
    def CopyFrom(self, other_msg: google___protobuf___message___Message) -> None: ...

global___ConversionOrAdjustmentLagBucketEnum = ConversionOrAdjustmentLagBucketEnum
