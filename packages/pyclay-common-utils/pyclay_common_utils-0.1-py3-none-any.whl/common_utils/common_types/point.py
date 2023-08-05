from __future__ import annotations
from typing import List
import numpy as np
from shapely.geometry import Point as ShapelyPoint

from logger import logger

from .constants import number_types
from ..check_utils import check_type, check_type_from_list, check_list_length
from ..utils import get_class_string

class Point:
    def __init__(self, coords: list):
        check_type(item=coords, valid_type_list=[list])
        check_type_from_list(item_list=coords, valid_type_list=number_types)
        self.coords = coords
        self.dimensionality = len(coords)

    def __str__(self):
        return f"{get_class_string(self)}: {self.coords}"

    def __repr__(self):
        return self.__str__()

    @classmethod
    def buffer(self, point: Point) -> Point:
        return point

    def copy(self) -> Point:
        return Point(coords=self.coords)

    def to_int(self) -> Point:
        return Point(coords=[int(val) for val in self.coords])

    def to_float(self) -> Point:
        return Point(coords=[float(val) for val in self.coords])

    def to_list(self) -> list:
        return self.coords

    def to_shapely(self) -> ShapelyPoint:
        return ShapelyPoint(self.to_list())

    @classmethod
    def from_list(self, coords: list) -> Point:
        return Point(coords=coords)

    @classmethod
    def from_shapely(self, shapely_point: ShapelyPoint) -> Point:
        return Point(coords=[list(val)[0] for val in shapely_point.coords.xy])

    def within(self, obj) -> bool:
        return self.to_shapely().within(obj.to_shapely())

class Point2D:
    def __init__(self, x: float, y: float):
        self.x = x
        self.y = y

    def __str__(self):
        return f"Point2D({self.x},{self.y})"

    def __repr__(self):
        return self.__str__()

    def to_list(self) -> list:
        return [self.x, self.y]

    @classmethod
    def from_list(cls, coords: list) -> Point2D:
        check_list_length(coords, correct_length=2)
        return Point2D(x=coords[0], y=coords[1])

    def to_numpy(self) -> np.ndarray:
        return np.array(self.to_list())

    @classmethod
    def from_numpy(cls, arr: np.ndarray) -> Point2D:
        if arr.shape != (2,):
            logger.error(f'Expected shape: (2,), got {arr.shape} instead.')
            raise Exception
        return cls.from_list(arr.tolist())

    def to_shapely(self) -> ShapelyPoint:
        return ShapelyPoint(self.to_list())

    @classmethod
    def from_shapely(self, shapely_point: ShapelyPoint) -> Point2D:
        return Point2D.from_list(coords=[list(val)[0] for val in shapely_point.coords.xy])

    def within(self, obj) -> bool:
        return self.to_shapely().within(obj.to_shapely())

class Point2D_List:
    def __init__(self, point_list: List[Point2D]):
        check_type_from_list(point_list, valid_type_list=[Point2D])
        self.point_list = point_list

    def __str__(self) -> str:
        return str(self.to_list(demarcation=True))

    def __repr__(self) -> str:
        return self.__str__()

    def __len__(self) -> int:
        return len(self.point_list)

    def __getitem__(self, idx: int) -> Point2D:
        if len(self.point_list) == 0:
            logger.error(f"Point2D_List is empty.")
            raise IndexError
        elif idx < 0 or idx >= len(self.point_list):
            logger.error(f"Index out of range: {idx}")
            raise IndexError
        else:
            return self.point_list[idx]

    def __setitem__(self, idx: int, value: Point2D):
        check_type(value, valid_type_list=[Point2D])
        self.point_list[idx] = value

    def __iter__(self):
        self.n = 0
        return self

    def __next__(self) -> Point2D:
        if self.n < len(self.point_list):
            result = self.point_list[self.n]
            self.n += 1
            return result
        else:
            raise StopIteration

    def to_numpy(self, demarcation: bool=True) -> np.ndarray:
        if demarcation:
            return np.array([point.to_list() for point in self])
        else:
            return np.array([point.to_list() for point in self]).reshape(-1)

    @classmethod
    def from_numpy(cls, arr: np.ndarray, demarcation: bool=True) -> Point2D_List:
        if demarcation:
            if arr.shape[-1] != 2:
                logger.error(f"arr.shape[-1] != 2")
                logger.error(f'arr.shape: {arr.shape}')
                raise Exception
            return Point2D_List(
                point_list=[Point2D.from_numpy(arr_part) for arr_part in arr]
            )
        else:
            if len(arr.shape) != 1:
                logger.error(f"Expecting flat array when demarcation=False")
                logger.error(f"arr.shape: {arr.shape}")
                raise Exception
            elif arr.shape[0] % 2 != 0:
                logger.error(f"arr.shape[0] % 2 == {arr.shape[0]} % 2 == {arr.shape[0] % 2} != 0")
                raise Exception
            return Point2D_List(
                point_list=[Point2D.from_numpy(arr_part) for arr_part in arr.reshape(-1, 2)]
            )

    def to_list(self, demarcation: bool=True) -> list:
        return self.to_numpy(demarcation=demarcation).tolist()

    @classmethod
    def from_list(cls, value_list: list, demarcation: bool=True) -> Point2D_List:
        return cls.from_numpy(arr=np.array(value_list), demarcation=demarcation)

    def to_shapely_list(self) -> List[ShapelyPoint]:
        return [point.to_shapely() for point in self]

    @classmethod
    def from_shapely(self, shapely_point_list: List[ShapelyPoint]) -> Point2D_List:
        return Point2D_List(point_list=[Point2D.from_shapely(shapely_point) for shapely_point in shapely_point_list])

    def within(self, obj) -> bool:
        if len(self) == 0:
            return False
        for point in self:
            if not point.within(obj):
                return False
        return True

class Point3D:
    def __init__(self, x: float, y: float, z: float):
        self.x = x
        self.y = y
        self.z = z

    def __str__(self):
        return f"Point3D({self.x},{self.y},{self.z})"

    def __repr__(self):
        return self.__str__()

    def to_list(self) -> list:
        return [self.x, self.y, self.z]

    @classmethod
    def from_list(cls, coords: list) -> Point3D:
        check_list_length(coords, correct_length=3)
        return Point3D(x=coords[0], y=coords[1], z=coords[2])