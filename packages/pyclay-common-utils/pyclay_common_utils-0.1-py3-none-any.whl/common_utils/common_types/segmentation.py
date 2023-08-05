from __future__ import annotations
from typing import List
import numpy as np
import cv2
from shapely.geometry import Point as ShapelyPoint
from shapely.geometry.polygon import Polygon as ShapelyPolygon
from shapely.ops import cascaded_union
from imgaug.augmentables.polys import Polygon as ImgAugPolygon, PolygonsOnImage as ImgAugPolygons

from logger import logger

from .constants import number_types
from ..check_utils import check_type, check_type_from_list, check_value
from ..utils import get_class_string

from .point import Point, Point2D_List
from .bbox import BBox

class Polygon:
    def __init__(self, points: list, dimensionality: int=2):
        check_type(item=points, valid_type_list=[list])
        check_type_from_list(item_list=points, valid_type_list=number_types)
        check_type(item=dimensionality, valid_type_list=[int])
        if len(points) % dimensionality != 0:
            logger.error(f"len(points) is not divisible by dimensionality={dimensionality}")
            raise Exception

        self.points = points
        self.dimensionality = dimensionality

    def __str__(self):
        return f"{get_class_string(self)}: {self.points}"

    def __repr__(self):
        return self.__str__()
    
    @classmethod
    def buffer(self, polygon: Polygon) -> Polygon:
        return polygon

    def copy(self) -> Polygon:
        return Polygon(points=self.points, dimensionality=self.dimensionality)

    def to_int(self) -> Polygon:
        return Polygon(points=[int(val) for val in self.points], dimensionality=self.dimensionality)

    def to_float(self) -> Polygon:
        return Polygon(points=[float(val) for val in self.points], dimensionality=self.dimensionality)

    def to_list(self, demarcation: bool=False) -> list:
        if demarcation:
            return np.array(self.points).reshape(-1, self.dimensionality).tolist()
        else:
            return self.points

    def to_point_list(self) -> list:
        return [Point(coords=coords) for coords in self.to_list(demarcation=True)]

    def to_shapely(self) -> ShapelyPolygon:
        return ShapelyPolygon(self.to_list(demarcation=True))

    def to_contour(self) -> np.ndarray:
        return np.array(self.to_int().to_list()).reshape(-1, 1, self.dimensionality)

    def to_bbox(self) -> BBox:
        points = np.array(self.to_list(demarcation=True))
        xmin, ymin = points.min(axis=0)
        xmax, ymax = points.max(axis=0)
        return BBox(xmin=xmin, ymin=ymin, xmax=xmax, ymax=ymax)

    def area(self) -> float:
        return self.to_shapely().area
    
    def centroid(self) -> Point:
        return Point.from_shapely(self.to_shapely().centroid)

    def contains_point(self, point: Point) -> bool:
        return self.to_shapely().contains(point.to_shapely())

    def contains_polygon(self, polygon: Polygon) -> bool:
        return self.to_shapely().contains(polygon.to_shapely())

    def contains_bbox(self, bbox: BBox) -> bool:
        return self.to_shapely().contains(bbox.to_shapely())

    def contains(self, obj) -> bool:
        check_type(item=obj, valid_type_list=[Point, Polygon, BBox])
        return self.to_shapely().contains(obj.to_shapely())

    def within_polygon(self, polygon: Polygon) -> bool:
        return self.to_shapely().within(polygon.to_shapely())

    def within_bbox(self, bbox: BBox) -> bool:
        return self.to_shapely().within(bbox.to_shapely())

    def within(self, obj) -> bool:
        check_type(item=obj, valid_type_list=[Polygon, BBox])
        return self.to_shapely().within(obj.to_shapely())

    def intersects_polygon(self, polygon: Polygon) -> bool:
        return self.to_shapely().intersects(polygon)

    def size(self) -> tuple:
        return np.array(self.points).reshape(-1, self.dimensionality).shape

    def resize(self, orig_frame_shape: list, new_frame_shape: list) -> Polygon:
        if self.dimensionality != 2:
            logger.error(f"Only resize of dimensionality 2 is supported at this time.")
            logger.error(f"This polygon is dimensionality: {self.dimensionality}")
            raise Exception
        orig_frame_h, orig_frame_w = orig_frame_shape[:2]
        new_frame_h, new_frame_w = new_frame_shape[:2]
        h_scale = new_frame_h / orig_frame_h
        w_scale = new_frame_w / orig_frame_w
        new_point_list = []
        for point in self.to_point_list():
            point = Point.buffer(point)
            [x, y] = point.coords
            x *= w_scale
            y *= h_scale
            new_point = Point([x, y])
            new_point_list.append(new_point)
        return Polygon.from_point_list(point_list=new_point_list, dimensionality=2)

    @classmethod
    def from_list(self, points: list, dimensionality: int=2, demarcation: bool=False) -> Polygon:
        if demarcation:
            flattened_list = np.array(points).reshape(-1).tolist()
            return Polygon(points=flattened_list, dimensionality=dimensionality)
        else:
            return Polygon(points=points, dimensionality=dimensionality)

    @classmethod
    def from_point_list(self, point_list: list, dimensionality: int=2) -> Polygon:
        check_type_from_list(item_list=point_list, valid_type_list=[Point])
        result = []
        for i, point in enumerate(point_list):
            numpy_array = np.array(point.to_list())
            if numpy_array.shape != (dimensionality,):
                logger.error(f"Found point at index {i} of point_list with a shape of {numpy_array.shape} != {(dimensionality,)}")
                raise Exception
            result.extend(point.to_list())
        return Polygon(points=result, dimensionality=dimensionality)

    @classmethod
    def from_shapely(self, shapely_polygon: ShapelyPolygon) -> Polygon:
        vals_tuple = shapely_polygon.exterior.coords.xy
        numpy_array = np.array(vals_tuple).T[:-1]
        flattened_list = numpy_array.reshape(-1).tolist()
        dimensionality = numpy_array.shape[1]
        return Polygon(points=flattened_list, dimensionality=dimensionality)

    @classmethod
    def from_contour(self, contour: np.ndarray) -> Polygon:
        cont = contour.reshape(contour.shape[0], contour.shape[2]).tolist()
        return self.from_list(points=cont, dimensionality=2, demarcation=True)

    @classmethod
    def from_polygon_list_to_merge(self, polygon_list: list) -> Polygon:
        from shapely.geometry import MultiPolygon as ShapelyMultiPolygon
        import matplotlib.pyplot as plt
        import geopandas as gpd

        valid_polygon_list = []
        for polygon in polygon_list:
            if polygon.size()[0] > 2: # Filter out polygons with less than 3 vertices.
                valid_polygon_list.append(polygon)
        # logger.red(valid_polygon_list)
        merged_polygon = None
        for i, valid_polygon in enumerate(valid_polygon_list):
            if merged_polygon is None:
                merged_polygon = valid_polygon.to_shapely()
                logger.yellow(f"{i+1}/{len(valid_polygon_list)}: type(merged_polygon): {type(merged_polygon)}")
            else:
                if merged_polygon.intersects(valid_polygon.to_shapely()):
                    logger.green(f"intersects!")
                else:
                    logger.red(f"Not intersects!")
                if type(merged_polygon) is ShapelyPolygon:
                    logger.cyan(f"Flag0")
                    polygons = gpd.GeoSeries(merged_polygon)
                    new_polygon = gpd.GeoSeries(valid_polygon.to_shapely())
                    polygons.plot()
                    new_polygon.plot()
                    plt.show()
                    if not merged_polygon.is_valid:
                        logger.error(f"merged_polygon is not valid")
                        raise Exception
                    if not valid_polygon.to_shapely().is_valid:
                        logger.error(f"New polygon is not valid")
                        raise Exception
                    if merged_polygon.intersects(valid_polygon.to_shapely()):
                        merged_polygon = merged_polygon.union(valid_polygon.to_shapely())
                    else:
                        merged_polygon = cascaded_union([merged_polygon, valid_polygon.to_shapely()])
                    if type(merged_polygon) is ShapelyMultiPolygon:
                        logger.cyan(f"Hull")
                        merged_polygon = merged_polygon.convex_hull
                        if type(merged_polygon) is ShapelyPolygon:
                            logger.green(f"Fixed!")
                        elif type(merged_polygon) is ShapelyMultiPolygon:
                            logger.error(f"Not Fixed!")
                            raise Exception
                        else:
                            logger.error(f"Unknown type: {type(merged_polygon)}")
                            raise Exception
                elif type(merged_polygon) is ShapelyMultiPolygon:
                    logger.error(f"Polygon turned into MultiPolygon in shapely!")
                    raise Exception
                else:
                    logger.error(f"type(merged_polygon): {type(merged_polygon)}")
                    raise Exception

                logger.yellow(f"{i+1}/{len(valid_polygon_list)}: type(merged_polygon): {type(merged_polygon)}")
                # logger.yellow(f"{i+1}/{len(valid_polygon_list)}: type(merged_polygon.exterior): {type(merged_polygon.exterior)}")
            logger.blue(f"{i+1}/{len(valid_polygon_list)}: valid_polygon.size(): {valid_polygon.size()}")

        import sys
        sys.exit()
        union = cascaded_union([valid_polygon.to_shapely() for valid_polygon in valid_polygon_list])
        return self.from_shapely(union)

    def to_imgaug(self) -> ImgAugPolygon:
        if self.dimensionality == 2:
            return ImgAugPolygon(self.to_list(demarcation=True))
        else:
            raise NotImplementedError

    @classmethod
    def from_imgaug(cls, imgaug_polygon: ImgAugPolygon) -> Polygon:
        return Polygon.from_shapely(imgaug_polygon.to_shapely_polygon())

    def to_point2d_list(self) -> Point2D_List:
        return Point2D_List.from_list(self.to_list(demarcation=True))

    @classmethod
    def from_point2d_list(cls, point2d_list: Point2D_List) -> Polygon:
        check_type(point2d_list, valid_type_list=[Point2D_List])
        return Polygon.from_list(
            points=point2d_list.to_list(demarcation=True),
            dimensionality=2,
            demarcation=True
        )
    
