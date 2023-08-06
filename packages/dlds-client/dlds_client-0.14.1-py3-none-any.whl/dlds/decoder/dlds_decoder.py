#  Copyright (c) 2020 Data Spree UG (haftungsbeschraenkt) - All Rights Reserved
#  Unauthorized copying of this file, via any medium is strictly prohibited.
#  Proprietary and confidential.

from abc import ABC, abstractmethod

from typing import Dict, List


class DLDSDecoder(ABC):
    def __init__(self) -> None:
        super().__init__()

    @abstractmethod
    def __call__(self, encoded_bytes):
        """
        Stub for implementing the decoding procedure
        called:
        >>> decoder = DLDSDecoder()
        >>> decoder(encoded_bytes)

        :return Decoded data.
        """
        pass

    @staticmethod
    @abstractmethod
    def get_file_extensions() -> List[str]:
        """
        Stub for returning allowed file endings
        """
        pass

    def __reduce__(self):
        return (DLDSDecoder, tuple(),)
#
# class DefaultDecoder(DLDSDecoder):
#     def __init__(self) -> None:
#         super().__init__()
#
#     def __call__(self, serialized_file):
#         return serialized_file
#
#     def get_file_extensions(self) -> List[str]:
#         return ['all']