class Segmentation:
    def __init__(self, polygon_list: list=None):
        if polygon_list is not None:
            check_type(item=polygon_list, valid_type_list=[list])
            check_type_from_list(item_list=polygon_list, valid_type_list=[Polygon])
            for i, polygon in enumerate(polygon_list):
                if polygon.dimensionality != 2:
                    logger.error(f"Found polygon of dimensionality {polygon.dimensionality} at index {i}")
                    logger.error(f"All polygons must be of dimensionality 2.")
                    raise Exception
            self.polygon_list = polygon_list
        else:
            self.polygon_list = []

    def __str__(self):
        return f"{get_class_string(self)}: {self.polygon_list}"

    def __repr__(self):
        return self.__str__()

    def __len__(self) -> int:
        return len(self.polygon_list)

    def __getitem__(self, idx: int) -> Polygon:
        if len(self.polygon_list) == 0:
            logger.error(f"polygon_list is empty.")
            raise IndexError
        elif idx < 0 or idx >= len(self.polygon_list):
            logger.error(f"Index out of range: {idx}")
            raise IndexError
        else:
            return self.polygon_list[idx]

    def __setitem__(self, idx: int, value: Polygon):
        check_type(value, valid_type_list=[Polygon])
        self.polygon_list[idx] = value

    def __iter__(self):
        self.n = 0
        return self

    def __next__(self) -> Polygon:
        if self.n < len(self.polygon_list):
            result = self.polygon_list[self.n]
            self.n += 1
            return result
        else:
            raise StopIteration

    @classmethod
    def buffer(self, segmentation: Segmentation) -> Segmentation:
        return segmentation

    def copy(self) -> Segmentation:
        return Segmentation(polygon_list=self.polygon_list)

    def append(self, item: Polygon):
        check_type(item, valid_type_list=[Polygon])
        self.polygon_list.append(item)

    def to_int(self) -> Segmentation:
        return Segmentation([polygon.to_int() for polygon in self])

    def to_float(self) -> Segmentation:
        return Segmentation([polygon.to_float() for polygon in self])

    def to_list(self, demarcation: bool=False) -> list:
        return [polygon.to_list(demarcation=demarcation) for polygon in self]

    def to_point_list(self) -> list:
        return [polygon.to_point_list() for polygon in self]

    def to_shapely(self) -> list:
        return [polygon.to_shapely() for polygon in self]

    def to_contour(self) -> list: # combine?
        return [polygon.to_contour() for polygon in self]

    def to_bbox(self) -> BBox:
        seg_bbox_list = [polygon.to_bbox() for polygon in self]
        seg_bbox_xmin = min([seg_bbox.xmin for seg_bbox in seg_bbox_list])
        seg_bbox_ymin = min([seg_bbox.ymin for seg_bbox in seg_bbox_list])
        seg_bbox_xmax = max([seg_bbox.xmax for seg_bbox in seg_bbox_list])
        seg_bbox_ymax = max([seg_bbox.ymax for seg_bbox in seg_bbox_list])
        result_bbox = BBox(xmin=seg_bbox_xmin, ymin=seg_bbox_ymin, xmax=seg_bbox_xmax, ymax=seg_bbox_ymax)
        return result_bbox

    def area(self) -> float:
        return sum([polygon.area() for polygon in self])
    
    def centroid(self) -> Point:
        poly_dim_valid = [polygon.dimensionality == 2 for polygon in self]
        if False in poly_dim_valid:
            logger.error(f'Found polygon of dimensionality != 2 in segmentation.')
            logger.error(f'Dimensionalities found: {[polygon.dimensionality for polygon in self]}')
            logger.error(f'Cannot calculate centroid.')
            raise Exception
        poly_c = [polygon.centroid() for polygon in self]
        poly_a = [polygon.area() for polygon in self]
        cxa = [c.coords[0] * a for c, a in zip(poly_c, poly_a)]
        cya = [c.coords[1] * a for c, a in zip(poly_c, poly_a)]
        sum_cxa, sum_cya, sum_a = sum(cxa), sum(cya), sum(poly_a)
        calc_cx, calc_cy = sum_cxa / sum_a, sum_cya / sum_a
        return Point(coords=[calc_cx, calc_cy])

    def contains_point(self, point: Point) -> bool:
        return any([polygon.contains_point() for polygon in self])

    def contains_polygon(self, polygon: Polygon) -> bool:
        return any([polygon.contains_polygon() for polygon in self])

    def contains_bbox(self, bbox: BBox) -> bool:
        return any([polygon.contains_bbox() for polygon in self])

    def contains(self, obj) -> bool:
        check_type(item=obj, valid_type_list=[Point, Polygon, BBox])
        return any([polygon.contains() for polygon in self])

    def within_polygon(self, polygon: Polygon) -> bool:
        return all([polygon.within_polygon() for polygon in self])

    def within_bbox(self, bbox: BBox) -> bool:
        return all([polygon.within_bbox(bbox) for polygon in self])

    def within(self, obj) -> bool:
        check_type(item=obj, valid_type_list=[Polygon, BBox])
        if type(obj) is BBox: # necessary?
            bbox_contains_seg = None
            for polygon in self:
                if len(polygon.to_list(demarcation=True)) < 3:
                    continue
                poly_in_bbox = obj.contains(polygon)
                bbox_contains_seg = bbox_contains_seg and poly_in_bbox if bbox_contains_seg is not None else poly_in_bbox
            bbox_contains_seg = bbox_contains_seg if bbox_contains_seg is not None else False
            return bbox_contains_seg
        elif type(obj) is Polygon: # necessary?
            poly_contains_seg = None
            for polygon in self:
                if len(polygon.to_list(demarcation=True)) < 3:
                    continue
                poly_in_poly = obj.contains(polygon)
                poly_contains_seg = poly_contains_seg and poly_in_poly if poly_contains_seg is not None else poly_in_poly
            poly_contains_seg = poly_contains_seg if poly_contains_seg is not None else False
            return poly_contains_seg
        return all([polygon.within(obj) for polygon in self])

    def merge(self) -> Segmentation:
        return Segmentation(
            polygon_list=[Polygon.from_polygon_list_to_merge(
                polygon_list=self.polygon_list
            )]
        )

    def resize(self, orig_frame_shape: list, new_frame_shape: list) -> Segmentation:
        new_polygon_list = []
        for polygon in self:
            polygon = Polygon.buffer(polygon)
            new_polygon = polygon.resize(
                orig_frame_shape=orig_frame_shape, new_frame_shape=new_frame_shape
            )
            new_polygon_list.append(new_polygon)
        return Segmentation(polygon_list=new_polygon_list)

    @classmethod
    def from_list(self, points_list: list, demarcation: bool=False) -> Segmentation:
        return Segmentation(
            polygon_list=[
                Polygon.from_list(
                    points=points, dimensionality=2, demarcation=demarcation
                ) for points in points_list
            ]
        )

    @classmethod
    def from_point_list(self, point_list_list: list) -> Segmentation:
        return Segmentation(
            polygon_list=[
                Polygon.from_point_list(
                    point_list=point_list, dimensionality=2
                ) for point_list in point_list_list
            ]
        )

    @classmethod
    def from_shapely(self, shapely_polygon_list: list) -> Segmentation:
        return Segmentation(
            polygon_list=[
                Polygon.from_shapely(
                    shapely_polygon=shapely_polygon
                ) for shapely_polygon in shapely_polygon_list
            ]
        )

    @classmethod
    def from_contour(self, contour_list: list) -> Segmentation:
        return Segmentation(
            polygon_list=[
                Polygon.from_contour(
                    contour=contour
                ) for contour in contour_list
            ]
        )

    def to_imgaug(self, img_shape: np.ndarray) -> ImgAugPolygons:
        return ImgAugPolygons(
            polygons=[poly.to_imgaug() for poly in self.polygon_list],
            shape=img_shape
        )

    @classmethod
    def from_imgaug(cls, imgaug_polygons: ImgAugPolygons) -> Segmentation:
        return Segmentation(
            polygon_list=[Polygon.from_imgaug(imgaug_polygon) for imgaug_polygon in imgaug_polygons.polygons]
        )

    def to_point2d_list_list(self) -> List[Point2D_List]:
        return [polygon.to_point2d_list() for polygon in self]

    @classmethod
    def from_point2d_list_list(cls, point2d_list_list: List[Point2D_List]) -> Segmentation:
        return Segmentation(
            polygon_list=[Polygon.from_point2d_list(point2d_list) for point2d_list in point2d_list_list]
        )